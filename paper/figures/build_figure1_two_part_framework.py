#!/usr/bin/env python3
"""Plot facility-, throughput-, and capacity-weighted fleet coverage."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
FIGURE_DIR = Path(__file__).resolve().parent
DATA_PATH = ROOT / "output" / "fleet_decomposition.csv"
PNG_OUT = FIGURE_DIR / "figure1_two_part_framework.png"
PDF_OUT = FIGURE_DIR / "figure1_two_part_framework.pdf"

INK = "#20262d"
MUTED = "#59636e"
GRID = "#d9dee3"
BLUE = "#0072b2"
ORANGE = "#d55e00"
CHARCOAL = "#4b5258"

SERIES = (
    (
        "facility_participation_pct",
        "Facilities",
        BLUE,
        "-",
        "o",
        1.8,
    ),
    (
        "throughput_coverage_pct",
        "Throughput",
        CHARCOAL,
        "-",
        "s",
        1.8,
    ),
    (
        "installed_design_capacity_share_pct",
        "Design capacity",
        ORANGE,
        (0, (4, 2)),
        "^",
        2.3,
    ),
)


def style_axes(ax: plt.Axes) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(MUTED)
    ax.spines["bottom"].set_color(MUTED)
    ax.tick_params(colors=INK, labelsize=8.0, length=3)
    ax.grid(axis="y", color=GRID, linewidth=0.65)
    ax.set_axisbelow(True)


def load_data() -> pd.DataFrame:
    if not DATA_PATH.exists():
        raise SystemExit("Run the fleet decomposition analysis before Figure 1.")
    data = pd.read_csv(DATA_PATH)
    required = {"fiscal_year", *(item[0] for item in SERIES)}
    missing = required.difference(data.columns)
    if missing:
        raise ValueError(f"Figure 1 input is missing columns: {sorted(missing)}")
    data = data.sort_values("fiscal_year").copy()
    if data["fiscal_year"].duplicated().any():
        raise ValueError("Figure 1 requires one row per fiscal year.")
    if data["fiscal_year"].tolist() != list(range(2005, 2025)):
        raise ValueError("Figure 1 expects complete FY2005-FY2024 coverage.")
    for column, *_ in SERIES:
        if not data[column].between(0, 100).all():
            raise ValueError(f"{column} contains values outside 0-100 percent.")
    return data


def build() -> None:
    data = load_data()
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 8.3,
            "axes.labelcolor": INK,
            "text.color": INK,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )

    fig, ax = plt.subplots(figsize=(3.7, 3.25), dpi=200)
    style_axes(ax)

    years = data["fiscal_year"]
    for column, label, color, linestyle, marker, label_offset in SERIES:
        values = data[column]
        ax.plot(
            years,
            values,
            color=color,
            linestyle=linestyle,
            linewidth=1.55,
            marker=marker,
            markevery=[0, 5, 10, 15, 19],
            markersize=3.6,
            markerfacecolor="white",
            markeredgecolor=color,
            markeredgewidth=1.0,
            zorder=3,
        )
        final = float(values.iloc[-1])
        ax.text(
            2023.65,
            final + label_offset,
            f"{label} {final:.1f}%",
            color=color,
            fontsize=7.7,
            fontweight="semibold",
            ha="right",
            va="center",
            clip_on=False,
            bbox={"facecolor": "white", "edgecolor": "none", "pad": 0.5, "alpha": 0.9},
        )

    ax.set_title(
        "Fleet coverage differs by denominator",
        loc="left",
        fontsize=9.6,
        fontweight="semibold",
        pad=15,
    )
    ax.text(
        0,
        1.015,
        "Municipal incinerators, FY2005-FY2024",
        transform=ax.transAxes,
        color=MUTED,
        fontsize=7.5,
        va="bottom",
    )
    ax.set_xlabel("Fiscal year", fontsize=8.2)
    ax.set_ylabel("Share of fleet total (%)", fontsize=8.2)
    ax.set_xlim(2005, 2024.8)
    ax.set_ylim(0, 100)
    ax.set_xticks([2005, 2010, 2015, 2020, 2024])
    ax.set_yticks([0, 20, 40, 60, 80, 100])

    fig.subplots_adjust(left=0.16, right=0.98, top=0.82, bottom=0.16)
    fig.savefig(PNG_OUT, dpi=300, facecolor="white")
    fig.savefig(PDF_OUT, facecolor="white", bbox_inches=None)
    plt.close(fig)


if __name__ == "__main__":
    build()
