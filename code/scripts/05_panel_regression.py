"""
05_panel_regression.py
======================
Canonical regression pipeline for the thesis analysis.

This script consumes the shared estimation frame from panel_utils so the
reported sample, transformations, and covariance assumptions are explicit.
"""

from __future__ import annotations

import os
import warnings

import pandas as pd
import statsmodels.api as sm

from panel_utils import (
    OUTPUT_DIR,
    build_regression_frame,
    load_panel,
    model_pvalues,
    model_std_errors,
    sample_summary,
    significance_stars,
    write_sample_definition_report,
    write_stage_manifest,
)

os.makedirs(OUTPUT_DIR, exist_ok=True)
warnings.filterwarnings("ignore", category=RuntimeWarning, module=r"linearmodels\..*")

MODEL_VARS = [
    "facility_age_years",
    "capacity_100t",
    "capacity_utilization_capped",
    "heating_value_mj_kg",
    "grid_ef_kgco2_kwh",
]


def load_regression_frame():
    """Load the enriched panel and build the shared regression frame."""
    panel = load_panel()
    regression = build_regression_frame(panel)
    summary = sample_summary(panel)

    print(f"Regression frame: {len(regression):,} obs")
    print(f"  Facilities: {regression['analysis_facility_id'].nunique():,}")
    print(f"  Years: FY{regression['fiscal_year'].min()}-FY{regression['fiscal_year'].max()}")
    print(
        "  Within/total ratio (log-efficiency): "
        f"{summary['regression_within_total_ratio']:.4f}"
    )

    return panel, regression, summary


def descriptive_stats(regression):
    """Table 1: Summary statistics on the canonical regression frame."""
    print("\n" + "=" * 60)
    print("TABLE 1: Summary Statistics (Regression Frame)")
    print("=" * 60)

    desc_vars = {
        "energy_efficiency_mwh_per_t": "Efficiency (MWh/t, winsorized)",
        "log_efficiency": "log(Efficiency)",
        "facility_age_years": "Facility Age (years)",
        "capacity_t_day": "Capacity (t/day)",
        "capacity_utilization_capped": "Capacity Utilization",
        "heating_value_mj_kg": "Heating Value (MJ/kg)",
        "grid_ef_kgco2_kwh": "Grid EF (kg-CO2/kWh)",
    }

    rows = []
    for var, label in desc_vars.items():
        s = regression[var].dropna()
        rows.append(
            {
                "Variable": label,
                "N": len(s),
                "Mean": f"{s.mean():.3f}",
                "Median": f"{s.median():.3f}",
                "SD": f"{s.std():.3f}",
                "Min": f"{s.min():.3f}",
                "Max": f"{s.max():.3f}",
            }
        )

    desc_df = pd.DataFrame(rows)
    print(desc_df.to_string(index=False))

    path = os.path.join(OUTPUT_DIR, "table1_summary_stats.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("# Table 1: Summary Statistics (Canonical Regression Frame)\n\n")
        f.write(desc_df.to_markdown(index=False))
        f.write(
            "\n\n"
            "*Note: heating value is a noisy administrative estimate derived from the "
            "source files and retained as a control variable rather than interpreted "
            "as a clean engineering measurement.*\n"
        )
    print(f"\n  Saved: {path}")

    return path


def efficiency_by_age_group(regression):
    """Table 2: Efficiency by age group on the regression frame."""
    print("\n" + "=" * 60)
    print("TABLE 2: Efficiency by Facility Age Group")
    print("=" * 60)

    grouped = regression.copy()
    grouped["age_group"] = pd.cut(
        grouped["facility_age_years"],
        bins=[0, 10, 20, 30, 100],
        labels=["0-10 yrs", "10-20 yrs", "20-30 yrs", "30+ yrs"],
        right=False,
    )

    table = grouped.groupby("age_group", observed=True).agg(
        n_obs=("energy_efficiency_mwh_per_t", "count"),
        mean_eff=("energy_efficiency_mwh_per_t", "mean"),
        median_eff=("energy_efficiency_mwh_per_t", "median"),
        mean_capacity=("capacity_t_day", "mean"),
        mean_avoided=("avoided_co2_t", "mean"),
        total_avoided=("avoided_co2_t", "sum"),
    ).reset_index()
    total_avoided = grouped["avoided_co2_t"].sum()
    table["pct_of_total_avoided"] = (
        table["total_avoided"] / total_avoided * 100
    ).round(1)
    table = table.drop(columns=["total_avoided"])

    print(table.to_string(index=False))

    path = os.path.join(OUTPUT_DIR, "table2_efficiency_by_age.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write("# Table 2: Energy Recovery Efficiency by Facility Age Group\n\n")
        f.write(table.to_markdown(index=False))
    print(f"\n  Saved: {path}")

    return path


def run_pooled_ols(regression):
    """Model 1: Pooled OLS with facility-clustered standard errors."""
    print("\n" + "=" * 60)
    print("MODEL 1: Pooled OLS (clustered by facility)")
    print("=" * 60)

    y = regression["log_efficiency"]
    X = sm.add_constant(regression[MODEL_VARS])

    model = sm.OLS(y, X).fit(
        cov_type="cluster",
        cov_kwds={"groups": regression["analysis_facility_id"]},
    )
    print(model.summary())
    return model


def run_ols_with_year_fe(regression):
    """Model 2: OLS with year fixed effects and clustered SEs."""
    print("\n" + "=" * 60)
    print("MODEL 2: OLS with Year Fixed Effects")
    print("=" * 60)

    y = regression["log_efficiency"]
    year_dummies = pd.get_dummies(
        regression["fiscal_year"],
        prefix="fy",
        drop_first=True,
        dtype=float,
    )
    X = sm.add_constant(pd.concat([regression[MODEL_VARS], year_dummies], axis=1))

    model = sm.OLS(y, X).fit(
        cov_type="cluster",
        cov_kwds={"groups": regression["analysis_facility_id"]},
    )
    print(f"  R-squared: {model.rsquared:.4f}")
    print(f"  Adj R-squared: {model.rsquared_adj:.4f}")
    print(f"  N: {int(model.nobs):,}")
    return model


def _fit_random_effects(regression, include_year_fe):
    """Shared RE estimator helper."""
    from linearmodels.panel import RandomEffects

    pdata = regression.set_index(["analysis_facility_id", "fiscal_year"])
    X = pdata[MODEL_VARS].copy()
    if include_year_fe:
        year_dummies = pd.get_dummies(
            pdata.index.get_level_values("fiscal_year"),
            prefix="fy",
            drop_first=True,
            dtype=float,
        )
        year_dummies.index = pdata.index
        X = pd.concat([X, year_dummies], axis=1)
    X = sm.add_constant(X)

    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            category=RuntimeWarning,
            module=r"linearmodels\..*",
        )
        return RandomEffects(pdata["log_efficiency"], X).fit(
            cov_type="clustered",
            cluster_entity=True,
        )


def run_random_effects(regression):
    """Model 3: Random effects with clustered SEs."""
    print("\n" + "=" * 60)
    print("MODEL 3: Random Effects")
    print("=" * 60)
    model = _fit_random_effects(regression, include_year_fe=False)
    print(f"  R-squared: {float(model.rsquared):.4f}")
    print(f"  N: {int(model.nobs):,}")
    for var in MODEL_VARS:
        coef = float(model.params[var])
        se = float(model_std_errors(model)[var])
        p = float(model_pvalues(model)[var])
        print(f"  {var:<28} {coef:>8.4f}  SE={se:>7.4f}  p={p:>7.4f}")
    return model


def run_random_effects_with_year_fe(regression):
    """Model 4: Random effects plus year dummies, clustered by facility."""
    print("\n" + "=" * 60)
    print("MODEL 4: Random Effects + Year Fixed Effects")
    print("=" * 60)
    model = _fit_random_effects(regression, include_year_fe=True)
    print(f"  R-squared: {float(model.rsquared):.4f}")
    print(f"  N: {int(model.nobs):,}")
    for var in MODEL_VARS:
        coef = float(model.params[var])
        se = float(model_std_errors(model)[var])
        p = float(model_pvalues(model)[var])
        print(f"  {var:<28} {coef:>8.4f}  SE={se:>7.4f}  p={p:>7.4f}")
    return model


def comparison_table(models, regression, sample_report_path):
    """Write a markdown comparison table for the four main models."""
    print("\n" + "=" * 60)
    print("MODEL COMPARISON")
    print("=" * 60)

    labels = [
        "Model 1 (Pooled OLS)",
        "Model 2 (Year FE)",
        "Model 3 (RE)",
        "Model 4 (Year FE + RE)",
    ]
    path = os.path.join(OUTPUT_DIR, "regression_results.md")

    with open(path, "w", encoding="utf-8") as f:
        f.write("# Regression Results: Determinants of Energy Recovery Efficiency\n\n")
        f.write("DV: winsorized log(MWh per tonne processed)\n\n")
        f.write(
            f"Canonical regression frame: {len(regression):,} observations across "
            f"{regression['analysis_facility_id'].nunique():,} facilities.\n\n"
        )
        f.write(f"Sample definition: `{os.path.basename(sample_report_path)}`\n\n")
        f.write("| Variable | " + " | ".join(labels) + " |\n")
        f.write("|:---------|" + "|".join([":--------------------:"] * 4) + "|\n")

        for var in MODEL_VARS:
            row = [var]
            for model in models:
                coef = float(model.params[var])
                p = float(model_pvalues(model)[var])
                row.append(f"{coef:.4f}{significance_stars(p)}")
            f.write("| " + " | ".join(row) + " |\n")

            se_row = ["SE"]
            for model in models:
                se = float(model_std_errors(model)[var])
                se_row.append(f"({se:.4f})")
            f.write("| " + " | ".join(se_row) + " |\n")

        f.write(
            "| Observations | "
            + " | ".join([f"{int(model.nobs):,}" for model in models])
            + " |\n"
        )
        f.write(
            "| Facilities | "
            + " | ".join([f"{regression['analysis_facility_id'].nunique():,}"] * 4)
            + " |\n"
        )
        f.write(
            "| R-squared | "
            + " | ".join([f"{float(model.rsquared):.4f}" for model in models])
            + " |\n"
        )

    print(f"  Saved: {path}")
    return path


def main():
    panel, regression, summary = load_regression_frame()

    sample_report_path = os.path.join(OUTPUT_DIR, "sample_definition.md")
    write_sample_definition_report(sample_report_path, summary)
    print(f"Sample report: {sample_report_path}")

    summary_stats_path = descriptive_stats(regression)
    age_table_path = efficiency_by_age_group(regression)
    m1 = run_pooled_ols(regression)
    m2 = run_ols_with_year_fe(regression)
    m3 = run_random_effects(regression)
    m4 = run_random_effects_with_year_fe(regression)
    results_path = comparison_table([m1, m2, m3, m4], regression, sample_report_path)

    manifest_path = write_stage_manifest(
        "05_panel_regression",
        inputs=["data/processed/incineration_panel_enriched.csv"],
        outputs=[
            "output/sample_definition.md",
            "output/table1_summary_stats.md",
            "output/table2_efficiency_by_age.md",
            "output/regression_results.md",
        ],
        metadata={
            "regression_obs": summary["regression_obs"],
            "regression_facilities": summary["regression_facilities"],
            "within_total_ratio": summary["regression_within_total_ratio"],
            "pre_fukushima_within_total_ratio": summary["pre_fukushima_within_total_ratio"],
            "post_fukushima_within_total_ratio": summary["post_fukushima_within_total_ratio"],
            "outputs": {
                "sample_report": os.path.basename(sample_report_path),
                "summary_stats": os.path.basename(summary_stats_path),
                "age_table": os.path.basename(age_table_path),
                "regression_results": os.path.basename(results_path),
            },
        },
    )
    print(f"Manifest: {manifest_path}")

    print("\n" + "=" * 60)
    print("REGRESSION COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
