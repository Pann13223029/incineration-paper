#!/usr/bin/env python3
"""Plot independent cohort models and accounting reconciliation for the thesis."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
FIGURE_DIR = Path(__file__).resolve().parent
CONTRAST_PATH = ROOT / "output" / "figure3_adjusted_components.csv"
DECOMPOSITION_PATH = ROOT / "output" / "common_control_component_decomposition.csv"
PNG_OUT = FIGURE_DIR / "thesis_cohort_components.png"
PDF_OUT = FIGURE_DIR / "thesis_cohort_components.pdf"

INK = "#1a1a1a"
MUTED = "#555555"
MID = "#6f6f6f"
LIGHT = "#999999"
GRID = "#d2d2d2"

COHORT_ORDER = ("Before 1990", "1990-1999", "2000-2009", "2010 or later")
COHORT_LABELS = ("Before 1990", "1990-1999", "2000-2009", "2010 or later\n(reference)")
DECOMPOSITION_ORDER = ("Before 1990", "1990-1999", "2000-2009")


def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    if not CONTRAST_PATH.exists() or not DECOMPOSITION_PATH.exists():
        raise SystemExit("Run the component analysis before the thesis cohort figure.")
    contrasts = pd.read_csv(CONTRAST_PATH)
    decomposition = pd.read_csv(DECOMPOSITION_PATH)
    contrast_cols = {
        "component", "cohort", "percent_difference", "ci_low_percent",
        "ci_high_percent",
    }
    decomposition_cols = {
        "sample", "cohort", "log_design_component",
        "log_capacity_factor_component", "negative_log_utilization_component",
        "direct_log_gross_intensity_difference", "identity_error",
    }
    if contrast_cols.difference(contrasts.columns):
        raise ValueError("Cohort-contrast input is incomplete.")
    if decomposition_cols.difference(decomposition.columns):
        raise ValueError("Common-control decomposition input is incomplete.")
    decomposition = decomposition[decomposition["sample"].eq("Primary engineering frame")]
    if len(decomposition) != 3:
        raise ValueError("Expected three primary common-control cohort rows.")
    if decomposition["identity_error"].abs().max() > 1e-10:
        raise ValueError("Component identity does not reconcile within tolerance.")
    return contrasts, decomposition


def style_contrast_axis(ax: plt.Axes) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color(INK)
    ax.spines["bottom"].set_linewidth(0.7)
    ax.tick_params(axis="x", colors=INK, labelsize=7.1, length=3)
    ax.tick_params(axis="y", colors=INK, labelsize=7.4, length=0, pad=5)
    ax.grid(axis="x", color=GRID, linewidth=0.65)
    ax.axvline(0, color=INK, linewidth=0.9, linestyle=(0, (3, 2)))
    ax.set_axisbelow(True)


def contrast_panel(
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
    style_contrast_axis(ax)
    ax.errorbar(
        estimates,
        y,
        xerr=np.vstack([estimates - lows, highs - estimates]),
        fmt=marker,
        color=color,
        ecolor=color,
        markerfacecolor="white",
        markeredgewidth=1.0,
        markersize=4.5,
        elinewidth=1.0,
        capsize=2.1,
        zorder=3,
    )
    ax.set_yticks(y, COHORT_LABELS)
    ax.set_xlim(*xlim)
    ax.set_xticks(ticks)
    ax.set_title(title, loc="left", fontsize=8.2, fontweight="bold", pad=5)
    ax.set_xlabel("Adjusted difference from 2010-or-later cohort (%)", fontsize=7.3)


def decomposition_panel(ax: plt.Axes, data: pd.DataFrame) -> None:
    subset = data.set_index("cohort").loc[list(DECOMPOSITION_ORDER)]
    y = np.arange(len(DECOMPOSITION_ORDER) - 1, -1, -1, dtype=float)
    columns = (
        ("log_design_component", "Generator design", INK, "o", -0.18),
        ("log_capacity_factor_component", "Capacity factor", MID, "s", 0.0),
        ("negative_log_utilization_component", "Waste loading", LIGHT, "^", 0.18),
    )
    style_contrast_axis(ax)
    for column, label, color, marker, offset in columns:
        ax.scatter(
            subset[column].to_numpy(float),
            y + offset,
            s=21,
            marker=marker,
            facecolors="white",
            edgecolors=color,
            linewidths=1.0,
            label=label,
            zorder=3,
        )
    direct = subset["direct_log_gross_intensity_difference"].to_numpy(float)
    ax.scatter(
        direct,
        y,
        s=24,
        marker="|",
        color=INK,
        linewidths=1.4,
        label="Direct log gap",
        zorder=4,
    )
    ax.set_yticks(y, DECOMPOSITION_ORDER)
    ax.set_xlim(-1.75, 0.45)
    ax.set_xticks([-1.5, -1.0, -0.5, 0.0])
    ax.set_title(
        "C. Common-control component accounting",
        loc="left",
        fontsize=8.2,
        fontweight="bold",
        pad=5,
    )
    ax.set_xlabel("Log difference from 2010-or-later cohort", fontsize=7.3)


def build() -> None:
    contrasts, decomposition = load_data()
    plt.rcParams.update(
        {
            "font.family": "DejaVu Serif",
            "font.size": 8.0,
            "axes.labelcolor": INK,
            "text.color": INK,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )
    fig, axes = plt.subplots(3, 1, figsize=(4.5, 5.75), dpi=200)
    contrast_panel(
        axes[0], contrasts, "Installed electrical capacity", INK, "o",
        "A. Installed electrical capacity", (-90, 10),
        [-80, -60, -40, -20, 0],
    )
    contrast_panel(
        axes[1], contrasts, "Electrical capacity factor", MID, "s",
        "B. Annual electrical capacity factor", (-15, 55),
        [-10, 0, 10, 20, 30, 40, 50],
    )
    decomposition_panel(axes[2], decomposition)

    handles, labels = axes[2].get_legend_handles_labels()
    fig.legend(
        handles,
        labels,
        loc="lower center",
        bbox_to_anchor=(0.62, 0.035),
        ncol=2,
        frameon=False,
        fontsize=6.5,
        handletextpad=0.35,
        columnspacing=0.8,
        borderaxespad=0,
    )
    fig.subplots_adjust(left=0.34, right=0.97, top=0.93, bottom=0.14, hspace=0.72)
    fig.savefig(PNG_OUT, dpi=300, facecolor="white")
    fig.savefig(PDF_OUT, facecolor="white", bbox_inches=None)
    plt.close(fig)


if __name__ == "__main__":
    build()
