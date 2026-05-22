# Paper Workspace

This directory is the active article layer. It contains the manuscript, supplement, figures, evidence snapshots, and submission package for the journal-style paper.

## Current Role

- Active writing target: `paper/manuscript/paper.md`
- Final reading/PDF source: `paper/manuscript/paper.tex`
- Target journal track: `Waste Management`
- Current share PDF: `paper/share/waste-management-manuscript-latex.pdf`
- Evidence copies: `paper/evidence/current/`

The paper layer narrows and reorganizes the thesis evidence. It must not become a second source of empirical truth.

## Start Here

| Task | File |
|:--|:--|
| Read or edit the paper | [`manuscript/paper.md`](manuscript/paper.md) |
| Check final PDF source | [`manuscript/paper.tex`](manuscript/paper.tex) |
| Check current submission state | [`submission/current-status.md`](submission/current-status.md) |
| Check paper claim discipline | [`notes/claim-stack.md`](notes/claim-stack.md) |
| Check thesis-to-paper conversion logic | [`notes/thesis-to-paper-map.md`](notes/thesis-to-paper-map.md) |
| Check reviewer risks | [`notes/reviewer-rubric.md`](notes/reviewer-rubric.md) |
| Check supplement | [`supplement/supplement.md`](supplement/supplement.md) |
| Check synced evidence | [`evidence/`](evidence/) |
| Present the paper in a Zoom meeting | [`slides/paper-zoom-briefing.md`](slides/paper-zoom-briefing.md) |

## Directory Roles

| Path | Role |
|:--|:--|
| `manuscript/` | Active paper prose and LaTeX source. |
| `figures/` | Paper figure scripts and rendered figure files. |
| `tables/` | Paper-facing table drafts and extracted result tables. |
| `notes/` | Claim stack, structure checks, paper budget, and reviewer rubric. |
| `references/` | Selected references and citation plan. |
| `slides/` | Paper-focused Zoom briefing deck, full speaker script, and presentation theme. |
| `supplement/` | Supplement text and supplement planning. |
| `submission/` | Local submission package outputs and administrative files. |
| `share/` | Tracked PDF for reading from another machine. |
| `evidence/` | Synced copies of selected canonical outputs from `../output/`. |

## Paper Commands

Refresh paper-facing evidence copies:

```bash
npm run paper:sync
```

Check that evidence copies are current:

```bash
npm run paper:check
```

Export Markdown, HTML, and DOCX submission files without relying on browser PDF:

```bash
npm run paper:export:nopdf
```

Build the authoritative LaTeX reading PDF:

```bash
npm run paper:build:latex
```

Run claim synchronization checks:

```bash
npm run claims:verify
```

Export the paper Zoom briefing deck:

```bash
npm run slides:paper
```

Export the shareable paper Zoom briefing PDF:

```bash
npm run slides:paper:pdf
```

## Output Rules

- Use `paper/share/waste-management-manuscript-latex.pdf` for cross-device reading.
- Use `paper/share/paper-zoom-briefing.pdf` for Zoom screen sharing.
- Use `paper/submission/waste-management-manuscript-latex.pdf` for local submission package review.
- Use `paper/submission/waste-management-manuscript.docx` only when a DOCX workflow is needed.
- Treat `paper/submission/waste-management-manuscript.pdf` as browser-export convenience only, not the preferred PDF.

## Resume Workflow

If paper work resumes after a pause:

1. Run `npm run analysis:rebuild` if evidence may have changed.
2. Run `npm run paper:sync`.
3. Run `npm run paper:check`.
4. Read `submission/current-status.md`.
5. Edit `manuscript/paper.md` or `manuscript/paper.tex` as needed.
6. Run `npm run claims:verify`.
7. Rebuild artifacts with `npm run paper:export:nopdf` and `npm run paper:build:latex`.

If the work is prose-only and no empirical claim changes, steps 1 and 2 can be skipped, but `claims:verify` should still pass before pushing.
