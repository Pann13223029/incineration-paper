#!/usr/bin/env python3
"""Plot bias-reduced entry estimates with lineage-bootstrap intervals."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
FIGURE_DIR = Path(__file__).resolve().parent
DATA_PATH = ROOT / "output" / "figure2_transition_effects.csv"
PNG_OUT = FIGURE_DIR / "figure2_selective_transition.png"
PDF_OUT = FIGURE_DIR / "figure2_selective_transition.pdf"

INK = "#20262d"
MUTED = "#59636e"
GRID = "#d9dee3"
BLUE = "#0072b2"
ORANGE = "#d55e00"

MODEL_STYLES = {
    "Broad exact-year risk frame": {
        "label": "Broad exact-year frame",
        "color": BLUE,
        "marker": "o",
        "offset": 0.11,
    },
    "Prior-operation risk frame": {
        "label": "Prior-operation frame",
        "color": ORANGE,
        "marker": "s",
        "offset": -0.11,
    },
}

TERM_ORDER = (
    "age_10-19 yrs",
    "age_20-29 yrs",
    "age_30+ yrs",
    "log_processing_capacity",
)
TERM_LABELS = {
    "age_10-19 yrs": "Age 10-19",
    "age_20-29 yrs": "Age 20-29",
    "age_30+ yrs": "Age 30+",
    "log_processing_capacity": "Capacity\n300 vs 100 t/day",
}


def load_data() -> pd.DataFrame:
    if not DATA_PATH.exists():
        raise SystemExit("Run the adoption analysis before Figure 2.")
    data = pd.read_csv(DATA_PATH)
    required = {
        "model",
        "term",
        "coefficient",
        "bootstrap_ci_low",
        "bootstrap_ci_high",
        "observations",
        "events",
    }
    missing = required.difference(data.columns)
    if missing:
        raise ValueError(f"Figure 2 input is missing columns: {sorted(missing)}")
    data = data[
        data["model"].isin(MODEL_STYLES) & data["term"].isin(TERM_ORDER)
    ].copy()
    expected = len(MODEL_STYLES) * len(TERM_ORDER)
    if len(data) != expected or data.duplicated(["model", "term"]).any():
        raise ValueError("Figure 2 requires one estimate per model and focal term.")
    numeric = ["coefficient", "bootstrap_ci_low", "bootstrap_ci_high"]
    if not np.isfinite(data[numeric].to_numpy()).all():
        raise ValueError("Figure 2 contains non-finite coefficient estimates.")
    return data


def odds_ratio_contrast(term: str, row: pd.Series) -> tuple[float, float, float]:
    multiplier = 1.0
    if term == "log_processing_capacity":
        # The fitted predictor is log(1 + t/day / 100).
        multiplier = np.log1p(300 / 100) - np.log1p(100 / 100)
    values = np.exp(
        np.asarray(
            [
                row["coefficient"],
                row["bootstrap_ci_low"],
                row["bootstrap_ci_high"],
            ],
            dtype=float,
        )
        * multiplier
    )
    return float(values[0]), float(values[1]), float(values[2])


def style_axes(ax: plt.Axes) -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color(MUTED)
    ax.tick_params(axis="x", colors=INK, labelsize=7.8, length=3)
    ax.tick_params(axis="y", colors=INK, labelsize=8.0, length=0, pad=5)
    ax.grid(axis="x", color=GRID, linewidth=0.65)
    ax.set_axisbelow(True)


def build() -> None:
    data = load_data()
    model_rows = {
        model: int(data.loc[data["model"].eq(model), "observations"].iloc[0])
        for model in MODEL_STYLES
    }
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

    fig, ax = plt.subplots(figsize=(3.7, 4.15), dpi=200)
    style_axes(ax)
    y_base = np.arange(len(TERM_ORDER) - 1, -1, -1, dtype=float)

    for model, style in MODEL_STYLES.items():
        subset = data[data["model"].eq(model)].set_index("term").loc[list(TERM_ORDER)]
        contrasts = [odds_ratio_contrast(term, row) for term, row in subset.iterrows()]
        estimates = np.array([item[0] for item in contrasts])
        lows = np.array([item[1] for item in contrasts])
        highs = np.array([item[2] for item in contrasts])
        y = y_base + style["offset"]
        context = subset.iloc[0]
        label = f"{style['label']} ({int(context['events'])} events)"
        ax.errorbar(
            estimates,
            y,
            xerr=np.vstack([estimates - lows, highs - estimates]),
            fmt=style["marker"],
            color=style["color"],
            ecolor=style["color"],
            markerfacecolor="white",
            markeredgewidth=1.25,
            markersize=5.0,
            elinewidth=1.25,
            capsize=2.5,
            label=label,
            zorder=3,
        )

    ax.axvline(1, color=INK, linewidth=0.9, linestyle=(0, (3, 2)), zorder=2)
    ax.set_xscale("log")
    ax.set_xlim(0.1, 12)
    ticks = [0.125, 0.25, 0.5, 1, 2, 4, 8]
    ax.set_xticks(ticks, ["0.125", "0.25", "0.5", "1", "2", "4", "8"])
    ax.set_yticks(y_base, [TERM_LABELS[item] for item in TERM_ORDER])
    ax.set_ylim(-0.55, 3.55)
    ax.set_xlabel("Odds ratio (log scale)", fontsize=8.2, labelpad=7)
    handles, labels = ax.get_legend_handles_labels()
    fig.text(
        0.08,
        0.965,
        "Scale-associated entry; age remains uncertain",
        fontsize=9.3,
        fontweight="semibold",
        ha="left",
        va="top",
    )
    fig.text(
        0.08,
        0.915,
        "Firth logistic models; 95% intervals from 499 lineage bootstraps",
        color=MUTED,
        fontsize=7.3,
        ha="left",
        va="top",
    )
    fig.legend(
        handles,
        labels,
        loc="upper left",
        bbox_to_anchor=(0.08, 0.875),
        frameon=False,
        fontsize=7.1,
        handletextpad=0.5,
        borderaxespad=0,
        labelspacing=0.35,
    )
    fig.text(
        0.08,
        0.03,
        "Age reference: 0-9 years; capacity compares 300 with 100 t/day.\n"
        f"Models use {model_rows['Broad exact-year risk frame']:,} and "
        f"{model_rows['Prior-operation risk frame']:,} risk rows, respectively.",
        color=MUTED,
        fontsize=6.6,
        ha="left",
        linespacing=1.25,
    )

    fig.subplots_adjust(left=0.34, right=0.97, top=0.68, bottom=0.18)
    fig.savefig(PNG_OUT, dpi=300, facecolor="white")
    fig.savefig(PDF_OUT, facecolor="white", bbox_inches=None)
    plt.close(fig)


if __name__ == "__main__":
    build()
