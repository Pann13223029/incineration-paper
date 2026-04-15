#!/usr/bin/env python3
"""Export the defense deck to reproducible local presentation artifacts."""

from __future__ import annotations

import argparse
import platform
import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SLIDES_DIR = REPO_ROOT / "research" / "slides"
SOURCE = SLIDES_DIR / "defense-deck.md"
THEME = SLIDES_DIR / "themes" / "defense-apu.css"
DIST_DIR = SLIDES_DIR / "dist"
HTML_OUT = DIST_DIR / "defense-deck.html"
PDF_OUT = DIST_DIR / "defense-deck.pdf"


def browser_path() -> str | None:
    candidates = []
    system = platform.system()

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


def run(command: list[str]) -> None:
    subprocess.run(command, cwd=REPO_ROOT, check=True)


def export_html(npx_cmd: str) -> None:
    run(
        [
            npx_cmd,
            "--no-install",
            "marp",
            str(SOURCE),
            "--theme-set",
            str(THEME),
            "--allow-local-files",
            "--html",
            "--output",
            str(HTML_OUT),
        ]
    )


def export_pdf(npx_cmd: str, browser: str | None) -> bool:
    if browser is None:
        return False
    subprocess.run(
        [
            npx_cmd,
            "--no-install",
            "marp",
            str(SOURCE),
            "--theme-set",
            str(THEME),
            "--allow-local-files",
            "--pdf",
            "--browser-path",
            browser,
            "--output",
            str(PDF_OUT),
        ],
        cwd=REPO_ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    return True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export the defense deck to local presentation artifacts."
    )
    parser.add_argument(
        "--pdf",
        action="store_true",
        help="Also export a PDF deck using a local Chrome/Edge browser.",
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

    DIST_DIR.mkdir(parents=True, exist_ok=True)

    try:
        export_html(npx_cmd)
    except subprocess.CalledProcessError:
        print(
            "HTML export failed. Run `npm install` first to install @marp-team/marp-cli.",
            file=sys.stderr,
        )
        return 1

    print(f"Exported HTML deck: {HTML_OUT.relative_to(REPO_ROOT)}")

    if not args.pdf:
        print("HTML-only export complete. Run `npm run slides:export:pdf` if you also want a PDF deck.")
        return 0

    browser = browser_path()
    if browser is None:
        print("PDF export requested, but no local Chrome/Edge browser was found.", file=sys.stderr)
        return 1

    try:
        export_pdf(npx_cmd, browser)
    except subprocess.CalledProcessError:
        print(
            "PDF export failed even though a browser was found. "
            "This usually means the local browser cannot launch headlessly in the current environment.",
            file=sys.stderr,
        )
        return 1

    if PDF_OUT.exists():
        print(f"Exported PDF deck:  {PDF_OUT.relative_to(REPO_ROOT)}")
    else:
        print("PDF export finished without producing the output file.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
