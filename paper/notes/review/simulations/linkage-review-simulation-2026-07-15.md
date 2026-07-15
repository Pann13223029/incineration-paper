# Simulated Linkage Review And Adjudication

Simulation date: 15 July 2026

## Status Warning

This is a deterministic workflow simulation, not independent human validation.
Both synthetic reviewers use only fields visible in the blinded packet. The
answer key is opened only after their decisions to map unresolved pairs to
lineages and run a conservative model stress test. These results must not be
reported as inter-rater reliability or external validation in the manuscript.

## Simulation Design

- Reviewer A is continuity-focused and accepts corroborated name changes.
- Reviewer B is more skeptical and requires stronger agreement across visible
  name, municipality, official-code, timing, capacity, and configuration fields.
- Exact agreement preserves all four allowed decisions.
- Binary agreement collapses `same` and `probable reset` into one same-lineage
  class.
- The adjudicator resolves only pairs with strong visible corroboration. Hard
  cases remain unresolved and require an archived municipal or Ministry source.

## Agreement Results

| stratum                  |   pairs |   exact_agreements |   exact_agreement_pct |   four_category_kappa |   binary_same_lineage_agreement_pct |   binary_same_lineage_kappa |   adjudicated_same |   adjudicated_reset |   unresolved |
|:-------------------------|--------:|-------------------:|----------------------:|----------------------:|------------------------------------:|----------------------------:|-------------------:|--------------------:|-------------:|
| All packet pairs         |     558 |                549 |                98.387 |                 0.909 |                              98.925 |                       0.722 |                503 |                  43 |           12 |
| modeled_event_link       |      35 |                 33 |                94.286 |                 0.882 |                              97.143 |                       0.000 |                 21 |                  13 |            1 |
| identity_match_uncertain |      16 |                 16 |               100.000 |                 1.000 |                             100.000 |                       1.000 |                 12 |                   4 |            0 |
| fuzzy_link               |     375 |                367 |                97.867 |                 0.870 |                              98.400 |                       0.693 |                341 |                  23 |           11 |
| gap_link                 |      31 |                 29 |                93.548 |                 0.857 |                              96.774 |                       0.652 |                 21 |                   9 |            1 |
| fy2019_2020_bridge       |      50 |                 50 |               100.000 |                 1.000 |                             100.000 |                       1.000 |                 49 |                   1 |            0 |

Overall exact agreement is 549/558
(98.39%), with four-category Cohen's kappa
0.909. This high value is partly structural:
the packet contains accepted candidate links rather than a balanced set of
matches and non-matches.

The modeled-event binary kappa is zero despite 97.14% binary agreement because
Reviewer A assigns all 35 pairs to the same-lineage class while Reviewer B
assigns only one pair outside it. This is a prevalence/marginal-distribution
artifact; the raw agreement and four-category table are more informative here.

## Decision Distribution

| Decision | Reviewer A | Reviewer B | Adjudicated |
|:--|--:|--:|--:|
| Same administrative history | 507 | 502 | 503 |
| Same lineage, probable reset | 43 | 42 | 43 |
| Indeterminate | 0 | 6 | 0 |
| Different | 8 | 8 | 0 |
| Unresolved pending external source | 0 | 0 | 12 |

## Modeled-Event Adjudication

Among 35 modeled-event links, 34 are
accepted as the same administrative history or same lineage with a probable
reset. 1 remains unresolved: LV0201.
After unblinding for the stress test, this pair maps to
site_e22135c6e858.

## Conservative Model Rerun

The primary five-parameter Firth point model was rerun after deleting every
lineage attached to an unresolved modeled-event pair. The baseline contains
15,154 rows and 35 events, with a
300-versus-100 t/day odds ratio of 6.723. The
conservative rerun contains 15,149 rows and
34 events; its scale odds ratio is
7.296, and its age-per-decade coefficient is
-0.348.

This adverse simulated exclusion does not reverse the scale result. It is not a
substitute for adjudication: the unresolved event pair still requires an
independent reviewer and an archived source before the linkage layer can be
called externally validated.

## Real Review Handoff

1. Give reviewers only `output/linkage_validation_packet.csv` and the protocol.
2. Require independent decisions for all 35 modeled-event and 16 uncertain
   links, plus the agreed sample of other strata.
3. Archive evidence URLs and notes for every disagreement.
4. Open the answer key only after decisions are locked.
5. Rerun the canonical pipeline if any event lineage is rejected or split.
