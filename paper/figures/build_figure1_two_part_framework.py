#!/usr/bin/env python3
"""Generate a formal Figure 1 for the paper manuscript.

This replaces the previous slide-like SVG with a source-generated paper figure
that can be used both in Markdown/HTML exports (PNG) and in the LaTeX reading
PDF (PDF).
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


ROOT = Path(__file__).resolve().parent
PNG_OUT = ROOT / "figure1_two_part_framework.png"
PDF_OUT = ROOT / "figure1_two_part_framework.pdf"


def add_box(
    ax,
    x: float,
    y: float,
    w: float,
    h: float,
    title: str,
    body_lines: list[str],
    edge: str = "#415364",
    face: str = "#fcfdff",
    title_color: str = "#1f2e3a",
) -> None:
    box = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="square,pad=0.012",
        linewidth=1.4,
        edgecolor=edge,
        facecolor=face,
    )
    ax.add_patch(box)
    ax.text(
        x + 0.025,
        y + h - 0.06,
        title,
        ha="left",
        va="top",
        fontsize=17.5,
        fontweight="bold",
        family="DejaVu Sans",
        color=title_color,
    )
    line_y = y + h - 0.12
    for line in body_lines:
        ax.text(
            x + 0.025,
            line_y,
            line,
            ha="left",
            va="top",
            fontsize=14.2,
            family="DejaVu Sans",
            color="#32414d",
        )
        line_y -= 0.056


def add_connector(ax, start: tuple[float, float], end: tuple[float, float]) -> None:
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=12,
            linewidth=1.35,
            color="#6d7d8d",
            shrinkA=4,
            shrinkB=4,
        )
    )


def build() -> None:
    plt.rcParams.update(
        {
            "figure.facecolor": "white",
            "savefig.facecolor": "white",
        }
    )

    fig = plt.figure(figsize=(11.0, 5.4), dpi=200)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    add_box(
        ax,
        0.245,
        0.74,
        0.51,
        0.12,
        "Full facility panel",
        [
            "MOE General Waste Treatment Survey, FY2005-FY2024",
            "23,599 facility-year rows before the analytical split",
        ],
        edge="#6d7f94",
        face="#f8fafc",
        title_color="#243443",
    )

    add_box(
        ax,
        0.08,
        0.36,
        0.37,
        0.27,
        "A. Adoption frame",
        [
            "At-risk facilities first seen without generation",
            "13,770 facility-years | 2,035 facilities | 141 events",
            "Signal: selective modernization",
        ],
        edge="#6f7f90",
        face="#fcfcfd",
    )

    add_box(
        ax,
        0.55,
        0.36,
        0.37,
        0.27,
        "B. Generator frame",
        [
            "Operating generators with positive throughput and output",
            "5,683 observations | 1,016 facilities",
            "Signal: bounded responsiveness",
        ],
        edge="#6f7f90",
        face="#fcfcfd",
    )

    add_box(
        ax,
        0.19,
        0.11,
        0.62,
        0.12,
        "Synthesis",
        [
            "Entry into generation and performance within generation are different estimands.",
        ],
        edge="#495767",
        face="#f8fafc",
        title_color="#243443",
    )

    add_connector(ax, (0.50, 0.74), (0.265, 0.61))
    add_connector(ax, (0.50, 0.74), (0.735, 0.61))
    add_connector(ax, (0.265, 0.36), (0.42, 0.23))
    add_connector(ax, (0.735, 0.36), (0.58, 0.23))

    fig.savefig(PNG_OUT, dpi=300, bbox_inches="tight")
    fig.savefig(PDF_OUT, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    build()
