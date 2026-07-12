# Current Paper Status

The corrected empirical pipeline and professor-facing manuscript package form a verified review baseline as of 12 July 2026. Analysis reconstruction, estimator benchmarks, evidence synchronization, claim verification, format validation, LaTeX compilation, and visual PDF review have passed. This is ready for substantive professor review, but it is not yet a journal-submission decision or a substitute for human sign-off.

## Readiness

| Item | Current state |
|:--|:--|
| Repository | Private paper workspace at `https://github.com/Pann13223029/incineration-paper` |
| Target journal track | `Waste Management` |
| Empirical pipeline | Corrected identity, fleet, entry, component, robustness, quality, and claim stages implemented |
| Manuscript and supplement | Reconciled with the corrected four-frame entry and component evidence |
| Figures | Four regenerated academic figures; manuscript rendering inspected |
| Evidence snapshot | 33 canonical artifacts synchronized; `paper:check` passes |
| Claim verification | Passed for evidence integrity, Markdown, LaTeX, supplement, and professor packet |
| Reading PDF | Rebuilt as a 21-page LaTeX PDF; every page visually inspected |
| Presentation | Rebuilt as an 18-slide PDF; every slide visually inspected |
| Preferred PDF path | `paper/share/waste-management-manuscript-latex.pdf` |

Current PDF: [open in browser](https://raw.githack.com/Pann13223029/incineration-paper/main/paper/share/waste-management-manuscript-latex.pdf) or [download from GitHub](https://github.com/Pann13223029/incineration-paper/raw/refs/heads/main/paper/share/waste-management-manuscript-latex.pdf).

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
- `paper:check`, `claims:verify`, and `repo:check` passed after final evidence sync.
- The LaTeX manuscript and presentation PDFs were rebuilt and visually inspected page by page.
- The submission Markdown, HTML, and DOCX were regenerated; the DOCX archive is structurally valid.

## Next Human Actions

1. Obtain professor feedback on the three-estimand architecture, continuity-sensitive age inference, and comparator lineage.
2. Record requested substantive changes before journal-oriented compression or reframing.
3. Re-run the complete verification sequence after any analytical or numerical revision.

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
npm run repo:check
git diff --check
```

Submission readiness begins only after this sequence passes and the rebuilt PDF receives human visual review.
