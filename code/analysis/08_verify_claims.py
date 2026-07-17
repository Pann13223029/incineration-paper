"""Verify high-risk paper claims against current generated evidence.

This verifier intentionally separates evidence-integrity checks from prose
checks. Canonical numbers are recomputed from generated CSVs and compared with
stage manifests before any manuscript wording is accepted.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
import subprocess
import sys
import unicodedata
from pathlib import Path
from typing import Any, Iterable

import numpy as np
import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[2]
ANALYSIS_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = REPO_ROOT / "output"
MANIFEST_DIR = OUTPUT_DIR / "manifests"
REPORT_PATH = OUTPUT_DIR / "claim_verification.md"
CLAIM_MAP_PATH = OUTPUT_DIR / "claim_evidence_map.md"

if str(ANALYSIS_DIR) not in sys.path:
    sys.path.insert(0, str(ANALYSIS_DIR))

from panel_utils import (  # noqa: E402
    build_adoption_frame,
    build_adoption_model_frame,
    sha256_manifest_path,
    write_stage_manifest,
)


DOCUMENTS = {
    "manuscript_md": REPO_ROOT / "paper" / "manuscript" / "paper.md",
    "manuscript_tex": REPO_ROOT / "paper" / "manuscript" / "paper.tex",
    "professor_manuscript_md": (
        REPO_ROOT / "paper" / "manuscript" / "professor" / "paper.md"
    ),
    "professor_manuscript_tex": (
        REPO_ROOT / "paper" / "manuscript" / "professor" / "paper.tex"
    ),
    "supplement": REPO_ROOT / "paper" / "supplement" / "supplement.md",
    "professor_lineage": (
        REPO_ROOT
        / "paper"
        / "notes"
        / "positioning"
        / "professor-comparator-method-lineage.md"
    ),
}

CORE_STAGES = [
    "02_parse_facility_panel",
    "02a_build_facility_identity",
    "02b_build_raw_data_manifest",
    "02c_build_linkage_validation_packet",
    "04_eda_facility",
    "05_fleet_decomposition",
    "05a_power_adoption",
    "05_panel_regression",
    "05b_scientific_revision",
    "06_robustness",
    "06a_data_quality_sensitivity",
    "06b_identifier_gap_audit",
]

ADOPTION_FOCAL_TERMS = [
    "age_10-19 yrs",
    "age_20-29 yrs",
    "age_30+ yrs",
    "log_processing_capacity",
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_manifest(stage: str) -> dict[str, Any]:
    return load_json(MANIFEST_DIR / f"{stage}.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def close(left: float, right: float, tolerance: float = 1e-6) -> bool:
    return math.isclose(float(left), float(right), rel_tol=tolerance, abs_tol=tolerance)


def clean_identifier(series: pd.Series) -> set[str]:
    cleaned = series.dropna().astype("string").str.strip()
    cleaned = cleaned[~cleaned.isin(["", "nan", "None", "<NA>"])]
    return set(cleaned.tolist())


def parse_diagnostic_table(path: Path) -> dict[str, dict[str, float]]:
    """Parse the generated legacy-versus-sizing diagnostic table."""
    rows: dict[str, dict[str, float]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.split("|")[1:-1]]
        if len(cells) != 5 or cells[0] not in {
            "facility_age_years",
            "capacity_100t",
            "capacity_utilization_raw",
            "log_generator_design_intensity",
        }:
            continue
        values: list[float] = []
        for value in cells[1:]:
            values.append(float(value) if value.lower() != "nan" else math.nan)
        rows[cells[0]] = {
            "legacy_coefficient": values[0],
            "legacy_p_value": values[1],
            "sizing_adjusted_coefficient": values[2],
            "sizing_adjusted_p_value": values[3],
        }
    required = {
        "facility_age_years",
        "capacity_100t",
        "capacity_utilization_raw",
        "log_generator_design_intensity",
    }
    if set(rows) != required:
        missing = sorted(required - set(rows))
        raise ValueError(f"Regression diagnostic table is incomplete: {missing}")
    return rows


def build_metrics() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Recompute canonical metrics and return evidence audit assertions."""
    assertions: list[dict[str, Any]] = []

    def assert_evidence(check_id: str, condition: bool, detail: str) -> None:
        assertions.append(
            {
                "type": "evidence_integrity",
                "id": check_id,
                "passed": bool(condition),
                "detail": detail,
            }
        )

    manifests = {stage: load_manifest(stage) for stage in CORE_STAGES}
    python_versions = sorted({manifest["python"] for manifest in manifests.values()})
    assert_evidence(
        "core_manifest_python",
        len(python_versions) == 1,
        f"Core manifest Python versions: {', '.join(python_versions)}",
    )
    current_code_hashes = {
        str(path.relative_to(REPO_ROOT)): sha256_file(path)
        for path in sorted(ANALYSIS_DIR.glob("*.py"))
    }
    manifest_hash_failures: list[str] = []
    for stage, manifest in manifests.items():
        script = manifest.get("script", "")
        if (
            not script
            or manifest.get("script_sha256")
            != sha256_file(REPO_ROOT / script)
            or manifest.get("analysis_code_sha256") != current_code_hashes
        ):
            manifest_hash_failures.append(f"{stage}: code hash mismatch")
        for kind in ("input", "output"):
            paths = manifest.get(f"{kind}s", [])
            recorded = manifest.get(f"{kind}_sha256", {})
            if set(recorded) != set(paths):
                manifest_hash_failures.append(f"{stage}: {kind} hash keys mismatch")
                continue
            for relative in paths:
                try:
                    current_hash = sha256_manifest_path(relative)
                except (FileNotFoundError, subprocess.CalledProcessError):
                    manifest_hash_failures.append(
                        f"{stage}: missing {kind} {relative}"
                    )
                    continue
                if recorded[relative] != current_hash:
                    manifest_hash_failures.append(
                        f"{stage}: {kind} hash mismatch for {relative}"
                    )
    assert_evidence(
        "canonical_stage_hashes",
        not manifest_hash_failures,
        (
            "All canonical stage script, analysis-code, input, and output hashes match."
            if not manifest_hash_failures
            else "; ".join(manifest_hash_failures[:20])
        ),
    )

    # Raw-source provenance.
    raw_manifest = pd.read_csv(OUTPUT_DIR / "raw_data_manifest.csv", dtype="string")
    schema_map = pd.read_csv(OUTPUT_DIR / "raw_workbook_schema_map.csv", dtype="string")
    present_raw = raw_manifest[raw_manifest["file_status"].eq("present")].copy()
    configured_years = raw_manifest["fiscal_year"].nunique()
    raw_hash_failures: list[str] = []
    for row in present_raw.itertuples(index=False):
        path = REPO_ROOT / row.repository_path
        if not path.exists() or sha256_file(path) != row.sha256:
            raw_hash_failures.append(row.filename)
    schema_counts = schema_map.groupby("fiscal_year")["standardized_field"].nunique()
    schema_duplicates = int(
        schema_map.duplicated(["fiscal_year", "standardized_field"], keep=False).sum()
    )
    assert_evidence(
        "raw_workbook_hashes",
        not raw_hash_failures,
        (
            f"Recomputed SHA-256 for {len(present_raw)} workbooks; mismatches: "
            f"{', '.join(raw_hash_failures) if raw_hash_failures else 'none'}"
        ),
    )
    assert_evidence(
        "raw_schema_grain",
        schema_duplicates == 0 and schema_counts.nunique() == 1,
        (
            f"Schema-map duplicate year-fields: {schema_duplicates}; "
            f"fields per year: {sorted(schema_counts.unique().tolist())}"
        ),
    )
    assert_evidence(
        "retrieval_time_boundary",
        raw_manifest["retrieval_timestamp_utc"].eq("unavailable").all()
        and raw_manifest["file_mtime_utc"].eq("unavailable_not_persisted").all()
        and raw_manifest["repository_commit_timestamp"].ne("unavailable").all(),
        (
            "Original retrieval time and volatile checkout mtime are explicitly "
            "unavailable; deterministic repository commit timestamps are separate."
        ),
    )
    provenance_meta = manifests["02b_build_raw_data_manifest"]["metadata"]
    assert_evidence(
        "provenance_manifest_sync",
        int(provenance_meta["present_workbooks"]) == len(present_raw)
        and int(provenance_meta["configured_fiscal_years"]) == configured_years,
        (
            f"Provenance CSV has {len(present_raw)}/{configured_years} present/configured; "
            "stage manifest agrees."
        ),
    )

    # Stable administrative-lineage identity.
    identified = pd.read_csv(
        REPO_ROOT / "data" / "processed" / "incineration_panel_identified.csv",
        dtype={
            "facility_code": "string",
            "stable_site_id": "string",
            "asset_episode_id": "string",
        },
    )
    identity_meta = manifests["02a_build_facility_identity"]["metadata"]
    stable_sites = int(identified["stable_site_id"].nunique())
    asset_episodes = int(identified["asset_episode_id"].nunique())
    duplicate_site_year_rows = int(
        identified.duplicated(["stable_site_id", "fiscal_year"], keep=False).sum()
    )
    maximum_years_per_site = int(
        identified.groupby("stable_site_id")["fiscal_year"].nunique().max()
    )
    fy2019 = identified[identified["fiscal_year"].eq(2019)]
    fy2020 = identified[identified["fiscal_year"].eq(2020)]
    fy2009 = identified[identified["fiscal_year"].eq(2009)]
    fy2013 = identified[identified["fiscal_year"].eq(2013)]
    official_overlap = len(
        clean_identifier(fy2019["facility_code"])
        & clean_identifier(fy2020["facility_code"])
    )
    stable_overlap = len(
        clean_identifier(fy2019["stable_site_id"])
        & clean_identifier(fy2020["stable_site_id"])
    )
    gap_official_overlap = len(
        clean_identifier(fy2009["facility_code"])
        & clean_identifier(fy2013["facility_code"])
    )
    gap_stable_overlap = len(
        clean_identifier(fy2009["stable_site_id"])
        & clean_identifier(fy2013["stable_site_id"])
    )
    collapsed_duplicate_rows = int(
        (identified["source_record_multiplicity"].fillna(1).astype(int) - 1).sum()
    )
    low_margin = pd.read_csv(
        OUTPUT_DIR / "identity_low_margin_links.csv",
        dtype={
            "source_record_id": "string",
            "identity_predecessor_record_id": "string",
            "identity_match_current_alternative_record_id": "string",
            "identity_match_prior_competitor_record_id": "string",
        },
    )
    matched = ~identified["identity_match_method"].eq("new_site")
    minimum_match_score = float(identity_meta["minimum_match_score"])
    minimum_unambiguous_margin = float(
        identity_meta["minimum_unambiguous_margin"]
    )
    expected_uncertain = matched & identified["identity_match_margin"].lt(
        minimum_unambiguous_margin
    )
    observed_uncertain = identified["identity_match_uncertain"].fillna(False).astype(bool)
    strong_override = identified[
        "identity_match_strong_evidence_override"
    ].fillna(False).astype(bool)
    low_margin_assignments = int(observed_uncertain.sum())
    uncertain_lineages = int(
        identified.loc[observed_uncertain, "stable_site_id"].nunique()
    )
    expected_uncertain_ids = set(
        identified.loc[observed_uncertain, "source_record_id"].astype(str)
    )
    exposed_uncertain_ids = set(low_margin["source_record_id"].astype(str))
    observed_minimum_margin = np.minimum(
        identified.loc[matched, "identity_match_current_row_margin"].to_numpy(float),
        identified.loc[matched, "identity_match_prior_record_margin"].to_numpy(float),
    )
    ordered_episodes = identified.sort_values(["asset_episode_id", "fiscal_year"])
    continued_start_resets = int(
        ordered_episodes.groupby("asset_episode_id")["year_started"]
        .diff()
        .abs()
        .ge(3)
        .sum()
    )
    identity_values = {
        "raw_source_rows": int(identity_meta.get("raw_source_rows", len(identified))),
        "retained_rows": len(identified),
        "stable_sites": stable_sites,
        "asset_episodes": asset_episodes,
        "duplicate_site_year_rows": duplicate_site_year_rows,
        "maximum_years_per_site": maximum_years_per_site,
        "fy2020_official_code_overlap": official_overlap,
        "fy2020_stable_site_overlap": stable_overlap,
        "fy2009_fy2013_official_code_overlap": gap_official_overlap,
        "fy2009_fy2013_stable_site_overlap": gap_stable_overlap,
        "collapsed_exact_duplicate_rows": collapsed_duplicate_rows,
        "low_margin_assignments": low_margin_assignments,
        "uncertain_lineages": uncertain_lineages,
    }
    assert_evidence(
        "stable_site_unique_grain",
        duplicate_site_year_rows == 0,
        f"Duplicate stable-lineage-year rows: {duplicate_site_year_rows}",
    )
    assert_evidence(
        "identity_duplicate_and_episode_guards",
        collapsed_duplicate_rows
        == int(identity_meta["collapsed_exact_duplicate_rows"])
        and identified["source_record_id"].is_unique
        and continued_start_resets == 0,
        (
            f"Collapsed exact duplicate rows: {collapsed_duplicate_rows}; "
            f"unique canonical record IDs: {identified['source_record_id'].is_unique}; "
            f"continued episode start-year resets >=3 years: {continued_start_resets}."
        ),
    )
    assert_evidence(
        "identity_executable_guardrails",
        int(identity_meta.get("golden_same_link_checks", 0)) >= 3
        and int(identity_meta.get("golden_separation_checks", 0)) >= 3
        and int(identity_meta.get("permutation_invariance_prefectures", 0)) >= 6
        and int(identity_meta.get("insertion_invariance_prefectures", 0)) >= 6
        and identified.loc[matched, "identity_match_score"].ge(
            minimum_match_score
        ).all()
        and np.allclose(
            observed_minimum_margin,
            identified.loc[matched, "identity_match_margin"].to_numpy(float),
        )
        and expected_uncertain.equals(observed_uncertain)
        and not (observed_uncertain & ~strong_override).any()
        and low_margin_assignments
        == int(identity_meta.get("uncertain_links_exposed", -1))
        and len(low_margin) == low_margin_assignments
        and not low_margin["source_record_id"].duplicated().any()
        and expected_uncertain_ids == exposed_uncertain_ids
        and low_margin["identity_match_strong_evidence_override"]
        .fillna(False)
        .astype(bool)
        .all()
        and int(identity_meta.get("accepted_subthreshold_links", -1)) == 0
        and int(identity_meta.get("accepted_weak_ambiguous_links", -1)) == 0,
        (
            "Golden, permutation, insertion, threshold, two-sided-margin, and "
            "uncertainty-exposure guardrails agree; "
            f"{low_margin_assignments} accepted uncertain links across "
            f"{uncertain_lineages} lineages are exposed exactly once."
        ),
    )
    assert_evidence(
        "identity_manifest_sync",
        int(
            identity_meta.get(
                "retained_unique_source_records",
                identity_meta.get("source_rows", len(identified)),
            )
        )
        == len(identified)
        and int(identity_meta["stable_sites"]) == stable_sites
        and int(identity_meta["asset_episodes"]) == asset_episodes
        and int(identity_meta["duplicate_site_year_rows"])
        == duplicate_site_year_rows
        and int(identity_meta["maximum_years_per_site"]) == maximum_years_per_site
        and int(identity_meta["fy2020_official_code_overlap"]) == official_overlap
        and int(identity_meta["fy2020_stable_site_overlap"]) == stable_overlap,
        (
            f"Recomputed {len(identified):,} retained records, {stable_sites} stable administrative lineages, "
            f"{asset_episodes} asset episodes, "
            f"and FY2019-FY2020 overlaps {official_overlap} official/{stable_overlap} stable."
        ),
    )
    assert_evidence(
        "official_code_regime_break",
        official_overlap == 0 and stable_overlap > 0,
        (
            f"FY2019-FY2020 official-code overlap is {official_overlap}; "
            f"administrative-lineage overlap is {stable_overlap}."
        ),
    )

    # FY2024 fleet count-volume decomposition.
    fleet = pd.read_csv(OUTPUT_DIR / "fleet_decomposition.csv")
    fy2024_rows = fleet[fleet["fiscal_year"].eq(2024)]
    if len(fy2024_rows) != 1:
        raise ValueError(f"Expected one FY2024 fleet row, found {len(fy2024_rows)}")
    fy2024 = fy2024_rows.iloc[0]
    facility_participation = (
        fy2024["installed_generation_facilities"] / fy2024["facilities"] * 100
    )
    throughput_coverage = (
        fy2024["positive_output_throughput_t"] / fy2024["total_throughput_t"] * 100
    )
    active_positive_output_share = (
        fy2024["positive_output_facilities"]
        / fy2024["positive_throughput_facilities"]
        * 100
    )
    valid_throughput_coverage = (
        fy2024["valid_output_throughput_t"] / fy2024["total_throughput_t"] * 100
    )
    fleet_identity_error = float(
        (fleet["fleet_valid_gross_mwh_t"] - fleet["identity_product_mwh_t"])
        .abs()
        .max()
    )
    fleet_meta = manifests["05_fleet_decomposition"]["metadata"]
    segments = pd.read_csv(OUTPUT_DIR / "fy2024_fleet_segments.csv")
    assert_evidence(
        "fy2024_fleet_arithmetic",
        close(facility_participation, fy2024["facility_participation_pct"])
        and close(throughput_coverage, fy2024["throughput_coverage_pct"])
        and close(
            active_positive_output_share,
            fy2024["active_positive_output_facility_share_pct"],
        )
        and close(
            valid_throughput_coverage,
            fy2024["engineering_valid_throughput_coverage_pct"],
        ),
        (
            f"FY2024 recomputed all-record/active/throughput/valid-throughput shares: "
            f"{facility_participation:.6f}/{active_positive_output_share:.6f}/"
            f"{throughput_coverage:.6f}/"
            f"{valid_throughput_coverage:.6f}%."
        ),
    )
    assert_evidence(
        "fleet_decomposition_identity",
        fleet_identity_error < 1e-12,
        f"Maximum fleet decomposition identity error: {fleet_identity_error:.3e}",
    )
    assert_evidence(
        "fy2024_segment_totals",
        int(segments["facility_rows"].sum()) == int(fy2024["facilities"])
        and close(segments["facility_share_pct"].sum(), 100.0)
        and int(
            segments.loc[
                segments["segment"].isin(
                    ["Operating generator", "Operating non-generator"]
                ),
                "facility_rows",
            ].sum()
        )
        == int(fy2024["positive_throughput_facilities"]),
        (
            f"FY2024 segment rows sum to {int(segments['facility_rows'].sum())}; "
            f"facility shares sum to {segments['facility_share_pct'].sum():.6f}%; "
            f"positive-throughput rows total {int(fy2024['positive_throughput_facilities'])}."
        ),
    )
    assert_evidence(
        "fleet_manifest_sync",
        close(
            fleet_meta["fy2024_facility_participation_pct"],
            fy2024["facility_participation_pct"],
        )
        and close(
            fleet_meta["fy2024_throughput_coverage_pct"],
            fy2024["throughput_coverage_pct"],
        )
        and close(
            fleet_meta["fy2024_active_positive_output_facility_share_pct"],
            fy2024["active_positive_output_facility_share_pct"],
        )
        and close(
            fleet_meta["fy2024_installed_design_capacity_share_pct"],
            fy2024["installed_design_capacity_share_pct"],
        ),
        "FY2024 fleet CSV and stage manifest headline metrics agree.",
    )

    # Firth adoption evidence.
    transition = pd.read_csv(OUTPUT_DIR / "figure2_transition_effects.csv")
    adoption_meta = manifests["05a_power_adoption"]["metadata"]
    model_names = transition["model"].drop_duplicates().tolist()
    broad_name = "Broad exact-year risk frame"
    prior_name = "Prior-operation risk frame"
    continuity_name = "Same-asset-episode continuity sensitivity"
    identity_certain_name = "Identity-certain-lineage sensitivity"
    broad = transition[transition["model"].eq(broad_name)]
    prior = transition[transition["model"].eq(prior_name)]
    continuity = transition[transition["model"].eq(continuity_name)]
    identity_certain = transition[
        transition["model"].eq(identity_certain_name)
    ]
    if broad.empty or prior.empty or continuity.empty or identity_certain.empty:
        raise ValueError(f"Unexpected adoption model labels: {model_names}")
    broad_capacity = broad[broad["term"].eq("log_processing_capacity")].iloc[0]
    prior_capacity = prior[prior["term"].eq("log_processing_capacity")].iloc[0]
    broad_rows = int(broad["observations"].iloc[0])
    broad_sites = int(broad["sites"].iloc[0])
    broad_events = int(broad["events"].iloc[0])
    prior_rows = int(prior["observations"].iloc[0])
    prior_sites = int(prior["sites"].iloc[0])
    prior_events = int(prior["events"].iloc[0])
    continuity_rows = int(continuity["observations"].iloc[0])
    continuity_sites = int(continuity["sites"].iloc[0])
    continuity_events = int(continuity["events"].iloc[0])
    identity_certain_rows = int(identity_certain["observations"].iloc[0])
    identity_certain_sites = int(identity_certain["sites"].iloc[0])
    identity_certain_events = int(identity_certain["events"].iloc[0])
    capacity_or_300_vs_100 = math.exp(
        float(broad_capacity["coefficient"]) * math.log(2.0)
    )
    prior_capacity_or_300_vs_100 = math.exp(
        float(prior_capacity["coefficient"]) * math.log(2.0)
    )
    bootstrap = pd.read_csv(OUTPUT_DIR / "adoption_bootstrap_coefficients.csv")
    bootstrap_counts = bootstrap.groupby("model")["repetition"].nunique().to_dict()
    pathways = pd.read_csv(OUTPUT_DIR / "adoption_pathway_audit.csv")
    pathway_counts = pathways["pathway_category"].value_counts().to_dict()
    bridge = pd.read_csv(OUTPUT_DIR / "post_adoption_bridge.csv")
    trajectories = pd.read_csv(OUTPUT_DIR / "post_adoption_trajectories.csv")
    exact_pathway_events = int(pathways["exact_one_year_lag"].fillna(False).astype(bool).sum())
    adoption_frame = build_adoption_frame(identified)
    exact_frame = build_adoption_model_frame(
        identified,
        adoption_frame,
        exact_year_only=True,
    )
    quartile_labels = ["Q1 smallest", "Q2", "Q3", "Q4 largest"]
    exact_frame["capacity_quartile"] = pd.qcut(
        exact_frame["lag_capacity_t_day"],
        4,
        labels=quartile_labels,
        duplicates="drop",
    )
    quartile_counts = (
        exact_frame.groupby("capacity_quartile", observed=True)
        .agg(
            risk_rows=("adopt_power_this_year", "size"),
            events=("adopt_power_this_year", "sum"),
        )
        .astype(int)
        .to_dict(orient="index")
    )
    assert_evidence(
        "adoption_capacity_quartile_counts",
        set(quartile_counts) == set(quartile_labels)
        and sum(item["risk_rows"] for item in quartile_counts.values()) == broad_rows
        and sum(item["events"] for item in quartile_counts.values()) == broad_events,
        f"Exact-frame capacity-quartile rows/events: {quartile_counts}",
    )
    assert_evidence(
        "firth_method_and_sample_sync",
        "Firth" in adoption_meta["bias_reduction"]
        and broad_rows == int(adoption_meta["exact_model_rows"])
        and broad_sites == int(adoption_meta["exact_model_sites"])
        and broad_events == int(adoption_meta["exact_model_events"])
        and prior_rows == int(adoption_meta["prior_operation_rows"])
        and prior_sites == int(adoption_meta["prior_operation_sites"])
        and prior_events == int(adoption_meta["prior_operation_events"])
        and continuity_rows == int(adoption_meta["same_episode_continuity_rows"])
        and continuity_sites == int(adoption_meta["same_episode_continuity_sites"])
        and continuity_events == int(adoption_meta["same_episode_continuity_events"])
        and identity_certain_rows == int(adoption_meta["identity_certain_rows"])
        and identity_certain_sites == int(adoption_meta["identity_certain_sites"])
        and identity_certain_events == int(adoption_meta["identity_certain_events"])
        and int(adoption_meta["uncertain_identity_lineages"])
        == identity_values["uncertain_lineages"],
        (
            f"Firth samples are {broad_rows}/{broad_sites}/{broad_events} broad and "
            f"{prior_rows}/{prior_sites}/{prior_events} prior-operation and "
            f"{continuity_rows}/{continuity_sites}/{continuity_events} same-episode "
            f"and {identity_certain_rows}/{identity_certain_sites}/"
            f"{identity_certain_events} identity-certain rows/lineages/events."
        ),
    )
    adoption_config = manifests["05a_power_adoption"]["analysis_config"]
    assert_evidence(
        "adoption_estimand_configuration",
        bool(adoption_config.get("adoption_exact_lag_requires_same_stable_lineage"))
        and bool(adoption_config.get("adoption_primary_allows_asset_episode_change"))
        and bool(
            adoption_config.get(
                "adoption_continuity_sensitivity_requires_same_asset_episode"
            )
        )
        and broad_rows - continuity_rows
        == int(adoption_meta["cross_episode_exact_rows"])
        and broad_events - continuity_events
        == int(adoption_meta["cross_episode_exact_events"]),
        (
            "Primary entry is broad administrative-lineage entry; same-episode "
            f"sensitivity excludes {broad_rows - continuity_rows} rows and "
            f"{broad_events - continuity_events} events."
        ),
    )
    convergence = adoption_meta.get("model_convergence", {})
    assert_evidence(
        "firth_convergence",
        set(convergence)
        == {
            "broad",
            "prior_operation",
            "same_episode_continuity",
            "identity_certain",
        }
        and all(bool(item.get("converged")) for item in convergence.values()),
        f"Firth convergence metadata: {convergence}",
    )
    assert_evidence(
        "firth_estimates_finite",
        len(transition) == 4 * len(ADOPTION_FOCAL_TERMS)
        and np.isfinite(
            transition[
                [
                    "coefficient",
                    "standard_error_model_based",
                    "bootstrap_ci_low",
                    "bootstrap_ci_high",
                ]
            ].to_numpy(float)
        ).all(),
        (
            f"All {len(transition)} focal Firth estimates and uncertainty fields are finite."
        ),
    )
    joint_tests = adoption_meta.get("joint_age_tests", {})
    assert_evidence(
        "cluster_bootstrap_joint_tests",
        set(joint_tests)
        == {
            "broad_cluster_bootstrap_covariance",
            "prior_operation_cluster_bootstrap_covariance",
            "same_episode_cluster_bootstrap_covariance",
            "identity_certain_cluster_bootstrap_covariance",
            "broad_model_based",
            "prior_operation_model_based",
            "same_episode_model_based",
            "identity_certain_model_based",
        }
        and all(
            len(values) == 4
            and int(values[3]) == int(adoption_meta["bootstrap_repetitions"])
            and np.isfinite(np.asarray(values, dtype=float)).all()
            for key, values in joint_tests.items()
            if "cluster_bootstrap" in key
        ),
        (
            f"Cluster-bootstrap joint tests: {joint_tests}"
        ),
    )
    assert_evidence(
        "cluster_bootstrap_sync",
        set(bootstrap_counts)
        == {
            "broad",
            "prior_operation",
            "same_episode_continuity",
            "identity_certain",
        }
        and set(bootstrap_counts.values())
        == {int(adoption_meta["bootstrap_repetitions"])}
        and bootstrap["converged"].fillna(False).astype(bool).all()
        and np.isfinite(bootstrap[ADOPTION_FOCAL_TERMS].to_numpy(float)).all(),
        f"Stable-lineage bootstrap repetitions by model: {bootstrap_counts}",
    )
    assert_evidence(
        "pathway_and_bridge_sync",
        pathway_counts == adoption_meta["pathway_counts"]
        and len(pathways) == int(adoption_meta["descriptive_events"])
        and len(bridge) == int(adoption_meta["post_entry"]["exact_events"])
        and exact_pathway_events == len(bridge),
        (
            f"Pathway events: {len(pathways)} descriptive, {exact_pathway_events} exact; "
            f"bridge rows: {len(bridge)}."
        ),
    )
    event_time_one = adoption_meta["post_entry"].get("event_time_one", {})
    trajectory_sync = True
    for row in trajectories.loc[trajectories["event_time"].eq(1)].to_dict(
        orient="records"
    ):
        key = (
            "all"
            if row["series"] == "All exact-year entrants"
            else str(row["pathway_category"])
        )
        recorded = event_time_one.get(key, {})
        trajectory_sync &= (
            int(recorded.get("rows", -1)) == int(row["rows"])
            and int(recorded.get("events", -1)) == int(row["events"])
            and close(recorded.get("mean_gross_mwh_t", math.nan), row["mean_gross_mwh_t"])
            and close(
                recorded.get("mean_gross_rank_pct", math.nan),
                row["mean_gross_rank_pct"],
            )
            and close(
                recorded.get("mean_design_rank_pct", math.nan),
                row["mean_design_rank_pct"],
            )
            and close(
                recorded.get("mean_capacity_factor_rank_pct", math.nan),
                row["mean_capacity_factor_rank_pct"],
            )
        )
    assert_evidence(
        "post_entry_trajectory_sync",
        trajectory_sync and len(event_time_one) == 4,
        "Event-time-one pathway rows and component ranks match adoption metadata.",
    )

    # Generator design and operating components.
    components = pd.read_csv(OUTPUT_DIR / "generator_component_results.csv")
    regression_meta = manifests["05_panel_regression"]["metadata"]
    diagnostic = parse_diagnostic_table(OUTPUT_DIR / "regression_results.md")
    regression_report_text = (OUTPUT_DIR / "regression_results.md").read_text(
        encoding="utf-8"
    )
    diagnostic_r2_match = re.search(
        r"R-squared (?:rises|changes) from ([0-9.]+) to ([0-9.]+)",
        regression_report_text,
    )
    if diagnostic_r2_match is None:
        raise ValueError("Regression report is missing the diagnostic R-squared change")
    report_legacy_r2, report_sizing_r2 = map(
        float, diagnostic_r2_match.groups()
    )
    design = components[components["model"].eq("design_intensity")]
    cohort_design = design[design["term"].str.startswith("cohort_")]
    design_rows = int(design["observations"].iloc[0])
    age_diagnostic = diagnostic["facility_age_years"]
    utilization_diagnostic = diagnostic["capacity_utilization_raw"]
    sizing_diagnostic = diagnostic["log_generator_design_intensity"]
    assert_evidence(
        "component_sample_sync",
        design_rows == int(regression_meta["engineering_valid_rows"])
        and components["observations"].nunique() == 1
        and len(components) == int(regression_meta["component_result_rows"]),
        (
            f"Component output has {len(components)} terms on {design_rows} "
            f"engineering-valid rows and {regression_meta['stable_sites']} stable administrative lineages."
        ),
    )
    assert_evidence(
        "component_estimates_finite",
        set(components["model"])
        == {"design_intensity", "capacity_factor"}
        and len(cohort_design) == 3
        and np.isfinite(
            components[
                [
                    "coefficient",
                    "standard_error",
                    "ci_low",
                    "ci_high",
                    "p_value",
                    "r_squared",
                ]
            ].to_numpy(float)
        ).all(),
        "All component-model focal estimates and uncertainty fields are finite.",
    )
    diagnostic_meta = regression_meta.get("diagnostic_terms", {})
    diagnostic_sync = set(diagnostic_meta) == set(diagnostic)
    for term, values in diagnostic.items():
        recorded = diagnostic_meta.get(term, {})
        for key, value in values.items():
            recorded_value = recorded.get(key)
            if math.isnan(value):
                diagnostic_sync &= recorded_value is None
            else:
                diagnostic_sync &= recorded_value is not None and close(
                    recorded_value, value, 1e-4
                )
    assert_evidence(
        "diagnostic_manifest_sync",
        diagnostic_sync
        and close(regression_meta["legacy_rsquared"], report_legacy_r2, 1e-4)
        and close(regression_meta["sizing_adjusted_rsquared"], report_sizing_r2, 1e-4),
        (
            "Generated diagnostic coefficients and p-values match the stage manifest "
            f"for {len(diagnostic)} terms."
        ),
    )

    # Major-revision sparse-entry and raw-quantity evidence.
    revised = pd.read_csv(OUTPUT_DIR / "revised_entry_results.csv")
    revised_bootstrap = pd.read_csv(OUTPUT_DIR / "revised_entry_bootstrap.csv")
    revised_influence = pd.read_csv(OUTPUT_DIR / "revised_entry_influence.csv")
    revised_robustness = pd.read_csv(OUTPUT_DIR / "revised_entry_robustness.csv")
    state_audit = pd.read_csv(OUTPUT_DIR / "entry_state_audit.csv").set_index(
        "metric"
    )["value"]
    event_composition = pd.read_csv(OUTPUT_DIR / "adoption_event_composition.csv")
    raw_quantities = pd.read_csv(OUTPUT_DIR / "raw_quantity_component_results.csv")
    adjusted_components = pd.read_csv(OUTPUT_DIR / "figure3_adjusted_components.csv")
    revision_meta = manifests["05b_scientific_revision"]["metadata"]
    revised_models = set(revised["model"])
    revised_repetitions = revised_bootstrap.groupby("model")["repetition"].nunique()
    broad_revised = revised[revised["model"].eq("Broad reduced-DF frame")]
    broad_scale = broad_revised[
        broad_revised["term"].eq("log_processing_capacity")
    ].iloc[0]
    broad_age = broad_revised[broad_revised["term"].eq("age_per_10y")].iloc[0]
    scale_or = math.exp(float(broad_scale["coefficient"]) * math.log(2.0))
    scale_or_ci = (
        math.exp(float(broad_scale["bootstrap_ci_low"]) * math.log(2.0)),
        math.exp(float(broad_scale["bootstrap_ci_high"]) * math.log(2.0)),
    )
    influence_range = (
        float(revised_influence["odds_ratio_300_vs_100"].min()),
        float(revised_influence["odds_ratio_300_vs_100"].max()),
    )
    functional_form = revised_robustness[
        revised_robustness["check_type"].eq("functional_form")
    ]
    geographic_deletion = revised_robustness[
        revised_robustness["check_type"].eq("geographic_deletion")
    ]
    reporting_state = revised_robustness[
        revised_robustness["check_type"].eq("reporting_state")
    ]
    functional_form_range = (
        float(functional_form["odds_ratio_300_vs_100"].min()),
        float(functional_form["odds_ratio_300_vs_100"].max()),
    )
    geographic_range = (
        float(geographic_deletion["odds_ratio_300_vs_100"].min()),
        float(geographic_deletion["odds_ratio_300_vs_100"].max()),
    )
    pathway_counts_revised = event_composition["pathway_category"].value_counts().to_dict()
    assert_evidence(
        "revised_entry_model_sync",
        revised_models
        == {
            "Broad reduced-DF frame",
            "Prior-operation reduced-DF frame",
            "Same-episode reduced-DF frame",
            "Identity-certain reduced-DF frame",
        }
        and revised.groupby("model").size().eq(4).all()
        and revised_repetitions.eq(1999).all()
        and revised_bootstrap["converged"].fillna(False).astype(bool).all()
        and int(revision_meta["bootstrap_repetitions"]) == 1999,
        (
            f"Reduced-DF frames: {sorted(revised_models)}; bootstrap repetitions: "
            f"{revised_repetitions.to_dict()}."
        ),
    )
    assert_evidence(
        "revised_event_composition_and_influence",
        pathway_counts_revised
        == {"Continuity-lineage entry": 24, "Rebuild/replacement-like entry": 11}
        and len(revised_influence) == 70
        and revised_influence["converged"].fillna(False).astype(bool).all()
        and influence_range[0] > 6.0
        and influence_range[1] < 7.5,
        (
            f"Modeled event pathways: {pathway_counts_revised}; event-attack scale OR "
            f"range {influence_range[0]:.4f}-{influence_range[1]:.4f}."
        ),
    )
    robustness_meta = revision_meta["entry_robustness"]
    assert_evidence(
        "revised_entry_functional_form_and_geographic_robustness",
        len(functional_form) == 2
        and len(geographic_deletion)
        == int(event_composition["prefecture"].nunique())
        and revised_robustness["converged"].fillna(False).astype(bool).all()
        and functional_form["ci_low_model_based"].gt(1).all()
        and geographic_deletion["odds_ratio_300_vs_100"].gt(1).all()
        and close(
            functional_form_range[0],
            robustness_meta["functional_form_scale_or_min"],
        )
        and close(
            functional_form_range[1],
            robustness_meta["functional_form_scale_or_max"],
        )
        and close(
            geographic_range[0],
            robustness_meta["geographic_deletion_scale_or_min"],
        )
        and close(
            geographic_range[1],
            robustness_meta["geographic_deletion_scale_or_max"],
        ),
        (
            f"Alternative-form scale OR range {functional_form_range[0]:.4f}-"
            f"{functional_form_range[1]:.4f}; leave-one-prefecture range "
            f"{geographic_range[0]:.4f}-{geographic_range[1]:.4f} across "
            f"{len(geographic_deletion)} event prefectures."
        ),
    )
    assert_evidence(
        "entry_reporting_state_audit",
        int(state_audit["positive_output_without_positive_capacity_rows"]) == 49
        and int(state_audit["positive_output_without_positive_capacity_lineages"])
        == 6
        and int(state_audit["modeled_events_prior_year_positive_output"]) == 0
        and len(reporting_state) == 1
        and int(reporting_state.iloc[0]["events"])
        == int(state_audit["strict_two_prior_year_events"])
        and float(reporting_state.iloc[0]["ci_low_model_based"]) > 1,
        (
            f"Positive-output rows without positive reported capacity: "
            f"{int(state_audit['positive_output_without_positive_capacity_rows'])} "
            f"across {int(state_audit['positive_output_without_positive_capacity_lineages'])} "
            f"lineages; strict state frame retains "
            f"{int(state_audit['strict_two_prior_year_rows']):,}/"
            f"{int(state_audit['strict_two_prior_year_lineages']):,}/"
            f"{int(state_audit['strict_two_prior_year_events'])} rows/lineages/events."
        ),
    )
    assert_evidence(
        "frozen_primary_not_legacy_sensitivity",
        close(
            scale_or,
            revision_meta["entry_models"]["Broad reduced-DF frame"][
                "scale_contrast"
            ]["odds_ratio_300_vs_100"],
        )
        and not close(scale_or, capacity_or_300_vs_100, 1e-3),
        (
            f"Frozen five-parameter primary OR is {scale_or:.4f}; the earlier "
            f"higher-dimensional sensitivity OR is {capacity_or_300_vs_100:.4f}."
        ),
    )
    installed_rows = raw_quantities[
        raw_quantities["outcome"].eq("log_installed_capacity_kw")
    ]
    assert_evidence(
        "raw_quantity_component_sync",
        len(installed_rows) == 4
        and set(adjusted_components["component"])
        == {"Installed electrical capacity", "Electrical capacity factor"}
        and raw_quantities["observations"].eq(design_rows).all()
        and raw_quantities["lineages"].eq(int(regression_meta["stable_sites"])).all(),
        (
            f"Raw quantity results have {len(raw_quantities)} focal rows and adjusted "
            f"component contrasts have {len(adjusted_components)} rows."
        ),
    )

    metrics = {
        "python_versions": python_versions,
        "provenance": {
            "configured_years": int(configured_years),
            "present_workbooks": int(len(present_raw)),
            "total_bytes": int(pd.to_numeric(present_raw["byte_size"]).sum()),
        },
        "identity": identity_values,
        "fleet": {
            "facilities": int(fy2024["facilities"]),
            "installed_facilities": int(fy2024["installed_generation_facilities"]),
            "facility_participation_pct": float(fy2024["facility_participation_pct"]),
            "positive_throughput_facilities": int(
                fy2024["positive_throughput_facilities"]
            ),
            "active_positive_output_facility_share_pct": float(
                fy2024["active_positive_output_facility_share_pct"]
            ),
            "throughput_coverage_pct": float(fy2024["throughput_coverage_pct"]),
            "installed_design_capacity_share_pct": float(
                fy2024["installed_design_capacity_share_pct"]
            ),
            "engineering_valid_throughput_coverage_pct": float(
                fy2024["engineering_valid_throughput_coverage_pct"]
            ),
            "conditional_valid_gross_mwh_t": float(
                fy2024["conditional_valid_gross_mwh_t"]
            ),
            "fleet_valid_gross_mwh_t": float(fy2024["fleet_valid_gross_mwh_t"]),
        },
        "adoption": {
            "bias_reduction": adoption_meta["bias_reduction"],
            "bootstrap_repetitions": int(adoption_meta["bootstrap_repetitions"]),
            "broad_rows": broad_rows,
            "broad_sites": broad_sites,
            "broad_events": broad_events,
            "prior_rows": prior_rows,
            "prior_sites": prior_sites,
            "prior_events": prior_events,
            "continuity_rows": continuity_rows,
            "continuity_sites": continuity_sites,
            "continuity_events": continuity_events,
            "identity_certain_rows": identity_certain_rows,
            "identity_certain_sites": identity_certain_sites,
            "identity_certain_events": identity_certain_events,
            "cross_episode_rows": int(adoption_meta["cross_episode_exact_rows"]),
            "cross_episode_events": int(
                adoption_meta["cross_episode_exact_events"]
            ),
            "descriptive_events": int(len(pathways)),
            "exact_observed_events": int(len(bridge)),
            "broad_capacity_coefficient": float(broad_capacity["coefficient"]),
            "prior_capacity_coefficient": float(prior_capacity["coefficient"]),
            "capacity_or_300_vs_100": capacity_or_300_vs_100,
            "prior_capacity_or_300_vs_100": prior_capacity_or_300_vs_100,
            "broad_age_joint_p_value": float(
                joint_tests["broad_cluster_bootstrap_covariance"][2]
            ),
            "prior_age_joint_p_value": float(
                joint_tests["prior_operation_cluster_bootstrap_covariance"][2]
            ),
            "continuity_age_joint_p_value": float(
                joint_tests["same_episode_cluster_bootstrap_covariance"][2]
            ),
            "identity_certain_age_joint_p_value": float(
                joint_tests["identity_certain_cluster_bootstrap_covariance"][2]
            ),
            "pathway_counts": pathway_counts,
            "capacity_quartile_counts": quartile_counts,
            "event_time_one": adoption_meta["post_entry"]["event_time_one"],
        },
        "components": {
            "rows": design_rows,
            "stable_sites": int(regression_meta["stable_sites"]),
            "design_r_squared": float(regression_meta["design_model"]["rsquared"]),
            "capacity_factor_r_squared": float(
                regression_meta["capacity_factor_model"]["rsquared"]
            ),
            "legacy_age_coefficient": age_diagnostic["legacy_coefficient"],
            "legacy_age_p_value": age_diagnostic["legacy_p_value"],
            "sizing_age_coefficient": age_diagnostic["sizing_adjusted_coefficient"],
            "sizing_age_p_value": age_diagnostic["sizing_adjusted_p_value"],
            "sizing_utilization_coefficient": utilization_diagnostic[
                "sizing_adjusted_coefficient"
            ],
            "sizing_utilization_p_value": utilization_diagnostic[
                "sizing_adjusted_p_value"
            ],
            "sizing_coefficient": sizing_diagnostic["sizing_adjusted_coefficient"],
            "legacy_r_squared": float(regression_meta["legacy_rsquared"]),
            "sizing_r_squared": float(regression_meta["sizing_adjusted_rsquared"]),
            "throughput_elasticity": float(
                regression_meta["gross_output_elasticities"]["throughput"]
            ),
            "electrical_capacity_elasticity": float(
                regression_meta["gross_output_elasticities"][
                    "installed_electrical_capacity"
                ]
            ),
            "before_1990_design_coefficient": float(
                cohort_design.loc[
                    cohort_design["term"].eq("cohort_Before 1990"), "coefficient"
                ].iloc[0]
            ),
        },
        "revision": {
            "bootstrap_repetitions": 1999,
            "scale_or": scale_or,
            "scale_or_ci_low": scale_or_ci[0],
            "scale_or_ci_high": scale_or_ci[1],
            "broad_age_coefficient": float(broad_age["coefficient"]),
            "broad_age_ci_low": float(broad_age["bootstrap_ci_low"]),
            "broad_age_ci_high": float(broad_age["bootstrap_ci_high"]),
            "influence_or_low": influence_range[0],
            "influence_or_high": influence_range[1],
            "functional_form_or_low": functional_form_range[0],
            "functional_form_or_high": functional_form_range[1],
            "geographic_or_low": geographic_range[0],
            "geographic_or_high": geographic_range[1],
            "event_prefectures": int(len(geographic_deletion)),
            "strict_state_rows": int(state_audit["strict_two_prior_year_rows"]),
            "strict_state_lineages": int(
                state_audit["strict_two_prior_year_lineages"]
            ),
            "strict_state_events": int(state_audit["strict_two_prior_year_events"]),
            "strict_state_or": float(
                reporting_state.iloc[0]["odds_ratio_300_vs_100"]
            ),
            "ambiguous_capacity_output_rows": int(
                state_audit["positive_output_without_positive_capacity_rows"]
            ),
            "ambiguous_capacity_output_lineages": int(
                state_audit["positive_output_without_positive_capacity_lineages"]
            ),
            "continuity_events": int(pathway_counts_revised["Continuity-lineage entry"]),
            "rebuild_events": int(pathway_counts_revised["Rebuild/replacement-like entry"]),
            "installed_capacity_elasticity": float(
                installed_rows.loc[
                    installed_rows["term"].eq("log_capacity_t_day"), "coefficient"
                ].iloc[0]
            ),
            "adjusted_components": {
                f"{row.component}::{row.cohort}": float(row.percent_difference)
                for row in adjusted_components.itertuples(index=False)
            },
        },
    }
    return metrics, assertions


def normalize_document(text: str) -> str:
    normalized = unicodedata.normalize("NFKC", text)
    normalized = normalized.replace("{,}", ",").replace(r"\%", "%")
    normalized = normalized.replace("−", "-").replace("–", "-").replace("—", "-")
    return normalized


def number_pattern(value: float | int, decimals: Iterable[int] = ()) -> str:
    if isinstance(value, int) or float(value).is_integer() and not tuple(decimals):
        integer = int(value)
        variants = {str(integer), f"{integer:,}"}
    else:
        variants = set()
        for places in decimals:
            formatted = f"{float(value):.{places}f}"
            variants.add(formatted)
            if formatted.startswith("0."):
                variants.add(formatted[1:])
            if formatted.startswith("-0."):
                variants.add("-." + formatted.split(".", maxsplit=1)[1])
    return rf"(?<![\d.])(?:{'|'.join(re.escape(item) for item in sorted(variants, key=len, reverse=True))})(?!\d)"


def contains_context_number(
    text: str,
    context_pattern: str,
    value: float | int,
    decimals: Iterable[int] = (),
    window: int = 180,
) -> bool:
    number = number_pattern(value, decimals)
    pattern = rf"(?:{context_pattern}).{{0,{window}}}{number}|{number}.{{0,{window}}}(?:{context_pattern})"
    return re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL) is not None


def contains_number(text: str, value: float | int, decimals: Iterable[int] = ()) -> bool:
    return re.search(number_pattern(value, decimals), text) is not None


def add_requirement(
    checks: list[dict[str, Any]],
    check_id: str,
    document_key: str,
    condition: bool,
    expectation: str,
) -> None:
    checks.append(
        {
            "type": "required_claim",
            "id": check_id,
            "document": document_key,
            "path": DOCUMENTS[document_key],
            "passed": bool(condition),
            "detail": expectation,
        }
    )


def build_document_checks(metrics: dict[str, Any]) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    texts: dict[str, str] = {}
    for key, path in DOCUMENTS.items():
        required = key != "professor_lineage"
        exists = path.exists()
        checks.append(
            {
                "type": "document_presence",
                "id": f"{key}_present",
                "document": key,
                "path": path,
                "passed": exists or not required,
                "detail": "Required document exists." if required else "Optional lineage checked when present.",
            }
        )
        if exists:
            texts[key] = normalize_document(path.read_text(encoding="utf-8"))

    identity = metrics["identity"]
    fleet = metrics["fleet"]
    adoption = metrics["adoption"]
    components = metrics["components"]
    revision = metrics["revision"]

    manuscript_keys = [
        key
        for key in (
            "manuscript_md",
            "manuscript_tex",
            "professor_manuscript_md",
            "professor_manuscript_tex",
        )
        if key in texts
    ]
    for key in manuscript_keys:
        text = texts[key]
        is_professor_profile = key.startswith("professor_")
        add_requirement(
            checks,
            "stable_site_identity",
            key,
            re.search(
                r"(?:reconstruct|identit|resolver|link).{0,80}stable.{0,40}(?:site|lineage)|stable.{0,40}(?:site|lineage).{0,80}(?:reconstruct|identit|resolver|link)",
                text,
                re.IGNORECASE | re.DOTALL,
            )
            is not None
            and contains_context_number(
                text,
                r"stable.{0,30}(?:sites?|lineages?)",
                identity["stable_sites"],
            )
            and contains_context_number(
                text, r"asset episodes?", identity["asset_episodes"]
            ),
            (
                f"Explain administrative-lineage identity and report {identity['stable_sites']:,} lineages "
                f"and {identity['asset_episodes']:,} asset episodes."
            ),
        )
        add_requirement(
            checks,
            "official_code_break",
            key,
            re.search(
                r"FY?2019.{0,120}FY?2020|FY?2020.{0,120}FY?2019",
                text,
                re.IGNORECASE | re.DOTALL,
            )
            is not None
            and re.search(r"official.{0,40}(?:facility )?codes?", text, re.IGNORECASE)
            is not None,
            (
                "Disclose the FY2019-FY2020 official-code regime break and explain why "
                "official codes are not longitudinal identities."
            ),
        )
        add_requirement(
            checks,
            "official_code_gap_bridge",
            key,
            contains_context_number(
                text,
                r"FY?2009.{0,60}FY?2013|FY?2013.{0,60}FY?2009|longer.{0,30}bridge",
                identity["fy2009_fy2013_official_code_overlap"],
            )
            and contains_context_number(
                text,
                r"FY?2009.{0,60}FY?2013|FY?2013.{0,60}FY?2009|longer.{0,30}bridge",
                identity["fy2009_fy2013_stable_site_overlap"],
            ),
            (
                "Report the FY2009-FY2013 bridge exactly: "
                f"{identity['fy2009_fy2013_official_code_overlap']} overlapping official codes and "
                f"{identity['fy2009_fy2013_stable_site_overlap']:,} linked administrative lineages."
            ),
        )
        add_requirement(
            checks,
            "fy2024_count_volume",
            key,
            contains_context_number(
                text,
                r"facilit(?:y|ies).{0,40}(?:participation|share|count)|installed[- ]generation",
                fleet["facility_participation_pct"],
                (1,),
            )
            and contains_context_number(
                text,
                r"throughput|waste volume",
                fleet["throughput_coverage_pct"],
                (1,),
            )
            and contains_context_number(
                text,
                r"(?:waste-processing )?design capacity",
                fleet["installed_design_capacity_share_pct"],
                (1,),
            ),
            (
                "Report the FY2024 count-volume contrast: "
                f"{fleet['facility_participation_pct']:.1f}% facilities, "
                f"{fleet['throughput_coverage_pct']:.1f}% throughput, and "
                f"{fleet['installed_design_capacity_share_pct']:.1f}% design capacity."
            ),
        )
        if is_professor_profile:
            add_requirement(
                checks,
                "fy2024_activity_matched_facility_share",
                key,
                contains_context_number(
                    text,
                    r"positive[- ]throughput|active facilit",
                    fleet["active_positive_output_facility_share_pct"],
                    (1,),
                )
                and contains_context_number(
                    text,
                    r"positive[- ]throughput|active facilit|operating",
                    fleet["positive_throughput_facilities"],
                ),
                (
                    "Report the activity-matched FY2024 facility comparison: "
                    f"{fleet['active_positive_output_facility_share_pct']:.1f}% of "
                    f"{fleet['positive_throughput_facilities']} positive-throughput facilities."
                ),
            )
        add_requirement(
            checks,
            "firth_method_and_frames",
            key,
            re.search(r"Firth|Jeffreys[- ]prior", text, re.IGNORECASE) is not None
            and all(
                contains_number(text, value)
                for value in (
                    adoption["broad_rows"],
                    adoption["broad_sites"],
                    adoption["broad_events"],
                    adoption["prior_rows"],
                    adoption["prior_sites"],
                    adoption["prior_events"],
                    adoption["continuity_rows"],
                    adoption["continuity_sites"],
                    adoption["continuity_events"],
                    adoption["identity_certain_rows"],
                    adoption["identity_certain_sites"],
                    adoption["identity_certain_events"],
                    revision["bootstrap_repetitions"],
                )
            ),
            (
                "Name Firth/Jeffreys-prior bias reduction and report broad frame "
                f"{adoption['broad_rows']:,}/{adoption['broad_sites']:,}/{adoption['broad_events']} "
                "plus prior-operation frame "
                f"{adoption['prior_rows']:,}/{adoption['prior_sites']:,}/{adoption['prior_events']} "
                "and same-episode sensitivity "
                f"{adoption['continuity_rows']:,}/{adoption['continuity_sites']:,}/"
                f"{adoption['continuity_events']}; identity-certain sensitivity "
                f"{adoption['identity_certain_rows']:,}/"
                f"{adoption['identity_certain_sites']:,}/"
                f"{adoption['identity_certain_events']}, with "
                f"{revision['bootstrap_repetitions']} "
                "lineage bootstraps for the reduced model."
            ),
        )
        add_requirement(
            checks,
            "revised_entry_scale_and_influence",
            key,
            contains_context_number(
                text,
                r"300.{0,30}100|100.{0,30}300|odds ratio|scale select",
                revision["scale_or"],
                (2,),
            )
            and contains_context_number(
                text,
                r"confidence interval|CI|bootstrap",
                revision["scale_or_ci_low"],
                (2,),
            )
            and contains_number(text, revision["influence_or_low"], (2,))
            and contains_number(text, revision["influence_or_high"], (2,))
            and contains_context_number(
                text, r"continuity[- ]lineage", revision["continuity_events"]
            )
            and contains_context_number(
                text, r"rebuild|replacement", revision["rebuild_events"]
            ),
            (
                f"Report reduced-model scale OR={revision['scale_or']:.2f} "
                f"(CI {revision['scale_or_ci_low']:.2f}-"
                f"{revision['scale_or_ci_high']:.2f}), event-attack range "
                f"{revision['influence_or_low']:.2f}-"
                f"{revision['influence_or_high']:.2f}, and exact-event composition."
            ),
        )
        if is_professor_profile:
            add_requirement(
                checks,
                "revised_entry_extended_robustness",
                key,
                contains_number(text, revision["functional_form_or_low"], (2,))
                and contains_number(text, revision["functional_form_or_high"], (2,))
                and contains_number(text, revision["geographic_or_low"], (2,))
                and contains_number(text, revision["geographic_or_high"], (2,))
                and contains_number(text, revision["event_prefectures"])
                and contains_context_number(
                    text,
                    r"two.{0,30}prior|two-year|reporting-state|reporting state",
                    revision["strict_state_events"],
                )
                and contains_number(text, revision["strict_state_or"], (2,)),
                (
                    "Report alternative-form and leave-one-prefecture OR ranges plus "
                    f"the {revision['strict_state_events']}-event two-prior-year "
                    "reporting-state sensitivity."
                ),
            )
            add_requirement(
                checks,
                "entry_state_semantic_boundary",
                key,
                contains_number(text, revision["ambiguous_capacity_output_rows"])
                and contains_number(text, revision["ambiguous_capacity_output_lineages"])
                and re.search(
                    r"no reported positive capacity|not (?:verified|proven) (?:physical )?absence|blank.{0,100}(?:absence|capacity)",
                    text,
                    re.IGNORECASE | re.DOTALL,
                )
                is not None,
                (
                    "Disclose blank/zero-capacity positive-output exceptions and avoid "
                    "equating a blank field with verified physical absence."
                ),
            )
        quartiles = adoption["capacity_quartile_counts"]
        add_requirement(
            checks,
            "adoption_capacity_quartile_counts",
            key,
            contains_context_number(
                text,
                r"smallest.{0,50}(?:quartile|processing)|Q1",
                quartiles["Q1 smallest"]["risk_rows"],
            )
            and contains_context_number(
                text,
                r"second quartile|Q2",
                quartiles["Q2"]["risk_rows"],
            )
            and contains_context_number(
                text,
                r"third(?: quartile)?|Q3",
                quartiles["Q3"]["risk_rows"],
                window=80,
            )
            and contains_context_number(
                text,
                r"largest(?: quartile)?|Q4",
                quartiles["Q4 largest"]["risk_rows"],
                window=80,
            ),
            (
                "Report exact capacity-quartile risk rows: "
                f"{quartiles['Q1 smallest']['risk_rows']:,}, "
                f"{quartiles['Q2']['risk_rows']:,}, "
                f"{quartiles['Q3']['risk_rows']:,}, and "
                f"{quartiles['Q4 largest']['risk_rows']:,}."
            ),
        )
        add_requirement(
            checks,
            "engineering_components",
            key,
            re.search(r"generator design intensity", text, re.IGNORECASE) is not None
            and re.search(r"electrical capacity factor", text, re.IGNORECASE) is not None
            and contains_context_number(text, r"engineering[- ]valid", components["rows"])
            and contains_context_number(
                text,
                r"stable.{0,30}(?:sites?|lineages?)",
                components["stable_sites"],
            ),
            (
                "Separate generator design intensity from electrical capacity factor and "
                f"report {components['rows']:,} engineering-valid rows across "
                f"{components['stable_sites']} stable administrative lineages."
            ),
        )
        adjusted = revision["adjusted_components"]
        add_requirement(
            checks,
            "raw_installed_capacity_contrasts",
            key,
            contains_context_number(
                text,
                r"installed electrical capacity|installed[- ]kW",
                revision["installed_capacity_elasticity"],
                (3,),
            )
            and all(
                contains_number(text, abs(adjusted[label]), (1,))
                for label in (
                    "Installed electrical capacity::Before 1990",
                    "Installed electrical capacity::1990-1999",
                    "Installed electrical capacity::2000-2009",
                    "Electrical capacity factor::Before 1990",
                    "Electrical capacity factor::1990-1999",
                )
            ),
            (
                "Report the raw installed-kW elasticity and the adjusted installed-capacity "
                "and capacity-factor cohort contrasts."
            ),
        )
        if is_professor_profile:
            add_requirement(
                checks,
                "sizing_diagnostic_conclusion",
                key,
                re.search(r"sizing|generator design intensity", text, re.IGNORECASE)
                is not None
                and contains_number(text, components["sizing_age_coefficient"], (3, 4))
                and contains_number(text, components["sizing_age_p_value"], (3, 4))
                and contains_number(text, components["legacy_r_squared"], (3, 4))
                and contains_number(text, components["sizing_r_squared"], (3, 4)),
                (
                    "State that the sizing-adjusted age coefficient is "
                    f"{components['sizing_age_coefficient']:.4f} (p="
                    f"{components['sizing_age_p_value']:.4f}) and that R-squared changes "
                    f"from {components['legacy_r_squared']:.4f} to "
                    f"{components['sizing_r_squared']:.4f}."
                ),
            )
        else:
            add_requirement(
                checks,
                "sizing_diagnostic_public_boundary",
                key,
                contains_number(text, components["sizing_age_coefficient"], (3, 4))
                and contains_number(text, components["sizing_age_p_value"], (3, 4))
                and re.search(
                    r"algebra|mechanical|accounting identity",
                    text,
                    re.IGNORECASE,
                )
                is not None,
                (
                    "Report the sizing-adjusted age result and disclose that shared "
                    "component quantities are algebraically or mechanically coupled."
                ),
            )
        t1 = adoption["event_time_one"]
        all_t1 = t1["all"]
        continuity_t1 = t1["Continuity-lineage entry"]
        rebuild_t1 = t1["Rebuild/replacement-like entry"]
        if is_professor_profile:
            add_requirement(
                checks,
                "post_entry_pathway_results",
                key,
                contains_number(text, int(all_t1["events"]))
                and contains_number(text, all_t1["mean_gross_rank_pct"] * 100, (1,))
                and contains_number(text, int(continuity_t1["events"]))
                and contains_number(
                    text, continuity_t1["mean_design_rank_pct"] * 100, (1,)
                )
                and contains_number(text, int(rebuild_t1["events"]))
                and contains_number(
                    text, rebuild_t1["mean_design_rank_pct"] * 100, (1,)
                ),
                (
                    "Report event-time-one pathway counts and ranks from the generated "
                    "trajectory table."
                ),
            )
        else:
            add_requirement(
                checks,
                "post_entry_pathway_public_placement",
                key,
                re.search(
                    r"pathway.{0,120}supplement|supplement.{0,120}pathway",
                    text,
                    re.IGNORECASE | re.DOTALL,
                )
                is not None,
                "State that the exploratory pathway comparison is supplemental.",
            )

    if "supplement" in texts:
        text = texts["supplement"]
        add_requirement(
            checks,
            "supplement_identity_audit",
            "supplement",
            all(
                contains_number(text, value)
                for value in (
                    identity["stable_sites"],
                    identity["asset_episodes"],
                    identity["fy2020_official_code_overlap"],
                    identity["fy2020_stable_site_overlap"],
                )
            )
            and re.search(
                r"duplicate stable[- ](?:site|lineage)[- ]years?",
                text,
                re.IGNORECASE,
            )
            is not None,
            (
                "Document identity audit counts, including official/stable FY2019-FY2020 "
                f"overlaps {identity['fy2020_official_code_overlap']}/"
                f"{identity['fy2020_stable_site_overlap']:,} and duplicate lineage-years."
            ),
        )
        add_requirement(
            checks,
            "supplement_raw_provenance",
            "supplement",
            re.search(r"SHA-?256", text, re.IGNORECASE) is not None
            and re.search(
                r"retrieval (?:time|timestamp).{0,80}unavailable",
                text,
                re.IGNORECASE | re.DOTALL,
            )
            is not None
            and re.search(r"schema|header mapping", text, re.IGNORECASE) is not None,
            (
                "Reference SHA-256 raw-file provenance, explicitly unavailable retrieval "
                "timestamps, and workbook schema/header mappings."
            ),
        )
        add_requirement(
            checks,
            "supplement_firth_inference",
            "supplement",
            re.search(r"Firth|Jeffreys[- ]prior", text, re.IGNORECASE) is not None
            and contains_context_number(
                text, r"bootstrap", revision["bootstrap_repetitions"]
            )
            and contains_number(text, revision["scale_or"], (2,))
            and contains_number(text, revision["broad_age_coefficient"], (3, 4))
            and contains_number(text, revision["influence_or_low"], (2,)),
            (
                f"Document the five-parameter Firth model, "
                f"{revision['bootstrap_repetitions']} cluster bootstraps, scale OR "
                f"{revision['scale_or']:.2f}, continuous age, and event influence."
            ),
        )
        add_requirement(
            checks,
            "supplement_component_diagnostic",
            "supplement",
            re.search(r"generator design intensity", text, re.IGNORECASE) is not None
            and re.search(r"electrical capacity factor", text, re.IGNORECASE) is not None
            and contains_number(text, components["sizing_age_p_value"], (3, 4)),
            "Document both engineering components and the non-significant sizing-adjusted age result.",
        )

    if "professor_lineage" in texts:
        text = texts["professor_lineage"]
        add_requirement(
            checks,
            "lineage_current_design",
            "professor_lineage",
            re.search(
                r"stable.{0,30}(?:site|lineage)",
                text,
                re.IGNORECASE | re.DOTALL,
            )
            is not None
            and re.search(r"Firth|Jeffreys[- ]prior", text, re.IGNORECASE) is not None
            and re.search(r"generator design intensity", text, re.IGNORECASE) is not None
            and re.search(r"electrical capacity factor", text, re.IGNORECASE) is not None,
            "Explain the current administrative-lineage, Firth, design-intensity, and capacity-factor design.",
        )
        add_requirement(
            checks,
            "lineage_current_headlines",
            "professor_lineage",
            contains_number(text, fleet["facility_participation_pct"], (1,))
            and contains_number(text, fleet["throughput_coverage_pct"], (1,))
            and contains_number(text, revision["scale_or"], (2,))
            and contains_number(text, revision["scale_or_ci_low"], (2,))
            and contains_number(text, revision["influence_or_low"], (2,))
            and contains_number(text, revision["broad_age_coefficient"], (3, 4))
            and contains_number(text, revision["installed_capacity_elasticity"], (3,))
            and contains_number(text, components["sizing_age_p_value"], (3, 4)),
            (
                "Report current count-volume, reduced-model entry, event-influence, raw-component, "
                "and sizing-diagnostic headline values in the professor lineage packet."
            ),
        )

    stale_patterns = [
        (
            "panel_exit_claim",
            r"panel[- ]exit|exit[- ]hazard|exit diagnostic|last observed before FY?2024",
            "Panel-exit evidence is invalid after the official-code regime break and must not remain.",
        ),
        (
            "active_conversion_frame",
            r"active[- ]conversion|active operating conversion",
            "The old active-conversion frame is replaced by the prior-operation sensitivity.",
        ),
        (
            "coded_longitudinal_frame",
            r"coded[- ]asset|coded[- ]panel|coded[- ]generator|coded facilities",
            "Officially coded rows must not be framed as stable longitudinal units.",
        ),
        (
            "stale_exact_event_count",
            r"(?:10,823|10823).{0,100}(?:98 events?|1,911)|(?:98 events?).{0,100}(?:10,823|10823)",
            "The superseded exact-code hazard sample must be removed.",
        ),
        (
            "stale_active_sample",
            r"(?:9,215|9215).{0,100}(?:58 events?|1,663)|(?:1,663).{0,100}(?:9,215|9215)",
            "The superseded active-conversion sample must be removed.",
        ),
        (
            "threshold_dependent_same_episode_claim",
            r"near but above (?:the conventional )?0\.05",
            "The sparse same-episode result must be described as continuity-sensitive, not classified by a fragile threshold.",
        ),
        (
            "unsupported_predeclared_language",
            r"\bpredeclared\b",
            "Analysis bounds and sensitivities were specified but not preregistered as predeclared choices.",
        ),
        (
            "overstated_design_vintage_claim",
            r"evidence establishes.{0,120}design[- ]vintage hierarchy",
            "Reported start-year cohorts cannot establish a verified physical design-vintage hierarchy.",
        ),
    ]

    for key, text in texts.items():
        path = DOCUMENTS[key]
        for pattern_id, pattern, reason in stale_patterns:
            matches = list(re.finditer(pattern, text, flags=re.IGNORECASE | re.DOTALL))
            if not matches:
                checks.append(
                    {
                        "type": "stale_phrase",
                        "id": pattern_id,
                        "document": key,
                        "path": path,
                        "passed": True,
                        "detail": reason,
                    }
                )
                continue
            locations = sorted({text.count("\n", 0, match.start()) + 1 for match in matches})
            checks.append(
                {
                    "type": "stale_phrase",
                    "id": pattern_id,
                    "document": key,
                    "path": path,
                    "passed": False,
                    "detail": f"{reason} Matches at lines {locations[:12]}",
                }
            )

        high_risk_patterns = [
            (
                "official_code_as_stable_id",
                r"(?:official )?(?:facility )?codes?.{0,100}(?:stable|track|identify|link).{0,80}(?:sites?|facilities|longitudinal)|group(?:ed|ing).{0,40}facility_code",
                r"not|cannot|do not|unstable|break|reconstruct|rather than",
                "Official facility codes cannot be asserted as stable longitudinal IDs.",
            ),
            (
                "causal_regression_interpretation",
                r"\b(?:age|capacity|utili[sz]ation|sizing)\b.{0,80}\b(?:causes?|caused|causal effect|leads? to)\b|\b(?:causes?|caused|causal effect)\b.{0,80}\b(?:age|capacity|utili[sz]ation|sizing)\b",
                r"does not|do not|did not|cannot|not a causal|no causal|without causal",
                "Observational regression terms must not be presented as causal effects.",
            ),
        ]
        for pattern_id, pattern, exemption, reason in high_risk_patterns:
            flagged: list[int] = []
            for match in re.finditer(pattern, text, flags=re.IGNORECASE | re.DOTALL):
                context = text[max(0, match.start() - 120) : min(len(text), match.end() + 120)]
                if re.search(exemption, context, flags=re.IGNORECASE | re.DOTALL):
                    continue
                flagged.append(text.count("\n", 0, match.start()) + 1)
            checks.append(
                {
                    "type": "high_risk_claim",
                    "id": pattern_id,
                    "document": key,
                    "path": path,
                    "passed": not flagged,
                    "detail": (
                        reason
                        if not flagged
                        else f"{reason} Matches at lines {sorted(set(flagged))[:12]}"
                    ),
                }
            )
    return checks


def split_results(
    evidence_assertions: list[dict[str, Any]],
    document_checks: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    checks = evidence_assertions + document_checks
    passes = [check for check in checks if check["passed"]]
    failures = [check for check in checks if not check["passed"]]
    return passes, failures


def relative(path: Path | None) -> str:
    if path is None:
        return "n/a"
    return path.relative_to(REPO_ROOT).as_posix()


def write_report(
    metrics: dict[str, Any],
    passes: list[dict[str, Any]],
    failures: list[dict[str, Any]],
) -> None:
    identity = metrics["identity"]
    fleet = metrics["fleet"]
    adoption = metrics["adoption"]
    components = metrics["components"]
    revision = metrics["revision"]
    lines = [
        "# Claim Verification Report",
        "",
        "This report verifies generated evidence first, then checks the manuscript, LaTeX, "
        "supplement, and professor lineage against the resulting canonical metrics.",
        "",
        f"## Result: {'PASS' if not failures else 'FAIL'}",
        "",
        f"- Passed checks: {len(passes)}",
        f"- Failed checks: {len(failures)}",
        "",
        "## Canonical Evidence",
        "",
        f"- Identity: {identity['retained_rows']:,} retained rows from "
        f"{identity['raw_source_rows']:,} raw rows, {identity['stable_sites']:,} stable administrative lineages, "
        f"{identity['asset_episodes']:,} asset episodes, {identity['duplicate_site_year_rows']} duplicate lineage-years.",
        f"- FY2019-FY2020 continuity: {identity['fy2020_official_code_overlap']} official-code overlap "
        f"versus {identity['fy2020_stable_site_overlap']:,} administrative-lineage overlap.",
        f"- FY2009-FY2013 bridge: {identity['fy2009_fy2013_official_code_overlap']} official-code overlap "
        f"versus {identity['fy2009_fy2013_stable_site_overlap']:,} administrative-lineage overlap.",
        f"- FY2024 fleet: {fleet['facility_participation_pct']:.1f}% facility participation, "
        f"{fleet['active_positive_output_facility_share_pct']:.1f}% positive-output share "
        f"among {fleet['positive_throughput_facilities']} positive-throughput facilities, "
        f"{fleet['throughput_coverage_pct']:.1f}% throughput coverage, "
        f"{fleet['installed_design_capacity_share_pct']:.1f}% installed design-capacity share.",
        f"- Firth entry frames: {adoption['broad_rows']:,}/{adoption['broad_sites']:,}/"
        f"{adoption['broad_events']} broad and {adoption['prior_rows']:,}/"
        f"{adoption['prior_sites']:,}/{adoption['prior_events']} prior-operation and "
        f"{adoption['continuity_rows']:,}/{adoption['continuity_sites']:,}/"
        f"{adoption['continuity_events']} same-episode and "
        f"{adoption['identity_certain_rows']:,}/{adoption['identity_certain_sites']:,}/"
        f"{adoption['identity_certain_events']} identity-certain rows/lineages/events.",
        "- Entry capacity-quartile risk rows: "
        + "/".join(
            f"{adoption['capacity_quartile_counts'][label]['risk_rows']:,}"
            for label in ("Q1 smallest", "Q2", "Q3", "Q4 largest")
        )
        + ".",
        f"- Primary entry inference: frozen five-parameter OR {revision['scale_or']:.2f} "
        f"(95% lineage-bootstrap interval {revision['scale_or_ci_low']:.2f}-"
        f"{revision['scale_or_ci_high']:.2f}) for 300 versus 100 t/day; event attacks "
        f"retain {revision['influence_or_low']:.2f}-{revision['influence_or_high']:.2f}.",
        f"- Extended entry diagnostics: alternative-form ORs "
        f"{revision['functional_form_or_low']:.2f}-{revision['functional_form_or_high']:.2f}; "
        f"leave-one-prefecture ORs {revision['geographic_or_low']:.2f}-"
        f"{revision['geographic_or_high']:.2f}; strict reporting-state OR "
        f"{revision['strict_state_or']:.2f} on {revision['strict_state_events']} events.",
        f"- Components: {components['rows']:,} rows across {components['stable_sites']} stable administrative lineages; "
        f"sizing-adjusted age {components['sizing_age_coefficient']:.4f} "
        f"(p={components['sizing_age_p_value']:.4f}); R-squared "
        f"{components['legacy_r_squared']:.4f} to {components['sizing_r_squared']:.4f}.",
        "",
        "## Failures",
        "",
    ]
    if not failures:
        lines.append("- None")
    else:
        for failure in failures:
            path = relative(failure.get("path"))
            lines.append(
                f"- `{failure['type']}::{failure['id']}` [{path}]: {failure['detail']}"
            )
    lines.extend(["", "## Passed Checks", ""])
    for item in passes:
        path = relative(item.get("path"))
        lines.append(f"- `{item['type']}::{item['id']}` [{path}]: {item['detail']}")
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_claim_map(metrics: dict[str, Any]) -> None:
    identity = metrics["identity"]
    fleet = metrics["fleet"]
    adoption = metrics["adoption"]
    components = metrics["components"]
    revision = metrics["revision"]
    lines = [
        "# Claim-to-Evidence Map",
        "",
        "This map identifies the generated artifacts behind the paper's defensible claims. "
        "It does not elevate descriptive associations into causal effects.",
        "",
        "## Raw Sources And Longitudinal Identity",
        "",
        f"Claim: the panel contains {identity['stable_sites']:,} reconstructed stable administrative lineages and "
        f"{identity['asset_episodes']:,} asset episodes; official codes are not persistent across "
        "the FY2019-FY2020 regime break. Across FY2009-FY2013, "
        f"{identity['fy2009_fy2013_official_code_overlap']} official codes overlap while "
        f"{identity['fy2009_fy2013_stable_site_overlap']:,} administrative lineages are linked.",
        "",
        "Evidence: `output/raw_data_manifest.csv`, `output/raw_workbook_schema_map.csv`, "
        "`output/raw_data_provenance.md`, `data/processed/facility_identity_crosswalk.csv`, "
        "`output/facility_identity_audit.md`, and `output/identity_low_margin_links.csv`.",
        "",
        "## FY2024 Count-Volume Contrast",
        "",
        f"Claim: installed-generation facilities are {fleet['facility_participation_pct']:.1f}% "
        f"of recorded facilities and {fleet['active_positive_output_facility_share_pct']:.1f}% "
        f"of the {fleet['positive_throughput_facilities']} positive-throughput facilities, "
        "while positive-output facilities handle "
        f"{fleet['throughput_coverage_pct']:.1f}% of recorded throughput; installed-generation "
        f"facilities hold {fleet['installed_design_capacity_share_pct']:.1f}% of waste-processing "
        "design capacity.",
        "",
        "Evidence: `output/fleet_decomposition.csv`, `output/fy2024_fleet_segments.csv`, "
        "and `output/fleet_decomposition.md`.",
        "",
        "## First Reported Installed-Generation Capacity",
        "",
        f"Claim: Firth bias-reduced hazards use {adoption['broad_events']} exact-year events in "
        f"the broad frame, {adoption['prior_events']} following positive prior-lineage "
        f"operation, and {adoption['continuity_events']} in the same-episode sensitivity. "
        f"The identity-certain sensitivity retains {adoption['identity_certain_events']} "
        "events after excluding every lineage containing an accepted uncertain link. "
        f"The frozen five-parameter primary 300-versus-100 t/day OR is "
        f"{revision['scale_or']:.2f} (95% lineage-bootstrap interval "
        f"{revision['scale_or_ci_low']:.2f}-{revision['scale_or_ci_high']:.2f}). "
        f"Event attacks retain {revision['influence_or_low']:.2f}-"
        f"{revision['influence_or_high']:.2f}; alternative capacity transforms retain "
        f"{revision['functional_form_or_low']:.2f}-{revision['functional_form_or_high']:.2f}; "
        f"and leave-one-event-prefecture fits retain {revision['geographic_or_low']:.2f}-"
        f"{revision['geographic_or_high']:.2f}. The nested frames and diagnostics are "
        "not interpreted as independent equivalence tests.",
        "",
        "Evidence: `output/revised_entry_results.csv`, "
        "`output/revised_entry_bootstrap.csv`, `output/revised_entry_influence.csv`, "
        "`output/revised_entry_robustness.csv`, `output/entry_state_audit.csv`, and "
        "`output/scientific_revision_results.md`. The earlier eleven-parameter estimates "
        "remain labeled sensitivity evidence in `output/adoption_results.md`.",
        "",
        "## Generator Design And Annual Operation",
        "",
        f"Claim: the primary generator analysis separates generator design intensity from "
        f"electrical capacity factor on {components['rows']:,} engineering-valid rows across "
        f"{components['stable_sites']} stable administrative lineages. After generator "
        f"sizing is added, the age coefficient is {components['sizing_age_coefficient']:.4f} "
        f"(p={components['sizing_age_p_value']:.4f}); model R-squared changes from "
        f"{components['legacy_r_squared']:.4f} to {components['sizing_r_squared']:.4f}.",
        "",
        "Evidence: `output/generator_component_results.csv`, "
        "`output/table2_generator_components_by_cohort.md`, `output/figure3_persistence.csv`, "
        "and `output/regression_results.md`.",
        "",
        "## Prohibited Interpretations",
        "",
        "- Do not infer closure or exit from disappearance of an official facility code.",
        "- Do not treat the prior-operation sensitivity as a separately identified active-conversion process.",
        "- Do not interpret a blank installed-capacity field as verified physical absence.",
        "- Do not label gross MWh/t as net efficiency, useful heat, R1 efficiency, or lifecycle benefit.",
        "- Do not present age or waste-processing utilization as independent gross-performance effects after generator sizing.",
    ]
    CLAIM_MAP_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    metrics, evidence_assertions = build_metrics()
    document_checks = build_document_checks(metrics)
    passes, failures = split_results(evidence_assertions, document_checks)
    write_report(metrics, passes, failures)
    write_claim_map(metrics)

    manifest_inputs = [
        "output/raw_data_manifest.csv",
        "output/raw_workbook_schema_map.csv",
        "output/raw_data_provenance.md",
        "data/processed/incineration_panel_identified.csv",
        "data/processed/facility_identity_crosswalk.csv",
        "output/facility_identity_audit.md",
        "output/identity_low_margin_links.csv",
        "output/fleet_decomposition.csv",
        "output/fy2024_fleet_segments.csv",
        "output/figure2_transition_effects.csv",
        "output/adoption_bootstrap_coefficients.csv",
        "output/adoption_pathway_audit.csv",
        "output/revised_entry_results.csv",
        "output/revised_entry_bootstrap.csv",
        "output/revised_entry_influence.csv",
        "output/revised_entry_robustness.csv",
        "output/entry_state_audit.csv",
        "output/adoption_event_composition.csv",
        "output/post_adoption_bridge.csv",
        "output/post_adoption_trajectories.csv",
        "output/generator_component_results.csv",
        "output/regression_results.md",
        "output/robustness_component_results.csv",
        "output/data_quality_sample_flow.csv",
        "output/data_quality_engineering_bounds.csv",
        "output/data_quality_official_code_duplicates.csv",
        "output/identifier_overlap_by_year.csv",
        "output/identifier_gap_bridges.csv",
        "output/identifier_duplicates_by_year.csv",
    ]
    manifest_inputs.extend(
        f"output/manifests/{stage}.json" for stage in CORE_STAGES
    )
    manifest_inputs.extend(
        relative(path) for path in DOCUMENTS.values() if path.exists()
    )
    manifest_path = write_stage_manifest(
        "08_verify_claims",
        inputs=manifest_inputs,
        outputs=["output/claim_verification.md", "output/claim_evidence_map.md"],
        metadata={
            "passed_checks": len(passes),
            "failed_checks": len(failures),
            "failure_ids": [f"{item['type']}::{item['id']}" for item in failures],
            "source_manifest_python": metrics["python_versions"],
            "documents_checked": [
                relative(path) for path in DOCUMENTS.values() if path.exists()
            ],
        },
    )

    print(f"Claim verification report: {REPORT_PATH}")
    print(f"Claim-to-evidence map: {CLAIM_MAP_PATH}")
    print(f"Stage manifest: {manifest_path}")
    if failures:
        print("\nCLAIM VERIFICATION FAILED\n")
        for item in failures:
            path = relative(item.get("path"))
            print(f"- {item['type']}::{item['id']} [{path}]: {item['detail']}")
        raise SystemExit(1)
    print("\nCLAIM VERIFICATION PASSED")


if __name__ == "__main__":
    main()
