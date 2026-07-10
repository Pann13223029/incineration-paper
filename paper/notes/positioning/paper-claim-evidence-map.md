# Paper Claim-To-Evidence Map

This map links each active manuscript claim to generated evidence and states the
maximum interpretation that evidence supports. Generated files in `output/`
remain authoritative.

## Evidence Chain

| Claim | Primary evidence | Main-text minimum | Interpretation boundary |
|:--|:--|:--|:--|
| The longitudinal panel is auditable | [identity audit](../../../output/facility_identity_audit.md), [uncertain links](../../../output/identity_low_margin_links.csv), [identifier-gap audit](../../../output/identifier_gap_audit.md), [raw provenance](../../../output/raw_data_provenance.md) | State 23,593 retained records, 1,690 stable administrative lineages, 1,767 asset episodes, 16 exposed uncertain links, the code-regime problem, and deterministic guardrails | Reconstructed continuity is not proof of unchanged equipment, ownership, or physical-site continuity |
| Facility participation understates activity coverage | [fleet decomposition](../../../output/fleet_decomposition.md), [FY2024 segments](../../../output/fy2024_fleet_segments.csv) | Report 41.1% of facilities, 80.1% of throughput, and 70.5% of design capacity | Do not infer unobserved technical feasibility or net energy potential |
| First reported entry is scale-selective | [entry results](../../../output/adoption_results.md), [bootstrap coefficients](../../../output/adoption_bootstrap_coefficients.csv) | Define the event, show the broad and sensitivity frames, report 35/33/24 events, and give the 300-versus-100 t/day odds ratios of 6.13 and 6.25 | Association is not a causal effect of expanding a facility |
| Age is not a defensible general entry headline | [entry results](../../../output/adoption_results.md), [transition estimates](../../../output/figure2_transition_effects.csv) | Report joint age p=0.380/0.186/0.051/0.357 for broad/prior/same-episode/identity-certain frames | Individual negative coefficients do not establish a monotonic or universal age pattern; inference is continuity-sensitive |
| Gross output must be decomposed | [component results](../../../output/regression_results.md), [component table](../../../output/generator_component_results.csv), [robustness](../../../output/robustness_results.md) | Define generator design intensity and electrical capacity factor; report 6,511 rows and 493 stable administrative lineages | Gross MWh/t is an administrative output ratio, not thermodynamic efficiency |
| Installed generator sizing changes the former gross-intensity pattern | [component results](../../../output/regression_results.md), [component table](../../../output/generator_component_results.csv) | Distinguish the 5,806-row plausible-heating-value diagnostic, which explicitly controls heating value, from the 6,511-row primary models; report legacy age -0.0349, capacity +0.1001, and utilization +0.6699, then sizing-adjusted age -0.0020 (p=0.2977), capacity -0.0092 (p=0.1991), utilization -0.0995 (p=0.2038), sizing +0.7532 (p<0.001), and R-squared 0.4737 to 0.8131 | This is a specification diagnostic, not causal mediation |
| Pathways qualify entry interpretation | [entry results](../../../output/adoption_results.md), [pathway audit](../../../output/adoption_pathway_audit.csv), [post-entry trajectories](../../../output/post_adoption_trajectories.csv) | Distinguish continuity-lineage, rebuild/replacement-like, and forward-dated records; state that labels are administrative | Categories do not prove construction, retrofit, or replacement mechanisms |
| Findings survive prespecified checks | [robustness](../../../output/robustness_results.md), [data-quality sensitivity](../../../output/data_quality_sensitivity.md), [claim verification](../../../output/claim_verification.md) | Summarize only checks that bear directly on entry sparsity, linkage, engineering bounds, or component specification | A robustness ladder cannot convert observational associations into causal estimates |

## Required Main-Text Claim Sequence

1. **Measurement baseline:** facility participation differs from throughput and
   design-capacity coverage.
2. **Entry result:** first reported installed-capacity entry is rare and strongly
   associated with prior waste-processing scale.
3. **Age restraint:** broad and identity-certain joint tests are null, while
   the sparse same-episode result is borderline; age inference is continuity-sensitive.
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
