# Paper Claim Stack

Status: current professor-review framing. Numerical anchors must agree with the
generated files in `output/`; this note is not an independent evidence source.

## One-Sentence Answer

Japan's incineration fleet shows a count-volume divergence: installed
electricity generation is reported by 41.1% of FY2024 facilities, but those
facilities represent 80.1% of recorded waste throughput and 70.5% of
waste-processing design capacity; first reported entry is strongly
scale-selective, while generator vintage differences operate mainly through
installed generator sizing rather than an independent age-performance effect.

## Contribution

The paper combines one descriptive baseline with two analytical layers:

1. It distinguishes facility participation from throughput and design-capacity
   coverage.
2. It models sparse first reported entry into installed electrical-generation
   capacity in reconstructed administrative-lineage histories.
3. It decomposes gross generation per tonne into generator design intensity,
   electrical capacity factor, and waste loading.

The originality is this linked measurement design, not a claim that larger or
newer facilities generate more electricity in the abstract.

## Empirical Anchors

| Layer | Current result | Defensible reading |
|:--|:--|:--|
| Identity | 23,593 retained records, 1,690 stable administrative lineages, 1,767 asset episodes; 16 accepted uncertain links exposed | Longitudinal units are reconstructed and audited rather than assumed from survey codes |
| FY2024 fleet | 41.1% facility participation, 80.1% throughput coverage, 70.5% design-capacity coverage | A facility-count gap is not a waste-volume gap |
| Entry description | 55 first observed capacity-entry events | Events are uncommon and pathway-heterogeneous |
| Broad exact-year Firth frame | 15,154 lineage-years, 1,137 lineages, 35 events | Sparse-event inference requires bias reduction and restrained claims |
| Prior-operation Firth frame | 13,072 lineage-years, 1,019 lineages, 33 events | Nested sensitivity requiring positive prior-year operation |
| Continuity and linkage frames | Same episode: 15,095/1,135/24; identity certain: 15,107/1,130/35 rows/lineages/events | Age inference must be tested against continuity and linkage assumptions |
| Scale contrast | Odds ratio 6.13 in the broad frame and 6.25 in the prior-operation frame for 300 versus 100 t/day | Scale selectivity is the stable entry result |
| Age tests | Lineage-bootstrap joint p=0.380/0.186/0.051/0.357 across broad/prior/same-episode/identity-certain frames | Age coefficients do not support a universal headline and are continuity-sensitive |
| Generator components | 6,511 engineering-valid rows across 493 stable administrative lineages | Generator sizing and annual use must be separated |
| Sizing diagnostic | Separate 5,806-row plausible-heating-value frame with heating value controlled: legacy age -0.0349, capacity +0.1001, utilization +0.6699; after sizing, age -0.0020 (p=0.2977), capacity -0.0092 (p=0.1991), utilization -0.0995 (p=0.2038), sizing +0.7532 (p<0.001), and R-squared 0.4737 to 0.8131 | The former gross-MWh/t pattern is specification-sensitive after omitted generator sizing is added; this is not causal mediation and is distinct from the 6,511-row primary component analysis |

## Claim Hierarchy

### Level 1: Main contribution

- Facility counts, waste-volume coverage, entry selection, and conditional
  generator components answer different questions and should not be collapsed
  into one modernization statistic.

### Level 2: Headline findings

- Generation is much more concentrated in high-throughput facilities than the
  41.1% facility-participation statistic alone suggests.
- Larger waste-processing facilities are substantially more likely to report
  first installed generation capacity in both prespecified Firth frames.
- The age terms are not jointly significant, and their differences across
  frames are not statistically supported.
- Older reported start-year cohorts have lower generator design intensity; the
  separate 5,806-row diagnostic with plausible heating value and heating value
  controlled no longer independently supports age, processing capacity, or
  utilization after installed sizing is included. This is a specification
  result, not causal mediation, and it is distinct from the 6,511-row primary
  component models.

### Level 3: Supporting findings

- Reconstructed entry pathways help bound interpretation but do not establish
  retrofit, replacement, or new-build mechanisms.
- Electrical capacity factor captures annual generator use and should not be
  treated as the same construct as installed sizing.
- Adjacent-year persistence describes observed hierarchy; it does not bound
  feasible improvement.

### Level 4: Transferable lesson

- Administrative infrastructure studies should validate longitudinal identity
  and separate participation, activity-weighted coverage, installed design,
  and annual operation before drawing transition conclusions.

## Safe Interpretation

Use wording close to this:

> The estimates are descriptive associations within histories reconstructed as
> stable administrative lineages. Firth models address sparse first reported capacity entries, and
> component models separate installed generator sizing from annual use. They do
> not identify causal retrofit effects, policy shocks, thermodynamic efficiency,
> or feasible generation potential at facilities without reported output.

## Claims Not Supported

- age is a robust universal predictor of entry
- the age pattern differs significantly between entry frames
- administrative records identify a physical retrofit or replacement mechanism
- gross generation per tonne is thermodynamic or lifecycle efficiency
- the sizing diagnostic identifies a causal mechanism
- every non-generating facility should install generation
- facility participation equals the share of waste treated without generation
- the estimates identify a policy intervention or an optimal investment order

## Writing Rule

Every main-text paragraph must either define a construct, establish an evidence
link, explain the integrated contribution, or state a limitation needed to
interpret a headline result. Move everything else to the supplement or notes.
