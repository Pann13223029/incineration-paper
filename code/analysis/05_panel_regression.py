"""Stable-lineage engineering decomposition for operating waste generators."""

from __future__ import annotations

import os
from typing import Any

import numpy as np
import pandas as pd
import statsmodels.api as sm

from panel_utils import (
    OUTPUT_DIR,
    build_operating_power_frame,
    build_regression_frame,
    load_panel,
    sample_summary,
    within_total_variance_ratio,
    write_sample_definition_report,
    write_stage_manifest,
)


COHORT_ORDER = ["Before 1990", "1990-1999", "2000-2009", "2010 or later"]
TECHNOLOGY_CATEGORICALS = ["furnace_type_group", "facility_type_group"]
FOCAL_COMPONENT_TERMS = [
    "cohort_Before 1990",
    "cohort_1990-1999",
    "cohort_2000-2009",
    "log_capacity_t_day",
]


def clustered_ols(y: pd.Series, design: pd.DataFrame, groups: pd.Series):
    return sm.OLS(y.astype(float), design.astype(float)).fit(
        cov_type="cluster",
        cov_kwds={"groups": groups},
    )


def common_design(frame: pd.DataFrame, *, include_utilization: bool) -> pd.DataFrame:
    cohort = pd.Categorical(
        frame["reported_start_year_cohort"],
        categories=COHORT_ORDER,
        ordered=True,
    )
    cohort_dummies = pd.get_dummies(
        cohort,
        prefix="cohort",
        drop_first=False,
        dtype=float,
    ).drop(columns=["cohort_2010 or later"])
    cohort_dummies.index = frame.index
    technology = pd.get_dummies(
        frame[TECHNOLOGY_CATEGORICALS],
        prefix=["furnace", "facility"],
        drop_first=True,
        dtype=float,
    )
    years = pd.get_dummies(
        frame["fiscal_year"],
        prefix="fy",
        drop_first=True,
        dtype=float,
    )
    parts = [
        frame[["log_capacity_t_day", "n_furnaces"]],
        cohort_dummies,
        technology,
        years,
    ]
    if include_utilization:
        parts.insert(1, frame[["capacity_utilization_raw"]])
    return sm.add_constant(pd.concat(parts, axis=1), has_constant="add")


def output_design(frame: pd.DataFrame) -> pd.DataFrame:
    base = common_design(frame, include_utilization=False)
    direct = pd.DataFrame(
        {
            "log_throughput_t_year": np.log(frame["throughput_t_year"]),
            "log_power_capacity_kw": np.log(frame["power_capacity_kw"]),
        },
        index=frame.index,
    )
    return pd.concat(
        [
            base.drop(columns=["log_capacity_t_day"]),
            direct,
        ],
        axis=1,
    )


def legacy_design(frame: pd.DataFrame, *, include_generator_sizing: bool) -> pd.DataFrame:
    base = common_design(frame, include_utilization=True)
    numeric = frame[
        ["facility_age_years", "capacity_100t", "heating_value_mj_kg"]
    ].copy()
    design = pd.concat(
        [
            base.drop(columns=FOCAL_COMPONENT_TERMS, errors="ignore"),
            numeric,
        ],
        axis=1,
    )
    if include_generator_sizing:
        design["log_generator_design_intensity"] = frame[
            "log_generator_design_intensity"
        ]
    return design


def fit_component_models(frame: pd.DataFrame) -> dict[str, Any]:
    groups = frame["analysis_facility_id"]
    design_model = clustered_ols(
        frame["log_generator_design_intensity"],
        common_design(frame, include_utilization=False),
        groups,
    )
    capacity_factor_model = clustered_ols(
        frame["log_electrical_capacity_factor"],
        common_design(frame, include_utilization=True),
        groups,
    )
    output_model = clustered_ols(
        np.log(frame["power_generated_mwh"]),
        output_design(frame),
        groups,
    )

    plausible = frame[frame["plausible_heating_value"]].copy()
    legacy_model = clustered_ols(
        plausible["log_efficiency_raw"],
        legacy_design(plausible, include_generator_sizing=False),
        plausible["analysis_facility_id"],
    )
    sizing_adjusted_model = clustered_ols(
        plausible["log_efficiency_raw"],
        legacy_design(plausible, include_generator_sizing=True),
        plausible["analysis_facility_id"],
    )
    return {
        "design_intensity": design_model,
        "capacity_factor": capacity_factor_model,
        "gross_output": output_model,
        "legacy_gross_intensity": legacy_model,
        "sizing_adjusted_gross_intensity": sizing_adjusted_model,
        "legacy_frame": plausible,
    }


def model_row(model, term: str) -> dict[str, float]:
    coefficient = float(model.params[term])
    standard_error = float(model.bse[term])
    return {
        "coefficient": coefficient,
        "standard_error": standard_error,
        "ci_low": coefficient - 1.96 * standard_error,
        "ci_high": coefficient + 1.96 * standard_error,
        "p_value": float(model.pvalues[term]),
    }


def write_summary_statistics(frame: pd.DataFrame) -> str:
    variables = {
        "energy_efficiency_raw_mwh_per_t": "Gross generation intensity (MWh/t)",
        "generator_design_intensity_kw_per_t_day": "Generator sizing intensity (kW per t/day)",
        "electrical_capacity_factor": "Electrical capacity factor",
        "capacity_utilization_raw": "Waste-processing utilization",
        "power_capacity_kw": "Installed electrical capacity (kW)",
        "capacity_t_day": "Waste-processing design capacity (t/day)",
    }
    rows = []
    for variable, label in variables.items():
        values = frame[variable].dropna()
        rows.append(
            {
                "Variable": label,
                "N": len(values),
                "Mean": values.mean(),
                "Median": values.median(),
                "SD": values.std(),
                "Min": values.min(),
                "Max": values.max(),
            }
        )
    table = pd.DataFrame(rows)
    path = os.path.join(OUTPUT_DIR, "table1_summary_stats.md")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("# Generator Component Summary Statistics\n\n")
        handle.write(table.to_markdown(index=False, floatfmt=".3f"))
        handle.write(
            "\n\nThe frame excludes predeclared implausible generation-intensity, "
            "capacity-factor, utilization, generator-sizing, and reported-age records. "
            "Values are not clipped into the model.\n"
        )
    return path


def write_cohort_table(frame: pd.DataFrame) -> tuple[str, pd.DataFrame]:
    table = (
        frame.groupby("reported_start_year_cohort", observed=True)
        .agg(
            observations=("analysis_facility_id", "size"),
            stable_sites=("analysis_facility_id", "nunique"),
            median_gross_mwh_t=("energy_efficiency_raw_mwh_per_t", "median"),
            median_generator_sizing=(
                "generator_design_intensity_kw_per_t_day",
                "median",
            ),
            median_capacity_factor=("electrical_capacity_factor", "median"),
            median_waste_utilization=("capacity_utilization_raw", "median"),
        )
        .reset_index()
    )
    path = os.path.join(OUTPUT_DIR, "table2_generator_components_by_cohort.md")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("# Generator Components By Reported Start-Year Cohort\n\n")
        handle.write(table.to_markdown(index=False, floatfmt=".3f"))
        handle.write(
            "\n\nReported start-year cohort is an administrative design-vintage marker. "
            "It is not a verified turbine or boiler installation date.\n"
        )
    return path, table


def build_persistence_data(frame: pd.DataFrame) -> tuple[str, dict[str, float | int]]:
    ranked = frame[
        [
            "analysis_facility_id",
            "fiscal_year",
            "energy_efficiency_raw_mwh_per_t",
            "generator_design_intensity_kw_per_t_day",
            "electrical_capacity_factor",
        ]
    ].copy()
    metric_map = {
        "gross_generation_intensity": "energy_efficiency_raw_mwh_per_t",
        "generator_design_intensity": "generator_design_intensity_kw_per_t_day",
        "electrical_capacity_factor": "electrical_capacity_factor",
    }
    output_rows: list[dict[str, float | int | str]] = []
    summary: dict[str, float | int] = {}
    for label, variable in metric_map.items():
        metric = ranked[["analysis_facility_id", "fiscal_year", variable]].copy()
        metric["rank_pct"] = metric.groupby("fiscal_year")[variable].rank(
            pct=True,
            method="average",
        )
        following = metric.rename(
            columns={
                "fiscal_year": "year_end",
                "rank_pct": "rank_end",
            }
        )[["analysis_facility_id", "year_end", "rank_end"]]
        pairs = metric.rename(
            columns={"fiscal_year": "year_start", "rank_pct": "rank_start"}
        ).merge(following, on="analysis_facility_id", how="inner")
        pairs = pairs[pairs["year_end"].eq(pairs["year_start"] + 1)].copy()
        annual = (
            pairs.groupby(["year_start", "year_end"])
            .apply(
                lambda group: pd.Series(
                    {
                        "correlation": group["rank_start"].corr(group["rank_end"]),
                        "pairs": len(group),
                    }
                ),
                include_groups=False,
            )
            .reset_index()
        )
        for row in annual.itertuples(index=False):
            output_rows.append(
                {
                    "metric": label,
                    "year_start": int(row.year_start),
                    "year_end": int(row.year_end),
                    "rank_correlation": float(row.correlation),
                    "pairs": int(row.pairs),
                }
            )
        summary[f"{label}_pairs"] = int(len(pairs))
        summary[f"{label}_sites"] = int(pairs["analysis_facility_id"].nunique())
        summary[f"{label}_pooled_rank_correlation"] = float(
            pairs["rank_start"].corr(pairs["rank_end"])
        )
        summary[f"{label}_median_annual_correlation"] = float(
            annual["correlation"].median()
        )
    output = pd.DataFrame(output_rows)
    path = os.path.join(OUTPUT_DIR, "figure3_persistence.csv")
    output.to_csv(path, index=False, float_format="%.10g")
    return path, summary


def write_regression_report(
    frame: pd.DataFrame,
    models: dict[str, Any],
    persistence: dict[str, float | int],
) -> tuple[str, pd.DataFrame]:
    rows: list[dict[str, Any]] = []
    terms = {
        "cohort_Before 1990": "Reported start before 1990",
        "cohort_1990-1999": "Reported start 1990-1999",
        "cohort_2000-2009": "Reported start 2000-2009",
        "log_capacity_t_day": "Log waste-processing design capacity",
        "capacity_utilization_raw": "Waste-processing utilization",
    }
    for model_name in ["design_intensity", "capacity_factor"]:
        model = models[model_name]
        for term, label in terms.items():
            if term not in model.params:
                continue
            rows.append(
                {
                    "model": model_name,
                    "term": term,
                    "label": label,
                    **model_row(model, term),
                    "observations": int(model.nobs),
                    "r_squared": float(model.rsquared),
                }
            )
    results = pd.DataFrame(rows)
    csv_path = os.path.join(OUTPUT_DIR, "generator_component_results.csv")
    results.to_csv(csv_path, index=False, float_format="%.10g")

    legacy = models["legacy_gross_intensity"]
    adjusted = models["sizing_adjusted_gross_intensity"]
    path = os.path.join(OUTPUT_DIR, "regression_results.md")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("# Generator Design And Operating Component Results\n\n")
        handle.write(
            "The primary analysis separates installed generator sizing from annual "
            "electrical capacity factor. Gross MWh/t is retained as a descriptive "
            "product of design intensity, electrical capacity factor, and waste loading; "
            "it is not labelled independent operational efficiency.\n\n"
        )
        handle.write("## Primary Component Models\n\n")
        display = results[
            [
                "model",
                "label",
                "coefficient",
                "standard_error",
                "ci_low",
                "ci_high",
                "p_value",
            ]
        ]
        handle.write(display.to_markdown(index=False, floatfmt=".4f"))
        handle.write("\n\n")
        handle.write(
            f"- Engineering-valid rows: {len(frame):,} across "
            f"{frame['analysis_facility_id'].nunique():,} stable administrative lineages.\n"
        )
        handle.write(
            f"- Design-intensity model R-squared: "
            f"{models['design_intensity'].rsquared:.4f}.\n"
        )
        handle.write(
            f"- Electrical-capacity-factor model R-squared: "
            f"{models['capacity_factor'].rsquared:.4f}.\n"
        )
        handle.write(
            f"- Direct gross-output model elasticities: throughput "
            f"{models['gross_output'].params['log_throughput_t_year']:.3f}; installed "
            f"electrical capacity {models['gross_output'].params['log_power_capacity_kw']:.3f}.\n\n"
        )
        handle.write("## Why The Previous Gross-Intensity Regression Is Not Primary\n\n")
        handle.write(
            "A legacy-style gross-MWh/t model and the same model with installed "
            "generator sizing demonstrate what the former specification combined. "
            f"Both use {int(legacy.nobs):,} rows with plausible reported heating value "
            "and include heating value as a control.\n\n"
        )
        diagnostic_terms = [
            "facility_age_years",
            "capacity_100t",
            "capacity_utilization_raw",
            "log_generator_design_intensity",
        ]
        diagnostic_rows = []
        for term in diagnostic_terms:
            diagnostic_rows.append(
                {
                    "term": term,
                    "legacy_coefficient": (
                        float(legacy.params[term]) if term in legacy.params else np.nan
                    ),
                    "legacy_p_value": (
                        float(legacy.pvalues[term]) if term in legacy.params else np.nan
                    ),
                    "sizing_adjusted_coefficient": (
                        float(adjusted.params[term]) if term in adjusted.params else np.nan
                    ),
                    "sizing_adjusted_p_value": (
                        float(adjusted.pvalues[term]) if term in adjusted.params else np.nan
                    ),
                }
            )
        handle.write(pd.DataFrame(diagnostic_rows).to_markdown(index=False, floatfmt=".4f"))
        handle.write("\n\n")
        handle.write(
            f"Gross-intensity model R-squared changes from {legacy.rsquared:.4f} to "
            f"{adjusted.rsquared:.4f} after generator sizing is included. This is a "
            "specification diagnostic, not a causal mediation analysis.\n\n"
        )
        handle.write("## Adjacent-Year Rank Persistence\n\n")
        for label in [
            "gross_generation_intensity",
            "generator_design_intensity",
            "electrical_capacity_factor",
        ]:
            handle.write(
                f"- {label.replace('_', ' ').title()}: "
                f"r={persistence[f'{label}_pooled_rank_correlation']:.4f} across "
                f"{persistence[f'{label}_pairs']:,} pairs and "
                f"{persistence[f'{label}_sites']:,} lineages.\n"
            )
        handle.write(
            "\nModels use fiscal-year indicators, coarse furnace/facility configuration "
            "controls, and stable-lineage-clustered standard errors. Associations remain "
            "descriptive and do not identify retrofit or operating interventions.\n"
        )
    return path, results


def main() -> None:
    panel = load_panel()
    operating = build_operating_power_frame(panel)
    frame = build_regression_frame(panel)
    summary = sample_summary(panel)

    sample_path = os.path.join(OUTPUT_DIR, "sample_definition.md")
    write_sample_definition_report(sample_path, summary)
    stats_path = write_summary_statistics(frame)
    cohort_path, cohort_table = write_cohort_table(frame)
    persistence_path, persistence = build_persistence_data(frame)
    models = fit_component_models(frame)
    report_path, results = write_regression_report(frame, models, persistence)

    manifest_path = write_stage_manifest(
        "05_panel_regression",
        inputs=["data/processed/incineration_panel_identified.csv"],
        outputs=[
            "output/sample_definition.md",
            "output/table1_summary_stats.md",
            "output/table2_generator_components_by_cohort.md",
            "output/figure3_persistence.csv",
            "output/generator_component_results.csv",
            "output/regression_results.md",
        ],
        metadata={
            "operating_rows": int(len(operating)),
            "engineering_valid_rows": int(len(frame)),
            "stable_sites": int(frame["analysis_facility_id"].nunique()),
            "within_total_log_gross_intensity": float(
                within_total_variance_ratio(frame, "log_efficiency_raw")
            ),
            "within_total_log_design_intensity": float(
                within_total_variance_ratio(
                    frame,
                    "log_generator_design_intensity",
                )
            ),
            "within_total_log_capacity_factor": float(
                within_total_variance_ratio(
                    frame,
                    "log_electrical_capacity_factor",
                )
            ),
            "design_model": {
                "rsquared": float(models["design_intensity"].rsquared),
                "coefficients": {
                    term: float(models["design_intensity"].params[term])
                    for term in FOCAL_COMPONENT_TERMS
                },
            },
            "capacity_factor_model": {
                "rsquared": float(models["capacity_factor"].rsquared),
                "coefficients": {
                    term: float(models["capacity_factor"].params[term])
                    for term in [*FOCAL_COMPONENT_TERMS, "capacity_utilization_raw"]
                },
            },
            "gross_output_elasticities": {
                "throughput": float(
                    models["gross_output"].params["log_throughput_t_year"]
                ),
                "installed_electrical_capacity": float(
                    models["gross_output"].params["log_power_capacity_kw"]
                ),
            },
            "legacy_age_coefficient": float(
                models["legacy_gross_intensity"].params["facility_age_years"]
            ),
            "diagnostic_rows": int(models["legacy_gross_intensity"].nobs),
            "diagnostic_includes_heating_value": True,
            "sizing_adjusted_age_coefficient": float(
                models["sizing_adjusted_gross_intensity"].params[
                    "facility_age_years"
                ]
            ),
            "legacy_rsquared": float(models["legacy_gross_intensity"].rsquared),
            "sizing_adjusted_rsquared": float(
                models["sizing_adjusted_gross_intensity"].rsquared
            ),
            "diagnostic_terms": {
                term: {
                    "legacy_coefficient": (
                        float(models["legacy_gross_intensity"].params[term])
                        if term in models["legacy_gross_intensity"].params
                        else None
                    ),
                    "legacy_p_value": (
                        float(models["legacy_gross_intensity"].pvalues[term])
                        if term in models["legacy_gross_intensity"].pvalues
                        else None
                    ),
                    "sizing_adjusted_coefficient": float(
                        models["sizing_adjusted_gross_intensity"].params[term]
                    ),
                    "sizing_adjusted_p_value": float(
                        models["sizing_adjusted_gross_intensity"].pvalues[term]
                    ),
                }
                for term in [
                    "facility_age_years",
                    "capacity_100t",
                    "capacity_utilization_raw",
                    "log_generator_design_intensity",
                ]
            },
            "persistence": persistence,
            "cohort_rows": cohort_table.to_dict(orient="records"),
            "component_result_rows": int(len(results)),
        },
    )
    print(f"Engineering-valid frame: {len(frame):,} rows, {frame['analysis_facility_id'].nunique():,} lineages")
    print(f"Saved: {report_path}")
    print(f"Manifest: {manifest_path}")


if __name__ == "__main__":
    main()
