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
    header_h = 0.082
    ax.add_patch(Rectangle((x, y + h - header_h), w, header_h, facecolor=HEADER, edgecolor=RULE, linewidth=1.0))
    add_text(ax, x + 0.018, y + h - 0.024, title, size=12.2, weight="bold")

    body_h = h - header_h
    row_h = body_h / len(rows)
    label_w = 0.112
    for idx, (label, body) in enumerate(rows):
        row_top = y + h - header_h - idx * row_h
        row_bottom = row_top - row_h
        if idx:
            ax.plot([x, x + w], [row_top, row_top], color="#c3c8ce", linewidth=0.65)
        add_text(ax, x + 0.018, row_top - 0.02, label, size=9.5, weight="bold", color=MUTED)
        add_text(ax, x + label_w, row_top - 0.02, body, size=9.4)
        if idx == len(rows) - 1:
            ax.plot([x, x + w], [row_bottom, row_bottom], color=RULE, linewidth=1.0)


def add_source_panel(ax) -> None:
    x, y, w, h = 0.12, 0.81, 0.76, 0.125
    ax.add_patch(Rectangle((x, y), w, h, facecolor=FILL, edgecolor=RULE, linewidth=1.0))
    add_text(ax, x + 0.025, y + h - 0.03, "Source panel", size=12.2, weight="bold")
    add_text(
        ax,
        x + 0.19,
        y + h - 0.03,
        "Ministry of the Environment General Waste Treatment Survey\nFY2005-FY2024 | 23,599 facility-year rows",
        size=10.2,
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
        "A. Entry frame",
        [
            (
                "Question",
                "Who first reports installed\ngeneration capacity?",
            ),
            (
                "Sample",
                "At-risk no-capacity facilities\n13,770 rows | 2,035 facilities | 141 events",
            ),
            (
                "Model",
                "Year + elapsed-duration logit\nbroad: 10,823/98 | active: 9,215/58",
            ),
            (
                "Claim",
                "Scale robust across frames;\nage pattern depends on risk set",
            ),
        ],
    )

    add_panel(
        ax,
        0.525,
        0.29,
        0.42,
        0.44,
        "B. Generator frame",
        [
            (
                "Question",
                "How much gross electricity\nis generated per tonne?",
            ),
            (
                "Sample",
                "Identifiable operating generators\n5,683 rows | 1,016 facilities",
            ),
            (
                "Model",
                "Logged MWh/t OLS\nyear + observed technology controls",
            ),
            (
                "Claim",
                "Structured age/vintage, scale,\nand utilization associations",
            ),
        ],
    )

    x, y, w, h = 0.15, 0.09, 0.70, 0.12
    ax.add_patch(Rectangle((x, y), w, h, facecolor=FILL, edgecolor=RULE, linewidth=1.0))
    add_text(ax, x + 0.025, y + h - 0.03, "Synthesis", size=12.0, weight="bold")
    add_text(
        ax,
        x + 0.16,
        y + h - 0.026,
        "One fleet, linked outcomes: asset entry, active conversion, and post-entry position.\n"
        "A fleet average would conflate distinct estimands and decision points.",
        size=9.8,
    )

    fig.savefig(PNG_OUT, dpi=300, bbox_inches="tight")
    fig.savefig(PDF_OUT, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    build()
