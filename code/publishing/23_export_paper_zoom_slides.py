#!/usr/bin/env python3
"""Export the paper Zoom briefing deck to reproducible presentation artifacts."""

from __future__ import annotations

import argparse
import platform
import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SLIDES_DIR = REPO_ROOT / "paper" / "slides"
SOURCE = SLIDES_DIR / "paper-zoom-briefing.md"
THEME = SLIDES_DIR / "themes" / "paper-zoom.css"
DIST_DIR = SLIDES_DIR / "dist"
HTML_OUT = DIST_DIR / "paper-zoom-briefing.html"
PDF_OUT = REPO_ROOT / "paper" / "share" / "paper-zoom-briefing.pdf"


def browser_path() -> str | None:
    system = platform.system()
    candidates: list[str | Path] = []

    if system == "Darwin":
        candidates.extend(
            [
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary",
                "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
                "/Applications/Chromium.app/Contents/MacOS/Chromium",
            ]
        )
    elif system == "Windows":
        local = Path.home() / "AppData" / "Local"
        program_files = Path("C:/Program Files")
        program_files_x86 = Path("C:/Program Files (x86)")
        candidates.extend(
            [
                local / "Google/Chrome/Application/chrome.exe",
                program_files / "Google/Chrome/Application/chrome.exe",
                program_files_x86 / "Google/Chrome/Application/chrome.exe",
                program_files / "Microsoft/Edge/Application/msedge.exe",
                program_files_x86 / "Microsoft/Edge/Application/msedge.exe",
            ]
        )
    else:
        for binary in ("google-chrome", "chromium", "chromium-browser", "microsoft-edge"):
            found = shutil.which(binary)
            if found:
                return found

    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            return str(path)
    return None


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=REPO_ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )


def marp_base(npx_cmd: str) -> list[str]:
    return [
        npx_cmd,
        "--no-install",
        "marp",
        str(SOURCE),
        "--theme-set",
        str(THEME),
        "--allow-local-files",
        "--html",
    ]


def export_html(npx_cmd: str) -> bool:
    command = marp_base(npx_cmd) + ["--output", str(HTML_OUT)]
    completed = run(command)
    if completed.returncode != 0:
        print("HTML export failed. Marp output:", file=sys.stderr)
        print(completed.stdout, file=sys.stderr)
        return False
    print(f"Exported HTML deck: {HTML_OUT.relative_to(REPO_ROOT)}")
    return True


def export_pdf(npx_cmd: str) -> bool:
    browser = browser_path()
    if browser is None:
        print("PDF export requested, but no local Chrome/Edge browser was found.", file=sys.stderr)
        return False

    command = marp_base(npx_cmd) + [
        "--pdf",
        "--browser-path",
        browser,
        "--output",
        str(PDF_OUT),
    ]
    completed = run(command)
    if completed.returncode != 0:
        print("PDF export failed. Marp output:", file=sys.stderr)
        print(completed.stdout, file=sys.stderr)
        if "TargetCloseError" in completed.stdout or "Target closed" in completed.stdout:
            print(
                "Headless browser export can fail in sandboxed terminals. "
                "Rerun `npm run slides:paper:pdf` in a normal local shell if needed.",
                file=sys.stderr,
            )
        return False

    print(f"Exported PDF deck:  {PDF_OUT.relative_to(REPO_ROOT)}")
    return True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export the paper Zoom briefing deck."
    )
    parser.add_argument(
        "--pdf",
        action="store_true",
        help="Also export the shareable PDF deck to paper/share/.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    npx_cmd = shutil.which("npx")
    if npx_cmd is None:
        print("npx is required. Install Node.js first.", file=sys.stderr)
        return 1

    if not SOURCE.exists():
        print(f"Slide source not found: {SOURCE}", file=sys.stderr)
        return 1
    if not THEME.exists():
        print(f"Slide theme not found: {THEME}", file=sys.stderr)
        return 1

    DIST_DIR.mkdir(parents=True, exist_ok=True)
    PDF_OUT.parent.mkdir(parents=True, exist_ok=True)

    if not export_html(npx_cmd):
        print("Run `npm install` first if @marp-team/marp-cli is not installed.", file=sys.stderr)
        return 1

    if args.pdf and not export_pdf(npx_cmd):
        return 1

    if not args.pdf:
        print("HTML-only export complete. Run `npm run slides:paper:pdf` for the shareable PDF.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
