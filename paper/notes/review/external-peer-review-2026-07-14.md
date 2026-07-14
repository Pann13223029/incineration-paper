# Simulated External Peer Review

**Manuscript:** *Coverage, Entry, and Engineering Components of Electricity
Recovery in Japan's Municipal Waste-Incineration Fleet, FY2005-FY2024*

**Review date:** 14 July 2026

**Target considered:** *Waste Management*, full-length article

**Recommendation:** Major revision before journal submission; suitable for
professor review in its current form.

## Scope Of This Review

This is an independent journal-style review of the scientific argument, not a
repetition of the repository's internal compliance rubric. It evaluates the
research question, contribution, construct validity, longitudinal linkage,
statistical specification, engineering interpretation, figures, and
evidence-to-claim alignment. It does not certify source-file redistribution
rights or replace subject-matter review by a waste-incineration engineer.

## Summary Assessment

The manuscript uses an unusually transparent national administrative panel and
shows strong discipline about what the data cannot establish. Its clearest
contributions are: (1) separating facility participation from throughput and
design-capacity coverage; (2) reconstructing administrative lineages before
defining transitions; and (3) separating installed generator sizing from annual
capacity use and waste loading. The FY2024 contrast between 41.1% facility
participation and 80.1% throughput coverage is important and policy relevant.

The present manuscript is not yet ready for journal submission. The central
problem is not numerical accuracy. It is that the paper asks three large
questions, then adds a small pathway comparison, without making one scientific
claim clearly primary. The longitudinal identity layer has strong engineering
tests but little independent ground-truth validation. The entry model asks 35
events to support 11 coefficients. The engineering section correctly identifies
an accounting identity, but several regressions use ratios that share
numerators or denominators, so part of the apparent explanatory gain is
mechanical. The pathway contrast is too sparse and selected for a main-text
figure without uncertainty.

These concerns are addressable. The national time span, data engineering, and
careful noncausal interpretation justify revision rather than rejection.

## Major Comments

### 1. Independent validation of longitudinal identity is insufficient

**Severity: High**

Every transition and repeated-observation result depends on the reconstructed
stable administrative lineages. The resolver has excellent implementation
guardrails: exact-duplicate collapse, contradiction vetoes, one-to-one
assignment, golden same/separate cases, row-permutation invariance, synthetic
insertion invariance, exposed low-margin links, and whole-lineage sensitivity.
Those checks establish deterministic behavior and catch known failures. They do
not estimate linkage accuracy against an external truth set.

Only three must-link and three must-separate examples are described. Internal
assignment margins can identify ambiguity under the algorithm but cannot reveal
confidently wrong links. The identity-certain sensitivity therefore addresses
flagged uncertainty, not all linkage error.

**Required revision:**

1. Create a blinded or independently checked, stratified manual validation
   sample covering exact-name links, code-supported non-exact links, fuzzy
   links, gaps, FY2009-FY2013, FY2019-FY2020, and inferred episode resets.
2. Report agreement and error categories with uncertainty, not only selected
   examples.
3. Add a transition-level sensitivity that removes the least verifiable link
   classes, not only the 14 internally flagged lineages.
4. State how many of the 35 modeled events depend on recode bridges, fuzzy
   links, gaps, or episode-boundary decisions.

Without this work, the manuscript should describe the linkage as carefully
audited but not independently validated.

### 2. The manuscript needs one primary contribution

**Severity: High**

The count-volume result, sparse entry analysis, engineering decomposition, and
pathway comparison are related, but they currently read as four analyses held
together by a common dataset. RQ3 alone asks about an identity, two component
models, a cohort comparison, a specification diagnostic, and pathway outcomes.
This breadth makes the paper look comprehensive while weakening the editorial
answer to "what is the one new result?"

The strongest unifying claim is a measurement claim: fleet diagnosis changes
when denominators, administrative states, and engineering components are
defined before interpreting performance. The national Japan panel then
demonstrates that claim. The entry model can remain as the transition component,
but the pathway comparison should not carry equal weight.

**Required revision:**

1. State one primary contribution at the end of the Introduction in one or two
   sentences.
2. Make RQ1-RQ3 subordinate tests of that contribution rather than three
   co-equal papers.
3. Shorten RQ3 and move the exploratory pathway question out of the formal RQ.
4. Remove the pathway comparison from the abstract and conclusion unless its
   inferential support is strengthened.

### 3. The sparse-event model is too ambitious for 35 events

**Severity: High**

Firth bias reduction is appropriate for separation and small-sample bias, and
lineage bootstrapping is preferable to treating facility-years as independent.
Neither method creates information. The broad model has approximately 3.2
events per coefficient, with age bands, transformed capacity, calendar era,
and elapsed-risk-duration bands. Age, calendar time, reported start year, and
elapsed observation duration are structurally related. The manuscript does not
show enough stability or influence analysis to establish that the large scale
coefficient is not being driven by a few events or specification choices.

The 499 bootstrap replications are adequate for a diagnostic but coarse for
tail intervals and especially for a joint result reported as p=0.0508. That
near-threshold result should not be numerically emphasized.

**Required revision:**

1. Define a lower-degree-of-freedom primary model and treat the current model as
   an adjusted sensitivity.
2. Report event counts by calendar era, age band, pathway, and scale category
   for the exact 35-event model sample.
3. Add leave-one-event or leave-one-lineage influence checks for the capacity
   contrast.
4. Evaluate collinearity and coefficient stability across defensible duration
   and calendar specifications.
5. Increase bootstrap replications for final inference, preferably to at least
   1,999, and report Monte Carlo stability for key interval endpoints.
6. Avoid framing the same-episode p=0.0508 as a threshold result; its value is
   evidence of instability.

### 4. Algebraic coupling needs to be separated from empirical explanation

**Severity: High**

The exact identity

`gross MWh/t = 0.024 x design intensity x capacity factor / utilization`

is correct and useful. It also means the variables are mechanically connected.
Gross MWh/t and capacity factor share gross generation; design intensity and
utilization share processing capacity; the legacy diagnostic regresses a ratio
on quantities that also enter its algebraic decomposition. A large increase in
R-squared after adding design intensity is therefore not solely evidence that a
previous scientific explanation omitted a latent design variable. Part of the
gain is expected from the identity.

The current text calls this a specification diagnostic and avoids causal
mediation language, which is good, but phrases such as "principally a sizing
hierarchy" can still be read as an empirical attribution stronger than the
design supports.

**Required revision:**

1. Make raw-variable models primary where possible. For example, model log
   installed kW as a function of log processing capacity and reported cohort,
   then translate the result into design-intensity terms.
2. Keep the direct log gross-output model prominent and explicitly separate it
   from the accounting identity.
3. Explain how coefficients transform between `log(K/C)` and `log(K)` models.
4. Quantify how much of the legacy-model R-squared change is expected
   mechanically, or remove the R-squared contrast from the headline argument.
5. Replace attribution language with "the observed hierarchy is expressed
   mainly through reported generator sizing" unless stronger identification is
   added.

### 5. Entry is a reporting transition, and its event mixture needs more exposure

**Severity: Medium-High**

The paper carefully says that entry is first reported installed capacity, not a
verified retrofit or commissioning event. That limitation materially affects
why the result matters. The 55 descriptive events include 35 continuity-lineage,
11 rebuild/replacement-like, and nine forward-dated/placeholder events. The
reader is not shown the corresponding composition of the 35 modeled events.
Scale-associated entry could partly represent replacement, reporting, or
administrative timing patterns concentrated among large facilities.

The exclusion of 467 lineages already generating in their first observed year
also creates a selected risk population: the model describes later observed
entry among initially observed non-generators, not diffusion across the full
fleet.

**Required revision:**

1. Cross-tabulate modeled events by pathway and calendar era.
2. Show the capacity contrast after excluding forward-dated/placeholder events.
3. State the selected risk-population estimand beside every main entry result.
4. Explain more directly how left truncation limits generalization to the full
   installed fleet.

### 6. The pathway comparison is not strong enough for a main-text result

**Severity: Medium-High**

Figure 4 compares 27 continuity-lineage and 11 rebuild/replacement-like
observations after conditioning on positive output, engineering validity, and
follow-up. It gives means without uncertainty. The groups are selected by
administrative patterns, labels are uncertain, and the smaller group is too
sparse for a visually strong ranking claim. The text acknowledges all of these
limitations, but the figure still encourages a stronger comparison than the
evidence warrants.

**Required revision:** move Figure 4 and Section 4.4 to the supplement. If the
comparison remains in the main text, add individual observations or interval
estimates, report missing follow-up by pathway, and use explicitly exploratory
language in the title and caption.

### 7. The novelty argument is framed as adaptation rather than a demonstrated gap

**Severity: Medium**

Table 1 is transparent for a professor, but a journal reviewer may see it as a
description of how the manuscript was assembled rather than a literature-based
argument. The closest Japan studies already show that processing capacity,
continuous operation, policy, waste properties, and age relate to energy
outputs. Sasao (2018) analyzes Japanese incinerator heat and electricity under
policy and technology factors. Shino (2019) analyzes power generation per unit
waste and thermal conversion in 22 Tokyo plants, including replacement cases.
The manuscript needs to state precisely what those studies could not answer.

Cui et al. (2026) uses much richer engineering and operational information to
construct corrected energy-efficiency tiers and optimization scenarios. It is a
useful contrast, but it should not be presented as the methodological template
for this substantially narrower administrative design.

**Required revision:** replace or shorten the comparator-adaptation table with
a focused gap synthesis showing: prior unit of analysis, period, outcome,
engineering fields, longitudinal identity treatment, and the unanswered gap.
Add record-linkage validation and cluster-bootstrap methodological references.

### 8. Cohort comparisons remain vulnerable to survivor and composition effects

**Severity: Medium**

Reported start year is correctly described as an administrative design-vintage
marker. Older observed cohorts are survivors into FY2005-FY2024, whereas newer
cohorts enter later and have shorter observed histories. Fiscal-year indicators
reduce period confounding but do not make cohort membership exogenous or
separate design progress from selection, replacement, municipality, and waste
composition.

The conclusion should therefore avoid language that resembles technological
progress or aging. Present adjusted cohort estimates with intervals and add
overlap diagnostics showing which cohorts are represented in each fiscal year.

## Figure Review

- **Figure 1:** Strong. Denominators, time range, line styles, endpoint labels,
  and zero-to-100 scale are clear. This is the paper's best main figure.
- **Figure 2:** Strong presentation of sparse estimates. Add the selected risk
  population to the caption and retain the event counts.
- **Figure 3:** Clear but shows medians without dispersion or uncertainty. Use
  distributions, interquartile ranges, or adjusted estimates with confidence
  intervals. The current points can overstate cohort separation.
- **Figure 4:** Visually clear but inferentially too strong for n=27 and n=11
  selected observations without uncertainty. Move to the supplement.

## Minor Comments

1. The abstract is accurate but excessively dense. Remove the pathway result
   and at least one set of event counts or p-values.
2. RQ3 should be split or shortened; it currently contains too many distinct
   tasks for one research question.
3. Use "conditional association" rather than "independent association" where
   residual confounding remains substantial.
4. Report very small p-values as thresholds such as `<0.001`, not `0.0000`, in
   all reader-facing tables.
5. Explain why electrical capacity factors above 1.0 are administratively
   plausible and why the primary upper bound is 1.20.
6. Distinguish model fit from scientific explanation when reporting R-squared.
7. Add a compact missing-data table by year or cohort for the fields used in
   each model, not only aggregate exclusions.
8. Expand the method references for deterministic record linkage, assignment,
   clustered resampling, and sparse-event influence diagnostics.
9. The long title is accurate, but a shorter title centered on measurement
   architecture may improve discoverability.
10. Correct the repository availability statement separately from scientific
    revision; it is an administrative inconsistency, not evidence against the
    results.

## Independent Spot Checks

The following high-impact quantities were recomputed directly from
`data/processed/incineration_panel_identified.csv`:

| Check | Result |
|:--|:--|
| FY2024 retained records | 1,014 |
| Positive installed capacity | 417 records; 41.124% |
| Positive-throughput, positive-output facilities | 410 |
| Total recorded throughput | 30.8407 million tonnes |
| Throughput at positive-output facilities | 24.7030 million tonnes; 80.099% |
| Design-capacity share at installed-capacity facilities | 70.503% |
| Engineering identity | Maximum relative numerical residual `5.23e-16` across 6,660 positive generator rows |

The reported FY2024 headline values and accounting identity are numerically
consistent. Repository claim verification and evidence synchronization also
pass. No numerical drift was identified in this review.

Not independently verified here: publisher-side workbook revision history,
physical truth of reconstructed lineages, source-file redistribution rights,
and every external bibliographic claim.

## Strengths That Should Be Preserved

1. Explicit separation of facility, throughput, and design-capacity
   denominators.
2. Clear distinction between administrative lineages and physical facilities.
3. Appropriate use of Firth bias reduction rather than ordinary logit as the
   primary sparse-event estimator.
4. Whole-lineage resampling and transparent sensitivity frames.
5. Exact engineering identity with correct units.
6. Strong noncausal discipline and unusually candid limitations.
7. Reproducible source-to-claim pipeline and machine-readable evidence.
8. Clear distinction between gross generation, net export, useful heat, and
   thermodynamic or lifecycle efficiency.

## Recommended Revision Order

1. **Validate identity externally.** Build the stratified manual truth sample
   and linkage-class sensitivities.
2. **Choose the primary contribution.** Center measurement architecture and
   make the three analyses serve one claim.
3. **Stabilize the entry model.** Reduce degrees of freedom, expose event
   composition, add influence checks, and increase bootstrap replications.
4. **Recast the engineering regressions.** Lead with raw-variable models and
   distinguish algebraic explanation from empirical association.
5. **Demote the pathway comparison.** Move it and Figure 4 to the supplement
   unless uncertainty and follow-up selection are addressed.
6. **Rebuild the literature gap.** Contrast directly with the closest Japan
   and high-profile studies rather than emphasizing inspiration.
7. **Revise Figures 2-3 and compress the abstract.** Show uncertainty and make
   the selected samples visible.
8. **Resolve repository governance.** Align public/private, availability,
   licensing, and raw-data redistribution statements before submission.

## Editorial Decision Rationale

For a professor, the manuscript is ready because it exposes its assumptions,
methods, and limitations well enough to support substantive direction-setting.
For *Waste Management*, a full-length article must present original research of
clear significance within 6,500 words and eight combined figures/tables. The
manuscript meets the formal size limits and journal scope, but formal compliance
does not resolve the scientific focus and construct-validity concerns above.

I recommend major revision rather than rejection because the national panel,
count-volume divergence, identity-aware design, and component separation are
valuable. A revision that directly validates linkage, simplifies sparse
inference, removes mechanically overstated interpretation, and focuses the
paper could become a defensible journal submission.

## External Sources Consulted

- *Waste Management*, Guide for Authors:
  <https://www.sciencedirect.com/journal/waste-management/publish/guide-for-authors>
- Cui et al. (2026), *Nature Communications*:
  <https://www.nature.com/articles/s41467-026-69897-w>
- Liu et al. (2025), *Nature Energy*:
  <https://www.nature.com/articles/s41560-024-01683-8>
- Sasao (2018), *Detritus*:
  <https://digital.detritusjournal.com/articles/how-does-municipal-solid-waste-policy-affect-heat-and-electricity-produced-by-incinerators/109>
- Shino (2019), J-STAGE:
  <https://www.jstage.jst.go.jp/article/jjsmcwm/30/0/30_113/_article/-char/en>
