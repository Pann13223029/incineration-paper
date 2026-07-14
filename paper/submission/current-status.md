# Current Paper Status

The repository now maintains two manuscript profiles over one empirical
pipeline as of 14 July 2026. The journal-facing public draft presents the
focused measurement contribution, while the preserved professor-facing version
retains the fuller methodological, comparator, diagnostic, and defense context.
Both profiles use the same generated evidence and claim-verification rules.
The public draft is ready for structured review, not journal submission.

## Readiness

| Item | Current state |
|:--|:--|
| Repository | Public review workspace at `https://github.com/Pann13223029/incineration-paper` |
| Target journal track | `Waste Management` |
| Empirical pipeline | Corrected identity, fleet, entry, component, robustness, quality, and claim stages implemented |
| Journal-facing draft | Focused 19-page draft: 213-word abstract, 5,909 conservative main-text words, three figures, and one table |
| Professor-facing draft | Preserved comprehensive 21-page version with four figures, two tables, and expanded method context |
| Shared supplement | Reconciled with the corrected four-frame entry and component evidence |
| Figures | Public draft uses three academic figures; exploratory pathway evidence remains outside its main text |
| Evidence snapshot | 33 canonical artifacts synchronized; `paper:check` passes |
| Claim verification | Profile-aware checks pass for journal and professor Markdown and LaTeX sources |
| Journal PDF | `paper/share/waste-management-manuscript-latex.pdf` |
| Professor PDF | `paper/share/professor-review-manuscript-latex.pdf` |
| Frozen professor baseline | Git tag `professor-review-v1` at `4ac9afe` |

Journal-facing PDF: [open in browser](https://raw.githack.com/Pann13223029/incineration-paper/main/paper/share/waste-management-manuscript-latex.pdf) or [download from GitHub](https://github.com/Pann13223029/incineration-paper/raw/refs/heads/main/paper/share/waste-management-manuscript-latex.pdf).

Professor-facing PDF: [open in browser](https://raw.githack.com/Pann13223029/incineration-paper/main/paper/share/professor-review-manuscript-latex.pdf) or [download from GitHub](https://github.com/Pann13223029/incineration-paper/raw/refs/heads/main/paper/share/professor-review-manuscript-latex.pdf).

## Corrected Evidence Baseline

- 23,599 parsed source rows become 23,593 unique retained records after exact-duplicate collapse.
- The identity layer contains 1,690 audited administrative facility lineages and 1,767 reported asset episodes; all 16 accepted uncertain links are exposed.
- Official facility codes are absent in FY2010-FY2012 and have zero overlap between FY2019 and FY2020; audited linkage restores 1,064 lineages across that break.
- `stable_site_id` is an administrative lineage, not proof of one immutable physical site, owner, or equipment configuration.
- The descriptive installed-capacity entry universe contains 55 events.
- The broad exact-year Firth model contains 15,154 rows, 1,137 lineages, and 35 events.
- The prior-operation Firth sensitivity contains 13,072 rows, 1,019 lineages, and 33 events.
- The same-episode continuity sensitivity contains 15,095 rows, 1,135 lineages, and 24 events.
- The identity-certain sensitivity contains 15,107 rows, 1,130 lineages, and 35 events.
- All four entry models complete 499 stable-lineage bootstrap replications; joint age p-values are 0.3800, 0.1863, 0.0508, and 0.3566, respectively.
- FY2024 installed-capacity participation is 41.1% by facility count, while positive-output facilities handle 80.1% of throughput and installed-generation facilities represent 70.5% of waste-processing design capacity.
- The generator component frame contains 6,511 engineering-valid rows across 493 lineages.
- Generator analysis separates installed design intensity from annual electrical capacity factor.
- Gross MWh/t remains a descriptive administrative output ratio, not a stand-alone efficiency measure.
- Administrative disappearance is not analyzed as physical closure.

## Completed Technical Gates

- Full raw-to-claims rebuild completed with exact workbook, code, input, and output hashes.
- The custom Firth estimator matches a closed-form separated-table solution and an independently optimized penalized likelihood.
- All four Firth models converged with all 499 requested whole-lineage bootstrap replications.
- Identity, continuity, component, robustness, data-quality, and identifier-gap audits passed.
- The journal and professor LaTeX profiles compile independently from shared evidence.
- Profile-aware `paper:check`, `claims:verify`, and repository-layout gates pass after evidence sync.
- The 19-page journal-facing PDF was visually inspected page by page for crop, overlap, spacing, and figure legibility.
- The submission Markdown, HTML, and DOCX were regenerated; the DOCX archive is structurally valid.

## Next Human Actions

1. Complete blinded human validation of the administrative-linkage and event-transition sample, with professor or second-reviewer adjudication for high-impact cases.
2. Freeze and run the lower-degree-of-freedom entry model, influence diagnostics, and at least 1,999 whole-lineage bootstrap replications.
3. Recast the engineering analysis around raw installed-capacity and gross-output quantities before finalizing the component claim.
4. Obtain professor feedback from the comprehensive profile before accepting the shorter journal-facing framing.
5. Resolve raw-workbook redistribution terms, licensing, citation metadata, and fresh-clone preflight behavior before public release is treated as archival publication.

## Deferred Scope

- Causal retrofit or intervention effects
- Verified closure and consolidation histories
- Net electricity export and useful-heat recovery
- Lifecycle avoided-emissions estimates
- Engineering-frontier or cost-effectiveness optimization
- Final journal-system metadata and venue-specific formatting

These require new data or a separate design and should not be inferred from the current administrative panel.

## Verification Sequence

```bash
npm run analysis:rebuild
npm run paper:sync
npm run paper:check
npm run claims:verify
npm run paper:export:nopdf
npm run paper:build:latex
npm run paper:build:professor
npm run repo:check
git diff --check
```

Submission readiness begins only after this sequence passes, the P0 scientific
workstreams are complete, and both the rebuilt PDF and substantive claims
receive human review.
