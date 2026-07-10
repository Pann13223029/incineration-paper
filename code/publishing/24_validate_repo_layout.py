#!/usr/bin/env python3
"""Validate repository ownership boundaries and tracked Markdown links."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path
from urllib.parse import unquote


REPO_ROOT = Path(__file__).resolve().parents[2]

REQUIRED_PATHS = [
    "code/analysis/07_rebuild_analysis.py",
    "code/analysis/08_verify_claims.py",
    "code/publishing/20_sync_paper_assets.py",
    "paper/manuscript/paper.md",
    "paper/manuscript/paper.tex",
    "paper/notes/planning",
    "paper/notes/positioning",
    "paper/notes/review",
    "paper/share/waste-management-manuscript-latex.pdf",
    "legacy/thesis/thesis.tex",
    "legacy/research",
    "legacy/scripts",
]

RETIRED_PATHS = ["code/scripts", "thesis", "research"]

ACTIVE_STALE_REFERENCES = {
    "code/scripts/": "use code/analysis/ or code/publishing/",
    "paper/notes/claim-stack.md": "use paper/notes/positioning/claim-stack.md",
    "paper/notes/professor-comparator-method-lineage.md": (
        "use paper/notes/positioning/professor-comparator-method-lineage.md"
    ),
}

LINK_RE = re.compile(r"!?(?:\[[^\]]*\])\(([^)]+)\)")


def tracked_markdown_files() -> list[Path]:
    result = subprocess.run(
        [
            "git",
            "ls-files",
            "--cached",
            "--others",
            "--exclude-standard",
            "--",
            "*.md",
        ],
        cwd=REPO_ROOT,
        check=True,
        stdout=subprocess.PIPE,
        text=True,
    )
    return [REPO_ROOT / line for line in result.stdout.splitlines() if line]


def normalize_link_target(raw_target: str) -> str:
    target = raw_target.strip().strip("<>")
    if " " in target and not target.startswith(("http://", "https://")):
        target = target.split(" ", 1)[0]
    return unquote(target.split("#", 1)[0].split("?", 1)[0])


def check_markdown_links(paths: list[Path]) -> list[str]:
    errors: list[str] = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        for match in LINK_RE.finditer(text):
            target = normalize_link_target(match.group(1))
            if not target or target.startswith(("#", "http://", "https://", "mailto:", "data:")):
                continue
            if target.startswith("/"):
                errors.append(
                    f"{path.relative_to(REPO_ROOT)}: host-absolute link is not portable: {target}"
                )
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                errors.append(
                    f"{path.relative_to(REPO_ROOT)}: missing link target: {target}"
                )
    return errors


def check_active_stale_references(paths: list[Path]) -> list[str]:
    errors: list[str] = []
    for path in paths:
        relative = path.relative_to(REPO_ROOT)
        if relative.parts and relative.parts[0] == "legacy":
            continue
        text = path.read_text(encoding="utf-8")
        for stale, replacement in ACTIVE_STALE_REFERENCES.items():
            if stale in text:
                errors.append(f"{relative}: stale `{stale}`; {replacement}")
    return errors


def main() -> int:
    errors: list[str] = []
    for relative in REQUIRED_PATHS:
        if not (REPO_ROOT / relative).exists():
            errors.append(f"required path is missing: {relative}")
    for relative in RETIRED_PATHS:
        if (REPO_ROOT / relative).exists():
            errors.append(f"retired path still exists: {relative}")

    markdown_paths = tracked_markdown_files()
    errors.extend(check_markdown_links(markdown_paths))
    errors.extend(check_active_stale_references(markdown_paths))

    if errors:
        print("Repository layout validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "Repository layout validation passed: "
        f"{len(REQUIRED_PATHS)} required paths and "
        f"{len(markdown_paths)} tracked Markdown files checked."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
