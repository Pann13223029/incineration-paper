#!/usr/bin/env python3
"""Generate a compact summary of changes since the last sendable checkpoint."""

from __future__ import annotations

import subprocess
from collections import defaultdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_PATH = REPO_ROOT / "output" / "checkpoint_delta.md"


def run(command: list[str]) -> str:
    result = subprocess.run(
        command,
        cwd=REPO_ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result.stdout.strip()


def head_sha() -> str:
    return run(["git", "rev-parse", "HEAD"])


def head_short() -> str:
    return run(["git", "rev-parse", "--short", "HEAD"])


def tags_pointing_at_head() -> set[str]:
    tags = run(["git", "tag", "--points-at", "HEAD"])
    return {tag for tag in tags.splitlines() if tag}


def sendable_tags() -> list[str]:
    tags = run(["git", "tag", "--list", "sendable-now-*", "--sort=-creatordate"])
    return [tag for tag in tags.splitlines() if tag]


def latest_distinct_baseline_tag() -> str | None:
    head_tags = tags_pointing_at_head()
    for tag in sendable_tags():
        if tag not in head_tags:
            return tag
    return None


def tag_sha(tag: str) -> str:
    return run(["git", "rev-list", "-n", "1", tag])


def commits_since(tag: str) -> list[str]:
    log = run(["git", "log", "--format=%h %s", f"{tag}..HEAD"])
    return [line for line in log.splitlines() if line]


def files_since(tag: str) -> list[str]:
    diff = run(["git", "diff", "--name-only", f"{tag}..HEAD"])
    return [line for line in diff.splitlines() if line]


def classify_path(path: str) -> str:
    if path == "output/checkpoint_delta.md":
        return "Workflow and repo operations"
    if path.startswith("thesis/") or path.startswith("output/") or path.startswith("code/scripts/05") or path.startswith("code/scripts/06") or path.startswith("code/scripts/07") or path.startswith("code/scripts/08"):
        return "Thesis and empirical core"
    if path.startswith("research/notes/") or path.startswith("research/slides/") or path.startswith("research/packets/"):
        return "Supervisor and defense materials"
    if path.startswith(".github/") or path.startswith("research/review-rounds/") or path.startswith("code/scripts/09") or path.startswith("code/scripts/10") or path.startswith("code/scripts/11") or path.startswith("code/scripts/12") or path.startswith("code/scripts/13") or path.startswith("code/scripts/14") or path in {"README.md", "ARCHITECTURE.md", "AGENTS.md", "package.json", ".gitignore", ".node-version"}:
        return "Workflow and repo operations"
    return "Other"


def interpret_delta(grouped: dict[str, list[str]]) -> str:
    if grouped.get("Thesis and empirical core"):
        return "This packet should be read as a substantive thesis revision, because the thesis core or defended empirical outputs changed."
    if grouped.get("Supervisor and defense materials"):
        return "This packet should be read as a support-layer revision, because the defended thesis stayed stable while supervisor or defense materials changed."
    if grouped.get("Workflow and repo operations"):
        return "This packet should be read as operational hardening, because the defended thesis stayed stable while workflow or review tooling changed."
    return "This packet should be read as a minor repo update with no detected thesis-core change."


def write_no_delta(tag: str | None) -> None:
    lines = [
        "# Changes Since Last Frozen Checkpoint",
        "",
        f"- Current HEAD: `{head_short()}`",
    ]
    if tag:
        lines.append(f"- Current frozen checkpoint tag: `{tag}`")
        lines.append("- Delta status: no changes since the current frozen checkpoint.")
    else:
        lines.append("- Delta status: no prior sendable checkpoint tag found.")
    lines.extend(
        [
            "",
            "This packet matches the latest frozen sendable baseline.",
        ]
    )
    OUTPUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    head_tags = tags_pointing_at_head()
    baseline_tag = latest_distinct_baseline_tag()

    if not baseline_tag:
        current_tag = next(iter(sorted(head_tags))) if head_tags else None
        write_no_delta(current_tag)
        return 0

    commit_lines = commits_since(baseline_tag)
    file_lines = files_since(baseline_tag)
    if not commit_lines and head_tags:
        current_tag = next(iter(sorted(head_tags)))
        write_no_delta(current_tag)
        return 0

    grouped: dict[str, list[str]] = defaultdict(list)
    for path in file_lines:
        grouped[classify_path(path)].append(path)

    lines = [
        "# Changes Since Last Frozen Checkpoint",
        "",
        f"- Current HEAD: `{head_short()}`",
        f"- Baseline checkpoint tag: `{baseline_tag}`",
        f"- Baseline SHA: `{tag_sha(baseline_tag)[:7]}`",
        f"- Commits since baseline: `{len(commit_lines)}`",
        "",
        "## Commit Summary",
        "",
    ]
    if commit_lines:
        lines.extend(f"- `{line}`" for line in commit_lines)
    else:
        lines.append("- None")

    lines.extend(["", "## Changed Areas", ""])
    for section in ["Thesis and empirical core", "Supervisor and defense materials", "Workflow and repo operations", "Other"]:
        paths = grouped.get(section, [])
        if not paths:
            continue
        lines.append(f"### {section}")
        for path in paths:
            lines.append(f"- `{path}`")
        lines.append("")

    lines.extend(
        [
            "## Interpretation",
            "",
            interpret_delta(grouped),
            "",
            "## Reviewer Guidance",
            "",
            "Use this file to answer the first supervisor question quickly:",
            "",
            "1. What changed since the last sendable version?",
            "2. Which layer changed: thesis core, support material, or workflow?",
            "3. Should the new packet be read as a substantive revision or as operational hardening?",
        ]
    )

    OUTPUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote checkpoint delta: {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
