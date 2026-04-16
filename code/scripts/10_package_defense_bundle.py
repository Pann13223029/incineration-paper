#!/usr/bin/env python3
"""Assemble a frozen local defense bundle from the current repo state."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


REPO_ROOT = Path(__file__).resolve().parents[2]
DIST_ROOT = REPO_ROOT / "research" / "slides" / "dist"
BUNDLE_ROOT = DIST_ROOT / "defense-bundle"
ZIP_PATH = DIST_ROOT / "defense-bundle.zip"

FILES_TO_COPY: list[tuple[str, str | None]] = [
    ("research/slides/defense-deck.md", None),
    ("research/slides/dist/defense-deck.html", "research/slides/defense-deck.html"),
    ("research/slides/themes/defense-apu.css", None),
    ("research/notes/final-viva-cheat-sheet.md", None),
    ("research/notes/defense-rapid-answers.md", None),
    ("research/notes/defense-run-sheet.md", None),
    ("research/notes/defense-question-order.md", None),
    ("research/notes/defense-q-and-a.md", None),
    ("research/notes/executive-summary-for-supervisor.md", None),
    ("research/notes/what-this-thesis-does-not-claim.md", None),
    ("output/claim_verification.md", None),
    ("output/adoption_results.md", None),
    ("output/regression_results.md", None),
]

DIRS_TO_COPY = [
    "research/slides/figures",
    "docs/figures",
]


def repo_git_sha() -> str:
    result = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "rev-parse", "HEAD"],
        check=True,
        stdout=subprocess.PIPE,
        text=True,
    )
    return result.stdout.strip()


def run_slide_export() -> None:
    subprocess.run(
        ["python3", "code/scripts/09_export_defense_slides.py"],
        cwd=REPO_ROOT,
        check=True,
    )


def relative_path(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def parse_claim_verification_status() -> tuple[str, int | None, int | None]:
    report = (REPO_ROOT / "output" / "claim_verification.md").read_text()
    result_match = re.search(r"## Result: (\w+)", report)
    passed_match = re.search(r"- Passed checks: (\d+)", report)
    failed_match = re.search(r"- Failed checks: (\d+)", report)
    status = result_match.group(1) if result_match else "UNKNOWN"
    passed = int(passed_match.group(1)) if passed_match else None
    failed = int(failed_match.group(1)) if failed_match else None
    return status, passed, failed


def reset_bundle_root() -> None:
    if BUNDLE_ROOT.exists():
        shutil.rmtree(BUNDLE_ROOT)
    BUNDLE_ROOT.mkdir(parents=True, exist_ok=True)


def copy_inputs() -> list[str]:
    copied: list[str] = []
    for src_rel, dest_rel in FILES_TO_COPY:
        src = REPO_ROOT / src_rel
        bundle_rel = dest_rel or src_rel
        dest = BUNDLE_ROOT / bundle_rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        copied.append(bundle_rel)
    for rel in DIRS_TO_COPY:
        src = REPO_ROOT / rel
        dest = BUNDLE_ROOT / rel
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(src, dest)
        copied.append(rel + "/")
    return copied


def write_bundle_readme(metadata: dict) -> None:
    content = f"""# Defense Bundle

Frozen local defense packet assembled from the current repo state.

- Generated at: {metadata["generated_at_utc"]}
- Repo git SHA: `{metadata["repo_git_sha"]}`
- Claim verification status: `{metadata["claim_verification"]["status"]}`
- Passed checks: `{metadata["claim_verification"]["passed_checks"]}`
- Failed checks: `{metadata["claim_verification"]["failed_checks"]}`

## Start here

1. Open `research/slides/defense-deck.html` in a browser for the presentation view.
2. Use `research/notes/final-viva-cheat-sheet.md` as the main oral-defense rehearsal sheet.
3. Use `research/notes/defense-run-sheet.md` for timed delivery.
4. Use `research/notes/defense-rapid-answers.md` for short-answer rehearsal.
5. Use `research/notes/defense-q-and-a.md` for hostile follow-up practice.
6. Use `output/claim_verification.md` to confirm the thesis-facing evidence spine.

## Included artifacts

- HTML deck: `research/slides/defense-deck.html`
- Slide source: `research/slides/defense-deck.md`
- Slide figures and theme: `research/slides/figures/`, `research/slides/themes/`
- Rehearsal notes: `research/notes/`
- Main viva cheat sheet: `research/notes/final-viva-cheat-sheet.md`
- Verification and core results: `output/claim_verification.md`, `output/adoption_results.md`, `output/regression_results.md`
"""
    (BUNDLE_ROOT / "README.md").write_text(content)


def write_metadata(copied: list[str], metadata: dict) -> None:
    metadata = {**metadata, "included_paths": copied}
    (BUNDLE_ROOT / "bundle-metadata.json").write_text(
        json.dumps(metadata, indent=2) + "\n"
    )


def write_zip_archive() -> None:
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    with ZipFile(ZIP_PATH, "w", compression=ZIP_DEFLATED) as zf:
        for path in BUNDLE_ROOT.rglob("*"):
            zf.write(path, arcname=path.relative_to(DIST_ROOT))


def main() -> int:
    DIST_ROOT.mkdir(parents=True, exist_ok=True)
    run_slide_export()

    status, passed, failed = parse_claim_verification_status()
    metadata = {
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "repo_git_sha": repo_git_sha(),
        "claim_verification": {
            "status": status,
            "passed_checks": passed,
            "failed_checks": failed,
        },
    }

    reset_bundle_root()
    copied = copy_inputs()
    write_bundle_readme(metadata)
    write_metadata(copied, metadata)
    write_zip_archive()

    print(f"Prepared defense bundle directory: {relative_path(BUNDLE_ROOT)}")
    print(f"Prepared defense bundle zip:       {relative_path(ZIP_PATH)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
