# Current Paper Status

This paper workspace now has a private GitHub remote, but it is still being
kept dormant as a side project.

Reason:
- the thesis remains the primary deliverable
- the paper is a side project derived from a frozen thesis evidence base
- keeping the repo private and lightly maintained reduces distraction and avoids
  turning the paper into a second live research track too early

## Current State

- private GitHub repo:
  - `https://github.com/Pann13223029/incineration-paper`
- frozen baseline tag:
  - `wm-near-submission-20260421`
- target journal: `Waste Management`
- manuscript status: near-submission draft
- figures in place: `3`
- main-text tables in place: `3`
- supplement: present
- title page, highlights, and cover letter: present
- export workflow: working via `npm run paper:export`
- LaTeX reading-PDF workflow: working via `npm run paper:build:latex`
- tracked share copy for cross-device reading:
  - `paper/share/waste-management-manuscript-latex.pdf`
- `paper:build:latex` now refreshes that tracked share copy automatically
- latest freeze includes:
  - tightened article framing
  - stronger Japan-specific and generator-only comparator citations
  - cleaned `Table 1` typesetting in the LaTeX manuscript
  - refreshed tracked shareable PDF

## What This Baseline Is Good For

- resuming paper work later without rebuilding the structure
- showing a clean article version of the thesis contribution
- preserving a stable private paper track after the thesis is fully settled

## What Is Still Deferred

- journal-system metadata beyond the local title page
- any new empirical analysis not needed for the thesis

## If Work Resumes Later

Start in this order:

1. `paper/manuscript/paper.md`
2. `paper/submission/submission-checklist.md`
3. `paper/supplement/supplement.md`
4. `paper/references/selected-references.md`

Then rerun:

```bash
npm run paper:export
npm run paper:build:latex
```

If the paper becomes active again, the next real decisions are editorial rather
than structural:

1. whether to revise the AI disclosure statement for actual submission
2. whether to expand the supplement further
3. whether to begin a true journal-submission workflow from this frozen baseline
