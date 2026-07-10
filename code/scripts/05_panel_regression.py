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

import numpy as np
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
]

MAIN_MODEL_LABELS = [
    "Model 1 (Pooled OLS)",
    "Model 2 (Year indicators)",
    "Model 3 (RE)",
    "Model 4 (Year indicators + RE)",
]

TECHNOLOGY_CATEGORICALS = [
    "furnace_type_group",
    "operation_mode_group",
    "facility_type_group",
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
        "energy_efficiency_mwh_per_t": "Gross electricity generation (MWh/t, bounded)",
        "log_efficiency": "log(Bounded gross MWh/t)",
        "facility_age_years": "Facility Age (years)",
        "capacity_t_day": "Capacity (t/day)",
        "capacity_utilization_capped": "Capacity Utilization",
        "heating_value_mj_kg": "Heating Value (MJ/kg)",
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
    """Table 2: bounded gross MWh/t by age group on the regression frame."""
    print("\n" + "=" * 60)
    print("TABLE 2: Gross Electricity Generation per Tonne by Facility Age Group")
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
        f.write("# Table 2: Gross Electricity Generation per Tonne by Facility Age Group\n\n")
        f.write(table.to_markdown(index=False))
    print(f"\n  Saved: {path}")

    return path


def build_persistence_figure_data(regression):
    """Write data-backed age-group intervals and adjacent-year rank persistence."""
    frame = regression.copy()
    frame["age_group"] = pd.cut(
        frame["facility_age_years"],
        bins=[0, 10, 20, 30, 100],
        labels=["0-10 yrs", "10-20 yrs", "20-30 yrs", "30+ yrs"],
        right=False,
    )

    age_dummies = pd.get_dummies(frame["age_group"], dtype=float)
    mean_model = sm.OLS(frame["energy_efficiency_mwh_per_t"], age_dummies).fit(
        cov_type="cluster",
        cov_kwds={"groups": frame["analysis_facility_id"]},
    )
    age_counts = frame.groupby("age_group", observed=True).agg(
        observations=("energy_efficiency_mwh_per_t", "size"),
        facilities=("analysis_facility_id", "nunique"),
    )

    rows = []
    for label in age_dummies.columns:
        mean = float(mean_model.params[label])
        se = float(mean_model.bse[label])
        rows.append(
            {
                "record_type": "age_mean",
                "label": str(label),
                "value": mean,
                "ci_low": mean - 1.96 * se,
                "ci_high": mean + 1.96 * se,
                "observations": int(age_counts.loc[label, "observations"]),
                "facilities": int(age_counts.loc[label, "facilities"]),
                "year_start": np.nan,
                "year_end": np.nan,
            }
        )

    ranked = (
        frame.groupby(["analysis_facility_id", "fiscal_year"], as_index=False)[
            "log_efficiency"
        ].mean()
    )
    ranked["rank_pct"] = ranked.groupby("fiscal_year")["log_efficiency"].rank(
        pct=True,
        method="average",
    )
    current = ranked[["analysis_facility_id", "fiscal_year", "rank_pct"]].rename(
        columns={"fiscal_year": "year_start", "rank_pct": "rank_start"}
    )
    following = current.rename(
        columns={"year_start": "year_end", "rank_start": "rank_end"}
    )
    pairs = current.merge(following, on="analysis_facility_id", how="inner")
    pairs = pairs[pairs["year_end"].eq(pairs["year_start"] + 1)].copy()

    annual = (
        pairs.groupby(["year_start", "year_end"])
        .apply(
            lambda group: pd.Series(
                {
                    "value": group["rank_start"].corr(group["rank_end"]),
                    "observations": len(group),
                    "facilities": group["analysis_facility_id"].nunique(),
                }
            ),
            include_groups=False,
        )
        .reset_index()
    )
    for row in annual.itertuples(index=False):
        rows.append(
            {
                "record_type": "rank_correlation",
                "label": f"FY{int(row.year_start)}-{str(int(row.year_end))[-2:]}",
                "value": float(row.value),
                "ci_low": np.nan,
                "ci_high": np.nan,
                "observations": int(row.observations),
                "facilities": int(row.facilities),
                "year_start": int(row.year_start),
                "year_end": int(row.year_end),
            }
        )

    output = pd.DataFrame(rows)
    path = os.path.join(OUTPUT_DIR, "figure3_persistence.csv")
    output.to_csv(path, index=False, float_format="%.10g")

    summary = {
        "exact_adjacent_year_pairs": int(len(pairs)),
        "facilities": int(pairs["analysis_facility_id"].nunique()),
        "pooled_rank_correlation": float(pairs["rank_start"].corr(pairs["rank_end"])),
        "median_annual_rank_correlation": float(annual["value"].median()),
        "minimum_annual_rank_correlation": float(annual["value"].min()),
        "maximum_annual_rank_correlation": float(annual["value"].max()),
        "annual_transitions": int(len(annual)),
    }
    print(
        "Rank persistence: "
        f"pooled={summary['pooled_rank_correlation']:.3f}, "
        f"median annual={summary['median_annual_rank_correlation']:.3f}, "
        f"pairs={summary['exact_adjacent_year_pairs']:,}"
    )
    print(f"Saved: {path}")
    return path, summary


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


def build_technology_adjusted_design(regression):
    """Build the primary year-adjusted cross-facility design matrix."""
    year_dummies = pd.get_dummies(
        regression["fiscal_year"],
        prefix="fy",
        drop_first=True,
        dtype=float,
    )
    technology_dummies = pd.get_dummies(
        regression[TECHNOLOGY_CATEGORICALS],
        prefix=["furnace", "operation", "facility"],
        drop_first=True,
        dtype=float,
    )
    return sm.add_constant(
        pd.concat(
            [
                regression[MODEL_VARS],
                regression[["n_furnaces"]],
                technology_dummies,
                year_dummies,
            ],
            axis=1,
        )
    )


def run_primary_technology_adjusted_model(regression):
    """Primary RQ2 model: year-adjusted OLS with plant-configuration controls."""
    print("\n" + "=" * 60)
    print("PRIMARY RQ2 MODEL: YEAR + TECHNOLOGY ADJUSTED OLS")
    print("=" * 60)

    X = build_technology_adjusted_design(regression)
    model = sm.OLS(regression["log_efficiency"], X).fit(
        cov_type="cluster",
        cov_kwds={"groups": regression["analysis_facility_id"]},
    )
    print(f"  R-squared: {model.rsquared:.4f}")
    print(f"  Adj R-squared: {model.rsquared_adj:.4f}")
    print(f"  N: {int(model.nobs):,}")
    for var in MODEL_VARS:
        print(
            f"  {var:<28} {float(model.params[var]):>8.4f}  "
            f"SE={float(model.bse[var]):>7.4f}  p={float(model.pvalues[var]):>7.4f}"
        )
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


def comparison_table(
    models,
    primary_model,
    regression,
    sample_report_path,
    persistence_summary,
):
    """Write the primary RQ2 model and the supplemental estimator ladder."""
    print("\n" + "=" * 60)
    print("MODEL COMPARISON")
    print("=" * 60)

    path = os.path.join(OUTPUT_DIR, "regression_results.md")

    with open(path, "w", encoding="utf-8") as f:
        f.write("# Regression Results: Structured Electricity Recovery\n\n")
        f.write("DV: log of bounded gross electricity generation per tonne processed\n\n")
        f.write("All reported standard errors are clustered by facility.\n\n")
        f.write(
            f"Canonical regression frame: {len(regression):,} observations across "
            f"{regression['analysis_facility_id'].nunique():,} facilities.\n\n"
        )
        f.write(f"Sample definition: `{os.path.basename(sample_report_path)}`\n\n")
        f.write("## Primary RQ2 Specification\n\n")
        f.write(
            "The primary estimand is a year-adjusted cross-facility comparison: "
            "how gross MWh/t differs across generator age/vintage, scale, "
            "utilization, heating value, and observed plant-configuration profiles "
            "within common fiscal years. It is not a causal within-plant aging "
            "effect. Both columns use facility-clustered standard errors.\n\n"
        )
        f.write(
            "| Variable | Base year-adjusted model | Primary year + technology model |\n"
        )
        f.write("|:--|--:|--:|\n")
        base_model = models[1]
        for var in MODEL_VARS:
            base_p = float(model_pvalues(base_model)[var])
            primary_p = float(model_pvalues(primary_model)[var])
            f.write(
                f"| {var} | {float(base_model.params[var]):.4f}"
                f"{significance_stars(base_p)} "
                f"({float(model_std_errors(base_model)[var]):.4f}) | "
                f"{float(primary_model.params[var]):.4f}"
                f"{significance_stars(primary_p)} "
                f"({float(model_std_errors(primary_model)[var]):.4f}) |\n"
            )
        f.write(
            f"| Observations | {int(base_model.nobs):,} | "
            f"{int(primary_model.nobs):,} |\n"
        )
        f.write(
            f"| Facilities | {regression['analysis_facility_id'].nunique():,} | "
            f"{regression['analysis_facility_id'].nunique():,} |\n"
        )
        f.write(
            f"| R-squared | {float(base_model.rsquared):.4f} | "
            f"{float(primary_model.rsquared):.4f} |\n\n"
        )
        f.write(
            "Technology controls in the primary model are normalized furnace type, "
            "operating mode, facility type, and number of furnaces. Fiscal-year "
            "indicators are included in both columns.\n\n"
        )

        f.write("## Supplemental Estimator Ladder\n\n")
        f.write("| Variable | " + " | ".join(MAIN_MODEL_LABELS) + " |\n")
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
        f.write(
            "\n## Adjacent-Year Rank Persistence\n\n"
            f"- Exact adjacent-year facility pairs: {persistence_summary['exact_adjacent_year_pairs']:,}\n"
            f"- Facilities represented: {persistence_summary['facilities']:,}\n"
            f"- Pooled adjacent-year rank correlation: {persistence_summary['pooled_rank_correlation']:.4f}\n"
            f"- Median annual rank correlation: {persistence_summary['median_annual_rank_correlation']:.4f}\n"
            f"- Annual range: {persistence_summary['minimum_annual_rank_correlation']:.4f} to "
            f"{persistence_summary['maximum_annual_rank_correlation']:.4f}\n"
        )

    print(f"  Saved: {path}")
    return path


def serialize_main_models(models):
    """Return structured coefficient metadata for the four main models."""
    payload = {
        "labels": MAIN_MODEL_LABELS,
        "coefficients": {},
        "std_errors": {},
        "pvalues": {},
        "rsquared": [float(model.rsquared) for model in models],
        "observations": [int(model.nobs) for model in models],
    }

    for var in MODEL_VARS:
        payload["coefficients"][var] = [float(model.params[var]) for model in models]
        payload["std_errors"][var] = [float(model_std_errors(model)[var]) for model in models]
        payload["pvalues"][var] = [float(model_pvalues(model)[var]) for model in models]

    return payload


def serialize_primary_model(model):
    """Return structured metadata for the declared primary RQ2 model."""
    return {
        "label": "Year + technology adjusted OLS",
        "estimand": "year-adjusted cross-facility generator comparison",
        "technology_controls": [
            "furnace_type_group",
            "operation_mode_group",
            "facility_type_group",
            "n_furnaces",
        ],
        "coefficients": {var: float(model.params[var]) for var in MODEL_VARS},
        "std_errors": {
            var: float(model_std_errors(model)[var]) for var in MODEL_VARS
        },
        "pvalues": {var: float(model_pvalues(model)[var]) for var in MODEL_VARS},
        "rsquared": float(model.rsquared),
        "observations": int(model.nobs),
    }


def serialize_age_group_summary(path):
    """Read the age-group markdown table into structured metadata."""
    lines = [line.strip() for line in open(path, "r", encoding="utf-8")]
    data_lines = [
        line
        for line in lines
        if line.startswith("|")
        and not set(line.replace("|", "").replace(":", "").replace("-", "").strip()) == set()
    ]

    rows = {}
    for line in data_lines[1:]:
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) < 7:
            continue
        key = cells[0]
        rows[key] = {
            "n_obs": int(cells[1]),
            "mean_eff": float(cells[2]),
            "median_eff": float(cells[3]),
            "mean_capacity": float(cells[4]),
            "mean_avoided": float(cells[5]),
            "pct_of_total_avoided": float(cells[6]),
        }
    return rows


def main():
    panel, regression, summary = load_regression_frame()

    sample_report_path = os.path.join(OUTPUT_DIR, "sample_definition.md")
    write_sample_definition_report(sample_report_path, summary)
    print(f"Sample report: {sample_report_path}")

    summary_stats_path = descriptive_stats(regression)
    age_table_path = efficiency_by_age_group(regression)
    figure_data_path, persistence_summary = build_persistence_figure_data(regression)
    m1 = run_pooled_ols(regression)
    m2 = run_ols_with_year_fe(regression)
    m3 = run_random_effects(regression)
    m4 = run_random_effects_with_year_fe(regression)
    primary_model = run_primary_technology_adjusted_model(regression)
    models = [m1, m2, m3, m4]
    results_path = comparison_table(
        models,
        primary_model,
        regression,
        sample_report_path,
        persistence_summary,
    )

    manifest_path = write_stage_manifest(
        "05_panel_regression",
        inputs=["data/processed/incineration_panel_enriched.csv"],
        outputs=[
            "output/sample_definition.md",
            "output/table1_summary_stats.md",
            "output/table2_efficiency_by_age.md",
            "output/figure3_persistence.csv",
            "output/regression_results.md",
        ],
        metadata={
            "regression_obs": summary["regression_obs"],
            "regression_facilities": summary["regression_facilities"],
            "within_total_ratio": summary["regression_within_total_ratio"],
            "pre_fukushima_within_total_ratio": summary["pre_fukushima_within_total_ratio"],
            "post_fukushima_within_total_ratio": summary["post_fukushima_within_total_ratio"],
            "early_coded_window": [2005, 2009],
            "later_coded_window": [2013, 2024],
            "early_coded_within_total_ratio": summary["pre_fukushima_within_total_ratio"],
            "later_coded_within_total_ratio": summary["post_fukushima_within_total_ratio"],
            "main_models": serialize_main_models(models),
            "primary_model": serialize_primary_model(primary_model),
            "age_group_summary": serialize_age_group_summary(age_table_path),
            "rank_persistence": persistence_summary,
            "outputs": {
                "sample_report": os.path.basename(sample_report_path),
                "summary_stats": os.path.basename(summary_stats_path),
                "age_table": os.path.basename(age_table_path),
                "figure_data": os.path.basename(figure_data_path),
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
