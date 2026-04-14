"""
06_robustness.py
=================
Robustness checks built from the shared regression frame.

Specifications:
1. Pre-Fukushima pooled OLS
2. Pre-Fukushima OLS with year FE
3. Post-Fukushima pooled OLS
4. Post-Fukushima OLS with year FE
5. Small capacity tercile (pooled OLS)
6. Large capacity tercile (pooled OLS)
7. Raw DV pooled OLS
8. Raw DV OLS with year FE
"""

from __future__ import annotations

import os

import numpy as np
import pandas as pd
import statsmodels.api as sm

from panel_utils import (
    OUTPUT_DIR,
    POST_FUKUSHIMA_START,
    PRE_FUKUSHIMA_END,
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


def main():
    frame = load_regression_frame()
    results = []

    print("=" * 60)
    print("TEST 1: Pre/Post Fukushima")
    print("=" * 60)
    pre = frame[frame["fiscal_year"] <= PRE_FUKUSHIMA_END].copy()
    post = frame[frame["fiscal_year"] >= POST_FUKUSHIMA_START].copy()
    for label, subset, year_fe in [
        (f"R1: Pre-Fukushima pooled OLS (FY2005-FY{PRE_FUKUSHIMA_END})", pre, False),
        (f"R2: Pre-Fukushima year FE (FY2005-FY{PRE_FUKUSHIMA_END})", pre, True),
        (f"R3: Post-Fukushima pooled OLS (FY{POST_FUKUSHIMA_START}-FY2024)", post, False),
        (f"R4: Post-Fukushima year FE (FY{POST_FUKUSHIMA_START}-FY2024)", post, True),
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
        f.write("All models use the canonical regression frame and facility-clustered standard errors.\n\n")
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

    print(f"\n  Saved: {path}")

    manifest_path = write_stage_manifest(
        "06_robustness",
        inputs=["data/processed/incineration_panel_enriched.csv"],
        outputs=["output/robustness_results.md"],
        metadata={
            "specifications": results,
            "pre_fukushima_window": [2005, PRE_FUKUSHIMA_END],
            "post_fukushima_window": [POST_FUKUSHIMA_START, 2024],
        },
    )
    print(f"Manifest: {manifest_path}")


if __name__ == "__main__":
    main()
