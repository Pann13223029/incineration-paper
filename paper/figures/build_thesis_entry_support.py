#!/usr/bin/env python3
"""Plot support-aware absolute risks for the professor-facing thesis."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
FIGURE_DIR = Path(__file__).resolve().parent
DATA_PATH = ROOT / "output" / "entry_capacity_support.csv"
PNG_OUT = FIGURE_DIR / "thesis_entry_support.png"
PDF_OUT = FIGURE_DIR / "thesis_entry_support.pdf"

INK = "#1a1a1a"
MUTED = "#555555"
LIGHT = "#777777"
GRID = "#d2d2d2"


def load_data() -> pd.DataFrame:
    if not DATA_PATH.exists():
        raise SystemExit("Run the entry-capacity support analysis before this figure.")
    data = pd.read_csv(DATA_PATH)
    required = {
        "capacity_t_day",
        "empirical_percentile_pct",
        "risk_rows_at_or_above",
        "modeled_events_at_or_above",
        "standardized_events_per_1000",
        "bootstrap_ci_low_per_1000",
        "bootstrap_ci_high_per_1000",
    }
    missing = required.difference(data.columns)
    if missing:
        raise ValueError(f"Entry-support input is missing columns: {sorted(missing)}")
    if set(data["capacity_t_day"]) != {24, 60, 100, 120, 300}:
        raise ValueError("Entry-support figure requires the five frozen capacities.")
    numeric = list(required)
    if not np.isfinite(data[numeric].to_numpy()).all():
        raise ValueError("Entry-support figure contains non-finite values.")
    return data.sort_values("capacity_t_day")


def style_axes(ax: plt.Axes) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(INK)
    ax.spines["bottom"].set_color(INK)
    ax.spines["left"].set_linewidth(0.7)
    ax.spines["bottom"].set_linewidth(0.7)
    ax.tick_params(colors=INK, labelsize=7.4, length=3)
    ax.grid(axis="y", color=GRID, linewidth=0.65)
    ax.set_axisbelow(True)


def draw_points(
    ax: plt.Axes, data: pd.DataFrame, color: str, marker: str = "o"
) -> None:
    estimates = data["standardized_events_per_1000"].to_numpy(float)
    lows = data["bootstrap_ci_low_per_1000"].to_numpy(float)
    highs = data["bootstrap_ci_high_per_1000"].to_numpy(float)
    ax.errorbar(
        data["capacity_t_day"],
        estimates,
        yerr=np.vstack([estimates - lows, highs - estimates]),
        fmt=marker,
        color=color,
        ecolor=color,
        markerfacecolor="white",
        markeredgewidth=1.0,
        markersize=4.6,
        elinewidth=1.0,
        capsize=2.2,
        zorder=3,
    )


def build() -> None:
    data = load_data()
    supported = data[data["capacity_t_day"].le(120)]
    tail = data[data["capacity_t_day"].eq(300)]

    plt.rcParams.update(
        {
            "font.family": "DejaVu Serif",
            "font.size": 8.2,
            "axes.labelcolor": INK,
            "text.color": INK,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )
    fig, axes = plt.subplots(
        1,
        2,
        figsize=(4.9, 2.8),
        dpi=200,
        gridspec_kw={"width_ratios": [2.35, 1.2]},
    )
    main_ax, tail_ax = axes
    for ax in axes:
        style_axes(ax)

    draw_points(main_ax, supported, INK)
    main_ax.set_xlim(15, 129)
    main_ax.set_ylim(0, 5.0)
    main_ax.set_xticks([24, 60, 100, 120])
    main_ax.set_yticks([0, 1, 2, 3, 4, 5])
    main_ax.set_title(
        "A. Support-rich range", loc="left", fontsize=8.2,
        fontweight="bold", pad=5
    )
    main_ax.set_ylabel("Annual entries per 1,000 facility-years")
    main_ax.set_xlabel("Prior processing capacity (t/day)", fontsize=7.6)
    for row in supported.itertuples(index=False):
        main_ax.annotate(
            f"{row.standardized_events_per_1000:.2f}",
            (row.capacity_t_day, row.bootstrap_ci_high_per_1000),
            xytext=(0, 5),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=6.4,
            color=INK,
        )

    draw_points(tail_ax, tail, LIGHT, marker="s")
    tail_ax.set_xlim(285, 315)
    tail_ax.set_ylim(0, 35)
    tail_ax.set_xticks([300])
    tail_ax.set_yticks([0, 10, 20, 30])
    tail_ax.set_title(
        "B. Sparse tail", loc="left", fontsize=8.2,
        fontweight="bold", pad=5
    )
    tail_ax.set_xlabel("Capacity (t/day)", fontsize=7.6)
    tail_row = tail.iloc[0]
    tail_ax.annotate(
        f"{tail_row['standardized_events_per_1000']:.2f}",
        (tail_row["capacity_t_day"], tail_row["standardized_events_per_1000"]),
        xytext=(8, 0),
        textcoords="offset points",
        ha="left",
        va="center",
        fontsize=6.5,
        color=INK,
    )
    fig.subplots_adjust(left=0.14, right=0.97, top=0.90, bottom=0.22, wspace=0.42)
    fig.savefig(PNG_OUT, dpi=300, facecolor="white")
    fig.savefig(PDF_OUT, facecolor="white", bbox_inches=None)
    plt.close(fig)


if __name__ == "__main__":
    build()
