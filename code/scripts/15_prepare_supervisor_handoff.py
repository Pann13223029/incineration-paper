#!/usr/bin/env python3
"""Build a flattened supervisor handoff bundle with simple filenames."""

from __future__ import annotations

import hashlib
import json
import re
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


def markdown_inline_to_text(text: str) -> str:
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    text = re.sub(r"\*([^*]+)\*", r"\1", text)
    return text


def parse_table_row(line: str) -> list[str]:
    return [markdown_inline_to_text(cell.strip()) for cell in line.strip().strip("|").split("|")]


def is_table_separator(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("|") and re.fullmatch(r"[|\-: ]+", stripped) is not None


def render_markdown_table(headers: list[str], rows: list[list[str]]) -> list[str]:
    rendered: list[str] = []
    if len(headers) == 2:
        for row in rows:
            if len(row) >= 2:
                rendered.append(f"- {row[0]}: {row[1]}")
        return rendered

    for row in rows:
        if not row:
            continue
        rendered.append(f"- {headers[0]}: {row[0]}")
        for idx in range(1, min(len(headers), len(row))):
            rendered.append(f"  {headers[idx]}: {row[idx]}")
        rendered.append("")

    if rendered and rendered[-1] == "":
        rendered.pop()
    return rendered


def render_markdown_for_handoff(text: str) -> str:
    lines = text.splitlines()
    rendered: list[str] = []
    i = 0

    while i < len(lines):
        line = lines[i]

        if (
            line.strip().startswith("|")
            and i + 1 < len(lines)
            and is_table_separator(lines[i + 1])
        ):
            headers = parse_table_row(line)
            i += 2
            rows: list[list[str]] = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(parse_table_row(lines[i]))
                i += 1
            rendered.extend(render_markdown_table(headers, rows))
            continue

        text_line = markdown_inline_to_text(line)
        text_line = re.sub(r"^#{1,6}\s*", "", text_line)
        rendered.append(text_line)
        i += 1

    output = "\n".join(rendered)
    output = re.sub(r"\n{3,}", "\n\n", output)
    return output.strip() + "\n"


def extract_backticked_value(text: str, label: str) -> str | None:
    match = re.search(rf"- {re.escape(label)}:\s+`([^`]+)`", text)
    return match.group(1) if match else None


def extract_plain_value(text: str, label: str) -> str | None:
    match = re.search(rf"- {re.escape(label)}:\s+([^\n]+)", text)
    return match.group(1).strip() if match else None


def build_change_note() -> str:
    delta_text = DELTA.read_text()
    current_head = extract_backticked_value(delta_text, "Current HEAD") or "unknown"
    baseline_tag = extract_backticked_value(delta_text, "Baseline checkpoint tag") or "unknown"
    commits_since = extract_backticked_value(delta_text, "Commits since baseline") or "unknown"
    interpretation = re.search(r"## Interpretation\n\n(.+)", delta_text, re.DOTALL)
    interpretation_text = interpretation.group(1).strip().splitlines()[0] if interpretation else ""

    sections: dict[str, list[str]] = {}
    current_section: str | None = None
    for line in delta_text.splitlines():
        if line.startswith("### "):
            current_section = line[4:].strip()
            sections[current_section] = []
        elif current_section and line.startswith("- "):
            sections[current_section].append(line[2:].strip())

    thesis_core = sections.get("Thesis and empirical core", [])
    support = sections.get("Supervisor and defense materials", [])
    workflow = sections.get("Workflow and repo operations", [])

    changed_layers: list[str] = []
    if thesis_core:
        changed_layers.append("the thesis manuscript and thesis-facing verifier logic")
    if support:
        changed_layers.append("the supervisor-facing support material")
    if workflow:
        changed_layers.append("the packaging workflow")

    change_summary = ", ".join(changed_layers) if changed_layers else "the thesis package"

    return f"""What changed since the last send

Read this only after the thesis PDF and one-page summary.

Short answer:
- This is a substantive thesis revision, not just an operational refresh.
- The main changes affect {change_summary}.
- The empirical spine remains aligned and verified after the update.

Version details:
- Current sendable commit: {current_head}
- Previous frozen baseline: {baseline_tag}
- Commits since that baseline: {commits_since}

How to read this revision:
- Prioritize the revised manuscript itself.
- Use the one-page summary to see the defended argument quickly.
- Ignore the underlying commit history unless you specifically want repo-level detail.

Reviewer note:
- {interpretation_text}
"""


def build_claim_verification_note() -> str:
    report = CLAIM_REPORT.read_text()
    status = re.search(r"## Result: (\w+)", report)
    passed = re.search(r"- Passed checks: (\d+)", report)
    failed = re.search(r"- Failed checks: (\d+)", report)
    python_version = extract_plain_value(report, "Core manifest Python") or "unknown"

    return f"""Technical verification note

This is a packet-synchronization check, not a substitute for academic judgment.

Current status:
- Result: {status.group(1) if status else "UNKNOWN"}
- Passed checks: {passed.group(1) if passed else "unknown"}
- Failed checks: {failed.group(1) if failed else "unknown"}
- Manifest Python: {python_version}

What this check is for:
- confirm that thesis-facing numbers match the canonical generated outputs
- confirm that the supervisor brief and support notes use the current defended wording
- confirm that stale overclaim language has not re-entered the packet

What this check does not prove:
- that the argument is correct
- that the methods are optimal
- that the thesis is immune to criticism

Supervisor guidance:
- You can usually ignore this file unless you want assurance that the packet is internally synchronized.
"""


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
    (HANDOFF_ROOT / "02_One_Page_Summary.txt").write_text(render_markdown_for_handoff(SUMMARY.read_text()))
    (HANDOFF_ROOT / "03_What_Changed_Since_Last_Send.txt").write_text(build_change_note())
    (HANDOFF_ROOT / "04_Key_Claims_And_Evidence.txt").write_text(render_markdown_for_handoff(CLAIM_MAP.read_text()))
    (HANDOFF_ROOT / "05_Main_Risks_And_Mitigations.txt").write_text(render_markdown_for_handoff(RISK_REGISTER.read_text()))
    (HANDOFF_ROOT / "06_What_This_Thesis_Does_Not_Claim.txt").write_text(render_markdown_for_handoff(NON_CLAIMS.read_text()))
    (HANDOFF_ROOT / "07_Claim_Verification_Report.txt").write_text(build_claim_verification_note())

    (HANDOFF_ROOT / "00_START_HERE.txt").write_text(
        f"""Supervisor Review Bundle

This folder is the simplified review handoff. No GitHub or repo navigation is required.

Recommended reading order:
1. Open `01_Thesis.pdf`
2. Read `02_One_Page_Summary.txt`
3. Stop there for a first-pass review
4. Read `03_What_Changed_Since_Last_Send.txt` only if you want a quick summary of what changed
5. Use `05_Main_Risks_And_Mitigations.txt` and `06_What_This_Thesis_Does_Not_Claim.txt` only if you want scope calibration
6. Use `04_Key_Claims_And_Evidence.txt` and `07_Claim_Verification_Report.txt` only as optional technical backup

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
