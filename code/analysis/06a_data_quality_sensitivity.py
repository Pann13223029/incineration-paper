"""Data-quality audit for administrative-lineage and engineering-component samples."""

from __future__ import annotations

import os
from typing import Any

import numpy as np
import pandas as pd

from panel_utils import (
    CAPACITY_FACTOR_CEIL,
    CAPACITY_FACTOR_FLOOR,
    CAPACITY_UTILIZATION_CAP,
    EFF_CEIL,
    EFF_FLOOR,
    HEATING_VALUE_CEIL_MJ_KG,
    HEATING_VALUE_FLOOR_MJ_KG,
    OUTPUT_DIR,
    build_adoption_frame,
    build_adoption_model_frame,
    build_full_fleet_frame,
    build_operating_power_frame,
    build_regression_frame,
    load_panel,
    write_stage_manifest,
)


REPORT_PATH = os.path.join(OUTPUT_DIR, "data_quality_sensitivity.md")
FLOW_PATH = os.path.join(OUTPUT_DIR, "data_quality_sample_flow.csv")
BOUNDS_PATH = os.path.join(OUTPUT_DIR, "data_quality_engineering_bounds.csv")
DUPLICATES_PATH = os.path.join(
    OUTPUT_DIR, "data_quality_official_code_duplicates.csv"
)


def normalize_official_code(series: pd.Series) -> pd.Series:
    """Normalize codes for same-year duplicate diagnostics only."""
    return (
        series.astype("string")
        .str.strip()
        .str.replace(r"\.0$", "", regex=True)
        .replace({"": pd.NA, "nan": pd.NA, "None": pd.NA, "<NA>": pd.NA})
    )


def sample_flow_table(
    panel: pd.DataFrame,
    fleet: pd.DataFrame,
    operating: pd.DataFrame,
    regression: pd.DataFrame,
    adoption: pd.DataFrame,
    adoption_model: pd.DataFrame,
) -> pd.DataFrame:
    """Build auditable row arithmetic for generator and entry samples."""
    flagged = panel[panel["has_power_gen"].fillna(False).astype(bool)].copy()
    positive_throughput = flagged[flagged["throughput_t_year"].gt(0)].copy()
    positive_output = positive_throughput[
        positive_throughput["power_generated_mwh"].gt(0)
    ].copy()
    valid = operating[operating["engineering_valid"]].copy()
    prior_operation = adoption_model[
        adoption_model["lag_throughput_t_year"].gt(0)
    ].copy()

    stages = [
        ("generator", "Administrative panel", panel),
        ("generator", "Audited administrative-lineage fleet", fleet),
        ("generator", "Installed generation reported", flagged),
        ("generator", "Positive annual throughput", positive_throughput),
        ("generator", "Positive gross electricity output", positive_output),
        ("generator", "Passes all engineering bounds", valid),
        ("generator", "Component-model complete cases", regression),
        ("entry", "Observed non-generator risk set", adoption),
        ("entry", "Exact-year lag and complete covariates", adoption_model),
        ("entry", "Exact-year lag after prior operation", prior_operation),
    ]
    rows: list[dict[str, Any]] = []
    previous_by_analysis: dict[str, int] = {}
    for analysis, stage, frame in stages:
        rows_count = int(len(frame))
        previous = previous_by_analysis.get(analysis)
        rows.append(
            {
                "analysis": analysis,
                "stage": stage,
                "rows": rows_count,
                "rows_removed_from_prior_stage": (
                    0 if previous is None else previous - rows_count
                ),
                "stable_sites": int(frame["analysis_facility_id"].nunique())
                if "analysis_facility_id" in frame.columns
                else int(frame["stable_site_id"].nunique()),
                "events": int(frame["adopt_power_this_year"].sum())
                if "adopt_power_this_year" in frame.columns
                else pd.NA,
            }
        )
        previous_by_analysis[analysis] = rows_count
    return pd.DataFrame(rows)


def bound_record(
    scope: str,
    metric: str,
    values: pd.Series,
    lower: float,
    upper: float,
) -> dict[str, Any]:
    """Summarize missing, below-bound, in-bound, and above-bound records."""
    numeric = pd.to_numeric(values, errors="coerce")
    return {
        "scope": scope,
        "metric": metric,
        "lower_bound": lower,
        "upper_bound": upper,
        "rows": int(len(numeric)),
        "missing": int(numeric.isna().sum()),
        "below_bound": int(numeric.lt(lower).sum()),
        "within_bounds": int(numeric.between(lower, upper).sum()),
        "above_bound": int(numeric.gt(upper).sum()),
    }


def engineering_bounds_table(
    operating: pd.DataFrame,
    regression: pd.DataFrame,
) -> pd.DataFrame:
    """Audit every predeclared component bound and heating-value plausibility."""
    definitions = [
        (
            "Gross generation intensity (MWh/t)",
            "energy_efficiency_raw_mwh_per_t",
            EFF_FLOOR,
            EFF_CEIL,
        ),
        (
            "Electrical capacity factor",
            "electrical_capacity_factor",
            CAPACITY_FACTOR_FLOOR,
            CAPACITY_FACTOR_CEIL,
        ),
        (
            "Waste-processing utilization",
            "capacity_utilization_raw",
            0.02,
            CAPACITY_UTILIZATION_CAP,
        ),
        (
            "Generator design intensity (kW per t/day)",
            "generator_design_intensity_kw_per_t_day",
            0.10,
            100.0,
        ),
        (
            "Heating value (MJ/kg; plausibility only)",
            "heating_value_mj_kg",
            HEATING_VALUE_FLOOR_MJ_KG,
            HEATING_VALUE_CEIL_MJ_KG,
        ),
    ]
    rows = []
    for scope, frame in [
        ("Operating generator rows", operating),
        ("Engineering-valid component rows", regression),
    ]:
        for label, column, lower, upper in definitions:
            rows.append(bound_record(scope, label, frame[column], lower, upper))
    return pd.DataFrame(rows)


def duplicate_code_table(panel: pd.DataFrame) -> pd.DataFrame:
    """Audit official-code duplicates within years without using codes as panel IDs."""
    frame = panel.assign(_official_code=normalize_official_code(panel["facility_code"]))
    rows = []
    for fiscal_year, year_frame in frame.groupby("fiscal_year", sort=True):
        coded = year_frame.dropna(subset=["_official_code"])
        sizes = coded.groupby("_official_code", sort=False).size()
        duplicate_codes = set(sizes[sizes > 1].index)
        duplicate_rows = coded[coded["_official_code"].isin(duplicate_codes)]
        rows.append(
            {
                "fiscal_year": int(fiscal_year),
                "rows": int(len(year_frame)),
                "coded_rows": int(len(coded)),
                "unique_official_codes": int(coded["_official_code"].nunique()),
                "duplicate_code_year_groups": int((sizes > 1).sum()),
                "rows_in_duplicate_code_year_groups": int(len(duplicate_rows)),
                "max_rows_per_official_code": int(sizes.max()) if len(sizes) else 0,
                "stable_sites_in_duplicate_groups": int(
                    duplicate_rows["stable_site_id"].nunique()
                ),
            }
        )
    return pd.DataFrame(rows)


def age_audit(
    panel: pd.DataFrame,
    fleet: pd.DataFrame,
    operating: pd.DataFrame,
    regression: pd.DataFrame,
) -> dict[str, int]:
    """Verify that negative reported ages become missing rather than zero."""
    raw_age = pd.to_numeric(panel["facility_age"], errors="coerce")
    return {
        "panel_missing_raw_age": int(raw_age.isna().sum()),
        "panel_negative_raw_age": int(raw_age.lt(0).sum()),
        "fleet_missing_analysis_age": int(fleet["facility_age_years"].isna().sum()),
        "fleet_negative_analysis_age": int(fleet["facility_age_years"].lt(0).sum()),
        "operating_missing_analysis_age": int(
            operating["facility_age_years"].isna().sum()
        ),
        "operating_negative_analysis_age": int(
            operating["facility_age_years"].lt(0).sum()
        ),
        "regression_missing_analysis_age": int(
            regression["facility_age_years"].isna().sum()
        ),
        "regression_negative_analysis_age": int(
            regression["facility_age_years"].lt(0).sum()
        ),
    }


def write_report(
    panel: pd.DataFrame,
    fleet: pd.DataFrame,
    operating: pd.DataFrame,
    regression: pd.DataFrame,
    flow: pd.DataFrame,
    bounds: pd.DataFrame,
    duplicates: pd.DataFrame,
    ages: dict[str, int],
    identity_uncertainty: dict[str, int],
) -> None:
    """Write a deterministic reviewer-facing data-quality report."""
    stable_duplicate_mask = panel.duplicated(
        ["stable_site_id", "fiscal_year"], keep=False
    )
    missing_asset_episodes = int(panel["asset_episode_id"].isna().sum())
    official_duplicate_groups = int(duplicates["duplicate_code_year_groups"].sum())
    operating_failures = int((~operating["engineering_valid"]).sum())
    plausible_hv = int(operating["plausible_heating_value"].sum())
    multi_failure = pd.DataFrame(
        {
            "gross": ~operating["energy_efficiency_raw_mwh_per_t"].between(
                EFF_FLOOR, EFF_CEIL
            ),
            "capacity_factor": ~operating["electrical_capacity_factor"].between(
                CAPACITY_FACTOR_FLOOR, CAPACITY_FACTOR_CEIL
            ),
            "utilization": ~operating["capacity_utilization_raw"].between(
                0.02, CAPACITY_UTILIZATION_CAP
            ),
            "design_intensity": ~operating[
                "generator_design_intensity_kw_per_t_day"
            ].between(0.10, 100.0),
            "age": operating["facility_age_years"].isna(),
        }
    ).sum(axis=1)

    flow_display = flow.copy()
    flow_display["events"] = flow_display["events"].map(
        lambda value: "NA" if pd.isna(value) else str(int(value))
    )
    with open(REPORT_PATH, "w", encoding="utf-8") as handle:
        handle.write("# Administrative-Lineage And Engineering Data-Quality Audit\n\n")
        handle.write("## Enforced Grain\n\n")
        handle.write(
            f"- Administrative rows: {len(panel):,}; audited stable administrative lineages: "
            f"{panel['stable_site_id'].nunique():,}; asset episodes: "
            f"{panel['asset_episode_id'].nunique():,}.\n"
            f"- Missing administrative-lineage IDs: {panel['stable_site_id'].isna().sum():,}.\n"
            f"- Missing asset-episode IDs: {missing_asset_episodes:,}.\n"
            f"- Duplicate stable-lineage-year rows: {stable_duplicate_mask.sum():,}.\n"
            "- Official facility codes are audited only within fiscal year. They are not used as longitudinal identifiers.\n\n"
        )
        handle.write("## Sample Arithmetic\n\n")
        handle.write(flow_display.to_markdown(index=False))
        handle.write("\n\n## Age Handling\n\n")
        handle.write(
            f"The raw panel contains {ages['panel_missing_raw_age']:,} missing and "
            f"{ages['panel_negative_raw_age']:,} negative reported ages. Negative values "
            "are converted to missing, not floored to zero. The constructed fleet has "
            f"{ages['fleet_missing_analysis_age']:,} missing and "
            f"{ages['fleet_negative_analysis_age']:,} negative analysis ages; the "
            f"operating-generator sample has {ages['operating_missing_analysis_age']:,} "
            f"missing and {ages['operating_negative_analysis_age']:,} negative analysis "
            f"ages. The component-model frame has "
            f"{ages['regression_missing_analysis_age']:,} missing ages.\n\n"
        )
        handle.write("## Engineering Bounds And Heating Values\n\n")
        handle.write(bounds.to_markdown(index=False, floatfmt=".3f"))
        handle.write(
            f"\n\nOf {len(operating):,} positive-throughput, positive-output generator rows, "
            f"{operating_failures:,} fail at least one predeclared engineering check and "
            f"{int((multi_failure > 1).sum()):,} fail more than one. Heating value is "
            f"within {HEATING_VALUE_FLOOR_MJ_KG:g}-{HEATING_VALUE_CEIL_MJ_KG:g} MJ/kg "
            f"for {plausible_hv:,} rows. Heating value is a plausibility/control field, "
            "not a condition for the primary component decomposition.\n\n"
        )
        handle.write("## Same-Year Official-Code Duplicates\n\n")
        handle.write(duplicates.to_markdown(index=False))
        handle.write(
            f"\n\nThere are {official_duplicate_groups:,} duplicate official-code-year groups. "
            "These collisions do not create duplicate stable-lineage-year observations and "
            "are not resolved by treating official codes as persistent facility IDs.\n\n"
        )
        handle.write("## Identity-Uncertainty Exposure\n\n")
        handle.write(
            f"The resolver accepts and explicitly exposes "
            f"{identity_uncertainty['uncertain_link_rows']:,} uncertain links, all "
            "supported by a strong exact-name or official-code signal. Those links occur "
            f"within {identity_uncertainty['uncertain_lineages']:,} administrative "
            "lineages. Excluding every affected lineage leaves "
            f"{identity_uncertainty['identity_certain_adoption_rows']:,} exact-year "
            f"entry-risk rows across "
            f"{identity_uncertainty['identity_certain_adoption_sites']:,} lineages and "
            f"{identity_uncertainty['identity_certain_adoption_events']:,} events, versus "
            f"{identity_uncertainty['all_adoption_rows']:,}/"
            f"{identity_uncertainty['all_adoption_sites']:,}/"
            f"{identity_uncertainty['all_adoption_events']:,} in the broad frame. The "
            "engineering-valid component sample retains "
            f"{identity_uncertainty['identity_certain_engineering_rows']:,} rows across "
            f"{identity_uncertainty['identity_certain_engineering_sites']:,} lineages "
            "after the same whole-lineage exclusion.\n\n"
        )
        handle.write("## Audit Conclusion\n\n")
        handle.write(
            "The model sample is a complete-case subset of the positive-output generator "
            "sample after explicit engineering exclusions. The audit supports administrative-lineage "
            "clustering and component interpretation; it does not establish measurement "
            "error absence or causal identification.\n"
        )


def main() -> None:
    panel = load_panel()
    fleet = build_full_fleet_frame(panel)
    operating = build_operating_power_frame(panel)
    regression = build_regression_frame(panel)
    adoption = build_adoption_frame(panel)
    adoption_model = build_adoption_model_frame(adoption=adoption)
    uncertain_mask = panel["identity_match_uncertain"].fillna(False).astype(bool)
    uncertain_lineages = set(
        panel.loc[uncertain_mask, "stable_site_id"].astype(str)
    )
    identity_certain_adoption = adoption_model[
        ~adoption_model["analysis_facility_id"].astype(str).isin(uncertain_lineages)
    ].copy()
    identity_certain_regression = regression[
        ~regression["identity_lineage_uncertain"]
    ].copy()
    identity_uncertainty = {
        "uncertain_link_rows": int(uncertain_mask.sum()),
        "uncertain_lineages": int(len(uncertain_lineages)),
        "all_adoption_rows": int(len(adoption_model)),
        "all_adoption_sites": int(adoption_model["analysis_facility_id"].nunique()),
        "all_adoption_events": int(adoption_model["adopt_power_this_year"].sum()),
        "identity_certain_adoption_rows": int(len(identity_certain_adoption)),
        "identity_certain_adoption_sites": int(
            identity_certain_adoption["analysis_facility_id"].nunique()
        ),
        "identity_certain_adoption_events": int(
            identity_certain_adoption["adopt_power_this_year"].sum()
        ),
        "all_engineering_rows": int(len(regression)),
        "all_engineering_sites": int(regression["analysis_facility_id"].nunique()),
        "identity_certain_engineering_rows": int(len(identity_certain_regression)),
        "identity_certain_engineering_sites": int(
            identity_certain_regression["analysis_facility_id"].nunique()
        ),
    }

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

    flow = sample_flow_table(
        panel, fleet, operating, regression, adoption, adoption_model
    )
    bounds = engineering_bounds_table(operating, regression)
    duplicates = duplicate_code_table(panel)
    ages = age_audit(panel, fleet, operating, regression)
    if (
        ages["fleet_negative_analysis_age"]
        or ages["operating_negative_analysis_age"]
        or ages["regression_negative_analysis_age"]
    ):
        raise ValueError("Negative analysis ages survived the missing-value rule")

    flow.to_csv(FLOW_PATH, index=False, float_format="%.10g")
    bounds.to_csv(BOUNDS_PATH, index=False, float_format="%.10g")
    duplicates.to_csv(DUPLICATES_PATH, index=False, float_format="%.10g")
    write_report(
        panel,
        fleet,
        operating,
        regression,
        flow,
        bounds,
        duplicates,
        ages,
        identity_uncertainty,
    )

    manifest_path = write_stage_manifest(
        "06a_data_quality_sensitivity",
        inputs=["data/processed/incineration_panel_identified.csv"],
        outputs=[
            "output/data_quality_sensitivity.md",
            "output/data_quality_sample_flow.csv",
            "output/data_quality_engineering_bounds.csv",
            "output/data_quality_official_code_duplicates.csv",
        ],
        metadata={
            "stable_site_year_duplicates": duplicate_stable_years,
            "missing_stable_site_ids": missing_stable,
            "missing_asset_episode_ids": missing_asset_episodes,
            "stable_sites": int(panel["stable_site_id"].nunique()),
            "asset_episodes": int(panel["asset_episode_id"].nunique()),
            "age_audit": ages,
            "operating_rows": int(len(operating)),
            "engineering_valid_rows": int(len(regression)),
            "engineering_excluded_rows": int(
                (~operating["engineering_valid"]).sum()
            ),
            "plausible_heating_value_rows": int(
                operating["plausible_heating_value"].sum()
            ),
            "official_duplicate_code_year_groups": int(
                duplicates["duplicate_code_year_groups"].sum()
            ),
            "identity_uncertainty": identity_uncertainty,
            "sample_flow": flow.to_dict(orient="records"),
        },
    )
    print(f"Saved: {REPORT_PATH}")
    print(f"Saved: {FLOW_PATH}")
    print(f"Saved: {BOUNDS_PATH}")
    print(f"Saved: {DUPLICATES_PATH}")
    print(f"Manifest: {manifest_path}")


if __name__ == "__main__":
    main()
