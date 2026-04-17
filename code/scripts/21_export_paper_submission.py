#!/usr/bin/env python3
"""Export the paper manuscript into submission-facing artifacts.

This script treats the Markdown manuscript as the single editable source and
generates:

- paper/submission/waste-management-manuscript.md
- paper/submission/waste-management-manuscript.html
- paper/submission/waste-management-manuscript.docx

The HTML is intentionally simple and self-contained enough for `textutil` to
convert it into a practical DOCX export on macOS without requiring Pandoc.
"""

from __future__ import annotations

import argparse
import html
import re
import shutil
import subprocess
import sys
from pathlib import Path
from urllib.parse import quote


REPO_ROOT = Path(__file__).resolve().parents[2]
MANUSCRIPT_MD = REPO_ROOT / "paper" / "manuscript" / "paper.md"
SUBMISSION_DIR = REPO_ROOT / "paper" / "submission"
OUT_MD = SUBMISSION_DIR / "waste-management-manuscript.md"
OUT_HTML = SUBMISSION_DIR / "waste-management-manuscript.html"
OUT_DOCX = SUBMISSION_DIR / "waste-management-manuscript.docx"


TITLE = (
    "Selective Modernization and Bounded Responsiveness in Japan's "
    "Waste-Incineration Fleet: A Facility-Level Panel Study"
)
AUTHOR = "Pann Phetra"
SUBJECT = "Waste Management manuscript export"
KEYWORDS = (
    "waste incineration, waste-to-energy, Japan, energy recovery, "
    "facility panel, transition"
)


def inline_markup(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\*(.+?)\*", r"<em>\1</em>", escaped)
    escaped = re.sub(r"`(.+?)`", r"<code>\1</code>", escaped)
    return escaped


def render_table(table_lines: list[str]) -> str:
    rows = []
    for raw in table_lines:
        if not raw.strip():
            continue
        parts = [part.strip() for part in raw.strip().strip("|").split("|")]
        rows.append(parts)

    if len(rows) < 2:
        return ""

    header = rows[0]
    body = rows[2:] if set(":- ") >= set(rows[1][0]) else rows[1:]

    lines = ["<table>", "<thead>", "<tr>"]
    for cell in header:
        lines.append(f"<th>{inline_markup(cell)}</th>")
    lines.extend(["</tr>", "</thead>", "<tbody>"])
    for row in body:
        lines.append("<tr>")
        for cell in row:
            lines.append(f"<td>{inline_markup(cell)}</td>")
        lines.append("</tr>")
    lines.extend(["</tbody>", "</table>"])
    return "\n".join(lines)


def figure_html(line: str) -> str:
    match = re.match(r"!\[(.*?)\]\((.*?)\)", line.strip())
    if not match:
        return ""
    caption, src = match.groups()
    src_attr = html.escape(src, quote=True)
    caption_html = inline_markup(caption)
    return (
        "<figure>\n"
        f'  <img src="{src_attr}" alt="{html.escape(caption, quote=True)}"/>\n'
        f"  <figcaption>{caption_html}</figcaption>\n"
        "</figure>"
    )


def markdown_to_html(markdown_text: str) -> str:
    body: list[str] = []
    paragraph: list[str] = []
    table_lines: list[str] = []

    def flush_paragraph() -> None:
        nonlocal paragraph
        if paragraph:
            text = " ".join(line.strip() for line in paragraph).strip()
            if text:
                body.append(f"<p>{inline_markup(text)}</p>")
            paragraph = []

    def flush_table() -> None:
        nonlocal table_lines
        if table_lines:
            rendered = render_table(table_lines)
            if rendered:
                body.append(rendered)
            table_lines = []

    for raw_line in markdown_text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()

        if stripped.startswith("|"):
            flush_paragraph()
            table_lines.append(line)
            continue

        flush_table()

        if not stripped:
            flush_paragraph()
            continue

        if stripped.startswith("!["):
            flush_paragraph()
            body.append(figure_html(stripped))
            continue

        if stripped.startswith("### "):
            flush_paragraph()
            body.append(f"<h3>{inline_markup(stripped[4:])}</h3>")
            continue

        if stripped.startswith("## "):
            flush_paragraph()
            body.append(f"<h2>{inline_markup(stripped[3:])}</h2>")
            continue

        if stripped.startswith("# "):
            flush_paragraph()
            body.append(f"<h1>{inline_markup(stripped[2:])}</h1>")
            continue

        paragraph.append(stripped)

    flush_table()
    flush_paragraph()

    styles = """
    body { font-family: Georgia, "Times New Roman", serif; color: #111827; line-height: 1.55; margin: 48px; }
    h1 { font-size: 24px; margin: 0 0 24px 0; }
    h2 { font-size: 19px; margin: 30px 0 12px 0; page-break-after: avoid; }
    h3 { font-size: 16px; margin: 22px 0 10px 0; page-break-after: avoid; }
    p { margin: 0 0 12px 0; }
    figure { margin: 18px 0 22px 0; text-align: center; }
    img { max-width: 100%; height: auto; border: 1px solid #d1d5db; background: #ffffff; }
    figcaption { font-size: 12px; color: #374151; margin-top: 8px; }
    table { width: 100%; border-collapse: collapse; margin: 16px 0 20px 0; font-size: 12px; }
    th, td { border: 1px solid #d1d5db; padding: 7px 8px; vertical-align: top; }
    th { background: #f3f4f6; font-weight: 700; }
    code { font-family: Menlo, Consolas, monospace; font-size: 90%; background: #f3f4f6; padding: 1px 3px; }
    """

    return (
        "<!DOCTYPE html>\n"
        '<html lang="en">\n<head>\n<meta charset="utf-8"/>\n'
        f"<title>{html.escape(TITLE)}</title>\n"
        f"<style>{styles}</style>\n"
        "</head>\n<body>\n"
        + "\n".join(body)
        + "\n</body>\n</html>\n"
    )


def export_docx() -> None:
    textutil = shutil.which("textutil")
    if not textutil:
        raise SystemExit("textutil not found; cannot export DOCX on this machine.")

    baseurl = "file://" + quote(str(SUBMISSION_DIR.resolve())) + "/"
    command = [
        textutil,
        "-convert",
        "docx",
        str(OUT_HTML),
        "-output",
        str(OUT_DOCX),
        "-title",
        TITLE,
        "-author",
        AUTHOR,
        "-subject",
        SUBJECT,
        "-baseurl",
        baseurl,
    ]
    subprocess.run(command, check=True)
    if not OUT_DOCX.exists():
        raise SystemExit(
            "DOCX export did not produce an output file on this machine. "
            "Use --no-docx to generate Markdown and HTML only."
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--no-docx",
        action="store_true",
        help="Generate Markdown and HTML only.",
    )
    args = parser.parse_args()

    SUBMISSION_DIR.mkdir(parents=True, exist_ok=True)

    manuscript_text = MANUSCRIPT_MD.read_text(encoding="utf-8")
    header = (
        "<!-- Generated by code/scripts/21_export_paper_submission.py. "
        "Edit paper/manuscript/paper.md instead. -->\n\n"
    )
    OUT_MD.write_text(header + manuscript_text, encoding="utf-8")
    OUT_HTML.write_text(markdown_to_html(manuscript_text), encoding="utf-8")

    if not args.no_docx:
        export_docx()

    print(f"Submission manuscript source: {OUT_MD}")
    print(f"Submission manuscript HTML: {OUT_HTML}")
    if not args.no_docx:
        print(f"Submission manuscript DOCX: {OUT_DOCX}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
