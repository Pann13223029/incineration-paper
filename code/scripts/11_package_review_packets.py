#!/usr/bin/env python3
"""Build frozen supervisor and submission packets from the current repo state."""

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
SUPERVISOR_ROOT = PACKET_ROOT / "supervisor-packet"
SUBMISSION_ROOT = PACKET_ROOT / "submission-packet"
SUPERVISOR_ZIP = PACKET_ROOT / "supervisor-packet.zip"
SUBMISSION_ZIP = PACKET_ROOT / "submission-packet.zip"
CLAIM_REPORT = REPO_ROOT / "output" / "claim_verification.md"
CLAIM_MAP = REPO_ROOT / "output" / "claim_evidence_map.md"
CHECKPOINT_DELTA = REPO_ROOT / "output" / "checkpoint_delta.md"
VERIFY_MANIFEST = REPO_ROOT / "output" / "manifests" / "08_verify_claims.json"
THESIS_DIR = REPO_ROOT / "thesis"
THESIS_PDF = THESIS_DIR / "thesis.pdf"
THESIS_TEX = THESIS_DIR / "thesis.tex"
THESIS_FIGURES_DIR = THESIS_DIR / "figures"

SUPERVISOR_FILES: list[tuple[str, str | None]] = [
    ("thesis/thesis.pdf", None),
    ("research/notes/executive-summary-for-supervisor.md", None),
    ("research/notes/examiner-risk-register.md", None),
    ("research/notes/what-this-thesis-does-not-claim.md", None),
    ("output/checkpoint_delta.md", None),
    ("output/claim_verification.md", None),
    ("output/claim_evidence_map.md", None),
    ("output/sample_definition.md", None),
    ("output/adoption_results.md", None),
    ("output/regression_results.md", None),
    ("output/robustness_results.md", None),
]

SUBMISSION_FILES: list[tuple[str, str | None]] = [
    ("README.md", None),
    ("ARCHITECTURE.md", None),
    ("requirements.txt", None),
    (".python-version", None),
    ("thesis/thesis.pdf", None),
    ("thesis/thesis.tex", None),
    ("research/notes/examiner-risk-register.md", None),
    ("code/scripts/panel_utils.py", None),
    ("code/scripts/05a_power_adoption.py", None),
    ("code/scripts/05_panel_regression.py", None),
    ("code/scripts/06_robustness.py", None),
    ("code/scripts/07_rebuild_analysis.py", None),
    ("code/scripts/08_verify_claims.py", None),
    ("code/scripts/14_generate_checkpoint_delta.py", None),
    ("output/checkpoint_delta.md", None),
    ("output/claim_verification.md", None),
    ("output/claim_evidence_map.md", None),
    ("output/sample_definition.md", None),
    ("output/adoption_results.md", None),
    ("output/regression_results.md", None),
    ("output/robustness_results.md", None),
]

SUPERVISOR_DIRS = []

SUBMISSION_DIRS = [
    "thesis/figures",
    "output/manifests",
]


def run(command: list[str], cwd: Path | None = None) -> None:
    subprocess.run(command, cwd=cwd or REPO_ROOT, check=True)


def resolve_tectonic() -> str:
    local = Path.home() / ".local" / "bin" / "tectonic"
    if local.exists():
        return str(local)
    found = shutil.which("tectonic")
    if found:
        return found
    raise FileNotFoundError("tectonic not found")


def thesis_sources() -> list[Path]:
    sources = [THESIS_TEX]
    if THESIS_FIGURES_DIR.exists():
        sources.extend(path for path in THESIS_FIGURES_DIR.rglob("*") if path.is_file())
    return sources


def thesis_pdf_is_current() -> bool:
    if not THESIS_PDF.exists():
        return False
    pdf_mtime = THESIS_PDF.stat().st_mtime
    return all(source.stat().st_mtime <= pdf_mtime for source in thesis_sources())


def ensure_current_state() -> None:
    run([sys.executable, "code/scripts/08_verify_claims.py"])
    run([sys.executable, "code/scripts/14_generate_checkpoint_delta.py"])
    try:
        tectonic = resolve_tectonic()
    except FileNotFoundError as exc:
        if thesis_pdf_is_current():
            print("tectonic not found; reusing existing current thesis/thesis.pdf")
            return
        raise FileNotFoundError(
            "tectonic not found and thesis/thesis.pdf is missing or stale relative to thesis sources"
        ) from exc
    run([tectonic, "-p", "--keep-logs", "--keep-intermediates", "thesis.tex"], cwd=THESIS_DIR)


def parse_claim_verification() -> dict[str, int | str | None]:
    report = CLAIM_REPORT.read_text()
    status = re.search(r"## Result: (\w+)", report)
    passed = re.search(r"- Passed checks: (\d+)", report)
    failed = re.search(r"- Failed checks: (\d+)", report)
    return {
        "status": status.group(1) if status else "UNKNOWN",
        "passed_checks": int(passed.group(1)) if passed else None,
        "failed_checks": int(failed.group(1)) if failed else None,
    }


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def repo_git_sha() -> str:
    result = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "rev-parse", "HEAD"],
        check=True,
        stdout=subprocess.PIPE,
        text=True,
    )
    return result.stdout.strip()


def reset_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def copy_spec(root: Path, files: list[tuple[str, str | None]], dirs: list[str]) -> list[str]:
    copied: list[str] = []
    for src_rel, dest_rel in files:
        src = REPO_ROOT / src_rel
        bundle_rel = dest_rel or src_rel
        dest = root / bundle_rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        copied.append(bundle_rel)
    for rel in dirs:
        src = REPO_ROOT / rel
        dest = root / rel
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(src, dest)
        copied.append(rel + "/")
    return copied


def write_readme(path: Path, kind: str, metadata: dict[str, object], start_lines: list[str], included_lines: list[str]) -> None:
    content = f"""# {kind}

Frozen packet assembled from the current verified repo state.

- Generated at: {metadata["generated_at_utc"]}
- Repo git SHA: `{metadata["repo_git_sha"]}`
- Claim verification status: `{metadata["claim_verification"]["status"]}`
- Passed checks: `{metadata["claim_verification"]["passed_checks"]}`
- Failed checks: `{metadata["claim_verification"]["failed_checks"]}`
- Thesis PDF SHA256: `{metadata["thesis_pdf_sha256"]}`

## Start here

{chr(10).join(start_lines)}

## Included artifacts

{chr(10).join(included_lines)}
"""
    (path / "README.md").write_text(content)


def write_metadata(path: Path, metadata: dict[str, object], included_paths: list[str]) -> None:
    payload = {**metadata, "included_paths": included_paths}
    (path / "packet-metadata.json").write_text(json.dumps(payload, indent=2) + "\n")


def zip_dir(src: Path, dest_zip: Path) -> None:
    if dest_zip.exists():
        dest_zip.unlink()
    with ZipFile(dest_zip, "w", compression=ZIP_DEFLATED) as zf:
        for path in src.rglob("*"):
            zf.write(path, arcname=path.relative_to(PACKET_ROOT))


def build_packets() -> None:
    verifier_manifest_before = VERIFY_MANIFEST.read_text() if VERIFY_MANIFEST.exists() else None
    ensure_current_state()
    PACKET_ROOT.mkdir(parents=True, exist_ok=True)
    metadata = {
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "repo_git_sha": repo_git_sha(),
        "claim_verification": parse_claim_verification(),
        "thesis_pdf_sha256": sha256(THESIS_PDF),
    }

    reset_dir(SUPERVISOR_ROOT)
    reset_dir(SUBMISSION_ROOT)

    supervisor_included = copy_spec(SUPERVISOR_ROOT, SUPERVISOR_FILES, SUPERVISOR_DIRS)
    submission_included = copy_spec(SUBMISSION_ROOT, SUBMISSION_FILES, SUBMISSION_DIRS)

    write_readme(
        SUPERVISOR_ROOT,
        "Supervisor Packet",
        metadata,
        [
            "1. Read `research/notes/executive-summary-for-supervisor.md` for the one-page brief.",
            "2. Read `output/checkpoint_delta.md` for the change summary since the last frozen checkpoint.",
            "3. Read `research/notes/examiner-risk-register.md` for the strongest remaining attack points and mitigations.",
            "4. Open `thesis/thesis.pdf` for the defended manuscript.",
            "5. Use `output/claim_verification.md` to confirm the thesis-facing evidence spine.",
            "6. Use `output/claim_evidence_map.md` to see which artifact supports each defended claim.",
            "7. Use `research/notes/what-this-thesis-does-not-claim.md` to keep scope calibration explicit.",
        ],
        [
            "- One-page supervisor brief",
            "- Change summary since the last frozen checkpoint",
            "- Examiner risk register",
            "- Current thesis PDF",
            "- Claim-verification report",
            "- Claim-to-evidence map",
            "- Sample definition and core empirical outputs",
            "- Non-claims calibration note",
        ],
    )
    write_readme(
        SUBMISSION_ROOT,
        "Submission Packet",
        metadata,
        [
            "1. Open `thesis/thesis.pdf` for the submission manuscript.",
            "2. Use `README.md` and `ARCHITECTURE.md` for repo-level orientation.",
            "3. Read `output/checkpoint_delta.md` for the change summary since the last frozen checkpoint.",
            "4. Read `research/notes/examiner-risk-register.md` for the calibrated weakness map.",
            "5. Use `output/claim_verification.md` to confirm the thesis-facing evidence spine.",
            "6. Use `output/claim_evidence_map.md` for a compact claim-to-evidence bridge.",
            "7. Use `thesis/thesis.tex` plus `thesis/figures/` as the authoritative source bundle.",
        ],
        [
            "- Current thesis PDF and authoritative LaTeX source",
            "- Change summary since the last frozen checkpoint",
            "- Examiner risk register",
            "- Thesis figures used by the manuscript",
            "- Core analysis scripts for the defended empirical design",
            "- Claim-verification report, claim-to-evidence map, and key empirical outputs",
            "- Stage manifests and repo-level reproduction docs",
        ],
    )

    write_metadata(SUPERVISOR_ROOT, metadata, supervisor_included)
    write_metadata(SUBMISSION_ROOT, metadata, submission_included)

    zip_dir(SUPERVISOR_ROOT, SUPERVISOR_ZIP)
    zip_dir(SUBMISSION_ROOT, SUBMISSION_ZIP)

    if verifier_manifest_before is not None:
        VERIFY_MANIFEST.write_text(verifier_manifest_before)

    print(f"Prepared supervisor packet: {SUPERVISOR_ROOT.relative_to(REPO_ROOT)}")
    print(f"Prepared supervisor zip:    {SUPERVISOR_ZIP.relative_to(REPO_ROOT)}")
    print(f"Prepared submission packet: {SUBMISSION_ROOT.relative_to(REPO_ROOT)}")
    print(f"Prepared submission zip:    {SUBMISSION_ZIP.relative_to(REPO_ROOT)}")


def main() -> int:
    try:
        build_packets()
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
