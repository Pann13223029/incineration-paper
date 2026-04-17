# AGENTS.md

Repository-wide guidance for coding and writing assistants.

## Purpose

This is a **paper-first derivative repo** seeded from the defended thesis workspace.

The thesis repo answered the bachelor's-thesis question and carries the full
supervision / defense machinery. This repo exists to extract a journal-style
paper from that base without destabilizing the original thesis workflow.

Do not treat this repo as a generic clone of the thesis project. Treat it as a
paper lab built on top of the same empirical core.

## Canonical Artifacts

| Area | Canonical artifact(s) | Rule |
| --- | --- | --- |
| Active paper prose | `paper/manuscript/paper.md` | Edit this directly for article-facing prose unless a task explicitly asks to work on the thesis record. |
| Thesis baseline | `thesis/thesis.tex` | Reference-only baseline for defended thesis claims and wording. Do not use it as the active paper draft. |
| Paper framing | `paper/notes/claim-stack.md`, `paper/notes/thesis-to-paper-map.md`, `paper/journals/target-journals.md` | Use these to keep the paper narrow, article-shaped, and journal-aware. |
| Analysis frame and estimation logic | `code/scripts/panel_utils.py` | Check this before changing any empirical claim, sample definition, or model description. |
| Generated sample and model facts | `output/sample_definition.md`, `output/adoption_results.md`, `output/regression_results.md`, `output/robustness_results.md`, `output/claim_verification.md` | Use these for current result values and repo-level sync status. |
| Paper-facing evidence snapshot | `paper/evidence/current/` | Refresh this with `npm run paper:sync` after any substantive result change. |
| Repo technical framing | `ARCHITECTURE.md` | Update when the active paper workflow, artifact flow, or source-of-truth structure materially changes. |
| Repo summary for readers | `README.md` | Update when a change materially affects the repo story, paper workflow, or active/reference boundary. |

## Core Rules

1. Keep the empirical core intact; the paper should narrow claims, not invent new evidence.
2. Treat `paper/manuscript/paper.md` as the active writing target.
3. Treat `thesis/thesis.tex` and `research/` as reference assets unless a task explicitly targets the thesis record.
4. Verify current facts from canonical outputs before repeating them.
5. Keep article claims narrower than thesis claims when in doubt.
6. Move technical overflow into paper notes or supplement planning instead of bloating the main paper draft.

## Working Defaults

- Audience: journal readers in waste management, industrial ecology, or environmental policy.
- Writing target: article-shaped, one dominant headline, lighter main text, stronger supplement.
- Source hierarchy: current `output/*` artifacts first, then `paper/*`, then `thesis/*` as baseline reference.
- Framing default: selective modernization on the adoption margin plus bounded responsiveness on the efficiency margin.

## Workflow

### Paper changes

- Edit `paper/manuscript/paper.md` directly.
- Before changing the article claim, check `paper/notes/claim-stack.md`.
- Before expanding scope, check `paper/notes/thesis-to-paper-map.md`.

### Analysis changes

- Inspect `code/scripts/panel_utils.py` first.
- Rebuild or refresh outputs before changing paper-facing empirical language.
- After substantive result changes, run `npm run paper:sync`.

### Sync rules

When a change materially affects paper-facing claims, decide explicitly whether each of these also needs an update:

- `paper/manuscript/paper.md`
- `paper/notes/claim-stack.md`
- `paper/notes/thesis-to-paper-map.md`
- `paper/journals/target-journals.md`
- `paper/evidence/current/*`
- `README.md`
- `ARCHITECTURE.md`

If only one layer is changed, leave a clear reason why the others do not need sync.

## Build And Verification

- Paper evidence sync: `python3 code/scripts/20_sync_paper_assets.py`
- Paper package scripts: `npm run paper:check` and `npm run paper:sync`
- Legacy thesis build and delivery commands remain available under the `legacy:*` namespace in `package.json`

## Maintenance

- Keep this file free of volatile claims and current result values.
- If the paper workflow or active/reference boundary changes, update this file in the same task.
- If assistant-specific files exist, they should stay thin and point back here.
