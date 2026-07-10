#!/usr/bin/env python3
"""Plot pathway profiles in the first complete fiscal year after entry."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
FIGURE_DIR = Path(__file__).resolve().parent
DATA_PATH = ROOT / "output" / "post_adoption_trajectories.csv"
PNG_OUT = FIGURE_DIR / "figure4_post_entry_trajectories.png"
PDF_OUT = FIGURE_DIR / "figure4_post_entry_trajectories.pdf"

INK = "#20262d"
MUTED = "#59636e"
GRID = "#d9dee3"
BLUE = "#0072b2"
ORANGE = "#d55e00"

PATHWAY_STYLES = {
    "Continuity-lineage entry": {
        "label": "Continuity-lineage",
        "color": BLUE,
        "marker": "o",
        "offset": -0.105,
    },
    "Rebuild/replacement-like entry": {
        "label": "Rebuild/replacement-like",
        "color": ORANGE,
        "marker": "s",
        "offset": 0.105,
    },
}

METRICS = (
    ("mean_gross_rank_pct", "Gross MWh/t\nrank"),
    ("mean_design_rank_pct", "Design intensity\nrank"),
    ("mean_capacity_factor_rank_pct", "Capacity factor\nrank"),
)


def load_data() -> tuple[pd.DataFrame, int]:
    if not DATA_PATH.exists():
        raise SystemExit("Run the adoption analysis before Figure 4.")
    data = pd.read_csv(DATA_PATH)
    required = {
        "series",
        "pathway_category",
        "event_time",
        "events",
        *(column for column, _ in METRICS),
    }
    missing = required.difference(data.columns)
    if missing:
        raise ValueError(f"Figure 4 input is missing columns: {sorted(missing)}")
    first_year = data[
        data["series"].eq("By pathway")
        & data["event_time"].eq(1)
        & data["pathway_category"].isin(PATHWAY_STYLES)
    ].copy()
    if len(first_year) != len(PATHWAY_STYLES) or first_year["pathway_category"].duplicated().any():
        raise ValueError("Figure 4 requires one t=1 row for each focal pathway.")
    metric_columns = [column for column, _ in METRICS]
    if not first_year[metric_columns].apply(lambda col: col.between(0, 1)).all().all():
        raise ValueError("Figure 4 percentile ranks must lie between 0 and 1.")
    omitted = data[
        data["series"].eq("By pathway")
        & data["event_time"].eq(1)
        & data["pathway_category"].eq("Forward-dated / placeholder entry")
    ]
    omitted_n = int(omitted["events"].iloc[0]) if len(omitted) == 1 else 0
    return first_year, omitted_n


def style_axes(ax: plt.Axes) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(MUTED)
    ax.spines["bottom"].set_color(MUTED)
    ax.tick_params(colors=INK, labelsize=7.7, length=3)
    ax.grid(axis="y", color=GRID, linewidth=0.65)
    ax.set_axisbelow(True)


def build() -> None:
    data, omitted_n = load_data()
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

    fig, ax = plt.subplots(figsize=(3.7, 3.75), dpi=200)
    style_axes(ax)
    x = np.arange(len(METRICS), dtype=float)

    for pathway, style in PATHWAY_STYLES.items():
        row = data[data["pathway_category"].eq(pathway)].iloc[0]
        values = np.array([float(row[column]) * 100 for column, _ in METRICS])
        x_values = x + style["offset"]
        label = f"{style['label']} (n={int(row['events'])})"
        ax.scatter(
            x_values,
            values,
            s=34,
            marker=style["marker"],
            facecolor="white",
            edgecolor=style["color"],
            linewidth=1.4,
            label=label,
            zorder=3,
        )
        for x_value, value in zip(x_values, values):
            ax.text(
                x_value,
                value + 3.2,
                f"{value:.0f}",
                color=style["color"],
                fontsize=7.3,
                fontweight="semibold",
                ha="center",
                va="bottom",
            )

    ax.axhline(50, color=INK, linewidth=0.9, linestyle=(0, (3, 2)), zorder=2)
    ax.text(
        -0.42,
        51.7,
        "50th percentile",
        color=MUTED,
        fontsize=6.8,
        ha="left",
        va="bottom",
    )
    handles, labels = ax.get_legend_handles_labels()
    fig.text(
        0.08,
        0.965,
        "First-year profile after generation entry",
        fontsize=9.4,
        fontweight="semibold",
        ha="left",
        va="top",
    )
    fig.text(
        0.08,
        0.91,
        "Mean within-year percentiles among engineering-valid generators",
        color=MUTED,
        fontsize=7.1,
        ha="left",
        va="top",
    )
    ax.set_ylabel("Mean percentile rank", fontsize=8.1)
    ax.set_ylim(0, 100)
    ax.set_yticks([0, 20, 40, 60, 80, 100])
    ax.set_xlim(-0.45, 2.55)
    ax.set_xticks(x, [label for _, label in METRICS])
    fig.legend(
        handles,
        labels,
        loc="upper left",
        bbox_to_anchor=(0.08, 0.87),
        frameon=False,
        fontsize=7.0,
        handletextpad=0.4,
        borderaxespad=0,
        labelspacing=0.3,
    )
    omission = (
        f"Placeholder/forward-dated pathway (n={omitted_n}) omitted for sparse support; "
        "pathway contrasts are descriptive."
    )
    fig.text(0.08, 0.035, omission, color=MUTED, fontsize=6.5, ha="left", wrap=True)

    fig.subplots_adjust(left=0.18, right=0.97, top=0.68, bottom=0.22)
    fig.savefig(PNG_OUT, dpi=300, facecolor="white")
    fig.savefig(PDF_OUT, facecolor="white", bbox_inches=None)
    plt.close(fig)


if __name__ == "__main__":
    build()
