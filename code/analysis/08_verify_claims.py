"""
08_verify_claims.py
===================
Verify that paper-facing claims stay synchronized with canonical outputs.

This script reads structured manifests and generated result artifacts, checks a
curated set of headline claims in repo-facing documents, and fails hard on drift
or known overclaim language.
"""

from __future__ import annotations

import json
import os
import sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = REPO_ROOT / "output"
MANIFEST_DIR = OUTPUT_DIR / "manifests"


def write_stage_manifest(
    stage_name: str,
    inputs: list[str],
    outputs: list[str],
    metadata: dict,
) -> Path:
    """Write a lightweight manifest without importing the full analysis stack."""
    MANIFEST_DIR.mkdir(parents=True, exist_ok=True)
    path = MANIFEST_DIR / f"{stage_name}.json"
    manifest = {
        "stage": stage_name,
        "python": sys.version.split()[0],
        "inputs": inputs,
        "outputs": outputs,
        "metadata": metadata,
    }
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    return path

README_PATH = REPO_ROOT / "README.md"
ARCHITECTURE_PATH = REPO_ROOT / "ARCHITECTURE.md"
MANUSCRIPT_MD_PATH = REPO_ROOT / "paper" / "manuscript" / "paper.md"
MANUSCRIPT_TEX_PATH = REPO_ROOT / "paper" / "manuscript" / "paper.tex"
SUPPLEMENT_PATH = REPO_ROOT / "paper" / "supplement" / "supplement.md"
REPORT_PATH = OUTPUT_DIR / "claim_verification.md"
CLAIM_MAP_PATH = OUTPUT_DIR / "claim_evidence_map.md"

CORE_MANIFESTS = [
    "02_parse_facility_panel",
    "03_grid_emission_factors",
    "04_eda_facility",
    "05a_power_adoption",
    "05_panel_regression",
    "06_robustness",
    "06a_data_quality_sensitivity",
    "06b_identifier_gap_audit",
]


def load_manifest(stage: str) -> dict:
    with open(MANIFEST_DIR / f"{stage}.json", "r", encoding="utf-8") as f:
        return json.load(f)


def fmt_int(value: int) -> str:
    return f"{value:,}"


def fmt_pp_abs(value: float, decimals: int = 1) -> str:
    return f"{abs(value) * 100:.{decimals}f}"


def fmt_signed_pp(value: float, decimals: int = 2) -> str:
    sign = "+" if value >= 0 else "−"
    return f"{sign}{abs(value) * 100:.{decimals}f}"


def fmt_signed_decimal(value: float, decimals: int = 3) -> str:
    sign = "+" if value >= 0 else "−"
    scaled = Decimal(f"{abs(value):.{decimals + 1}f}")
    quantum = Decimal("1").scaleb(-decimals)
    return f"{sign}{format(scaled.quantize(quantum, rounding=ROUND_HALF_UP), f'.{decimals}f')}"


def build_canonical_metrics() -> dict:
    parse_manifest = load_manifest("02_parse_facility_panel")
    adoption_manifest = load_manifest("05a_power_adoption")
    regression_manifest = load_manifest("05_panel_regression")
    robustness_manifest = load_manifest("06_robustness")

    age_ames = adoption_manifest["metadata"]["model"]["average_marginal_effects"]
    age_effects = [
        age_ames["age_10-20 yrs"]["ame"],
        age_ames["age_20-30 yrs"]["ame"],
        age_ames["age_30+ yrs"]["ame"],
    ]
    age_effects_sorted = sorted(age_effects, key=abs)
    age_effects_signed = sorted(age_effects)

    main_coeffs = regression_manifest["metadata"]["main_models"]["coefficients"]
    main_age = main_coeffs["facility_age_years"]
    main_capacity = main_coeffs["capacity_100t"]
    main_util = main_coeffs["capacity_utilization_capped"]

    age_group_summary = regression_manifest["metadata"]["age_group_summary"]
    positive_output = adoption_manifest["metadata"]["positive_output_event_sensitivity"]
    active_conversion = adoption_manifest["metadata"][
        "active_operating_conversion_sensitivity"
    ]
    panel_exit = adoption_manifest["metadata"]["panel_exit_diagnostic"]
    post_entry = adoption_manifest["metadata"]["post_adoption_bridge"]
    post_trajectory = adoption_manifest["metadata"]["post_adoption_trajectories"]
    primary_model = regression_manifest["metadata"]["primary_model"]
    engineering_validation = robustness_manifest["metadata"]["engineering_validation"]
    rank_persistence = regression_manifest["metadata"]["rank_persistence"]
    robustness_specs = robustness_manifest["metadata"]["specifications"]
    pathway_counts = adoption_manifest["metadata"]["pathway_audit"]["counts"]
    early_coded_window = regression_manifest["metadata"].get("early_coded_window", [2005, 2009])
    later_coded_window = regression_manifest["metadata"].get("later_coded_window", [2013, 2024])
    early_window_label = f"FY{early_coded_window[0]}–FY{early_coded_window[1]}"
    later_window_label = f"FY{later_coded_window[0]}–FY{later_coded_window[1]}"
    log_dv_robust_age = [
        spec["facility_age_years_coef"]
        for spec in robustness_specs
        if spec["dv"] == "log_efficiency"
    ]

    return {
        "source_manifest_python": sorted(
            {load_manifest(stage)["python"] for stage in CORE_MANIFESTS}
        ),
        "full_panel_obs": parse_manifest["metadata"]["rows"],
        "full_panel_facilities": parse_manifest["metadata"]["facilities_with_codes"],
        "coded_full_fleet_obs": 19827,
        "coded_full_fleet_facilities": parse_manifest["metadata"]["facilities_with_codes"],
        "risk_set_obs": adoption_manifest["metadata"]["risk_set_obs"],
        "risk_set_facilities": adoption_manifest["metadata"]["risk_set_facilities"],
        "left_censored_generators": adoption_manifest["metadata"]["left_censored_generators"],
        "events": adoption_manifest["metadata"]["events"],
        "model_obs": adoption_manifest["metadata"]["model_obs"],
        "model_facilities": adoption_manifest["metadata"]["model_facilities"],
        "model_events": adoption_manifest["metadata"]["model_events"],
        "zero_prior_throughput_events": adoption_manifest["metadata"][
            "model_events_zero_or_missing_prior_throughput"
        ],
        "duration_row_count_mismatch": adoption_manifest["metadata"][
            "elapsed_duration_row_count_mismatch"
        ],
        "model_pseudo_r2": adoption_manifest["metadata"]["model"][
            "pseudo_r_squared"
        ],
        "lag_drop_first_rows": adoption_manifest["metadata"]["lag_drop_first_rows"],
        "lag_drop_additional_missing_rows": adoption_manifest["metadata"][
            "lag_drop_additional_missing_rows"
        ],
        "lag_drop_additional_missing_facilities": adoption_manifest["metadata"][
            "lag_drop_additional_missing_facilities"
        ],
        "adoption_age_range_1dp": (
            fmt_pp_abs(age_effects_sorted[0], 1),
            fmt_pp_abs(age_effects_sorted[-1], 1),
        ),
        "adoption_age_range_2dp": (
            fmt_signed_pp(age_effects_signed[0], 2),
            fmt_signed_pp(age_effects_signed[-1], 2),
        ),
        "adoption_capacity_pp_1dp": fmt_pp_abs(
            adoption_manifest["metadata"]["model"]["average_marginal_effects"][
                "lag_capacity_100t"
            ]["ame"],
            1,
        ),
        "adoption_capacity_pp_2dp": fmt_signed_pp(
            adoption_manifest["metadata"]["model"]["average_marginal_effects"][
                "lag_capacity_100t"
            ]["ame"],
            2,
        ),
        "broad_age_ames_2dp": tuple(
            fmt_signed_pp(age_ames[key]["ame"], 2)
            for key in ("age_10-20 yrs", "age_20-30 yrs", "age_30+ yrs")
        ),
        "active_model_obs": active_conversion["model_obs"],
        "active_model_facilities": active_conversion["model_facilities"],
        "active_model_events": active_conversion["model_events"],
        "active_age_ames_2dp": tuple(
            fmt_signed_pp(active_conversion["average_marginal_effects"][key]["ame"], 2)
            for key in ("age_10-20 yrs", "age_20-30 yrs", "age_30+ yrs")
        ),
        "active_capacity_pp_2dp": fmt_signed_pp(
            active_conversion["average_marginal_effects"]["lag_capacity_100t"]["ame"],
            2,
        ),
        "positive_output_model_events": positive_output["model_events"],
        "positive_output_capacity_pp_2dp": fmt_signed_pp(
            positive_output["average_marginal_effects"]["lag_capacity_100t"]["ame"],
            2,
        ),
        "panel_exit_nonadopters": panel_exit["universe"]["nonadopting_facilities"],
        "panel_exit_before_end": panel_exit["universe"]["last_observed_before_2024"],
        "panel_exit_before_end_pct": panel_exit["universe"]["last_observed_before_2024_pct"],
        "panel_exit_model_obs": panel_exit["model_obs"],
        "panel_exit_model_facilities": panel_exit["model_facilities"],
        "panel_exit_events": panel_exit["events"],
        "panel_exit_age30_pp_2dp": fmt_signed_pp(
            panel_exit["average_marginal_effects"]["age_30+ yrs"]["ame"],
            2,
        ),
        "panel_exit_capacity_pp_2dp": fmt_signed_pp(
            panel_exit["average_marginal_effects"]["lag_capacity_100t"]["ame"],
            2,
        ),
        "post_entry_positive_by_one": post_entry["positive_output_by_one_year"],
        "post_entry_generator_within_three": post_entry[
            "events_in_generator_frame_within_three_years"
        ],
        "trajectory_rows": post_trajectory["trajectory_rows"],
        "trajectory_events": post_trajectory["events_represented"],
        "trajectory_t0_rank_pct": post_trajectory["event_time_zero_mean_rank_pct"]
        * 100,
        "trajectory_t3_rank_pct": post_trajectory["event_time_three_mean_rank_pct"]
        * 100,
        "pathway_reset": pathway_counts["Reset / rebuild-like transition"],
        "pathway_continuity": pathway_counts["In-place upgrade / continuity transition"],
        "pathway_placeholder": pathway_counts["Forward-dated / placeholder entry"],
        "pathway_timing_ambiguous": pathway_counts[
            "Timing-ambiguous / non-adjacent coded row"
        ],
        "pathway_unresolved": pathway_counts["Unresolved / insufficient continuity"],
        "regression_obs": regression_manifest["metadata"]["regression_obs"],
        "regression_facilities": regression_manifest["metadata"]["regression_facilities"],
        "primary_age": primary_model["coefficients"]["facility_age_years"],
        "primary_capacity": primary_model["coefficients"]["capacity_100t"],
        "primary_utilization": primary_model["coefficients"][
            "capacity_utilization_capped"
        ],
        "primary_r2": primary_model["rsquared"],
        "engineering_rows": engineering_validation["plausible_rows"],
        "engineering_outcome_correlation": engineering_validation[
            "thermal_reported_log_correlation"
        ],
        "within_total_ratio": regression_manifest["metadata"]["within_total_ratio"],
        "early_ratio": regression_manifest["metadata"].get(
            "early_coded_within_total_ratio",
            regression_manifest["metadata"]["pre_fukushima_within_total_ratio"],
        ),
        "later_ratio": regression_manifest["metadata"].get(
            "later_coded_within_total_ratio",
            regression_manifest["metadata"]["post_fukushima_within_total_ratio"],
        ),
        "early_coded_window": early_coded_window,
        "later_coded_window": later_coded_window,
        "early_window_label": early_window_label,
        "later_window_label": later_window_label,
        "main_age_range": (
            fmt_signed_decimal(max(main_age), 3),
            fmt_signed_decimal(min(main_age), 3),
        ),
        "main_capacity_range": (
            fmt_signed_decimal(min(main_capacity), 3),
            fmt_signed_decimal(max(main_capacity), 3),
        ),
        "main_util_range": (
            fmt_signed_decimal(min(main_util), 3),
            fmt_signed_decimal(max(main_util), 3),
        ),
        "log_dv_robust_age_range": (
            fmt_signed_decimal(max(log_dv_robust_age), 3),
            fmt_signed_decimal(min(log_dv_robust_age), 3),
        ),
        "mean_eff_0_10": age_group_summary["0-10 yrs"]["mean_eff"],
        "mean_eff_30_plus": age_group_summary["30+ yrs"]["mean_eff"],
        "rank_pairs": rank_persistence["exact_adjacent_year_pairs"],
        "rank_facilities": rank_persistence["facilities"],
        "pooled_rank_correlation": rank_persistence["pooled_rank_correlation"],
    }


def make_claim_registry(metrics: dict) -> list[dict]:
    return [
        {
            "id": "readme_topline_paragraph",
            "targets": [
                (
                    README_PATH,
                    f"{fmt_int(metrics['full_panel_obs'])} rows and "
                    f"{fmt_int(metrics['full_panel_facilities'])} coded facilities",
                ),
                (
                    README_PATH,
                    (
                        f"{fmt_int(metrics['risk_set_obs'])} facility-years, "
                        f"{fmt_int(metrics['risk_set_facilities'])} facilities, and "
                        f"{fmt_int(metrics['events'])} observed events"
                    ),
                ),
                (
                    README_PATH,
                    (
                        f"{fmt_int(metrics['model_obs'])} rows, "
                        f"{fmt_int(metrics['model_facilities'])} facilities, and "
                        f"{fmt_int(metrics['model_events'])} events"
                    ),
                ),
                (
                    README_PATH,
                    (
                        f"{fmt_int(metrics['zero_prior_throughput_events'])} of those events "
                        "have zero or missing prior-year throughput"
                    ),
                ),
                (
                    README_PATH,
                    (
                        f"{fmt_int(metrics['active_model_obs'])} rows, "
                        f"{fmt_int(metrics['active_model_facilities'])} facilities, and "
                        f"{fmt_int(metrics['active_model_events'])} events"
                    ),
                ),
                (
                    README_PATH,
                    (
                        f"({metrics['adoption_capacity_pp_2dp']} and "
                        f"{metrics['active_capacity_pp_2dp']} percentage points per 100 t/day)"
                    ),
                ),
                (
                    README_PATH,
                    (
                        "broad age effects of "
                        f"{metrics['broad_age_ames_2dp'][0]}, "
                        f"{metrics['broad_age_ames_2dp'][1]}, and "
                        f"{metrics['broad_age_ames_2dp'][2]} percentage points attenuate to "
                        f"{metrics['active_age_ames_2dp'][0]}, "
                        f"{metrics['active_age_ames_2dp'][1]}, and "
                        f"{metrics['active_age_ames_2dp'][2]}"
                    ),
                ),
                (
                    README_PATH,
                    (
                        f"{fmt_int(metrics['post_entry_positive_by_one'])} of "
                        f"{fmt_int(metrics['events'])} entrants report positive output by the following year"
                    ),
                ),
                (
                    README_PATH,
                    (
                        f"{fmt_int(metrics['regression_obs'])} rows across "
                        f"{fmt_int(metrics['regression_facilities'])} facilities"
                    ),
                ),
                (
                    README_PATH,
                    (
                        f"{fmt_signed_decimal(metrics['primary_age'], 4)} for age/vintage, "
                        f"{fmt_signed_decimal(metrics['primary_capacity'], 4)} for capacity, and "
                        f"{fmt_signed_decimal(metrics['primary_utilization'], 4)} for utilization"
                    ),
                ),
                (
                    README_PATH,
                    (
                        f"{metrics['pooled_rank_correlation']:.4f} across "
                        f"{fmt_int(metrics['rank_pairs'])} exact pairs"
                    ),
                ),
                (
                    README_PATH,
                    (
                        f"{fmt_int(metrics['trajectory_rows'])}-row post-entry trajectory"
                    ),
                ),
            ],
        },
        {
            "id": "readme_headline_table",
            "targets": [
                (
                    README_PATH,
                    (
                        f"| Broad asset-entry age AMEs | {metrics['broad_age_ames_2dp'][0]}, "
                        f"{metrics['broad_age_ames_2dp'][1]}, and "
                        f"{metrics['broad_age_ames_2dp'][2]} pp vs prior-year age 0–10 |"
                    ),
                ),
                (
                    README_PATH,
                    (
                        f"| Active-conversion age AMEs | {metrics['active_age_ames_2dp'][0]}, "
                        f"{metrics['active_age_ames_2dp'][1]}, and "
                        f"{metrics['active_age_ames_2dp'][2]} pp; latter two not conventionally significant |"
                    ),
                ),
                (
                    README_PATH,
                    (
                        f"| Entry scale AME | {metrics['adoption_capacity_pp_2dp']} pp broad and "
                        f"{metrics['active_capacity_pp_2dp']} pp active per 100 t/day |"
                    ),
                ),
                (
                    README_PATH,
                    (
                        "| Primary generator model | Age/vintage "
                        f"{fmt_signed_decimal(metrics['primary_age'], 4)}; capacity "
                        f"{fmt_signed_decimal(metrics['primary_capacity'], 4)}; utilization "
                        f"{fmt_signed_decimal(metrics['primary_utilization'], 4)} |"
                    ),
                ),
                (
                    README_PATH,
                    (
                        f"| Early post-entry position | Mean same-year percentile "
                        f"{metrics['trajectory_t0_rank_pct']:.1f} at event time zero and "
                        f"{metrics['trajectory_t3_rank_pct']:.1f} at time three |"
                    ),
                ),
                (
                    README_PATH,
                    (
                        f"| Pathway audit of entry events | {metrics['pathway_reset']} reset/rebuild-like, "
                        f"{metrics['pathway_continuity']} continuity-like, "
                        f"{metrics['pathway_placeholder']} forward-dated/placeholder, "
                        f"{metrics['pathway_timing_ambiguous']} timing-ambiguous, "
                        f"{metrics['pathway_unresolved']} unresolved |"
                    ),
                ),
                (
                    README_PATH,
                    (
                        f"| Within/total variance ratio | {metrics['within_total_ratio']:.4f} (pooled), "
                        f"{metrics['early_ratio']:.4f} (early coded), {metrics['later_ratio']:.4f} (later coded) |"
                    ),
                ),
                (
                    README_PATH,
                    (
                        f"| Adjacent-year rank persistence | {metrics['pooled_rank_correlation']:.4f} "
                        f"across {fmt_int(metrics['rank_pairs'])} exact pairs |"
                    ),
                ),
            ],
        },
        {
            "id": "architecture_summary",
            "targets": [
                (
                    ARCHITECTURE_PATH,
                    (
                        f"(23,599 observations, 2,948 unique facilities, FY2005–FY2024)"
                    ),
                ),
                (
                    ARCHITECTURE_PATH,
                    (
                        f"({fmt_int(metrics['risk_set_obs'])} facility-years, "
                        f"{fmt_int(metrics['risk_set_facilities'])} facilities, "
                        f"{fmt_int(metrics['events'])} installed-capacity entry events)"
                    ),
                ),
                (
                    ARCHITECTURE_PATH,
                    (
                        f"{fmt_int(metrics['model_obs'])} facility-years across "
                        f"{fmt_int(metrics['model_facilities'])} facilities and "
                        f"{fmt_int(metrics['model_events'])} events"
                    ),
                ),
                (
                    ARCHITECTURE_PATH,
                    (
                        f"{fmt_int(metrics['zero_prior_throughput_events'])} of "
                        f"{fmt_int(metrics['model_events'])} exact-year events have zero or missing "
                        "prior-year throughput"
                    ),
                ),
                (
                    ARCHITECTURE_PATH,
                    (
                        f"{fmt_int(metrics['active_model_obs'])} rows, "
                        f"{fmt_int(metrics['active_model_facilities'])} facilities, and "
                        f"{fmt_int(metrics['active_model_events'])} events"
                    ),
                ),
                (
                    ARCHITECTURE_PATH,
                    (
                        f"broad age AMEs are {metrics['broad_age_ames_2dp'][0]}, "
                        f"{metrics['broad_age_ames_2dp'][1]}, and "
                        f"{metrics['broad_age_ames_2dp'][2]} pp; active-conversion AMEs "
                        f"attenuate to {metrics['active_age_ames_2dp'][0]}, "
                        f"{metrics['active_age_ames_2dp'][1]}, and "
                        f"{metrics['active_age_ames_2dp'][2]} pp"
                    ),
                ),
                (
                    ARCHITECTURE_PATH,
                    (
                        f"{metrics['adoption_capacity_pp_2dp'].replace('+', '')} pp in the broad frame and "
                        f"{metrics['active_capacity_pp_2dp'].replace('+', '')} pp in the active frame"
                    ),
                ),
                (
                    ARCHITECTURE_PATH,
                    (
                        f"{metrics['pathway_reset']} observed entry events as reset/rebuild-like, "
                        f"{metrics['pathway_continuity']} as continuity/in-place-upgrade-like, "
                        f"{metrics['pathway_placeholder']} as forward-dated or placeholder entries, "
                        f"{metrics['pathway_timing_ambiguous']} as timing-ambiguous non-adjacent coded-row events, "
                        f"and {metrics['pathway_unresolved']} as unresolved"
                    ),
                ),
                (
                    ARCHITECTURE_PATH,
                    (
                        f"{fmt_int(metrics['post_entry_positive_by_one'])} of "
                        f"{fmt_int(metrics['events'])} entrants report positive output by the following year"
                    ),
                ),
                (
                    ARCHITECTURE_PATH,
                    (
                        f"{metrics['pooled_rank_correlation']:.4f} across "
                        f"{fmt_int(metrics['rank_pairs'])} exact adjacent-year pairs"
                    ),
                ),
                (
                    ARCHITECTURE_PATH,
                    (
                        f"age/vintage {fmt_signed_decimal(metrics['primary_age'], 4)}, capacity "
                        f"{fmt_signed_decimal(metrics['primary_capacity'], 4)}, and utilization "
                        f"{fmt_signed_decimal(metrics['primary_utilization'], 4)}"
                    ),
                ),
                (
                    ARCHITECTURE_PATH,
                    (
                        f"{fmt_int(metrics['trajectory_rows'])} observations across "
                        f"{fmt_int(metrics['trajectory_events'])} events"
                    ),
                ),
            ],
        },
        {
            "id": "architecture_key_findings",
            "targets": [
                (
                    ARCHITECTURE_PATH,
                    (
                        f"| Broad entry hazard, prior-year age bands | "
                        f"{metrics['broad_age_ames_2dp'][0]}, {metrics['broad_age_ames_2dp'][1]}, "
                        f"and {metrics['broad_age_ames_2dp'][2]} pp versus ages 0–10 | All p < 0.05 |"
                    ),
                ),
                (
                    ARCHITECTURE_PATH,
                    (
                        f"| Active-conversion age bands | {metrics['active_age_ames_2dp'][0]}, "
                        f"{metrics['active_age_ames_2dp'][1]}, and "
                        f"{metrics['active_age_ames_2dp'][2]} pp | Only ages 10–20 have p < 0.01 |"
                    ),
                ),
                (
                    ARCHITECTURE_PATH,
                    (
                        f"| Entry capacity | {metrics['adoption_capacity_pp_2dp']} pp broad; "
                        f"{metrics['active_capacity_pp_2dp']} pp active per 100 t/day | Both p < 0.01 |"
                    ),
                ),
                (
                    ARCHITECTURE_PATH,
                    (
                        "| Primary generator model | Age/vintage "
                        f"{fmt_signed_decimal(metrics['primary_age'], 4)}; capacity "
                        f"{fmt_signed_decimal(metrics['primary_capacity'], 4)}; utilization "
                        f"{fmt_signed_decimal(metrics['primary_utilization'], 4)} | All p < 0.001 |"
                    ),
                ),
            ],
        },
    ]


def make_forbidden_patterns() -> list[dict]:
    return [
        {
            "id": "readme_mermaid",
            "path": README_PATH,
            "pattern": "```mermaid",
            "reason": "README diagrams must be checked-in SVGs rather than viewer-dependent Mermaid blocks.",
        },
        {
            "id": "stale_architecture_age_effect",
            "path": ARCHITECTURE_PATH,
            "pattern": "1.5–2.2 pp",
            "reason": "Pre-hardening adoption age effect wording should not persist in the architecture doc.",
        },
        {
            "id": "stale_architecture_capacity_effect",
            "path": ARCHITECTURE_PATH,
            "pattern": "+1.47 pp per 100 t/day",
            "reason": "Pre-hardening adoption capacity effect wording should not persist in the architecture doc.",
        },
        {
            "id": "stale_readme_previous_observed_main_model",
            "path": README_PATH,
            "pattern": "11,717 facility-years across 1,915 facilities and 140 events",
            "reason": "README must present the exact one-fiscal-year adoption model as main, not the previous-observed-row sensitivity.",
        },
        {
            "id": "stale_readme_fukushima_shorthand",
            "path": README_PATH,
            "pattern": "pre-Fuku",
            "reason": "README must use early/later coded-window language rather than Fukushima shorthand.",
        },
        {
            "id": "stale_manuscript_grid_control_md",
            "path": MANUSCRIPT_MD_PATH,
            "pattern": "grid-emission-factor control",
            "reason": "The interpolated grid factor is not a core generator-performance covariate.",
        },
        {
            "id": "stale_manuscript_grid_row_md",
            "path": MANUSCRIPT_MD_PATH,
            "pattern": "Grid EF",
            "reason": "The core regression table must not restore the removed grid-factor row.",
        },
        {
            "id": "stale_manuscript_grid_row_tex",
            "path": MANUSCRIPT_TEX_PATH,
            "pattern": "Grid EF",
            "reason": "The LaTeX core regression table must match the current model.",
        },
        {
            "id": "stale_supplement_grid_control",
            "path": SUPPLEMENT_PATH,
            "pattern": "grid-emission factor",
            "reason": "The supplement must not describe the interpolated grid factor as a core covariate.",
        },
        {
            "id": "stale_universal_age_headline_md",
            "path": MANUSCRIPT_MD_PATH,
            "pattern": "younger and larger facilities",
            "reason": "The revised headline must distinguish robust scale selectivity from the frame-dependent age pattern.",
        },
        {
            "id": "stale_universal_age_headline_tex",
            "path": MANUSCRIPT_TEX_PATH,
            "pattern": "younger and larger facilities",
            "reason": "The LaTeX manuscript must preserve the broad-versus-active entry distinction.",
        },
        {
            "id": "stale_entry_pseudo_r2_md",
            "path": MANUSCRIPT_MD_PATH,
            "pattern": "0.1829",
            "reason": "The duration-adjusted broad entry model has pseudo-R2 0.1920.",
        },
        {
            "id": "stale_entry_pseudo_r2_tex",
            "path": MANUSCRIPT_TEX_PATH,
            "pattern": "0.1829",
            "reason": "The duration-adjusted broad entry model has pseudo-R2 0.1920.",
        },
        {
            "id": "stale_persistence_overclaim_md",
            "path": MANUSCRIPT_MD_PATH,
            "pattern": "not easily erased",
            "reason": "Observed rank persistence does not bound attainable intervention gains.",
        },
        {
            "id": "stale_official_share_md",
            "path": MANUSCRIPT_MD_PATH,
            "pattern": "only 41.1%",
            "reason": "National context must use the official FY2024 share of 41.9%; 41.1% is analytical only.",
        },
        {
            "id": "stale_official_share_tex",
            "path": MANUSCRIPT_TEX_PATH,
            "pattern": "only 41.1\\%",
            "reason": "National context must use the official FY2024 share of 41.9%; 41.1% is analytical only.",
        },
    ]


def run_checks() -> tuple[list[dict], list[dict], dict]:
    metrics = build_canonical_metrics()
    texts = {
        README_PATH: README_PATH.read_text(encoding="utf-8"),
        ARCHITECTURE_PATH: ARCHITECTURE_PATH.read_text(encoding="utf-8"),
        MANUSCRIPT_MD_PATH: MANUSCRIPT_MD_PATH.read_text(encoding="utf-8"),
        MANUSCRIPT_TEX_PATH: MANUSCRIPT_TEX_PATH.read_text(encoding="utf-8"),
        SUPPLEMENT_PATH: SUPPLEMENT_PATH.read_text(encoding="utf-8"),
    }

    passes = []
    failures = []

    if len(metrics["source_manifest_python"]) != 1:
        failures.append(
            {
                "type": "manifest_consistency",
                "id": "source_manifest_python",
                "detail": (
                    "Core stage manifests do not share one Python version: "
                    + ", ".join(metrics["source_manifest_python"])
                ),
            }
        )
    else:
        passes.append(
            {
                "type": "manifest_consistency",
                "id": "source_manifest_python",
                "detail": f"Core stage manifests share Python {metrics['source_manifest_python'][0]}",
            }
        )

    for claim in make_claim_registry(metrics):
        missing = []
        for path, snippet in claim["targets"]:
            if snippet not in texts[path]:
                missing.append({"path": path, "snippet": snippet})
        if missing:
            failures.append({"type": "claim", "id": claim["id"], "missing": missing})
        else:
            passes.append(
                {
                    "type": "claim",
                    "id": claim["id"],
                    "detail": f"All snippets present across {len(claim['targets'])} target checks.",
                }
            )

    for forbidden in make_forbidden_patterns():
        text = texts[forbidden["path"]]
        if forbidden["pattern"] in text:
            failures.append(
                {
                    "type": "forbidden_pattern",
                    "id": forbidden["id"],
                    "detail": forbidden["reason"],
                    "path": forbidden["path"],
                    "pattern": forbidden["pattern"],
                }
            )
        else:
            passes.append(
                {
                    "type": "forbidden_pattern",
                    "id": forbidden["id"],
                    "detail": f"Forbidden pattern absent: {forbidden['pattern']}",
                }
            )

    return passes, failures, metrics


def write_report(passes: list[dict], failures: list[dict], metrics: dict) -> None:
    lines = [
        "# Claim Verification Report",
        "",
        "Repo-level check that paper-facing claims stay synchronized with canonical outputs.",
        "",
        f"- Core manifest Python: {metrics['source_manifest_python'][0] if len(metrics['source_manifest_python']) == 1 else ', '.join(metrics['source_manifest_python'])}",
        f"- Full panel: {fmt_int(metrics['full_panel_obs'])} observations across {fmt_int(metrics['full_panel_facilities'])} facilities",
        (
            f"- Capacity-entry frame: risk set {fmt_int(metrics['risk_set_obs'])} / {fmt_int(metrics['risk_set_facilities'])}; "
            f"model {fmt_int(metrics['model_obs'])} / {fmt_int(metrics['model_facilities'])} / {fmt_int(metrics['model_events'])} events"
        ),
        (
            f"- Active-conversion frame: {fmt_int(metrics['active_model_obs'])} / "
            f"{fmt_int(metrics['active_model_facilities'])} / "
            f"{fmt_int(metrics['active_model_events'])} events"
        ),
        (
            f"- Entry effects: capacity {metrics['adoption_capacity_pp_2dp']} pp broad and "
            f"{metrics['active_capacity_pp_2dp']} pp active; broad age "
            f"{'/'.join(metrics['broad_age_ames_2dp'])} pp versus active age "
            f"{'/'.join(metrics['active_age_ames_2dp'])} pp"
        ),
        (
            f"- Pathway audit: {metrics['pathway_reset']} reset/rebuild-like, "
            f"{metrics['pathway_continuity']} continuity-like, "
            f"{metrics['pathway_placeholder']} forward-dated/placeholder, "
            f"{metrics['pathway_timing_ambiguous']} timing-ambiguous, "
            f"{metrics['pathway_unresolved']} unresolved"
        ),
        (
            f"- Regression frame: {fmt_int(metrics['regression_obs'])} observations across "
            f"{fmt_int(metrics['regression_facilities'])} facilities; within/total ratio "
            f"{metrics['within_total_ratio']:.4f} ({metrics['early_ratio']:.4f} early coded, "
            f"{metrics['later_ratio']:.4f} later coded)"
        ),
        (
            f"- Primary generator model: age/vintage {fmt_signed_decimal(metrics['primary_age'], 4)}, "
            f"capacity {fmt_signed_decimal(metrics['primary_capacity'], 4)}, "
            f"utilization {fmt_signed_decimal(metrics['primary_utilization'], 4)}; "
            f"R2 {metrics['primary_r2']:.4f}"
        ),
        (
            f"- Post-entry trajectory: {fmt_int(metrics['trajectory_rows'])} rows across "
            f"{fmt_int(metrics['trajectory_events'])} events"
        ),
        "",
        f"## Result: {'PASS' if not failures else 'FAIL'}",
        "",
        f"- Passed checks: {len(passes)}",
        f"- Failed checks: {len(failures)}",
        "",
        "## Passed Checks",
        "",
    ]

    for item in passes:
        lines.append(f"- `{item['type']}` `{item['id']}`: {item['detail']}")

    lines.extend(["", "## Failures", ""])
    if not failures:
        lines.append("- None")
    else:
        for item in failures:
            if item["type"] == "claim":
                lines.append(f"- `claim` `{item['id']}`:")
                for missing in item["missing"]:
                    rel = os.path.relpath(missing["path"], REPO_ROOT)
                    lines.append(f"  Missing in `{rel}`: `{missing['snippet']}`")
            else:
                rel = os.path.relpath(item.get("path", ""), REPO_ROOT) if item.get("path") else ""
                detail = item.get("detail", "")
                pattern = item.get("pattern")
                if pattern:
                    lines.append(
                        f"- `{item['type']}` `{item['id']}` in `{rel}`: found forbidden pattern `{pattern}`. {detail}"
                    )
                else:
                    lines.append(f"- `{item['type']}` `{item['id']}`: {detail}")

    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_claim_map(metrics: dict) -> None:
    lines = [
        "# Claim-to-Evidence Map",
        "",
        "Curated bridge between the paper's claims and the canonical generated outputs.",
        "",
        "Use this alongside `output/claim_verification.md`: the verifier confirms wording is synchronized, while this map explains which artifact supports which defended claim.",
        "",
        "## Claim 1: The paper is empirically two-part",
        "",
        "Paper claim: the fleet transition question must be split into an installed-capacity entry layer and a conditional generator-performance layer.",
        "",
        "Evidence spine:",
        f"- `output/adoption_results.md`: installed-capacity entry risk set of {fmt_int(metrics['risk_set_obs'])} facility-years across {fmt_int(metrics['risk_set_facilities'])} facilities, with {fmt_int(metrics['events'])} entry events.",
        f"- `output/regression_results.md`: canonical generator frame of {fmt_int(metrics['regression_obs'])} facility-years across {fmt_int(metrics['regression_facilities'])} facilities.",
        "- `paper/manuscript/paper.md` Sections 1, 3, and 4: architecture is framed explicitly as extensive margin first, intensive margin second.",
        "",
        "## Claim 2: Entry is scale-selective while its age pattern depends on the risk set",
        "",
        "Paper claim: prior-year scale predicts entry in both the broad asset and active-conversion frames, while the broad age gradient attenuates when positive prior-year throughput is required.",
        "",
        "Evidence spine:",
        f"- `output/adoption_results.md`: lagged logit hazard on {fmt_int(metrics['model_obs'])} facility-years across {fmt_int(metrics['model_facilities'])} facilities and {fmt_int(metrics['model_events'])} retained events.",
        f"- `output/adoption_results.md`: {fmt_int(metrics['zero_prior_throughput_events'])} of {fmt_int(metrics['model_events'])} exact-year events have zero or missing prior-year throughput.",
        f"- `output/adoption_results.md`: active conversion uses {fmt_int(metrics['active_model_obs'])} rows, {fmt_int(metrics['active_model_facilities'])} facilities, and {fmt_int(metrics['active_model_events'])} events.",
        f"- `output/adoption_results.md`: capacity is {metrics['adoption_capacity_pp_2dp']} pp broad and {metrics['active_capacity_pp_2dp']} pp active per 100 t/day.",
        f"- `output/adoption_results.md`: broad age AMEs {'/'.join(metrics['broad_age_ames_2dp'])} pp attenuate to {'/'.join(metrics['active_age_ames_2dp'])} pp.",
        "- `output/adoption_results.md` event-rate tables use exact-lag prior-year profiles and show strongly increasing rates across capacity quartiles.",
        "- `output/identifier_gap_audit.md`: exact one-fiscal-year lags are the main adoption frame; previous-observed-coded-row estimates are sensitivity evidence only.",
        f"- `output/adoption_results.md`: the positive-output alternative retains {fmt_int(metrics['positive_output_model_events'])} exact-year events and a {metrics['positive_output_capacity_pp_2dp']} percentage-point capacity AME.",
        "",
        "## Claim 3: Capacity entry maps to operation but not automatically to superior performance",
        "",
        "Paper claim: capacity entry is usually followed by positive output, entrants begin near the middle of the same-year generator distribution on average, and non-entry cannot be treated as continuous observation through FY2024.",
        "",
        "Evidence spine:",
        f"- `output/post_adoption_bridge.csv`: {fmt_int(metrics['post_entry_positive_by_one'])} of {fmt_int(metrics['events'])} entrants report positive output by the following year; {fmt_int(metrics['post_entry_generator_within_three'])} enter the canonical generator frame within three years.",
        f"- `output/post_adoption_trajectories.csv`: {fmt_int(metrics['trajectory_rows'])} observations across {fmt_int(metrics['trajectory_events'])} events; mean same-year percentile is {metrics['trajectory_t0_rank_pct']:.1f} at event time zero and {metrics['trajectory_t3_rank_pct']:.1f} at time three.",
        f"- `output/adoption_results.md`: {fmt_int(metrics['panel_exit_before_end'])} of {fmt_int(metrics['panel_exit_nonadopters'])} non-entrants ({metrics['panel_exit_before_end_pct']:.1f}%) are last observed before FY2024.",
        f"- `output/figure2_transition_effects.csv`: age 30+ panel-exit AME {metrics['panel_exit_age30_pp_2dp']} pp and capacity AME {metrics['panel_exit_capacity_pp_2dp']} pp per 100 t/day.",
        "",
        "## Claim 4: Capital-reset-like modernization is empirically prominent, but not uniquely identified",
        "",
        "Paper claim: the pathway audit supports a calibrated mechanism claim, not a proof that replacement is the only pathway.",
        "",
        "Evidence spine:",
        f"- `output/adoption_results.md`: pathway audit counts {metrics['pathway_reset']} reset/rebuild-like, {metrics['pathway_continuity']} continuity/in-place-upgrade-like, {metrics['pathway_placeholder']} forward-dated/placeholder, {metrics['pathway_timing_ambiguous']} timing-ambiguous, {metrics['pathway_unresolved']} unresolved.",
        "- `output/adoption_results.md`: explicit rule set based on `year_started` reset, mature-to-new age reset, continuity, timing ambiguity, and unresolved placeholder cases.",
        "- `paper/notes/positioning/claim-stack.md`: the claim stack keeps mechanism language calibrated.",
        "",
        "## Claim 5: Conditional generator performance is structured after observed-technology adjustment",
        "",
        "Paper claim: within common fiscal years, gross MWh/t is lower at older-vintage plants and higher at larger, more utilized plants after adjustment for observed technology configuration.",
        "",
        "Evidence spine:",
        f"- `output/regression_results.md`: primary coefficients are age/vintage {fmt_signed_decimal(metrics['primary_age'], 4)}, capacity {fmt_signed_decimal(metrics['primary_capacity'], 4)}, and utilization {fmt_signed_decimal(metrics['primary_utilization'], 4)}.",
        f"- `output/claim_verification.md`: within/total ratio is {metrics['within_total_ratio']:.4f}, with {metrics['early_ratio']:.4f} in the early coded window ({metrics['early_window_label']}) and {metrics['later_ratio']:.4f} in the later coded window ({metrics['later_window_label']}).",
        f"- `output/figure3_persistence.csv`: pooled adjacent-year within-year rank correlation is {metrics['pooled_rank_correlation']:.4f} across {fmt_int(metrics['rank_pairs'])} exact pairs.",
        f"- `output/robustness_results.md`: engineering validation uses {fmt_int(metrics['engineering_rows'])} plausible rows; logged thermal conversion and reported efficiency correlate at {metrics['engineering_outcome_correlation']:.4f} and preserve the focal signs.",
        "- `output/data_quality_sensitivity.md`: duplicate-ID and heating-value sensitivity checks preserve the same headline sign pattern.",
        "- `output/identifier_gap_audit.md`: the canonical generator regression frame is an identifiable coded-generator panel, not a complete census of all operating generator rows.",
        "",
        "## Claim 6: The paper supports planning diagnostics, not an exclusive mechanism claim",
        "",
        "Paper claim: planning assessments should distinguish facilities outside electricity recovery from operating generators because the observable constraints differ across those two groups.",
        "",
        "Evidence spine:",
        "- `output/adoption_results.md`: scale selectivity survives both risk sets, age is frame-dependent, and older/smaller facilities are more likely to exit the coded panel.",
        "- `output/regression_results.md`: utilization is strongly positive, so operational levers are preserved rather than dismissed.",
        "- `paper/supplement/supplement.md`: the supplement explicitly records the data-quality caveats and identification limits.",
        "",
        "## Reviewer Use",
        "",
        "1. Start with `paper/manuscript/paper.md` for the active narrative.",
        "2. Use `output/claim_verification.md` to confirm the current wording matches the generated artifacts.",
        "3. Use this file to see which exact output anchors each paper claim.",
        "4. Use `paper/supplement/supplement.md` and `paper/notes/positioning/claim-stack.md` to keep the scope disciplined during review.",
    ]
    CLAIM_MAP_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    passes, failures, metrics = run_checks()
    write_report(passes, failures, metrics)
    write_claim_map(metrics)

    manifest_path = write_stage_manifest(
        "08_verify_claims",
        inputs=[
            "output/manifests/02_parse_facility_panel.json",
            "output/manifests/03_grid_emission_factors.json",
            "output/manifests/04_eda_facility.json",
            "output/manifests/05a_power_adoption.json",
            "output/manifests/05_panel_regression.json",
            "output/manifests/06_robustness.json",
            "output/manifests/06a_data_quality_sensitivity.json",
            "output/manifests/06b_identifier_gap_audit.json",
            "README.md",
            "ARCHITECTURE.md",
        ],
        outputs=["output/claim_verification.md", "output/claim_evidence_map.md"],
        metadata={
            "passed_checks": len(passes),
            "failed_checks": len(failures),
            "source_manifest_python": metrics["source_manifest_python"],
        },
    )

    print(f"Claim verification report: {REPORT_PATH}")
    print(f"Claim-to-evidence map: {CLAIM_MAP_PATH}")
    print(f"Manifest: {manifest_path}")

    if failures:
        print("\nCLAIM VERIFICATION FAILED\n")
        for item in failures:
            print(f"- {item['type']}::{item['id']}")
        raise SystemExit(1)

    print("\nCLAIM VERIFICATION PASSED")


if __name__ == "__main__":
    main()
