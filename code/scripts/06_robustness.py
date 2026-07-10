"""
06_robustness.py
=================
Robustness checks built from the shared regression frame.

Specifications:
1. Early coded-window pooled OLS
2. Early coded-window OLS with year FE
3. Later coded-window pooled OLS
4. Later coded-window OLS with year FE
5. Small capacity tercile (pooled OLS)
6. Large capacity tercile (pooled OLS)
7. Raw DV pooled OLS
8. Raw DV OLS with year FE
9. Within-between correlated-RE-style OLS with year FE
"""

from __future__ import annotations

import os

import numpy as np
import pandas as pd
import statsmodels.api as sm

from panel_utils import (
    OUTPUT_DIR,
    build_regression_frame,
    load_panel,
    significance_stars,
    write_stage_manifest,
)

os.makedirs(OUTPUT_DIR, exist_ok=True)

CORE_IVS = [
    "facility_age_years",
    "capacity_100t",
    "capacity_utilization_capped",
    "heating_value_mj_kg",
    "grid_ef_kgco2_kwh",
]
EARLY_CODED_END = 2009
LATER_CODED_START = 2013


def load_regression_frame():
    """Load the canonical regression frame."""
    frame = build_regression_frame(load_panel())
    print(f"Regression frame: {len(frame):,} obs across {frame['analysis_facility_id'].nunique():,} facilities")
    return frame


def run_ols(data, label, dv="log_efficiency", include_year_fe=False):
    """Run pooled OLS with facility-clustered SEs and return summary stats."""
    ivs = CORE_IVS
    reg = data[[dv, "analysis_facility_id", "fiscal_year"] + ivs].dropna().copy()
    if len(reg) < 50:
        print(f"  {label}: too few observations ({len(reg)}), skipping")
        return None

    y = reg[dv]
    X = reg[ivs].copy()
    if include_year_fe:
        year_dummies = pd.get_dummies(
            reg["fiscal_year"],
            prefix="fy",
            drop_first=True,
            dtype=float,
        )
        X = pd.concat([X, year_dummies], axis=1)
    X = sm.add_constant(X)

    model = sm.OLS(y, X).fit(
        cov_type="cluster",
        cov_kwds={"groups": reg["analysis_facility_id"]},
    )

    result = {
        "label": label,
        "n": int(model.nobs),
        "facilities": int(reg["analysis_facility_id"].nunique()),
        "r2": float(model.rsquared),
        "dv": dv,
        "year_fe": include_year_fe,
    }
    for var in ivs[:3]:
        result[f"{var}_coef"] = float(model.params[var])
        result[f"{var}_p"] = float(model.pvalues[var])

    print(f"\n  {label} (N={result['n']:,}, facilities={result['facilities']:,}, R²={result['r2']:.3f})")
    for var in ivs[:3]:
        coef = result[f"{var}_coef"]
        p = result[f"{var}_p"]
        print(f"    {var:<28} {coef:>8.4f} {significance_stars(p):>3}")

    return result


def run_within_between_ols(data, label, dv="log_efficiency", include_year_fe=True):
    """
    Run a within-between sensitivity that separates facility means from deviations.

    This is a reviewer-shield model rather than a new headline estimator. It
    asks whether the cross-facility structure behind the main random-effects
    reading remains visible after adding facility-level means and within-facility
    deviations for the same covariates.
    """
    reg = data[[dv, "analysis_facility_id", "fiscal_year"] + CORE_IVS].dropna().copy()
    if len(reg) < 50:
        print(f"  {label}: too few observations ({len(reg)}), skipping")
        return None

    means = reg.groupby("analysis_facility_id")[CORE_IVS].transform("mean")
    x_parts = []
    for var in CORE_IVS:
        reg[f"{var}_within"] = reg[var] - means[var]
        reg[f"{var}_between"] = means[var]
        x_parts.extend([f"{var}_within", f"{var}_between"])

    X = reg[x_parts].copy()
    if include_year_fe:
        year_dummies = pd.get_dummies(
            reg["fiscal_year"],
            prefix="fy",
            drop_first=True,
            dtype=float,
        )
        X = pd.concat([X, year_dummies], axis=1)
    X = sm.add_constant(X)

    model = sm.OLS(reg[dv], X).fit(
        cov_type="cluster",
        cov_kwds={"groups": reg["analysis_facility_id"]},
    )

    result = {
        "label": label,
        "n": int(model.nobs),
        "facilities": int(reg["analysis_facility_id"].nunique()),
        "r2": float(model.rsquared),
        "dv": dv,
        "year_fe": include_year_fe,
        "model_family": "within_between",
    }
    for var in CORE_IVS[:3]:
        between = f"{var}_between"
        within = f"{var}_within"
        result[f"{var}_coef"] = float(model.params[between])
        result[f"{var}_p"] = float(model.pvalues[between])
        result[f"{var}_between_coef"] = float(model.params[between])
        result[f"{var}_between_p"] = float(model.pvalues[between])
        result[f"{var}_within_coef"] = float(model.params[within])
        result[f"{var}_within_p"] = float(model.pvalues[within])

    print(f"\n  {label} (N={result['n']:,}, facilities={result['facilities']:,}, R²={result['r2']:.3f})")
    for var in CORE_IVS[:3]:
        b = result[f"{var}_between_coef"]
        bp = result[f"{var}_between_p"]
        w = result[f"{var}_within_coef"]
        wp = result[f"{var}_within_p"]
        print(
            f"    {var:<28} between={b:>8.4f}{significance_stars(bp):>3} "
            f"within={w:>8.4f}{significance_stars(wp):>3}"
        )

    return result


def main():
    frame = load_regression_frame()
    results = []

    print("=" * 60)
    print("TEST 1: Early/Later Coded Windows")
    print("=" * 60)
    pre = frame[frame["fiscal_year"] <= EARLY_CODED_END].copy()
    post = frame[frame["fiscal_year"] >= LATER_CODED_START].copy()
    for label, subset, year_fe in [
        (f"R1: Early coded-window pooled OLS (FY2005-FY{EARLY_CODED_END})", pre, False),
        (f"R2: Early coded-window year FE (FY2005-FY{EARLY_CODED_END})", pre, True),
        (f"R3: Later coded-window pooled OLS (FY{LATER_CODED_START}-FY2024)", post, False),
        (f"R4: Later coded-window year FE (FY{LATER_CODED_START}-FY2024)", post, True),
    ]:
        result = run_ols(subset, label, include_year_fe=year_fe)
        if result:
            results.append(result)

    print("\n" + "=" * 60)
    print("TEST 2: Capacity Tercile Endpoints")
    print("=" * 60)
    terciles = pd.qcut(frame["capacity_t_day"], 3, labels=["Small", "Medium", "Large"])
    for label, subset in [
        ("R5: Small capacity tercile", frame[terciles == "Small"].copy()),
        ("R6: Large capacity tercile", frame[terciles == "Large"].copy()),
    ]:
        result = run_ols(subset, label, include_year_fe=False)
        if result:
            results.append(result)

    print("\n" + "=" * 60)
    print("TEST 3: Raw Dependent Variable")
    print("=" * 60)
    for label, year_fe in [
        ("R7: Raw DV pooled OLS", False),
        ("R8: Raw DV year FE", True),
    ]:
        result = run_ols(frame, label, dv="energy_efficiency_mwh_per_t", include_year_fe=year_fe)
        if result:
            results.append(result)

    print("\n" + "=" * 60)
    print("TEST 4: Within-Between Correlated-RE-Style Sensitivity")
    print("=" * 60)
    result = run_within_between_ols(
        frame,
        "R9: Within-between sensitivity with year FE",
        dv="log_efficiency",
        include_year_fe=True,
    )
    if result:
        results.append(result)

    df_results = pd.DataFrame(results)
    core_vars = [
        "facility_age_years",
        "capacity_100t",
        "capacity_utilization_capped",
    ]

    print("\n" + "=" * 60)
    print("ROBUSTNESS SUMMARY")
    print("=" * 60)
    print(f"\n{'Specification':<42} {'N':>6} {'R²':>6}", end="")
    for var in core_vars:
        print(f" {var[:12]:>14}", end="")
    print()
    print("-" * 112)

    for _, row in df_results.iterrows():
        print(f"{row['label']:<42} {row['n']:>6} {row['r2']:>6.3f}", end="")
        for var in core_vars:
            coef = row[f"{var}_coef"]
            p = row[f"{var}_p"]
            print(f" {coef:>11.4f}{significance_stars(p):<3}", end="")
        print()

    path = os.path.join(OUTPUT_DIR, "robustness_results.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("# Robustness Checks\n\n")
        f.write(
            "All models use the canonical identifiable generator frame and "
            "facility-clustered standard errors. Early/later coded-window checks "
            "avoid treating the FY2010-FY2012 official-code gap as a clean "
            "Fukushima identification split.\n\n"
        )
        f.write("| Specification | N | Facilities | R² | facility_age | capacity_100t | cap_utilization |\n")
        f.write("|:---|---:|---:|---:|---:|---:|---:|\n")
        for _, row in df_results.iterrows():
            f.write(
                f"| {row['label']} | {row['n']} | {row['facilities']} | {row['r2']:.3f} |"
            )
            for var in core_vars:
                coef = row[f"{var}_coef"]
                p = row[f"{var}_p"]
                f.write(f" {coef:.4f}{significance_stars(p)} |")
            f.write("\n")

        wb_rows = [
            row for _, row in df_results.iterrows()
            if row.get("model_family") == "within_between"
        ]
        if wb_rows:
            f.write(
                "\n## Within-between sensitivity\n\n"
                "The within-between sensitivity separates facility-level means "
                "from within-facility deviations. It is reported as a reviewer "
                "shield for the descriptive random-effects interpretation, not as "
                "a replacement for the main models.\n\n"
            )
            f.write("| Variable | Between-facility coefficient | Within-facility coefficient |\n")
            f.write("|:---|---:|---:|\n")
            row = wb_rows[0]
            for var in core_vars:
                bcoef = row[f"{var}_between_coef"]
                bp = row[f"{var}_between_p"]
                wcoef = row[f"{var}_within_coef"]
                wp = row[f"{var}_within_p"]
                f.write(
                    f"| {var} | {bcoef:.4f}{significance_stars(bp)} | "
                    f"{wcoef:.4f}{significance_stars(wp)} |\n"
                )
            f.write(
                "\n*Interpretation: the between-facility columns preserve the "
                "cross-facility structure emphasized in the main paper, while the "
                "within-facility columns show how limited within-panel movement "
                "maps onto the same variables.*\n"
            )

    print(f"\n  Saved: {path}")

    manifest_path = write_stage_manifest(
        "06_robustness",
        inputs=["data/processed/incineration_panel_enriched.csv"],
        outputs=["output/robustness_results.md"],
        metadata={
            "specifications": results,
            "early_coded_window": [2005, EARLY_CODED_END],
            "later_coded_window": [LATER_CODED_START, 2024],
        },
    )
    print(f"Manifest: {manifest_path}")


if __name__ == "__main__":
    main()
