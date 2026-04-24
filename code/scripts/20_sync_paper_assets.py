#!/usr/bin/env python3
"""Sync canonical thesis outputs into the active paper workspace."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = REPO_ROOT / "output"
PAPER_DIR = REPO_ROOT / "paper"
CURRENT_DIR = PAPER_DIR / "evidence" / "current"

SOURCE_FILES = [
    "sample_definition.md",
    "adoption_results.md",
    "regression_results.md",
    "robustness_results.md",
    "data_quality_sensitivity.md",
    "claim_evidence_map.md",
    "claim_verification.md",
    "panel_summary.md",
    "table1_summary_stats.md",
    "table2_efficiency_by_age.md",
    "adoption_pathway_audit.csv",
]


def check_sources() -> list[str]:
    missing = []
    for filename in SOURCE_FILES:
        if not (OUTPUT_DIR / filename).exists():
            missing.append(filename)
    return missing


def write_index() -> Path:
    CURRENT_DIR.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Paper Evidence Snapshot",
        "",
        "This directory is a paper-facing copy of the canonical output artifacts.",
        "",
        "- source repo state: canonical paper-workspace outputs",
        f"- source directory: `{OUTPUT_DIR.relative_to(REPO_ROOT)}`",
        f"- target directory: `{CURRENT_DIR.relative_to(REPO_ROOT)}`",
        "",
        "Use these files when drafting the paper so the manuscript stays downstream of the empirical core.",
        "",
        "## Synced Artifacts",
        "",
    ]
    for filename in SOURCE_FILES:
        lines.append(f"- `{filename}`")
    lines.append("")
    lines.append("## Rule")
    lines.append("")
    lines.append("If the outputs change materially, rerun `npm run paper:sync` before updating paper-facing claims.")
    lines.append("")
    target = PAPER_DIR / "evidence" / "README.md"
    target.write_text("\n".join(lines), encoding="utf-8")
    return target


def sync() -> None:
    missing = check_sources()
    if missing:
        raise SystemExit(
            "Missing canonical output artifacts:\n- " + "\n- ".join(missing)
        )
    CURRENT_DIR.mkdir(parents=True, exist_ok=True)
    for filename in SOURCE_FILES:
        shutil.copy2(OUTPUT_DIR / filename, CURRENT_DIR / filename)
    index = write_index()
    print(f"Synced {len(SOURCE_FILES)} artifacts to {CURRENT_DIR}")
    print(f"Wrote evidence index: {index}")


def check() -> None:
    missing = check_sources()
    if missing:
        raise SystemExit(
            "Missing canonical output artifacts:\n- " + "\n- ".join(missing)
        )
    print("Paper evidence sources are available.")
    for filename in SOURCE_FILES:
        print(f"- output/{filename}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="verify source artifacts only")
    args = parser.parse_args()

    if args.check:
        check()
    else:
        sync()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
