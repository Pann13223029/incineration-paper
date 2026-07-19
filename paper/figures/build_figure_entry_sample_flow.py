#!/usr/bin/env python3
"""Render the entry-model sample flow as a compact academic diagram."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
FIGURE_DIR = Path(__file__).resolve().parent
DATA_PATH = ROOT / "output" / "entry_sample_flow.csv"
PNG_OUT = FIGURE_DIR / "figure_entry_sample_flow.png"
PDF_OUT = FIGURE_DIR / "figure_entry_sample_flow.pdf"

INK = "#1a1a1a"
MUTED = "#555555"
LINE = "#4a4a4a"
FILL = "#ffffff"
ACCENT_FILL = "#ededed"


def load_data() -> pd.DataFrame:
    if not DATA_PATH.exists():
        raise SystemExit("Run the scientific revision analysis before the sample-flow figure.")
    data = pd.read_csv(DATA_PATH).sort_values("order")
    required = {"order", "stage", "facility_year_rows", "lineages", "events"}
    missing = required.difference(data.columns)
    if missing:
        raise ValueError(f"Sample-flow input is missing columns: {sorted(missing)}")
    expected = {
        "All reconstructed administrative lineages",
        "Left-censored: positive capacity in first observed year",
        "Observed non-generator risk set",
        "Exact-year complete-covariate model",
        "Positive-prior-throughput sensitivity",
    }
    if set(data["stage"]) != expected:
        raise ValueError("Sample-flow stages do not match the analytical contract")
    return data.set_index("stage")


def count(value: float) -> str:
    return f"{int(value):,}"


def add_box(
    ax: plt.Axes,
    x: float,
    title: str,
    detail: str,
    *,
    accent: bool = False,
) -> None:
    box = Rectangle(
        (x, 0.42),
        0.205,
        0.64,
        linewidth=0.75,
        edgecolor=LINE,
        facecolor=ACCENT_FILL if accent else FILL,
    )
    ax.add_patch(box)
    ax.text(
        x + 0.1025,
        0.91,
        title,
        ha="center",
        va="top",
        color=INK,
        fontsize=7.5,
        fontweight="bold",
        linespacing=1.15,
    )
    ax.text(
        x + 0.1025,
        0.57,
        detail,
        ha="center",
        va="center",
        color=MUTED,
        fontsize=6.8,
        linespacing=1.28,
    )


def add_arrow(ax: plt.Axes, start: float, end: float, label: str) -> None:
    ax.annotate(
        "",
        xy=(end, 0.74),
        xytext=(start, 0.74),
        arrowprops={"arrowstyle": "-|>", "color": LINE, "lw": 0.75},
    )
    ax.text(
        (start + end) / 2,
        1.25,
        label,
        ha="center",
        va="bottom",
        color=MUTED,
        fontsize=6.3,
        linespacing=1.15,
    )


def build() -> None:
    data = load_data()
    full = data.loc["All reconstructed administrative lineages"]
    censored = data.loc[
        "Left-censored: positive capacity in first observed year"
    ]
    risk = data.loc["Observed non-generator risk set"]
    exact = data.loc["Exact-year complete-covariate model"]
    prior = data.loc["Positive-prior-throughput sensitivity"]

    plt.rcParams.update(
        {
            "font.family": "DejaVu Serif",
            "text.color": INK,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )
    fig, ax = plt.subplots(figsize=(6.7, 1.65), dpi=200)
    ax.set_xlim(0, 1)
    ax.set_ylim(0.25, 1.48)
    ax.axis("off")

    x_positions = [0.01, 0.265, 0.52, 0.775]
    add_box(
        ax,
        x_positions[0],
        "Reconstructed\npanel",
        f"{count(full.facility_year_rows)} rows\n{count(full.lineages)} lineages",
    )
    add_box(
        ax,
        x_positions[1],
        "Observed\nnon-generator risk set",
        f"{count(risk.facility_year_rows)} risk rows\n"
        f"{count(risk.lineages)} lineages | {count(risk.events)} events",
    )
    add_box(
        ax,
        x_positions[2],
        "Frozen primary\nentry model",
        f"{count(exact.facility_year_rows)} risk rows\n"
        f"{count(exact.lineages)} lineages | {count(exact.events)} events",
        accent=True,
    )
    add_box(
        ax,
        x_positions[3],
        "Prior-operation\nsensitivity",
        f"{count(prior.facility_year_rows)} risk rows\n"
        f"{count(prior.lineages)} lineages | {count(prior.events)} events",
    )

    add_arrow(
        ax,
        x_positions[0] + 0.205,
        x_positions[1],
        f"Exclude {count(censored.lineages)} lineages\nalready installed at first observation",
    )
    add_arrow(
        ax,
        x_positions[1] + 0.205,
        x_positions[2],
        "Require exact annual lag\nand complete prior covariates",
    )
    add_arrow(
        ax,
        x_positions[2] + 0.205,
        x_positions[3],
        "Require positive\nprior-year throughput",
    )

    fig.subplots_adjust(left=0.01, right=0.99, top=0.96, bottom=0.06)
    fig.savefig(PNG_OUT, dpi=300, facecolor="white")
    fig.savefig(PDF_OUT, facecolor="white", bbox_inches=None)
    plt.close(fig)


if __name__ == "__main__":
    build()
