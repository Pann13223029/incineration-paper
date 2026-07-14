# Paper Workspace

This directory contains the active article, supplement, figures, evidence snapshot, presentation, and submission artifacts for the Japan municipal waste-incineration study.

## Current Role

- Target journal track: `Waste Management`
- Public journal prose: [`manuscript/paper.md`](manuscript/paper.md)
- Public LaTeX source: [`manuscript/paper.tex`](manuscript/paper.tex)
- Professor prose: [`manuscript/professor/paper.md`](manuscript/professor/paper.md)
- Professor LaTeX source: [`manuscript/professor/paper.tex`](manuscript/professor/paper.tex)
- Revision state: [`submission/current-status.md`](submission/current-status.md)
- Canonical evidence: [`../output/`](../output/)
- Synchronized evidence copies: [`evidence/`](evidence/)
- Journal-facing PDF: [open in browser](https://raw.githack.com/Pann13223029/incineration-paper/main/paper/share/waste-management-manuscript-latex.pdf) or [download from GitHub](https://github.com/Pann13223029/incineration-paper/raw/refs/heads/main/paper/share/waste-management-manuscript-latex.pdf)
- Professor-facing PDF: [open in browser](https://raw.githack.com/Pann13223029/incineration-paper/main/paper/share/professor-review-manuscript-latex.pdf) or [download from GitHub](https://github.com/Pann13223029/incineration-paper/raw/refs/heads/main/paper/share/professor-review-manuscript-latex.pdf)

The shared empirical core, focused public draft, and preserved professor package form the current review baseline. The status page records completed rebuilds, evidence sync, claim checks, format gates, and visual PDF inspection; rerun those gates after any substantive change.

## Paper Logic

The article links three evidence blocks:

1. FY2024 count-volume decomposition: 41.1% facility participation, 80.1% throughput coverage, and 70.5% waste-processing design-capacity share.
2. First reported installed-capacity entry: 55 descriptive events, with the broad exact-year Firth model on 15,154 rows across 1,137 administrative lineages and 35 events.
3. Conditional generator components: 6,511 engineering-valid rows across 493 lineages, separating installed generator design intensity from annual electrical capacity factor.

The prior-operation sensitivity uses 13,072 rows, 1,019 lineages, and 33 events; same-episode continuity uses 15,095/1,135/24; and identity-certain linkage uses 15,107/1,130/35 rows/lineages/events. Administrative disappearance is not modeled. Gross MWh/t is not presented as a stand-alone efficiency measure.

## Start Here

| Task | File |
|:--|:--|
| Read or revise the public article | [`manuscript/paper.md`](manuscript/paper.md) |
| Check public PDF wording | [`manuscript/paper.tex`](manuscript/paper.tex) |
| Review the comprehensive professor version | [`manuscript/professor/paper.md`](manuscript/professor/paper.md) |
| Check readiness and blockers | [`submission/current-status.md`](submission/current-status.md) |
| Inspect synchronized evidence | [`evidence/README.md`](evidence/README.md) |
| Trace claims to outputs | [`../output/claim_evidence_map.md`](../output/claim_evidence_map.md) |
| Review source and identity audits | [`../output/raw_data_provenance.md`](../output/raw_data_provenance.md), [`../output/facility_identity_audit.md`](../output/facility_identity_audit.md) |
| Review supplement detail | [`supplement/supplement.md`](supplement/supplement.md) |
| Review comparator lineage | [`notes/positioning/professor-comparator-method-lineage.md`](notes/positioning/professor-comparator-method-lineage.md) |
| Review current red-team plan | [`notes/review/defense-red-team-revision-map.md`](notes/review/defense-red-team-revision-map.md) |
| Present the study | [`slides/paper-zoom-briefing.md`](slides/paper-zoom-briefing.md) |

## Directory Roles

| Path | Role |
|:--|:--|
| `manuscript/` | Public journal sources plus the comprehensive professor profile. |
| `supplement/` | Identity, estimator, robustness, and supporting detail. |
| `figures/` | Figure builders plus rendered PDF/PNG assets. |
| `tables/` | Paper-facing table drafts and extracts. |
| `evidence/current/` | Generated copies of selected canonical `output/` artifacts. |
| `notes/` | Planning, positioning, comparator, and review workspaces. |
| `references/` | Selected references and citation planning. |
| `slides/` | Zoom briefing deck, theme, and speaker script. |
| `submission/` | Review and journal-package artifacts; not empirical sources. |
| `share/` | Tracked cross-device reading and presentation PDFs. |

## Evidence Hierarchy

```text
../output/* canonical evidence
  -> evidence/current/* synchronized copies
  -> manuscript and supplement interpretation
  -> submission and share artifacts
```

If any numbers disagree, resolve the canonical output first. `stable_site_id` refers to an audited administrative facility lineage, not a proven immutable physical site.

## Commands

```bash
npm run paper:sync
npm run paper:check
npm run claims:verify
npm run paper:export:nopdf
npm run paper:build:latex
npm run paper:build:professor
npm run slides:paper
npm run slides:paper:pdf
```

- `paper:sync` refreshes selected evidence copies.
- `paper:check` fails when those copies are missing or stale.
- `claims:verify` checks registered high-risk claims and stale wording.
- `paper:export:nopdf` creates Markdown, HTML, and DOCX review files.
- `paper:build:latex` creates the public journal reading PDF.
- `paper:build:professor` creates the comprehensive professor reading PDF.

Use `share/waste-management-manuscript-latex.pdf` for the public journal draft,
`share/professor-review-manuscript-latex.pdf` for comprehensive supervision,
`submission/waste-management-manuscript-latex.pdf` for local package review,
and `share/paper-zoom-briefing.pdf` for screen sharing.

## Resume Workflow

```bash
npm run analysis:rebuild
npm run paper:sync
npm run paper:check
npm run claims:verify
npm run paper:export:nopdf
npm run paper:build:latex
npm run paper:build:professor
```

If only style changes and no empirical statement changes, the full analysis rebuild can be skipped. The evidence sync, claim check, and relevant artifact build must still be current before human review.
