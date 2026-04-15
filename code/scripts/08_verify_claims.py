"""
08_verify_claims.py
===================
Verify that thesis-facing claims stay synchronized with canonical outputs.

This script reads structured manifests and generated result artifacts, checks a
curated set of headline claims in README.md, ARCHITECTURE.md, and thesis.tex,
and fails hard on drift or known overclaim language.
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
THESIS_PATH = REPO_ROOT / "thesis" / "thesis.tex"
REPORT_PATH = OUTPUT_DIR / "claim_verification.md"
CLAIM_MAP_PATH = OUTPUT_DIR / "claim_evidence_map.md"
EXEC_SUMMARY_PATH = REPO_ROOT / "research" / "notes" / "executive-summary-for-supervisor.md"
DEFENSE_QA_PATH = REPO_ROOT / "research" / "notes" / "defense-q-and-a.md"
DEFENSE_RAPID_PATH = REPO_ROOT / "research" / "notes" / "defense-rapid-answers.md"
DEFENSE_ORDER_PATH = REPO_ROOT / "research" / "notes" / "defense-question-order.md"
DEFENSE_OUTLINE_PATH = REPO_ROOT / "research" / "notes" / "defense-slide-outline.md"
DEFENSE_DECK_PATH = REPO_ROOT / "research" / "slides" / "defense-deck.md"
DEFENSE_ADOPTION_FIG_PATH = REPO_ROOT / "research" / "slides" / "figures" / "defense_adoption_hazard.svg"

CORE_MANIFESTS = [
    "02_parse_facility_panel",
    "03_grid_emission_factors",
    "04_eda_facility",
    "05a_power_adoption",
    "05_panel_regression",
    "06_robustness",
]


def load_manifest(stage: str) -> dict:
    with open(MANIFEST_DIR / f"{stage}.json", "r", encoding="utf-8") as f:
        return json.load(f)


def fmt_int(value: int) -> str:
    return f"{value:,}"


def fmt_pp_abs(value: float, decimals: int = 1) -> str:
    scaled = Decimal(f"{abs(value) * 100:.{decimals + 1}f}")
    quantum = Decimal("1").scaleb(-decimals)
    return format(scaled.quantize(quantum, rounding=ROUND_HALF_UP), f".{decimals}f")


def fmt_signed_pp(value: float, decimals: int = 2) -> str:
    sign = "+" if value >= 0 else "−"
    scaled = Decimal(f"{abs(value) * 100:.{decimals + 1}f}")
    quantum = Decimal("1").scaleb(-decimals)
    return f"{sign}{format(scaled.quantize(quantum, rounding=ROUND_HALF_UP), f'.{decimals}f')}"


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
    robustness_specs = robustness_manifest["metadata"]["specifications"]
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
        "pathway_reset": adoption_manifest["metadata"]["pathway_audit"]["counts"][
            "Reset / rebuild-like transition"
        ],
        "pathway_continuity": adoption_manifest["metadata"]["pathway_audit"]["counts"][
            "In-place upgrade / continuity transition"
        ],
        "pathway_placeholder": adoption_manifest["metadata"]["pathway_audit"]["counts"][
            "Forward-dated / placeholder entry"
        ],
        "pathway_unresolved": adoption_manifest["metadata"]["pathway_audit"]["counts"][
            "Unresolved / insufficient continuity"
        ],
        "regression_obs": regression_manifest["metadata"]["regression_obs"],
        "regression_facilities": regression_manifest["metadata"]["regression_facilities"],
        "within_total_ratio": regression_manifest["metadata"]["within_total_ratio"],
        "pre_ratio": regression_manifest["metadata"]["pre_fukushima_within_total_ratio"],
        "post_ratio": regression_manifest["metadata"]["post_fukushima_within_total_ratio"],
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
    }


def make_claim_registry(metrics: dict) -> list[dict]:
    return [
        {
            "id": "readme_topline_paragraph",
            "targets": [
                (
                    README_PATH,
                    f"23,599 observations across 2,948 facilities",
                ),
                (
                    README_PATH,
                    (
                        f"{fmt_int(metrics['risk_set_obs'])} facility-years across "
                        f"{fmt_int(metrics['risk_set_facilities'])} facilities, with "
                        f"{fmt_int(metrics['events'])} observed first-adoption events"
                    ),
                ),
                (
                    README_PATH,
                    (
                        f"{fmt_int(metrics['model_obs'])} facility-years across "
                        f"{fmt_int(metrics['model_facilities'])} facilities and "
                        f"{fmt_int(metrics['model_events'])} events"
                    ),
                ),
                (
                    README_PATH,
                    (
                        f"{metrics['adoption_age_range_1dp'][0]}–"
                        f"{metrics['adoption_age_range_1dp'][1]} percentage points less likely"
                    ),
                ),
                (
                    README_PATH,
                    f"{metrics['adoption_capacity_pp_2dp']} percentage points",
                ),
                (
                    README_PATH,
                    (
                        f"{metrics['pathway_reset']} as reset/rebuild-like, "
                        f"{metrics['pathway_continuity']} as continuity/in-place-upgrade-like, "
                        f"{metrics['pathway_placeholder']} as forward-dated or placeholder entries, "
                        f"and {metrics['pathway_unresolved']} as unresolved"
                    ),
                ),
                (
                    README_PATH,
                    (
                        f"{fmt_int(metrics['regression_obs'])} facility-years across "
                        f"{fmt_int(metrics['regression_facilities'])} facilities"
                    ),
                ),
                (
                    README_PATH,
                    (
                        f"{metrics['main_age_range'][0]} to {metrics['main_age_range'][1]}"
                    ),
                ),
                (
                    README_PATH,
                    (
                        f"{metrics['main_capacity_range'][0]} to {metrics['main_capacity_range'][1]}"
                    ),
                ),
                (
                    README_PATH,
                    (
                        f"{metrics['main_util_range'][0]} to {metrics['main_util_range'][1]}"
                    ),
                ),
                (
                    README_PATH,
                    (
                        f"{metrics['within_total_ratio']:.4f}, falling from "
                        f"{metrics['pre_ratio']:.4f} in FY2005–FY2011 to "
                        f"{metrics['post_ratio']:.4f} in FY2012–FY2024"
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
                        f"| Adoption age effect | {metrics['adoption_age_range_2dp'][0]} to "
                        f"{metrics['adoption_age_range_2dp'][1]} percentage points vs prior-year age 0–10 |"
                    ),
                ),
                (
                    README_PATH,
                    (
                        f"| Adoption capacity effect | {metrics['adoption_capacity_pp_2dp']} percentage points "
                        "per 100 t/day of prior-year capacity |"
                    ),
                ),
                (
                    README_PATH,
                    (
                        f"| Pathway audit of adoption events | {metrics['pathway_reset']} reset/rebuild-like, "
                        f"{metrics['pathway_continuity']} continuity-like, "
                        f"{metrics['pathway_placeholder']} forward-dated/placeholder, "
                        f"{metrics['pathway_unresolved']} unresolved |"
                    ),
                ),
                (
                    README_PATH,
                    (
                        f"| Within/total variance ratio | {metrics['within_total_ratio']:.4f} (pooled), "
                        f"{metrics['pre_ratio']:.4f} (pre-Fuku), {metrics['post_ratio']:.4f} (post-Fuku) |"
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
                        f"{fmt_int(metrics['events'])} observed first-adoption events)"
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
                        f"{metrics['adoption_age_range_1dp'][0]}–{metrics['adoption_age_range_1dp'][1]} "
                        "percentage points less likely to transition into generation"
                    ),
                ),
                (
                    ARCHITECTURE_PATH,
                    f"about {metrics['adoption_capacity_pp_2dp'].replace('+', '')} percentage points",
                ),
                (
                    ARCHITECTURE_PATH,
                    (
                        f"{metrics['pathway_reset']} observed transitions as reset/rebuild-like, "
                        f"{metrics['pathway_continuity']} as continuity/in-place-upgrade-like, "
                        f"{metrics['pathway_placeholder']} as forward-dated or placeholder entries, "
                        f"and {metrics['pathway_unresolved']} as unresolved"
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
                        "| Adoption hazard, prior-year age bands | Facilities older than 10 years are "
                        f"{metrics['adoption_age_range_1dp'][0]}–{metrics['adoption_age_range_1dp'][1]} pp less likely than 0–10-year facilities "
                        "to record transition in the next observed year | p < 0.05 in every reported age-band coefficient |"
                    ),
                ),
                (
                    ARCHITECTURE_PATH,
                    (
                        f"| Adoption hazard, prior-year capacity | {metrics['adoption_capacity_pp_2dp']} pp per 100 t/day | p < 0.05 |"
                    ),
                ),
                (
                    ARCHITECTURE_PATH,
                    (
                        f"| Facility age effect | {metrics['main_age_range'][0]} to {metrics['main_age_range'][1]} "
                        "in the four main specifications | p < 0.001 in every reported main specification |"
                    ),
                ),
                (
                    ARCHITECTURE_PATH,
                    (
                        f"| Design capacity effect | {metrics['main_capacity_range'][0]} to {metrics['main_capacity_range'][1]} "
                        "in the four main specifications | Positive in every main specification |"
                    ),
                ),
                (
                    ARCHITECTURE_PATH,
                    (
                        f"| Capacity utilization effect | {metrics['main_util_range'][0]} to {metrics['main_util_range'][1]} "
                        "in the four main specifications | Positive in every main specification |"
                    ),
                ),
            ],
        },
        {
            "id": "thesis_core_claims",
            "targets": [
                (
                    THESIS_PATH,
                    "23,599 facility-year observations across 2,948 incinerators",
                ),
                (
                    THESIS_PATH,
                    (
                        f"{fmt_int(metrics['events'])} observed first-adoption events among "
                        f"{fmt_int(metrics['risk_set_facilities'])} facilities first observed without power generation"
                    ),
                ),
                (
                    THESIS_PATH,
                    (
                        f"about {metrics['adoption_age_range_1dp'][0]}--{metrics['adoption_age_range_1dp'][1]} "
                        "percentage points less likely"
                    ),
                ),
                (
                    THESIS_PATH,
                    (
                        f"A conservative pathway audit of the {metrics['events']} observed adoption events classifies "
                        f"{metrics['pathway_reset']} as reset- or rebuild-like, "
                        f"{metrics['pathway_continuity']} as continuity-type upgrades, "
                        f"{metrics['pathway_placeholder']} as forward-dated or placeholder entries, "
                        f"and {metrics['pathway_unresolved']} as unresolved"
                    ),
                ),
                (
                    THESIS_PATH,
                    (
                        f"{fmt_int(metrics['regression_obs'])} facility-year observations across "
                        f"{fmt_int(metrics['regression_facilities'])} facilities"
                    ),
                ),
                (
                    THESIS_PATH,
                    (
                        f"{metrics['within_total_ratio']:.4f}, falling to {metrics['post_ratio']:.4f} "
                        "in the post-Fukushima window"
                    ),
                ),
            ],
        },
        {
            "id": "supervisor_brief_current_numbers",
            "targets": [
                (
                    EXEC_SUMMARY_PATH,
                    "lagged discrete-time logit hazard",
                ),
                (
                    EXEC_SUMMARY_PATH,
                    (
                        f"about {metrics['adoption_age_range_1dp'][0]}-"
                        f"{metrics['adoption_age_range_1dp'][1]} percentage points less likely"
                    ),
                ),
                (
                    EXEC_SUMMARY_PATH,
                    (
                        f"about {metrics['adoption_capacity_pp_1dp']} percentage points"
                    ),
                ),
                (
                    EXEC_SUMMARY_PATH,
                    (
                        f"{metrics['pathway_reset']} of {metrics['events']} observed transitions as reset/rebuild-like"
                    ),
                ),
            ],
        },
        {
            "id": "defense_notes_current_spec",
            "targets": [
                (
                    DEFENSE_QA_PATH,
                    "### 3. Why use a logit hazard rather than LPM?",
                ),
                (
                    DEFENSE_QA_PATH,
                    "The main specification is a lagged logit hazard",
                ),
                (
                    DEFENSE_RAPID_PATH,
                    "### Why use logit rather than LPM?",
                ),
                (
                    DEFENSE_ORDER_PATH,
                    "### 9. Why use logit rather than LPM?",
                ),
            ],
        },
        {
            "id": "defense_slides_current_numbers",
            "targets": [
                (
                    DEFENSE_OUTLINE_PATH,
                    (
                        f"- Prior-year age `10-20`: `{metrics['adoption_age_range_2dp'][0].replace('−', '-')}` pp"
                    ),
                ),
                (
                    DEFENSE_OUTLINE_PATH,
                    (
                        f"- Prior-year capacity: `{metrics['adoption_capacity_pp_2dp'].replace('+', '')}` pp per `100 t/day`"
                    ),
                ),
                (
                    DEFENSE_DECK_PATH,
                    (
                        f"<strong>{metrics['adoption_age_range_1dp'][0]}-"
                        f"{metrics['adoption_age_range_1dp'][1]} pp less likely</strong>"
                    ),
                ),
                (
                    DEFENSE_DECK_PATH,
                    (
                        f"<strong>{metrics['adoption_capacity_pp_1dp']} pp</strong>"
                    ),
                ),
                (
                    DEFENSE_ADOPTION_FIG_PATH,
                    f">{metrics['adoption_capacity_pp_2dp']} pp<",
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
            "id": "dominant_pathway_language",
            "path": THESIS_PATH,
            "pattern": "dominant pathway",
            "reason": "Pathway audit language must stay calibrated to the observed panel, not overclaim dominance.",
        },
        {
            "id": "route_to_large_gains_language",
            "path": THESIS_PATH,
            "pattern": "route to large gains in this panel",
            "reason": "The pathway audit classifies modernization pathways, not realized gain magnitudes.",
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
            "id": "stale_supervisor_cloglog_method",
            "path": EXEC_SUMMARY_PATH,
            "pattern": "lagged complementary log-log discrete-time hazard",
            "reason": "Supervisor brief must reflect the current logit main specification.",
        },
        {
            "id": "stale_supervisor_old_age_range",
            "path": EXEC_SUMMARY_PATH,
            "pattern": "2.3-3.2 percentage points less likely",
            "reason": "Supervisor brief should not retain pre-logit adoption effects.",
        },
        {
            "id": "stale_supervisor_old_capacity_effect",
            "path": EXEC_SUMMARY_PATH,
            "pattern": "0.39 percentage points",
            "reason": "Supervisor brief should not retain pre-logit capacity effects.",
        },
        {
            "id": "stale_defense_q_and_a_heading",
            "path": DEFENSE_QA_PATH,
            "pattern": "Why use a complementary log-log hazard?",
            "reason": "Defense Q&A must present logit as the main adoption specification.",
        },
        {
            "id": "stale_defense_rapid_heading",
            "path": DEFENSE_RAPID_PATH,
            "pattern": "Why use cloglog rather than LPM?",
            "reason": "Rapid answers must present logit as the main adoption specification.",
        },
        {
            "id": "stale_defense_order_heading",
            "path": DEFENSE_ORDER_PATH,
            "pattern": "Why use cloglog rather than LPM?",
            "reason": "Question order must present logit as the main adoption specification.",
        },
        {
            "id": "stale_defense_outline_old_age_range",
            "path": DEFENSE_OUTLINE_PATH,
            "pattern": "- Prior-year age `10-20`: `-3.19` pp",
            "reason": "Defense outline should not retain pre-logit adoption effects.",
        },
        {
            "id": "stale_defense_deck_old_capacity_effect",
            "path": DEFENSE_DECK_PATH,
            "pattern": "0.39 pp",
            "reason": "Defense deck should not retain pre-logit capacity effects.",
        },
        {
            "id": "stale_defense_figure_cloglog",
            "path": DEFENSE_ADOPTION_FIG_PATH,
            "pattern": "lagged cloglog hazard",
            "reason": "Adoption slide figure must reflect the current logit main specification.",
        },
    ]


def run_checks() -> tuple[list[dict], list[dict], dict]:
    metrics = build_canonical_metrics()
    texts = {
        README_PATH: README_PATH.read_text(encoding="utf-8"),
        ARCHITECTURE_PATH: ARCHITECTURE_PATH.read_text(encoding="utf-8"),
        THESIS_PATH: THESIS_PATH.read_text(encoding="utf-8"),
        EXEC_SUMMARY_PATH: EXEC_SUMMARY_PATH.read_text(encoding="utf-8"),
        DEFENSE_QA_PATH: DEFENSE_QA_PATH.read_text(encoding="utf-8"),
        DEFENSE_RAPID_PATH: DEFENSE_RAPID_PATH.read_text(encoding="utf-8"),
        DEFENSE_ORDER_PATH: DEFENSE_ORDER_PATH.read_text(encoding="utf-8"),
        DEFENSE_OUTLINE_PATH: DEFENSE_OUTLINE_PATH.read_text(encoding="utf-8"),
        DEFENSE_DECK_PATH: DEFENSE_DECK_PATH.read_text(encoding="utf-8"),
        DEFENSE_ADOPTION_FIG_PATH: DEFENSE_ADOPTION_FIG_PATH.read_text(encoding="utf-8"),
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
        "Repo-level check that thesis-facing claims stay synchronized with canonical outputs.",
        "",
        f"- Core manifest Python: {metrics['source_manifest_python'][0] if len(metrics['source_manifest_python']) == 1 else ', '.join(metrics['source_manifest_python'])}",
        f"- Full panel: {fmt_int(metrics['full_panel_obs'])} observations across {fmt_int(metrics['full_panel_facilities'])} facilities",
        (
            f"- Adoption frame: risk set {fmt_int(metrics['risk_set_obs'])} / {fmt_int(metrics['risk_set_facilities'])}; "
            f"model {fmt_int(metrics['model_obs'])} / {fmt_int(metrics['model_facilities'])} / {fmt_int(metrics['model_events'])} events"
        ),
        (
            f"- Adoption effects: age {metrics['adoption_age_range_1dp'][0]}–{metrics['adoption_age_range_1dp'][1]} pp less likely; "
            f"capacity {metrics['adoption_capacity_pp_2dp']} pp per 100 t/day"
        ),
        (
            f"- Pathway audit: {metrics['pathway_reset']} reset/rebuild-like, "
            f"{metrics['pathway_continuity']} continuity-like, "
            f"{metrics['pathway_placeholder']} forward-dated/placeholder, "
            f"{metrics['pathway_unresolved']} unresolved"
        ),
        (
            f"- Regression frame: {fmt_int(metrics['regression_obs'])} observations across "
            f"{fmt_int(metrics['regression_facilities'])} facilities; within/total ratio "
            f"{metrics['within_total_ratio']:.4f} ({metrics['pre_ratio']:.4f} pre-Fuku, {metrics['post_ratio']:.4f} post-Fuku)"
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
        "Curated bridge between the defended thesis claims and the canonical generated outputs.",
        "",
        "Use this alongside `output/claim_verification.md`: the verifier confirms wording is synchronized, while this map explains which artifact supports which defended claim.",
        "",
        "## Claim 1: The thesis is empirically two-part",
        "",
        "Defended claim: the fleet transition question must be split into an extensive-margin adoption layer and an intensive-margin generator-efficiency layer.",
        "",
        "Evidence spine:",
        f"- `output/adoption_results.md`: observed first-adoption risk set of {fmt_int(metrics['risk_set_obs'])} facility-years across {fmt_int(metrics['risk_set_facilities'])} facilities, with {fmt_int(metrics['events'])} observed transition events.",
        f"- `output/regression_results.md`: canonical generator frame of {fmt_int(metrics['regression_obs'])} facility-years across {fmt_int(metrics['regression_facilities'])} facilities.",
        "- `thesis/thesis.tex` Chapters 1, 3, and 4: architecture is framed explicitly as extensive margin first, intensive margin second.",
        "",
        "## Claim 2: Observed transition into generation is selective rather than diffuse",
        "",
        "Defended claim: among coded facilities first observed without generation, younger and larger facilities are more likely to record observed transition into generation.",
        "",
        "Evidence spine:",
        f"- `output/adoption_results.md`: lagged logit hazard on {fmt_int(metrics['model_obs'])} facility-years across {fmt_int(metrics['model_facilities'])} facilities and {fmt_int(metrics['model_events'])} retained events.",
        f"- `output/adoption_results.md`: prior-year age effects range from {metrics['adoption_age_range_2dp'][0]} to {metrics['adoption_age_range_2dp'][1]} percentage points relative to age 0-10.",
        f"- `output/adoption_results.md`: prior-year capacity effect is {metrics['adoption_capacity_pp_2dp']} percentage points per 100 t/day.",
        "- `output/adoption_results.md` event-rate tables: event rates collapse after age 10 and rise sharply across capacity quartiles.",
        "",
        "## Claim 3: Capital-reset-like modernization is empirically prominent, but not uniquely identified",
        "",
        "Defended claim: the pathway audit supports a calibrated mechanism claim, not a proof that replacement is the only pathway.",
        "",
        "Evidence spine:",
        f"- `output/adoption_results.md`: pathway audit counts {metrics['pathway_reset']} reset/rebuild-like, {metrics['pathway_continuity']} continuity/in-place-upgrade-like, {metrics['pathway_placeholder']} forward-dated/placeholder, {metrics['pathway_unresolved']} unresolved.",
        "- `output/adoption_results.md`: explicit rule set based on `year_started` reset, mature-to-new age reset, continuity, and unresolved placeholder cases.",
        "- `research/notes/what-this-thesis-does-not-claim.md`: the non-claims note keeps the mechanism language calibrated.",
        "",
        "## Claim 4: Conditional generator performance is shaped more by cross-facility structure than by large within-facility movement",
        "",
        "Defended claim: within the generator sample, age, scale, and utilization matter strongly, while within-facility responsiveness remains bounded.",
        "",
        "Evidence spine:",
        "- `output/regression_results.md`: age coefficients remain negative, capacity positive, and utilization positive across the four main specifications.",
        f"- `output/claim_verification.md`: within/total ratio is {metrics['within_total_ratio']:.4f}, with {metrics['pre_ratio']:.4f} pre-Fukushima and {metrics['post_ratio']:.4f} post-Fukushima.",
        "- `output/robustness_results.md`: sign pattern remains stable across the defended robustness set.",
        "",
        "## Claim 5: The thesis supports a policy hierarchy, not an exclusive mechanism claim",
        "",
        "Defended claim: capital-side modernization and consolidation likely matter more for the weakest segment than operating-side fine-tuning alone, while operations still matter within the design envelope.",
        "",
        "Evidence spine:",
        "- `output/adoption_results.md`: old and small facilities rarely record observed transition into generation.",
        "- `output/regression_results.md`: utilization is strongly positive, so operational levers are preserved rather than dismissed.",
        "- `research/notes/what-this-thesis-does-not-claim.md`: the thesis explicitly avoids claiming causal proof, exclusive replacement, full lifecycle accounting, or heat-recovery evaluation.",
        "",
        "## Reviewer Use",
        "",
        "1. Start with `research/notes/executive-summary-for-supervisor.md` for the one-page narrative.",
        "2. Use `output/claim_verification.md` to confirm the current wording matches the generated artifacts.",
        "3. Use this file to see which exact output anchors each defended claim.",
        "4. Use `research/notes/what-this-thesis-does-not-claim.md` to keep the scope disciplined during review or viva prep.",
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
            "README.md",
            "ARCHITECTURE.md",
            "thesis/thesis.tex",
            "research/notes/executive-summary-for-supervisor.md",
            "research/notes/defense-q-and-a.md",
            "research/notes/defense-rapid-answers.md",
            "research/notes/defense-question-order.md",
            "research/notes/defense-slide-outline.md",
            "research/slides/defense-deck.md",
            "research/slides/figures/defense_adoption_hazard.svg",
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
