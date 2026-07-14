"""Primary sparse-entry and raw-quantity models for the major revision."""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import statsmodels.api as sm

from panel_utils import (
    OUTPUT_DIR,
    build_adoption_frame,
    build_adoption_model_frame,
    build_adoption_pathway_audit,
    build_regression_frame,
    load_panel,
    write_stage_manifest,
)
from rare_event_utils import (
    bootstrap_covariance_wald_test,
    cluster_bootstrap_coefficients,
    fit_firth_logit,
)


SCRIPT_DIR = Path(__file__).resolve().parent
BOOTSTRAP_REPETITIONS = int(
    os.environ.get("SCIENTIFIC_REVISION_BOOTSTRAP_REPETITIONS", "1999")
)
ENTRY_TERMS = [
    "age_per_10y",
    "log_processing_capacity",
    "calendar_per_5y",
    "log_elapsed_risk",
]
COHORT_TERMS = [
    "cohort_Before 1990",
    "cohort_1990-1999",
    "cohort_2000-2009",
]


def load_component_stage():
    """Load shared component-design helpers without running their stage."""
    path = SCRIPT_DIR / "05_panel_regression.py"
    spec = importlib.util.spec_from_file_location("component_stage", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load component stage: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def primary_entry_design(frame: pd.DataFrame) -> pd.DataFrame:
    """Build the prespecified five-parameter sparse-entry design."""
    design = pd.DataFrame(
        {
            "age_per_10y": frame["lag_facility_age_years"] / 10.0,
            "log_processing_capacity": np.log1p(
                frame["lag_capacity_t_day"] / 100.0
            ),
            "calendar_per_5y": (frame["fiscal_year"] - 2014.5) / 5.0,
            "log_elapsed_risk": np.log1p(frame["elapsed_at_risk_years"]),
        },
        index=frame.index,
    )
    if not np.isfinite(design.to_numpy(float)).all():
        raise ValueError("Revised entry design contains non-finite values")
    return sm.add_constant(design, has_constant="add")


def fit_entry_frame(frame: pd.DataFrame, label: str) -> dict[str, Any]:
    design = primary_entry_design(frame)
    fit_frame = frame.copy()
    for column in design.columns:
        fit_frame[column] = design[column]
    fit_frame["event"] = fit_frame["adopt_power_this_year"].astype(float)
    result = fit_firth_logit(design, fit_frame["event"])
    if not result.converged:
        raise RuntimeError(f"Revised Firth model failed to converge: {label}")
    bootstrap = cluster_bootstrap_coefficients(
        fit_frame,
        list(design.columns),
        "event",
        "analysis_facility_id",
        repetitions=BOOTSTRAP_REPETITIONS,
        seed=20260714,
    )
    if len(bootstrap) != BOOTSTRAP_REPETITIONS:
        raise RuntimeError(f"Incomplete revised bootstrap: {label}")
    return {
        "label": label,
        "frame": frame,
        "fit_frame": fit_frame,
        "result": result,
        "bootstrap": bootstrap,
        "age_bootstrap_wald": bootstrap_covariance_wald_test(
            result.params,
            bootstrap,
            ["age_per_10y"],
        ),
    }


def entry_result_rows(bundles: list[dict[str, Any]]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for bundle in bundles:
        result = bundle["result"]
        bootstrap = bundle["bootstrap"]
        for term in ENTRY_TERMS:
            samples = bootstrap[term].dropna()
            rows.append(
                {
                    "model": bundle["label"],
                    "term": term,
                    "coefficient": float(result.params[term]),
                    "standard_error_model_based": float(
                        result.standard_errors[term]
                    ),
                    "p_value_model_based": float(result.pvalues[term]),
                    "bootstrap_ci_low": float(samples.quantile(0.025)),
                    "bootstrap_ci_high": float(samples.quantile(0.975)),
                    "observations": int(len(bundle["frame"])),
                    "lineages": int(
                        bundle["frame"]["analysis_facility_id"].nunique()
                    ),
                    "events": int(bundle["frame"]["adopt_power_this_year"].sum()),
                    "bootstrap_repetitions": int(len(bootstrap)),
                }
            )
    return pd.DataFrame(rows)


def scale_contrast(bundle: dict[str, Any]) -> dict[str, float]:
    contrast = np.log(2.0)
    coefficient = float(bundle["result"].params["log_processing_capacity"])
    samples = np.exp(
        bundle["bootstrap"]["log_processing_capacity"].to_numpy(float) * contrast
    )
    return {
        "odds_ratio_300_vs_100": float(np.exp(coefficient * contrast)),
        "bootstrap_ci_low": float(np.quantile(samples, 0.025)),
        "bootstrap_ci_high": float(np.quantile(samples, 0.975)),
    }


def build_event_composition(
    panel: pd.DataFrame,
    adoption: pd.DataFrame,
    exact: pd.DataFrame,
) -> pd.DataFrame:
    pathways = build_adoption_pathway_audit(panel, adoption=adoption)
    event_columns = [
        "analysis_facility_id",
        "fiscal_year",
        "lag_facility_age_years",
        "lag_capacity_t_day",
        "lag_throughput_t_year",
        "same_asset_episode_as_lag",
    ]
    events = exact.loc[exact["adopt_power_this_year"].eq(1), event_columns].copy()
    events = events.merge(
        pathways[
            [
                "analysis_facility_id",
                "fiscal_year",
                "prefecture",
                "facility_name",
                "pathway_category",
                "pathway_basis",
            ]
        ],
        on=["analysis_facility_id", "fiscal_year"],
        how="left",
        validate="one_to_one",
    )
    events["calendar_era"] = pd.cut(
        events["fiscal_year"],
        bins=[2004, 2009, 2014, 2019, 2024],
        labels=["FY2005-2009", "FY2010-2014", "FY2015-2019", "FY2020-2024"],
    ).astype("string")
    events["capacity_group"] = pd.cut(
        events["lag_capacity_t_day"],
        bins=[0, 99.999, 199.999, 299.999, np.inf],
        labels=["<100", "100-199", "200-299", "300+"],
    ).astype("string")
    if len(events) != 35 or events["pathway_category"].isna().any():
        raise ValueError("Revised modeled-event composition is incomplete")
    return events.sort_values(["fiscal_year", "analysis_facility_id"])


def influence_diagnostics(bundle: dict[str, Any]) -> pd.DataFrame:
    frame = bundle["fit_frame"]
    events = frame[frame["event"].eq(1)].copy()
    rows: list[dict[str, Any]] = []
    contrast = np.log(2.0)
    for event_index, event in events.iterrows():
        event_deleted = frame.copy()
        event_deleted.loc[event_index, "event"] = 0.0
        event_result = fit_firth_logit(
            event_deleted[["const", *ENTRY_TERMS]],
            event_deleted["event"],
        )
        lineage_deleted = frame[
            ~frame["analysis_facility_id"].eq(event["analysis_facility_id"])
        ].copy()
        lineage_result = fit_firth_logit(
            lineage_deleted[["const", *ENTRY_TERMS]],
            lineage_deleted["event"],
        )
        for deletion, result in (
            ("event_reclassified", event_result),
            ("event_lineage_removed", lineage_result),
        ):
            if not result.converged:
                raise RuntimeError(
                    f"Influence fit failed for {event['analysis_facility_id']}"
                )
            coefficient = float(result.params["log_processing_capacity"])
            rows.append(
                {
                    "deletion": deletion,
                    "omitted_lineage": event["analysis_facility_id"],
                    "event_year": int(event["fiscal_year"]),
                    "capacity_coefficient": coefficient,
                    "odds_ratio_300_vs_100": float(
                        np.exp(coefficient * contrast)
                    ),
                    "age_per_10y_coefficient": float(
                        result.params["age_per_10y"]
                    ),
                    "converged": bool(result.converged),
                }
            )
    return pd.DataFrame(rows)


def clustered_ols(y: pd.Series, design: pd.DataFrame, groups: pd.Series):
    return sm.OLS(y.astype(float), design.astype(float)).fit(
        cov_type="cluster",
        cov_kwds={"groups": groups},
    )


def raw_quantity_models(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    component = load_component_stage()
    common = component.common_design(frame, include_utilization=False)
    installed = clustered_ols(
        np.log(frame["power_capacity_kw"]),
        common,
        frame["analysis_facility_id"],
    )
    factor = clustered_ols(
        frame["log_electrical_capacity_factor"],
        component.common_design(frame, include_utilization=True),
        frame["analysis_facility_id"],
    )
    gross = clustered_ols(
        np.log(frame["power_generated_mwh"]),
        component.output_design(frame),
        frame["analysis_facility_id"],
    )
    rows: list[dict[str, Any]] = []
    models = {
        "log_installed_capacity_kw": installed,
        "log_electrical_capacity_factor": factor,
        "log_gross_generation_mwh": gross,
    }
    terms = {
        "log_installed_capacity_kw": [*COHORT_TERMS, "log_capacity_t_day"],
        "log_electrical_capacity_factor": [
            *COHORT_TERMS,
            "log_capacity_t_day",
            "capacity_utilization_raw",
        ],
        "log_gross_generation_mwh": [
            "log_throughput_t_year",
            "log_power_capacity_kw",
        ],
    }
    for outcome, model in models.items():
        confidence = model.conf_int()
        for term in terms[outcome]:
            rows.append(
                {
                    "outcome": outcome,
                    "term": term,
                    "coefficient": float(model.params[term]),
                    "standard_error": float(model.bse[term]),
                    "ci_low": float(confidence.loc[term, 0]),
                    "ci_high": float(confidence.loc[term, 1]),
                    "p_value": float(model.pvalues[term]),
                    "observations": int(model.nobs),
                    "lineages": int(frame["analysis_facility_id"].nunique()),
                    "r_squared": float(model.rsquared),
                }
            )
    results = pd.DataFrame(rows)

    figure_rows: list[dict[str, Any]] = []
    for outcome, label in (
        ("log_installed_capacity_kw", "Installed electrical capacity"),
        ("log_electrical_capacity_factor", "Electrical capacity factor"),
    ):
        subset = results[results["outcome"].eq(outcome)].set_index("term")
        for term, cohort in zip(
            COHORT_TERMS,
            ["Before 1990", "1990-1999", "2000-2009"],
        ):
            row = subset.loc[term]
            figure_rows.append(
                {
                    "component": label,
                    "cohort": cohort,
                    "percent_difference": 100.0
                    * (np.exp(float(row["coefficient"])) - 1.0),
                    "ci_low_percent": 100.0
                    * (np.exp(float(row["ci_low"])) - 1.0),
                    "ci_high_percent": 100.0
                    * (np.exp(float(row["ci_high"])) - 1.0),
                    "reference": "2010 or later",
                }
            )
        figure_rows.append(
            {
                "component": label,
                "cohort": "2010 or later",
                "percent_difference": 0.0,
                "ci_low_percent": 0.0,
                "ci_high_percent": 0.0,
                "reference": "2010 or later",
            }
        )
    return results, pd.DataFrame(figure_rows)


def cohort_overlap(frame: pd.DataFrame) -> pd.DataFrame:
    overlap = (
        frame.groupby(["reported_start_year_cohort", "fiscal_year"], observed=True)
        .agg(
            rows=("analysis_facility_id", "size"),
            lineages=("analysis_facility_id", "nunique"),
        )
        .reset_index()
    )
    return overlap


def write_report(
    entry_results: pd.DataFrame,
    bundles: list[dict[str, Any]],
    composition: pd.DataFrame,
    influence: pd.DataFrame,
    raw_results: pd.DataFrame,
    engineering_frame: pd.DataFrame,
) -> str:
    path = os.path.join(OUTPUT_DIR, "scientific_revision_results.md")
    scale_rows = []
    for bundle in bundles:
        scale_rows.append({"Model": bundle["label"], **scale_contrast(bundle)})
    composition_table = pd.crosstab(
        composition["calendar_era"], composition["pathway_category"]
    ).reset_index()
    influence_summary = (
        influence.groupby("deletion")["odds_ratio_300_vs_100"]
        .agg(["min", "median", "max"])
        .reset_index()
    )
    installed = raw_results[
        raw_results["outcome"].eq("log_installed_capacity_kw")
    ]
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("# Major-Revision Scientific Results\n\n")
        handle.write("## Lower-Degree-Of-Freedom Entry Model\n\n")
        handle.write(
            f"The prespecified primary model uses five parameters including the "
            f"intercept and {BOOTSTRAP_REPETITIONS:,} deterministic whole-lineage "
            "bootstrap replications per frame.\n\n"
        )
        handle.write(pd.DataFrame(scale_rows).to_markdown(index=False, floatfmt=".4f"))
        handle.write("\n\n")
        age = entry_results[entry_results["term"].eq("age_per_10y")]
        handle.write(age.to_markdown(index=False, floatfmt=".4f"))
        handle.write("\n\n## Exact Modeled-Event Composition\n\n")
        handle.write(composition_table.to_markdown(index=False))
        handle.write("\n\n")
        handle.write(
            composition["pathway_category"].value_counts().rename_axis(
                "Pathway"
            ).reset_index(name="Events").to_markdown(index=False)
        )
        handle.write("\n\n## Event Influence\n\n")
        handle.write(influence_summary.to_markdown(index=False, floatfmt=".4f"))
        handle.write(
            "\n\nThe deletion range is diagnostic. It does not convert event histories "
            "into independent observations.\n\n"
        )
        handle.write("## Raw-Quantity Engineering Models\n\n")
        handle.write(installed.to_markdown(index=False, floatfmt=".4f"))
        handle.write("\n\n")
        handle.write(
            "The installed-kW model is the raw-quantity primary representation. "
            "With identical controls, subtracting log processing capacity from its "
            "outcome yields the design-intensity parameterization; this translation "
            "is algebraic rather than independent corroboration.\n\n"
        )
        handle.write(
            f"Administrative proxy exceptions retained within the audited 1.20 upper "
            f"bounds: {(engineering_frame['electrical_capacity_factor'] > 1).sum()} "
            f"capacity-factor rows and "
            f"{(engineering_frame['capacity_utilization_raw'] > 1).sum()} utilization rows.\n"
        )
    return path


def main() -> None:
    panel = load_panel()
    adoption = build_adoption_frame(panel)
    exact = build_adoption_model_frame(panel, adoption, exact_year_only=True)
    uncertain_lineages = set(
        panel.loc[panel["identity_match_uncertain"], "stable_site_id"].astype(str)
    )
    frames = [
        ("Broad reduced-DF frame", exact),
        ("Prior-operation reduced-DF frame", exact[exact["lag_throughput_t_year"].gt(0)].copy()),
        ("Same-episode reduced-DF frame", exact[exact["same_asset_episode_as_lag"]].copy()),
        ("Identity-certain reduced-DF frame", exact[~exact["analysis_facility_id"].astype(str).isin(uncertain_lineages)].copy()),
    ]
    bundles = [fit_entry_frame(frame, label) for label, frame in frames]
    entry_results = entry_result_rows(bundles)
    bootstrap = pd.concat(
        [bundle["bootstrap"].assign(model=bundle["label"]) for bundle in bundles],
        ignore_index=True,
    )
    composition = build_event_composition(panel, adoption, exact)
    influence = influence_diagnostics(bundles[0])

    engineering_frame = build_regression_frame(panel)
    raw_results, figure_data = raw_quantity_models(engineering_frame)
    overlap = cohort_overlap(engineering_frame)

    outputs = {
        "output/revised_entry_results.csv": entry_results,
        "output/revised_entry_bootstrap.csv": bootstrap,
        "output/revised_entry_influence.csv": influence,
        "output/adoption_event_composition.csv": composition,
        "output/raw_quantity_component_results.csv": raw_results,
        "output/figure3_adjusted_components.csv": figure_data,
        "output/cohort_year_overlap.csv": overlap,
    }
    for relative, frame in outputs.items():
        frame.to_csv(
            Path(OUTPUT_DIR).parent / relative,
            index=False,
            float_format="%.10g",
        )
    report_path = write_report(
        entry_results,
        bundles,
        composition,
        influence,
        raw_results,
        engineering_frame,
    )
    manifest_path = write_stage_manifest(
        "05b_scientific_revision",
        inputs=["data/processed/incineration_panel_identified.csv"],
        outputs=[*outputs.keys(), "output/scientific_revision_results.md"],
        metadata={
            "bootstrap_repetitions": BOOTSTRAP_REPETITIONS,
            "entry_models": {
                bundle["label"]: {
                    "rows": int(len(bundle["frame"])),
                    "lineages": int(bundle["frame"]["analysis_facility_id"].nunique()),
                    "events": int(bundle["frame"]["adopt_power_this_year"].sum()),
                    "coefficients": {
                        term: float(bundle["result"].params[term])
                        for term in ENTRY_TERMS
                    },
                    "scale_contrast": scale_contrast(bundle),
                    "age_bootstrap_wald": list(bundle["age_bootstrap_wald"]),
                }
                for bundle in bundles
            },
            "event_pathway_counts": {
                str(key): int(value)
                for key, value in composition["pathway_category"].value_counts().items()
            },
            "influence_scale_or_min": float(
                influence["odds_ratio_300_vs_100"].min()
            ),
            "influence_scale_or_max": float(
                influence["odds_ratio_300_vs_100"].max()
            ),
            "capacity_factor_above_one": int(
                (engineering_frame["electrical_capacity_factor"] > 1).sum()
            ),
            "utilization_above_one": int(
                (engineering_frame["capacity_utilization_raw"] > 1).sum()
            ),
            "raw_quantity_result_rows": int(len(raw_results)),
        },
    )
    print(
        f"Revised entry models: {len(entry_results):,} coefficient rows; "
        f"{BOOTSTRAP_REPETITIONS:,} bootstraps per frame"
    )
    print(f"Saved: {report_path}")
    print(f"Manifest: {manifest_path}")


if __name__ == "__main__":
    main()
