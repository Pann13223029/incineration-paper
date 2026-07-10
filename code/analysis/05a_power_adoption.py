"""Sparse-event lineage analysis of first reported generation capacity."""

from __future__ import annotations

import os
import warnings
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
    sample_summary,
    write_stage_manifest,
)
from rare_event_utils import (
    bootstrap_covariance_wald_test,
    cluster_bootstrap_coefficients,
    fit_firth_logit,
    wald_test,
)


AGE_TERMS = ["age_10-19 yrs", "age_20-29 yrs", "age_30+ yrs"]
FOCAL_TERMS = [*AGE_TERMS, "log_processing_capacity"]
BOOTSTRAP_REPETITIONS = 499


def fit_firth_quietly(design: pd.DataFrame, outcome: pd.Series):
    """Suppress expected optimizer arithmetic warnings without hiding fit failures."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        return fit_firth_logit(design, outcome)


def build_hazard_design(frame: pd.DataFrame) -> pd.DataFrame:
    age = pd.get_dummies(
        frame["lag_age_band"],
        prefix="age",
        drop_first=True,
        dtype=float,
    )
    capacity = np.log1p(frame["lag_capacity_t_day"] / 100.0).rename(
        "log_processing_capacity"
    )
    era = pd.cut(
        frame["fiscal_year"],
        bins=[2004, 2009, 2014, 2019, 2024],
        labels=["FY2005-2009", "FY2010-2014", "FY2015-2019", "FY2020-2024"],
    )
    era_dummies = pd.get_dummies(
        era,
        prefix="calendar",
        drop_first=True,
        dtype=float,
    )
    duration = pd.cut(
        frame["elapsed_at_risk_years"],
        bins=[0, 4, 9, 14, np.inf],
        labels=["1-4", "5-9", "10-14", "15+"],
    )
    duration_dummies = pd.get_dummies(
        duration,
        prefix="duration",
        drop_first=True,
        dtype=float,
    )
    return sm.add_constant(
        pd.concat([age, capacity, era_dummies, duration_dummies], axis=1),
        has_constant="add",
    )


def fit_firth_frame(frame: pd.DataFrame, label: str) -> dict[str, Any]:
    design = build_hazard_design(frame)
    fit_frame = frame.copy()
    for column in design.columns:
        fit_frame[column] = design[column]
    fit_frame["event"] = fit_frame["adopt_power_this_year"].astype(float)
    result = fit_firth_quietly(design, fit_frame["event"])
    bootstrap = cluster_bootstrap_coefficients(
        fit_frame,
        list(design.columns),
        "event",
        "analysis_facility_id",
        repetitions=BOOTSTRAP_REPETITIONS,
    )
    model_based_age_test = wald_test(result, AGE_TERMS)
    bootstrap_age_test = bootstrap_covariance_wald_test(
        result.params,
        bootstrap,
        AGE_TERMS,
    )
    return {
        "label": label,
        "frame": frame,
        "design": design,
        "fit_frame": fit_frame,
        "result": result,
        "bootstrap": bootstrap,
        "age_wald_model_based": model_based_age_test,
        "age_wald_bootstrap": bootstrap_age_test,
    }


def fit_link_sensitivity(frame: pd.DataFrame, link) -> Any:
    design = build_hazard_design(frame)
    return sm.GLM(
        frame["adopt_power_this_year"].astype(float),
        design,
        family=sm.families.Binomial(link=link),
    ).fit(
        cov_type="cluster",
        cov_kwds={"groups": frame["analysis_facility_id"]},
    )


def coefficient_table(results: list[dict[str, Any]]) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for bundle in results:
        result = bundle["result"]
        bootstrap = bundle["bootstrap"]
        for term in FOCAL_TERMS:
            samples = bootstrap[term].dropna() if term in bootstrap else pd.Series(dtype=float)
            rows.append(
                {
                    "model": bundle["label"],
                    "term": term,
                    "coefficient": float(result.params[term]),
                    "standard_error_model_based": float(result.standard_errors[term]),
                    "ci_low_model_based": float(
                        result.params[term] - 1.96 * result.standard_errors[term]
                    ),
                    "ci_high_model_based": float(
                        result.params[term] + 1.96 * result.standard_errors[term]
                    ),
                    "p_value_model_based": float(result.pvalues[term]),
                    "bootstrap_ci_low": float(samples.quantile(0.025)),
                    "bootstrap_ci_high": float(samples.quantile(0.975)),
                    "odds_ratio": float(np.exp(result.params[term])),
                    "observations": int(len(bundle["frame"])),
                    "sites": int(bundle["frame"]["analysis_facility_id"].nunique()),
                    "events": int(bundle["frame"]["adopt_power_this_year"].sum()),
                }
            )
    return pd.DataFrame(rows)


def event_rate_tables(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    age = (
        frame.groupby("lag_age_band", observed=True)
        .agg(
            risk_rows=("adopt_power_this_year", "size"),
            events=("adopt_power_this_year", "sum"),
            mean_processing_capacity_t_day=("lag_capacity_t_day", "mean"),
        )
        .reset_index()
    )
    age["event_rate_pct"] = age["events"] / age["risk_rows"] * 100
    capacity = frame.copy()
    capacity["capacity_quartile"] = pd.qcut(
        capacity["lag_capacity_t_day"],
        4,
        labels=["Q1 smallest", "Q2", "Q3", "Q4 largest"],
        duplicates="drop",
    )
    capacity_table = (
        capacity.groupby("capacity_quartile", observed=True)
        .agg(
            risk_rows=("adopt_power_this_year", "size"),
            events=("adopt_power_this_year", "sum"),
            mean_processing_capacity_t_day=("lag_capacity_t_day", "mean"),
        )
        .reset_index()
    )
    capacity_table["event_rate_pct"] = (
        capacity_table["events"] / capacity_table["risk_rows"] * 100
    )
    return age, capacity_table


def exact_entry_events(adoption: pd.DataFrame) -> pd.DataFrame:
    ordered = adoption.sort_values(["analysis_facility_id", "fiscal_year"]).copy()
    group = ordered.groupby("analysis_facility_id", sort=False)
    ordered["lag_fiscal_year"] = group["fiscal_year"].shift(1)
    ordered["lag_throughput_t_year"] = group["throughput_t_year"].shift(1)
    events = ordered[
        ordered["adopt_power_this_year"].eq(1)
        & ordered["fiscal_year"].sub(ordered["lag_fiscal_year"]).eq(1)
    ].copy()
    return events.rename(columns={"fiscal_year": "event_year"})


def build_post_entry_evidence(
    panel: pd.DataFrame,
    adoption: pd.DataFrame,
    pathway: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    events = exact_entry_events(adoption)[
        [
            "analysis_facility_id",
            "event_year",
            "lag_throughput_t_year",
        ]
    ].copy()
    pathway_exact = pathway[pathway["exact_one_year_lag"]][
        ["analysis_facility_id", "fiscal_year", "pathway_category"]
    ].rename(columns={"fiscal_year": "event_year"})
    events = events.merge(
        pathway_exact,
        on=["analysis_facility_id", "event_year"],
        how="left",
        validate="one_to_one",
    )
    events["prior_site_operation"] = events["lag_throughput_t_year"].gt(0)

    observed = panel[
        [
            "stable_site_id",
            "fiscal_year",
            "has_power_gen",
            "power_generated_mwh",
        ]
    ].rename(columns={"stable_site_id": "analysis_facility_id"})
    bridge_rows: list[dict[str, Any]] = []
    for event in events.itertuples(index=False):
        site = observed[observed["analysis_facility_id"].eq(event.analysis_facility_id)]
        row: dict[str, Any] = {
            "analysis_facility_id": event.analysis_facility_id,
            "event_year": int(event.event_year),
            "pathway_category": event.pathway_category,
            "prior_site_operation": bool(event.prior_site_operation),
        }
        for horizon in range(4):
            target = int(event.event_year) + horizon
            target_rows = site[site["fiscal_year"].eq(target)]
            row[f"eligible_t{horizon}"] = target <= 2024
            row[f"observed_t{horizon}"] = not target_rows.empty
            row[f"positive_output_t{horizon}"] = bool(
                target_rows["power_generated_mwh"].fillna(0).gt(0).any()
            )
        bridge_rows.append(row)
    bridge = pd.DataFrame(bridge_rows)

    generator = build_regression_frame(panel)
    generator["gross_rank_pct"] = generator.groupby("fiscal_year")[
        "energy_efficiency_raw_mwh_per_t"
    ].rank(pct=True, method="average")
    generator["design_rank_pct"] = generator.groupby("fiscal_year")[
        "generator_design_intensity_kw_per_t_day"
    ].rank(pct=True, method="average")
    generator["capacity_factor_rank_pct"] = generator.groupby("fiscal_year")[
        "electrical_capacity_factor"
    ].rank(pct=True, method="average")
    trajectory = events.merge(generator, on="analysis_facility_id", how="left")
    trajectory["event_time"] = trajectory["fiscal_year"] - trajectory["event_year"]
    trajectory = trajectory[trajectory["event_time"].between(0, 3)].copy()
    trajectory["full_followup_eligible"] = trajectory["event_year"].le(2021)

    summary_rows: list[dict[str, Any]] = []
    grouping_specs = [
        ("All exact-year entrants", ["event_time"]),
        ("By pathway", ["pathway_category", "event_time"]),
    ]
    for series, columns in grouping_specs:
        for keys, group in trajectory.groupby(columns, dropna=False):
            if not isinstance(keys, tuple):
                keys = (keys,)
            key_map = dict(zip(columns, keys))
            summary_rows.append(
                {
                    "series": series,
                    "pathway_category": key_map.get("pathway_category", ""),
                    "event_time": int(key_map["event_time"]),
                    "rows": int(len(group)),
                    "events": int(group["analysis_facility_id"].nunique()),
                    "mean_gross_mwh_t": float(
                        group["energy_efficiency_raw_mwh_per_t"].mean()
                    ),
                    "median_gross_mwh_t": float(
                        group["energy_efficiency_raw_mwh_per_t"].median()
                    ),
                    "mean_gross_rank_pct": float(group["gross_rank_pct"].mean()),
                    "mean_design_rank_pct": float(group["design_rank_pct"].mean()),
                    "mean_capacity_factor_rank_pct": float(
                        group["capacity_factor_rank_pct"].mean()
                    ),
                    "full_followup_eligible_events": int(
                        group.loc[group["full_followup_eligible"], "analysis_facility_id"].nunique()
                    ),
                }
            )
    trajectory_summary = pd.DataFrame(summary_rows)
    summary = {
        "exact_events": int(len(events)),
        "event_year_positive_output": int(bridge["positive_output_t0"].sum()),
        "eligible_for_one_year": int(bridge["eligible_t1"].sum()),
        "positive_output_by_one_year": int(
            (
                bridge["positive_output_t0"]
                | bridge["positive_output_t1"]
            ).sum()
        ),
        "trajectory_rows": int(len(trajectory)),
        "trajectory_events": int(trajectory["analysis_facility_id"].nunique()),
        "event_time_one": {
            (
                "all"
                if row["series"] == "All exact-year entrants"
                else str(row["pathway_category"])
            ): {
                "rows": int(row["rows"]),
                "events": int(row["events"]),
                "mean_gross_mwh_t": float(row["mean_gross_mwh_t"]),
                "mean_gross_rank_pct": float(row["mean_gross_rank_pct"]),
                "mean_design_rank_pct": float(row["mean_design_rank_pct"]),
                "mean_capacity_factor_rank_pct": float(
                    row["mean_capacity_factor_rank_pct"]
                ),
            }
            for row in trajectory_summary.loc[
                trajectory_summary["event_time"].eq(1)
            ].to_dict(orient="records")
        },
    }
    return bridge, trajectory_summary, summary


def write_report(
    summary: dict[str, Any],
    broad: dict[str, Any],
    prior: dict[str, Any],
    continuity: dict[str, Any],
    identity_certain: dict[str, Any],
    coefficients: pd.DataFrame,
    age_rates: pd.DataFrame,
    capacity_rates: pd.DataFrame,
    pathway: pd.DataFrame,
    bridge_summary: dict[str, Any],
    link_sensitivity: dict[str, Any],
) -> None:
    path = os.path.join(OUTPUT_DIR, "adoption_results.md")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("# First Reported Installed-Generation-Capacity Entry\n\n")
        handle.write(
            "The event is the first stable-lineage observation with positive installed "
            "electrical-generation capacity after an observed non-generating history. "
            "It is not automatically a retrofit, first operation, or new physical site.\n\n"
        )
        handle.write("## Stable Administrative-Lineage Risk Set\n\n")
        handle.write(
            f"- Descriptive risk set: {summary['adoption_risk_obs']:,} rows across "
            f"{summary['adoption_risk_facilities']:,} lineages with "
            f"{summary['adoption_events']:,} observed events.\n"
        )
        handle.write(
            f"- Exact-year model: {summary['adoption_model_obs']:,} rows across "
            f"{summary['adoption_model_facilities']:,} lineages with "
            f"{summary['adoption_model_events']:,} events.\n"
        )
        handle.write(
            f"- Prior-operation model: {summary['adoption_prior_operation_obs']:,} "
            f"rows, {summary['adoption_prior_operation_sites']:,} lineages, and "
            f"{summary['adoption_prior_operation_events']:,} events.\n"
        )
        handle.write(
            f"- Same-asset-episode continuity sensitivity: "
            f"{len(continuity['frame']):,} rows, "
            f"{continuity['frame']['analysis_facility_id'].nunique():,} lineages, and "
            f"{int(continuity['frame']['adopt_power_this_year'].sum()):,} events.\n"
        )
        handle.write(
            f"- Identity-certain-lineage sensitivity: "
            f"{len(identity_certain['frame']):,} rows, "
            f"{identity_certain['frame']['analysis_facility_id'].nunique():,} lineages, and "
            f"{int(identity_certain['frame']['adopt_power_this_year'].sum()):,} events.\n"
        )
        handle.write(
            f"- Exact events without positive prior-year throughput: "
            f"{summary['adoption_nonpositive_prior_throughput_events']:,}.\n\n"
        )
        handle.write("## Bias-Reduced Hazard Results\n\n")
        handle.write(
            "Models use Firth bias reduction, log waste-processing design capacity, "
            "four calendar eras, flexible duration bands, and 499 stable-lineage cluster "
            "bootstrap replications. Coefficients are log-odds; waste-processing "
            "capacity is transformed as log(1 + t/day / 100). Bootstrap percentile "
            "intervals and joint age tests use complete-lineage resampling; standard "
            "errors and p-values in the machine-readable coefficient table are explicitly "
            "labelled model-based.\n\n"
        )
        display = coefficients[
            [
                "model",
                "term",
                "coefficient",
                "standard_error_model_based",
                "bootstrap_ci_low",
                "bootstrap_ci_high",
                "odds_ratio",
                "events",
            ]
        ]
        handle.write(display.to_markdown(index=False, floatfmt=".4f"))
        handle.write("\n\n")
        handle.write(
            f"- Broad-frame lineage-bootstrap-covariance joint age test: "
            f"chi-square={broad['age_wald_bootstrap'][0]:.2f}, "
            f"df={broad['age_wald_bootstrap'][1]}, "
            f"p={broad['age_wald_bootstrap'][2]:.4f}.\n"
        )
        handle.write(
            f"- Prior-operation lineage-bootstrap-covariance joint age test: "
            f"chi-square={prior['age_wald_bootstrap'][0]:.2f}, "
            f"df={prior['age_wald_bootstrap'][1]}, "
            f"p={prior['age_wald_bootstrap'][2]:.4f}.\n"
        )
        handle.write(
            f"- Same-episode continuity lineage-bootstrap-covariance joint age test: "
            f"chi-square={continuity['age_wald_bootstrap'][0]:.2f}, "
            f"df={continuity['age_wald_bootstrap'][1]}, "
            f"p={continuity['age_wald_bootstrap'][2]:.4f}.\n"
        )
        handle.write(
            f"- Identity-certain lineage-bootstrap-covariance joint age test: "
            f"chi-square={identity_certain['age_wald_bootstrap'][0]:.2f}, "
            f"df={identity_certain['age_wald_bootstrap'][1]}, "
            f"p={identity_certain['age_wald_bootstrap'][2]:.4f}.\n"
        )
        handle.write(
            "The prior-operation frame is a nested sensitivity, not an independent "
            "comparison group. The former two-event interaction contrast is not used "
            "as an equality or equivalence test.\n"
        )
        broad_capacity = broad["result"].params["log_processing_capacity"]
        prior_capacity = prior["result"].params["log_processing_capacity"]
        capacity_contrast = np.log1p(300 / 100) - np.log1p(100 / 100)
        handle.write(
            f"- Odds ratio comparing 300 with 100 t/day: broad "
            f"{np.exp(broad_capacity * capacity_contrast):.2f}; prior operation "
            f"{np.exp(prior_capacity * capacity_contrast):.2f}.\n\n"
        )
        handle.write("## Observed Exact-Year Rates\n\n")
        handle.write("### By prior reported age band\n\n")
        handle.write(age_rates.to_markdown(index=False, floatfmt=".3f"))
        handle.write("\n\n### By waste-processing design-capacity quartile\n\n")
        handle.write(capacity_rates.to_markdown(index=False, floatfmt=".3f"))
        handle.write("\n\n## Transition Pathways\n\n")
        pathway_counts = (
            pathway.groupby("pathway_category", as_index=False)
            .size()
            .rename(columns={"size": "events"})
        )
        handle.write(pathway_counts.to_markdown(index=False))
        handle.write("\n\n")
        handle.write(
            "`Continuity-lineage entry` requires an exact adjacent-year observation in "
            "the same administrative lineage and asset episode. `Rebuild/replacement-like` records "
            "an asset-episode or start-year reset; neither category proves a causal mechanism.\n\n"
        )
        handle.write("## Post-Entry Bridge\n\n")
        handle.write(
            f"The bridge uses {bridge_summary['exact_events']:,} exact-year events only. "
            f"{bridge_summary['event_year_positive_output']:,} report positive output in "
            f"the event year, and {bridge_summary['positive_output_by_one_year']:,} report "
            "positive output by the following observed fiscal year. Pathway-stratified "
            "first-complete-year component results are stored in "
            "`post_adoption_trajectories.csv`.\n\n"
        )
        handle.write("## Link Sensitivity\n\n")
        handle.write(
            f"The complementary-log-log capacity coefficient is "
            f"{link_sensitivity['cloglog_capacity']:.4f}; the conventional logit "
            f"coefficient is {link_sensitivity['logit_capacity']:.4f}. These are "
            "specification checks, not additional hypotheses.\n\n"
        )
        handle.write(
            "Administrative disappearance is not modeled because closure, recoding, "
            "consolidation, and reporting change cannot be separated without external "
            "facility histories.\n"
        )


def main() -> None:
    panel = load_panel()
    adoption = build_adoption_frame(panel)
    exact = build_adoption_model_frame(adoption=adoption)
    summary = sample_summary(panel)
    prior_frame = exact[exact["lag_throughput_t_year"].gt(0)].copy()
    continuity_frame = exact[exact["same_asset_episode_as_lag"]].copy()
    uncertain_lineages = set(
        panel.loc[panel["identity_match_uncertain"], "stable_site_id"].astype(str)
    )
    identity_certain_frame = exact[
        ~exact["analysis_facility_id"].astype(str).isin(uncertain_lineages)
    ].copy()

    broad = fit_firth_frame(exact, "Broad exact-year risk frame")
    prior = fit_firth_frame(prior_frame, "Prior-operation risk frame")
    continuity = fit_firth_frame(
        continuity_frame,
        "Same-asset-episode continuity sensitivity",
    )
    identity_certain = fit_firth_frame(
        identity_certain_frame,
        "Identity-certain-lineage sensitivity",
    )
    fitted_models = {
        "broad": broad["result"],
        "prior_operation": prior["result"],
        "same_episode_continuity": continuity["result"],
        "identity_certain": identity_certain["result"],
    }
    failed_fits = [
        label for label, result in fitted_models.items() if not result.converged
    ]
    if failed_fits:
        raise RuntimeError(
            "Firth model failed to converge: " + ", ".join(failed_fits)
        )
    bootstrap_counts = {
        "broad": int(broad["bootstrap"]["repetition"].nunique()),
        "prior_operation": int(prior["bootstrap"]["repetition"].nunique()),
        "same_episode_continuity": int(
            continuity["bootstrap"]["repetition"].nunique()
        ),
        "identity_certain": int(
            identity_certain["bootstrap"]["repetition"].nunique()
        ),
    }
    if set(bootstrap_counts.values()) != {BOOTSTRAP_REPETITIONS}:
        raise RuntimeError(
            "Cluster bootstrap did not retain every requested replication: "
            f"{bootstrap_counts}"
        )
    bootstrap_term_counts = {
        label: {
            term: int(bundle["bootstrap"][term].notna().sum())
            for term in FOCAL_TERMS
        }
        for label, bundle in {
            "broad": broad,
            "prior_operation": prior,
            "same_episode_continuity": continuity,
            "identity_certain": identity_certain,
        }.items()
    }
    if any(
        count != BOOTSTRAP_REPETITIONS
        for counts in bootstrap_term_counts.values()
        for count in counts.values()
    ):
        raise RuntimeError(
            "Cluster bootstrap has incomplete focal-term estimates: "
            f"{bootstrap_term_counts}"
        )
    coefficients = coefficient_table([broad, prior, continuity, identity_certain])
    age_rates, capacity_rates = event_rate_tables(exact)
    pathway = build_adoption_pathway_audit(panel, adoption=adoption)
    bridge, trajectories, bridge_summary = build_post_entry_evidence(
        panel,
        adoption,
        pathway,
    )
    logit = fit_link_sensitivity(exact, sm.families.links.Logit())
    cloglog = fit_link_sensitivity(exact, sm.families.links.CLogLog())
    link_sensitivity = {
        "logit_capacity": float(logit.params["log_processing_capacity"]),
        "cloglog_capacity": float(cloglog.params["log_processing_capacity"]),
    }

    coefficient_path = os.path.join(OUTPUT_DIR, "figure2_transition_effects.csv")
    coefficients.to_csv(coefficient_path, index=False, float_format="%.10g")
    bootstrap_path = os.path.join(OUTPUT_DIR, "adoption_bootstrap_coefficients.csv")
    broad_bootstrap = broad["bootstrap"].assign(model="broad")
    prior_bootstrap = prior["bootstrap"].assign(model="prior_operation")
    continuity_bootstrap = continuity["bootstrap"].assign(
        model="same_episode_continuity"
    )
    identity_certain_bootstrap = identity_certain["bootstrap"].assign(
        model="identity_certain"
    )
    pd.concat(
        [
            broad_bootstrap,
            prior_bootstrap,
            continuity_bootstrap,
            identity_certain_bootstrap,
        ],
        ignore_index=True,
    ).to_csv(
        bootstrap_path,
        index=False,
        float_format="%.10g",
    )
    pathway_path = os.path.join(OUTPUT_DIR, "adoption_pathway_audit.csv")
    pathway.to_csv(pathway_path, index=False, float_format="%.10g")
    bridge_path = os.path.join(OUTPUT_DIR, "post_adoption_bridge.csv")
    bridge.to_csv(bridge_path, index=False, float_format="%.10g")
    trajectory_path = os.path.join(OUTPUT_DIR, "post_adoption_trajectories.csv")
    trajectories.to_csv(trajectory_path, index=False, float_format="%.10g")

    write_report(
        summary,
        broad,
        prior,
        continuity,
        identity_certain,
        coefficients,
        age_rates,
        capacity_rates,
        pathway,
        bridge_summary,
        link_sensitivity,
    )
    report_path = os.path.join(OUTPUT_DIR, "adoption_results.md")
    manifest_path = write_stage_manifest(
        "05a_power_adoption",
        inputs=["data/processed/incineration_panel_identified.csv"],
        outputs=[
            "output/adoption_results.md",
            "output/adoption_pathway_audit.csv",
            "output/figure2_transition_effects.csv",
            "output/adoption_bootstrap_coefficients.csv",
            "output/post_adoption_bridge.csv",
            "output/post_adoption_trajectories.csv",
        ],
        metadata={
            "risk_set_rows": int(len(adoption)),
            "risk_set_sites": int(adoption["analysis_facility_id"].nunique()),
            "descriptive_events": int(adoption["adopt_power_this_year"].sum()),
            "exact_model_rows": int(len(exact)),
            "exact_model_sites": int(exact["analysis_facility_id"].nunique()),
            "exact_model_events": int(exact["adopt_power_this_year"].sum()),
            "prior_operation_rows": int(len(prior_frame)),
            "prior_operation_sites": int(
                prior_frame["analysis_facility_id"].nunique()
            ),
            "prior_operation_events": int(
                prior_frame["adopt_power_this_year"].sum()
            ),
            "same_episode_continuity_rows": int(len(continuity_frame)),
            "same_episode_continuity_sites": int(
                continuity_frame["analysis_facility_id"].nunique()
            ),
            "same_episode_continuity_events": int(
                continuity_frame["adopt_power_this_year"].sum()
            ),
            "identity_certain_rows": int(len(identity_certain_frame)),
            "identity_certain_sites": int(
                identity_certain_frame["analysis_facility_id"].nunique()
            ),
            "identity_certain_events": int(
                identity_certain_frame["adopt_power_this_year"].sum()
            ),
            "uncertain_identity_lineages": int(len(uncertain_lineages)),
            "cross_episode_exact_rows": int(
                (~exact["same_asset_episode_as_lag"]).sum()
            ),
            "cross_episode_exact_events": int(
                exact.loc[
                    ~exact["same_asset_episode_as_lag"],
                    "adopt_power_this_year",
                ].sum()
            ),
            "bias_reduction": "Firth Jeffreys-prior penalization",
            "bootstrap_repetitions": BOOTSTRAP_REPETITIONS,
            "bootstrap_successful_repetitions": bootstrap_counts,
            "bootstrap_complete_focal_terms": bootstrap_term_counts,
            "model_convergence": {
                label: {
                    "converged": bool(result.converged),
                    "iterations": int(result.iterations),
                }
                for label, result in fitted_models.items()
            },
            "broad_coefficients": {
                term: float(broad["result"].params[term]) for term in FOCAL_TERMS
            },
            "prior_operation_coefficients": {
                term: float(prior["result"].params[term]) for term in FOCAL_TERMS
            },
            "same_episode_continuity_coefficients": {
                term: float(continuity["result"].params[term])
                for term in FOCAL_TERMS
            },
            "identity_certain_coefficients": {
                term: float(identity_certain["result"].params[term])
                for term in FOCAL_TERMS
            },
            "joint_age_tests": {
                "broad_cluster_bootstrap_covariance": list(
                    broad["age_wald_bootstrap"]
                ),
                "prior_operation_cluster_bootstrap_covariance": list(
                    prior["age_wald_bootstrap"]
                ),
                "same_episode_cluster_bootstrap_covariance": list(
                    continuity["age_wald_bootstrap"]
                ),
                "identity_certain_cluster_bootstrap_covariance": list(
                    identity_certain["age_wald_bootstrap"]
                ),
                "broad_model_based": list(broad["age_wald_model_based"]),
                "prior_operation_model_based": list(
                    prior["age_wald_model_based"]
                ),
                "same_episode_model_based": list(
                    continuity["age_wald_model_based"]
                ),
                "identity_certain_model_based": list(
                    identity_certain["age_wald_model_based"]
                ),
            },
            "pathway_counts": {
                str(key): int(value)
                for key, value in pathway["pathway_category"].value_counts().items()
            },
            "post_entry": bridge_summary,
            "link_sensitivity": link_sensitivity,
        },
    )
    print(f"Exact-year events: {int(exact['adopt_power_this_year'].sum()):,}")
    print(f"Saved: {report_path}")
    print(f"Manifest: {manifest_path}")


if __name__ == "__main__":
    main()
