#!/usr/bin/env python3
"""Build a clean LaTeX reading PDF for the paper workspace.

This script keeps the journal-facing Markdown export workflow intact while
adding a higher-quality reading PDF:

- regenerates the paper figures from their source scripts
- compiles `paper/manuscript/paper.tex` with Tectonic
- copies the resulting PDF into `paper/submission/`
- refreshes the tracked `paper/share/` copy used for GitHub and cross-device reading
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
MANUSCRIPT_DIR = REPO_ROOT / "paper" / "manuscript"
LATEX_SOURCE = MANUSCRIPT_DIR / "paper.tex"
LATEX_PDF = MANUSCRIPT_DIR / "paper.pdf"
SUBMISSION_DIR = REPO_ROOT / "paper" / "submission"
OUT_PDF = SUBMISSION_DIR / "waste-management-manuscript-latex.pdf"
SHARE_DIR = REPO_ROOT / "paper" / "share"
SHARE_PDF = SHARE_DIR / "waste-management-manuscript-latex.pdf"
FIGURE1_SCRIPT = REPO_ROOT / "paper" / "figures" / "build_figure1_two_part_framework.py"
FIGURE2_SCRIPT = REPO_ROOT / "paper" / "figures" / "build_figure2_selective_transition.py"
FIGURE3_SCRIPT = REPO_ROOT / "paper" / "figures" / "build_figure3_efficiency_structure.py"


def tectonic_binary() -> str:
    tectonic = shutil.which("tectonic")
    if tectonic:
        return tectonic

    local_binary = Path.home() / ".local" / "bin" / "tectonic"
    if local_binary.exists():
        return str(local_binary)

    raise SystemExit("Tectonic not found; cannot compile the LaTeX manuscript.")

def build_figures() -> None:
    for script in (FIGURE1_SCRIPT, FIGURE2_SCRIPT, FIGURE3_SCRIPT):
        if not script.exists():
            raise SystemExit(f"Figure build script not found: {script}")
        subprocess.run([sys.executable, str(script)], check=True)


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
    parser.parse_args()

    if not LATEX_SOURCE.exists():
        raise SystemExit(f"LaTeX manuscript not found: {LATEX_SOURCE}")

    SUBMISSION_DIR.mkdir(parents=True, exist_ok=True)
    SHARE_DIR.mkdir(parents=True, exist_ok=True)
    build_figures()

    tectonic = tectonic_binary()
    compile_latex(tectonic)
    shutil.copy2(LATEX_PDF, OUT_PDF)
    shutil.copy2(LATEX_PDF, SHARE_PDF)

    print(f"LaTeX manuscript source: {LATEX_SOURCE}")
    print("Rendered figure assets: paper/figures/")
    print(f"LaTeX manuscript PDF: {OUT_PDF}")
    print(f"Tracked share PDF: {SHARE_PDF}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
