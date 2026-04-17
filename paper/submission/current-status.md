# Current Paper Status

This paper workspace is intentionally local-only for now.

Reason:
- the thesis remains the primary deliverable
- the paper is a side project derived from a frozen thesis evidence base
- keeping the repo local reduces distraction and avoids turning the paper into a
  second live research track too early

## Current State

- target journal: `Waste Management`
- manuscript status: near-submission draft
- figures in place: `3`
- main-text tables in place: `3`
- supplement: present
- title page, highlights, and cover letter: present
- export workflow: working via `npm run paper:export`

## What This Baseline Is Good For

- resuming paper work later without rebuilding the structure
- showing a clean article version of the thesis contribution
- converting into a real submission track after the thesis is fully settled

## What Is Still Deferred

- creating a real remote
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
```
