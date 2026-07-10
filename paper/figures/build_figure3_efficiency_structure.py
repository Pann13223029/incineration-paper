#!/usr/bin/env python3
"""Generate Figure 3 from canonical generator-performance output."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
FIGURE_DIR = Path(__file__).resolve().parent
DATA_PATH = ROOT / "output" / "figure3_persistence.csv"
PNG_OUT = FIGURE_DIR / "figure3_efficiency_structure.png"
PDF_OUT = FIGURE_DIR / "figure3_efficiency_structure.pdf"


def style_axes(ax, grid_axis: str = "y") -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#66727f")
    ax.spines["bottom"].set_color("#66727f")
    ax.tick_params(colors="#33414d", labelsize=9.2)
    ax.grid(axis=grid_axis, color="#dce3ea", linewidth=0.8)
    ax.set_axisbelow(True)


def build() -> None:
    if not DATA_PATH.exists():
        raise SystemExit("Run the generator regression analysis before building Figure 3.")
    data = pd.read_csv(DATA_PATH)
    age = data[data["record_type"].eq("age_mean")].copy()
    rank = data[data["record_type"].eq("rank_correlation")].copy()

    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "axes.titlesize": 11.5,
            "axes.titleweight": "bold",
            "axes.labelsize": 10.5,
        }
    )
    fig, (ax1, ax2) = plt.subplots(
        1,
        2,
        figsize=(10.8, 4.5),
        dpi=200,
        gridspec_kw={"width_ratios": [0.9, 1.25]},
    )

    style_axes(ax1)
    x_age = np.arange(len(age))
    yerr = np.vstack(
        [age["value"] - age["ci_low"], age["ci_high"] - age["value"]]
    )
    ax1.errorbar(
        x_age,
        age["value"],
        yerr=yerr,
        fmt="o",
        color="#35689a",
        ecolor="#35689a",
        markerfacecolor="white",
        markeredgewidth=1.8,
        markersize=8,
        capsize=4,
        linewidth=1.6,
    )
    for x_value, mean in zip(x_age, age["value"]):
        ax1.text(
            x_value,
            mean + 0.028,
            f"{mean:.3f}",
            ha="center",
            fontsize=8.7,
            color="#263440",
            fontweight="bold",
        )
    ax1.set_title(
        "A. Mean gross electricity per tonne",
        loc="left",
        color="#22313f",
        pad=16,
    )
    ax1.text(
        0,
        1.015,
        "Facility-clustered 95% confidence intervals",
        transform=ax1.transAxes,
        fontsize=8.5,
        color="#53616d",
        va="bottom",
    )
    ax1.set_ylabel("Bounded MWh per tonne")
    ax1.set_xticks(x_age, [label.replace(" yrs", "") for label in age["label"]])
    ax1.set_xlabel("Generator age group (years)")
    ax1.set_ylim(0, 0.47)

    style_axes(ax2)
    x_rank = np.arange(len(rank))
    ax2.scatter(
        x_rank,
        rank["value"],
        marker="s",
        s=38,
        facecolors="white",
        edgecolors="#a35f2d",
        linewidths=1.5,
        zorder=3,
    )
    median_corr = float(rank["value"].median())
    ax2.axhline(
        median_corr,
        color="#263440",
        linestyle="--",
        linewidth=1.0,
        label=f"Median annual = {median_corr:.3f}",
    )
    ax2.set_title(
        "B. Adjacent-year facility rank persistence",
        loc="left",
        color="#22313f",
        pad=16,
    )
    ax2.text(
        0,
        1.015,
        "Spearman rank correlation; focused vertical scale",
        transform=ax2.transAxes,
        fontsize=8.5,
        color="#53616d",
        va="bottom",
    )
    ax2.set_ylabel("Rank correlation")
    period_labels = [
        f"{str(int(start))[-2:]}-{str(int(end))[-2:]}"
        for start, end in zip(rank["year_start"], rank["year_end"])
    ]
    ax2.set_xticks(x_rank, period_labels, rotation=45, ha="right")
    ax2.set_xlabel("Fiscal-year pair")
    ax2.set_ylim(0.84, 1.0)
    ax2.legend(frameon=False, fontsize=8.5, loc="lower right")

    fig.tight_layout(w_pad=2.4)
    fig.savefig(PNG_OUT, dpi=300, bbox_inches="tight", facecolor="white")
    fig.savefig(PDF_OUT, bbox_inches="tight", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    build()
