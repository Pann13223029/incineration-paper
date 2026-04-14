"""
Shared helpers for the incineration-thesis analysis pipeline.

This module centralizes the empirical design so the scripts and repo docs can
point to one canonical set of sample-construction and transformation rules.
"""

from __future__ import annotations

import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
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

IDENTIFIER_DTYPES = {
    "facility_code": "string",
    "muni_code": "string",
}


def get_git_sha() -> str:
    """Return the current git SHA when available."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
        )
        return result.stdout.strip()
    except Exception:
        return "unknown"


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
    }


def load_panel(filename: str = "incineration_panel_enriched.csv") -> pd.DataFrame:
    """Load a processed panel file."""
    path = os.path.join(PROCESSED_DIR, filename)
    return pd.read_csv(path, dtype=IDENTIFIER_DTYPES)


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

    power["analysis_facility_id"] = power["facility_code"].astype("string").str.strip()
    power["analysis_facility_id"] = power["analysis_facility_id"].str.replace(
        ".0", "", regex=False
    )
    power["analysis_facility_id"] = power["analysis_facility_id"].replace(
        {"": pd.NA, "nan": pd.NA, "None": pd.NA, "<NA>": pd.NA}
    )
    power["facility_age_years"] = power["facility_age"].clip(lower=0)
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

    power_flagged = panel[panel["has_power_gen"] == True].copy()
    operating = build_operating_power_frame(panel)
    regression = build_regression_frame(panel)

    summary = {
        "full_panel_obs": int(len(panel)),
        "full_panel_facilities_with_codes": int(panel["facility_code"].nunique()),
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
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "git_sha": get_git_sha(),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "analysis_config": analysis_config(),
        "inputs": inputs,
        "outputs": outputs,
        "metadata": metadata,
    }
    path = os.path.join(MANIFEST_DIR, f"{stage_name}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    return path


def write_sample_definition_report(path: str, summary: dict[str, Any]) -> None:
    """Write a human-readable sample definition report."""
    lines = [
        "# Analysis Sample Definition",
        "",
        "This report documents the canonical descriptive and regression samples used by the analysis scripts.",
        "",
        f"- Full panel: {summary['full_panel_obs']:,} rows",
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
