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

    fig = plt.figure(figsize=(9.6, 3.9), dpi=200, constrained_layout=True)
    gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.0])

    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])

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

    fig.savefig(PNG_OUT, dpi=300, bbox_inches="tight")
    fig.savefig(PDF_OUT, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    build()
