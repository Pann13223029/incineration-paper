#!/usr/bin/env python3
"""Generate a formal Figure 3 for the paper manuscript."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parent
PNG_OUT = ROOT / "figure3_efficiency_structure.png"
PDF_OUT = ROOT / "figure3_efficiency_structure.pdf"


AGE_LABELS = ["0-10", "10-20", "20-30", "30+"]
AGE_EFF = np.array([0.400, 0.338, 0.272, 0.183])

VAR_LABELS = ["Full sample", "Pre-2011", "Post-2011"]
VAR_VALUES = np.array([0.1499, 0.1795, 0.0956])


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
        }
    )

    fig, (ax1, ax2) = plt.subplots(
        1,
        2,
        figsize=(10.8, 4.2),
        dpi=200,
        constrained_layout=True,
        gridspec_kw={"width_ratios": [1.05, 0.95]},
    )

    style_axes(ax1)
    ax1.set_title("A. Mean efficiency by generator age group", loc="left", color="#22313f")
    ax1.set_ylabel("Winsorized MWh per tonne")
    x_age = np.arange(len(AGE_LABELS))
    colors_age = ["#345d94", "#5f84b8", "#88a8cf", "#b7cae1"]
    bars1 = ax1.bar(x_age, AGE_EFF, color=colors_age, edgecolor="#4a5763", linewidth=0.6, width=0.62)
    ax1.set_xticks(x_age, AGE_LABELS)
    ax1.set_ylim(0, 0.46)
    for rect, value in zip(bars1, AGE_EFF):
        ax1.text(
            rect.get_x() + rect.get_width() / 2,
            rect.get_height() + 0.012,
            f"{value:.3f}",
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold",
            color="#22313f",
        )

    style_axes(ax2)
    ax2.set_title("B. Within-to-total variance ratio", loc="left", color="#22313f")
    ax2.set_ylabel("Ratio")
    x_var = np.arange(len(VAR_LABELS))
    colors_var = ["#7a67c7", "#5c4ab3", "#a899e0"]
    bars2 = ax2.bar(x_var, VAR_VALUES, color=colors_var, edgecolor="#4a5763", linewidth=0.6, width=0.62)
    ax2.set_xticks(x_var, VAR_LABELS)
    ax2.set_ylim(0, 0.22)
    for rect, value in zip(bars2, VAR_VALUES):
        ax2.text(
            rect.get_x() + rect.get_width() / 2,
            rect.get_height() + 0.008,
            f"{value:.4f}",
            ha="center",
            va="bottom",
            fontsize=10,
            fontweight="bold",
            color="#22313f",
        )

    fig.savefig(PNG_OUT, dpi=300, bbox_inches="tight")
    fig.savefig(PDF_OUT, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    build()
