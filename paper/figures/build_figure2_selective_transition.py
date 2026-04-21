#!/usr/bin/env python3
"""Generate a formal Figure 2 for the paper manuscript."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parent
PNG_OUT = ROOT / "figure2_selective_transition.png"
PDF_OUT = ROOT / "figure2_selective_transition.pdf"


AGE_LABELS = ["0-10", "10-20", "20-30", "30+"]
AGE_RATES = np.array([5.94, 0.35, 0.34, 0.27])

CAPACITY_LABELS = ["Q1", "Q2", "Q3", "Q4"]
CAPACITY_RATES = np.array([0.03, 0.08, 1.16, 3.11])

EFFECT_LABELS = [
    "Age 10-20 vs 0-10",
    "Age 20-30 vs 0-10",
    "Age 30+ vs 0-10",
    "Capacity per 100 t/day",
]
EFFECTS = np.array([-1.76, -1.72, -1.13, 0.50])
EFFECT_SE = np.array([0.28, 0.42, 0.39, 0.20])


def style_axes(ax) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#66727f")
    ax.spines["bottom"].set_color("#66727f")
    ax.tick_params(colors="#33414d", labelsize=10.5)
    ax.grid(axis="y", color="#dce3ea", linewidth=0.8)
    ax.set_axisbelow(True)


def build() -> None:
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "axes.titlesize": 12.5,
            "axes.titleweight": "bold",
            "axes.labelsize": 11,
        }
    )

    fig = plt.figure(figsize=(10.6, 6.6), dpi=200, constrained_layout=True)
    gs = fig.add_gridspec(2, 2, height_ratios=[1.0, 1.05], width_ratios=[1.0, 1.0])

    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[1, :])

    style_axes(ax1)
    age_colors = ["#3f6ea8", "#91a7c2", "#91a7c2", "#91a7c2"]
    bars1 = ax1.bar(AGE_LABELS, AGE_RATES, color=age_colors, edgecolor="#4a5763", linewidth=0.6)
    ax1.set_title("A. Event rate by age band", loc="left", color="#22313f")
    ax1.set_ylabel("Percent")
    ax1.set_ylim(0, 6.5)
    for rect, value in zip(bars1, AGE_RATES):
        ax1.text(
            rect.get_x() + rect.get_width() / 2,
            rect.get_height() + 0.12,
            f"{value:.2f}",
            ha="center",
            va="bottom",
            fontsize=10,
            color="#22313f",
            fontweight="bold",
        )

    style_axes(ax2)
    cap_colors = ["#c7d6e6", "#adc3dc", "#6f98c9", "#3f6ea8"]
    bars2 = ax2.bar(CAPACITY_LABELS, CAPACITY_RATES, color=cap_colors, edgecolor="#4a5763", linewidth=0.6)
    ax2.set_title("B. Event rate by capacity quartile", loc="left", color="#22313f")
    ax2.set_ylabel("Percent")
    ax2.set_ylim(0, 3.5)
    for rect, value in zip(bars2, CAPACITY_RATES):
        ax2.text(
            rect.get_x() + rect.get_width() / 2,
            rect.get_height() + 0.07,
            f"{value:.2f}",
            ha="center",
            va="bottom",
            fontsize=10,
            color="#22313f",
            fontweight="bold",
        )

    ax3.axvline(0, color="#66727f", linewidth=1)
    y_positions = np.arange(len(EFFECT_LABELS))
    effect_colors = ["#9b654a", "#9b654a", "#b1846d", "#3f6ea8"]
    ax3.errorbar(
        EFFECTS,
        y_positions,
        xerr=EFFECT_SE,
        fmt="none",
        ecolor="#7b8792",
        elinewidth=1.1,
        capsize=3,
        zorder=1,
    )
    ax3.scatter(EFFECTS, y_positions, s=55, c=effect_colors, zorder=2)
    ax3.set_yticks(y_positions, EFFECT_LABELS)
    ax3.invert_yaxis()
    ax3.set_title("C. Main hazard model effects", loc="left", color="#22313f")
    ax3.set_xlabel("Average marginal effect (pp)")
    ax3.grid(axis="x", color="#dce3ea", linewidth=0.8)
    ax3.set_axisbelow(True)
    ax3.spines["top"].set_visible(False)
    ax3.spines["right"].set_visible(False)
    ax3.spines["left"].set_visible(False)
    ax3.spines["bottom"].set_color("#66727f")
    ax3.tick_params(colors="#33414d", labelsize=10.8)
    ax3.set_xlim(-2.35, 0.8)
    for x, y in zip(EFFECTS, y_positions):
        offset = 0.11 if x >= 0 else -0.11
        ha = "left" if x >= 0 else "right"
        ax3.text(
            x + offset,
            y,
            f"{x:+.2f}",
            va="center",
            ha=ha,
            fontsize=10.5,
            fontweight="bold",
            color="#22313f",
        )

    fig.savefig(PNG_OUT, dpi=300, bbox_inches="tight")
    fig.savefig(PDF_OUT, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    build()
