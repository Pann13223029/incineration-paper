#!/usr/bin/env python3
"""Build a flattened supervisor handoff bundle with simple filenames."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile


REPO_ROOT = Path(__file__).resolve().parents[2]
PACKET_ROOT = REPO_ROOT / "research" / "packets" / "dist"
SUPERVISOR_PACKET_ROOT = PACKET_ROOT / "supervisor-packet"
HANDOFF_ROOT = PACKET_ROOT / "supervisor-handoff"
HANDOFF_ZIP = PACKET_ROOT / "supervisor-handoff.zip"
LATEST_ALIAS = REPO_ROOT / "research" / "packets" / "latest-supervisor-handoff"

THESIS_PDF = SUPERVISOR_PACKET_ROOT / "thesis" / "thesis.pdf"
SUMMARY = SUPERVISOR_PACKET_ROOT / "research" / "notes" / "executive-summary-for-supervisor.md"
RISK_REGISTER = SUPERVISOR_PACKET_ROOT / "research" / "notes" / "examiner-risk-register.md"
NON_CLAIMS = SUPERVISOR_PACKET_ROOT / "research" / "notes" / "what-this-thesis-does-not-claim.md"
DELTA = SUPERVISOR_PACKET_ROOT / "output" / "checkpoint_delta.md"
CLAIM_MAP = SUPERVISOR_PACKET_ROOT / "output" / "claim_evidence_map.md"
CLAIM_REPORT = SUPERVISOR_PACKET_ROOT / "output" / "claim_verification.md"
PACKET_METADATA = SUPERVISOR_PACKET_ROOT / "packet-metadata.json"


def run(command: list[str]) -> None:
    subprocess.run(command, cwd=REPO_ROOT, check=True)


def reset_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_text(dest: Path, source: Path) -> None:
    dest.write_text(source.read_text())


def refresh_latest_alias() -> None:
    if LATEST_ALIAS.is_symlink() or LATEST_ALIAS.is_file():
        LATEST_ALIAS.unlink()
    elif LATEST_ALIAS.exists():
        shutil.rmtree(LATEST_ALIAS)

    try:
        LATEST_ALIAS.symlink_to(Path("dist") / HANDOFF_ROOT.name, target_is_directory=True)
    except OSError:
        LATEST_ALIAS.mkdir(parents=True, exist_ok=True)
        (LATEST_ALIAS / "README.txt").write_text(
            "Open research/packets/dist/supervisor-handoff for the latest supervisor bundle.\n"
        )


def zip_dir(src: Path, dest_zip: Path) -> None:
    if dest_zip.exists():
        dest_zip.unlink()
    with ZipFile(dest_zip, "w", compression=ZIP_DEFLATED) as zf:
        for path in sorted(src.rglob("*")):
            zf.write(path, arcname=path.relative_to(PACKET_ROOT))


def build_handoff() -> None:
    run([sys.executable, "code/scripts/11_package_review_packets.py"])

    reset_dir(HANDOFF_ROOT)
    metadata = json.loads(PACKET_METADATA.read_text())
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    shutil.copy2(THESIS_PDF, HANDOFF_ROOT / "01_Thesis.pdf")
    write_text(HANDOFF_ROOT / "02_One_Page_Summary.txt", SUMMARY)
    write_text(HANDOFF_ROOT / "03_What_Changed_Since_Last_Send.txt", DELTA)
    write_text(HANDOFF_ROOT / "04_Key_Claims_And_Evidence.txt", CLAIM_MAP)
    write_text(HANDOFF_ROOT / "05_Main_Risks_And_Mitigations.txt", RISK_REGISTER)
    write_text(HANDOFF_ROOT / "06_What_This_Thesis_Does_Not_Claim.txt", NON_CLAIMS)
    write_text(HANDOFF_ROOT / "07_Claim_Verification_Report.txt", CLAIM_REPORT)

    (HANDOFF_ROOT / "00_START_HERE.txt").write_text(
        f"""Supervisor Review Bundle

This folder is the simplified review handoff. No GitHub or repo navigation is required.

Recommended reading order:
1. Open `01_Thesis.pdf`
2. Read `02_One_Page_Summary.txt`
3. Read `03_What_Changed_Since_Last_Send.txt`
4. If useful, scan `05_Main_Risks_And_Mitigations.txt`
5. Use `04_Key_Claims_And_Evidence.txt` only if you want a compact map from headline claims to supporting outputs

Bundle details:
- Generated at: {generated_at}
- Repo git SHA: {metadata["repo_git_sha"]}
- Thesis PDF SHA256: {metadata["thesis_pdf_sha256"]}

Send this ZIP or this folder directly. The rest of the repo is not required for normal review.
"""
    )

    handoff_metadata = {
        "generated_at_utc": generated_at,
        "repo_git_sha": metadata["repo_git_sha"],
        "thesis_pdf_sha256": sha256(HANDOFF_ROOT / "01_Thesis.pdf"),
        "source_supervisor_packet_sha256": sha256(REPO_ROOT / "research" / "packets" / "dist" / "supervisor-packet.zip"),
        "included_files": [
            "00_START_HERE.txt",
            "01_Thesis.pdf",
            "02_One_Page_Summary.txt",
            "03_What_Changed_Since_Last_Send.txt",
            "04_Key_Claims_And_Evidence.txt",
            "05_Main_Risks_And_Mitigations.txt",
            "06_What_This_Thesis_Does_Not_Claim.txt",
            "07_Claim_Verification_Report.txt",
        ],
    }
    (HANDOFF_ROOT / "handoff-metadata.json").write_text(json.dumps(handoff_metadata, indent=2) + "\n")

    zip_dir(HANDOFF_ROOT, HANDOFF_ZIP)
    refresh_latest_alias()

    print(f"Prepared supervisor handoff: {HANDOFF_ROOT.relative_to(REPO_ROOT)}")
    print(f"Prepared handoff zip:       {HANDOFF_ZIP.relative_to(REPO_ROOT)}")
    print(f"Latest handoff alias:       {LATEST_ALIAS.relative_to(REPO_ROOT)}")


def main() -> int:
    build_handoff()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
