"""
Shared helpers for the incineration-thesis analysis pipeline.

This module centralizes the empirical design so the scripts and repo docs can
point to one canonical set of sample-construction and transformation rules.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
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
    "throughput_t_year",
    "power_generated_mwh",
    "facility_age_years",
    "capacity_t_day",
    "capacity_100t",
    "capacity_utilization_capped",
    "heating_value_mj_kg",
    "grid_ef_kgco2_kwh",
    "avoided_co2_t",
    "energy_efficiency_raw_mwh_per_t",
    "energy_efficiency_mwh_per_t",
    "log_efficiency",
]

ADOPTION_COLUMNS = [
    "analysis_facility_id",
    "facility_code",
    "fiscal_year",
    "facility_name",
    "prefecture",
    "year_started",
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
    "lag_facility_age_years",
    "lag_age_band",
    "lag_capacity_t_day",
    "lag_capacity_100t",
]

ADOPTION_PATHWAY_AUDIT_COLUMNS = [
    "analysis_facility_id",
    "facility_code",
    "fiscal_year",
    "prefecture",
    "facility_name",
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


def stable_float(value: float, sig_digits: int = 15) -> float:
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
        "adoption_model": "observed_first_adoption_cloglog_hazard",
        "adoption_risk_set_excludes_left_censored_generators": True,
        "adoption_predictors_lagged_one_year": True,
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
    return fleet


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
) -> pd.DataFrame:
    """
    Build the estimation frame for the adoption model.

    The hazard uses lagged facility characteristics so the reported predictors
    are measured before the observed adoption year rather than contemporaneously
    with it.
    """
    if adoption is None:
        adoption = build_adoption_frame(panel)

    model = adoption.sort_values(["analysis_facility_id", "fiscal_year"]).copy()
    group = model.groupby("analysis_facility_id", sort=False)
    model["lag_facility_age_years"] = group["facility_age_years"].shift(1)
    model["lag_age_band"] = group["age_band"].shift(1)
    model["lag_capacity_t_day"] = group["capacity_t_day"].shift(1)
    model["lag_capacity_100t"] = group["capacity_100t"].shift(1)

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
    model.attrs["lag_drop_first_rows"] = lag_drop_first_rows
    model.attrs["lag_drop_additional_missing_rows"] = lag_drop_additional_missing_rows
    model.attrs["lag_drop_additional_missing_facilities"] = lag_drop_additional_missing_facilities
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

    forward_mask = events["year_started_forward"] | placeholder_mask
    reset_mask = ~forward_mask & (events["year_reset"] | events["age_reset"])
    continuity_mask = (
        ~forward_mask
        & ~reset_mask
        & events["lag_year_started"].notna()
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
    power["log_efficiency"] = np.log(power["energy_efficiency_mwh_per_t"])
    power["capacity_100t"] = power["capacity_t_day"] / 100.0
    power["heating_value_mj_kg"] = power["heating_value_kj_kg"] / 1000.0

    return power


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
            "grid_ef_kgco2_kwh",
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
            f"- Lagged adoption-model observations: {summary['adoption_model_obs']:,} "
            f"({summary['adoption_model_facilities']:,} facilities; "
            f"{summary['adoption_model_events']:,} events)"
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
            f"- Pre-Fukushima ratio (FY2005-FY{PRE_FUKUSHIMA_END}): "
            f"{summary['pre_fukushima_within_total_ratio']:.4f}"
        ),
        (
            f"- Post-Fukushima ratio (FY{POST_FUKUSHIMA_START}-FY2024): "
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
