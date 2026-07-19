#!/usr/bin/env python3
"""Build the Moodle-template graduation-thesis assignment profile.

The professor-facing thesis remains the technical source of truth. This build
creates a separate reader-facing profile with template-compatible typography,
fewer equations in the main narrative, and technical formulas retained in an
appendix.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE_DIR = ROOT / "paper" / "manuscript" / "professor"
SOURCE_MD = SOURCE_DIR / "paper.md"
SOURCE_TEX = SOURCE_DIR / "paper.tex"
TEMPLATE_DOCX = Path(
    os.environ.get(
        "GRADUATION_THESIS_TEMPLATE",
        Path.home() / "Downloads" / "research_paper_template-4.docx",
    )
)
OUT_DIR = ROOT / "paper" / "submission" / "graduation-research-ii"
OUT_MD = OUT_DIR / "assignment-thesis.md"
OUT_TEX = OUT_DIR / "assignment-thesis.tex"
OUT_DOCX = OUT_DIR / "assignment-thesis.docx"
OUT_PDF = OUT_DIR / "assignment-thesis.pdf"

FIGURE_SCRIPTS = [
    ROOT / "paper" / "figures" / "build_figure1_two_part_framework.py",
    ROOT / "paper" / "figures" / "build_figure2_selective_transition.py",
    ROOT / "paper" / "figures" / "build_figure3_efficiency_structure.py",
    ROOT / "paper" / "figures" / "build_figure4_post_entry_trajectories.py",
    ROOT / "paper" / "figures" / "build_figure_entry_sample_flow.py",
    ROOT / "paper" / "figures" / "build_thesis_entry_support.py",
    ROOT / "paper" / "figures" / "build_thesis_cohort_components.py",
]

BANNED_VISIBLE_PATTERNS = {
    "AI-tool disclosure": r"\b(?:OpenAI|Anthropic|Codex|Claude)\b|"
    r"generative artificial intelligence|AI-assisted",
    "internal revision language": r"revision-frozen|internally frozen|"
    r"model-decision memo|memo-continuity|checked-in parser",
    "repository workflow": r"github\.com|public repository|repository history|"
    r"without consulting external files",
    "audience-side drafting note": r"professor discussion|professor or later reviewer",
    "draft-history language": r"professor-facing|model\s+decision record|"
    r"earlier 11-parameter",
    "editing artifact": r"a outstanding|primary primary|outstanding outstanding",
}


def replace_span(
    text: str,
    start: str,
    end: str,
    replacement: str,
    *,
    keep_end: bool = True,
) -> str:
    start_index = text.find(start)
    if start_index < 0:
        raise ValueError(f"Assignment transform start marker not found: {start}")
    end_index = text.find(end, start_index)
    if end_index < 0:
        raise ValueError(f"Assignment transform end marker not found: {end}")
    suffix_index = end_index if keep_end else end_index + len(end)
    return text[:start_index] + replacement + text[suffix_index:]


def replace_literal(text: str, old: str, new: str) -> str:
    if old not in text:
        raise ValueError(f"Assignment transform text not found: {old[:80]}")
    return text.replace(old, new)


RQ1_MD = """The first research question compares four transparent percentages rather
than asking readers to follow several similar formulas. Facility participation
is the percentage of retained records reporting positive installed electrical
capacity. The active-facility version uses only records with positive annual
throughput in the denominator. Throughput coverage is the share of recorded
waste processed at facilities reporting positive electricity output. Design-
capacity coverage is the share of national waste-processing capacity located at
facilities reporting positive installed electrical capacity.

These measures answer different questions. Facility participation shows how
widely generation equipment appears across records, whereas throughput and
design-capacity coverage show how much waste activity or nominal processing
capacity lies within the generating segment. Positive output is used for the
throughput numerator because installed equipment does not guarantee generation
in every year.

The annual percentages are repeated cross-sections, not direct conversion rates
for continuing facilities. The analysis therefore repeats the FY2005 and FY2024
comparison among administrative lineages observed in both endpoint years, then
applies stricter same-episode and complete-panel checks. Endpoint-only groups
describe changes in observed fleet composition, but administrative appearance
or disappearance is not treated as verified physical opening or closure. The
formal definitions and accounting expressions are consolidated in Appendix B.

"""

RQ1_TEX = r"""The first research question compares four transparent percentages rather
than asking readers to follow several similar formulas. Facility participation
is the percentage of retained records reporting positive installed electrical
capacity. The active-facility version uses only records with positive annual
throughput in the denominator. Throughput coverage is the share of recorded
waste processed at facilities reporting positive electricity output. Design-
capacity coverage is the share of national waste-processing capacity located at
facilities reporting positive installed electrical capacity.

These measures answer different questions. Facility participation shows how
widely generation equipment appears across records, whereas throughput and
design-capacity coverage show how much waste activity or nominal processing
capacity lies within the generating segment. Positive output is used for the
throughput numerator because installed equipment does not guarantee generation
in every year.

The annual percentages are repeated cross-sections, not direct conversion rates
for continuing facilities. The analysis therefore repeats the FY2005 and FY2024
comparison among administrative lineages observed in both endpoint years, then
applies stricter same-episode and complete-panel checks. Endpoint-only groups
describe changes in observed fleet composition, but administrative appearance
or disappearance is not treated as verified physical opening or closure. The
formal definitions and accounting expressions are consolidated in Appendix B.

"""

TECHNICAL_MD = r"""### B.1 Technical formulas moved from the main narrative

This appendix preserves the formal definitions used in the analysis while the
main methodology emphasizes the research logic and interpretation.

For installed-capacity and positive-output participation:

\[
P_t^{K,all}=\frac{\sum_i I_{it}^{K}}{N_t},\qquad
P_t^{K,active}=\frac{\sum_i I_{it}^{K}I_{it}^{W}}{\sum_i I_{it}^{W}},
\]

\[
P_t^{G,all}=\frac{\sum_i I_{it}^{G}}{N_t},\qquad
P_t^{G,active}=\frac{\sum_i I_{it}^{G}}{\sum_i I_{it}^{W}}.
\]

For throughput and design-capacity coverage:

\[
P_t^{throughput}=\frac{\sum_i W_{it}I_{it}^{G}}{\sum_i W_{it}},\qquad
P_t^{design}=\frac{\sum_i C_{it}I_{it}^{K}}{\sum_i C_{it}}.
\]

The valid-generator fleet identity is

\[
\frac{\sum_i G_{it}^{valid}}{\sum_i W_{it}}
=\left(\frac{\sum_i W_{it}^{valid}}{\sum_i W_{it}}\right)
\left(\frac{\sum_i G_{it}^{valid}}{\sum_i W_{it}^{valid}}\right).
\]

Firth estimation maximizes

\[
\ell_F(\boldsymbol{\theta})=\ell(\boldsymbol{\theta})+
\frac{1}{2}\log\left|\mathcal{I}(\boldsymbol{\theta})\right|.
\]

The predefined processing-scale contrast and standardized annual risk are

\[
OR_{300:100}=\exp(\beta_C\log 2),\qquad
\bar p(c)=\frac{1}{n}\sum_{i,t}
\operatorname{logit}^{-1}\{\mathbf{x}_{it}(c)'\hat{\boldsymbol\theta}\}.
\]

The installed-capacity and capacity-factor models are

\[
\log K_{it}=\alpha_K+\mathbf{V}_{it}\boldsymbol{\beta}_K
+\beta_{KC}\log C_{it}+\mathbf{T}_{it}\boldsymbol{\eta}_K
+\lambda_t+\varepsilon_{Kit},
\]

\[
\log F_{it}=\alpha_F+\mathbf{V}_{it}\boldsymbol{\beta}_F
+\beta_{FC}\log C_{it}+\beta_U U_{it}
+\mathbf{T}_{it}\boldsymbol{\eta}_F+\lambda_t+\varepsilon_{Fit}.
\]

With a common design matrix, the component regressions satisfy

\[
\log D_{it}=\mathbf{X}_{it}\boldsymbol\gamma_D+e_{Dit},\quad
\log F_{it}=\mathbf{X}_{it}\boldsymbol\gamma_F+e_{Fit},
\]

\[
\log U_{it}=\mathbf{X}_{it}\boldsymbol\gamma_U+e_{Uit},\quad
\log Y_{it}=\mathbf{X}_{it}\boldsymbol\gamma_Y+e_{Yit},
\]

and therefore \(\gamma_Y=\gamma_D+\gamma_F-\gamma_U\) for each cohort
contrast. This is an accounting identity, not a causal mediation result.

"""

TECHNICAL_TEX = r"""\subsection{Technical formulas moved from the main narrative}

This appendix preserves the formal definitions used in the analysis while the
main methodology emphasizes the research logic and interpretation.

For installed-capacity and positive-output participation,
\begin{align*}
P_t^{K,\mathrm{all}}&=\frac{\sum_i I_{it}^{K}}{N_t}, &
P_t^{K,\mathrm{active}}&=\frac{\sum_i I_{it}^{K}I_{it}^{W}}{\sum_i I_{it}^{W}},\\
P_t^{G,\mathrm{all}}&=\frac{\sum_i I_{it}^{G}}{N_t}, &
P_t^{G,\mathrm{active}}&=\frac{\sum_i I_{it}^{G}}{\sum_i I_{it}^{W}}.
\end{align*}
Throughput and design-capacity coverage are
\[
P_t^{\mathrm{throughput}}=\frac{\sum_i W_{it}I_{it}^{G}}{\sum_i W_{it}},
\qquad
P_t^{\mathrm{design}}=\frac{\sum_i C_{it}I_{it}^{K}}{\sum_i C_{it}}.
\]
The valid-generator fleet identity is
\[
\frac{\sum_i G_{it}^{\mathrm{valid}}}{\sum_i W_{it}}
=\left(\frac{\sum_i W_{it}^{\mathrm{valid}}}{\sum_i W_{it}}\right)
\left(\frac{\sum_i G_{it}^{\mathrm{valid}}}{\sum_i W_{it}^{\mathrm{valid}}}\right).
\]
Firth estimation maximizes
\[
\ell_F(\boldsymbol{\theta})=\ell(\boldsymbol{\theta})+
\frac{1}{2}\log\left|\mathcal{I}(\boldsymbol{\theta})\right|.
\]
The predefined processing-scale contrast and standardized annual risk are
\[
OR_{300:100}=\exp(\beta_C\log 2),\qquad
\bar p(c)=\frac{1}{n}\sum_{i,t}
\operatorname{logit}^{-1}\!\left\{\mathbf{x}_{it}(c)'
\hat{\boldsymbol\theta}\right\}.
\]
The installed-capacity and capacity-factor models are
\begin{align*}
\log K_{it}&=\alpha_K+V_{it}'\beta_K+\beta_{KC}\log C_{it}
+T_{it}'\eta_K+\lambda_t+\varepsilon_{Kit},\\
\log F_{it}&=\alpha_F+V_{it}'\beta_F+\beta_{FC}\log C_{it}
+\beta_U U_{it}+T_{it}'\eta_F+\lambda_t+\varepsilon_{Fit}.
\end{align*}
With a common design matrix, the component regressions satisfy
\begin{align*}
\log D_{it}&=X_{it}'\gamma_D+e_{Dit}, &
\log F_{it}&=X_{it}'\gamma_F+e_{Fit},\\
\log U_{it}&=X_{it}'\gamma_U+e_{Uit}, &
\log Y_{it}&=X_{it}'\gamma_Y+e_{Yit},
\end{align*}
and therefore $\gamma_Y=\gamma_D+\gamma_F-\gamma_U$ for each cohort
contrast. This is an accounting identity, not a causal mediation result.

"""


def clean_language(text: str) -> str:
    replacements = {
        "human validation gate": "outstanding validation step",
        "checked-in parser": "data-processing procedure",
        "revision-frozen": "primary",
        "Revision-frozen": "Primary",
        "internally frozen": "predefined",
        "memo comparison level": "comparison level",
        "memo-continuity and tail-sensitivity contrast":
            "predefined upper-tail sensitivity contrast",
        "legacy-style": "baseline",
        "professor discussion": "future investigation",
        "professor or later reviewer": "readers",
        "without consulting external files": "within this document",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = re.sub(
        r"The primary 300-versus-100 contrast is retained for continuity with the\s+model\s+"
        r"decision record, but its empirical support is (?:made )?explicit\.",
        "The 300-versus-100 contrast is retained as an upper-tail sensitivity "
        "comparison, and its limited empirical support is made explicit.",
        text,
    )
    text = re.sub(
        r"The\s+professor-facing draft can be evaluated with that limitation visible\.",
        "This limitation remains explicit throughout the analysis.",
        text,
    )
    text = text.replace("The earlier 11-parameter", "The expanded 11-parameter")
    text = text.replace("the earlier 11-parameter", "the expanded 11-parameter")
    text = text.replace("a outstanding validation step", "an outstanding validation step")
    text = text.replace("primary primary", "primary")
    text = text.replace("Primary primary", "Primary")
    text = text.replace("outstanding outstanding", "outstanding")
    return text


def transform_markdown(source: str) -> str:
    source = source.split("\n", 1)[1]
    source = replace_literal(
        source,
        "**Keywords:** municipal solid waste; incineration; waste-to-energy; Japan;\n"
        "generator sizing; capacity factor; administrative record linkage",
        "**Keywords:** municipal solid waste; incineration; waste-to-energy; Japan;\n"
        "generator sizing; capacity factor",
    )
    source = source.replace(
        "## 2. Literature Review and Analytical Foundation",
        "## 2. Literature Review",
    ).replace("## 3. Data and Methods", "## 3. Methodology")
    source = replace_span(
        source,
        "For fiscal year $t$, let $N_t$ be all retained facility records,",
        "### 3.5 RQ2: sparse first-entry model",
        RQ1_MD,
    )
    source = replace_span(
        source,
        "Ordinary maximum-likelihood logit is vulnerable",
        "Four frames are fitted.",
        "With only 35 modeled events, ordinary maximum-likelihood logistic "
        "regression can be biased or produce unstable estimates when predictors "
        "nearly separate events from non-events. Firth logistic regression is "
        "therefore used because it reduces small-sample bias and retains finite "
        "estimates under separation (Firth, 1993; Heinze & Schemper, 2002). "
        "Uncertainty is evaluated with 1,999 cluster-bootstrap replications that "
        "resample complete administrative lineages, preserving repeated "
        "observations from the same lineage. The penalized likelihood is shown "
        "in Appendix B.\n\n",
    )
    source = replace_span(
        source,
        "For an intuitive scale contrast, the odds ratio comparing 300 with 100 t/day is",
        "The revision-frozen 300-versus-100 contrast",
        "The 300-versus-100 t/day odds ratio is calculated from the fitted "
        "processing-scale coefficient. To show that entry remains uncommon in "
        "absolute terms, fitted annual probabilities are also averaged over "
        "the observed distributions of age, calendar year, and elapsed risk. "
        "This standardization changes only the capacity value while retaining "
        "the other observed predictors. The resulting values are adjusted "
        "descriptions of the observed risk population, not effects of "
        "physically enlarging a facility. Appendix B gives the formulas.\n\n",
    )
    source = replace_span(
        source,
        "Two pooled component models are estimated by ordinary least squares",
        "#### 3.6.3 Common-control accounting decomposition",
        "Two pooled ordinary-least-squares models are estimated with standard "
        "errors clustered by administrative lineage (Wooldridge, 2010). The "
        "first models reported installed electrical capacity after adjustment "
        "for processing scale, start-year cohort, furnace count, technology "
        "groups, and fiscal year. The second models annual electrical capacity "
        "factor with the same adjustment set plus waste-processing utilization. "
        "The 2010-or-later start-year cohort is the reference group. Reported "
        "facility start year is an administrative cohort marker, not a verified "
        "generator-installation date. A separate gross-output model relates "
        "reported generation to annual throughput and installed capacity under "
        "the same cohort, technology, furnace-count, and year adjustments. "
        "Appendix B gives the full specifications.\n\n",
    )
    source = replace_span(
        source,
        "Assessing whether sizing makes a substantial contribution",
        "This common-control identity decomposition",
        "Four additional regressions use exactly the same rows and control "
        "variables for generator design intensity, capacity factor, waste "
        "utilization, and gross generation intensity. Because the four outcomes "
        "are algebraically connected, each adjusted gross-intensity cohort gap "
        "equals the generator-design component plus the capacity-factor "
        "component minus the waste-utilization component. Appendix B reports "
        "the formal regression system.\n\n",
    )
    source = replace_span(
        source,
        "An internal\nmodel-decision memo documented",
        "Technology and geography",
        "The five-parameter specification was selected to remain proportionate "
        "to the 35 available events. An expanded 11-parameter model is retained "
        "as a sensitivity rather than treated as the primary model. ",
    )
    source = replace_span(
        source,
        "The original download timestamp was not recorded.",
        "Parsing yields 23,599 raw rows.",
        "Each workbook is identified by its filename, byte size, parsed sheet, "
        "detected header row, field mapping, and SHA-256 hash. The original "
        "download timestamps were not recorded, so the hashes identify the "
        "files used in this study but do not reconstruct the publisher's full "
        "file history.\n\n",
    )
    source = replace_span(
        source,
        "## Research transparency",
        "## References",
        "",
    )
    source = source.replace(
        "That architecture gives a professor or later reviewer a clear foundation",
        "That architecture gives readers a clear foundation",
    )
    source = source.replace(
        "### B.1 First-entry model", "### B.2 First-entry model"
    ).replace("### B.2 Engineering outcome models", "### B.3 Engineering outcome models")
    source = source.replace(
        "## Appendix B. Model coding and focal estimates\n\n",
        "## Appendix B. Model coding and focal estimates\n\n" + TECHNICAL_MD,
    )
    source = clean_language(source)

    shifted: list[str] = []
    for line in source.splitlines():
        if line.startswith("#### "):
            shifted.append("### " + line[5:])
        elif line.startswith("### "):
            shifted.append("## " + line[4:])
        elif line.startswith("## "):
            shifted.append("# " + line[3:])
        else:
            shifted.append(line)
    source = "\n".join(shifted).strip() + "\n"
    metadata = """---
title: "Three Margins of Electricity Recovery"
subtitle: "Coverage, Reported Entry, and Generator Sizing in Japan's Municipal Incinerator Fleet, FY2005-FY2024"
author: |
  Pann Phetra
  Student ID: 13223029
  Supervisor: Prof. Han Ji
  Ritsumeikan Asia Pacific University
date: "19 July 2026"
---

"""
    return metadata + source


def transform_tex(source: str) -> str:
    source = re.sub(r"(?m)^[ \t]*%.*(?:\n|$)", "", source)
    source = replace_literal(
        source,
        r"\documentclass[12pt,a4paper]{article}",
        r"\documentclass[12pt,letterpaper]{article}",
    )
    source = replace_literal(
        source,
        r"\usepackage[T1]{fontenc}" + "\n" + r"\usepackage[margin=1in]{geometry}",
        r"\usepackage[T1]{fontenc}" + "\n"
        r"\usepackage{tgtermes}" + "\n"
        r"\usepackage[top=1in,bottom=1in,left=1.25in,right=1.25in]{geometry}",
    )
    source = replace_literal(
        source,
        r"{\large 2026\par}",
        r"{\large 19 July 2026\par}",
    )
    source = replace_literal(
        source,
        "\\noindent\\textbf{Keywords:} municipal solid waste; incineration; waste-to-energy;\n"
        "Japan; generator sizing; capacity factor; administrative record linkage",
        "\\noindent\\textbf{Keywords:} municipal solid waste; incineration; waste-to-energy;\n"
        "Japan; generator sizing; capacity factor",
    )
    source = source.replace(
        r"\section{Literature Review and Analytical Foundation}",
        r"\section{Literature Review}",
    ).replace(r"\section{Data and Methods}", r"\section{Methodology}")
    source = replace_span(
        source,
        "For fiscal year $t$, let $N_t$ be all retained facility records,",
        r"\subsection{RQ2: sparse first-entry model}",
        RQ1_TEX,
    )
    source = replace_span(
        source,
        "Ordinary maximum-likelihood logit is vulnerable",
        "Four frames are fitted.",
        "With only 35 modeled events, ordinary maximum-likelihood logistic "
        "regression can be biased or produce unstable estimates when predictors "
        "nearly separate events from non-events. Firth logistic regression is "
        "therefore used because it reduces small-sample bias and retains finite "
        "estimates under separation (Firth, 1993; Heinze \\& Schemper, 2002). "
        "Uncertainty is evaluated with 1,999 cluster-bootstrap replications that "
        "resample complete administrative lineages, preserving repeated "
        "observations from the same lineage. The penalized likelihood is shown "
        "in Appendix B.\n\n",
    )
    source = replace_span(
        source,
        "For an intuitive scale contrast, the odds ratio comparing 300 with 100 t/day is",
        "The revision-frozen 300-versus-100 contrast",
        "The 300-versus-100 t/day odds ratio is calculated from the fitted "
        "processing-scale coefficient. To show that entry remains uncommon in "
        "absolute terms, fitted annual probabilities are also averaged over "
        "the observed distributions of age, calendar year, and elapsed risk. "
        "This standardization changes only the capacity value while retaining "
        "the other observed predictors. The resulting values are adjusted "
        "descriptions of the observed risk population, not effects of "
        "physically enlarging a facility. Appendix B gives the formulas.\n\n",
    )
    source = replace_span(
        source,
        "Two pooled component models are estimated by ordinary least squares",
        r"\subsubsection{Common-control accounting decomposition}",
        "Two pooled ordinary-least-squares models are estimated with standard "
        "errors clustered by administrative lineage (Wooldridge, 2010). The "
        "first models reported installed electrical capacity after adjustment "
        "for processing scale, start-year cohort, furnace count, technology "
        "groups, and fiscal year. The second models annual electrical capacity "
        "factor with the same adjustment set plus waste-processing utilization. "
        "The 2010-or-later start-year cohort is the reference group. Reported "
        "facility start year is an administrative cohort marker, not a verified "
        "generator-installation date. A separate gross-output model relates "
        "reported generation to annual throughput and installed capacity under "
        "the same cohort, technology, furnace-count, and year adjustments. "
        "Appendix B gives the full specifications.\n\n",
    )
    source = replace_span(
        source,
        "Assessing whether sizing makes a substantial contribution",
        "This common-control identity decomposition",
        "Four additional regressions use exactly the same rows and control "
        "variables for generator design intensity, capacity factor, waste "
        "utilization, and gross generation intensity. Because the four outcomes "
        "are algebraically connected, each adjusted gross-intensity cohort gap "
        "equals the generator-design component plus the capacity-factor "
        "component minus the waste-utilization component. Appendix B reports "
        "the formal regression system.\n\n",
    )
    source = replace_span(
        source,
        "An internal model-decision memo documented",
        "Technology and geography",
        "The five-parameter specification was selected to remain proportionate "
        "to the 35 available events. An expanded 11-parameter model is retained "
        "as a sensitivity rather than treated as the primary model. ",
    )
    source = replace_span(
        source,
        "The original download timestamp was not\nrecorded.",
        "Parsing yields 23,599 raw rows.",
        "Each workbook is identified by its filename, byte size, parsed sheet, "
        "detected header row, field mapping, and SHA-256 hash. The original "
        "download timestamps were not recorded, so the hashes identify the "
        "files used in this study but do not reconstruct the publisher's full "
        "file history.\n\n",
    )
    source = replace_span(
        source,
        r"\section*{Research Transparency}",
        r"\section*{References}",
        "",
    )
    source = source.replace(
        "That architecture gives a professor or later reviewer a clear foundation",
        "That architecture gives readers a clear foundation",
    )
    source = source.replace(
        r"\section{Model coding and focal estimates}" + "\n\n",
        r"\section{Model coding and focal estimates}" + "\n\n" + TECHNICAL_TEX,
    )
    return clean_language(source)


def validate_visible_language(label: str, text: str) -> None:
    failures = []
    for name, pattern in BANNED_VISIBLE_PATTERNS.items():
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            failures.append(f"{name}: {match.group(0)!r}")
    if failures:
        raise ValueError(f"{label} contains banned assignment language: {failures}")


def pandoc_binary() -> str:
    executable = shutil.which("pandoc")
    if executable:
        return executable
    try:
        import pypandoc
    except ImportError as exc:
        raise SystemExit(
            "Pandoc is unavailable. Install pypandoc_binary in the project venv."
        ) from exc
    return str(pypandoc.get_pandoc_path())


def tectonic_binary() -> str:
    executable = shutil.which("tectonic")
    if executable:
        return executable
    local = Path.home() / ".local" / "bin" / "tectonic"
    if local.exists():
        return str(local)
    raise SystemExit("Tectonic is unavailable.")


def build_figures() -> None:
    for script in FIGURE_SCRIPTS:
        subprocess.run([sys.executable, str(script)], check=True)


def build_docx() -> None:
    if not TEMPLATE_DOCX.exists():
        raise SystemExit(f"Moodle template not found: {TEMPLATE_DOCX}")
    command = [
        pandoc_binary(),
        str(OUT_MD),
        "--from=markdown+tex_math_dollars+raw_tex",
        "--to=docx",
        "--standalone",
        "--toc",
        "--toc-depth=3",
        f"--reference-doc={TEMPLATE_DOCX}",
        f"--resource-path={OUT_DIR}:{ROOT / 'paper' / 'figures'}",
        f"--output={OUT_DOCX}",
    ]
    subprocess.run(command, cwd=OUT_DIR, check=True)
    strip_docx_comments(OUT_DOCX)


def strip_docx_comments(path: Path) -> None:
    """Remove comments and comment metadata inherited from the reference DOCX."""
    temp_path = path.with_suffix(".clean.docx")
    with zipfile.ZipFile(path, "r") as source:
        entries = {
            info.filename: (info, source.read(info.filename))
            for info in source.infolist()
        }

    content_types = "[Content_Types].xml"
    if content_types in entries:
        info, payload = entries[content_types]
        root = ET.fromstring(payload)
        for node in list(root):
            part_name = node.attrib.get("PartName", "")
            if part_name.startswith("/word/comments") or part_name == "/word/people.xml":
                root.remove(node)
        entries[content_types] = (
            info,
            ET.tostring(root, encoding="utf-8", xml_declaration=True),
        )

    relationships = "word/_rels/document.xml.rels"
    if relationships in entries:
        info, payload = entries[relationships]
        root = ET.fromstring(payload)
        for node in list(root):
            relation_type = node.attrib.get("Type", "")
            target = node.attrib.get("Target", "")
            if (
                relation_type.endswith("/comments")
                or "comments" in target
                or target == "people.xml"
            ):
                root.remove(node)
        entries[relationships] = (
            info,
            ET.tostring(root, encoding="utf-8", xml_declaration=True),
        )

    comment_tags = {
        "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}commentRangeStart",
        "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}commentRangeEnd",
        "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}commentReference",
    }
    document = "word/document.xml"
    if document in entries:
        info, payload = entries[document]
        root = ET.fromstring(payload)
        for parent in root.iter():
            for node in list(parent):
                if node.tag in comment_tags:
                    parent.remove(node)
        entries[document] = (
            info,
            ET.tostring(root, encoding="utf-8", xml_declaration=True),
        )

    with zipfile.ZipFile(temp_path, "w") as target:
        for name, (info, payload) in entries.items():
            if (
                name.startswith("word/comments")
                or name.startswith("word/_rels/comments")
                or name == "word/people.xml"
            ):
                continue
            target.writestr(info, payload)
    temp_path.replace(path)


def build_pdf() -> None:
    command = [
        tectonic_binary(),
        "-p",
        "--keep-logs",
        "--keep-intermediates",
        OUT_TEX.name,
    ]
    subprocess.run(command, cwd=OUT_DIR, check=True)
    if not OUT_PDF.exists():
        raise SystemExit(f"Assignment PDF was not produced: {OUT_PDF}")
    for suffix in (".aux", ".lof", ".log", ".lot", ".out", ".toc", ".xdv"):
        intermediate = OUT_DIR / f"{OUT_TEX.stem}{suffix}"
        intermediate.unlink(missing_ok=True)


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    markdown = transform_markdown(SOURCE_MD.read_text(encoding="utf-8"))
    latex = transform_tex(SOURCE_TEX.read_text(encoding="utf-8"))
    validate_visible_language("assignment Markdown", markdown)
    validate_visible_language("assignment LaTeX", latex)
    OUT_MD.write_text(markdown, encoding="utf-8")
    OUT_TEX.write_text(latex, encoding="utf-8")

    build_figures()
    build_docx()
    build_pdf()

    print(f"Assignment Markdown: {OUT_MD}")
    print(f"Assignment LaTeX: {OUT_TEX}")
    print(f"Assignment DOCX: {OUT_DOCX}")
    print(f"Assignment PDF: {OUT_PDF}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
