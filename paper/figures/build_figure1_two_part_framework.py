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
        y + h - 0.05,
        title,
        ha="left",
        va="top",
        fontsize=15.6,
        fontweight="bold",
        family="DejaVu Sans",
        color=title_color,
    )
    line_y = y + h - 0.11
    for line in body_lines:
        ax.text(
            x + 0.025,
            line_y,
            line,
            ha="left",
            va="top",
            fontsize=12.2,
            family="DejaVu Sans",
            color="#32414d",
            linespacing=1.35,
        )
        line_y -= 0.058 * (line.count("\n") + 1)


def add_connector(ax, start: tuple[float, float], end: tuple[float, float]) -> None:
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=11,
            linewidth=1.35,
            color="#6d7d8d",
            shrinkA=4,
            shrinkB=4,
        )
    )


def add_line(ax, start: tuple[float, float], end: tuple[float, float]) -> None:
    ax.plot(
        [start[0], end[0]],
        [start[1], end[1]],
        color="#6d7d8d",
        linewidth=1.35,
        solid_capstyle="round",
    )


def build() -> None:
    plt.rcParams.update(
        {
            "figure.facecolor": "white",
            "savefig.facecolor": "white",
        }
    )

    fig = plt.figure(figsize=(11.2, 6.8), dpi=200)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    add_box(
        ax,
        0.22,
        0.78,
        0.56,
        0.18,
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
        0.06,
        0.40,
        0.39,
        0.32,
        "A. Adoption frame",
        [
            "At-risk facilities first seen\nwithout generation",
            "13,770 facility-years | 2,035 facilities | 141 events",
            "Signal: selective modernization",
        ],
        edge="#6f7f90",
        face="#fcfcfd",
    )

    add_box(
        ax,
        0.54,
        0.40,
        0.39,
        0.32,
        "B. Generator frame",
        [
            "Operating generators with positive\nthroughput and output",
            "5,683 observations | 1,016 facilities",
            "Signal: bounded responsiveness",
        ],
        edge="#6f7f90",
        face="#fcfcfd",
    )

    add_box(
        ax,
        0.17,
        0.05,
        0.64,
        0.20,
        "Synthesis",
        [
            "Entry into generation and performance within generation\nare different estimands.",
        ],
        edge="#495767",
        face="#f8fafc",
        title_color="#243443",
    )

    # Clean tree-style split above the middle row.
    add_line(ax, (0.50, 0.78), (0.50, 0.74))
    add_line(ax, (0.26, 0.74), (0.74, 0.74))
    add_connector(ax, (0.26, 0.74), (0.26, 0.71))
    add_connector(ax, (0.74, 0.74), (0.74, 0.71))

    # Clean join into the synthesis box.
    add_line(ax, (0.26, 0.39), (0.26, 0.28))
    add_line(ax, (0.74, 0.39), (0.74, 0.28))
    add_line(ax, (0.26, 0.28), (0.74, 0.28))
    add_connector(ax, (0.50, 0.28), (0.50, 0.25))

    fig.savefig(PNG_OUT, dpi=300, bbox_inches="tight")
    fig.savefig(PDF_OUT, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    build()
