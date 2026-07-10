"""Build stable longitudinal site and asset identities for the MOE panel."""

from __future__ import annotations

import os

import pandas as pd

from identity_utils import (
    MIN_AMBIGUOUS_MATCH_MARGIN,
    MIN_MATCH_SCORE,
    identity_audit_tables,
    resolve_stable_identities,
)
from panel_utils import PROCESSED_DIR, OUTPUT_DIR, write_stage_manifest


BASE_PATH = os.path.join(PROCESSED_DIR, "incineration_panel.csv")
IDENTIFIED_PATH = os.path.join(PROCESSED_DIR, "incineration_panel_identified.csv")
CROSSWALK_PATH = os.path.join(PROCESSED_DIR, "facility_identity_crosswalk.csv")
AUDIT_PATH = os.path.join(OUTPUT_DIR, "facility_identity_audit.md")
LOW_MARGIN_PATH = os.path.join(OUTPUT_DIR, "identity_low_margin_links.csv")


def _record_lookup(frame: pd.DataFrame) -> pd.DataFrame:
    columns = [
        "stable_site_id",
        "asset_episode_id",
        "identity_predecessor_record_id",
        "identity_match_score",
        "identity_match_current_row_margin",
        "identity_match_prior_record_margin",
        "identity_match_margin",
        "identity_match_uncertain",
        "identity_match_strong_evidence_override",
        "identity_match_current_alternative_record_id",
        "identity_match_prior_competitor_record_id",
    ]
    return frame.set_index("source_record_id")[columns].sort_index()


def build_low_margin_links(frame: pd.DataFrame) -> pd.DataFrame:
    """Build the canonical row-level audit of accepted ambiguous links."""
    low_margin = frame.loc[frame["identity_match_uncertain"]].copy()
    record_details = frame.set_index("source_record_id")
    detail_specs = [
        (
            "identity_predecessor_record_id",
            "predecessor_facility_code",
            "predecessor_facility_name",
        ),
        (
            "identity_match_current_alternative_record_id",
            "current_alternative_facility_code",
            "current_alternative_facility_name",
        ),
        (
            "identity_match_prior_competitor_record_id",
            "prior_competitor_facility_code",
            "prior_competitor_facility_name",
        ),
    ]
    for id_column, code_column, name_column in detail_specs:
        low_margin[code_column] = low_margin[id_column].map(
            record_details["facility_code"]
        )
        low_margin[name_column] = low_margin[id_column].map(
            record_details["facility_name"]
        )

    columns = [
        "source_record_id",
        "fiscal_year",
        "prefecture",
        "muni_code",
        "facility_code",
        "facility_name",
        "stable_site_id",
        "identity_predecessor_year",
        "identity_predecessor_record_id",
        "predecessor_facility_code",
        "predecessor_facility_name",
        "identity_match_score",
        "identity_match_current_row_margin",
        "identity_match_current_alternative_score",
        "identity_match_current_alternative_record_id",
        "current_alternative_facility_code",
        "current_alternative_facility_name",
        "identity_match_prior_record_margin",
        "identity_match_prior_competitor_score",
        "identity_match_prior_competitor_record_id",
        "prior_competitor_facility_code",
        "prior_competitor_facility_name",
        "identity_match_margin",
        "identity_match_uncertain",
        "identity_match_uncertainty_reason",
        "identity_match_strong_evidence_override",
        "identity_match_method",
    ]
    return low_margin[columns].sort_values(
        ["fiscal_year", "prefecture", "source_record_id"],
        kind="mergesort",
    ).reset_index(drop=True)


def _validate_low_margin_exposure(
    identified: pd.DataFrame,
    low_margin: pd.DataFrame,
) -> None:
    matched = ~identified["identity_match_method"].eq("new_site")
    if identified.loc[matched, "identity_match_score"].lt(MIN_MATCH_SCORE).any():
        raise ValueError("Identity guardrail found an accepted sub-threshold link")

    expected_uncertain = matched & identified["identity_match_margin"].lt(
        MIN_AMBIGUOUS_MATCH_MARGIN
    )
    if not expected_uncertain.equals(identified["identity_match_uncertain"]):
        raise ValueError("Identity guardrail found an inconsistent uncertainty flag")
    if (
        identified["identity_match_uncertain"]
        & ~identified["identity_match_strong_evidence_override"]
    ).any():
        raise ValueError("Identity guardrail found an accepted weak ambiguous link")

    expected_ids = set(
        identified.loc[expected_uncertain, "source_record_id"].astype(str)
    )
    exposed_ids = set(low_margin["source_record_id"].astype(str))
    if len(low_margin) != len(expected_ids) or exposed_ids != expected_ids:
        raise ValueError("Low-margin artifact does not expose every uncertain link once")
    if low_margin["source_record_id"].duplicated().any():
        raise ValueError("Low-margin artifact contains duplicate source records")
    if not low_margin["identity_match_strong_evidence_override"].all():
        raise ValueError("Low-margin artifact contains a link without strong evidence")


def _validate_low_margin_readback(expected: pd.DataFrame) -> None:
    persisted = pd.read_csv(
        LOW_MARGIN_PATH,
        dtype={"source_record_id": "string"},
        encoding="utf-8-sig",
    )
    if persisted.columns.tolist() != expected.columns.tolist():
        raise ValueError("Low-margin artifact schema changed during CSV serialization")
    if persisted["source_record_id"].tolist() != expected["source_record_id"].tolist():
        raise ValueError("Low-margin artifact order changed during CSV serialization")


def _one_record(
    frame: pd.DataFrame,
    *,
    year: int,
    name_fragment: str,
) -> pd.Series:
    matches = frame[
        frame["fiscal_year"].eq(year)
        & frame["facility_name"].fillna("").str.contains(name_fragment, regex=False)
    ]
    if len(matches) != 1:
        raise ValueError(
            f"Golden-link lookup expected one FY{year} row containing "
            f"{name_fragment!r}; found {len(matches)}"
        )
    return matches.iloc[0]


def run_identity_guardrails(
    source: pd.DataFrame,
    identified: pd.DataFrame,
    low_margin: pd.DataFrame,
) -> dict[str, int]:
    """Fail on known bad links and non-deterministic resolver behavior."""
    _validate_low_margin_exposure(identified, low_margin)
    yokote_2019 = _one_record(identified, year=2019, name_fragment="クリーンプラザよこて")
    yokote_2020 = _one_record(identified, year=2020, name_fragment="クリーンプラザよこて")
    port_2019 = _one_record(identified, year=2019, name_fragment="港島クリーンセンター")
    port_2020 = _one_record(identified, year=2020, name_fragment="港島クリーンセンター")
    hikari_2016 = _one_record(identified, year=2016, name_fragment="光が丘清掃工場")
    hikari_2017 = _one_record(identified, year=2017, name_fragment="光が丘清掃工場")
    setagaya_2017 = _one_record(identified, year=2017, name_fragment="世田谷清掃工場")
    chubo_2016 = _one_record(identified, year=2016, name_fragment="中防灰溶融施設")
    tenryu_2016 = _one_record(identified, year=2016, name_fragment="天竜ごみ処理工場")
    haruno_2016 = _one_record(identified, year=2016, name_fragment="はるのクリーンセンター")

    expected_same = [
        ("Yokote FY2019-FY2020", yokote_2019, yokote_2020),
        ("Port Island FY2019-FY2020", port_2019, port_2020),
        ("Hikarigaoka FY2016-FY2017", hikari_2016, hikari_2017),
    ]
    expected_different = [
        ("Hikarigaoka versus Setagaya", hikari_2016, setagaya_2017),
        ("Chubo versus Hikarigaoka", chubo_2016, hikari_2017),
        ("Tenryu versus Haruno", tenryu_2016, haruno_2016),
    ]
    for label, left, right in expected_same:
        if left["stable_site_id"] != right["stable_site_id"]:
            raise ValueError(f"Golden-link failure: {label} should share a stable ID")
    for label, left, right in expected_different:
        if left["stable_site_id"] == right["stable_site_id"]:
            raise ValueError(f"Golden-link failure: {label} must not share a stable ID")
    if hikari_2016["asset_episode_id"] == hikari_2017["asset_episode_id"]:
        raise ValueError("Golden-link failure: Hikarigaoka start-year reset needs a new episode")

    # Matching is prefecture-separable. Exercise the known difficult regimes plus
    # duplicate-bearing prefectures without tripling the full rebuild runtime.
    test_prefectures = ["秋田県", "兵庫県", "東京都", "静岡県", "徳島県", "宮城県"]
    test_source = source[source["prefecture"].isin(test_prefectures)].copy()
    test_baseline = identified[identified["prefecture"].isin(test_prefectures)].copy()
    shuffled = resolve_stable_identities(
        test_source.sample(frac=1.0, random_state=20260710)
    )
    if not _record_lookup(test_baseline).equals(_record_lookup(shuffled)):
        raise ValueError("Identity resolution is not invariant to source-row permutation")

    synthetic = test_source.iloc[[0]].copy()
    synthetic_index = synthetic.index[0]
    synthetic_name = "__isolated_identity_invariance_test__"
    synthetic.loc[synthetic_index, "prefecture"] = test_prefectures[0]
    synthetic.loc[synthetic_index, "muni_code"] = "99999"
    synthetic.loc[synthetic_index, "facility_code"] = "9999900001"
    synthetic.loc[synthetic_index, "facility_name"] = synthetic_name
    synthetic.loc[synthetic_index, "fiscal_year"] = int(
        source["fiscal_year"].min()
    )
    augmented = pd.concat([test_source, synthetic], ignore_index=True)
    augmented_result = resolve_stable_identities(augmented)
    augmented_original = augmented_result[
        ~augmented_result["facility_name"].eq(synthetic_name)
    ]
    if not _record_lookup(test_baseline).equals(_record_lookup(augmented_original)):
        raise ValueError(
            "Identity resolution changes after a same-prefecture unrelated insertion"
        )

    matched = ~identified["identity_match_method"].eq("new_site")

    return {
        "golden_same_link_checks": len(expected_same),
        "golden_separation_checks": len(expected_different),
        "permutation_invariance_prefectures": len(test_prefectures),
        "insertion_invariance_prefectures": len(test_prefectures),
        "two_sided_margin_rows_checked": int(matched.sum()),
        "accepted_subthreshold_links": 0,
        "accepted_weak_ambiguous_links": 0,
        "uncertain_links_exposed": len(low_margin),
    }


def main() -> None:
    panel = pd.read_csv(
        BASE_PATH,
        dtype={"facility_code": "string", "muni_code": "string"},
    )
    identified = resolve_stable_identities(panel)
    tables = identity_audit_tables(identified)
    low_margin = build_low_margin_links(identified)
    guardrails = run_identity_guardrails(panel, identified, low_margin)

    identified.to_csv(
        IDENTIFIED_PATH,
        index=False,
        encoding="utf-8-sig",
        float_format="%.15g",
    )
    crosswalk_columns = [
        "source_row_id",
        "source_record_id",
        "source_record_multiplicity",
        "fiscal_year",
        "prefecture",
        "muni_code",
        "facility_code",
        "facility_name",
        "year_started",
        "capacity_t_day",
        "stable_site_id",
        "asset_episode_id",
        "identity_match_method",
        "identity_match_score",
        "identity_match_current_row_margin",
        "identity_match_prior_record_margin",
        "identity_match_margin",
        "identity_match_uncertain",
        "identity_match_uncertainty_reason",
        "identity_match_strong_evidence_override",
        "identity_predecessor_year",
        "identity_predecessor_record_id",
        "identity_match_current_alternative_record_id",
        "identity_match_current_alternative_score",
        "identity_match_prior_competitor_record_id",
        "identity_match_prior_competitor_score",
        "asset_episode_reason",
    ]
    identified[crosswalk_columns].to_csv(
        CROSSWALK_PATH,
        index=False,
        encoding="utf-8-sig",
        float_format="%.15g",
    )
    low_margin.to_csv(
        LOW_MARGIN_PATH,
        index=False,
        encoding="utf-8-sig",
        float_format="%.15g",
    )
    _validate_low_margin_readback(low_margin)

    duplicate_site_years = int(
        identified.duplicated(["stable_site_id", "fiscal_year"], keep=False).sum()
    )
    max_years = int(identified.groupby("stable_site_id")["fiscal_year"].nunique().max())
    annual = tables["annual"]
    break_2020 = annual.loc[annual["fiscal_year"].eq(2020)].iloc[0]
    resolution_metadata = identified.attrs.get("identity_resolution_metadata", {})
    accepted_links = int(
        (~identified["identity_match_method"].eq("new_site")).sum()
    )
    uncertain_share_pct = (
        len(low_margin) / accepted_links * 100 if accepted_links else 0.0
    )

    with open(AUDIT_PATH, "w", encoding="utf-8") as handle:
        handle.write("# Facility Identity Audit\n\n")
        handle.write(
            "Stable administrative facility lineages are resolved by deterministic "
            "one-to-one matching. Adjacent fiscal years are matched before short gaps; "
            "official codes are supporting evidence rather than conclusive keys and are "
            "rejected when names and configuration evidence contradict them. Exact source "
            "duplicates are collapsed before matching. Sub-threshold and weak ambiguous "
            "edges are excluded before assignment, and unique unmatched dummy choices keep "
            "rejected edges from changing accepted links. Asset episodes split at symmetric "
            "reported start-year resets or major configuration resets.\n\n"
        )
        handle.write(f"- Raw source rows: {len(panel):,}\n")
        handle.write(f"- Unique retained source records: {len(identified):,}\n")
        handle.write(f"- Collapsed exact duplicate rows: {len(panel) - len(identified):,}\n")
        handle.write(f"- Stable administrative lineages: {identified['stable_site_id'].nunique():,}\n")
        handle.write(f"- Asset episodes: {identified['asset_episode_id'].nunique():,}\n")
        handle.write(f"- Duplicate stable-lineage-years: {duplicate_site_years:,}\n")
        handle.write(f"- Maximum observed fiscal years per lineage: {max_years}\n")
        handle.write(f"- Accepted uncertain links exposed: {len(low_margin):,}\n")
        handle.write(
            "- Accepted uncertain-link share: "
            f"{uncertain_share_pct:.3f}% of accepted links\n"
        )
        handle.write(
            "- Sub-threshold candidate edges excluded before assignment: "
            f"{int(resolution_metadata.get('subthreshold_candidate_edges_excluded', 0)):,}\n"
        )
        handle.write(
            "- Weak ambiguous candidate edges excluded before assignment: "
            f"{int(resolution_metadata.get('weak_ambiguous_candidate_edges_excluded', 0)):,}\n"
        )
        handle.write(
            "- FY2019-FY2020 official-code overlap: "
            f"{int(break_2020['official_code_overlap_prior_year']):,}\n"
        )
        handle.write(
            "- FY2019-FY2020 restored administrative-lineage overlap: "
            f"{int(break_2020['stable_site_overlap_prior_year']):,}\n\n"
        )
        handle.write("## Annual Continuity\n\n")
        handle.write(annual.to_markdown(index=False, floatfmt=".1f"))
        handle.write("\n\n## Match Families\n\n")
        handle.write(tables["methods"].to_markdown(index=False, floatfmt=".1f"))
        handle.write("\n\n## Collapsed Exact Source Duplicates\n\n")
        if tables["duplicate_records"].empty:
            handle.write("None.\n")
        else:
            handle.write(
                tables["duplicate_records"].to_markdown(index=False, floatfmt=".1f")
            )
        handle.write("\n\n## Accepted Two-Sided Low-Margin Links\n\n")
        handle.write(
            "These exact-name or official-code-supported links remain accepted even though "
            "the current-row alternative margin, prior-record competitor margin, or both "
            "are below 3 points. Every row is uncertainty-flagged for downstream "
            "sensitivity analysis and is canonically exposed in "
            "`output/identity_low_margin_links.csv`.\n\n"
        )
        if low_margin.empty:
            handle.write("None.\n")
        else:
            handle.write(
                low_margin[
                    [
                        "fiscal_year",
                        "prefecture",
                        "facility_code",
                        "facility_name",
                        "identity_match_score",
                        "identity_match_current_row_margin",
                        "identity_match_prior_record_margin",
                        "identity_match_margin",
                        "identity_match_uncertainty_reason",
                        "identity_match_strong_evidence_override",
                        "identity_match_method",
                    ]
                ].to_markdown(index=False, floatfmt=".2f")
            )
        handle.write("\n\n## Executable Guardrails\n\n")
        for label, value in guardrails.items():
            handle.write(f"- {label.replace('_', ' ').capitalize()}: {value}\n")
        handle.write(
            "\nThe audit is an administrative identity reconstruction, not proof of "
            "physical closure, ownership continuity, or unchanged equipment.\n"
        )

    if duplicate_site_years:
        raise ValueError("Identity audit found duplicate stable-lineage-years")
    if max_years > identified["fiscal_year"].nunique():
        raise ValueError("Identity audit found an impossible site history length")
    if int(break_2020["stable_site_overlap_prior_year"]) < 900:
        raise ValueError("FY2019-FY2020 administrative-lineage continuity remains implausibly low")

    manifest_path = write_stage_manifest(
        "02a_build_facility_identity",
        inputs=["data/processed/incineration_panel.csv"],
        outputs=[
            "data/processed/incineration_panel_identified.csv",
            "data/processed/facility_identity_crosswalk.csv",
            "output/facility_identity_audit.md",
            "output/identity_low_margin_links.csv",
        ],
        metadata={
            "raw_source_rows": int(len(panel)),
            "retained_unique_source_records": int(len(identified)),
            "collapsed_exact_duplicate_rows": int(len(panel) - len(identified)),
            "low_local_margin_global_assignments": int(len(low_margin)),
            "uncertain_identity_links": int(len(low_margin)),
            "uncertain_identity_link_share_pct": float(uncertain_share_pct),
            "strong_evidence_ambiguity_overrides": int(
                identified["identity_match_strong_evidence_override"].sum()
            ),
            "low_margin_audit_rows": int(len(low_margin)),
            "stable_sites": int(identified["stable_site_id"].nunique()),
            "asset_episodes": int(identified["asset_episode_id"].nunique()),
            "duplicate_site_year_rows": duplicate_site_years,
            "maximum_years_per_site": max_years,
            "fy2020_official_code_overlap": int(
                break_2020["official_code_overlap_prior_year"]
            ),
            "fy2020_stable_site_overlap": int(
                break_2020["stable_site_overlap_prior_year"]
            ),
            **resolution_metadata,
            **guardrails,
        },
    )
    print(f"Stable administrative lineages: {identified['stable_site_id'].nunique():,}")
    print(f"Asset episodes: {identified['asset_episode_id'].nunique():,}")
    print(f"Saved: {IDENTIFIED_PATH}")
    print(f"Saved: {CROSSWALK_PATH}")
    print(f"Saved: {AUDIT_PATH}")
    print(f"Saved: {LOW_MARGIN_PATH}")
    print(f"Manifest: {manifest_path}")


if __name__ == "__main__":
    main()
