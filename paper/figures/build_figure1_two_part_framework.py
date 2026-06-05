#!/usr/bin/env python3
"""Generate Figure 1 as a formal analytical-design schematic."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


ROOT = Path(__file__).resolve().parent
PNG_OUT = ROOT / "figure1_two_part_framework.png"
PDF_OUT = ROOT / "figure1_two_part_framework.pdf"

INK = "#1f2933"
RULE = "#3f4a56"
MUTED = "#596671"
FILL = "#f4f5f6"
HEADER = "#e8eaed"


def add_text(
    ax,
    x: float,
    y: float,
    text: str,
    *,
    size: float = 10.5,
    weight: str = "normal",
    color: str = INK,
    ha: str = "left",
    va: str = "top",
) -> None:
    ax.text(
        x,
        y,
        text,
        ha=ha,
        va=va,
        fontsize=size,
        fontweight=weight,
        family="DejaVu Serif",
        color=color,
        linespacing=1.18,
    )


def add_panel(
    ax,
    x: float,
    y: float,
    w: float,
    h: float,
    title: str,
    rows: list[tuple[str, str]],
) -> None:
    ax.add_patch(Rectangle((x, y), w, h, facecolor="white", edgecolor=RULE, linewidth=1.0))
    header_h = 0.075
    ax.add_patch(Rectangle((x, y + h - header_h), w, header_h, facecolor=HEADER, edgecolor=RULE, linewidth=1.0))
    add_text(ax, x + 0.018, y + h - 0.022, title, size=11.3, weight="bold")

    body_h = h - header_h
    row_h = body_h / len(rows)
    label_w = 0.105
    for idx, (label, body) in enumerate(rows):
        row_top = y + h - header_h - idx * row_h
        row_bottom = row_top - row_h
        if idx:
            ax.plot([x, x + w], [row_top, row_top], color="#c3c8ce", linewidth=0.65)
        add_text(ax, x + 0.018, row_top - 0.018, label, size=8.8, weight="bold", color=MUTED)
        add_text(ax, x + label_w, row_top - 0.018, body, size=8.6)
        if idx == len(rows) - 1:
            ax.plot([x, x + w], [row_bottom, row_bottom], color=RULE, linewidth=1.0)


def add_source_panel(ax) -> None:
    x, y, w, h = 0.12, 0.81, 0.76, 0.125
    ax.add_patch(Rectangle((x, y), w, h, facecolor=FILL, edgecolor=RULE, linewidth=1.0))
    add_text(ax, x + 0.025, y + h - 0.03, "Source panel", size=11.5, weight="bold")
    add_text(
        ax,
        x + 0.19,
        y + h - 0.03,
        "Ministry of the Environment General Waste Treatment Survey\nFY2005-FY2024 | 23,599 facility-year rows",
        size=9.5,
    )


def add_connectors(ax) -> None:
    # Minimal bracket-style split: source panel to the two analytical frames.
    ax.plot([0.50, 0.50], [0.81, 0.765], color=RULE, linewidth=0.9)
    ax.plot([0.25, 0.75], [0.765, 0.765], color=RULE, linewidth=0.9)
    ax.plot([0.25, 0.25], [0.765, 0.735], color=RULE, linewidth=0.9)
    ax.plot([0.75, 0.75], [0.765, 0.735], color=RULE, linewidth=0.9)
    ax.add_patch(Rectangle((0.455, 0.745), 0.09, 0.028, facecolor="white", edgecolor="none"))
    add_text(ax, 0.50, 0.755, "analytical split", size=8.2, color=MUTED, ha="center")

    # Minimal merge into synthesis.
    ax.plot([0.25, 0.25], [0.29, 0.245], color=RULE, linewidth=0.9)
    ax.plot([0.75, 0.75], [0.29, 0.245], color=RULE, linewidth=0.9)
    ax.plot([0.25, 0.75], [0.245, 0.245], color=RULE, linewidth=0.9)
    ax.plot([0.50, 0.50], [0.245, 0.205], color=RULE, linewidth=0.9)


def build() -> None:
    plt.rcParams.update(
        {
            "figure.facecolor": "white",
            "savefig.facecolor": "white",
        }
    )

    fig = plt.figure(figsize=(11.8, 7.0), dpi=220)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    add_source_panel(ax)
    add_connectors(ax)

    add_panel(
        ax,
        0.055,
        0.29,
        0.42,
        0.44,
        "A. Adoption frame: entry margin",
        [
            (
                "Sample",
                "Coded at-risk facilities first observed\nwithout power generation\n13,770 facility-years | 2,035 facilities | 141 events",
            ),
            (
                "Estimand",
                "First observed reporting of power\ngeneration in the following fiscal year",
            ),
            (
                "Model",
                "Lagged discrete-time logit hazard\nwith year and prefecture fixed effects",
            ),
            (
                "Role",
                "Identifies selective observed entry,\nnot a causal retrofit mechanism",
            ),
        ],
    )

    add_panel(
        ax,
        0.525,
        0.29,
        0.42,
        0.44,
        "B. Generator frame: performance margin",
        [
            (
                "Sample",
                "Operating generators with positive\nthroughput and power output\n5,683 observations | 1,016 facilities",
            ),
            (
                "Outcome",
                "Electricity recovered per tonne\nclipped and logged MWh/t",
            ),
            (
                "Model",
                "Pooled, year-FE, and random-effects\npanel specifications",
            ),
            (
                "Role",
                "Describes structured performance\nhierarchy within generators",
            ),
        ],
    )

    x, y, w, h = 0.15, 0.09, 0.70, 0.12
    ax.add_patch(Rectangle((x, y), w, h, facecolor=FILL, edgecolor=RULE, linewidth=1.0))
    add_text(ax, x + 0.025, y + h - 0.028, "Synthesis", size=11.2, weight="bold")
    add_text(
        ax,
        x + 0.16,
        y + h - 0.026,
        "The same national fleet is interpreted through two linked but non-identical margins;\n"
        "one average-fleet estimate would conflate entry with post-entry performance.",
        size=9.0,
    )

    fig.savefig(PNG_OUT, dpi=300, bbox_inches="tight")
    fig.savefig(PDF_OUT, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    build()
