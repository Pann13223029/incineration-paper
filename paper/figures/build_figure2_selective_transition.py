#!/usr/bin/env python3
"""Generate Figure 2 from canonical transition-model output."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
FIGURE_DIR = Path(__file__).resolve().parent
DATA_PATH = ROOT / "output" / "figure2_transition_effects.csv"
MANIFEST_PATH = ROOT / "output" / "manifests" / "05a_power_adoption.json"
PNG_OUT = FIGURE_DIR / "figure2_selective_transition.png"
PDF_OUT = FIGURE_DIR / "figure2_selective_transition.pdf"

VARIABLE_ORDER = [
    "age_10-20 yrs",
    "age_20-30 yrs",
    "age_30+ yrs",
    "lag_capacity_100t",
]
DISPLAY_LABELS = {
    "age_10-20 yrs": "Age 10-20 vs 0-10",
    "age_20-30 yrs": "Age 20-30 vs 0-10",
    "age_30+ yrs": "Age 30+ vs 0-10",
    "lag_capacity_100t": "Capacity (+100 t/day)",
}


def style_axes(ax) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#66727f")
    ax.spines["bottom"].set_color("#66727f")
    ax.tick_params(colors="#33414d", labelsize=9.5)
    ax.grid(axis="x", color="#dce3ea", linewidth=0.8)
    ax.axvline(0, color="#263440", linewidth=1.0, zorder=1)
    ax.set_axisbelow(True)


def model_context(manifest: dict, outcome: str) -> str:
    metadata = manifest["metadata"]
    if outcome == "Broad asset entry":
        return (
            f"N = {metadata['model_obs']:,}; "
            f"events = {metadata['model_events']:,}"
        )
    if outcome == "Active conversion":
        active = metadata["active_operating_conversion_sensitivity"]
        return f"N = {active['model_obs']:,}; events = {active['model_events']:,}"
    exit_meta = metadata["panel_exit_diagnostic"]
    return f"N = {exit_meta['model_obs']:,}; exits = {exit_meta['events']:,}"


def build() -> None:
    if not DATA_PATH.exists() or not MANIFEST_PATH.exists():
        raise SystemExit("Run the adoption analysis before building Figure 2.")

    data = pd.read_csv(DATA_PATH)
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "axes.titlesize": 11.5,
            "axes.titleweight": "bold",
            "axes.labelsize": 10.5,
        }
    )
    fig, axes = plt.subplots(1, 3, figsize=(13.0, 4.6), dpi=200, sharey=True)

    panel_specs = [
        ("Broad asset entry", "A. Broad asset entry", "#35689a", "o"),
        ("Active conversion", "B. Active conversion", "#2f7d68", "D"),
        ("Panel exit", "C. Final coded-panel exit", "#b06532", "s"),
    ]
    y = np.arange(len(VARIABLE_ORDER))
    for ax, (outcome, title, color, marker) in zip(axes, panel_specs):
        style_axes(ax)
        subset = (
            data[data["outcome"].eq(outcome)]
            .set_index("variable")
            .loc[VARIABLE_ORDER]
            .reset_index()
        )
        lower = subset["ame_pp"] - subset["ci_low_pp"]
        upper = subset["ci_high_pp"] - subset["ame_pp"]
        ax.errorbar(
            subset["ame_pp"],
            y,
            xerr=np.vstack([lower, upper]),
            fmt=marker,
            color=color,
            ecolor=color,
            markerfacecolor="white",
            markeredgewidth=1.7,
            markersize=7,
            capsize=3.5,
            linewidth=1.5,
            zorder=3,
        )
        for x_value, y_value in zip(subset["ame_pp"], y):
            offset = 0.13 if x_value >= 0 else -0.13
            ax.text(
                x_value + offset,
                y_value - 0.15,
                f"{x_value:+.2f}",
                ha="left" if x_value >= 0 else "right",
                va="center",
                fontsize=8.5,
                color="#263440",
                fontweight="bold",
            )
        ax.set_title(title, loc="left", color="#22313f", pad=16)
        ax.text(
            0,
            1.015,
            model_context(manifest, outcome),
            transform=ax.transAxes,
            fontsize=8.5,
            color="#53616d",
            va="bottom",
        )
        ax.set_xlabel("Average marginal effect (percentage points)")
        ax.set_yticks(y, [DISPLAY_LABELS[var] for var in VARIABLE_ORDER])

    axes[0].invert_yaxis()
    axes[0].set_xlim(-3.0, 1.2)
    axes[1].set_xlim(-1.5, 0.9)
    axes[2].set_xlim(-2.8, 4.8)
    fig.tight_layout(w_pad=1.6)
    fig.savefig(PNG_OUT, dpi=300, bbox_inches="tight", facecolor="white")
    fig.savefig(PDF_OUT, bbox_inches="tight", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    build()
