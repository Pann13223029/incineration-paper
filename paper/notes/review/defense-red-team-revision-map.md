# Defense Red-Team Review And Revision Map

Review baseline: current professor-facing manuscript and 17-page LaTeX reading
PDF, reviewed on 10 July 2026.

## Executive Verdict

The two-margin architecture survives review. The paper has a coherent and
potentially publishable descriptive contribution: it separates first observed
entry into installed electricity-generation capacity from performance among
identifiable operating generators.

The current version is not ready to be treated as methodologically settled.
Four issues should be corrected before the next professor review or simulated
defense:

1. The descriptive entry table uses event-year age and capacity even though the
   hazard uses prior-year values. Rebuild-like events can reset age in the event
   year, so the table currently makes the entry pattern look younger than the
   pre-event data show.
2. The entry risk set includes coded assets with zero or missing prior-year
   throughput. That is valid for an asset-transition question, but it is not the
   same as conversion among actively operating non-generators.
3. The duration sensitivity counts observed coded rows, not elapsed fiscal
   years, and is therefore mislabeled.
4. RQ2 has a four-model ladder but no single primary estimand. With year
   indicators, facility age mainly represents commissioning vintage or cohort
   differences, not a clean within-facility aging effect.

These findings argue for a focused empirical revision, not abandonment of the
paper. Exploratory checks conducted during this review are encouraging:

- the broad entry age/capacity pattern survives a correctly calculated elapsed-
  duration control;
- capacity remains strongly positive when the entry frame is restricted to
  facilities with positive prior-year throughput;
- generator age, capacity, and utilization remain stable after adding available
  technology/configuration controls;
- a plausible thermal-conversion proxy and the survey's reported generation-
  efficiency field produce nearly the same age, scale, and utilization pattern.

Overall assessment:

| Use | Assessment |
|:--|:--|
| Professor discussion now | Share only with this review packet and describe the manuscript as under empirical revision |
| Formal defense rehearsal | Suitable after the four mandatory corrections are implemented |
| Waste Management submission | Needs revision |
| Top-tier or high-profile submission | Not reached by prose polishing alone; would require a stronger integrated estimand, counterfactual, or external mechanism data |

## Review Scope And Evidence Pack

The review examined:

- [active manuscript](../../manuscript/paper.md)
- [LaTeX source](../../manuscript/paper.tex)
- [current reading PDF](../../share/waste-management-manuscript-latex.pdf)
- [sample definition](../../evidence/current/sample_definition.md)
- [entry and exit results](../../evidence/current/adoption_results.md)
- [generator regressions](../../evidence/current/regression_results.md)
- [robustness results](../../evidence/current/robustness_results.md)
- [data-quality sensitivity](../../evidence/current/data_quality_sensitivity.md)
- [identifier-gap audit](../../evidence/current/identifier_gap_audit.md)
- [shared panel construction](../../../code/analysis/panel_utils.py)
- [entry estimator implementation](../../../code/analysis/05a_power_adoption.py)
- [generator estimator implementation](../../../code/analysis/05_panel_regression.py)
- [supplement](../../supplement/supplement.md)

The rendered PDF was inspected page by page. No clipping, overlap, unreadable
figure, or broken table was found. Layout is not the current bottleneck.

External comparator intake identified three sources that materially affect the
next revision:

- Sasao (2018) already used an unbalanced Japan incinerator panel for FY2007-
  FY2015, with 635 plants, random-effects Tobit models, and technological,
  policy, and demographic predictors. This is a close predecessor that the
  manuscript must cite and distinguish:
  <https://doi.org/10.31025/2611-4135/2018.13650>.
- Shino (2019) directly discusses power generation per unit mass of waste as a
  measurable performance index and explains the measurement difficulty of
  gross thermal efficiency when lower calorific value is noisy. This is a
  better outcome-definition citation than relying only on broad WtE reviews:
  <https://doi.org/10.3985/jjsmcwm.30.113>.
- The official FY2024 MOE summary reports 415 power-generating plants out of
  991, or 41.9%. The processed panel has 417 positive-capacity rows out of
  1,014, or 41.1%. Both can be correct under different row/plant definitions,
  but the manuscript must not let the panel statistic look like the official
  national denominator:
  <https://www.env.go.jp/en/press/press_01569.html>.

The Cui et al. (2026) comparison remains useful, but it should be used as an
ambition benchmark rather than as evidence that the current paper has comparable
technical depth. Cui et al. combine national plant/line data, detailed technical
and operational variables, classification, optimization measures, and future
scenario analysis: <https://doi.org/10.1038/s41467-026-69897-w>.

## Panel Protocol

Mode: High-Output / Discovery with a formal red-team pass.

| Persona | Assumption trusted | Assumption distrusted | Evidence discounted |
|:--|:--|:--|:--|
| Waste Management editor | A narrow contribution can publish if the gap and target audience are explicit | A new national case is novel by itself | Long robustness lists without a clear main estimand |
| Applied econometrician | Estimands and risk sets should determine estimator choice | Stable signs alone establish robustness | Policy narratives unsupported by identification |
| Waste-to-energy engineer | MWh/t is useful when its energy boundary is explicit | Administrative fields equal engineering truth | Statistical significance without physical validation |
| Administrative-data auditor | Exact identifiers, lags, and denominators can be checked | Blank fields always mean true absence | Smooth narratives that hide coding discontinuities |
| Municipal planning reader | A diagnostic can be useful without being causal | Every non-generator should install generation | Results without a decision boundary |
| Hostile thesis examiner | Honest limitations can be defended | Repetition of caveats substitutes for a precise answer | Appeals to journal prestige or model complexity |

Coverage axes were contribution, risk-set validity, estimator validity, outcome
validity, policy relevance, and pivot feasibility.

## Normalized Claim Ledger

Scores use the panel protocol's 0-2 scale for evidence (E), support (S), novelty
(N), actionability (A), and objection severity (O).

| ID | Normalized claim | Status | E | S | N | A | O | Next test or action |
|:--|:--|:--|--:|--:|--:|--:|--:|:--|
| N1 | The two-margin architecture remains the strongest contribution | SURVIVES | 2 | 2 | 1 | 2 | 1 | Preserve it while clarifying state definitions |
| N2 | Event-year descriptive profiles cannot be used as evidence for prior-year selectivity | SURVIVES | 2 | 2 | 2 | 2 | 0 | Rebuild entry summaries from the exact-lag frame |
| N3 | Broad asset entry and active-facility conversion are different estimands | SURVIVES | 2 | 2 | 2 | 2 | 1 | Report both and select one as primary |
| N4 | The duration variable is currently mislabeled | SURVIVES | 2 | 2 | 1 | 2 | 0 | Recompute elapsed fiscal years and rerun |
| N5 | RQ2 needs one primary cross-facility estimand and estimator | SURVIVES | 2 | 2 | 1 | 2 | 1 | Make a year-adjusted, technology-adjusted model primary |
| N6 | Available technology and engineering fields can materially strengthen RQ2 without new data collection | SURVIVES | 2 | 2 | 2 | 2 | 0 | Add normalized technology controls and alternate outcomes |
| N7 | The novelty discussion is incomplete without Sasao (2018) and Shino (2019) | SURVIVES | 2 | 2 | 2 | 2 | 0 | Add and distinguish both sources |
| N8 | A joint multi-state or competing-risk model could make the integration more original | OPEN | 1 | 1 | 2 | 1 | 2 | Prototype only after mandatory corrections |
| N9 | Persistence supports observed hierarchy, not a bound on attainable improvement | SURVIVES | 2 | 2 | 1 | 2 | 0 | Remove potential-outcome wording from discussion |
| N10 | The PDF and figures are visually adequate for the next methods revision | SURVIVES | 2 | 2 | 0 | 1 | 0 | Do not spend the next round on design polish |

### Named Dissents

- The editor would stop after a clean two-margin descriptive paper and avoid a
  multi-state model unless it changes the conclusion.
- The econometrician would not accept the current entry headline until the
  active-risk and duration choices are made explicit.
- The engineer considers an engineering-outcome validation essential, not
  optional, because MWh/t is not full thermodynamic efficiency.
- The planning reader wants a descriptive decomposition of how many current
  assets fall into each decision segment, but accepts that intervention ranking
  is outside the current design.

## Findings In Priority Order

### F1 - High: The entry description mixes event-year and prior-year profiles

The manuscript says that 102 of 141 entry events occur at age 0-10 and that
annual event rates collapse after age 10. Those numbers group the broad risk set
by age on the event row. The hazard, however, correctly uses age and capacity
from the prior fiscal year.

This matters because 50 exact adjacent-year events are reset/rebuild-like. A
start-year or age reset can move a mature facility into the event-year 0-10
group. Event-year age is therefore partly an outcome of the same transition
being described.

In the exact-lag model frame, the prior-year profile is:

| Prior-year age | Risk rows | Events | Unadjusted annual rate |
|:--|--:|--:|--:|
| 0-10 | 1,322 | 26 | 1.97% |
| 10-20 | 3,265 | 6 | 0.18% |
| 20-30 | 4,037 | 29 | 0.72% |
| 30+ | 2,199 | 37 | 1.68% |

The adjusted AMEs can still be negative because the model controls for design
capacity and fiscal year. Counts, raw rates, and adjusted hazards answer
different questions. The current prose incorrectly presents the event-year
table and adjusted model as the same pattern.

Required correction:

1. Replace the main descriptive entry table with exact-lag prior-year age and
   capacity summaries.
2. Keep event-year age resets only in the pathway audit, where they are evidence
   about event type rather than pre-event selectivity.
3. Rewrite the result as an adjusted annual hazard difference, not as "most
   entrants were young."

### F2 - High: The RQ1 population is an asset frame, not necessarily an operating frame

The exact-lag model has 98 events. Forty have zero or missing prior-year
throughput. These include all 12 forward-dated/placeholder entries, 20 of 50
reset/rebuild-like entries, and 8 of 36 continuity entries.

Restricting the model to positive prior-year throughput gives 9,211 rows, 1,661
facilities, and 58 events:

| Predictor | Active-frame AME | p-value |
|:--|--:|--:|
| Age 10-20 vs 0-10 | -0.72 pp | 0.0005 |
| Age 20-30 vs 0-10 | -0.65 pp | 0.0354 |
| Age 30+ vs 0-10 | -0.38 pp | 0.1963 |
| Capacity per 100 t/day | +0.44 pp | <0.001 |

Capacity is robust. The oldest-age contrast is not. This does not invalidate the
broad asset-transition model, but it changes its meaning.

Recommended design:

- Primary frame: broad coded asset entry, if the paper is about commissioning,
  rebuild, and in-place pathways together.
- Required sensitivity: positive prior-year-throughput conversion frame, if the
  paper makes claims about operating non-generators upgrading in place.
- Headline wording: scale-selective entry is robust; the age gradient is
  estimand-dependent and should be described separately for broad asset entry
  and active-facility conversion.

An additional exploratory restriction to at least three consecutive coded
zero-capacity years retains 48 events. Capacity remains positive (+0.37 pp),
while the 20-30 and 30+ age contrasts become statistically indistinguishable
from zero. This is a pivot trigger, not yet a canonical result, because the
restriction conditions on continued non-entry.

### F3 - High: Duration is observation count, not elapsed time

`risk_duration_years` is currently created as group row count. Because official
facility codes are absent in FY2010-FY2012 and some facilities have other gaps,
this is not elapsed fiscal time. It differs from true elapsed duration in 4,055
of the 10,823 main model rows.

A review-only rerun using actual elapsed fiscal years preserved the broad sign
pattern. A parsimonious linear duration control produced age AMEs of -1.41,
-1.45, and -0.83 pp and a capacity AME of +0.45 pp. A categorical duration check
also preserved negative age and positive capacity associations.

Required correction:

1. Define elapsed duration as current fiscal year minus first at-risk fiscal
   year, plus one.
2. Rename row-count duration if it is retained for any separate diagnostic.
3. Make actual duration part of the main event-history logic or a clearly
   specified high-priority sensitivity.
4. Test a parsimonious functional form before adding many duration indicators,
   because the main frame has only 98 events.

### F4 - High: RQ2 does not yet have one primary estimand

The four-model ladder is transparent, but an examiner can still ask: "Which
model answers RQ2?" The current answer is unclear.

With fiscal-year indicators, facility age is close to an inverse commissioning-
year measure. The coefficient mainly compares older- and newer-vintage
facilities within common fiscal years. It is not a clean estimate of physical
aging inside the same plant. Facility fixed effects plus year effects would
leave little independent age movement and would answer a different question.

Recommended primary estimand:

> Among identifiable operating generators observed in the same fiscal year,
> how does gross electricity generated per tonne differ across age/vintage,
> scale, utilization, and technology profiles?

Recommended model hierarchy:

1. Primary: year-adjusted OLS with facility-clustered standard errors and a
   compact technology/configuration control set.
2. Robustness: correlated random-effects or within-between decomposition.
3. Supplement: pooled OLS and conventional random-effects ladder.
4. Interpretation: cross-facility conditional structure, not a causal aging
   effect.

### F5 - Medium-High: Available technology variables are omitted

The processed panel already contains furnace type, operating mode, facility
type, number of furnaces, reported generation efficiency, and power sold. Sasao
(2018) also shows that 24-hour operation and incineration configuration are
relevant Japan-specific comparators. Omitting all such variables leaves an easy
"age is only technology vintage" objection.

A review-only normalized technology-control model retained all 5,683 canonical
rows. Relative to the current year-indicator model:

| Term | Current coefficient | Technology-adjusted coefficient |
|:--|--:|--:|
| Facility age | -0.0348 | -0.0329 |
| Capacity per 100 t/day | +0.1051 | +0.1104 |
| Capacity utilization | +0.7760 | +0.7592 |
| R-squared | 0.3699 | 0.3831 |

This is strong evidence that the next revision can answer the omitted-
configuration objection without destabilizing the main pattern. These numbers
are exploratory until implemented in the canonical pipeline.

Required work:

- normalize whitespace and label variants in furnace, operation, and facility
  categories;
- document which variables are pre-existing configuration controls and which
  could be outcomes or mediators;
- add a compact control specification rather than every raw category;
- add a lagged-predictor sensitivity. A review-only exact-adjacent-year model
  with lagged predictors retained age -0.0361, capacity +0.1040, and utilization
  +0.6074.

### F6 - Medium-High: The outcome can be validated more directly

The manuscript correctly calls MWh/t a bounded gross electricity-recovery
intensity rather than full thermodynamic efficiency. That boundary should be
strengthened with an engineering validation.

Among 4,971 rows with plausible heating value, reported generation efficiency,
and raw MWh/t, the log thermal-conversion proxy and log reported generation
efficiency correlate at 0.864. Technology-adjusted regressions using either
outcome retain nearly identical age, scale, and utilization patterns.

Recommended revision:

- keep MWh/t as the primary transparent administrative outcome;
- cite Shino (2019) for its measurement rationale;
- add a plausible-value thermal-conversion proxy and reported-efficiency model
  as outcome-validity checks;
- state that reported efficiency may be constructed from related source fields
  and is therefore a convergent check, not fully independent validation;
- retain the caveat that gross output is not net export and excludes useful heat.

### F7 - Medium: The closest Japan comparator is missing

Sasao (2018) is closer than the manuscript's Taiwan DEA comparators on country,
data source, period, age, capacity, and panel structure. Failing to cite it makes
the novelty review look incomplete.

The distinction is still defensible:

| Sasao (2018) | Current paper after revision |
|:--|:--|
| 635 WtE plants, FY2007-FY2015 | National administrative panel through FY2024 |
| Heat/electricity output among WtE plants | First installed-capacity entry plus post-entry MWh/t |
| Policy, technology, and demographic correlates | State-conditioned transition and performance diagnostic |
| Random-effects Tobit | Discrete-time entry hazard plus generator performance model |

The originality claim should become:

> Prior Japan panel work explains energy outputs among WtE facilities. This
> paper adds the pre-generation state and links observed capacity entry,
> administrative exit, and post-entry performance in one state-conditioned
> fleet design.

### F8 - Medium: Persistence language occasionally exceeds the design

Rank correlation of 0.93 and a within/total ratio of 0.1499 establish observed
persistence. They do not show how far a facility could move after an unobserved
intervention.

Revise phrases such as:

- "how far operating generators can move"
- "not easily erased"
- "bounded responsiveness" when presented as an engineering limit

Prefer:

- "large observed year-to-year rank persistence"
- "limited observed convergence during the panel window"
- "consistent with durable facility structure, while not identifying
  attainable intervention effects"

### F9 - Medium: The opening denominator needs reconciliation

The official FY2024 result is 41.9% (415 of 991 plants). The parsed source panel
contains 41.1% positive-capacity rows (417 of 1,014 rows). The processed count
also includes zero-throughput and possibly administratively retained asset rows.

Use the official 41.9% in the national context sentence. Report 41.1% only when
describing the analytic panel and explain the denominator difference. This also
prevents readers from treating panel rows and official operating-plant counts as
interchangeable.

### F10 - Medium: The integration is conceptually clear but empirically thin

The 137-of-141 bridge is useful, but a hostile reviewer can still call the paper
"two regressions joined by a diagram." The next revision should add one stronger
empirical bridge before considering a more complex pivot.

Lowest-cost option:

- show post-entry MWh/t trajectories by event pathway and prior operating status;
- compare entrants with same-year incumbents using uncertainty intervals rather
  than one equal rounded mean;
- report whether entrants move through the generator rank distribution over the
  first three observed years.

Higher-cost option:

- estimate a multi-state framework with no capacity, installed capacity, and
  coded-panel exit as observed states, followed by a state-conditioned
  performance model.

The higher-cost option should be prototyped only after the risk-set corrections.

## Prioritized Revision Roadmap

### Gate 0 - Integrity Corrections

Do these before any narrative polishing:

1. Rebuild descriptive entry summaries with exact prior-year profiles.
2. Recompute actual elapsed risk duration.
3. Reconcile the official 41.9% and analytic-panel 41.1% denominators.
4. Replace causal-potential wording around persistence.
5. Add Sasao (2018) and Shino (2019) to the literature map.

Exit condition: every headline number uses the same time index, sample, and
denominator stated in its sentence.

### Gate 1 - RQ1 Re-Specification

1. Name the broad model `coded asset entry`, not generic retrofit or conversion.
2. Add a positive-prior-throughput `operating non-generator conversion`
   sensitivity.
3. Add true elapsed duration to the event-history design.
4. Add prior operating mode/configuration controls in one secondary model.
5. Add a sustained-capacity or sustained-output event check.
6. Report adjusted predicted probabilities or AMEs, raw exact-lag rates, and
   event counts separately.

Exit condition: a reader can explain why a large number of old-facility events
can coexist with a negative adjusted old-age AME.

### Gate 2 - RQ2 Estimand And Engineering Validation

1. Declare a primary year-adjusted cross-facility estimand.
2. Add normalized technology/configuration controls.
3. Add lagged-predictor sensitivity.
4. Add thermal-proxy and reported-efficiency outcome checks.
5. Move non-primary pooled/RE variants to the supplement.
6. Label age as an age/vintage profile where year indicators are present.

Exit condition: the answer to "Which model answers RQ2?" is one sentence.

### Gate 3 - Empirical Integration

1. Expand the post-entry bridge into a trajectory or rank-transition result.
2. Stratify by prior operating status and pathway category.
3. Decide whether separate entry and exit hazards are sufficient or whether a
   multi-state prototype changes the scientific conclusion.

Exit condition: the paper demonstrates, rather than only asserts, why both
margins belong in one article.

### Gate 4 - Narrative Rewrite

1. Reframe novelty against Sasao (2018), Shino (2019), and the high-profile
   China comparators.
2. Rewrite RQ1 around the chosen target population.
3. Compress repeated limitation loops after the methods are stronger.
4. Keep the professor-facing comparator map for supervision, then move it to the
   supplement for journal mode.
5. Rewrite the abstract last.

### Gate 5 - Verification And Defense Rehearsal

1. Rebuild all evidence and paper artifacts.
2. Extend claim verification to the new risk-set and technology-control claims.
3. Conduct a blind reader pass using only the PDF.
4. Rehearse the Tier 1 defense questions below without notes.

## Pivot Decision Tree

### Continue With The Current Two-Margin Paper If

- capacity remains positive in the broad and active entry frames;
- the age result is rewritten to match whichever risk set supports it;
- technology-adjusted and alternate-outcome generator results remain stable;
- an expanded post-entry bridge makes the integration visible.

This is the recommended path based on the current diagnostic checks.

### Pivot The Headline, But Keep The Design, If

- age becomes weak in the active and duration-adjusted entry models while
  capacity remains robust.

Use this headline instead:

> Entry is strongly scale-selective, while the apparent age gradient depends on
> whether the frame includes commissioning, rebuild, and inactive asset rows.

This would be a stronger paper than defending an unstable universal age claim.

### Pivot To A Multi-State Paper If

- entry, continued non-generation, and panel exit show clearly different
  covariate profiles;
- state-transition modeling improves interpretation without sparse-state
  instability;
- post-entry trajectories vary systematically by path.

Possible contribution:

> Municipal incineration modernization is a competing-path process, not a
> binary adoption decision followed by homogeneous performance.

### Do Not Claim A Top-Tier Pivot Unless

At least one of the following becomes available:

- verified capital histories that distinguish replacement, refurbishment, and
  new build;
- municipality finance, governance, procurement, and consolidation covariates;
- net electricity/heat export and emissions-control variables;
- a defensible counterfactual optimization or fleet-potential decomposition;
- an externally valid multi-country replication.

More words, more citations, or a more complex estimator will not substitute for
one of these contributions.

## Simulated Thesis Defense

### Opening Statement - 90 Seconds

> This study asks whether Japan's incineration modernization is one fleet-wide
> process or two distinct empirical problems. I use the Ministry of the
> Environment facility records from FY2005 to FY2024. First, I follow coded
> assets initially observed without installed generation capacity and model
> first positive capacity reporting. Second, I examine gross electricity
> generated per tonne among identifiable operating generators. The core finding
> is not simply that age and scale matter. It is that the target population and
> outcome change across the two margins: capacity entry is an asset-transition
> outcome, while generator performance is a conditional operating outcome. The
> study is observational. It does not identify a causal retrofit effect or claim
> that every non-generator should adopt. Its contribution is a reproducible,
> state-conditioned diagnostic that prevents non-generators, commissioning or
> rebuild events, administrative exits, and mature generators from being
> collapsed into one fleet average.

### Tier 1 - Questions That Can Change The Paper

#### 1. Sasao already used Japan's MOE panel, age, capacity, and operating mode. What is new?

Best answer:

> Sasao is the closest Japan predecessor and must be cited explicitly. That
> study analyzes heat and electricity outputs among WtE plants during FY2007-
> FY2015 using policy, technology, and demographic predictors. My distinct
> contribution is the state boundary: I include coded facilities before
> installed generation capacity, model first observed entry and administrative
> exit, and then link entrants to performance among generators through FY2024.
> The novelty is not rediscovering age or scale. It is separating pre-generation
> transition from post-entry performance in one fleet design.

Examiner follow-up:

> Then why are Sasao's technology and policy variables not in your model?

Best answer after revision:

> The revised generator model includes the technology/configuration fields
> available consistently in the MOE files. Municipality policy and demographic
> variables require an external merge and remain outside the present scope. I
> therefore interpret residual age/vintage associations descriptively rather
> than as isolated technology effects.

#### 2. Is this just two regressions stapled together?

Best answer:

> It would be if the samples were unrelated. The capacity-entry records are
> traced forward: most entrants soon report positive output and enter the
> generator frame. The revised paper also reports their early performance and
> rank trajectories. The models remain distinct because entry and conditional
> performance are different outcomes, but the same observed assets connect them.

Weak answer to avoid:

> They use the same dataset, so they belong together.

#### 3. Your paper says most entrants are young, but the prior-year data include many old entrants. Which is correct?

Best answer:

> The current event-year descriptive table is not the correct basis for a pre-
> event selectivity claim because rebuild events can reset age in the event year.
> The hazard uses prior-year age and capacity. The revised table reports those
> lagged profiles, separates raw counts from adjusted probabilities, and treats
> age resets only as pathway evidence. The defensible result is an adjusted
> hazard difference, not a claim that most event counts occur at young plants.

This answer should be delivered as a correction, not defended away.

#### 4. Are you modeling operating non-generators or every coded asset?

Best answer:

> The broad main frame models coded assets and therefore includes commissioning,
> rebuild, inactive, and in-place pathways. It is an asset-entry estimand. The
> revised paper reports a separate positive-prior-throughput frame for actively
> operating non-generators. Capacity is robust across both; the oldest age
> contrast is weaker in the active frame. I do not treat the two estimands as
> interchangeable.

#### 5. Where is duration dependence in your discrete-time hazard?

Best answer after revision:

> The revised model uses elapsed fiscal time from first at-risk observation. I
> report a parsimonious duration specification because there are 98 exact-lag
> events, and I retain a flexible duration sensitivity. Calendar-year indicators
> control common period conditions; elapsed duration controls time already at
> risk. They are not the same clock.

Current-version answer to avoid:

> Risk duration is already included.

That is not accurate until the row-count variable is corrected.

#### 6. Which generator model is your actual model?

Best answer after revision:

> The primary model is a fiscal-year-adjusted cross-facility regression with
> facility-clustered uncertainty and compact technology controls. It answers how
> operating generators differ within common fiscal years. Random-effects and
> within-between models are sensitivity analyses, not competing headline models.

#### 7. Is your age coefficient aging, vintage, or technology?

Best answer:

> With fiscal-year indicators, it is mainly an age/vintage profile across
> facilities observed in the same year. It can also absorb unmeasured technology,
> maintenance, and governance differences. It is not a causal estimate of one
> more year of physical aging. That is why the revised model adds observed
> technology controls and keeps the interpretation cross-facility.

#### 8. Why use MWh/t instead of real energy efficiency?

Best answer:

> MWh/t is directly observable and transparent across the national panel. Shino
> shows why per-mass generation can be measured more reliably than gross thermal
> efficiency when calorific-value measurement is noisy. I therefore use MWh/t as
> the primary administrative outcome, not as a full thermodynamic measure. The
> revised supplement validates the pattern against plausible thermal-conversion
> and reported-efficiency outcomes.

### Tier 2 - Identification And Data Questions

#### 9. Does the random-effects assumption hold?

> I do not rely on random effects for causal identification. The revised paper
> makes the year-adjusted cross-facility model primary and uses correlated
> within-between or RE variants as sensitivity descriptions. Unobserved facility
> traits may remain correlated with age, capacity, and technology.

#### 10. Why not facility fixed effects?

> Facility fixed effects answer a within-plant change question. The paper's main
> RQ2 estimand is cross-facility age/vintage and design structure. Age also moves
> mechanically with calendar time, so two-way fixed effects provide little clean
> age variation. I report within-facility diagnostics for persistence, but I do
> not present them as substitutes for the cross-facility estimand.

#### 11. Is 98 events enough for a model with year indicators?

> It is modest, which is why the main model is parsimonious and the saturated
> prefecture model is not primary. The revised analysis reports event-per-
> parameter diagnostics, convergence, flexible-link checks, and a parsimonious
> duration term. If a bias-reduced or penalized sensitivity changes the estimates,
> the headline will be revised rather than protected.

#### 12. Why treat blank installed capacity as no capacity?

> Blank capacity is an administrative absence indicator, not perfect engineering
> proof. The positive-output event sensitivity addresses this directly and
> preserves the broad scale pattern. The paper also reports that some positive-
> output rows lack positive capacity, so event definitions are not treated as
> interchangeable.

#### 13. What does the FY2010-FY2012 identifier gap do to your results?

> It prevents reliable facility continuity for those years. The main entry model
> therefore requires an exact one-fiscal-year lag and excludes non-adjacent
> transitions. The canonical generator panel excludes uncoded rows in those
> years. I do not call the early/later comparison a Fukushima causal design.

#### 14. Is panel exit really closure?

> No. It is final disappearance from the coded panel before FY2024. Closure,
> recoding, consolidation, and reporting loss cannot be separated. It is included
> to reveal informative administrative attrition, not to estimate physical plant
> retirement.

#### 15. Could utilization be simultaneous with MWh/t?

> Yes. Same-year utilization is an operating association, not an exogenous
> intervention. The revised paper adds lagged-predictor and alternate-outcome
> checks. The positive utilization pattern survives a one-year lag, but I still
> do not interpret its coefficient as the causal gain from raising load.

### Tier 3 - Meaning And Policy Questions

#### 16. Does a 0.93 rank correlation prove lock-in?

> No. It proves high observed adjacent-year rank persistence. It is consistent
> with durable facility structure, but it does not identify a mechanism or the
> effect of an unobserved intervention.

#### 17. Are you recommending generation at every non-generator?

> No. Small plants may have weak technical or economic justification for power
> generation. The paper recommends segment-specific screening before a detailed
> engineering and governance assessment, not universal installation.

#### 18. Does electricity recovery make incineration climate-positive?

> The study does not establish that. It does not estimate full lifecycle
> emissions, fossil carbon in waste, heat utilization, or the waste-hierarchy
> opportunity cost. It studies one performance dimension within the residual
> waste incineration system.

#### 19. What decision can a municipality make from a descriptive association?

> It can decide which diagnostic to commission next. A non-generating asset needs
> an entry, renewal, consolidation, or continued-non-generation assessment. An
> existing generator needs a performance and upgrade assessment relative to
> comparable plants. The regression does not select the intervention.

#### 20. What is the single biggest remaining limitation after revision?

> The administrative panel does not contain verified capital histories. It
> cannot cleanly distinguish replacement, major refurbishment, new construction,
> and reporting change for every event. That limits mechanism and causal claims.

## Defense Scoring Rubric

Score each rehearsal answer from 0 to 2:

- 0: overclaims, evades the risk-set issue, or gives a model name without an
  estimand.
- 1: technically correct but too long, defensive, or incomplete.
- 2: states the narrow claim, gives the relevant sample/model fact, names the
  limitation, and returns to the contribution.

Minimum readiness rule:

- Questions 1-8 must all score 2.
- Questions 9-15 may have at most two scores of 1.
- No answer may describe panel exit as closure, MWh/t as full efficiency, or an
  age coefficient as causal aging.

## Recommended Next Action

Start with Gate 0 and Gate 1. Do not rewrite the abstract or redesign the
figures first. The immediate empirical decision is whether RQ1's primary target
is broad coded-asset entry or conversion among actively operating
non-generators. The recommended answer is broad asset entry as primary, with an
active conversion sensitivity and headline wording that makes the distinction
visible.

Closure status: the paper direction survives, the universal age-entry wording
does not, and the next revision should prioritize target-population integrity
over additional polish.
