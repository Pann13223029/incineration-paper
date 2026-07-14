# Paper Claim-To-Evidence Map

This map links each active manuscript claim to generated evidence and states the
maximum interpretation that evidence supports. Generated files in `output/`
remain authoritative.

## Evidence Chain

| Claim | Primary evidence | Main-text minimum | Interpretation boundary |
|:--|:--|:--|:--|
| The longitudinal panel is auditable | [identity audit](../../../output/facility_identity_audit.md), [uncertain links](../../../output/identity_low_margin_links.csv), [identifier-gap audit](../../../output/identifier_gap_audit.md), [raw provenance](../../../output/raw_data_provenance.md) | State 23,593 retained records, 1,690 stable administrative lineages, 1,767 asset episodes, 16 exposed uncertain links, the code-regime problem, and deterministic guardrails | Reconstructed continuity is not proof of unchanged equipment, ownership, or physical-site continuity |
| Facility participation understates activity coverage | [fleet decomposition](../../../output/fleet_decomposition.md), [FY2024 segments](../../../output/fy2024_fleet_segments.csv) | Report 41.1% of facilities, 80.1% of throughput, and 70.5% of design capacity | Do not infer unobserved technical feasibility or net energy potential |
| First reported entry is scale-selective | [revised entry results](../../../output/revised_entry_results.csv), [bootstrap coefficients](../../../output/revised_entry_bootstrap.csv), [event attacks](../../../output/revised_entry_influence.csv) | Define the event; report 35/33/24 events; give the 300-versus-100 t/day odds ratios of 6.72/7.09/7.15/6.76 across frames and the 6.12-7.30 event-attack range | Association is not a causal effect of expanding a facility |
| Age is continuity-sensitive, not a general entry headline | [revised entry results](../../../output/revised_entry_results.csv), [scientific revision report](../../../output/scientific_revision_results.md) | Report broad age -0.327 per decade (bootstrap CI -0.774 to 0.070) and same-episode age -0.751 (-1.364 to -0.206; 24 events) | The stricter-frame result does not establish a monotonic or universal age barrier |
| Gross output must be decomposed | [component results](../../../output/regression_results.md), [component table](../../../output/generator_component_results.csv), [robustness](../../../output/robustness_results.md) | Define generator design intensity and electrical capacity factor; report 6,511 rows and 493 stable administrative lineages | Gross MWh/t is an administrative output ratio, not thermodynamic efficiency |
| Installed generator sizing changes the former gross-intensity pattern | [raw component results](../../../output/raw_quantity_component_results.csv), [adjusted component contrasts](../../../output/figure3_adjusted_components.csv), [component diagnostic](../../../output/regression_results.md) | Report installed-kW elasticity 1.532; installed-capacity cohort contrasts 79.1%, 58.6%, and 23.5% lower; capacity-factor contrasts 35.3%, 22.0%, and 1.5% higher; retain the 5,806-row sizing diagnostic as secondary | Reported start year is not generator installation date; this is not causal mediation |
| Pathways qualify entry interpretation | [entry results](../../../output/adoption_results.md), [pathway audit](../../../output/adoption_pathway_audit.csv), [post-entry trajectories](../../../output/post_adoption_trajectories.csv) | Distinguish continuity-lineage, rebuild/replacement-like, and forward-dated records; state that labels are administrative | Categories do not prove construction, retrofit, or replacement mechanisms |
| Findings survive prespecified checks | [robustness](../../../output/robustness_results.md), [data-quality sensitivity](../../../output/data_quality_sensitivity.md), [claim verification](../../../output/claim_verification.md) | Summarize only checks that bear directly on entry sparsity, linkage, engineering bounds, or component specification | A robustness ladder cannot convert observational associations into causal estimates |

## Required Main-Text Claim Sequence

1. **Measurement baseline:** facility participation differs from throughput and
   design-capacity coverage.
2. **Entry result:** first reported installed-capacity entry is rare and strongly
   associated with prior waste-processing scale.
3. **Age restraint:** the broad continuous-age interval spans zero, while the
   24-event same-episode estimate is more negative; age inference is continuity-sensitive.
4. **Engineering result:** reported start-year cohorts differ mainly in installed
   generator design intensity, while annual use is a separate component.
5. **Diagnostic correction:** in the separate 5,806-row plausible-heating-value
   frame with heating value controlled, age, processing capacity, and
   utilization are no longer independently supported after installed sizing
   enters the former gross-intensity model; this is specification evidence, not
   causal mediation.
6. **Integrated implication:** modernization cannot be evaluated from facility
   counts or one gross-output ratio alone.

## Construct Definitions That Must Stay Visible

- **Stable administrative lineage:** a deterministic history built from names,
  municipality, timing, capacity, technology, and source-code evidence.
- **Asset episode:** a segment within a stable administrative lineage separated by a material
  start-year or configuration reset.
- **Entry event:** first positive reported installed electrical-generation
  capacity after observed non-generating history.
- **Waste-processing design capacity:** tonnes of waste per day; this is the
  entry scale predictor.
- **Generator design intensity:** installed electrical kW per tonne/day of
  waste-processing design capacity.
- **Electrical capacity factor:** annual gross MWh relative to installed
  electrical capacity operating at nameplate for the year.
- **Gross generation intensity:** gross MWh per tonne of waste processed; a
  descriptive product of design and operation, not an efficiency measure.

## Red-Line Checks

Reject a draft if it:

- treats source facility codes as stable longitudinal identifiers
- equates the 41.1% facility share with the share of waste throughput
- reports conventional maximum-likelihood logit as the primary sparse-event
  estimator
- turns individual age coefficients into a headline despite the joint tests
- describes gross MWh/t as plant efficiency
- omits installed generator sizing from interpretation of gross output
- presents pathway labels or coefficients as causal mechanisms
- cites a comparator without stating what was adapted and what remains original

## Update Rule

When analysis changes, update generated evidence first, then this map, then the
manuscript and TeX source. No note may override a failed claim-verification check.
