"""Audit official-code discontinuities against audited administrative-lineage continuity."""

from __future__ import annotations

import os
from typing import Any

import pandas as pd

from panel_utils import OUTPUT_DIR, load_panel, write_stage_manifest


REPORT_PATH = os.path.join(OUTPUT_DIR, "identifier_gap_audit.md")
OVERLAP_PATH = os.path.join(OUTPUT_DIR, "identifier_overlap_by_year.csv")
BRIDGE_PATH = os.path.join(OUTPUT_DIR, "identifier_gap_bridges.csv")
DUPLICATE_PATH = os.path.join(OUTPUT_DIR, "identifier_duplicates_by_year.csv")


def normalize_official_code(series: pd.Series) -> pd.Series:
    """Normalize administrative codes for annual coverage comparisons."""
    return (
        series.astype("string")
        .str.strip()
        .str.replace(r"\.0$", "", regex=True)
        .replace({"": pd.NA, "nan": pd.NA, "None": pd.NA, "<NA>": pd.NA})
    )


def transition_record(
    previous: pd.DataFrame,
    current: pd.DataFrame,
    previous_year: int,
    current_year: int,
) -> dict[str, Any]:
    """Compare code-set overlap with row-linked administrative-lineage continuity."""
    previous_codes = set(previous["_official_code"].dropna().unique())
    current_codes = set(current["_official_code"].dropna().unique())
    previous_sites = set(previous["stable_site_id"].dropna().unique())
    current_sites = set(current["stable_site_id"].dropna().unique())
    shared_sites = previous_sites & current_sites

    left = previous[
        previous["stable_site_id"].isin(shared_sites)
    ][["stable_site_id", "_official_code"]].rename(
        columns={"_official_code": "previous_official_code"}
    )
    right = current[
        current["stable_site_id"].isin(shared_sites)
    ][["stable_site_id", "_official_code"]].rename(
        columns={"_official_code": "current_official_code"}
    )
    linked = left.merge(right, on="stable_site_id", how="inner", validate="one_to_one")
    both_codes = linked[
        linked["previous_official_code"].notna()
        & linked["current_official_code"].notna()
    ]
    same_code = both_codes["previous_official_code"].eq(
        both_codes["current_official_code"]
    )

    return {
        "previous_fiscal_year": previous_year,
        "fiscal_year": current_year,
        "previous_rows": int(len(previous)),
        "current_rows": int(len(current)),
        "previous_coded_rows": int(previous["_official_code"].notna().sum()),
        "current_coded_rows": int(current["_official_code"].notna().sum()),
        "previous_unique_official_codes": int(len(previous_codes)),
        "current_unique_official_codes": int(len(current_codes)),
        "official_code_set_overlap": int(len(previous_codes & current_codes)),
        "stable_site_overlap": int(len(shared_sites)),
        "linked_sites_same_official_code": int(same_code.sum()),
        "linked_sites_changed_official_code": int((~same_code).sum()),
        "linked_sites_missing_code_either_year": int(len(linked) - len(both_codes)),
        "official_code_overlap_pct_of_previous": (
            len(previous_codes & current_codes) / len(previous_codes) * 100.0
            if previous_codes
            else float("nan")
        ),
        "stable_site_overlap_pct_of_previous": (
            len(shared_sites) / len(previous_sites) * 100.0
            if previous_sites
            else float("nan")
        ),
    }


def annual_overlap_table(panel: pd.DataFrame) -> pd.DataFrame:
    """Return every exact-adjacent-year code and administrative-lineage overlap comparison."""
    years = sorted(int(year) for year in panel["fiscal_year"].unique())
    rows = []
    for previous_year, current_year in zip(years[:-1], years[1:]):
        if current_year - previous_year != 1:
            continue
        previous = panel[panel["fiscal_year"].eq(previous_year)]
        current = panel[panel["fiscal_year"].eq(current_year)]
        rows.append(
            transition_record(previous, current, previous_year, current_year)
        )
    return pd.DataFrame(rows)


def bridge_table(panel: pd.DataFrame) -> pd.DataFrame:
    """Report the multi-year code gap and the FY2019-FY2020 reset explicitly."""
    rows = []
    for previous_year, current_year, label in [
        (2009, 2013, "Bridge across FY2010-FY2012 official-code gap"),
        (2019, 2020, "FY2019-FY2020 official-code regime reset"),
    ]:
        previous = panel[panel["fiscal_year"].eq(previous_year)]
        current = panel[panel["fiscal_year"].eq(current_year)]
        record = transition_record(previous, current, previous_year, current_year)
        record = {"transition": label, **record}
        rows.append(record)
    return pd.DataFrame(rows)


def duplicate_table(panel: pd.DataFrame) -> pd.DataFrame:
    """Compare same-year official-code collisions with administrative-lineage grain checks."""
    rows = []
    for fiscal_year, frame in panel.groupby("fiscal_year", sort=True):
        coded = frame.dropna(subset=["_official_code"])
        official_sizes = coded.groupby("_official_code", sort=False).size()
        stable_sizes = frame.groupby("stable_site_id", sort=False).size()
        rows.append(
            {
                "fiscal_year": int(fiscal_year),
                "official_code_year_duplicate_groups": int(
                    (official_sizes > 1).sum()
                ),
                "rows_in_official_duplicate_groups": int(
                    official_sizes[official_sizes > 1].sum()
                ),
                "max_rows_per_official_code": int(official_sizes.max())
                if len(official_sizes)
                else 0,
                "stable_site_year_duplicate_groups": int((stable_sizes > 1).sum()),
                "rows_in_stable_site_duplicate_groups": int(
                    stable_sizes[stable_sizes > 1].sum()
                ),
                "max_rows_per_stable_site": int(stable_sizes.max())
                if len(stable_sizes)
                else 0,
            }
        )
    return pd.DataFrame(rows)


def write_report(
    panel: pd.DataFrame,
    annual: pd.DataFrame,
    bridges: pd.DataFrame,
    duplicates: pd.DataFrame,
) -> None:
    """Write the reviewer-facing identifier discontinuity audit."""
    gap = panel[panel["fiscal_year"].between(2010, 2012)]
    gap_coded = int(gap["_official_code"].notna().sum())
    missing_asset_episodes = int(panel["asset_episode_id"].isna().sum())
    reset = bridges[bridges["previous_fiscal_year"].eq(2019)].iloc[0]
    gap_bridge = bridges[bridges["previous_fiscal_year"].eq(2009)].iloc[0]

    annual_display = annual.copy()
    for column in [
        "official_code_overlap_pct_of_previous",
        "stable_site_overlap_pct_of_previous",
    ]:
        annual_display[column] = annual_display[column].map(
            lambda value: "NA" if pd.isna(value) else f"{value:.1f}"
        )
    with open(REPORT_PATH, "w", encoding="utf-8") as handle:
        handle.write("# Official-Code Gaps And Administrative-Lineage Continuity Audit\n\n")
        handle.write("## Bottom Line\n\n")
        handle.write(
            f"- FY2010-FY2012 contain {len(gap):,} rows and {gap_coded:,} non-missing "
            "official facility codes. Audited administrative-lineage IDs remain present for every row.\n"
            f"- Across FY2009-FY2013, exact official-code overlap is "
            f"{int(gap_bridge['official_code_set_overlap']):,}, while the audited identity "
            f"links {int(gap_bridge['stable_site_overlap']):,} administrative lineages.\n"
            f"- Across the FY2019-FY2020 code-regime reset, exact official-code overlap is "
            f"{int(reset['official_code_set_overlap']):,}, while administrative-lineage continuity "
            f"restores {int(reset['stable_site_overlap']):,} site links. Of those links, "
            f"{int(reset['linked_sites_changed_official_code']):,} have non-missing but "
            "changed official codes.\n"
            f"- Duplicate stable-lineage-year groups: "
            f"{int(duplicates['stable_site_year_duplicate_groups'].sum()):,}; missing "
            f"asset-episode IDs: {missing_asset_episodes:,}.\n\n"
        )
        handle.write(
            "Official codes are therefore treated as annual administrative fields, not "
            "as longitudinal facility keys. Adoption lags, pathway continuity, clustering, "
            "and repeated-lineage checks use the audited administrative-lineage identifier.\n\n"
        )
        handle.write("## Annual Adjacent-Year Overlap\n\n")
        handle.write(annual_display.to_markdown(index=False))
        handle.write("\n\n## Explicit Gap And Reset Bridges\n\n")
        handle.write(bridges.to_markdown(index=False, floatfmt=".2f"))
        handle.write("\n\n## Same-Year Duplicate Checks\n\n")
        handle.write(duplicates.to_markdown(index=False))
        handle.write("\n\n## Interpretation Guardrails\n\n")
        handle.write(
            "Administrative-lineage restoration is deterministic record linkage supported by names, "
            "municipality, reported start year, processing capacity, furnace count, and "
            "technology fields. It restores an auditable longitudinal grain but does not "
            "make every historical linkage certain. Asset-episode IDs remain separate so "
            "a rebuilt or replaced asset at the same site is not silently interpreted as "
            "unchanged equipment.\n"
        )


def main() -> None:
    panel = load_panel().copy()
    panel["_official_code"] = normalize_official_code(panel["facility_code"])

    missing_stable = int(panel["stable_site_id"].isna().sum())
    missing_asset_episodes = int(panel["asset_episode_id"].isna().sum())
    duplicate_stable_years = int(
        panel.duplicated(["stable_site_id", "fiscal_year"]).sum()
    )
    if missing_stable:
        raise ValueError(f"Administrative-lineage identity is incomplete: {missing_stable} rows")
    if missing_asset_episodes:
        raise ValueError(
            f"Asset-episode identity is incomplete: {missing_asset_episodes} rows"
        )
    if duplicate_stable_years:
        raise ValueError(
            f"Stable-lineage-year grain is not unique: {duplicate_stable_years} duplicates"
        )

    annual = annual_overlap_table(panel)
    bridges = bridge_table(panel)
    duplicates = duplicate_table(panel)
    reset = bridges[bridges["previous_fiscal_year"].eq(2019)].iloc[0]
    if int(reset["official_code_set_overlap"]) != 0:
        raise ValueError("FY2019-FY2020 no longer exhibits a complete official-code reset")
    if int(reset["stable_site_overlap"]) == 0:
        raise ValueError("Administrative-lineage identity failed to restore FY2019-FY2020 continuity")

    annual.to_csv(OVERLAP_PATH, index=False, float_format="%.10g")
    bridges.to_csv(BRIDGE_PATH, index=False, float_format="%.10g")
    duplicates.to_csv(DUPLICATE_PATH, index=False, float_format="%.10g")
    write_report(panel, annual, bridges, duplicates)

    gap = panel[panel["fiscal_year"].between(2010, 2012)]
    gap_bridge = bridges[bridges["previous_fiscal_year"].eq(2009)].iloc[0]
    manifest_path = write_stage_manifest(
        "06b_identifier_gap_audit",
        inputs=["data/processed/incineration_panel_identified.csv"],
        outputs=[
            "output/identifier_gap_audit.md",
            "output/identifier_overlap_by_year.csv",
            "output/identifier_gap_bridges.csv",
            "output/identifier_duplicates_by_year.csv",
        ],
        metadata={
            "missing_stable_site_ids": missing_stable,
            "missing_asset_episode_ids": missing_asset_episodes,
            "stable_site_year_duplicates": duplicate_stable_years,
            "fy2010_2012_rows": int(len(gap)),
            "fy2010_2012_coded_rows": int(gap["_official_code"].notna().sum()),
            "fy2009_2013_official_code_overlap": int(
                gap_bridge["official_code_set_overlap"]
            ),
            "fy2009_2013_stable_site_overlap": int(
                gap_bridge["stable_site_overlap"]
            ),
            "fy2019_2020_official_code_overlap": int(
                reset["official_code_set_overlap"]
            ),
            "fy2019_2020_stable_site_overlap": int(reset["stable_site_overlap"]),
            "fy2019_2020_changed_codes_on_linked_sites": int(
                reset["linked_sites_changed_official_code"]
            ),
            "official_code_year_duplicate_groups": int(
                duplicates["official_code_year_duplicate_groups"].sum()
            ),
            "annual_transition_rows": int(len(annual)),
        },
    )
    print(f"Saved: {REPORT_PATH}")
    print(f"Saved: {OVERLAP_PATH}")
    print(f"Saved: {BRIDGE_PATH}")
    print(f"Saved: {DUPLICATE_PATH}")
    print(f"Manifest: {manifest_path}")


if __name__ == "__main__":
    main()
