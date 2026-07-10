#!/usr/bin/env python3
"""Generate Figure 4 from the post-entry trajectory evidence."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
FIGURE_DIR = Path(__file__).resolve().parent
DATA_PATH = ROOT / "output" / "post_adoption_trajectories.csv"
PNG_OUT = FIGURE_DIR / "figure4_post_entry_trajectories.png"
PDF_OUT = FIGURE_DIR / "figure4_post_entry_trajectories.pdf"


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
        raise SystemExit("Run the adoption analysis before building Figure 4.")
    data = pd.read_csv(DATA_PATH)
    overall = data[data["series"].eq("All entrants")].sort_values("event_time")
    status = data[data["series"].eq("Prior operating status")].copy()

    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "axes.titlesize": 11.5,
            "axes.titleweight": "bold",
            "axes.labelsize": 10.5,
        }
    )
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.8, 4.5), dpi=200)

    style_axes(ax1)
    x = overall["event_time"].to_numpy()
    entrant = overall["mean_mwh_t"].to_numpy()
    entrant_ci = 1.96 * overall["se_mwh_t"].to_numpy()
    incumbent = overall["mean_incumbent_mwh_t"].to_numpy()
    ax1.errorbar(
        x,
        entrant,
        yerr=entrant_ci,
        color="#35689a",
        marker="o",
        markerfacecolor="white",
        markeredgewidth=1.6,
        capsize=3.5,
        linewidth=1.8,
        label="Entrants",
    )
    ax1.plot(
        x,
        incumbent,
        color="#3f4a54",
        linestyle="--",
        marker="s",
        markersize=4.5,
        linewidth=1.4,
        label="Same-year incumbents",
    )
    ax1.set_title(
        "A. Electricity recovery after entry",
        loc="left",
        color="#22313f",
        pad=16,
    )
    ax1.text(
        0,
        1.015,
        "Means and 95% intervals; descriptive comparison",
        transform=ax1.transAxes,
        fontsize=8.5,
        color="#53616d",
        va="bottom",
    )
    ax1.set_xlabel("Years from installed-capacity entry")
    ax1.set_ylabel("Bounded gross MWh per tonne")
    ax1.set_xticks([0, 1, 2, 3])
    ax1.set_ylim(0.24, 0.40)
    ax1.legend(frameon=False, fontsize=8.4, loc="lower right")

    style_axes(ax2)
    status_specs = [
        ("Operating prior year", "Operating prior year", "#35689a", "o", -1.0),
        (
            "Zero/missing prior throughput",
            "Zero/missing prior throughput",
            "#a35f2d",
            "s",
            -1.1,
        ),
        (
            "No exact prior-year row",
            "No exact prior-year row",
            "#6f7b84",
            "^",
            1.3,
        ),
    ]
    for value, label, color, marker, label_offset in status_specs:
        subset = status[status["prior_operating_status"].eq(value)].sort_values(
            "event_time"
        )
        ax2.errorbar(
            subset["event_time"],
            subset["mean_rank_pct"] * 100,
            yerr=1.96 * subset["se_rank_pct"] * 100,
            color=color,
            marker=marker,
            markerfacecolor="white",
            markeredgewidth=1.4,
            capsize=3,
            linewidth=1.5,
            label=label,
        )
        final = subset.iloc[-1]
        ax2.text(
            3.08,
            final["mean_rank_pct"] * 100 + label_offset,
            label,
            color=color,
            fontsize=7.6,
            va="center",
        )
    ax2.axhline(50, color="#3f4a54", linestyle="--", linewidth=1.0)
    ax2.set_title(
        "B. Within-year rank by prior status",
        loc="left",
        color="#22313f",
        pad=16,
    )
    ax2.text(
        0,
        1.015,
        "Mean percentile and 95% intervals",
        transform=ax2.transAxes,
        fontsize=8.5,
        color="#53616d",
        va="bottom",
    )
    ax2.set_xlabel("Years from installed-capacity entry")
    ax2.set_ylabel("Mean generator percentile")
    ax2.set_xticks([0, 1, 2, 3])
    ax2.set_xlim(-0.15, 4.15)
    ax2.set_ylim(20, 80)

    fig.tight_layout(w_pad=2.5)
    fig.savefig(PNG_OUT, dpi=300, bbox_inches="tight", facecolor="white")
    fig.savefig(PDF_OUT, bbox_inches="tight", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    build()
