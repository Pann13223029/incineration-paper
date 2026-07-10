"""Predeclared robustness checks for the engineering-component analysis.

The primary analysis separates installed generator sizing, annual electrical
capacity factor, and gross output.  This stage asks whether those component
results survive reasonable changes in calendar window, observation weights,
and engineering-validity bounds.  It also reports within-lineage operational
models where the panel contains defensible variation. It deliberately avoids
administrative-disappearance inference and does not treat gross MWh/t as an
efficiency outcome.
"""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import statsmodels.api as sm

from panel_utils import (
    CAPACITY_FACTOR_CEIL,
    CAPACITY_FACTOR_FLOOR,
    CAPACITY_UTILIZATION_CAP,
    EFF_CEIL,
    EFF_FLOOR,
    OUTPUT_DIR,
    build_operating_power_frame,
    build_regression_frame,
    load_panel,
    within_total_variance_ratio,
    write_stage_manifest,
)


SCRIPT_DIR = Path(__file__).resolve().parent
RESULTS_PATH = os.path.join(OUTPUT_DIR, "robustness_component_results.csv")
REPORT_PATH = os.path.join(OUTPUT_DIR, "robustness_results.md")

COHORT_TERMS = [
    "cohort_Before 1990",
    "cohort_1990-1999",
    "cohort_2000-2009",
]

# These bounds are sensitivity analyses, not data-driven trimming rules.
BOUND_SETS = {
    "Main predeclared bounds": {
        "gross": (EFF_FLOOR, EFF_CEIL),
        "capacity_factor": (CAPACITY_FACTOR_FLOOR, CAPACITY_FACTOR_CEIL),
        "utilization": (0.02, CAPACITY_UTILIZATION_CAP),
        "design_intensity": (0.10, 100.0),
    },
    "Conservative engineering bounds": {
        "gross": (0.02, 0.70),
        "capacity_factor": (0.05, 1.05),
        "utilization": (0.05, 1.10),
        "design_intensity": (0.25, 75.0),
    },
    "Broad engineering bounds": {
        "gross": (0.005, 1.00),
        "capacity_factor": (0.01, 1.50),
        "utilization": (0.01, 1.50),
        "design_intensity": (0.05, 150.0),
    },
}


def load_component_stage():
    """Load the canonical component-design helpers without running its stage."""
    path = SCRIPT_DIR / "05_panel_regression.py"
    spec = importlib.util.spec_from_file_location("component_regression_stage", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load component regression stage: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def apply_engineering_bounds(
    operating: pd.DataFrame,
    bounds: dict[str, tuple[float, float]],
) -> pd.DataFrame:
    """Construct a complete component frame under an explicit bound set."""
    mask = (
        operating["energy_efficiency_raw_mwh_per_t"].between(*bounds["gross"])
        & operating["electrical_capacity_factor"].between(
            *bounds["capacity_factor"]
        )
        & operating["capacity_utilization_raw"].between(*bounds["utilization"])
        & operating["generator_design_intensity_kw_per_t_day"].between(
            *bounds["design_intensity"]
        )
        & operating["facility_age_years"].notna()
    )
    required = [
        "analysis_facility_id",
        "reported_start_year_cohort",
        "log_capacity_t_day",
        "capacity_utilization_raw",
        "log_generator_design_intensity",
        "log_electrical_capacity_factor",
        "throughput_t_year",
        "power_capacity_kw",
        "power_generated_mwh",
    ]
    frame = operating.loc[mask].dropna(subset=required).copy()
    if frame.duplicated(["analysis_facility_id", "fiscal_year"]).any():
        raise ValueError("Alternative-bound frame contains duplicate stable-lineage-years")
    return frame


def active_design(design: pd.DataFrame) -> pd.DataFrame:
    """Drop non-finite and zero-variance nuisance columns before estimation."""
    clean = design.astype(float).replace([np.inf, -np.inf], np.nan)
    if clean.isna().any().any():
        raise ValueError("Model design contains non-finite values")
    keep = [
        column
        for column in clean.columns
        if column == "const" or float(clean[column].var(ddof=0)) > 1e-12
    ]
    return clean[keep]


def fit_clustered_model(
    y: pd.Series,
    design: pd.DataFrame,
    groups: pd.Series,
    weights: pd.Series | None,
):
    """Fit OLS/WLS with stable-lineage clustered covariance."""
    x = active_design(design)
    if weights is None:
        estimator = sm.OLS(y.astype(float), x)
    else:
        estimator = sm.WLS(y.astype(float), x, weights=weights.astype(float))
    return estimator.fit(cov_type="cluster", cov_kwds={"groups": groups})


def append_model_rows(
    rows: list[dict[str, Any]],
    *,
    specification: str,
    evidence: str,
    outcome: str,
    model,
    terms: list[str],
    frame: pd.DataFrame,
) -> None:
    """Append deterministic coefficient records for focal terms."""
    confidence = model.conf_int()
    for term in terms:
        if term not in model.params.index:
            continue
        rows.append(
            {
                "specification": specification,
                "evidence": evidence,
                "outcome": outcome,
                "term": term,
                "coefficient": float(model.params[term]),
                "standard_error": float(model.bse[term]),
                "ci_low": float(confidence.loc[term, 0]),
                "ci_high": float(confidence.loc[term, 1]),
                "p_value": float(model.pvalues[term]),
                "observations": int(model.nobs),
                "stable_sites": int(frame["analysis_facility_id"].nunique()),
                "r_squared": float(model.rsquared),
            }
        )


def run_component_specification(
    component_stage,
    frame: pd.DataFrame,
    specification: str,
    *,
    site_equal_weights: bool,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Fit the three canonical component models under one sample specification."""
    weights = None
    if site_equal_weights:
        site_counts = frame.groupby("analysis_facility_id")[
            "analysis_facility_id"
        ].transform("size")
        weights = 1.0 / site_counts

    groups = frame["analysis_facility_id"]
    design_model = fit_clustered_model(
        frame["log_generator_design_intensity"],
        component_stage.common_design(frame, include_utilization=False),
        groups,
        weights,
    )
    capacity_factor_model = fit_clustered_model(
        frame["log_electrical_capacity_factor"],
        component_stage.common_design(frame, include_utilization=True),
        groups,
        weights,
    )
    output_model = fit_clustered_model(
        np.log(frame["power_generated_mwh"]),
        component_stage.output_design(frame),
        groups,
        weights,
    )

    rows: list[dict[str, Any]] = []
    append_model_rows(
        rows,
        specification=specification,
        evidence="between-and-within pooled component model",
        outcome="log_generator_design_intensity",
        model=design_model,
        terms=[*COHORT_TERMS, "log_capacity_t_day"],
        frame=frame,
    )
    append_model_rows(
        rows,
        specification=specification,
        evidence="between-and-within pooled component model",
        outcome="log_electrical_capacity_factor",
        model=capacity_factor_model,
        terms=[*COHORT_TERMS, "log_capacity_t_day", "capacity_utilization_raw"],
        frame=frame,
    )
    append_model_rows(
        rows,
        specification=specification,
        evidence="between-and-within pooled component model",
        outcome="log_gross_generation_mwh",
        model=output_model,
        terms=["log_throughput_t_year", "log_power_capacity_kw"],
        frame=frame,
    )
    metadata = {
        "observations": int(len(frame)),
        "stable_sites": int(frame["analysis_facility_id"].nunique()),
        "site_equal_weights": site_equal_weights,
        "design_r_squared": float(design_model.rsquared),
        "capacity_factor_r_squared": float(capacity_factor_model.rsquared),
        "gross_output_r_squared": float(output_model.rsquared),
    }
    return rows, metadata


def demean_within_asset_episode(
    frame: pd.DataFrame,
    outcome: str,
    predictors: list[str],
) -> tuple[pd.Series, pd.DataFrame, pd.DataFrame]:
    """Return within-asset outcome/design with demeaned fiscal-year indicators."""
    columns = [
        "analysis_facility_id",
        "asset_episode_id",
        "fiscal_year",
        outcome,
        *predictors,
    ]
    reg = frame[columns].replace([np.inf, -np.inf], np.nan).dropna().copy()
    repeated = reg.groupby("asset_episode_id")["fiscal_year"].transform("size")
    reg = reg[repeated >= 2].copy()
    years = pd.get_dummies(
        reg["fiscal_year"], prefix="fy", drop_first=True, dtype=float
    )
    design = pd.concat([reg[predictors], years], axis=1)
    episode = reg["asset_episode_id"]
    y_within = reg[outcome] - reg.groupby("asset_episode_id")[outcome].transform(
        "mean"
    )
    x_within = design - design.groupby(episode).transform("mean")
    return y_within, active_design(x_within), reg


def run_within_site_models(frame: pd.DataFrame) -> list[dict[str, Any]]:
    """Estimate operational relationships using only within-lineage changes."""
    rows: list[dict[str, Any]] = []
    model_specs = [
        (
            "Within-lineage asset-episode FE: capacity factor",
            "log_electrical_capacity_factor",
            ["capacity_utilization_raw"],
            ["capacity_utilization_raw"],
            "within-lineage, within-asset operational model",
        ),
        (
            "Within-lineage asset-episode FE: gross output",
            "log_power_generated_mwh",
            ["log_throughput_t_year", "log_power_capacity_kw"],
            ["log_throughput_t_year", "log_power_capacity_kw"],
            "within-lineage, within-asset operational model",
        ),
    ]
    augmented = frame.assign(
        log_power_generated_mwh=np.log(frame["power_generated_mwh"]),
        log_throughput_t_year=np.log(frame["throughput_t_year"]),
        log_power_capacity_kw=np.log(frame["power_capacity_kw"]),
    )
    for label, outcome, predictors, terms, evidence in model_specs:
        y, design, reg = demean_within_asset_episode(
            augmented, outcome, predictors
        )
        model = sm.OLS(y.astype(float), design).fit(
            cov_type="cluster",
            cov_kwds={"groups": reg["analysis_facility_id"]},
        )
        append_model_rows(
            rows,
            specification=label,
            evidence=evidence,
            outcome=outcome,
            model=model,
            terms=terms,
            frame=reg,
        )

    ordered = augmented.sort_values(["analysis_facility_id", "fiscal_year"]).copy()
    group = ordered.groupby("analysis_facility_id", sort=False)
    ordered["lag_fiscal_year"] = group["fiscal_year"].shift(1)
    ordered["lag_asset_episode_id"] = group["asset_episode_id"].shift(1)
    for variable in [
        "log_electrical_capacity_factor",
        "capacity_utilization_raw",
        "log_power_generated_mwh",
        "log_throughput_t_year",
        "log_power_capacity_kw",
    ]:
        ordered[f"delta_{variable}"] = ordered[variable] - group[variable].shift(1)
    adjacent = ordered[
        ordered["fiscal_year"].sub(ordered["lag_fiscal_year"]).eq(1)
        & ordered["asset_episode_id"].eq(ordered["lag_asset_episode_id"])
    ].copy()
    difference_specs = [
        (
            "Exact-adjacent first difference: capacity factor",
            "delta_log_electrical_capacity_factor",
            ["delta_capacity_utilization_raw"],
        ),
        (
            "Exact-adjacent first difference: gross output",
            "delta_log_power_generated_mwh",
            ["delta_log_throughput_t_year", "delta_log_power_capacity_kw"],
        ),
    ]
    for label, outcome, predictors in difference_specs:
        columns = ["analysis_facility_id", "fiscal_year", outcome, *predictors]
        reg = adjacent[columns].replace([np.inf, -np.inf], np.nan).dropna().copy()
        years = pd.get_dummies(
            reg["fiscal_year"], prefix="fy", drop_first=True, dtype=float
        )
        design = active_design(
            sm.add_constant(pd.concat([reg[predictors], years], axis=1))
        )
        model = sm.OLS(reg[outcome].astype(float), design).fit(
            cov_type="cluster",
            cov_kwds={"groups": reg["analysis_facility_id"]},
        )
        append_model_rows(
            rows,
            specification=label,
            evidence="exact-adjacent within-lineage change model",
            outcome=outcome,
            model=model,
            terms=predictors,
            frame=reg,
        )
    return rows


def write_report(
    results: pd.DataFrame,
    specification_metadata: dict[str, Any],
    bound_samples: pd.DataFrame,
    variation: pd.DataFrame,
) -> None:
    """Write the reviewer-facing robustness report."""
    display = results.copy()
    for column in ["coefficient", "standard_error", "ci_low", "ci_high", "r_squared"]:
        display[column] = display[column].map(lambda value: f"{value:.4f}")
    display["p_value"] = display["p_value"].map(
        lambda value: "<0.0001" if value < 0.0001 else f"{value:.4f}"
    )
    display = display.rename(
        columns={
            "specification": "Specification",
            "evidence": "Evidence",
            "outcome": "Outcome",
            "term": "Term",
            "coefficient": "Coefficient",
            "standard_error": "Clustered SE",
            "ci_low": "95% CI low",
            "ci_high": "95% CI high",
            "p_value": "p-value",
            "observations": "N",
            "stable_sites": "Administrative lineages",
            "r_squared": "R-squared",
        }
    )
    sample_display = pd.DataFrame(
        [
            {
                "Specification": label,
                "Rows": values["observations"],
                "Administrative lineages": values["stable_sites"],
                "Lineage-equal weights": values["site_equal_weights"],
                "Design R-squared": values["design_r_squared"],
                "Capacity-factor R-squared": values[
                    "capacity_factor_r_squared"
                ],
                "Gross-output R-squared": values["gross_output_r_squared"],
            }
            for label, values in specification_metadata.items()
        ]
    )
    with open(REPORT_PATH, "w", encoding="utf-8") as handle:
        handle.write("# Engineering-Component Robustness Checks\n\n")
        handle.write(
            "These checks preserve the paper's component estimands: installed generator "
            "sizing, annual electrical capacity factor, and gross electricity output. "
            "Gross MWh/t is not relabeled as technical efficiency, and administrative "
            "disappearance is not modeled. All covariance estimates are clustered by audited "
            "stable administrative lineage.\n\n"
        )
        handle.write("## Predeclared Sensitivity Design\n\n")
        handle.write(
            "- Calendar splits use the first and second ten-year halves of FY2005-FY2024.\n"
            "- Lineage-equal WLS gives each administrative lineage equal total weight, limiting influence from long histories.\n"
            "- The identity-certain sensitivity excludes every lineage containing an accepted low-margin link.\n"
            "- Conservative and broad bound sets are fixed below and are not chosen from coefficient results.\n"
            "- Asset-episode fixed effects and exact-adjacent first differences are used only for operational components with meaningful within-lineage, within-asset variation. Uncertainty remains clustered by stable lineage. Generator design intensity remains primarily a between-asset design attribute.\n\n"
        )
        handle.write(bound_samples.to_markdown(index=False, floatfmt=".3f"))
        handle.write("\n\n## Model Samples\n\n")
        handle.write(sample_display.to_markdown(index=False, floatfmt=".4f"))
        handle.write("\n\n## Within-Asset Variation Available\n\n")
        handle.write(variation.to_markdown(index=False, floatfmt=".4f"))
        handle.write("\n\n## Coefficient Results\n\n")
        handle.write(display.to_markdown(index=False))
        handle.write("\n\n## Interpretation Guardrails\n\n")
        handle.write(
            "The window, weighting, and bound checks test specification dependence; "
            "they do not convert the observational relationships into causal effects. "
            "Within-asset models absorb time-invariant asset-episode attributes, but annual throughput, "
            "utilization, generator capacity, and output may still be jointly determined. "
            "The gross-output model is an accounting-consistent operational description, "
            "not an independent thermodynamic-efficiency estimate.\n"
        )


def main() -> None:
    component_stage = load_component_stage()
    panel = load_panel()
    operating = build_operating_power_frame(panel)
    main_frame = build_regression_frame(panel)
    identity_certain = main_frame[~main_frame["identity_lineage_uncertain"]].copy()
    conservative = apply_engineering_bounds(
        operating, BOUND_SETS["Conservative engineering bounds"]
    )
    broad = apply_engineering_bounds(
        operating, BOUND_SETS["Broad engineering bounds"]
    )

    specifications = [
        ("Main predeclared bounds", main_frame, False),
        (
            "First decade (FY2005-FY2014)",
            main_frame[main_frame["fiscal_year"].between(2005, 2014)].copy(),
            False,
        ),
        (
            "Second decade (FY2015-FY2024)",
            main_frame[main_frame["fiscal_year"].between(2015, 2024)].copy(),
            False,
        ),
        ("Lineage-equal weights", main_frame, True),
        ("Identity-certain lineages", identity_certain, False),
        ("Conservative engineering bounds", conservative, False),
        ("Broad engineering bounds", broad, False),
    ]

    rows: list[dict[str, Any]] = []
    specification_metadata: dict[str, Any] = {}
    for label, frame, site_equal in specifications:
        if len(frame) < 100 or frame["analysis_facility_id"].nunique() < 30:
            raise ValueError(f"Robustness sample is unexpectedly sparse: {label}")
        spec_rows, metadata = run_component_specification(
            component_stage,
            frame,
            label,
            site_equal_weights=site_equal,
        )
        rows.extend(spec_rows)
        specification_metadata[label] = metadata

    rows.extend(run_within_site_models(main_frame))
    results = pd.DataFrame(rows)
    results.to_csv(RESULTS_PATH, index=False, float_format="%.10g")

    bound_rows = []
    for label, bounds in BOUND_SETS.items():
        if label == "Main predeclared bounds":
            frame = main_frame
        elif label == "Conservative engineering bounds":
            frame = conservative
        else:
            frame = broad
        bound_rows.append(
            {
                "Bound set": label,
                "Gross MWh/t": f"{bounds['gross'][0]:g}-{bounds['gross'][1]:g}",
                "Electrical capacity factor": f"{bounds['capacity_factor'][0]:g}-{bounds['capacity_factor'][1]:g}",
                "Processing utilization": f"{bounds['utilization'][0]:g}-{bounds['utilization'][1]:g}",
                "Generator kW per t/day": f"{bounds['design_intensity'][0]:g}-{bounds['design_intensity'][1]:g}",
                "Rows": int(len(frame)),
                "Administrative lineages": int(frame["analysis_facility_id"].nunique()),
            }
        )
    bound_samples = pd.DataFrame(bound_rows)
    variation = pd.DataFrame(
        [
            {
                "Component": "Log generator design intensity",
                "Within/total variance ratio": within_total_variance_ratio(
                    main_frame,
                    "log_generator_design_intensity",
                    entity_col="asset_episode_id",
                ),
            },
            {
                "Component": "Log electrical capacity factor",
                "Within/total variance ratio": within_total_variance_ratio(
                    main_frame,
                    "log_electrical_capacity_factor",
                    entity_col="asset_episode_id",
                ),
            },
            {
                "Component": "Log gross generation intensity",
                "Within/total variance ratio": within_total_variance_ratio(
                    main_frame,
                    "log_efficiency_raw",
                    entity_col="asset_episode_id",
                ),
            },
        ]
    )
    write_report(results, specification_metadata, bound_samples, variation)

    manifest_path = write_stage_manifest(
        "06_robustness",
        inputs=["data/processed/incineration_panel_identified.csv"],
        outputs=[
            "output/robustness_results.md",
            "output/robustness_component_results.csv",
        ],
        metadata={
            "specifications": specification_metadata,
            "coefficient_rows": int(len(results)),
            "within_site_result_rows": int(
                results["evidence"].str.contains("within-lineage").sum()
            ),
            "within_total_variance": {
                row["Component"]: float(row["Within/total variance ratio"])
                for row in variation.to_dict(orient="records")
            },
            "bound_sets": BOUND_SETS,
        },
    )
    print(f"Saved: {RESULTS_PATH}")
    print(f"Saved: {REPORT_PATH}")
    print(f"Manifest: {manifest_path}")


if __name__ == "__main__":
    main()
