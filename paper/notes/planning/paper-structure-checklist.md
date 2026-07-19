# Paper Structure Checklist

## Narrative Spine

The paper is one integrated study with a descriptive baseline and two analytical
layers:

> Facility counts understate activity coverage; entry is rare and
> scale-selective; among generators, installed sizing and annual use are
> distinct components of gross output.

Every section should advance that spine.

## Recommended Structure

1. Introduction
2. Related evidence and comparator lineage
3. Data, provenance, and administrative-lineage reconstruction
4. Empirical design
5. Results
6. Discussion, limitations, and future validation
7. Conclusion

## Title

The title should name the fleet and signal the measurement contribution without
promising causal mechanisms. A suitable pattern is:

> From Facility Counts to Generator Components: Entry and Electricity Recovery
> in Japan's Waste-Incineration Fleet

Avoid titles centered on efficiency, lock-in, optimization, or causal retrofit
effects.

## Introduction Gate

By the end of page two, the reader must know:

- why 41.1% facility participation and 80.1% throughput coverage are different
- why administrative lineages had to be reconstructed
- the three research questions
- why sparse entry and generator components require different models
- the headline scale result and the restrained age result
- what was adapted from prior papers and what is original

## Data And Identity

Keep in the main text:

- workbook years and source provenance
- 23,593 retained records, 1,690 stable administrative lineages, and 1,767 asset episodes
- the source-code discontinuity problem
- a plain-language summary of matching evidence and executable guardrails
- the distinction between a stable administrative lineage and an asset episode

Move to the supplement:

- matching weights and thresholds
- low-margin records
- golden-link examples
- duplicate-collapse details
- permutation and insertion invariance implementation

## Methods

### Fleet baseline

- Define facility participation, throughput coverage, and design-capacity share.
- State every denominator.
- Explain why these quantities answer different planning questions.

### Sparse entry model

- Define first reported positive installed capacity after observed zero capacity.
- Distinguish the 55-event descriptive universe from the 35-event exact model.
- Explain the exact and prior-operation frames.
- Show the discrete-time equation and describe Firth bias reduction.
- State calendar-era, duration, age, and log-capacity terms.
- Explain stable-lineage bootstrap uncertainty and joint tests.

### Generator components

- Define engineering-valid operating-generator rows.
- Present generator design intensity and electrical capacity factor separately.
- Show how gross MWh/t combines installed sizing, annual generator use, and waste
  loading.
- Identify reported start year as a vintage proxy, not physical aging.
- Explain that the sizing-added gross model is a diagnostic.

## Results Order

1. **Fleet coverage and composition:** 41.1% facilities, 80.1% throughput, 70.5% design capacity; 19.50-point all-record rise versus 2.19 endpoint-common.
2. **Entry:** 55 descriptive events; broad/prior/same-episode events of
   35/33/24; revision-frozen broad scale odds ratio 6.72 and support-aware absolute risks.
3. **Age inference:** lineage-bootstrap joint p=0.380, 0.186, 0.051, and 0.357
   for broad, prior-operation, same-episode, and identity-certain frames.
4. **Components:** 6,511 rows across 493 stable administrative lineages; common-control component sums identify sizing as the largest older-cohort gap component.
5. **Sizing diagnostic:** in a separate 5,806-row frame with plausible heating
   value and heating value controlled, legacy age -0.0349, capacity +0.1001,
   and utilization +0.6699; after sizing, age -0.0020 (p=0.2977), capacity
   -0.0092 (p=0.1991), utilization -0.0995 (p=0.2038), sizing +0.7532
   (p<0.001), and R-squared 0.4737 to 0.8131. Treat this as a specification
   diagnostic, not causal mediation or part of the 6,511-row primary models.
6. **Pathways:** describe heterogeneity without assigning physical mechanisms.

Do not lead with coefficients before explaining the construct and denominator.

## Discussion Jobs

The discussion should answer four questions:

1. What does the count-volume divergence change about the original problem?
2. Why is scale selectivity meaningful even though causal mechanisms are not
   identified?
3. Why does separating installed sizing from annual use revise the old
   gross-output interpretation?
4. What external histories or engineering data would be needed for the next
   causal or technical step?

Include one compact comparator paragraph explaining adaptation rather than
similarity by assertion.

## Conclusion Gate

The conclusion should state:

- the count-volume answer
- robust scale selectivity and unsupported age headline
- the generator-sizing reinterpretation
- the narrow transferable measurement lesson

It must not introduce a new mechanism, policy ranking, or emissions estimate.

## Main Text Versus Supplement

Main text must stand alone on the research questions, constructs, equations,
samples, estimators, headline evidence, and interpretation limits.

The supplement should carry raw provenance detail, complete linkage audits,
additional Firth diagnostics, engineering-bound sensitivities, pathway coding,
and extended robustness results.

## Structural Failure Conditions

Revise before professor review if:

- the paper treats the 41.1% count as the whole empirical problem
- administrative-lineage reconstruction appears only in the supplement
- 55 descriptive events and 35 modeled events are conflated
- Firth regression is named but not motivated
- individual age coefficients override the joint tests
- gross MWh/t is described as efficiency
- installed generator sizing is absent from the central interpretation
- comparator influence is asserted without an adaptation map
- limitations are repeated but the estimand remains unclear
- tables, figures, abstract, and conclusion use different sample counts
