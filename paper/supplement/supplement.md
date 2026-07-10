# Supplementary Material

## S1. Purpose Of The Supplement

This supplement protects the main paper from technical overload. The main text
keeps the argument readable; the supplement carries the denser sample,
classification, robustness, and estimator-comparison detail that a skeptical
reviewer may still want to inspect.

### S1.1 Abbreviation and term guide

The manuscript uses a small number of repeated abbreviations:

| Term | Meaning in this paper |
|:--|:--|
| FY | Fiscal year |
| RQ | Research question |
| WtE | Waste-to-energy or waste incineration with energy recovery |
| OLS | Ordinary least squares |
| FE | Fixed effects, usually fiscal-year fixed effects in the main models |
| RE | Random effects, used descriptively to represent persistent facility-level differences |
| AME | Average marginal effect from the adoption logit, reported in percentage points |
| pp | Percentage points |
| EF | Grid emissions factor |
| MWh/t | Megawatt-hours of electricity recovered per tonne of waste processed |
| MJ/kg | Megajoules per kilogram |

Terms such as `observed transition`, `canonical generator frame`, and
`structured conditional association` are intentional scope markers. They signal
that the paper is describing administrative-panel patterns rather than claiming
to identify a unique physical retrofit mechanism or a causal policy effect.

## S2. Analytical Frames And Sample Construction

The analysis begins from a Ministry of the Environment facility panel covering
FY2005-FY2024. The full panel contains 23,599 facility-year rows. Within that,
the coded full-fleet frame contains 19,827 observations across 2,948
facilities.

### S2.0 Reviewer-facing scope map

This paper uses the administrative panel as a diagnostic fleet-decomposition
dataset. The design is intentionally conservative about what the data can and
cannot identify.

| Potential reviewer concern | Defensive response in this paper |
|:--|:--|
| Observed adoption may not equal a directly observed physical retrofit. | The paper uses `observed transition into generation` language and treats the pathway audit as descriptive support, not mechanism proof. |
| Left-censored generators can distort adoption estimates. | Facilities already generating in their first observed year are excluded from the adoption risk set. |
| Official-code gaps can turn prior-year lags into previous-observed-row lags. | The main adoption model now keeps only exact one-fiscal-year lags; the broader previous-observed-coded-row model is reported only as sensitivity evidence. |
| Official facility codes sometimes repeat within a fiscal year. | The supplement reports a composite-ID sensitivity; headline adoption and electricity-recovery signs remain stable. |
| Heating value is noisy in administrative files. | Heating value is treated as a control, not an engineering outcome; plausible-value restrictions leave the core coefficients stable. |
| The generator frame excludes uncoded operating rows. | The main text defines the electricity-recovery sample as the canonical identifiable generator frame, and this supplement compares coded and uncoded operating-generator rows. |
| Age effects could be confounded with durable facility characteristics. | The paper interprets coefficients as structured conditional associations and uses the variance structure to justify descriptive cross-facility comparison, not causal vintage isolation. |
| Adoption events are temporally clustered. | The paper reports the clustering and uses year fixed effects; it does not interpret the timing as a uniquely identified policy shock or reporting change. |
| Adoption risk may vary with time already spent at risk. | A duration-augmented exact-year hazard preserves the expected age and capacity sign pattern. |

The result is a narrower but more defensible claim: the linked samples show
selective observed entry into generation and structured conditional performance
among identifiable generators.

### S2.0a Bridge-map placement decision

The current review-facing manuscript keeps two explanatory bridge maps in the
main text: the research-question-to-model bridge and the linked analytical
framework. They are retained there because the current priority is making the
methodological foundation easy to inspect before a human review meeting.

For a journal-compressed version, these bridge maps are optional main-text
material. The preferred journal-mode action is:

- keep Table 1, the linked analytical framework, in the main text because it
  anchors the two-margin contribution;
- move the research-question-to-model bridge to the supplement if the editor or
  target format pressures the figure/table count or if the methods section feels
  too table-heavy;
- do not remove the bridge logic entirely, because it is the clearest defense
  against the critique that the paper is two unrelated analyses placed side by
  side.

### S2.1 Adoption frame

- Left-censored facilities already generating in their first observed year: 913
- Adoption risk-set observations: 13,770
- Adoption risk-set facilities: 2,035
- Observed first-adoption events in the panel window: 141
- Exact-year lagged adoption-model observations: 10,823
- Exact-year lagged adoption-model facilities: 1,911
- First-adoption events retained in the exact-year lagged model: 98
- Broader previous-observed-coded-row model frame before exact-year restriction: 11,717 observations, 1,915 facilities, 140 events
- Non-exact lag rows excluded from the main adoption model: 894 rows, including 42 events

Interpretation: the main adoption model is a model of observed transition within
the coded at-risk frame, not an unrestricted fleet-wide modernization model.

### S2.2 Generator frame

- Canonical regression observations: 5,683
- Canonical regression facilities: 1,016
- Fiscal years covered: FY2005-FY2024
- Within/total variance ratio of pooled log electricity-recovery intensity: 0.1499
- Early coded-window ratio (FY2005-FY2009): 0.1795
- Later coded-window ratio (FY2013-FY2024): 0.0956

Interpretation: the intensive-margin models are designed to describe structured
conditional performance within the generating segment, not to identify a strict
causal policy effect.

### S2.3 Generator-frame inclusion audit

The operating-generator sample contains 6,660 rows with positive throughput and
positive electricity output. The canonical regression frame requires official
facility codes and complete model covariates, leaving 5,683 rows.

| Group | Rows | Facility proxy | FY range | Mean capacity (t/day) | Mean bounded electricity recovery (MWh/t) | Mean age |
|:--|--:|--:|:--|--:|--:|--:|
| Official facility code present | 5,753 | 1,018 | FY2005-FY2024 | 332.1 | 0.330 | 15.0 |
| Official facility code missing | 907 | 316 | FY2008-FY2012 | 359.0 | 0.296 | 13.4 |

The missing-code rows are concentrated in FY2010-FY2012, when all operating
generator rows in the source file lack official facility codes. This is why the
paper calls the regression sample the canonical identifiable generator frame
rather than a census of all generation activity. The full year-by-year code
availability table is generated in
`paper/evidence/current/data_quality_sensitivity.md`.

## S3. Adoption Risk-Set Rules

The adoption frame includes facilities first observed without power generation.
Facilities already generating in their first observed year are excluded as
left-censored for the adoption question. The main lagged hazard specification
then requires exact one-fiscal-year prior age band and prior-year design
capacity, which removes the first observed at-risk year for each facility, a
small number of additional rows with missing lagged predictors, and non-exact
lag rows created by duplicate same-year codes or official-code gaps.

The adoption estimand is therefore not "which facilities ever modernized" in a
complete historical sense. It is the probability that a coded facility first
records power generation in the next observed fiscal year, conditional on still
being observed at risk in the panel and conditional on exact one-fiscal-year
prior age and capacity. This distinction protects the paper from overclaiming about
unobserved pre-panel investments or physical retrofit histories that the
administrative file does not directly record.

Observed first-adoption events are temporally clustered: 109 of 141 events occur
in FY2013-FY2019. The main hazard includes year fixed effects, and the paper
does not interpret the timing pattern as a separately identified policy shock or
reporting change.

## S4. Pathway-Audit Rule Set

The pathway audit is designed to bound mechanism language, not to prove a unique
modernization pathway.

### S4.1 Categories

- `Reset / rebuild-like transition`
- `In-place upgrade / continuity transition`
- `Forward-dated / placeholder entry`
- `Timing-ambiguous / non-adjacent coded row`
- `Unresolved / insufficient continuity`

### S4.2 Rule logic

- `Reset / rebuild-like` requires an exact adjacent-year event plus an observed
  reset in `year_started` or a mature-to-new age reset before adoption.
- `In-place upgrade / continuity` requires an exact adjacent-year event, no such
  reset on the observed event row, and continuity of the facility record into the
  adoption event.
- `Forward-dated / placeholder` captures cases where the event row appears to be
  forward-dated or placeholder-like and should not be forced into a stronger
  mechanism claim.
- `Timing-ambiguous / non-adjacent coded row` captures events whose prior coded
  row is not the immediately preceding fiscal year.
- `Unresolved` is reserved for events without a usable continuity row.

### S4.3 Category counts

- Reset / rebuild-like: 50
- In-place upgrade / continuity: 36
- Forward-dated / placeholder: 12
- Timing-ambiguous / non-adjacent coded row: 42
- Unresolved: 1

Interpretation: the adjacent-year pathway distribution is supportive descriptive
evidence for selective modernization, but timing-ambiguous events are deliberately
weakened and the audit does not uniquely identify replacement, major
refurbishment, or new build as the dominant mechanism.

## S5. Robustness And Estimator Notes

### S5.0 Regression reader guide

This subsection expands the regression notation used in the main text. It is
included to make the estimation choices auditable without turning the article
body into an econometrics appendix.

#### Adoption model

For facility \(i\) in prefecture \(p\) and fiscal year \(t\), let \(A_{it}=1\)
if the facility first reports power generation in year \(t\). The model is
estimated only when the facility is still in the adoption risk set, denoted
\(R_{it}=1\). The main discrete-time logit hazard is:

$$
\Pr(A_{it}=1 \mid R_{it}=1)
= \operatorname{logit}^{-1}
\left[
\alpha
+ \beta_1 I(\text{Age}_{i,t-1}=10\text{-}20)
+ \beta_2 I(\text{Age}_{i,t-1}=20\text{-}30)
+ \beta_3 I(\text{Age}_{i,t-1}\geq 30)
+ \beta_4 \text{Capacity100}_{i,t-1}
+ \gamma_t
\right].
$$

The omitted age category is 0-10 years. \(\gamma_t\) denotes fiscal-year fixed
effects. Capacity is measured in 100 t/day units. Standard errors are clustered
by facility. The table reports average marginal effects in percentage points
because those are easier to read than log-odds coefficients. For example, an
average marginal effect of -1.67 percentage points means that the annual
probability of first reporting generation is 1.67 percentage points lower than
in the omitted 0-10 year age group, conditional on the included variables and
year fixed effects. A saturated year-plus-prefecture fixed-effects model is
reported as sensitivity evidence rather than as the primary estimate. This
keeps the primary model at 18 parameters and 5.44 events per parameter, instead
of 64 parameters and 1.53 events per parameter in the saturated sensitivity.

The adoption equation should not be read as a physical retrofit model. The
dependent variable is observed entry into reported generation in the
administrative panel. A recorded event may correspond to a new plant,
replacement, major refurbishment, reporting transition, or a continuity-type
upgrade; the pathway audit is used only to bound that interpretation.

#### Electricity recovery model

For each operating generator, raw electricity recovery intensity is:

$$
q^{raw}_{it} =
\frac{\text{power generated}_{it}\;(\text{MWh})}
{\text{waste processed}_{it}\;(\text{tonnes})}.
$$

The analysis clips this ratio to 0.01-0.80 MWh/t and then logs it:

$$
q_{it}=\operatorname{clip}(q^{raw}_{it},0.01,0.80),
\qquad
y_{it}=\log(q_{it}).
$$

The core panel regression can be written as:

$$
y_{it}
= \alpha + X_{it}'\beta + \gamma_t + u_i + \varepsilon_{it}.
$$

\(X_{it}\) contains facility age, design capacity in 100 t/day units, capacity
utilization capped at 1.0, heating value in MJ/kg, and the grid-emission factor.
The four main models use the same outcome and covariates but vary the panel
structure:

| Model | Equation terms included | Interpretation |
|:--|:--|:--|
| Pooled OLS | \(X_{it}\) | Overall cross-facility comparison with clustered standard errors |
| Year fixed effects | \(X_{it}+\gamma_t\) | Adds fiscal-year adjustments for shocks common to the fleet |
| Random effects | \(X_{it}+u_i\) | Summarizes persistent facility-level differences |
| Year fixed effects + random effects | \(X_{it}+\gamma_t+u_i\) | Combines fiscal-year adjustment with persistent facility-level differences |

Because the outcome is logged, coefficients are semi-elasticities. For small
coefficients, multiplying by 100 gives an approximate percentage change in MWh/t
for a one-unit change in the predictor. The exact transformation is
\(100[\exp(\beta)-1]\). Thus the pooled age coefficient of -0.0279 corresponds
to about 2.8% lower electricity recovered per tonne for each additional
facility year, while the pooled capacity coefficient of 0.0874 corresponds to
about 9.1% higher electricity recovered per tonne per additional 100 t/day of
design capacity. For utilization, a 0.10 increase in the capped utilization
ratio under the pooled model corresponds to about 7.8% higher electricity
recovered per tonne.

The random-effects specifications are used descriptively. They retain
between-facility structure by estimating a facility-specific intercept, but the
paper does not rely on a causal assumption that unobserved facility or municipal
traits are unrelated to age, capacity, technology, or utilization. A
facility-fixed-effects model would answer a different question: how much
electricity recovery changes within the same facility as its covariates change
over time. That is useful for some policy-effect designs, but it would absorb
much of the durable plant scale, design, and vintage structure that this paper
is explicitly trying to describe. The main paper therefore treats fixed-effects
and random-effects choices as complementary descriptive views, not as a claim
that one estimator identifies a structural causal effect.

### S5.1 Adoption robustness

The main adoption result is estimated as an exact one-fiscal-year lagged
discrete-time logit hazard with year fixed effects plus facility-clustered
standard errors. The saturated year-plus-prefecture fixed-effects model is
retained as sensitivity evidence because first-adoption events are sparse: it
has 64 estimated parameters and 1.53 events per parameter, compared with 18
estimated parameters and 5.44 events per parameter in the primary model. The
broader previous-observed-coded-row model is also retained only as sensitivity
evidence because official facility codes are missing for FY2010-FY2012. Several
robustness variants preserve the main sign pattern:

- previous-observed-coded-row logit
- saturated exact-year logit with year and prefecture fixed effects
- exact-year logit with prefecture fixed effects only
- exact-year logit with age and capacity only
- lagged complementary log-log
- lagged linear probability model

Across these variants, older facilities remain less likely to record observed
transition and larger facilities remain more likely to do so.

The additional duration check adds elapsed at-risk duration, measured in 10-year
units, to the exact-year year fixed-effects hazard. This keeps the expected sign
pattern: age 10-20 is -1.47 pp, age 20-30 is -1.55 pp, age 30+ is -0.90 pp,
and prior-year capacity is +0.45 pp per 100 t/day. The duration coefficient is
-1.329 (p = 0.0099). This is interpreted as a sensitivity check for duration
dependence, not as a separate theory of why facilities wait to enter generation.

The robustness checks are interpreted as sign-pattern checks. They are not used
to claim that the adoption estimates are policy effects or that the event path
is uniquely identified as replacement, refurbishment, or new construction.

### S5.2 Electricity-recovery estimator note

The main electricity-recovery results are presented through four compact specifications:

- pooled OLS
- year fixed effects
- random effects
- year fixed effects plus random effects

The paper keeps these models because the intensive-margin question is largely
about structured cross-facility differences inside the generating segment. The
coefficients are therefore interpreted as structured conditional associations,
not as strict structural parameters. This choice is deliberate: a strict
facility-fixed-effects-only reading would absorb much of the durable facility
heterogeneity that is substantively central to the paper's question. The paper
therefore reports models that preserve cross-facility structure while
explicitly avoiding causal language about vintage or policy effects.

The within-between sensitivity adds another check on this choice. It separates
facility-level means from within-facility deviations and includes year fixed
effects. The between-facility component remains aligned with the main paper:
facility age is negative (-0.0358), capacity is positive (+0.1110), and
utilization is positive (+0.8707). Within-facility deviations also retain the
same signs for the three core variables, but they are not used as the main
interpretive basis because within-panel movement is limited.

### S5.3 Identifier and heating-value sensitivity

The administrative source contains a small number of same-year duplicate
official facility codes. This is a data-structure issue rather than a hidden
result change, so the paper keeps the official-code specification as the main
analysis and reports a composite-ID sensitivity. The sensitivity appends
facility names to affected duplicate official codes and reruns the core
adoption and electricity-recovery checks.

- Official codes with at least one same-year duplicate: 39
- Source rows using those affected official codes: 444
- Adoption-model same-year lag events under official codes: 5
- Regression duplicate facility-year pairs under official codes: 11

**Panel A. Adoption hazard sensitivity**

| Variable | Exact-year official AME (pp) | Official SE | Composite AME (pp) | Composite SE |
|:--|--:|--:|--:|--:|
| Prior-year age 10-20 yrs | -1.67 | 0.25 | -1.66 | 0.25 |
| Prior-year age 20-30 yrs | -1.94 | 0.39 | -1.89 | 0.39 |
| Prior-year age 30+ yrs | -1.24 | 0.38 | -1.22 | 0.39 |
| Prior-year capacity per 100 t/day | 0.45 | 0.15 | 0.46 | 0.16 |

| ID rule | Observations | Facilities | Events | Pseudo-R2 |
|:--|--:|--:|--:|--:|
| Official code | 10,823 | 1,911 | 98 | 0.1829 |
| Composite sensitivity | 10,850 | 1,931 | 99 | 0.1777 |

**Panel B. Electricity-recovery sensitivity**

| Specification | Variable | Official coef. | Composite coef. |
|:--|:--|--:|--:|
| Pooled OLS | Facility age | -0.0279*** | -0.0279*** |
| Pooled OLS | Capacity (100 t/day) | 0.0874*** | 0.0874*** |
| Pooled OLS | Capacity utilization | 0.7468*** | 0.7468*** |
| Year FE | Facility age | -0.0348*** | -0.0348*** |
| Year FE | Capacity (100 t/day) | 0.1030*** | 0.1030*** |
| Year FE | Capacity utilization | 0.7789*** | 0.7789*** |

Heating value is also noisy in the administrative files: 512 rows in the
canonical regression frame have nonpositive heating value and 17 exceed 30
MJ/kg. Restricting the frame to positive values at or below 30 MJ/kg, or to the
stricter 3-25 MJ/kg interval, leaves the age, capacity, and utilization
coefficients substantively unchanged. The detailed generated report is
available at `paper/evidence/current/data_quality_sensitivity.md`.

The implication for review is limited but important: the main electricity-recovery
patterns do not rely on treating every heating-value record as a clean
engineering measurement.

## S5.4 What the checks do not prove

The sensitivity checks reduce several obvious data-quality risks, but they do
not convert the study into a causal or engineering-mechanism design. In
particular, they do not prove:

- that every observed adoption event is a physical retrofit rather than a
  rebuild, replacement, coding update, or administrative timing issue
- that official facility identifiers perfectly track all real-world plant
  histories
- that heating value is measured with engineering-grade precision
- that age coefficients isolate vintage effects from all durable facility,
  municipal, or technology characteristics
- that the generator-frame estimates generalize to uncoded operating-generator
  rows excluded from the canonical panel comparison

These limits are why the main paper uses calibrated phrases such as
`observed transition`, `canonical generator frame`, `structured conditional
association`, and `descriptive pathway evidence`.

## S5.5 Reviewer-response map

This map records the intended answer path for predictable peer-review and
professor-review concerns. It is not a substitute for the main argument; it is a
navigation aid for checking whether each concern already has evidence and
bounded language.

| Likely concern | Main response | Where to inspect |
|:--|:--|:--|
| "Is this just saying newer and larger plants perform better?" | No. The contribution is the two-margin structure: selective entry before generation and persistent hierarchy after entry. | Introduction, Section 4.3, Discussion |
| "Why not one model for the full fleet?" | Non-generators and generators answer different questions. Adoption requires an at-risk transition frame; performance requires positive output and identifiable panel rows. | Section 3, Table 1, S2 |
| "Does adoption mean physical retrofit?" | Not necessarily. The paper uses observed-transition language and treats the pathway audit as descriptive support, not mechanism proof. | Section 4.1, S3, S4 |
| "Are 98 hazard events enough?" | The headline model is parsimonious with year fixed effects; saturated year-plus-prefecture fixed effects are kept as sensitivity evidence because of sparse-event pressure. | Section 3, S5.1 |
| "Why use random effects?" | RE is used descriptively to retain cross-facility structure; it is not presented as a causal solution to unobserved heterogeneity. | Section 3, S5.0, S5.2 |
| "Could missing FY2010-FY2012 codes bias period claims?" | Yes, which is why period language is bounded and the generator frame is called canonical identifiable rather than a census. | Section 3, Section 4.2, S2.3 |
| "Is heating value too noisy?" | Heating value is a control, not a key interpreted outcome; plausible-value restrictions leave the core sign pattern stable. | S5.3 |
| "Can this support policy recommendations?" | It supports planning triage, not intervention ranking. Entry-side asset questions and generator-side performance questions should be separated first. | Discussion, Table 4 |

## S6. Appendix Tables

### S6.1 Table S1. Summary statistics for the canonical generator frame

This table gives the main scale and dispersion of the variables used in the
intensive-margin regressions.

| Variable                       |    N |    Mean |   Median |      SD |    Min |      Max |
|:-------------------------------|-----:|--------:|---------:|--------:|-------:|---------:|
| Electricity recovery (MWh/t, bounded) | 5683 |   0.330 |    0.332 |   0.149 |  0.010 |    0.800 |
| log(Electricity recovery)             | 5683 |  -1.265 |   -1.102 |   0.675 | -4.605 |   -0.223 |
| Facility age (years)           | 5683 |  14.955 |   15.000 |   9.626 |  0.000 |   47.000 |
| Capacity (t/day)               | 5683 | 330.882 |  280.000 | 226.213 | 20.000 | 1800.000 |
| Capacity utilization           | 5683 |   0.600 |    0.610 |   0.135 |  0.013 |    1.000 |
| Heating value (MJ/kg)          | 5683 |   7.936 |    8.295 |   4.304 |  0.000 |  158.942 |
| Grid EF (kg-CO2/kWh)           | 5683 |   0.458 |    0.453 |   0.088 |  0.282 |    0.860 |

*Note: heating value is a noisy administrative estimate derived from the source
files and is retained as a control variable rather than interpreted as a clean
engineering measurement.*

### S6.2 Table S2. Adoption pathway-audit detail

This appendix table makes the adoption-pathway evidence more explicit than the
short main-text summary.

**Panel A. Pathway categories**

| Category                                  | Events | Share (%) |
|:------------------------------------------|------:|----------:|
| Reset / rebuild-like transition           |    50 |      35.5 |
| In-place upgrade / continuity transition  |    36 |      25.5 |
| Forward-dated / placeholder entry         |    12 |       8.5 |
| Timing-ambiguous / non-adjacent coded row |    42 |      29.8 |
| Unresolved / insufficient continuity      |     1 |       0.7 |

**Panel B. Event-year distribution**

| Fiscal year | First adoptions |
|------------:|----------------:|
|        2006 |               5 |
|        2007 |               4 |
|        2008 |               2 |
|        2009 |               2 |
|        2013 |              30 |
|        2014 |               3 |
|        2015 |              21 |
|        2016 |              17 |
|        2017 |              12 |
|        2018 |              10 |
|        2019 |              16 |
|        2021 |               6 |
|        2022 |               8 |
|        2023 |               2 |
|        2024 |               3 |

Interpretation: the pathway audit supports a selective modernization reading,
but non-adjacent coded-row events are timing-ambiguous and the panel still does
not uniquely identify replacement, major refurbishment, or new build as the
singular pathway behind the observed transition events.

## S7. Additional Descriptive Material

Useful descriptive tables already synchronized into the paper workspace include:

- [sample_definition.md](../evidence/current/sample_definition.md)
- [adoption_results.md](../evidence/current/adoption_results.md)
- [regression_results.md](../evidence/current/regression_results.md)
- [table1_summary_stats.md](../evidence/current/table1_summary_stats.md)
- [table2_efficiency_by_age.md](../evidence/current/table2_efficiency_by_age.md)
- [data_quality_sensitivity.md](../evidence/current/data_quality_sensitivity.md)

These files remain part of the paper's evidence layer and can be converted into
appendix tables if a target journal asks for additional detail.
