# Current Paper Status

This paper workspace is a private side project derived from the defended thesis evidence base. It is ready to resume, but it should remain downstream of the canonical pipeline rather than becoming a second live research track.

## Current State

| Item | Status |
|:--|:--|
| Private GitHub repo | `https://github.com/Pann13223029/incineration-paper` |
| Frozen baseline tag | `wm-near-submission-20260421` |
| Target journal track | `Waste Management` |
| Manuscript | Professor-review-ready near-submission draft |
| Current review mode | Professor comprehension first; peer-review-safe wording preserved |
| Main figures | 3 |
| Main-text tables | 4 formal tables, plus 2 review-facing bridge maps kept for professor-review clarity |
| Supplement | Present and updated with event-definition, panel-exit, post-entry, persistence, data-quality, and estimator diagnostics |
| Title page, highlights, cover letter | Present |
| Evidence sync | Managed by `npm run paper:sync` |
| Claim verification | Managed by `npm run claims:verify` |
| Authoritative PDF | `paper/share/waste-management-manuscript-latex.pdf` |

## Latest Verified Baseline

The current repo includes:

- duplicate official-code and heating-value sensitivity checks
- operating-generator inclusion audit showing 907 uncoded operating-generator rows, concentrated in FY2010-FY2012
- event-timing disclosure showing 109 of 141 observed first-adoption events occur in FY2013-FY2019 without treating that cluster as an identified policy shock
- precise main event definition as first positive installed generation capacity
- positive-output event sensitivity with 146 exact-year events and the same age/scale pattern
- post-entry bridge showing 135 of 141 capacity entrants report positive output by the following year and 137 appear in the canonical generator frame within three years
- competing panel-exit diagnostic covering 1,285 final coded-panel exits without equating administrative disappearance with physical closure
- quantified FY2024 power-generation share of 41.1% in the abstract and introduction
- explicit adoption-hazard and electricity-recovery regression equations in the
  main manuscript
- review-facing comparator-adaptation and method-to-RQ bridge maps in the
  main manuscript
- a documented bridge-map placement decision: keep both bridge maps in the
  professor-review manuscript; move the research-question-to-model bridge to
  the supplement during journal compression if needed
- explicit two-margin contribution wording clarifying that the novelty is not
  simply that age and scale matter, but that entry and post-entry performance
  show distinct fleet constraints
- reader-facing regression guide explaining AMEs, log coefficients, fiscal-year
  indicators, random effects, facility fixed effects as a different estimand, and clustered standard errors
- stronger methods-defense wording explaining parsimony in the sparse adoption
  hazard and the descriptive purpose of the OLS/year-FE/RE model ladder
- official MOE/e-Stat source citation updated to the FY2024 survey release and
  statistics code `00650101`
- adoption-hazard duration robustness added to guard against time-at-risk
  dependence
- within-between electricity-recovery sensitivity added to separate
  cross-facility means from within-facility deviations
- adjacent-year percentile-rank persistence of 0.9325 across 4,368 exact pairs
- unclipped-log outcome sensitivity and explicit gross MWh/t and utilization definitions
- interpolated grid emissions factor removed from the core regressions
- supplement abbreviation guide and reviewer-response map for predictable
  concerns about adoption events, random effects, uncoded rows, heating value,
  and planning implications
- supervisor-facing comparator and method-lineage packet at
  `paper/notes/professor-comparator-method-lineage.md`
- explicit facility-clustered standard-error language for the electricity-recovery models
- safer policy wording around asset-renewal screening and capital-side triage
- planning interpretation framed as triage rather than intervention ranking
- synced data-quality report in `paper/evidence/current/data_quality_sensitivity.md`
- supplement language documenting the sensitivity checks, inclusion audit, and event-timing caveat
- claim verification passing locally and in GitHub Actions
- rebuilt LaTeX reading PDF in `paper/share/`

## What This Baseline Is Good For

- resuming paper work without rebuilding the structure
- explaining the article version of the thesis contribution
- giving a professor the methodological foundation and comparator lineage
  without making the manuscript sound like a private supervision note
- preserving a stable private paper track after thesis completion
- keeping reviewer-sensitive caveats visible before submission
- preventing older, stronger renewal wording from being accidentally revived in future edits

## What Is Still Deferred

- journal-system metadata beyond local submission files
- final journal-specific formatting
- new causal, closure-history, net-export, heat-recovery, or engineering-frontier analysis
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
5. `paper/notes/professor-comparator-method-lineage.md`

After editing, refresh artifacts:

```bash
npm run paper:export:nopdf
npm run paper:build:latex
```

If the edit is purely stylistic and does not touch evidence or claims, `analysis:rebuild` can be skipped. Still run `paper:check`, `claims:verify`, and `paper:build:latex` before pushing.

## Next Real Decisions

1. Whether the professor agrees that the two-margin diagnostic is the right
   central contribution.
2. Whether to do a final human editorial pass for readability and journal tone.
3. Whether journal mode should move the research-question-to-model bridge from
   the main text into the supplement.
4. Whether to expand or compress the supplement for the actual target journal.
5. Whether the journal submission should retain the current full AI disclosure wording or adapt it to the submission form without reducing its scope.
6. Whether to start a true journal-submission workflow from this private baseline.
