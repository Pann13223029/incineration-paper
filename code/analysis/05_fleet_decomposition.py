"""Decompose fleet electricity recovery into coverage and conditional intensity."""

from __future__ import annotations

import os

import numpy as np
import pandas as pd

from panel_utils import (
    CAPACITY_FACTOR_CEIL,
    CAPACITY_FACTOR_FLOOR,
    EFF_CEIL,
    EFF_FLOOR,
    OUTPUT_DIR,
    load_panel,
    write_stage_manifest,
)


ANNUAL_PATH = os.path.join(OUTPUT_DIR, "fleet_decomposition.csv")
SEGMENT_PATH = os.path.join(OUTPUT_DIR, "fy2024_fleet_segments.csv")
REPORT_PATH = os.path.join(OUTPUT_DIR, "fleet_decomposition.md")


def build_annual_decomposition(panel: pd.DataFrame) -> pd.DataFrame:
    frame = panel.copy()
    frame["positive_throughput"] = frame["throughput_t_year"].fillna(0).gt(0)
    frame["positive_output"] = frame["power_generated_mwh"].fillna(0).gt(0)
    frame["installed_generation"] = frame["has_power_gen"].fillna(False)
    frame["gross_mwh_t"] = frame["power_generated_mwh"] / frame["throughput_t_year"]
    frame["electrical_capacity_factor"] = (
        frame["power_generated_mwh"] / (frame["power_capacity_kw"] * 8.76)
    )
    frame["engineering_output_valid"] = (
        frame["positive_throughput"]
        & frame["positive_output"]
        & frame["power_capacity_kw"].gt(0)
        & frame["gross_mwh_t"].between(EFF_FLOOR, EFF_CEIL)
        & frame["electrical_capacity_factor"].between(
            CAPACITY_FACTOR_FLOOR,
            CAPACITY_FACTOR_CEIL,
        )
    )

    rows: list[dict[str, float | int]] = []
    for fiscal_year, year in frame.groupby("fiscal_year", sort=True):
        total_throughput = float(year["throughput_t_year"].fillna(0).sum())
        total_capacity = float(year["capacity_t_day"].fillna(0).sum())
        active = year[year["positive_throughput"]]
        installed = year[year["installed_generation"]]
        active_installed = year[
            year["positive_throughput"] & year["installed_generation"]
        ]
        output = year[year["positive_output"] & year["positive_throughput"]]
        valid = year[year["engineering_output_valid"]]
        output_throughput = float(output["throughput_t_year"].sum())
        valid_throughput = float(valid["throughput_t_year"].sum())
        valid_generation = float(valid["power_generated_mwh"].sum())
        throughput_coverage = output_throughput / total_throughput
        conditional_intensity = valid_generation / valid_throughput
        valid_coverage = valid_throughput / total_throughput
        fleet_intensity = valid_generation / total_throughput
        rows.append(
            {
                "fiscal_year": int(fiscal_year),
                "facilities": int(len(year)),
                "positive_throughput_facilities": int(len(active)),
                "installed_generation_facilities": int(len(installed)),
                "active_installed_generation_facilities": int(len(active_installed)),
                "positive_output_facilities": int(len(output)),
                "facility_participation_pct": float(len(installed) / len(year) * 100),
                "positive_output_facility_share_pct": float(len(output) / len(year) * 100),
                "active_installed_generation_facility_share_pct": float(
                    len(active_installed) / len(active) * 100
                ),
                "active_positive_output_facility_share_pct": float(
                    len(output) / len(active) * 100
                ),
                "throughput_coverage_pct": float(throughput_coverage * 100),
                "engineering_valid_throughput_coverage_pct": float(valid_coverage * 100),
                "installed_design_capacity_share_pct": float(
                    installed["capacity_t_day"].fillna(0).sum() / total_capacity * 100
                ),
                "total_throughput_t": total_throughput,
                "positive_output_throughput_t": output_throughput,
                "valid_output_throughput_t": valid_throughput,
                "valid_gross_generation_mwh": valid_generation,
                "conditional_valid_gross_mwh_t": conditional_intensity,
                "fleet_valid_gross_mwh_t": fleet_intensity,
                "identity_product_mwh_t": valid_coverage * conditional_intensity,
                "excluded_positive_output_rows": int(
                    (year["positive_output"] & ~year["engineering_output_valid"]).sum()
                ),
            }
        )
    result = pd.DataFrame(rows)
    error = (
        result["fleet_valid_gross_mwh_t"] - result["identity_product_mwh_t"]
    ).abs().max()
    if error > 1e-12:
        raise ValueError(f"Fleet decomposition identity failed: {error}")
    return result


def build_fy2024_segments(panel: pd.DataFrame) -> pd.DataFrame:
    frame = panel[panel["fiscal_year"].eq(2024)].copy()
    positive_throughput = frame["throughput_t_year"].fillna(0).gt(0)
    positive_output = frame["power_generated_mwh"].fillna(0).gt(0)
    installed = frame["has_power_gen"].fillna(False)
    frame["segment"] = np.select(
        [
            positive_throughput & positive_output,
            installed & ~positive_output,
            positive_throughput & ~installed,
        ],
        [
            "Operating generator",
            "Installed capacity without positive output",
            "Operating non-generator",
        ],
        default="No positive throughput or generation",
    )
    total_throughput = float(frame["throughput_t_year"].fillna(0).sum())
    total_capacity = float(frame["capacity_t_day"].fillna(0).sum())
    result = (
        frame.groupby("segment", as_index=False)
        .agg(
            facility_rows=("stable_site_id", "size"),
            stable_sites=("stable_site_id", "nunique"),
            design_capacity_t_day=("capacity_t_day", "sum"),
            throughput_t_year=("throughput_t_year", "sum"),
            gross_generation_mwh=("power_generated_mwh", "sum"),
        )
    )
    result["facility_share_pct"] = result["facility_rows"] / len(frame) * 100
    result["design_capacity_share_pct"] = (
        result["design_capacity_t_day"] / total_capacity * 100
    )
    result["throughput_share_pct"] = result["throughput_t_year"] / total_throughput * 100
    return result


def write_report(annual: pd.DataFrame, segments: pd.DataFrame) -> None:
    fy2024 = annual.loc[annual["fiscal_year"].eq(2024)].iloc[0]
    with open(REPORT_PATH, "w", encoding="utf-8") as handle:
        handle.write("# Fleet Coverage And Conditional Generation Intensity\n\n")
        handle.write(
            "The fleet result is decomposed into the share of recorded waste throughput "
            "handled by facilities with plausible positive generation and the weighted "
            "gross generation intensity within those facilities. This prevents a facility "
            "count from being interpreted as a waste-volume or energy-output share.\n\n"
        )
        handle.write("## FY2024 Headline\n\n")
        handle.write(
            f"- Installed-generation facility participation: "
            f"{fy2024['facility_participation_pct']:.1f}% of all records; "
            f"{fy2024['active_installed_generation_facility_share_pct']:.1f}% "
            "of positive-throughput records\n"
        )
        handle.write(
            f"- Throughput handled by positive-output facilities: "
            f"{fy2024['throughput_coverage_pct']:.1f}%\n"
        )
        handle.write(
            f"- Positive-output facility participation: "
            f"{fy2024['positive_output_facility_share_pct']:.1f}% of all records; "
            f"{fy2024['active_positive_output_facility_share_pct']:.1f}% "
            "of positive-throughput records\n"
        )
        handle.write(
            f"- Waste-processing design capacity at installed-generation facilities: "
            f"{fy2024['installed_design_capacity_share_pct']:.1f}%\n"
        )
        handle.write(
            f"- Engineering-valid throughput coverage: "
            f"{fy2024['engineering_valid_throughput_coverage_pct']:.1f}%\n"
        )
        handle.write(
            f"- Conditional engineering-valid gross intensity: "
            f"{fy2024['conditional_valid_gross_mwh_t']:.3f} MWh/t\n"
        )
        handle.write(
            f"- Engineering-valid fleet gross intensity: "
            f"{fy2024['fleet_valid_gross_mwh_t']:.3f} MWh per total tonne\n\n"
        )
        handle.write("The exact identity is:\n\n")
        handle.write(
            "`fleet gross MWh / total tonnes = valid generator-throughput share "
            "x conditional valid generator MWh/t`.\n\n"
        )
        handle.write("## FY2024 Segments\n\n")
        handle.write(segments.to_markdown(index=False, floatfmt=".1f"))
        handle.write("\n\n## Annual Decomposition\n\n")
        display = annual[
            [
                "fiscal_year",
                "facility_participation_pct",
                "active_installed_generation_facility_share_pct",
                "positive_output_facility_share_pct",
                "active_positive_output_facility_share_pct",
                "throughput_coverage_pct",
                "installed_design_capacity_share_pct",
                "conditional_valid_gross_mwh_t",
                "fleet_valid_gross_mwh_t",
                "excluded_positive_output_rows",
            ]
        ]
        handle.write(display.to_markdown(index=False, floatfmt=".3f"))
        handle.write(
            "\n\nGross generation is an administrative gross-output measure. It is not net "
            "export, useful heat, R1 efficiency, lifecycle benefit, or a causal estimate "
            "of recoverable potential.\n"
        )


def main() -> None:
    panel = load_panel()
    annual = build_annual_decomposition(panel)
    segments = build_fy2024_segments(panel)
    annual.to_csv(ANNUAL_PATH, index=False, float_format="%.10g")
    segments.to_csv(SEGMENT_PATH, index=False, float_format="%.10g")
    write_report(annual, segments)
    fy2024 = annual.loc[annual["fiscal_year"].eq(2024)].iloc[0]
    manifest_path = write_stage_manifest(
        "05_fleet_decomposition",
        inputs=["data/processed/incineration_panel_identified.csv"],
        outputs=[
            "output/fleet_decomposition.csv",
            "output/fy2024_fleet_segments.csv",
            "output/fleet_decomposition.md",
        ],
        metadata={
            "fy2024_facility_participation_pct": float(
                fy2024["facility_participation_pct"]
            ),
            "fy2024_throughput_coverage_pct": float(
                fy2024["throughput_coverage_pct"]
            ),
            "fy2024_active_positive_output_facility_share_pct": float(
                fy2024["active_positive_output_facility_share_pct"]
            ),
            "fy2024_active_installed_generation_facility_share_pct": float(
                fy2024["active_installed_generation_facility_share_pct"]
            ),
            "fy2024_positive_output_facility_share_pct": float(
                fy2024["positive_output_facility_share_pct"]
            ),
            "fy2024_installed_design_capacity_share_pct": float(
                fy2024["installed_design_capacity_share_pct"]
            ),
            "fy2024_conditional_valid_gross_mwh_t": float(
                fy2024["conditional_valid_gross_mwh_t"]
            ),
            "identity_max_absolute_error": float(
                (
                    annual["fleet_valid_gross_mwh_t"]
                    - annual["identity_product_mwh_t"]
                ).abs().max()
            ),
        },
    )
    print(f"Saved: {ANNUAL_PATH}")
    print(f"Saved: {SEGMENT_PATH}")
    print(f"Saved: {REPORT_PATH}")
    print(f"Manifest: {manifest_path}")


if __name__ == "__main__":
    main()
