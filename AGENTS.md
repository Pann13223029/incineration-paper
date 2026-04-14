# AGENTS.md

Repository-wide guidance for coding and writing assistants.

## Purpose

This file defines the stable operating rules for work in this thesis repo.
Do not use it as a source for volatile thesis facts such as sample sizes,
word counts, readiness claims, or current result values. Verify those from
the canonical artifacts listed below.

## Canonical Artifacts

| Area | Canonical artifact(s) | Rule |
| --- | --- | --- |
| Thesis prose | `thesis/thesis.tex` | Edit this directly for thesis-facing prose unless a task explicitly asks for a draft artifact. |
| Legacy chapter drafts | `thesis/0*-*.md` | Read-only legacy drafts. Do not regenerate `thesis/thesis.tex` from them. |
| Analysis frame and estimation logic | `code/scripts/panel_utils.py` | Check this before changing any empirical claim, sample definition, or model description. |
| Generated sample and model facts | `output/sample_definition.md`, `output/regression_results.md`, `output/robustness_results.md` | Use these for current published numbers. |
| Provenance | `output/manifests/` | Use this when tracing how an output was generated. |
| Repo-level technical framing | `ARCHITECTURE.md` | Update when the analytical design, artifact flow, or defended methodological framing materially changes. |
| Repo summary for readers | `README.md` | Update when a change materially affects the top-line repo story, workflow, or reproducibility instructions. |

## Core Rules

1. Verify current facts from canonical artifacts before repeating them.
2. Never fabricate citations or empirical claims. If support is missing, flag it explicitly.
3. Keep thesis-facing claims synchronized with the generated outputs they depend on.
4. State limitations, uncertainty, or competing interpretations before strong policy conclusions.
5. Preserve scope discipline for the main thesis design, but adjacent methods may be proposed when clearly labeled as robustness checks, limitations, or future work.
6. Treat durable repo policy and current thesis choices as different things. Stable workflow rules belong here; mutable analytical choices belong in the thesis and architecture artifacts.

## Working Defaults

- Audience: bachelor's-thesis level in sustainability / industrial ecology.
- Framing: material metabolism, infrastructure lock-in, and policy implications.
- Source hierarchy: if `thesis/thesis.tex`, generated outputs, and legacy drafts disagree, trust `thesis/thesis.tex` plus the generated outputs, then repair the stale layer.
- Writing target: lead with the finding, but do not compress out caveats needed for defendability.

## Workflow

### Prose changes

- Edit `thesis/thesis.tex` directly.
- Read the local section plus adjacent context before making substantive argument changes.
- Do not edit `thesis/0*-*.md` unless the task explicitly asks for draft back-porting or archival sync.

### Analysis changes

- Inspect `code/scripts/panel_utils.py` first.
- Rebuild analysis outputs when a change affects the sample, specification, coefficients, or reported numbers.
- Before changing thesis-facing empirical language, confirm the relevant current values in `output/sample_definition.md`, `output/regression_results.md`, and any relevant manifest.

### Sync rules

When a change materially affects thesis-facing claims, decide explicitly whether each of these also needs an update:

- `thesis/thesis.tex`
- `README.md`
- `ARCHITECTURE.md`
- `output/*` generated artifacts
- `output/manifests/*`

If only one layer is changed, leave a clear reason why the others do not need sync.

## Build And Verification

- Analysis rebuild entry point: `python3 code/scripts/07_rebuild_analysis.py`
- Thesis build: compile from `thesis/`
- Prefer `tectonic` if available; otherwise use the local LaTeX workflow required by the repo
- After a thesis build, review warnings that could affect defendability or formatting, especially table overflow, broken references, and citation issues

## Panel Workflow

- Use `research/notes/PANEL-PROTOCOL.md` for substantive analytic or argumentative changes, red-team review, or high-stakes prioritization.
- Do not invoke the panel workflow for trivial copyedits, formatting fixes, or single-paragraph cleanups unless the user explicitly asks for it.

## Maintenance

- Keep this file free of volatile status claims.
- When the repo workflow or source-of-truth structure changes, update this file in the same task.
- If assistant-specific files exist, they should be thin adapters that point back here rather than duplicating project facts.
