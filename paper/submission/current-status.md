# Current Paper Status

The repository now maintains two manuscript profiles over one empirical
pipeline as of 17 July 2026. The journal-facing public draft presents the
focused measurement contribution, while the professor-facing thesis version
retains the fuller methodological, comparator, diagnostic, and defense context
in A4 graduation-thesis format.
Both profiles use the same generated evidence and claim-verification rules.
The public draft is ready for structured review, not journal submission.

## Readiness

| Item | Current state |
|:--|:--|
| Repository | Public review workspace at `https://github.com/Pann13223029/incineration-paper` |
| Target journal track | `Waste Management` |
| Empirical pipeline | Identity, fleet composition, entry support, common-control components, robustness, quality, and claim stages implemented |
| Journal-facing draft | Major-revision draft with a three-margin contribution, support-audited Firth entry model, and common-control component attribution |
| Professor-facing thesis | Comprehensive A4 thesis profile with comparator adaptation, pathway context, and the same revised empirical core |
| Shared supplement | Reconciled with endpoint composition, entry support and collinearity, event attacks, and common-control components |
| Figures | Public draft uses three academic figures; exploratory pathway evidence remains outside its main text |
| Evidence snapshot | 53 synchronized artifacts, including lineage review, endpoint composition, entry support, influence, and component decomposition |
| Claim verification | Profile-aware checks pass for journal and professor Markdown and LaTeX sources |
| Journal PDF | `paper/share/waste-management-manuscript-latex.pdf` |
| Professor thesis PDF | `paper/share/professor-review-thesis.pdf` |
| Frozen professor baseline | Git tag `professor-review-v1` at `4ac9afe` |

Journal-facing PDF: [open in browser](https://raw.githack.com/Pann13223029/incineration-paper/main/paper/share/waste-management-manuscript-latex.pdf) or [download from GitHub](https://github.com/Pann13223029/incineration-paper/raw/refs/heads/main/paper/share/waste-management-manuscript-latex.pdf).

Professor-facing thesis PDF: [open in browser](https://raw.githack.com/Pann13223029/incineration-paper/main/paper/share/professor-review-thesis.pdf) or [download from GitHub](https://github.com/Pann13223029/incineration-paper/raw/refs/heads/main/paper/share/professor-review-thesis.pdf).

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
- The all-record installed-capacity share rises 19.50 points, but only 2.19 points among 732 endpoint-common lineages; administrative appearance and disappearance are not physical opening or closure measures.
- The revision-frozen five-parameter Firth model gives 300-versus-100 t/day odds ratios of 6.72, 7.09, 7.15, and 6.76 across the four frames.
- All four revised entry models complete 1,999 whole-lineage bootstrap replications; the broad scale interval is 4.31-12.46.
- The 300-t/day contrast is at the 98.98th empirical percentile with 315 risk rows and four events at or above it; support-aware predictions are also reported at 24, 60, and 120 t/day.
- Calendar and elapsed risk are correlated at 0.909 with VIFs of 5.76 and 6.15, while the processing-scale VIF is 1.10; the temporal coefficients are not interpreted separately.
- The 35 modeled events comprise 24 continuity-lineage and 11 rebuild/replacement-like entries; all 70 event attacks leave the scale odds ratio between 6.12 and 7.30.
- FY2024 installed-capacity participation is 41.1% by facility count, while positive-output facilities handle 80.1% of throughput and installed-generation facilities represent 70.5% of waste-processing design capacity.
- The generator component frame contains 6,511 engineering-valid rows across 493 lineages.
- The raw installed-kW model has a processing-scale elasticity of 1.532 and separates installed design from annual capacity factor.
- Relative to 2010 or later, adjusted installed kW is 79.1%, 58.6%, and 23.5% lower in the older cohorts, while capacity factor is 35.3%, 22.0%, and 1.5% higher.
- Under shared controls, generator sizing is the largest component of every older-cohort gross-intensity gap; the component sums reproduce each direct gap exactly and are not causal mediation.
- Gross MWh/t remains a descriptive administrative output ratio, not a stand-alone efficiency measure.
- Administrative disappearance is not analyzed as physical closure.

## Completed Technical Gates

- Full raw-to-claims rebuild completed with exact workbook, code, input, and output hashes.
- The custom Firth estimator matches a closed-form separated-table solution and an independently optimized penalized likelihood.
- All four revised Firth models converged with all 1,999 requested whole-lineage bootstrap replications.
- Every modeled event was reclassified and every event lineage deleted once without reversing the scale result.
- A 558-pair blinded linkage-review packet and separate answer key were generated; independent human completion remains pending.
- Identity, continuity, component, robustness, data-quality, and identifier-gap audits passed.
- The journal and professor-thesis LaTeX profiles compile independently from shared evidence.
- Profile-aware `paper:check`, `claims:verify`, and repository-layout gates pass after evidence sync.
- The 19-page journal PDF and 39-page A4 professor-facing thesis PDF were visually inspected for crop, overlap, spacing, equation layout, table breaks, and figure legibility.
- The submission Markdown and HTML were regenerated. DOCX export is an optional platform-dependent command and is not part of the portable verification sequence.

## Next Human Actions

1. Complete blinded human validation of the linkage packet, with professor or second-reviewer adjudication for high-impact cases.
2. Obtain professor feedback from the comprehensive profile before accepting the journal-facing framing.
3. Add a repository code license, citation metadata, and source-data attribution notice before treating the public repository as archival publication.
4. Confirm the fresh-clone preflight and full continuous-integration rebuild after this major revision.

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
