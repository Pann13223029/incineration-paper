#!/usr/bin/env python3
"""Plot adjusted raw-quantity and operating contrasts by reported cohort."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
FIGURE_DIR = Path(__file__).resolve().parent
DATA_PATH = ROOT / "output" / "figure3_adjusted_components.csv"
PNG_OUT = FIGURE_DIR / "figure3_efficiency_structure.png"
PDF_OUT = FIGURE_DIR / "figure3_efficiency_structure.pdf"

INK = "#20262d"
MUTED = "#59636e"
GRID = "#d9dee3"
BLUE = "#0072b2"
ORANGE = "#d55e00"

COHORT_ORDER = ("Before 1990", "1990-1999", "2000-2009", "2010 or later")
COHORT_LABELS = ("Before 1990", "1990-1999", "2000-2009", "2010 or later\n(reference)")


def load_data() -> pd.DataFrame:
    if not DATA_PATH.exists():
        raise SystemExit("Run the scientific-revision analysis before Figure 3.")
    data = pd.read_csv(DATA_PATH)
    required = {
        "component",
        "cohort",
        "percent_difference",
        "ci_low_percent",
        "ci_high_percent",
        "reference",
    }
    missing = required.difference(data.columns)
    if missing:
        raise ValueError(f"Figure 3 input is missing columns: {sorted(missing)}")
    expected_components = {
        "Installed electrical capacity",
        "Electrical capacity factor",
    }
    if set(data["component"]) != expected_components:
        raise ValueError("Figure 3 has unexpected components")
    if not np.isfinite(
        data[["percent_difference", "ci_low_percent", "ci_high_percent"]]
    ).all().all():
        raise ValueError("Figure 3 contains non-finite contrasts")
    return data


def style_axes(ax: plt.Axes) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color(MUTED)
    ax.tick_params(axis="x", colors=INK, labelsize=7.4, length=3)
    ax.tick_params(axis="y", colors=INK, labelsize=7.7, length=0, pad=5)
    ax.grid(axis="x", color=GRID, linewidth=0.65)
    ax.axvline(0, color=INK, linewidth=0.9, linestyle=(0, (3, 2)))
    ax.set_axisbelow(True)


def panel(
    ax: plt.Axes,
    data: pd.DataFrame,
    component: str,
    color: str,
    marker: str,
    title: str,
    xlim: tuple[float, float],
    ticks: list[int],
) -> None:
    subset = data[data["component"].eq(component)].set_index("cohort").loc[
        list(COHORT_ORDER)
    ]
    y = np.arange(len(COHORT_ORDER) - 1, -1, -1, dtype=float)
    estimates = subset["percent_difference"].to_numpy(float)
    lows = subset["ci_low_percent"].to_numpy(float)
    highs = subset["ci_high_percent"].to_numpy(float)
    style_axes(ax)
    ax.errorbar(
        estimates,
        y,
        xerr=np.vstack([estimates - lows, highs - estimates]),
        fmt=marker,
        color=color,
        ecolor=color,
        markerfacecolor="white",
        markeredgewidth=1.25,
        markersize=5.0,
        elinewidth=1.25,
        capsize=2.4,
        zorder=3,
    )
    ax.set_yticks(y, COHORT_LABELS)
    ax.set_xlim(*xlim)
    ax.set_xticks(ticks)
    ax.set_title(title, loc="left", fontsize=8.7, fontweight="semibold", pad=6)
    ax.set_xlabel("Adjusted difference from 2010-or-later cohort (%)", fontsize=7.6)


def build() -> None:
    data = load_data()
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 8.2,
            "axes.labelcolor": INK,
            "text.color": INK,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )
    fig, axes = plt.subplots(2, 1, figsize=(4.0, 4.75), dpi=200)
    panel(
        axes[0],
        data,
        "Installed electrical capacity",
        BLUE,
        "o",
        "A. Installed capacity (raw kW model)",
        (-90, 10),
        [-80, -60, -40, -20, 0],
    )
    panel(
        axes[1],
        data,
        "Electrical capacity factor",
        ORANGE,
        "s",
        "B. Annual electrical capacity factor",
        (-15, 55),
        [-10, 0, 10, 20, 30, 40, 50],
    )
    fig.suptitle(
        "Adjusted cohort contrasts",
        x=0.08,
        y=0.985,
        ha="left",
        fontsize=9.3,
        fontweight="semibold",
    )
    fig.text(
        0.08,
        0.945,
        "Installed design versus annual use; clustered 95% confidence intervals",
        color=MUTED,
        fontsize=7.2,
        ha="left",
    )
    fig.text(
        0.08,
        0.025,
        "Models adjust for processing scale, configuration, furnace count, and fiscal year.\n"
        "Capacity-factor estimates also adjust for waste utilization. N=6,511 years / 493\n"
        "lineages. Start year is not an equipment date; contrasts are not causal.",
        color=MUTED,
        fontsize=6.4,
        ha="left",
        linespacing=1.2,
    )
    fig.subplots_adjust(left=0.36, right=0.97, top=0.86, bottom=0.18, hspace=0.62)
    fig.savefig(PNG_OUT, dpi=300, facecolor="white")
    fig.savefig(PDF_OUT, facecolor="white", bbox_inches=None)
    plt.close(fig)


if __name__ == "__main__":
    build()
