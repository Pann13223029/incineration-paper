"""
06b_identifier_gap_audit.py
===========================
Reviewer-facing audit of official-code gaps and lag continuity.

This stage exists because FY2010-FY2012 rows in the source panel lack official
facility codes. The paper's facility-level models require trackable identifiers,
so this audit makes the resulting exclusions and lag restrictions explicit.
"""

from __future__ import annotations

import os

import pandas as pd

from panel_utils import (
    OUTPUT_DIR,
    build_adoption_frame,
    build_adoption_model_frame,
    build_operating_power_frame,
    build_regression_frame,
    load_panel,
    write_stage_manifest,
)

os.makedirs(OUTPUT_DIR, exist_ok=True)


def code_coverage_table(panel: pd.DataFrame) -> pd.DataFrame:
    """Summarize official facility-code coverage by fiscal year."""
    frame = panel.copy()
    frame["official_code_present"] = frame["facility_code"].notna()
    return (
        frame.groupby("fiscal_year", as_index=False)
        .agg(
            rows=("facility_code", "size"),
            coded_rows=("official_code_present", "sum"),
        )
        .assign(
            missing_code_rows=lambda df: df["rows"] - df["coded_rows"],
            coded_share_pct=lambda df: df["coded_rows"] / df["rows"] * 100.0,
        )
    )


def adoption_lag_table(previous_observed_model: pd.DataFrame) -> pd.DataFrame:
    """Summarize lag gaps in the broader previous-observed-coded-row adoption frame."""
    return (
        previous_observed_model.groupby("lag_gap_years", as_index=False)
        .agg(
            rows=("adopt_power_this_year", "size"),
            events=("adopt_power_this_year", "sum"),
            facilities=("analysis_facility_id", "nunique"),
        )
        .sort_values("lag_gap_years")
    )


def generator_code_table(panel: pd.DataFrame) -> pd.DataFrame:
    """Summarize operating-generator code coverage by fiscal year."""
    operating = build_operating_power_frame(panel)
    operating["official_code_present"] = operating["analysis_facility_id"].notna()
    return (
        operating.groupby("fiscal_year", as_index=False)
        .agg(
            operating_rows=("analysis_facility_id", "size"),
            coded_operating_rows=("official_code_present", "sum"),
            mean_efficiency_mwh_t=("energy_efficiency_mwh_per_t", "mean"),
        )
        .assign(
            missing_code_rows=lambda df: df["operating_rows"] - df["coded_operating_rows"],
            missing_code_share_pct=lambda df: df["missing_code_rows"] / df["operating_rows"] * 100.0,
        )
    )


def write_report(
    path: str,
    coverage: pd.DataFrame,
    adoption_lags: pd.DataFrame,
    generator_codes: pd.DataFrame,
    exact_model: pd.DataFrame,
    previous_model: pd.DataFrame,
    regression: pd.DataFrame,
) -> dict[str, int | float]:
    """Write the markdown audit and return compact manifest metadata."""
    non_exact = previous_model[~previous_model["exact_one_year_lag"]]
    non_exact_events = int(non_exact["adopt_power_this_year"].sum())
    same_year_events = int(
        previous_model.loc[
            (previous_model["lag_gap_years"] == 0)
            & (previous_model["adopt_power_this_year"] == 1),
            "adopt_power_this_year",
        ].sum()
    )
    multi_year_events = int(
        previous_model.loc[
            (previous_model["lag_gap_years"] > 1)
            & (previous_model["adopt_power_this_year"] == 1),
            "adopt_power_this_year",
        ].sum()
    )
    missing_code_2010_2012 = int(
        coverage.loc[
            coverage["fiscal_year"].between(2010, 2012),
            "missing_code_rows",
        ].sum()
    )
    operating_missing_2010_2012 = int(
        generator_codes.loc[
            generator_codes["fiscal_year"].between(2010, 2012),
            "missing_code_rows",
        ].sum()
    )

    lines = [
        "# Identifier Gap And Lag-Continuity Audit",
        "",
        "This audit documents the official facility-code gap that affects facility-level tracking.",
        "It is designed to answer a reviewer concern directly: whether the adoption model uses true prior-year lags or merely the previous observed coded row.",
        "",
        "## Bottom Line",
        "",
        (
            f"- The source panel has {missing_code_2010_2012:,} rows without official facility codes in FY2010-FY2012."
        ),
        (
            f"- The broader previous-observed-coded-row adoption frame contains {len(previous_model):,} rows and "
            f"{int(previous_model['adopt_power_this_year'].sum()):,} events."
        ),
        (
            f"- The main exact-year adoption model keeps {len(exact_model):,} rows and "
            f"{int(exact_model['adopt_power_this_year'].sum()):,} events."
        ),
        (
            f"- Non-exact lag rows excluded from the main adoption model: {len(non_exact):,} rows "
            f"and {non_exact_events:,} events ({same_year_events:,} same-year duplicate-code events; "
            f"{multi_year_events:,} multi-year-gap events)."
        ),
        (
            f"- Operating-generator rows missing official codes in FY2010-FY2012: "
            f"{operating_missing_2010_2012:,}; these rows are excluded from the canonical regression frame."
        ),
        "",
        "Interpretation: the main adoption specification should be described as an exact one-fiscal-year lagged observed-transition model. The broader previous-observed-coded-row frame is useful as a sensitivity check but should not be used for the main prior-year claim.",
        "",
        "## Official Facility-Code Coverage By Fiscal Year",
        "",
        coverage.assign(
            coded_share_pct=lambda df: df["coded_share_pct"].map(lambda x: f"{x:.1f}")
        ).to_markdown(index=False),
        "",
        "## Adoption Lag Gaps In Previous-Observed-Coded-Row Frame",
        "",
        adoption_lags.assign(
            lag_gap_years=lambda df: df["lag_gap_years"].map(lambda x: int(x))
        ).to_markdown(index=False),
        "",
        "## Operating-Generator Code Coverage By Fiscal Year",
        "",
        generator_codes.assign(
            mean_efficiency_mwh_t=lambda df: df["mean_efficiency_mwh_t"].map(lambda x: f"{x:.3f}"),
            missing_code_share_pct=lambda df: df["missing_code_share_pct"].map(lambda x: f"{x:.1f}"),
        ).to_markdown(index=False),
        "",
        "## Implications For The Paper",
        "",
        "- Use exact one-fiscal-year lags as the main adoption model.",
        "- Treat previous-observed-coded-row adoption estimates as sensitivity evidence only.",
        "- Treat pathway-audit mechanism labels as strongest only for adjacent-year events.",
        "- Describe the generator regression frame as an identifiable coded-generator panel, not a complete census of all operating generator rows.",
        "- Avoid strong Fukushima-window identification language unless a proxy-ID sensitivity later restores FY2010-FY2012 continuity.",
        "",
    ]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return {
        "missing_code_rows_2010_2012": missing_code_2010_2012,
        "adoption_previous_observed_rows": int(len(previous_model)),
        "adoption_previous_observed_events": int(previous_model["adopt_power_this_year"].sum()),
        "adoption_exact_year_rows": int(len(exact_model)),
        "adoption_exact_year_events": int(exact_model["adopt_power_this_year"].sum()),
        "adoption_non_exact_rows_excluded": int(len(non_exact)),
        "adoption_non_exact_events_excluded": non_exact_events,
        "same_year_duplicate_code_events": same_year_events,
        "multi_year_gap_events": multi_year_events,
        "operating_generator_missing_code_rows_2010_2012": operating_missing_2010_2012,
        "regression_rows": int(len(regression)),
        "regression_facilities": int(regression["analysis_facility_id"].nunique()),
    }


def main() -> None:
    panel = load_panel()
    adoption = build_adoption_frame(panel)
    exact_model = build_adoption_model_frame(adoption=adoption)
    previous_model = build_adoption_model_frame(adoption=adoption, exact_year_only=False)
    regression = build_regression_frame(panel)

    coverage = code_coverage_table(panel)
    adoption_lags = adoption_lag_table(previous_model)
    generator_codes = generator_code_table(panel)

    output_path = os.path.join(OUTPUT_DIR, "identifier_gap_audit.md")
    metadata = write_report(
        output_path,
        coverage,
        adoption_lags,
        generator_codes,
        exact_model,
        previous_model,
        regression,
    )
    print(f"Saved: {output_path}")

    manifest_path = write_stage_manifest(
        "06b_identifier_gap_audit",
        inputs=["data/processed/incineration_panel_enriched.csv"],
        outputs=["output/identifier_gap_audit.md"],
        metadata=metadata,
    )
    print(f"Manifest: {manifest_path}")


if __name__ == "__main__":
    main()
