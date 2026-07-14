"""Build a blinded, stratified human-review packet for accepted identity links."""

from __future__ import annotations

import hashlib
import os

import numpy as np
import pandas as pd

from panel_utils import (
    OUTPUT_DIR,
    PROCESSED_DIR,
    build_adoption_frame,
    build_adoption_model_frame,
    load_panel,
    write_stage_manifest,
)


RANDOM_SEED = 20260714
TARGET_RANDOM_PER_STRATUM = 40


def match_family(method: pd.Series) -> pd.Series:
    values = method.fillna("")
    return pd.Series(
        np.select(
            [
                values.str.contains(r"code\+name_exact", regex=True),
                values.str.startswith("code+"),
                values.str.startswith("name_exact"),
                values.str.contains("name_fuzzy", regex=False),
            ],
            [
                "official_code_and_exact_name",
                "official_code_with_other_support",
                "exact_name_without_code",
                "fuzzy_name_without_code",
            ],
            default="other_accepted_link",
        ),
        index=method.index,
        dtype="string",
    )


def deterministic_sample(frame: pd.DataFrame, n: int, salt: str) -> pd.DataFrame:
    if len(frame) <= n:
        return frame.copy()
    keys = frame["source_record_id"].astype(str).map(
        lambda value: hashlib.sha256(f"{salt}|{value}".encode()).hexdigest()
    )
    return (
        frame.assign(_sample_key=keys)
        .sort_values("_sample_key")
        .head(n)
        .drop(columns="_sample_key")
    )


def build_packet() -> tuple[pd.DataFrame, pd.DataFrame, dict[str, int]]:
    crosswalk = pd.read_csv(
        os.path.join(PROCESSED_DIR, "facility_identity_crosswalk.csv"),
        dtype="string",
    )
    panel = load_panel()
    matched = crosswalk[~crosswalk["identity_match_method"].eq("new_site")].copy()
    matched["fiscal_year"] = pd.to_numeric(matched["fiscal_year"])
    matched["identity_predecessor_year"] = pd.to_numeric(
        matched["identity_predecessor_year"]
    )
    matched["lag_gap_years"] = (
        matched["fiscal_year"] - matched["identity_predecessor_year"]
    )
    matched["match_family"] = match_family(matched["identity_match_method"])
    matched["identity_match_uncertain"] = (
        matched["identity_match_uncertain"].str.lower().eq("true")
    )

    adoption = build_adoption_frame(panel)
    exact = build_adoption_model_frame(panel, adoption, exact_year_only=True)
    event_keys = set(
        zip(
            exact.loc[exact["adopt_power_this_year"].eq(1), "analysis_facility_id"].astype(str),
            exact.loc[exact["adopt_power_this_year"].eq(1), "fiscal_year"].astype(int),
        )
    )
    matched["modeled_event_link"] = [
        (str(site), int(year)) in event_keys
        for site, year in zip(matched["stable_site_id"], matched["fiscal_year"])
    ]
    matched["fuzzy_link"] = matched["identity_match_method"].str.contains(
        "name_fuzzy", regex=False, na=False
    )
    matched["gap_link"] = matched["lag_gap_years"].gt(1)
    matched["fy2019_2020_bridge"] = matched["identity_predecessor_year"].eq(
        2019
    ) & matched["fiscal_year"].eq(2020)

    required = matched[
        matched[
            [
                "modeled_event_link",
                "identity_match_uncertain",
                "fuzzy_link",
                "gap_link",
            ]
        ].any(axis=1)
    ].copy()
    samples = [required]
    for family in [
        "official_code_and_exact_name",
        "official_code_with_other_support",
        "exact_name_without_code",
        "fuzzy_name_without_code",
    ]:
        samples.append(
            deterministic_sample(
                matched[matched["match_family"].eq(family)],
                TARGET_RANDOM_PER_STRATUM,
                family,
            )
        )
    samples.append(
        deterministic_sample(
            matched[matched["fy2019_2020_bridge"]],
            TARGET_RANDOM_PER_STRATUM,
            "fy2019_2020_bridge",
        )
    )
    selected = (
        pd.concat(samples, ignore_index=True)
        .drop_duplicates("source_record_id")
        .sort_values(["fiscal_year", "prefecture", "facility_name"])
        .reset_index(drop=True)
    )
    selected.insert(
        0,
        "validation_pair_id",
        [f"LV{number:04d}" for number in range(1, len(selected) + 1)],
    )

    record_columns = [
        "source_record_id",
        "fiscal_year",
        "prefecture",
        "muni_code",
        "facility_code",
        "facility_name",
        "year_started",
        "capacity_t_day",
        "n_furnaces",
        "furnace_type",
        "operation_mode",
        "facility_type",
    ]
    records = panel[record_columns].copy()
    current = records.rename(
        columns={column: f"current_{column}" for column in record_columns}
    )
    prior = records.rename(
        columns={column: f"prior_{column}" for column in record_columns}
    )
    packet = selected.merge(
        current,
        left_on="source_record_id",
        right_on="current_source_record_id",
        how="left",
        validate="one_to_one",
    ).merge(
        prior,
        left_on="identity_predecessor_record_id",
        right_on="prior_source_record_id",
        how="left",
        validate="many_to_one",
    )
    if packet["current_source_record_id"].isna().any() or packet[
        "prior_source_record_id"
    ].isna().any():
        raise ValueError("Linkage-validation packet has unresolved record references")

    role_columns = [
        "modeled_event_link",
        "identity_match_uncertain",
        "fuzzy_link",
        "gap_link",
        "fy2019_2020_bridge",
    ]
    visible_columns = [
        "validation_pair_id",
        *role_columns,
        *[column for column in packet.columns if column.startswith("prior_")],
        *[column for column in packet.columns if column.startswith("current_")],
    ]
    visible = packet[visible_columns].copy()
    for column in [
        "reviewer_id",
        "review_decision",
        "review_confidence",
        "same_lineage_but_asset_reset",
        "evidence_url",
        "review_notes",
    ]:
        visible[column] = ""

    key_columns = [
        "validation_pair_id",
        "stable_site_id",
        "asset_episode_id",
        "identity_predecessor_record_id",
        "source_record_id",
        "match_family",
        "identity_match_method",
        "identity_match_score",
        "identity_match_current_row_margin",
        "identity_match_prior_record_margin",
        "identity_match_uncertain",
        "identity_match_uncertainty_reason",
        *role_columns,
    ]
    answer_key = selected[key_columns].copy()
    summary = {
        "packet_pairs": int(len(visible)),
        "modeled_event_links": int(visible["modeled_event_link"].sum()),
        "uncertain_links": int(visible["identity_match_uncertain"].sum()),
        "fuzzy_links": int(visible["fuzzy_link"].sum()),
        "gap_links": int(visible["gap_link"].sum()),
        "fy2019_2020_bridges": int(visible["fy2019_2020_bridge"].sum()),
    }
    return visible, answer_key, summary


def write_report(summary: dict[str, int]) -> str:
    path = os.path.join(OUTPUT_DIR, "linkage_validation_protocol.md")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("# Blinded Linkage-Validation Protocol\n\n")
        handle.write(
            "The review packet hides algorithmic scores, match methods, and final "
            "lineage labels. Reviewers compare the prior and current administrative "
            "records and classify each pair before opening the answer key.\n\n"
        )
        handle.write("## Packet Coverage\n\n")
        for key, value in summary.items():
            handle.write(f"- {key.replace('_', ' ').title()}: {value:,}\n")
        handle.write("\n## Allowed Decisions\n\n")
        handle.write(
            "- `same administrative facility history`\n"
            "- `different facility history`\n"
            "- `indeterminate from available evidence`\n"
            "- `same lineage but probable asset/configuration reset`\n\n"
        )
        handle.write(
            "A second reviewer should independently assess every modeled-event link, "
            "every uncertain link, and a blinded subset of the remaining packet. "
            "Disagreements require adjudication with an archived municipal or Ministry "
            "source. Completed decisions belong in a dated review copy, not in the "
            "generated packet.\n"
        )
    return path


def main() -> None:
    packet, answer_key, summary = build_packet()
    packet_path = os.path.join(OUTPUT_DIR, "linkage_validation_packet.csv")
    key_path = os.path.join(OUTPUT_DIR, "linkage_validation_key.csv")
    packet.to_csv(packet_path, index=False)
    answer_key.to_csv(key_path, index=False)
    report_path = write_report(summary)
    manifest_path = write_stage_manifest(
        "02c_build_linkage_validation_packet",
        inputs=[
            "data/processed/incineration_panel_identified.csv",
            "data/processed/facility_identity_crosswalk.csv",
        ],
        outputs=[
            "output/linkage_validation_packet.csv",
            "output/linkage_validation_key.csv",
            "output/linkage_validation_protocol.md",
        ],
        metadata=summary,
    )
    print(f"Linkage-validation packet: {len(packet):,} pairs")
    print(f"Saved: {report_path}")
    print(f"Manifest: {manifest_path}")


if __name__ == "__main__":
    main()
