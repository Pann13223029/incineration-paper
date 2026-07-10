"""
Shared helpers for the incineration-thesis analysis pipeline.

This module centralizes the empirical design so the scripts and repo docs can
point to one canonical set of sample-construction and transformation rules.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import unicodedata
from typing import Any

import numpy as np
import pandas as pd

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
RAW_DIR = os.path.join(REPO_ROOT, "data", "raw", "facility_annual")
PROCESSED_DIR = os.path.join(REPO_ROOT, "data", "processed")
OUTPUT_DIR = os.path.join(REPO_ROOT, "output")
MANIFEST_DIR = os.path.join(OUTPUT_DIR, "manifests")
os.makedirs(MANIFEST_DIR, exist_ok=True)

EFF_FLOOR = 0.01
EFF_CEIL = 0.80
CAPACITY_UTILIZATION_CAP = 1.0
PRE_FUKUSHIMA_END = 2011
POST_FUKUSHIMA_START = 2012
AGE_BAND_BINS = [0, 10, 20, 30, float("inf")]
AGE_BAND_LABELS = ["0-10 yrs", "10-20 yrs", "20-30 yrs", "30+ yrs"]

REGRESSION_COLUMNS = [
    "analysis_facility_id",
    "facility_code",
    "fiscal_year",
    "facility_name",
    "prefecture",
    "n_furnaces",
    "furnace_type",
    "operation_mode",
    "facility_type",
    "furnace_type_group",
    "operation_mode_group",
    "facility_type_group",
    "continuous_operation",
    "gasification_melting",
    "throughput_t_year",
    "power_generated_mwh",
    "power_efficiency_pct",
    "facility_age_years",
    "capacity_t_day",
    "capacity_100t",
    "capacity_utilization_capped",
    "heating_value_mj_kg",
    "grid_ef_kgco2_kwh",
    "avoided_co2_t",
    "energy_efficiency_raw_mwh_per_t",
    "energy_efficiency_mwh_per_t",
    "log_efficiency_raw",
    "log_efficiency",
    "gross_thermal_conversion_ratio",
    "log_thermal_conversion_proxy",
    "log_reported_power_efficiency",
]

ADOPTION_COLUMNS = [
    "analysis_facility_id",
    "facility_code",
    "fiscal_year",
    "facility_name",
    "prefecture",
    "year_started",
    "n_furnaces",
    "furnace_type_group",
    "operation_mode_group",
    "facility_type_group",
    "continuous_operation",
    "gasification_melting",
    "has_power_gen",
    "adopt_power_this_year",
    "facility_age_years",
    "age_band",
    "capacity_t_day",
    "capacity_100t",
    "throughput_t_year",
    "throughput_100k_t",
    "heating_value_mj_kg",
]

ADOPTION_MODEL_COLUMNS = [
    *ADOPTION_COLUMNS,
    "risk_observed_rows",
    "first_risk_fiscal_year",
    "elapsed_at_risk_years",
    "lag_fiscal_year",
    "lag_gap_years",
    "exact_one_year_lag",
    "lag_facility_age_years",
    "lag_age_band",
    "lag_capacity_t_day",
    "lag_capacity_100t",
    "lag_throughput_t_year",
    "lag_n_furnaces",
    "lag_furnace_type_group",
    "lag_operation_mode_group",
    "lag_facility_type_group",
    "lag_continuous_operation",
    "lag_gasification_melting",
]

ADOPTION_PATHWAY_AUDIT_COLUMNS = [
    "analysis_facility_id",
    "facility_code",
    "fiscal_year",
    "prefecture",
    "facility_name",
    "lag_fiscal_year",
    "lag_gap_years",
    "exact_one_year_lag",
    "year_started",
    "lag_year_started",
    "facility_age_years",
    "lag_facility_age_years",
    "capacity_t_day",
    "lag_capacity_t_day",
    "name_changed",
    "year_started_forward",
    "year_reset",
    "age_reset",
    "pathway_category",
    "pathway_basis",
]

IDENTIFIER_DTYPES = {
    "facility_code": "string",
    "muni_code": "string",
}


def stable_float(value: float, sig_digits: int = 7) -> float:
    """Round floats to a stable significant-digit representation."""
    if not np.isfinite(value):
        return value
    return float(f"{value:.{sig_digits}g}")


def normalize_manifest_value(value: Any) -> Any:
    """Recursively coerce manifest payloads into deterministic JSON values."""
    if isinstance(value, dict):
        return {str(k): normalize_manifest_value(v) for k, v in value.items()}
    if isinstance(value, list):
        return [normalize_manifest_value(v) for v in value]
    if isinstance(value, tuple):
        return [normalize_manifest_value(v) for v in value]
    if isinstance(value, np.floating):
        return stable_float(float(value))
    if isinstance(value, float):
        return stable_float(value)
    if isinstance(value, np.integer):
        return int(value)
    if isinstance(value, np.bool_):
        return bool(value)
    return value


def analysis_config() -> dict[str, Any]:
    """Return the shared analysis configuration."""
    return {
        "efficiency_floor_mwh_per_t": EFF_FLOOR,
        "efficiency_ceiling_mwh_per_t": EFF_CEIL,
        "capacity_utilization_cap": CAPACITY_UTILIZATION_CAP,
        "pre_fukushima_end": PRE_FUKUSHIMA_END,
        "post_fukushima_start": POST_FUKUSHIMA_START,
        "regression_requires_positive_output": True,
        "regression_requires_official_facility_code": True,
        "regression_winsorization_method": "clip",
        "adoption_model": "observed_first_adoption_logit_hazard",
        "adoption_risk_set_excludes_left_censored_generators": True,
        "adoption_predictors_lagged_exact_one_year": True,
        "adoption_elapsed_duration_uses_fiscal_years": True,
        "adoption_active_conversion_requires_positive_prior_throughput": True,
        "adoption_previous_observed_coded_row_retained_as_sensitivity": True,
        "technology_categories_normalized_to_compact_groups": True,
    }


def load_panel(filename: str = "incineration_panel_enriched.csv") -> pd.DataFrame:
    """Load a processed panel file."""
    path = os.path.join(PROCESSED_DIR, filename)
    return pd.read_csv(path, dtype=IDENTIFIER_DTYPES)


def normalize_analysis_facility_id(series: pd.Series) -> pd.Series:
    """Standardize the facility identifier used across analysis stages."""
    ids = series.astype("string").str.strip()
    ids = ids.str.replace(".0", "", regex=False)
    return ids.replace({"": pd.NA, "nan": pd.NA, "None": pd.NA, "<NA>": pd.NA})


def age_band_from_years(series: pd.Series) -> pd.Series:
    """Bucket facility ages into interpretable bands."""
    return pd.cut(
        series,
        bins=AGE_BAND_BINS,
        labels=AGE_BAND_LABELS,
        right=False,
    )


def normalize_category_value(value: Any) -> str:
    """Normalize source category labels while preserving an explicit unknown group."""
    if pd.isna(value):
        return ""
    normalized = unicodedata.normalize("NFKC", str(value)).strip()
    return re.sub(r"\s+", "", normalized)


def add_technology_profiles(frame: pd.DataFrame) -> pd.DataFrame:
    """Add compact, stable technology groups used by sensitivity models."""
    result = frame.copy()
    furnace = result["furnace_type"].map(normalize_category_value)
    operation = result["operation_mode"].map(normalize_category_value)
    facility = result["facility_type"].map(normalize_category_value)

    result["furnace_type_group"] = np.select(
        [
            furnace.str.contains("\u30b9\u30c8\u30fc\u30ab", na=False),
            furnace.str.contains("\u6d41\u52d5\u5e8a", na=False),
            furnace.str.contains("\u30b7\u30e3\u30d5\u30c8", na=False),
            furnace.str.contains("\u56de\u8ee2", na=False),
        ],
        ["Stoker", "Fluidized bed", "Shaft", "Rotary"],
        default="Other/unknown",
    )
    result["operation_mode_group"] = np.select(
        [
            operation.str.contains("\u5168\u9023\u7d9a\u904b\u8ee2", na=False),
            operation.str.contains("\u51c6\u9023\u7d9a\u904b\u8ee2", na=False),
            operation.str.contains("\u30d0\u30c3\u30c1\u904b\u8ee2", na=False),
        ],
        ["Continuous", "Semi-continuous", "Batch"],
        default="Other/unknown",
    )
    result["facility_type_group"] = np.select(
        [
            facility.str.contains("\u30ac\u30b9\u5316", na=False),
            facility.str.contains("\u713c\u5374", na=False),
        ],
        ["Gasification/melting", "Incineration"],
        default="Other/unknown",
    )
    result["continuous_operation"] = result["operation_mode_group"].eq(
        "Continuous"
    ).astype(int)
    result["gasification_melting"] = result["facility_type_group"].eq(
        "Gasification/melting"
    ).astype(int)
    return result


def build_full_fleet_frame(panel: pd.DataFrame | None = None) -> pd.DataFrame:
    """
    Build the coded full-fleet frame used for extensive-margin analysis.

    Rules:
    - requires an official facility identifier so facilities can be tracked over time
    - preserves both generating and non-generating facilities
    - adds shared transformations used by the adoption and efficiency stages
    """
    if panel is None:
        panel = load_panel()

    fleet = panel.copy()
    fleet["analysis_facility_id"] = normalize_analysis_facility_id(fleet["facility_code"])
    fleet = fleet[fleet["analysis_facility_id"].notna()].copy()
    fleet["facility_age_years"] = fleet["facility_age"].clip(lower=0)
    fleet["age_band"] = age_band_from_years(fleet["facility_age_years"])
    fleet["capacity_100t"] = fleet["capacity_t_day"] / 100.0
    fleet["throughput_100k_t"] = fleet["throughput_t_year"] / 100000.0
    fleet["heating_value_mj_kg"] = fleet["heating_value_kj_kg"] / 1000.0
    fleet["has_power_gen"] = fleet["has_power_gen"].fillna(False).astype(bool)
    return add_technology_profiles(fleet)


def build_adoption_frame(panel: pd.DataFrame | None = None) -> pd.DataFrame:
    """
    Build the extensive-margin adoption-risk frame.

    Each facility enters the risk set only if it is first observed without
    power generation. The frame then keeps yearly observations up to and
    including the first observed adoption of power generation.
    """
    fleet = build_full_fleet_frame(panel)

    rows: list[dict[str, Any]] = []
    left_censored_generators = 0

    for facility_id, group in fleet.groupby("analysis_facility_id", sort=False):
        group = group.sort_values("fiscal_year")
        if bool(group["has_power_gen"].iloc[0]):
            left_censored_generators += 1
            continue

        adopted = False
        for _, row in group.iterrows():
            if adopted:
                break

            adopt_now = bool(row["has_power_gen"])
            rows.append(
                {
                    "analysis_facility_id": facility_id,
                    "facility_code": row["facility_code"],
                    "fiscal_year": int(row["fiscal_year"]),
                    "facility_name": row["facility_name"],
                    "prefecture": row["prefecture"],
                    "year_started": row["year_started"],
                    "n_furnaces": row["n_furnaces"],
                    "furnace_type_group": row["furnace_type_group"],
                    "operation_mode_group": row["operation_mode_group"],
                    "facility_type_group": row["facility_type_group"],
                    "continuous_operation": row["continuous_operation"],
                    "gasification_melting": row["gasification_melting"],
                    "has_power_gen": bool(row["has_power_gen"]),
                    "adopt_power_this_year": int(adopt_now),
                    "facility_age_years": row["facility_age_years"],
                    "age_band": row["age_band"],
                    "capacity_t_day": row["capacity_t_day"],
                    "capacity_100t": row["capacity_100t"],
                    "throughput_t_year": row["throughput_t_year"],
                    "throughput_100k_t": row["throughput_100k_t"],
                    "heating_value_mj_kg": row["heating_value_mj_kg"],
                }
            )

            if adopt_now:
                adopted = True

    adoption = pd.DataFrame(rows, columns=ADOPTION_COLUMNS)
    adoption.attrs["left_censored_generators"] = left_censored_generators
    return adoption


def build_adoption_model_frame(
    panel: pd.DataFrame | None = None,
    adoption: pd.DataFrame | None = None,
    *,
    exact_year_only: bool = True,
) -> pd.DataFrame:
    """
    Build the estimation frame for the adoption model.

    The main hazard uses exact one-fiscal-year lagged facility characteristics so
    the reported predictors are measured before the observed adoption year rather
    than contemporaneously with it. Setting ``exact_year_only=False`` keeps the
    broader previous-observed-coded-row frame for sensitivity checks.
    """
    if adoption is None:
        adoption = build_adoption_frame(panel)

    model = adoption.sort_values(["analysis_facility_id", "fiscal_year"]).copy()
    group = model.groupby("analysis_facility_id", sort=False)
    model["risk_observed_rows"] = group.cumcount() + 1
    model["first_risk_fiscal_year"] = group["fiscal_year"].transform("min")
    model["elapsed_at_risk_years"] = (
        model["fiscal_year"] - model["first_risk_fiscal_year"] + 1
    )
    model["lag_fiscal_year"] = group["fiscal_year"].shift(1)
    model["lag_gap_years"] = model["fiscal_year"] - model["lag_fiscal_year"]
    model["exact_one_year_lag"] = model["lag_gap_years"].eq(1)
    model["lag_facility_age_years"] = group["facility_age_years"].shift(1)
    model["lag_age_band"] = group["age_band"].shift(1)
    model["lag_capacity_t_day"] = group["capacity_t_day"].shift(1)
    model["lag_capacity_100t"] = group["capacity_100t"].shift(1)
    model["lag_throughput_t_year"] = group["throughput_t_year"].shift(1)
    model["lag_n_furnaces"] = group["n_furnaces"].shift(1)
    model["lag_furnace_type_group"] = group["furnace_type_group"].shift(1)
    model["lag_operation_mode_group"] = group["operation_mode_group"].shift(1)
    model["lag_facility_type_group"] = group["facility_type_group"].shift(1)
    model["lag_continuous_operation"] = group["continuous_operation"].shift(1)
    model["lag_gasification_melting"] = group["gasification_melting"].shift(1)

    first_rows = group.cumcount().eq(0)
    extra_missing_mask = (
        model[["lag_age_band", "lag_capacity_100t", "prefecture"]].isna().any(axis=1)
        & ~first_rows
    )

    lag_drop_first_rows = int(first_rows.sum())
    lag_drop_additional_missing_rows = int(extra_missing_mask.sum())
    lag_drop_additional_missing_facilities = int(
        model.loc[extra_missing_mask, "analysis_facility_id"].nunique()
    )

    model = model.dropna(subset=["lag_age_band", "lag_capacity_100t", "prefecture"]).copy()
    previous_observed_obs = int(len(model))
    previous_observed_facilities = int(model["analysis_facility_id"].nunique())
    previous_observed_events = int(model["adopt_power_this_year"].sum())
    non_exact_mask = ~model["exact_one_year_lag"]
    non_exact_rows = int(non_exact_mask.sum())
    non_exact_events = int(model.loc[non_exact_mask, "adopt_power_this_year"].sum())
    lag_gap_counts = {
        str(int(gap)): int(count)
        for gap, count in model["lag_gap_years"].value_counts().sort_index().items()
    }
    event_lag_gap_counts = {
        str(int(gap)): int(count)
        for gap, count in model.loc[
            model["adopt_power_this_year"] == 1,
            "lag_gap_years",
        ].value_counts().sort_index().items()
    }
    if exact_year_only:
        model = model[model["exact_one_year_lag"]].copy()
    model.attrs["lag_drop_first_rows"] = lag_drop_first_rows
    model.attrs["lag_drop_additional_missing_rows"] = lag_drop_additional_missing_rows
    model.attrs["lag_drop_additional_missing_facilities"] = lag_drop_additional_missing_facilities
    model.attrs["exact_year_only"] = exact_year_only
    model.attrs["previous_observed_model_obs"] = previous_observed_obs
    model.attrs["previous_observed_model_facilities"] = previous_observed_facilities
    model.attrs["previous_observed_model_events"] = previous_observed_events
    model.attrs["non_exact_lag_rows"] = non_exact_rows
    model.attrs["non_exact_lag_events"] = non_exact_events
    model.attrs["lag_gap_counts"] = lag_gap_counts
    model.attrs["event_lag_gap_counts"] = event_lag_gap_counts
    result = model[ADOPTION_MODEL_COLUMNS].copy()
    result.attrs.update(model.attrs)
    return result


def build_adoption_pathway_audit(
    panel: pd.DataFrame | None = None,
    adoption: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """
    Audit observed first-adoption events by likely transition pathway.

    The audit is intentionally conservative. It classifies event rows using only
    continuity information already present in the administrative panel:
    - forward-dated or placeholder rows stay unresolved as planning/coding entries
    - year-start resets or age resets are treated as reset/rebuild-like events
    - continuity rows with no reset are treated as in-place upgrade-like events
    """
    if adoption is None:
        adoption = build_adoption_frame(panel)

    adoption_aug = adoption.sort_values(["analysis_facility_id", "fiscal_year"]).copy()

    group = adoption_aug.groupby("analysis_facility_id", sort=False)
    adoption_aug["lag_fiscal_year"] = group["fiscal_year"].shift(1)
    adoption_aug["lag_gap_years"] = adoption_aug["fiscal_year"] - adoption_aug["lag_fiscal_year"]
    adoption_aug["exact_one_year_lag"] = adoption_aug["lag_gap_years"].eq(1)
    adoption_aug["lag_year_started"] = group["year_started"].shift(1)
    adoption_aug["lag_facility_age_years"] = group["facility_age_years"].shift(1)
    adoption_aug["lag_capacity_t_day"] = group["capacity_t_day"].shift(1)
    adoption_aug["lag_facility_name"] = group["facility_name"].shift(1)

    events = adoption_aug[adoption_aug["adopt_power_this_year"] == 1].copy()
    placeholder_mask = events["facility_name"].fillna("").str.contains(
        "仮称|新設|建設中|名称未定",
        regex=True,
    )
    events["name_changed"] = events["facility_name"] != events["lag_facility_name"]
    events["year_started_forward"] = events["year_started"] > events["fiscal_year"]
    events["year_reset"] = events["year_started"] > events["lag_year_started"]
    events["age_reset"] = (
        (events["lag_facility_age_years"] >= 10)
        & (events["facility_age_years"] <= 2)
    )

    events["pathway_category"] = "Unresolved / insufficient continuity"
    events["pathway_basis"] = "No prior observed at-risk row with usable continuity fields"

    timing_ambiguous_mask = ~events["exact_one_year_lag"]
    forward_mask = ~timing_ambiguous_mask & (events["year_started_forward"] | placeholder_mask)
    reset_mask = ~timing_ambiguous_mask & ~forward_mask & (events["year_reset"] | events["age_reset"])
    continuity_mask = (
        ~timing_ambiguous_mask
        & ~forward_mask
        & ~reset_mask
        & events["lag_year_started"].notna()
    )

    events.loc[timing_ambiguous_mask, "pathway_category"] = (
        "Timing-ambiguous / non-adjacent coded row"
    )
    events.loc[timing_ambiguous_mask, "pathway_basis"] = (
        "Prior coded row is not the immediately preceding fiscal year; mechanism language is weakened"
    )
    events.loc[forward_mask, "pathway_category"] = "Forward-dated / placeholder entry"
    events.loc[forward_mask, "pathway_basis"] = (
        "Forward-dated `year_started` or placeholder/new-build naming at event row"
    )
    events.loc[reset_mask, "pathway_category"] = "Reset / rebuild-like transition"
    events.loc[reset_mask, "pathway_basis"] = (
        "Observed reset in `year_started` or mature-to-new age reset before adoption"
    )
    events.loc[continuity_mask, "pathway_category"] = (
        "In-place upgrade / continuity transition"
    )
    events.loc[continuity_mask, "pathway_basis"] = (
        "No observed start-year reset; continuity row remains in service at adoption"
    )

    return events[ADOPTION_PATHWAY_AUDIT_COLUMNS].copy()


def build_operating_power_frame(panel: pd.DataFrame | None = None) -> pd.DataFrame:
    """
    Build the descriptive operating sample.

    Rules:
    - power-generation capacity must be present (`has_power_gen == True`)
    - throughput must be positive
    - electricity output must be positive
    - efficiency is retained in both raw and winsorized form
    - age is floored at zero for one-year commissioning mismatches
    - utilization is capped at 1.0 for analysis
    """
    if panel is None:
        panel = load_panel()

    power = panel[panel["has_power_gen"] == True].copy()
    power = power[
        power["throughput_t_year"].notna() & (power["throughput_t_year"] > 0)
    ].copy()
    power = power[
        power["power_generated_mwh"].notna() & (power["power_generated_mwh"] > 0)
    ].copy()

    power["analysis_facility_id"] = normalize_analysis_facility_id(power["facility_code"])
    power["facility_age_years"] = power["facility_age"].clip(lower=0)
    power["age_band"] = age_band_from_years(power["facility_age_years"])
    power["capacity_utilization_capped"] = power["capacity_utilization"].clip(
        lower=0,
        upper=CAPACITY_UTILIZATION_CAP,
    )
    power["energy_efficiency_raw_mwh_per_t"] = (
        power["power_generated_mwh"] / power["throughput_t_year"]
    )
    power["energy_efficiency_mwh_per_t"] = power[
        "energy_efficiency_raw_mwh_per_t"
    ].clip(lower=EFF_FLOOR, upper=EFF_CEIL)
    power["log_efficiency_raw"] = np.log(power["energy_efficiency_raw_mwh_per_t"])
    power["log_efficiency"] = np.log(power["energy_efficiency_mwh_per_t"])
    power["capacity_100t"] = power["capacity_t_day"] / 100.0
    power["heating_value_mj_kg"] = power["heating_value_kj_kg"] / 1000.0

    positive_heating_value = power["heating_value_mj_kg"].gt(0)
    power["gross_thermal_conversion_ratio"] = np.where(
        positive_heating_value,
        power["energy_efficiency_raw_mwh_per_t"]
        * 3.6
        / power["heating_value_mj_kg"],
        np.nan,
    )
    power["log_thermal_conversion_proxy"] = np.where(
        power["gross_thermal_conversion_ratio"].gt(0),
        np.log(power["gross_thermal_conversion_ratio"]),
        np.nan,
    )
    reported_efficiency_fraction = power["power_efficiency_pct"] / 100.0
    power["log_reported_power_efficiency"] = np.where(
        reported_efficiency_fraction.gt(0),
        np.log(reported_efficiency_fraction),
        np.nan,
    )

    return add_technology_profiles(power)


def build_regression_frame(panel: pd.DataFrame | None = None) -> pd.DataFrame:
    """
    Build the canonical regression sample.

    This frame is stricter than the descriptive operating sample:
    - requires an official facility identifier for clustering
    - requires all model covariates to be non-missing
    """
    power = build_operating_power_frame(panel)
    reg = power[power["analysis_facility_id"].notna()].copy()
    reg = reg.dropna(
        subset=[
            "facility_age_years",
            "capacity_100t",
            "capacity_utilization_capped",
            "heating_value_mj_kg",
            "log_efficiency",
        ]
    ).copy()
    return reg[REGRESSION_COLUMNS].copy()


def within_total_variance_ratio(
    frame: pd.DataFrame,
    value_col: str,
    entity_col: str = "analysis_facility_id",
) -> float:
    """Compute the within-entity to total variance ratio."""
    if frame.empty:
        return float("nan")

    means = frame.groupby(entity_col)[value_col].transform("mean")
    total_var = frame[value_col].var(ddof=1)
    if pd.isna(total_var) or total_var <= 0:
        return float("nan")

    within_var = ((frame[value_col] - means) ** 2).sum() / max(len(frame) - 1, 1)
    return float(within_var / total_var)


def sample_summary(panel: pd.DataFrame | None = None) -> dict[str, Any]:
    """Return a compact summary of descriptive and regression samples."""
    if panel is None:
        panel = load_panel()

    full_fleet = build_full_fleet_frame(panel)
    adoption = build_adoption_frame(panel)
    adoption_model = build_adoption_model_frame(adoption=adoption)
    power_flagged = panel[panel["has_power_gen"] == True].copy()
    operating = build_operating_power_frame(panel)
    regression = build_regression_frame(panel)
    active_adoption_model = adoption_model[
        adoption_model["lag_throughput_t_year"].gt(0)
    ].copy()
    duration_mismatch = adoption_model["elapsed_at_risk_years"].ne(
        adoption_model["risk_observed_rows"]
    )
    fy2024 = panel[panel["fiscal_year"].eq(2024)].copy()

    summary = {
        "full_panel_obs": int(len(panel)),
        "full_panel_facilities_with_codes": int(panel["facility_code"].nunique()),
        "coded_full_fleet_obs": int(len(full_fleet)),
        "coded_full_fleet_facilities": int(full_fleet["analysis_facility_id"].nunique()),
        "power_generation_flagged_obs": int(len(power_flagged)),
        "operating_power_obs": int(len(operating)),
        "operating_power_facilities_with_codes": int(operating["facility_code"].nunique()),
        "operating_power_missing_facility_codes": int(
            operating["analysis_facility_id"].isna().sum()
        ),
        "operating_negative_age_rows_floored_to_zero": int(
            (operating["facility_age"] < 0).sum()
        ),
        "raw_efficiency_below_floor": int(
            (operating["energy_efficiency_raw_mwh_per_t"] < EFF_FLOOR).sum()
        ),
        "raw_efficiency_above_ceiling": int(
            (operating["energy_efficiency_raw_mwh_per_t"] > EFF_CEIL).sum()
        ),
        "left_censored_generators": int(adoption.attrs.get("left_censored_generators", 0)),
        "adoption_risk_obs": int(len(adoption)),
        "adoption_risk_facilities": int(adoption["analysis_facility_id"].nunique()),
        "adoption_events": int(adoption["adopt_power_this_year"].sum()),
        "adoption_model_obs": int(len(adoption_model)),
        "adoption_model_facilities": int(adoption_model["analysis_facility_id"].nunique()),
        "adoption_model_events": int(adoption_model["adopt_power_this_year"].sum()),
        "adoption_active_model_obs": int(len(active_adoption_model)),
        "adoption_active_model_facilities": int(
            active_adoption_model["analysis_facility_id"].nunique()
        ),
        "adoption_active_model_events": int(
            active_adoption_model["adopt_power_this_year"].sum()
        ),
        "adoption_nonpositive_prior_throughput_rows": int(
            adoption_model["lag_throughput_t_year"].fillna(0).le(0).sum()
        ),
        "adoption_nonpositive_prior_throughput_events": int(
            adoption_model.loc[
                adoption_model["lag_throughput_t_year"].fillna(0).le(0),
                "adopt_power_this_year",
            ].sum()
        ),
        "adoption_duration_row_count_mismatch": int(duration_mismatch.sum()),
        "adoption_previous_observed_model_obs": int(
            adoption_model.attrs.get("previous_observed_model_obs", len(adoption_model))
        ),
        "adoption_previous_observed_model_facilities": int(
            adoption_model.attrs.get(
                "previous_observed_model_facilities",
                adoption_model["analysis_facility_id"].nunique(),
            )
        ),
        "adoption_previous_observed_model_events": int(
            adoption_model.attrs.get(
                "previous_observed_model_events",
                adoption_model["adopt_power_this_year"].sum(),
            )
        ),
        "adoption_non_exact_lag_rows": int(adoption_model.attrs.get("non_exact_lag_rows", 0)),
        "adoption_non_exact_lag_events": int(adoption_model.attrs.get("non_exact_lag_events", 0)),
        "adoption_lag_gap_counts": adoption_model.attrs.get("lag_gap_counts", {}),
        "adoption_event_lag_gap_counts": adoption_model.attrs.get("event_lag_gap_counts", {}),
        "adoption_model_drop_first_rows": int(adoption_model.attrs.get("lag_drop_first_rows", 0)),
        "adoption_model_drop_additional_missing_rows": int(
            adoption_model.attrs.get("lag_drop_additional_missing_rows", 0)
        ),
        "adoption_model_drop_additional_missing_facilities": int(
            adoption_model.attrs.get("lag_drop_additional_missing_facilities", 0)
        ),
        "regression_obs": int(len(regression)),
        "regression_facilities": int(regression["analysis_facility_id"].nunique()),
        "regression_year_start": int(regression["fiscal_year"].min()),
        "regression_year_end": int(regression["fiscal_year"].max()),
        "regression_within_total_ratio": round(
            within_total_variance_ratio(regression, "log_efficiency"), 4
        ),
        "fy2024_panel_rows": int(len(fy2024)),
        "fy2024_positive_capacity_rows": int(fy2024["has_power_gen"].sum()),
        "fy2024_positive_capacity_share_pct": float(
            fy2024["has_power_gen"].mean() * 100
        ),
    }

    for label, subset in [
        ("pre_fukushima", regression[regression["fiscal_year"] <= PRE_FUKUSHIMA_END]),
        ("post_fukushima", regression[regression["fiscal_year"] >= POST_FUKUSHIMA_START]),
    ]:
        summary[f"{label}_obs"] = int(len(subset))
        summary[f"{label}_facilities"] = int(subset["analysis_facility_id"].nunique())
        summary[f"{label}_within_total_ratio"] = round(
            within_total_variance_ratio(subset, "log_efficiency"), 4
        )

    return summary


def write_stage_manifest(
    stage_name: str,
    inputs: list[str],
    outputs: list[str],
    metadata: dict[str, Any],
) -> str:
    """Write a JSON manifest for a stage and return the manifest path."""
    manifest = {
        "stage": stage_name,
        "python": sys.version.split()[0],
        "analysis_config": analysis_config(),
        "inputs": inputs,
        "outputs": outputs,
        "metadata": normalize_manifest_value(metadata),
    }
    path = os.path.join(MANIFEST_DIR, f"{stage_name}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False, sort_keys=True)
        f.write("\n")
    return path


def write_sample_definition_report(path: str, summary: dict[str, Any]) -> None:
    """Write a human-readable sample definition report."""
    lines = [
        "# Analysis Sample Definition",
        "",
        "This report documents the canonical descriptive and regression samples used by the analysis scripts.",
        "",
        f"- Full panel: {summary['full_panel_obs']:,} rows",
        (
            f"- Coded full-fleet frame (facility identifier present): "
            f"{summary['coded_full_fleet_obs']:,} rows "
            f"({summary['coded_full_fleet_facilities']:,} facilities)"
        ),
        f"- Power-generation rows flagged by MOE (`has_power_gen == True`): {summary['power_generation_flagged_obs']:,}",
        (
            f"- FY2024 analytic-panel positive-capacity share: "
            f"{summary['fy2024_positive_capacity_rows']:,} of "
            f"{summary['fy2024_panel_rows']:,} rows "
            f"({summary['fy2024_positive_capacity_share_pct']:.1f}%)"
        ),
        (
            f"- Operating power-generation sample (positive throughput and positive output): "
            f"{summary['operating_power_obs']:,}"
        ),
        (
            f"- Operating sample rows missing official facility codes: "
            f"{summary['operating_power_missing_facility_codes']:,}"
        ),
        (
            f"- Raw efficiency below {EFF_FLOOR:.2f} MWh/t before winsorization: "
            f"{summary['raw_efficiency_below_floor']:,}"
        ),
        (
            f"- Raw efficiency above {EFF_CEIL:.2f} MWh/t before winsorization: "
            f"{summary['raw_efficiency_above_ceiling']:,}"
        ),
        (
            f"- Negative facility-age rows floored to zero: "
            f"{summary['operating_negative_age_rows_floored_to_zero']:,}"
        ),
        "",
        "## Extensive-Margin Adoption Frame",
        "",
        (
            f"- Left-censored facilities already generating power in their first observed year: "
            f"{summary['left_censored_generators']:,}"
        ),
        (
            f"- Adoption risk-set observations: {summary['adoption_risk_obs']:,} "
            f"({summary['adoption_risk_facilities']:,} facilities)"
        ),
        (
            f"- Observed first-adoption events in the panel window: "
            f"{summary['adoption_events']:,}"
        ),
        (
            f"- Exact-year lagged adoption-model observations: {summary['adoption_model_obs']:,} "
            f"({summary['adoption_model_facilities']:,} facilities; "
            f"{summary['adoption_model_events']:,} events)"
        ),
        (
            f"- Positive-prior-throughput conversion sensitivity: "
            f"{summary['adoption_active_model_obs']:,} observations "
            f"({summary['adoption_active_model_facilities']:,} facilities; "
            f"{summary['adoption_active_model_events']:,} events)"
        ),
        (
            f"- Main-frame events with zero or missing prior-year throughput: "
            f"{summary['adoption_nonpositive_prior_throughput_events']:,}"
        ),
        (
            f"- Exact-lag rows where elapsed fiscal duration differs from observed-row count: "
            f"{summary['adoption_duration_row_count_mismatch']:,}"
        ),
        (
            f"- Broader previous-observed-coded-row adoption frame before exact-year restriction: "
            f"{summary['adoption_previous_observed_model_obs']:,} observations "
            f"({summary['adoption_previous_observed_model_facilities']:,} facilities; "
            f"{summary['adoption_previous_observed_model_events']:,} events)"
        ),
        (
            f"- Non-exact lag rows excluded from the main adoption model: "
            f"{summary['adoption_non_exact_lag_rows']:,} "
            f"({summary['adoption_non_exact_lag_events']:,} events)"
        ),
        (
            f"- First observed at-risk years dropped because lagged predictors are required: "
            f"{summary['adoption_model_drop_first_rows']:,}"
        ),
        (
            f"- Additional rows dropped for missing lagged age/capacity: "
            f"{summary['adoption_model_drop_additional_missing_rows']:,} "
            f"({summary['adoption_model_drop_additional_missing_facilities']:,} facilities)"
        ),
        "",
        "## Regression Frame",
        "",
        (
            f"- Regression observations: {summary['regression_obs']:,} "
            f"({summary['regression_facilities']:,} facilities)"
        ),
        (
            f"- Fiscal years: FY{summary['regression_year_start']} to "
            f"FY{summary['regression_year_end']}"
        ),
        (
            f"- Within/total variance ratio (pooled log-efficiency): "
            f"{summary['regression_within_total_ratio']:.4f}"
        ),
        (
            f"- Early coded-window ratio (FY2005-FY2009): "
            f"{summary['pre_fukushima_within_total_ratio']:.4f}"
        ),
        (
            f"- Later coded-window ratio (FY2013-FY2024): "
            f"{summary['post_fukushima_within_total_ratio']:.4f}"
        ),
    ]

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def model_std_errors(model: Any) -> pd.Series:
    """Return model standard errors for statsmodels or linearmodels results."""
    if hasattr(model, "std_errors"):
        return model.std_errors
    return model.bse


def model_pvalues(model: Any) -> pd.Series:
    """Return model p-values for statsmodels or linearmodels results."""
    return model.pvalues


def significance_stars(p_value: float) -> str:
    """Convert a p-value into significance stars."""
    if p_value < 0.001:
        return "***"
    if p_value < 0.01:
        return "**"
    if p_value < 0.05:
        return "*"
    return ""
