# Abstract And Introduction Checklist

Purpose: make the professor-facing draft understandable to a technically
informed reader who does not already know the dataset, Firth regression, or
waste-to-energy engineering terms.

## Abstract Arc

Write the abstract in six moves:

1. **Puzzle:** Japan has many incinerators, but a facility count alone does not
   show how much waste passes through generating facilities.
2. **Data:** identify a national FY2005-FY2024 administrative panel whose
   longitudinal site identities were reconstructed and audited.
3. **Design:** distinguish fleet coverage, first reported installed-capacity
   entry, and generator design/operation components.
4. **Entry answer:** larger waste-processing facilities have substantially
   higher entry odds; the age terms are not jointly supported.
5. **Engineering answer:** reported start-year differences are concentrated in
   installed generator sizing; in the separate 5,806-row, heating-value-
   controlled specification diagnostic, age, processing capacity, and
   utilization are no longer independently supported after sizing is included.
6. **Meaning:** infrastructure transition cannot be judged from facility counts
   or one gross-output ratio alone.

## Abstract Number Budget

Use no more than four numerical anchors:

- 41.1% facility participation versus 80.1% throughput coverage
- 35 exact-frame events, if sparse inference must be motivated numerically
- odds ratio 6.13 for 300 versus 100 t/day
- 6,511 engineering-valid generator-year observations, if space permits

The 70.5% design-capacity share, prior-operation frame, p-values, pathway counts,
and model diagnostics can remain in the main text.

## Abstract Language Checks

Use:

- `first reported installed electrical-generation capacity`
- `Firth bias-reduced discrete-time model`
- `waste-processing design capacity`
- `generator design intensity`
- `electrical capacity factor`
- `descriptive association`

Avoid:

- implying that an administrative entry is necessarily a retrofit
- calling gross MWh/t thermodynamic efficiency
- making age the entry headline
- saying the model identifies a policy effect or optimal investment
- presenting the 41.1% facility share as the untreated waste-volume share

## Introduction Sequence

### Paragraph 1: Count-volume puzzle

- Give the 41.1%, 80.1%, and 70.5% FY2024 contrast.
- Explain in plain language that large facilities process disproportionate
  volumes.
- End with why a single facility-count statistic is insufficient.

### Paragraph 2: Analytical problem

- Distinguish participation, first entry, installed sizing, and annual use.
- Explain that gross electricity per tonne combines these dimensions.
- State why collapsing them can misdiagnose modernization.

### Paragraph 3: Prior work and comparator lineage

- Name the closest Japan and engineering comparators.
- State the principle adapted from each.
- State how the current sample, estimands, and contribution differ.
- Avoid claiming novelty merely because the panel reaches FY2024.

### Paragraph 4: Data and identity

- Explain why source facility codes cannot simply be followed through time.
- State that 23,593 records form 1,690 audited stable administrative lineages and 1,767
  asset episodes.
- Keep the algorithm detail for methods and supplement.

### Paragraph 5: Research questions

State three distinct questions:

1. How do facility participation, throughput coverage, and design-capacity
   coverage differ?
2. Which prior site characteristics are associated with first reported
   installed-capacity entry?
3. How do generator sizing and annual electrical capacity factor structure gross
   generation among operating generators?

### Paragraph 6: Answers and contribution

- Lead with count-volume divergence.
- State robust scale selectivity and restrained age inference.
- State the generator-sizing result.
- End with the integrated measurement contribution and noncausal boundary.

## Jargon Test

Define each term at first use:

| Term | Plain-language explanation |
|:--|:--|
| Stable administrative lineage | Records judged to represent the same administrative facility history through time |
| Asset episode | A period before or after a material reported facility reset |
| Firth regression | A bias-reduced logistic method used because first entries are rare |
| Design intensity | Installed generator kW relative to tonnes/day of waste-processing capacity |
| Capacity factor | Actual annual generation relative to a full year at installed nameplate power |
| Gross MWh/t | Electricity reported before plant use, divided by waste processed |

## Professor-Comprehension Test

After the first two pages, a reader should be able to answer:

1. Why is 41.1% not the whole national story?
2. What exactly counts as an entry event?
3. Why is Firth inference used?
4. Why is age not the main entry result?
5. Why does installed generator sizing change the old gross-output conclusion?
6. Which parts were adapted from comparator papers, and what is original here?

If any answer is unclear, revise the opening before adding background.
