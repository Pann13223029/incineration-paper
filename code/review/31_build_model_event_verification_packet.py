#!/usr/bin/env python3
"""Build a blank external-source review packet for the 35 modeled events."""

from __future__ import annotations

import csv
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE = REPO_ROOT / "output" / "adoption_event_composition.csv"
DESTINATION = (
    REPO_ROOT
    / "paper"
    / "notes"
    / "review"
    / "model-event-external-verification-packet.csv"
)

SOURCE_FIELDS = [
    "analysis_facility_id",
    "fiscal_year",
    "prefecture",
    "facility_name",
    "lag_facility_age_years",
    "lag_capacity_t_day",
    "lag_throughput_t_year",
    "same_asset_episode_as_lag",
    "pathway_category",
    "pathway_basis",
    "calendar_era",
    "capacity_group",
]

REVIEW_FIELDS = [
    "reviewer_id",
    "verification_status",
    "verified_event_year",
    "source_title",
    "source_publisher",
    "source_url",
    "source_access_date",
    "archived_url",
    "evidence_locator",
    "review_notes",
]


def read_source() -> list[dict[str, str]]:
    if not SOURCE.exists():
        raise SystemExit(f"Modeled-event source not found: {SOURCE}")

    with SOURCE.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = set(SOURCE_FIELDS) - set(reader.fieldnames or [])
        if missing:
            raise SystemExit(f"Modeled-event source is missing fields: {sorted(missing)}")
        rows = list(reader)

    if len(rows) != 35:
        raise SystemExit(f"Expected 35 modeled events, found {len(rows)}")

    keys = {(row["analysis_facility_id"], row["fiscal_year"]) for row in rows}
    if len(keys) != len(rows):
        raise SystemExit("Modeled-event source contains duplicate facility-year keys")

    if any(row["pathway_category"] == "Forward-dated/placeholder entry" for row in rows):
        raise SystemExit("Modeled-event packet unexpectedly contains a placeholder event")

    return rows


def main() -> int:
    rows = read_source()
    DESTINATION.parent.mkdir(parents=True, exist_ok=True)

    with DESTINATION.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=SOURCE_FIELDS + REVIEW_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {**{field: row[field] for field in SOURCE_FIELDS}, **dict.fromkeys(REVIEW_FIELDS, "")}
            )

    print(f"External event-verification packet: {DESTINATION}")
    print(f"Blank modeled-event rows: {len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
