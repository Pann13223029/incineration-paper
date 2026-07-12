#!/usr/bin/env python3
"""Plot generator design intensity and capacity factor by start-year cohort."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
FIGURE_DIR = Path(__file__).resolve().parent
DATA_PATH = ROOT / "output" / "table2_generator_components_by_cohort.md"
PNG_OUT = FIGURE_DIR / "figure3_efficiency_structure.png"
PDF_OUT = FIGURE_DIR / "figure3_efficiency_structure.pdf"

INK = "#20262d"
MUTED = "#59636e"
GRID = "#d9dee3"
BLUE = "#0072b2"
ORANGE = "#d55e00"

COHORT_ORDER = ("Before 1990", "1990-1999", "2000-2009", "2010 or later")
COHORT_LABELS = ("Before\n1990", "1990-\n1999", "2000-\n2009", "2010 or\nlater")


def read_markdown_table(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise SystemExit("Run the generator component analysis before Figure 3.")
    table_lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line.startswith("|")]
    if len(table_lines) < 3:
        raise ValueError("Figure 3 could not find the cohort table.")
    rows = [[cell.strip() for cell in line.strip().strip("|").split("|")] for line in table_lines]
    header = rows[0]
    body = [row for row in rows[1:] if not set(row[0]).issubset({":", "-"})]
    frame = pd.DataFrame(body, columns=header)
    required = {
        "reported_start_year_cohort",
        "observations",
        "stable_sites",
        "median_generator_sizing",
        "median_capacity_factor",
    }
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"Figure 3 input is missing columns: {sorted(missing)}")
    numeric = required.difference({"reported_start_year_cohort"})
    for column in numeric:
        frame[column] = pd.to_numeric(frame[column], errors="raise")
    frame = frame.set_index("reported_start_year_cohort").loc[list(COHORT_ORDER)].reset_index()
    if frame["reported_start_year_cohort"].duplicated().any():
        raise ValueError("Figure 3 requires one row per start-year cohort.")
    if not frame["median_capacity_factor"].between(0, 1.2).all():
        raise ValueError("Capacity-factor medians are outside the audited range.")
    return frame


def style_axes(ax: plt.Axes) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(MUTED)
    ax.spines["bottom"].set_color(MUTED)
    ax.tick_params(colors=INK, labelsize=7.7, length=3)
    ax.grid(axis="y", color=GRID, linewidth=0.65)
    ax.set_axisbelow(True)


def annotate_points(ax: plt.Axes, x: np.ndarray, values: np.ndarray, suffix: str) -> None:
    offset = 0.035 * (ax.get_ylim()[1] - ax.get_ylim()[0])
    for x_value, value in zip(x, values):
        ax.text(
            x_value,
            value + offset,
            f"{value:.1f}{suffix}",
            ha="center",
            va="bottom",
            fontsize=7.2,
            color=INK,
        )


def build() -> None:
    data = read_markdown_table(DATA_PATH)
    site_counts = ", ".join(str(int(value)) for value in data["stable_sites"])
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

    fig, axes = plt.subplots(2, 1, figsize=(3.9, 4.6), dpi=200, sharex=True)
    x = np.arange(len(data), dtype=float)

    design = data["median_generator_sizing"].to_numpy(dtype=float)
    style_axes(axes[0])
    axes[0].vlines(x, 0, design, color="#b8cbd8", linewidth=1.2, zorder=2)
    axes[0].scatter(
        x,
        design,
        s=30,
        marker="o",
        facecolor="white",
        edgecolor=BLUE,
        linewidth=1.35,
        zorder=3,
    )
    axes[0].set_ylim(0, 25)
    axes[0].set_yticks([0, 5, 10, 15, 20, 25])
    axes[0].set_ylabel("Installed kW per t/day", fontsize=8.0)
    axes[0].set_title(
        "A. Generator design intensity",
        loc="left",
        fontsize=8.8,
        fontweight="semibold",
        pad=6,
    )
    annotate_points(axes[0], x, design, "")

    capacity_factor = data["median_capacity_factor"].to_numpy(dtype=float) * 100
    style_axes(axes[1])
    axes[1].vlines(x, 0, capacity_factor, color="#e7c7b8", linewidth=1.2, zorder=2)
    axes[1].scatter(
        x,
        capacity_factor,
        s=30,
        marker="s",
        facecolor="white",
        edgecolor=ORANGE,
        linewidth=1.35,
        zorder=3,
    )
    axes[1].set_ylim(0, 100)
    axes[1].set_yticks([0, 20, 40, 60, 80, 100])
    axes[1].set_ylabel("Capacity factor (%)", fontsize=8.0)
    axes[1].set_title(
        "B. Electrical capacity factor",
        loc="left",
        fontsize=8.8,
        fontweight="semibold",
        pad=6,
    )
    annotate_points(axes[1], x, capacity_factor, "%")
    axes[1].set_xticks(x, COHORT_LABELS)
    axes[1].set_xlabel("Reported facility start-year cohort", fontsize=8.0, labelpad=6)

    fig.suptitle(
        "Generator components by reported cohort",
        x=0.08,
        y=0.985,
        ha="left",
        fontsize=9.5,
        fontweight="semibold",
    )
    fig.text(
        0.08,
        0.945,
        "Engineering-valid facility-years; medians",
        color=MUTED,
        fontsize=7.4,
        ha="left",
    )
    fig.text(
        0.08,
        0.025,
        f"Lineage counts, oldest to newest: {site_counts}.\n"
        "Counts are non-additive because lineages can span cohorts.\n"
        "Start year is not a verified equipment date.",
        color=MUTED,
        fontsize=6.5,
        ha="left",
        linespacing=1.25,
    )

    fig.subplots_adjust(left=0.21, right=0.97, top=0.84, bottom=0.25, hspace=0.38)
    fig.savefig(PNG_OUT, dpi=300, facecolor="white")
    fig.savefig(PDF_OUT, facecolor="white", bbox_inches=None)
    plt.close(fig)


if __name__ == "__main__":
    build()
