#!/usr/bin/env python3
"""Validate repository ownership boundaries and tracked Markdown links."""

from __future__ import annotations

import ast
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
WORD_RE = re.compile(r"[A-Za-z0-9]+(?:[\u2019'-][A-Za-z0-9]+)*")

MANUSCRIPT_PATH = REPO_ROOT / "paper" / "manuscript" / "paper.md"
TITLE_PAGE_PATH = REPO_ROOT / "paper" / "submission" / "title-page.md"
HIGHLIGHTS_PATH = REPO_ROOT / "paper" / "submission" / "highlights.md"
EXPORTER_PATH = REPO_ROOT / "code" / "publishing" / "21_export_paper_submission.py"


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
    paths = [REPO_ROOT / line for line in result.stdout.splitlines() if line]
    # `git ls-files --cached` includes tracked files staged for deletion in a
    # working tree. Deleting a retired Markdown artifact must not crash link QA.
    return [path for path in paths if path.is_file()]


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


def normalize_space(text: str) -> str:
    return " ".join(text.split())


def count_words(text: str) -> int:
    return len(WORD_RE.findall(text))


def strip_equations(text: str) -> str:
    text = re.sub(r"\\\[.*?\\\]", " ", text, flags=re.DOTALL)
    text = re.sub(r"\$\$.*?\$\$", " ", text, flags=re.DOTALL)
    return re.sub(r"\$[^$]*\$", " ", text)


def reader_main_text(text: str) -> str:
    text = strip_equations(text)
    text = re.sub(r"^\s*\|.*$", " ", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*!\[.*$", " ", text, flags=re.MULTILINE)
    return re.sub(r"^\s*#{1,6}\s+.*$", " ", text, flags=re.MULTILINE)


def literal_assignment(path: Path, name: str) -> str:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if any(isinstance(target, ast.Name) and target.id == name for target in node.targets):
            value = ast.literal_eval(node.value)
            if isinstance(value, str):
                return value
    raise ValueError(f"{path.relative_to(REPO_ROOT)} does not define literal {name}")


def check_submission_format() -> tuple[list[str], dict[str, int]]:
    errors: list[str] = []
    manuscript = MANUSCRIPT_PATH.read_text(encoding="utf-8")
    title_page = TITLE_PAGE_PATH.read_text(encoding="utf-8")
    highlights_text = HIGHLIGHTS_PATH.read_text(encoding="utf-8")

    title_match = re.match(r"^#\s+(.+)$", manuscript, flags=re.MULTILINE)
    if not title_match:
        return ["paper/manuscript/paper.md: missing level-one title"], {}
    title = normalize_space(title_match.group(1))

    try:
        abstract = manuscript.split("## Abstract", 1)[1].split("## 1. Introduction", 1)[0]
        main = manuscript.split("## 1. Introduction", 1)[1].split("## Acknowledgements", 1)[0]
    except IndexError:
        return ["paper/manuscript/paper.md: required manuscript section boundary is missing"], {}

    keyword_match = re.search(
        r"\*\*Keywords:\*\*\s*(.*?)(?:\n\n|\Z)", manuscript, flags=re.DOTALL
    )
    if not keyword_match:
        errors.append("paper/manuscript/paper.md: missing Keywords line")
        keywords: list[str] = []
    else:
        keywords = [
            normalize_space(item)
            for item in keyword_match.group(1).split(";")
            if normalize_space(item)
        ]

    abstract_body = abstract.split("**Keywords:**", 1)[0]
    abstract_words = count_words(strip_equations(abstract_body))
    reader_words = count_words(reader_main_text(main))
    journal_words = count_words(strip_equations(main))
    figure_count = len(re.findall(r"^!\[", main, flags=re.MULTILINE))
    table_count = len(
        re.findall(r"^\*\*Table\s+\d+\.", main, flags=re.MULTILINE)
    )
    highlights = [
        line[2:].strip()
        for line in highlights_text.splitlines()
        if line.startswith("- ")
    ]

    if abstract_words > 250:
        errors.append(f"abstract has {abstract_words} words; maximum is 250")
    if journal_words > 6500:
        errors.append(
            f"main text has {journal_words} conservative-count words; maximum is 6500"
        )
    if not 1 <= len(keywords) <= 7:
        errors.append(f"manuscript has {len(keywords)} keywords; required range is 1-7")
    if figure_count + table_count > 8:
        errors.append(
            f"manuscript has {figure_count} figures plus {table_count} tables; maximum is 8"
        )
    if not 3 <= len(highlights) <= 5:
        errors.append(f"highlights file has {len(highlights)} bullets; required range is 3-5")
    for index, item in enumerate(highlights, start=1):
        if len(item) > 85:
            errors.append(
                f"highlight {index} has {len(item)} characters; maximum is 85"
            )

    exporter_title = literal_assignment(EXPORTER_PATH, "TITLE")
    exporter_keywords = [
        normalize_space(item) for item in literal_assignment(EXPORTER_PATH, "KEYWORDS").split(",")
    ]
    if normalize_space(exporter_title) != title:
        errors.append("submission exporter TITLE differs from the manuscript title")
    if exporter_keywords != keywords:
        errors.append("submission exporter KEYWORDS differ from the manuscript keywords")
    if title not in normalize_space(title_page):
        errors.append("title page title differs from the manuscript title")

    abstract_metric = re.search(r"abstract word count:\s*([0-9,]+)", title_page)
    main_metric = re.search(r"main-text word count:\s*([0-9,]+)", title_page)
    if not abstract_metric or int(abstract_metric.group(1).replace(",", "")) != abstract_words:
        errors.append("title-page abstract word count is missing or stale")
    if not main_metric or int(main_metric.group(1).replace(",", "")) != reader_words:
        errors.append("title-page main-text word count is missing or stale")

    metrics = {
        "abstract_words": abstract_words,
        "reader_main_words": reader_words,
        "journal_main_words": journal_words,
        "keywords": len(keywords),
        "figures": figure_count,
        "tables": table_count,
        "highlights": len(highlights),
    }
    return errors, metrics


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
    format_errors, format_metrics = check_submission_format()
    errors.extend(format_errors)

    if errors:
        print("Repository layout validation failed:")
        for error in errors:
            print(f"- {error}")
        if format_metrics:
            print(f"Submission metrics: {format_metrics}")
        return 1

    print(
        "Repository layout validation passed: "
        f"{len(REQUIRED_PATHS)} required paths and "
        f"{len(markdown_paths)} tracked Markdown files checked."
    )
    print(
        "Submission format passed: "
        f"abstract {format_metrics['abstract_words']}/250 words; "
        f"main text {format_metrics['journal_main_words']}/6500 conservative words "
        f"({format_metrics['reader_main_words']} excluding tables, captions, equations, and headings); "
        f"{format_metrics['keywords']} keywords; "
        f"{format_metrics['figures']} figures + {format_metrics['tables']} tables; "
        f"{format_metrics['highlights']} highlights."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
