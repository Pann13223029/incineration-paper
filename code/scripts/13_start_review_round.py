#!/usr/bin/env python3
"""Create a structured local workspace for a supervisor/review feedback round."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
DIST_ROOT = REPO_ROOT / "research" / "review-rounds" / "dist"
PACKET_ROOT = REPO_ROOT / "research" / "packets" / "dist"
SUPERVISOR_ZIP = PACKET_ROOT / "supervisor-packet.zip"


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=REPO_ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def repo_sha() -> str:
    return run(["git", "rev-parse", "HEAD"]).stdout.strip()


def current_branch() -> str:
    return run(["git", "rev-parse", "--abbrev-ref", "HEAD"]).stdout.strip()


def worktree_dirty() -> bool:
    return bool(run(["git", "status", "--porcelain"]).stdout.strip())


def resolve_python() -> str:
    venv_python = REPO_ROOT / ".venv" / "bin" / "python"
    if venv_python.exists():
        return str(venv_python)
    return sys.executable


def ensure_supervisor_packet() -> None:
    if SUPERVISOR_ZIP.exists():
        return
    subprocess.run([resolve_python(), "code/scripts/11_package_review_packets.py"], cwd=REPO_ROOT, check=True)


def safe_slug(value: str) -> str:
    slug = "".join(ch.lower() if ch.isalnum() else "-" for ch in value).strip("-")
    return "-".join(part for part in slug.split("-") if part)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a dated review-round workspace anchored to the current supervisor packet."
    )
    parser.add_argument(
        "--label",
        default="supervisor-feedback",
        help="Short label used in the review-round directory name.",
    )
    parser.add_argument(
        "--allow-dirty",
        action="store_true",
        help="Allow review-round creation even if the git worktree is dirty.",
    )
    return parser.parse_args()


def write_feedback_intake(path: Path) -> None:
    path.write_text(
        """# Feedback Intake

Record each supervisor or reviewer comment as one row. Keep comments granular:
one criticism, ambiguity, or requested change per row.

| ID | Source | Comment | Class | Severity | Linked artifact | Initial reading | Proposed action | Status |
|:---|:-------|:--------|:------|:---------|:----------------|:----------------|:----------------|:-------|
| 1 | supervisor | | empirical design / evidence / logic / writing / citation / formatting / workflow | high / medium / low | thesis.tex / output/* / README / slide / packet | misunderstanding / real weakness / wording issue / open question | accept / narrow / test / reject / defer | open |

## Triage rules

1. Split bundled comments into separate rows.
2. Link each row to the exact artifact it touches.
3. If the comment is valid, decide whether the fix is `wording`, `analysis`, or `scope`.
4. If the comment is invalid or based on a misunderstanding, draft the narrow rebuttal anyway.
5. Do not mark a row `closed` until the underlying repo change or response memo exists.
""",
        encoding="utf-8",
    )


def write_decision_log(path: Path) -> None:
    path.write_text(
        """# Revision Decision Log

Use this after triage to record what the repo actually changed and why.

| Decision ID | Trigger row(s) | Decision | Why | Repo change needed | Verification | Closed |
|:------------|:---------------|:---------|:----|:-------------------|:------------|:-------|
| D1 |  | accept / narrow / test / reject / defer | | thesis / code / output / packet / none | rebuild / verify / packet / slide / none | no |

## Notes

- `accept`: the feedback is right and the thesis should change.
- `narrow`: the core evidence stays, but the wording or scope should tighten.
- `test`: run extra analysis before deciding.
- `reject`: keep the thesis as-is and prepare a response.
- `defer`: valid point, but outside the defended scope or current timeline.
""",
        encoding="utf-8",
    )


def write_response_memo(path: Path) -> None:
    path.write_text(
        """# Response Draft

Use this file to draft a concise reply or update note after triage.

## Round summary

- Packet baseline:
- Main themes in feedback:
- Highest-risk issue:
- Biggest accepted change:
- Biggest rejected or narrowed point:

## Reply draft

Thank you for the feedback. I have grouped the comments into:

1. comments requiring direct thesis revision
2. comments resolved by narrowing or clarifying the claim
3. comments that identify limitations already acknowledged in the thesis

The linked intake table and decision log record the exact disposition of each point.
""",
        encoding="utf-8",
    )


def main() -> int:
    args = parse_args()
    if worktree_dirty() and not args.allow_dirty:
        print(
            "Refusing to start a review round from a dirty worktree. "
            "Commit first or rerun with --allow-dirty.",
            file=sys.stderr,
        )
        return 1

    ensure_supervisor_packet()

    sha = repo_sha()
    short_sha = sha[:7]
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    date_slug = generated_at[:10].replace("-", "")
    round_name = f"{date_slug}-{safe_slug(args.label)}-{short_sha}"
    round_root = DIST_ROOT / round_name
    if round_root.exists():
        shutil.rmtree(round_root)
    round_root.mkdir(parents=True, exist_ok=True)

    shutil.copy2(SUPERVISOR_ZIP, round_root / SUPERVISOR_ZIP.name)

    metadata = {
        "generated_at_utc": generated_at,
        "repo_git_sha": sha,
        "branch": current_branch(),
        "worktree_dirty": worktree_dirty(),
        "packet_baseline": SUPERVISOR_ZIP.name,
    }
    (round_root / "round-metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    (round_root / "README.md").write_text(
        f"""# Review Round

- Generated at: {generated_at}
- Branch: `{metadata["branch"]}`
- Repo git SHA: `{sha}`
- Worktree dirty at creation time: `{metadata["worktree_dirty"]}`
- Baseline packet: `supervisor-packet.zip`

## Files

- `supervisor-packet.zip`: exact packet baseline for this round
- `feedback-intake.md`: row-by-row comment triage
- `revision-decision-log.md`: disposition of each accepted / narrowed / rejected point
- `response-draft.md`: concise summary reply or update memo

## Recommended flow

1. Read the packet actually sent.
2. Enter every supervisor comment into `feedback-intake.md`.
3. Convert the rows into actions in `revision-decision-log.md`.
4. Only then start changing the repo.
""",
        encoding="utf-8",
    )

    write_feedback_intake(round_root / "feedback-intake.md")
    write_decision_log(round_root / "revision-decision-log.md")
    write_response_memo(round_root / "response-draft.md")

    print(f"Created review round: {round_root.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
