#!/usr/bin/env python3
"""Freeze a sendable checkpoint from the current verified repo state."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
DIST_ROOT = REPO_ROOT / "research" / "checkpoints" / "dist"
PACKET_ROOT = REPO_ROOT / "research" / "packets" / "dist"
SUPERVISOR_ZIP = PACKET_ROOT / "supervisor-packet.zip"
SUBMISSION_ZIP = PACKET_ROOT / "submission-packet.zip"


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=REPO_ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def repo_sha() -> str:
    return run(["git", "rev-parse", "HEAD"]).stdout.strip()


def current_branch() -> str:
    return run(["git", "rev-parse", "--abbrev-ref", "HEAD"]).stdout.strip()


def worktree_dirty() -> bool:
    status = run(["git", "status", "--porcelain"]).stdout.strip()
    return bool(status)


def ensure_packets() -> None:
    subprocess.run([sys.executable, "code/scripts/11_package_review_packets.py"], cwd=REPO_ROOT, check=True)


def safe_slug(value: str) -> str:
    slug = "".join(ch.lower() if ch.isalnum() else "-" for ch in value).strip("-")
    return "-".join(part for part in slug.split("-") if part)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Freeze a local sendable checkpoint from the current verified repo state."
    )
    parser.add_argument(
        "--label",
        default="sendable-now",
        help="Short checkpoint label used in the folder name and suggested tag.",
    )
    parser.add_argument(
        "--allow-dirty",
        action="store_true",
        help="Allow checkpoint creation even if the git worktree is dirty.",
    )
    parser.add_argument(
        "--create-tag",
        action="store_true",
        help="Create a local annotated git tag after the checkpoint is assembled.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if worktree_dirty() and not args.allow_dirty:
        print(
            "Refusing to freeze a checkpoint from a dirty worktree. "
            "Commit first or rerun with --allow-dirty.",
            file=sys.stderr,
        )
        return 1

    ensure_packets()

    label = safe_slug(args.label)
    sha = repo_sha()
    short_sha = sha[:7]
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    date_slug = generated_at[:10].replace("-", "")
    checkpoint_name = f"{date_slug}-{label}-{short_sha}"
    checkpoint_root = DIST_ROOT / checkpoint_name
    if checkpoint_root.exists():
        shutil.rmtree(checkpoint_root)
    checkpoint_root.mkdir(parents=True, exist_ok=True)

    shutil.copy2(SUPERVISOR_ZIP, checkpoint_root / SUPERVISOR_ZIP.name)
    shutil.copy2(SUBMISSION_ZIP, checkpoint_root / SUBMISSION_ZIP.name)

    suggested_tag = f"{label}-{date_slug}-{short_sha}"
    metadata = {
        "generated_at_utc": generated_at,
        "repo_git_sha": sha,
        "branch": current_branch(),
        "worktree_dirty": worktree_dirty(),
        "suggested_tag": suggested_tag,
        "supervisor_packet": {
            "path": SUPERVISOR_ZIP.name,
            "sha256": sha256(SUPERVISOR_ZIP),
        },
        "submission_packet": {
            "path": SUBMISSION_ZIP.name,
            "sha256": sha256(SUBMISSION_ZIP),
        },
    }
    (checkpoint_root / "checkpoint-metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    (checkpoint_root / "README.md").write_text(
        f"""# Frozen Checkpoint

- Generated at: {generated_at}
- Branch: `{metadata["branch"]}`
- Repo git SHA: `{sha}`
- Worktree dirty at freeze time: `{metadata["worktree_dirty"]}`
- Suggested git tag: `{suggested_tag}`

## Included artifacts

- `supervisor-packet.zip`
- `submission-packet.zip`
- `checkpoint-metadata.json`

## Recommended next step

1. Review the packet ZIPs.
2. If this is the sendable state, create a git tag such as `{suggested_tag}`.
3. Keep this checkpoint as the reference baseline for the next supervisor or submission milestone.
"""
    )

    if args.create_tag:
        subprocess.run(
            [
                "git",
                "tag",
                "-a",
                suggested_tag,
                "-m",
                f"Frozen checkpoint {suggested_tag}",
            ],
            cwd=REPO_ROOT,
            check=True,
        )
        print(f"Created local git tag: {suggested_tag}")

    print(f"Frozen checkpoint: {checkpoint_root.relative_to(REPO_ROOT)}")
    print(f"Suggested tag:    {suggested_tag}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
