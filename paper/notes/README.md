# Paper Notes

These notes support drafting, positioning, professor discussion, and internal
review. They are not empirical sources. Active numbers must trace to generated
artifacts in [`output/`](../../output/), and a failed verifier overrides any note.

## Planning

- [Abstract and introduction checklist](planning/abstract-introduction-checklist.md):
  opening logic, research questions, jargon definitions, and comprehension test
- [Paper budget](planning/paper-budget.md): professor-review word, figure, table,
  equation, and scope limits
- [Paper structure checklist](planning/paper-structure-checklist.md): section
  order, methods coverage, results sequence, and failure conditions

## Positioning

- [Claim stack](positioning/claim-stack.md): authoritative narrative hierarchy
  and interpretation limits
- [Claim-to-evidence map](positioning/paper-claim-evidence-map.md): direct links
  from active claims to generated evidence
- [Professor comparator and method lineage](positioning/professor-comparator-method-lineage.md):
  equations, intellectual provenance, adaptation, and originality boundaries
- [Thesis-to-paper map](positioning/thesis-to-paper-map.md): what the paper keeps,
  reframes, removes, and defers

## Review

- [Professor and reviewer rubric](review/reviewer-rubric.md): hard gates and
  readiness scoring
- [Defense red-team revision map](review/defense-red-team-revision-map.md):
  resolved identity blockers, remaining attacks, revision priorities, and oral
  defense answers
- [Major-revision red-team review](review/major-revision-red-team-2026-07-14.md):
  multi-persona novelty attacks, resolved objections, and the remaining human
  linkage-validation gate
- [Professor meeting brief](review/professor-meeting-brief-2026-07-15.md):
  one-page orientation, intellectual foundation, and three decisions requested
- [Simulated linkage review](review/simulations/linkage-review-simulation-2026-07-15.md):
  synthetic reviewer agreement, conservative adjudication, and event-lineage
  model stress test; explicitly not human validation
- [Simulated professor review](review/simulations/professor-review-simulation-2026-07-15.md):
  likely supervisory questions, critique, answers, and meeting flow

## Current Anchor Set

- 23,593 retained records, 1,690 stable administrative lineages, 1,767 asset episodes; 16 accepted uncertain links exposed
- FY2024: 41.1% facility participation, 80.1% throughput coverage, 70.5%
  design-capacity coverage
- 55 descriptive entries; broad/prior/same-episode Firth frames
  15,154/1,137/35, 13,072/1,019/33, and 15,095/1,135/24; identity-certain
  15,107/1,130/35 for rows/lineages/events
- scale odds ratios 6.72/7.09/7.15/6.76 across broad/prior/same-episode/identity-certain frames; all event attacks remain within 6.12-7.30
- broad age -0.327 per decade (bootstrap CI -0.774 to 0.070), versus -0.751 (-1.364 to -0.206) in the 24-event same-episode frame
- generator components: 6,511 engineering-valid rows across 493 stable
  administrative lineages
- installed-kW elasticity 1.532; adjusted older-cohort installed capacity is
  79.1%/58.6%/23.5% lower while capacity factor is 35.3%/22.0%/1.5% higher
- separate sizing diagnostic: 5,806 engineering-valid rows with plausible
  heating value, explicitly controlling heating value; legacy age -0.0349,
  capacity +0.1001, and utilization +0.6699; after sizing, age -0.0020
  (p=0.2977), capacity -0.0092 (p=0.1991), utilization -0.0995 (p=0.2038),
  and sizing +0.7532 (p<0.001); R-squared 0.4737 to 0.8131; this is a
  specification diagnostic, not causal mediation

This duplicated anchor list is deliberate: it provides a fast stale-note check,
not an alternative source of truth.

## Update Protocol

1. Rebuild analysis outputs.
2. Review generated identity, entry, fleet, component, and robustness evidence.
3. Update the claim-to-evidence map and claim stack.
4. Update manuscript, supplement, TeX, tables, and figures.
5. Synchronize evidence and run claim and repository checks.
6. Rebuild and visually inspect the PDF before professor review.

Preserve superseded decisions only when they explain a resolved failure. Label
them explicitly as historical; never leave obsolete counts or interpretations
as active guidance.
