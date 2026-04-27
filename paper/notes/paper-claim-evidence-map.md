# Paper Claim-To-Evidence Map

This note protects the manuscript against over-cutting during thesis-to-paper
compression.

For each core claim, it records:

- what the claim is
- which current evidence artifact supports it
- what must stay in main text
- what can move to supplement

## Claim 1: The fleet transition problem is empirically two-part

Claim:

- the paper must separate transition into generation from conditional
  performance within the generating segment

Current evidence:

- [sample_definition.md](../evidence/current/sample_definition.md)
- [adoption_results.md](../evidence/current/adoption_results.md)
- [regression_results.md](../evidence/current/regression_results.md)

Must stay in main text:

- one sentence defining the adoption frame
- one sentence defining the generator frame
- one framework figure showing why one average fleet model is insufficient

May move to supplement:

- extra sample-construction detail
- edge-case cleaning notes

## Claim 2: Observed transition into generation is selective rather than diffuse

Claim:

- within the coded adoption frame, younger and larger facilities are more likely
  to record observed transition into generation

Current evidence:

- [adoption_results.md](../evidence/current/adoption_results.md)

Must stay in main text:

- adoption model sample counts
- one adoption results table
- one adoption figure or compact event-rate visualization
- plain-language statement of the age and capacity pattern
- concise disclosure that 109 of 141 first-adoption events occur in
  FY2013-FY2019, without interpreting the cluster as an identified shock

May move to supplement:

- alternative lag structures
- extended event-year detail
- extra subgroup tables

## Claim 3: Conditional generator performance is bounded and strongly structured

Claim:

- within the canonical generator frame, performance is structured by age, scale,
  and utilization, and between-facility structure matters more than large
  within-facility movement

Current evidence:

- [regression_results.md](../evidence/current/regression_results.md)
- [sample_definition.md](../evidence/current/sample_definition.md)
- [data_quality_sensitivity.md](../evidence/current/data_quality_sensitivity.md)

Must stay in main text:

- generator sample counts
- one efficiency results table
- the within / total variance ratio in prose or compact display
- a concise interpretation of bounded responsiveness
- short explanation that the canonical generator frame excludes 907 uncoded
  operating-generator rows and that the supplement audits this exclusion

May move to supplement:

- fuller estimator comparisons
- extra robustness variants
- expanded post-Fukushima split detail

## Claim 4: The paper supports a calibrated asset-renewal interpretation

Claim:

- the evidence is most consistent with asset-renewal screening and capital-side
  triage at the weak end of the fleet, alongside bounded responsiveness within
  the generating segment

Current evidence:

- [adoption_results.md](../evidence/current/adoption_results.md)
- [regression_results.md](../evidence/current/regression_results.md)
- [data_quality_sensitivity.md](../evidence/current/data_quality_sensitivity.md)

Must stay in main text:

- one synthesis paragraph linking the two margins
- one sentence marking this as an evidence-consistent interpretation, not a
  uniquely identified mechanism
- one sentence avoiding stronger claims that the data directly identify capital
  replacement, policy-shock timing, or governance effects

May move to supplement:

- longer policy discussion
- extended comparisons with alternative institutional channels

## Claim 5: The pathway audit is supportive, not the paper's main novelty

Claim:

- the pathway audit bounds mechanism language without proving replacement,
  refurbishment, or new build as the unique pathway

Current evidence:

- [adoption_results.md](../evidence/current/adoption_results.md)

Must stay in main text:

- concise category summary
- one sentence saying the audit supports calibrated interpretation rather than
  mechanism proof

May move to supplement:

- rule detail
- classification logic
- extra audit tables

## Use Rule

Before cutting anything from the manuscript, check whether it protects one of
the `Must stay in main text` items above.

If yes, keep it or replace it with something equally clear.
