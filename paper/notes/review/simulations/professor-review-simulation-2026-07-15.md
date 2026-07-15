# Simulated Professor Review

Simulation date: 15 July 2026

## Status Warning

This document anticipates a demanding supervisor discussion. It is not actual
professor feedback and must not be represented as endorsement or peer review.

## Simulated Overall Decision

**Decision: strong foundation, proceed to real professor review after one
measurement-layer action.**

The paper now has a coherent intellectual structure and a defensible empirical
contribution. It is more than the observation that large or newer facilities
generate more electricity because it shows where that hierarchy appears:
coverage, first reported entry, installed generator size, and annual use do not
tell the same story. The principal unresolved issue is independent linkage
validation, not a need for additional unconstrained regression specifications.

## Simulated Scorecard

| Dimension | Score | Professor-style assessment |
|:--|--:|:--|
| Research-question clarity | 4.5/5 | The three questions are distinct, sequenced, and tied to explicit estimands. |
| Methodological discipline | 4.2/5 | The reduced Firth model, full bootstrap completion, and event attacks are appropriate for 35 events. |
| Empirical contribution | 4.1/5 | The integration is meaningful; RQ2 and RQ3 carry most novelty, while RQ1 establishes denominator discipline. |
| Comparator adaptation | 4.5/5 | The manuscript clearly identifies what is borrowed as research logic and what remains project-specific. |
| Interpretation discipline | 4.7/5 | Causal, physical-project, efficiency, and recoverable-potential boundaries are unusually explicit. |
| Identity validity | 3.2/5 | Computational auditing is strong, but the blinded packet still needs independent human review. |
| Journal readiness | 3.8/5 | Ready for substantive external feedback, not final submission until linkage validation and administrative items are resolved. |

## Simulated Discussion By Research Question

### RQ1: coverage

**Likely professor reaction:** The count-volume contrast is clear and useful,
but descriptive accounting alone is not sufficient novelty.

**Best response:** Agree. RQ1 is the measurement baseline. It prevents 41.1%
facility participation from being misread as only 41.1% waste coverage and
creates the denominator discipline needed for RQ2 and RQ3.

**Direction:** Keep RQ1 concise. Do not expand it with causal or potential-
recovery language.

### RQ2: first reported entry

**Likely professor reaction:** This is the most distinctive part, but why should
the event be trusted and why is scale not merely urban size or finance?

**Best response:** The event is deliberately defined as an administrative
transition, not a retrofit. The paper reconstructs lineages across code gaps,
uses exact adjacent-year histories, reports prior-operation, same-episode, and
identity-certain frames, and attacks every event. Scale remains associational
and may proxy for urban, fiscal, contractual, or policy conditions.

**Direction:** Make the linkage-review outcome the next scientific gate. New
municipal finance or population data would explain the scale association, but
should become a later mechanism extension rather than an improvised control set.

### RQ3: installed design and annual use

**Likely professor reaction:** It is unsurprising that newer facilities have
larger generators. What is learned beyond that intuition?

**Best response:** The result is not simply new versus old. Raw installed kW is
much lower in older reported start-year cohorts after observed controls, while
capacity factors are not uniformly lower. Therefore gross MWh/t should not be
read as one performance score: installed design, annual electrical use, and
waste loading are separate components.

**Direction:** Retain the raw-kW and capacity-factor contrast as the main RQ3
result. Keep the older sizing-adjusted gross-intensity regression secondary as
a specification diagnostic.

## Simulated Comparator Examination

### "Is this copied from Cui et al.?"

No. Cui et al. supplies the idea that a national fleet contains a meaningful
facility hierarchy. This paper does not reuse Cui data, code, thresholds,
optimization equations, frontier, or scenarios. It asks different estimands in
Japanese administrative data: denominator coverage, witnessed first entry, and
the distinction between installed kW and annual capacity factor.

### "How is this different from Sasao?"

Sasao establishes that repeated Japanese facility observations can support
policy analysis of heat and electricity. This paper adds a twenty-year identity
layer, explicit at-risk histories for first reported capacity, sparse-event
bias reduction, and event-level influence analysis.

### "How is this different from Shino?"

Shino examines electricity generation per unit waste in 22 Tokyo facilities
and emphasizes the information needed for thermal efficiency. This paper uses
national administrative coverage and deliberately avoids calling gross MWh/t
thermal efficiency. It decomposes the ratio into reported installed capacity,
capacity factor, and waste loading.

## Simulated Defense Questions And Answers

1. **Why Firth rather than ordinary logit?** With 35 events, conventional
   maximum likelihood is vulnerable to bias and separation. Firth reduces
   first-order bias and keeps finite estimates; it does not solve confounding.
2. **Why compare 300 with 100 t/day?** The capacity predictor is transformed as
   `log(1 + capacity/100)`. The contrast is an interpretable comparison within
   observed facility scales, not a causal intervention.
3. **Why only five parameters?** The event count cannot support the former
   11-parameter primary specification. Age, scale, centered calendar time, and
   elapsed risk answer the core question with lower degrees of freedom.
4. **What does the bootstrap add?** It resamples whole lineages, preserving
   repeated-observation dependence. All 1,999 requested replications must
   converge; none is silently discarded.
5. **Could one event drive the result?** Every event was reclassified once and
   every event lineage deleted once. The scale odds ratio remains 6.12-7.30.
6. **Is reported start year generator age?** No. It is an administrative cohort
   marker and may not date the boiler, turbine, or control system.
7. **Does 80.1% coverage mean the remaining waste should be moved?** No. It is
   an accounting share, not a feasibility, cost, equity, or lifecycle result.
8. **What would falsify the paper's main interpretation?** Independent linkage
   review that materially changes event lineages, or raw-component results that
   show the cohort pattern lies uniformly in annual use rather than sizing.

## Simulated Meeting Flow

| Minutes | Topic | Desired outcome |
|--:|:--|:--|
| 0-3 | One-minute paper explanation and three-margin diagram | Confirm that the professor sees one integrated argument |
| 3-10 | RQs and estimands | Confirm that RQ1 supports, RQ2 distinguishes, and RQ3 interprets |
| 10-20 | Identity and sparse-entry method | Obtain judgment on event language and validation standard |
| 20-28 | Main results and event attacks | Test whether the scale result is meaningful but properly bounded |
| 28-35 | Cui, Sasao, and Shino adaptation | Confirm originality and non-plagiaristic method lineage |
| 35-42 | Limitations and simulated linkage stress test | Agree that human linkage review is the next P0 action |
| 42-45 | Three requested decisions | Leave with explicit direction rather than general comments |

## Simulated Final Professor Comment

> The paper now has a credible foundation and a clear reason to exist. Its
> strongest contribution is not that larger facilities are associated with
> generation, but that it reconstructs when that state first appears and shows
> why participation, waste coverage, installed sizing, and annual use must be
> interpreted separately. Do not add more models until the linkage packet has
> been independently reviewed. After that, decide whether the next extension is
> mechanism data or journal submission, not both at once.

## Recommended Real-Meeting Ask

Use the [professor meeting brief](../professor-meeting-brief-2026-07-15.md) and
request answers to exactly three questions: contribution framing, event/method
acceptability, and assignment of an independent linkage reviewer.
