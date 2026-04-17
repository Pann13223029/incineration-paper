#!/usr/bin/env python3
"""Build a clean LaTeX reading PDF for the paper workspace.

This script keeps the journal-facing Markdown export workflow intact while
adding a higher-quality reading PDF:

- renders the three SVG manuscript figures into high-resolution PNG assets
- compiles `paper/manuscript/paper.tex` with Tectonic
- copies the resulting PDF into `paper/submission/`
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
MANUSCRIPT_DIR = REPO_ROOT / "paper" / "manuscript"
BUILD_DIR = MANUSCRIPT_DIR / "build"
BUILD_FIGURES_DIR = BUILD_DIR / "figures"
LATEX_SOURCE = MANUSCRIPT_DIR / "paper.tex"
LATEX_PDF = MANUSCRIPT_DIR / "paper.pdf"
SUBMISSION_DIR = REPO_ROOT / "paper" / "submission"
OUT_PDF = SUBMISSION_DIR / "waste-management-manuscript-latex.pdf"
FIGURE1_SCRIPT = REPO_ROOT / "paper" / "figures" / "build_figure1_two_part_framework.py"


@dataclass(frozen=True)
class FigureSpec:
    source_name: str
    output_name: str
    width: int
    height: int


FIGURES = (
    FigureSpec("figure2_selective_transition.svg", "figure2_selective_transition.png", 1200, 760),
    FigureSpec("figure3_efficiency_structure.svg", "figure3_efficiency_structure.png", 1200, 720),
)


def chrome_binary() -> str:
    chrome = shutil.which("google-chrome")
    if chrome:
        return chrome

    app_binary = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    if Path(app_binary).exists():
        return app_binary

    raise SystemExit(
        "Google Chrome not found; cannot rasterize SVG figures for the LaTeX PDF."
    )


def tectonic_binary() -> str:
    tectonic = shutil.which("tectonic")
    if tectonic:
        return tectonic

    local_binary = Path.home() / ".local" / "bin" / "tectonic"
    if local_binary.exists():
        return str(local_binary)

    raise SystemExit("Tectonic not found; cannot compile the LaTeX manuscript.")


def render_figure(chrome: str, spec: FigureSpec) -> Path:
    source = REPO_ROOT / "paper" / "figures" / spec.source_name
    output = BUILD_FIGURES_DIR / spec.output_name
    command = [
        chrome,
        "--headless",
        "--disable-gpu",
        "--hide-scrollbars",
        "--force-device-scale-factor=2",
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=1000",
        f"--window-size={spec.width},{spec.height}",
        f"--screenshot={output}",
        source.resolve().as_uri(),
    ]
    subprocess.run(command, check=True)
    if not output.exists():
        raise SystemExit(f"Expected rendered figure was not created: {output}")
    return output


def build_figure1() -> None:
    if not FIGURE1_SCRIPT.exists():
        raise SystemExit(f"Figure 1 build script not found: {FIGURE1_SCRIPT}")
    subprocess.run([sys.executable, str(FIGURE1_SCRIPT)], check=True)


def compile_latex(tectonic: str) -> None:
    command = [
        tectonic,
        "-p",
        "--keep-logs",
        "--keep-intermediates",
        LATEX_SOURCE.name,
    ]
    subprocess.run(command, cwd=MANUSCRIPT_DIR, check=True)
    if not LATEX_PDF.exists():
        raise SystemExit(f"Tectonic did not produce the expected PDF: {LATEX_PDF}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--skip-rasterize",
        action="store_true",
        help="Reuse existing PNG build figures instead of rerendering the SVG sources.",
    )
    args = parser.parse_args()

    if not LATEX_SOURCE.exists():
        raise SystemExit(f"LaTeX manuscript not found: {LATEX_SOURCE}")

    SUBMISSION_DIR.mkdir(parents=True, exist_ok=True)
    BUILD_FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    build_figure1()

    if not args.skip_rasterize:
        chrome = chrome_binary()
        for spec in FIGURES:
            render_figure(chrome, spec)

    tectonic = tectonic_binary()
    compile_latex(tectonic)
    shutil.copy2(LATEX_PDF, OUT_PDF)

    print(f"LaTeX manuscript source: {LATEX_SOURCE}")
    print(f"Rendered figure assets: {BUILD_FIGURES_DIR}")
    print(f"LaTeX manuscript PDF: {OUT_PDF}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
