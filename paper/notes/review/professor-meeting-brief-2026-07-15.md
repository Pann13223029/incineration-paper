# Professor Meeting Brief

Meeting purpose: obtain direction on the paper's intellectual framing and the
remaining identity-validation requirement before journal-oriented polishing.

Primary document: [professor-facing manuscript](../../share/professor-review-manuscript-latex.pdf)

## The Paper In One Minute

The paper does not ask only whether Japanese incinerators generate electricity.
It separates three questions that are usually collapsed:

1. **Coverage:** how common generation is by facility count versus how much
   waste and processing capacity sit at generating facilities.
2. **Entry:** which observed non-generating administrative lineages first report
   installed electrical capacity.
3. **Components:** whether apparent cohort differences arise from installed
   generator sizing or from annual use of that installed capacity.

The FY2024 shares are 41.1% of facility records, 80.1% of throughput, and 70.5%
of processing design capacity. The frozen five-parameter Firth model estimates
a 300-versus-100 t/day entry odds ratio of 6.72, with a 1,999-lineage-bootstrap
interval of 4.31-12.46. Adjusted older-cohort installed kW is much lower, while
annual capacity factors are not uniformly lower. The central interpretation is
therefore a three-margin fleet diagnosis, not a causal retrofit or efficiency
claim.

## Intellectual Foundation

| Source family | Logic adapted | What is original here |
|:--|:--|:--|
| Cui et al. | Examine facility hierarchy rather than only a fleet mean | Japan-specific coverage, transition, and generator-component margins; no frontier or Cui data reused |
| Sasao | Repeated Japanese facility observations can support policy-relevant output analysis | Reconstructed twenty-year lineages and first-entry risk sets |
| Shino | Electricity per waste input is informative but not equivalent to thermal efficiency | National decomposition into raw installed kW, capacity factor, and waste loading |
| Firth; Heinze and Schemper | Bias reduction and finite estimates under sparse-event separation | Frozen five-parameter specification, whole-lineage bootstrap, event attacks, and current estimates |
| Harron et al. | Linkage error must be validated and propagated | Domain-specific blinded packet and lineage-sensitive model frames |

## Three Decisions Requested

1. Is the integrated three-margin contribution sufficiently meaningful as the
   paper's central claim, with RQ1 supporting rather than carrying novelty?
2. Is "first reported installed-capacity entry" the correct event language and
   is the five-parameter Firth specification appropriately restrained?
3. Who should independently review the 558-pair blinded linkage packet, and
   what archived sources should be used to adjudicate the highest-impact cases?

## Boundaries To Confirm

- No causal effect of scale, age, policy, or retrofit.
- No verified physical commissioning, replacement, or closure event.
- No claim of net electricity, useful heat, thermal efficiency, or recoverable
  potential.
- No claim that the paper invents Firth estimation or is Japan's first facility
  panel.
- No claim of completed linkage validation until an independent reviewer
  returns locked decisions.

## Supporting Material

- [Simulated linkage-review stress test](simulations/linkage-review-simulation-2026-07-15.md)
- [Comparator and method lineage](../positioning/professor-comparator-method-lineage.md)
- [Major-revision red-team review](major-revision-red-team-2026-07-14.md)
- [Generated scientific revision results](../../../output/scientific_revision_results.md)
