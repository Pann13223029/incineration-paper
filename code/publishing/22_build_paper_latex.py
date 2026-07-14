#!/usr/bin/env python3
"""Build a clean LaTeX reading PDF for a manuscript profile.

This script keeps the journal-facing Markdown export workflow intact while
adding a higher-quality reading PDF:

- regenerates the paper figures from their source scripts
- compiles the journal-facing or professor-facing source with Tectonic
- refreshes the corresponding tracked `paper/share/` reading copy
- copies the journal-facing PDF into `paper/submission/`
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
MANUSCRIPT_ROOT = REPO_ROOT / "paper" / "manuscript"
SUBMISSION_DIR = REPO_ROOT / "paper" / "submission"
SHARE_DIR = REPO_ROOT / "paper" / "share"
FIGURE1_SCRIPT = REPO_ROOT / "paper" / "figures" / "build_figure1_two_part_framework.py"
FIGURE2_SCRIPT = REPO_ROOT / "paper" / "figures" / "build_figure2_selective_transition.py"
FIGURE3_SCRIPT = REPO_ROOT / "paper" / "figures" / "build_figure3_efficiency_structure.py"
FIGURE4_SCRIPT = REPO_ROOT / "paper" / "figures" / "build_figure4_post_entry_trajectories.py"


def tectonic_binary() -> str:
    tectonic = shutil.which("tectonic")
    if tectonic:
        return tectonic

    local_binary = Path.home() / ".local" / "bin" / "tectonic"
    if local_binary.exists():
        return str(local_binary)

    raise SystemExit("Tectonic not found; cannot compile the LaTeX manuscript.")


def build_figures() -> None:
    for script in (FIGURE1_SCRIPT, FIGURE2_SCRIPT, FIGURE3_SCRIPT, FIGURE4_SCRIPT):
        if not script.exists():
            raise SystemExit(f"Figure build script not found: {script}")
        subprocess.run([sys.executable, str(script)], check=True)


def compile_latex(tectonic: str, manuscript_dir: Path, latex_source: Path) -> Path:
    latex_pdf = manuscript_dir / "paper.pdf"
    previous_mtime_ns = latex_pdf.stat().st_mtime_ns if latex_pdf.exists() else None
    command = [
        tectonic,
        "-p",
        "--keep-logs",
        "--keep-intermediates",
        latex_source.name,
    ]
    subprocess.run(command, cwd=manuscript_dir, check=True)
    if not latex_pdf.exists():
        raise SystemExit(f"Tectonic did not produce the expected PDF: {latex_pdf}")
    if previous_mtime_ns is not None and latex_pdf.stat().st_mtime_ns == previous_mtime_ns:
        raise SystemExit(f"Tectonic did not refresh the expected PDF: {latex_pdf}")
    return latex_pdf


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--profile",
        choices=("journal", "professor"),
        default="journal",
        help="Build the public journal draft or the comprehensive professor draft.",
    )
    args = parser.parse_args()

    if args.profile == "journal":
        manuscript_dir = MANUSCRIPT_ROOT
        out_pdf = SUBMISSION_DIR / "waste-management-manuscript-latex.pdf"
        share_pdf = SHARE_DIR / "waste-management-manuscript-latex.pdf"
    else:
        manuscript_dir = MANUSCRIPT_ROOT / "professor"
        out_pdf = None
        share_pdf = SHARE_DIR / "professor-review-manuscript-latex.pdf"

    latex_source = manuscript_dir / "paper.tex"

    if not latex_source.exists():
        raise SystemExit(f"LaTeX manuscript not found: {latex_source}")

    SUBMISSION_DIR.mkdir(parents=True, exist_ok=True)
    SHARE_DIR.mkdir(parents=True, exist_ok=True)
    build_figures()

    tectonic = tectonic_binary()
    latex_pdf = compile_latex(tectonic, manuscript_dir, latex_source)
    if out_pdf is not None:
        shutil.copy2(latex_pdf, out_pdf)
    shutil.copy2(latex_pdf, share_pdf)

    print(f"Manuscript profile: {args.profile}")
    print(f"LaTeX manuscript source: {latex_source}")
    print("Rendered figure assets: paper/figures/")
    if out_pdf is not None:
        print(f"LaTeX manuscript PDF: {out_pdf}")
    print(f"Tracked share PDF: {share_pdf}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
