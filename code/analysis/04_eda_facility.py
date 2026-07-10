"""Descriptive audit for the stable-lineage and generator-component frames."""

from __future__ import annotations

import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from panel_utils import (
    OUTPUT_DIR,
    build_operating_power_frame,
    build_regression_frame,
    load_panel,
    sample_summary,
    write_stage_manifest,
)


PANEL_REPORT = os.path.join(OUTPUT_DIR, "panel_summary.md")
DECISION_REPORT = os.path.join(OUTPUT_DIR, "pre_regression_decision.md")
FIGURE_1 = os.path.join(OUTPUT_DIR, "fig01_establishing_shot.png")
FIGURE_2 = os.path.join(OUTPUT_DIR, "fig02_heterogeneity_shot.png")


def annual_summary(panel: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for year, group in panel.groupby("fiscal_year", sort=True):
        throughput = group["throughput_t_year"].fillna(0)
        positive_output = group["power_generated_mwh"].fillna(0).gt(0)
        rows.append(
            {
                "fiscal_year": int(year),
                "facility_rows": int(len(group)),
                "installed_capacity_share_pct": float(
                    group["has_power_gen"].fillna(False).mean() * 100
                ),
                "positive_output_throughput_share_pct": float(
                    throughput[positive_output].sum() / throughput.sum() * 100
                ),
            }
        )
    return pd.DataFrame(rows)


def save_figures(panel: pd.DataFrame, regression: pd.DataFrame) -> None:
    annual = annual_summary(panel)
    plt.style.use("seaborn-v0_8-whitegrid")

    fig, axis = plt.subplots(figsize=(7.2, 4.2))
    axis.plot(
        annual["fiscal_year"],
        annual["installed_capacity_share_pct"],
        marker="o",
        linewidth=1.7,
        label="Facilities with installed generation capacity",
    )
    axis.plot(
        annual["fiscal_year"],
        annual["positive_output_throughput_share_pct"],
        marker="s",
        linewidth=1.7,
        label="Throughput at facilities reporting positive output",
    )
    axis.set(xlabel="Fiscal year", ylabel="Share (%)", ylim=(0, 100))
    axis.legend(frameon=False, loc="lower right")
    fig.tight_layout()
    fig.savefig(FIGURE_1, dpi=180)
    plt.close(fig)

    fig, axis = plt.subplots(figsize=(7.2, 4.2))
    sample = regression.sample(min(2500, len(regression)), random_state=20260710)
    colors = np.log10(sample["power_capacity_kw"])
    points = axis.scatter(
        sample["generator_design_intensity_kw_per_t_day"],
        sample["electrical_capacity_factor"],
        c=colors,
        cmap="viridis",
        alpha=0.38,
        s=12,
        linewidths=0,
    )
    colorbar = fig.colorbar(points, ax=axis)
    colorbar.set_label("log10 installed electrical capacity (kW)")
    axis.set(
        xlabel="Generator design intensity (kW per t/day)",
        ylabel="Electrical capacity factor",
    )
    fig.tight_layout()
    fig.savefig(FIGURE_2, dpi=180)
    plt.close(fig)


def main() -> None:
    panel = load_panel()
    operating = build_operating_power_frame(panel)
    regression = build_regression_frame(panel)
    summary = sample_summary(panel)
    annual = annual_summary(panel)

    invalid = operating.loc[~operating["engineering_valid"]]
    with open(PANEL_REPORT, "w", encoding="utf-8") as handle:
        handle.write("# Stable-Lineage Panel Summary\n\n")
        handle.write(
            "The descriptive frame uses audited stable administrative facility "
            "lineages rather than official facility codes as longitudinal identifiers. "
            "Exact duplicate source records are collapsed before analysis.\n\n"
        )
        handle.write(f"- Facility-year records: {len(panel):,}\n")
        handle.write(
            f"- Stable administrative lineages: "
            f"{summary['stable_full_fleet_sites']:,}\n"
        )
        handle.write(f"- Asset episodes: {summary['asset_episodes']:,}\n")
        handle.write(
            f"- Operating positive-output rows: {len(operating):,} across "
            f"{operating['analysis_facility_id'].nunique():,} lineages\n"
        )
        handle.write(
            f"- Engineering-valid generator rows: {len(regression):,} across "
            f"{regression['analysis_facility_id'].nunique():,} lineages\n"
        )
        handle.write(f"- Engineering-invalid positive-output rows: {len(invalid):,}\n")
        handle.write(
            f"- Negative reported-age rows retained in source but excluded from "
            f"age-dependent models: {int(panel['facility_age'].lt(0).sum()):,}\n\n"
        )
        handle.write("## Annual Count And Throughput Coverage\n\n")
        handle.write(annual.to_markdown(index=False, floatfmt=".2f"))
        handle.write(
            "\n\nFacility participation and throughput coverage have different "
            "denominators and must not be interpreted as interchangeable fleet shares.\n"
        )

    with open(DECISION_REPORT, "w", encoding="utf-8") as handle:
        handle.write("# Pre-Model Decision: Separate Generator Design From Operation\n\n")
        handle.write(
            "Gross annual generation per tonne combines installed electrical sizing, "
            "electrical capacity factor, and waste-processing utilization. It is not an "
            "independent measure of operating efficiency. The primary generator analysis "
            "therefore models log generator design intensity and log electrical capacity "
            "factor separately, with stable-lineage-clustered uncertainty. Gross MWh/t is "
            "retained as a transparent accounting outcome and specification diagnostic.\n\n"
        )
        handle.write(
            "Reported start-year cohorts are administrative design-vintage markers, not "
            "verified boiler or turbine installation dates. Within-lineage checks answer "
            "a narrower operational question and do not identify causal aging effects.\n"
        )

    save_figures(panel, regression)
    manifest = write_stage_manifest(
        "04_eda_facility",
        inputs=["data/processed/incineration_panel_identified.csv"],
        outputs=[
            "output/panel_summary.md",
            "output/pre_regression_decision.md",
        ],
        metadata={
            "panel_rows": int(len(panel)),
            "stable_lineages": int(panel["stable_site_id"].nunique()),
            "asset_episodes": int(panel["asset_episode_id"].nunique()),
            "operating_generator_rows": int(len(operating)),
            "engineering_valid_rows": int(len(regression)),
        },
    )
    print(f"Saved: {PANEL_REPORT}")
    print(f"Saved: {DECISION_REPORT}")
    print(f"Manifest: {manifest}")


if __name__ == "__main__":
    main()
