# Current Paper Status

This paper workspace is a private side project derived from the defended thesis evidence base. It is ready to resume, but it should remain downstream of the canonical pipeline rather than becoming a second live research track.

## Current State

| Item | Status |
|:--|:--|
| Private GitHub repo | `https://github.com/Pann13223029/incineration-paper` |
| Frozen baseline tag | `wm-near-submission-20260421` |
| Target journal track | `Waste Management` |
| Manuscript | Near-submission draft |
| Main figures | 3 |
| Main-text tables | 3 |
| Supplement | Present and updated with data-quality, identifier, and event-timing caveats |
| Title page, highlights, cover letter | Present |
| Evidence sync | Managed by `npm run paper:sync` |
| Claim verification | Managed by `npm run claims:verify` |
| Authoritative PDF | `paper/share/waste-management-manuscript-latex.pdf` |

## Latest Verified Baseline

The current repo includes:

- duplicate official-code and heating-value sensitivity checks
- operating-generator inclusion audit showing 907 uncoded operating-generator rows, concentrated in FY2010-FY2012
- event-timing disclosure showing 109 of 141 observed first-adoption events occur in FY2013-FY2019 without treating that cluster as an identified policy shock
- quantified FY2024 power-generation share of 41.1% in the abstract and introduction
- explicit facility-clustered standard-error language for the efficiency models
- safer policy wording around asset-renewal screening and capital-side triage
- synced data-quality report in `paper/evidence/current/data_quality_sensitivity.md`
- supplement language documenting the sensitivity checks, inclusion audit, and event-timing caveat
- claim verification passing locally and in GitHub Actions
- rebuilt LaTeX reading PDF in `paper/share/`

## What This Baseline Is Good For

- resuming paper work without rebuilding the structure
- explaining the article version of the thesis contribution
- preserving a stable private paper track after thesis completion
- keeping reviewer-sensitive caveats visible before submission
- preventing older, stronger renewal wording from being accidentally revived in future edits

## What Is Still Deferred

- journal-system metadata beyond local submission files
- final journal-specific formatting
- any new empirical analysis beyond the current sensitivity checks
- human editorial review of tone, concision, and target-journal fit

## Resume Workflow

Use this order if work resumes:

```bash
npm run analysis:rebuild
npm run paper:sync
npm run paper:check
npm run claims:verify
```

Then review:

1. `paper/manuscript/paper.md`
2. `paper/supplement/supplement.md`
3. `paper/submission/submission-checklist.md`
4. `paper/references/selected-references.md`

After editing, refresh artifacts:

```bash
npm run paper:export:nopdf
npm run paper:build:latex
```

If the edit is purely stylistic and does not touch evidence or claims, `analysis:rebuild` can be skipped. Still run `paper:check`, `claims:verify`, and `paper:build:latex` before pushing.

## Next Real Decisions

1. Whether to do a final human editorial pass for readability and journal tone.
2. Whether to expand or compress the supplement for the actual target journal.
3. Whether to revise the AI disclosure statement for the actual submission context.
4. Whether to start a true journal-submission workflow from this private baseline.
