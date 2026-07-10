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
| Year indicators | Fiscal-year dummy variables that absorb conditions common to the fleet in a given year; these are not facility fixed effects |
| FE | Fixed effects; facility FE are discussed as a different estimand but are not used in the main table |
| RE | Random effects, used descriptively to represent persistent facility-level differences |
| AME | Average marginal effect from a logit hazard, reported in percentage points |
| pp | Percentage points |
| MWh/t | Gross megawatt-hours of electricity generated per tonne of waste processed |
| MJ/kg | Megajoules per kilogram |
| Panel exit | Final disappearance from the coded panel before FY2024; not verified physical closure |
| Broad asset entry | First positive installed capacity among all coded at-risk assets, including rows that may reflect commissioning, rebuild, or inactivity |
| Active conversion | First positive installed capacity after requiring positive throughput in the immediately preceding fiscal year |
| Age/vintage | A cross-facility age comparison that may combine physical age, design vintage, and other durable plant characteristics |

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
| Installed-capacity entry may not equal a directly observed physical retrofit or first operating date. | The event is defined explicitly as first positive installed generation capacity; a positive-output alternative and post-entry bridge test whether it maps to operation. |
| Left-censored generators can distort adoption estimates. | Facilities already generating in their first observed year are excluded from the adoption risk set. |
| Official-code gaps can turn prior-year lags into previous-observed-row lags. | The main adoption model now keeps only exact one-fiscal-year lags; the broader previous-observed-coded-row model is reported only as sensitivity evidence. |
| Official facility codes sometimes repeat within a fiscal year. | The supplement reports a composite-ID sensitivity; headline adoption and electricity-recovery signs remain stable. |
| Heating value is noisy in administrative files. | Heating value is treated as a control, not an engineering outcome; plausible-value restrictions leave the core coefficients stable. |
| The generator frame excludes uncoded operating rows. | The main text defines the electricity-recovery sample as the canonical identifiable generator frame, and this supplement compares coded and uncoded operating-generator rows. |
| Age effects could be confounded with durable facility characteristics. | The paper explicitly calls the generator coefficient an age/vintage association and does not interpret it as a within-plant aging effect. |
| Entry events are temporally clustered. | The paper reports the clustering and uses fiscal-year indicators; it does not interpret the timing as a uniquely identified policy shock or reporting change. |
| Adoption risk may vary with time already spent at risk. | Actual elapsed fiscal time at risk is included in the main entry model; it is not inferred from the number of observed rows. |
| Broad asset entry may be mistaken for retrofit of an operating plant. | The paper reports a required positive-prior-throughput model. Scale persists, while the age gradient attenuates. |
| Non-entry may be confused with continued operation through the panel endpoint. | A separate panel-exit hazard treats final coded disappearance as a competing observed path but does not call it closure. |
| Bounded MWh/t could create the regression pattern. | Unclipped-log outcome models preserve the age, capacity, and utilization signs. |
| MWh/t may be too remote from engineering performance. | Heating-value-based thermal conversion and reported generation-efficiency models preserve the main signs in a plausible-value frame. |
| “Persistent hierarchy” could rely only on a variance decomposition. | Adjacent-year within-year percentile ranks correlate at 0.9325 across 4,368 exact pairs. |

The result is a narrower but more defensible claim: entry is robustly scale-
selective, its age pattern depends on the risk-set definition, and post-entry
performance remains structured among identifiable generators.

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

### S2.1 Installed-capacity entry frame

- Main event: first observed positive installed generation capacity
- Left-censored facilities already reporting positive capacity in their first observed year: 913
- Entry risk-set observations: 13,770
- Entry risk-set facilities: 2,035
- Observed installed-capacity entry events in the panel window: 141
- Exact-year lagged entry-model observations: 10,823
- Exact-year lagged entry-model facilities: 1,911
- Installed-capacity entry events retained in the exact-year lagged model: 98
- Exact-year events with zero or missing prior-year throughput: 40
- Active-conversion sensitivity: 9,215 facility-years, 1,663 facilities, 58 events
- Exact-lag rows where actual elapsed fiscal duration differs from observed-row count: 4,055
- Broader previous-observed-coded-row model frame before exact-year restriction: 11,717 observations, 1,915 facilities, 140 events
- Non-exact lag rows excluded from the main entry model: 894 rows, including 42 events
- Positive-output alternative: 10,937 exact-year observations and 146 events
- Post-entry output bridge: 128 of 141 positive in the event year, 135 by year +1, and 138 within the observed event-to-three-year window

Interpretation: the main model estimates broad coded-asset entry, not unrestricted
fleet-wide modernization or a verified engineering retrofit. The active-
conversion model narrows the estimand to facilities with positive prior-year
throughput; comparing the two is part of the result rather than a cosmetic check.

### S2.2 Generator frame

- Canonical regression observations: 5,683
- Canonical regression facilities: 1,016
- Fiscal years covered: FY2005-FY2024
- Within/total variance ratio of pooled log electricity-recovery intensity: 0.1499
- Early coded-window ratio (FY2005-FY2009): 0.1795
- Later coded-window ratio (FY2013-FY2024): 0.0956
- Exact adjacent-year rank pairs: 4,368 across 915 facilities
- Pooled adjacent-year within-year percentile-rank correlation: 0.9325
- Median annual rank correlation: 0.9323 (range 0.8848-0.9763)

Interpretation: the intensive-margin models are designed to describe structured
conditional performance within the generating segment, not to identify a strict
causal policy effect.

### S2.3 Competing coded-panel exit

Among 1,894 facilities with no installed-capacity event, 1,305 (68.9%) are last
observed before FY2024. A separate exact-year next-period hazard contains 12,108
facility-years across 2,022 facilities and 1,285 final coded-panel exits.
Facilities aged 30 or more have a +2.60 pp AME relative to age 0-10, while
capacity has a -1.63 pp AME per 100 t/day. The two younger age-band estimates
are not statistically distinguishable from zero. Known non-adjacent code-gap
intervals are excluded rather than forced into exit events. Because the source
does not verify physical closure, this is an attrition diagnostic, not a closure
model.

### S2.4 Generator-frame inclusion audit

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

The entry frame includes facilities first observed without positive installed
power-generation capacity. Facilities already reporting positive capacity in
their first observed year are excluded as left-censored for the entry question.
The main lagged hazard specification
then requires exact one-fiscal-year prior age band and prior-year design
capacity, which removes the first observed at-risk year for each facility, a
small number of additional rows with missing lagged predictors, and non-exact
lag rows created by duplicate same-year codes or official-code gaps.

The model also includes actual elapsed fiscal time since first entering the risk
set, measured from fiscal-year values. It does not use the number of observed
rows as a duration proxy. Those quantities differ on 4,055 exact-lag rows because
the official-code panel has gaps.

The entry estimand is therefore not "which facilities ever modernized" in a
complete historical sense. It is the probability that a coded facility first
records positive installed generation capacity in the next observed fiscal
year, conditional on still
being observed at risk in the panel and conditional on exact one-fiscal-year
prior age and capacity. This distinction protects the paper from overclaiming about
unobserved pre-panel investments or physical retrofit histories that the
administrative file does not directly record.

The broad risk set does not require positive throughput before entry. Because 40
of 98 exact-year events have zero or missing prior-year throughput, it can include
commissioning, rebuild, inactive-asset, and reporting pathways. The active-
conversion model requires positive prior-year throughput and therefore answers a
narrower question about operating non-generators. It is not assumed that the two
frames estimate the same population parameter.

Observed entry events are temporally clustered: 109 of 141 events occur in
FY2013-FY2019. The main hazard includes fiscal-year indicators, and the paper
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

#### Installed-capacity entry model

For facility \(i\) in prefecture \(p\) and fiscal year \(t\), let \(A_{it}=1\)
if the facility first reports positive installed power-generation capacity in
year \(t\). The model is estimated only when the facility is still in the entry risk set, denoted
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
+ \delta D_{it}
+ \gamma_t
\right].
$$

The omitted age category is 0-10 years. \(\gamma_t\) denotes fiscal-year
indicators, not facility fixed effects. Capacity is measured in 100 t/day units,
and \(D_{it}\) is actual elapsed at-risk duration in ten-fiscal-year units.
Standard errors are clustered
by facility. The table reports average marginal effects in percentage points
because those are easier to read than log-odds coefficients. For example, an
average marginal effect of -1.41 percentage points means that the annual
probability of first reporting positive installed capacity is 1.41 percentage points lower than
in the omitted 0-10 year age group, conditional on the included variables and
year indicators. A saturated year-plus-prefecture specification is
reported as sensitivity evidence rather than as the primary estimate. This
keeps the primary model at 19 parameters and 5.16 events per parameter, instead
of 64 parameters and 1.53 events per parameter in the saturated sensitivity.

The entry equation should not be read as a physical retrofit model. The
dependent variable is observed entry into reported installed capacity in the
administrative panel. A recorded event may correspond to a new plant,
replacement, major refurbishment, reporting transition, or a continuity-type
upgrade; the pathway audit is used only to bound that interpretation.

The active-conversion sensitivity fits the same equation after requiring
positive prior-year throughput. It contains 58 events rather than 98. The broad
and active models should be compared term by term: capacity AMEs are +0.45 and
+0.44 pp, while the three age AMEs move from -1.41, -1.45, and -0.83 pp to
-0.67, -0.56, and -0.29 pp.

Two event diagnostics use the same logic. The positive-output alternative sets
\(A_{it}=1\) at first reported positive electricity generation. The panel-exit
hazard instead sets \(E_{it}=1\) when a still-at-risk facility is observed in
year \(t\), is not observed in \(t+1\), and is last observed before FY2024,
after excluding known non-adjacent code-gap intervals. Neither event is treated
as a direct observation of engineering retrofit or physical closure.

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

The primary RQ2 regression can be written as:

$$
y_{it}
= \alpha + X_{it}'\beta + Z_{it}'\theta + \gamma_t + \varepsilon_{it}.
$$

\(X_{it}\) contains facility age, design capacity in 100 t/day units, capacity
utilization capped at 1.0, and heating value in MJ/kg. Before capping,
utilization is

$$
U^{raw}_{it}=\frac{\text{annual waste processed}_{it}}
{\text{design capacity}_{it}\times365},
\qquad U_{it}=\min(U^{raw}_{it},1).
$$

The numerator of \(q^{raw}_{it}\) is reported gross generation, not net export
after onsite use. The metric also excludes useful heat and should not be read as
full thermodynamic efficiency. \(Z_{it}\) contains normalized furnace type,
operating mode, facility type, and number of furnaces. The primary model uses
fiscal-year indicators and facility-clustered standard errors. Facility age is
derived from fiscal year and reported starting year; with year indicators, its
coefficient is an age/vintage comparison across facilities observed in a common
year, not a causal within-plant aging effect.

The supplemental estimator ladder uses the same core outcome and covariates but
varies the panel structure:

| Model | Equation terms included | Interpretation |
|:--|:--|:--|
| Pooled OLS | \(X_{it}\) | Overall cross-facility comparison with clustered standard errors |
| Year indicators | \(X_{it}+\gamma_t\) | Adds fiscal-year adjustments for shocks common to the fleet |
| Random effects | \(X_{it}+u_i\) | Summarizes persistent facility-level differences |
| Year indicators + random effects | \(X_{it}+\gamma_t+u_i\) | Combines fiscal-year adjustment with persistent facility-level differences |

Because the outcome is logged, coefficients are semi-elasticities. For small
coefficients, multiplying by 100 gives an approximate percentage change in MWh/t
for a one-unit change in the predictor. The exact transformation is
\(100[\exp(\beta)-1]\). Thus the primary age/vintage coefficient of -0.0329
corresponds to about 3.2% lower electricity recovered per tonne for each
additional age year in a cross-facility comparison, while the capacity
coefficient of 0.1103 corresponds to about 11.7% higher electricity recovered
per tonne per additional 100 t/day. For utilization, a 0.10 difference under
the primary model corresponds to about 7.9% higher electricity recovered per
tonne.

The primary model is year- and technology-adjusted OLS. Random-effects
specifications are supplementary and descriptive. They retain
between-facility structure by estimating a facility-specific intercept, but the
paper does not rely on a causal assumption that unobserved facility or municipal
traits are unrelated to age, capacity, technology, or utilization. A
facility-fixed-effects model would answer a different question: how much
electricity recovery changes within the same facility as its covariates change
over time. That is useful for some policy-effect designs, but it would absorb
much of the durable plant scale, design, and vintage structure that this paper
is explicitly trying to describe. The paper therefore treats the estimator
ladder as complementary descriptive views, not as a claim that one estimator
identifies a structural causal effect.

The bounded outcome is not the sole basis of the result. Robustness models use
\(\log(q^{raw}_{it})\) without clipping and preserve the negative age and
positive capacity and utilization coefficients. Persistence is also assessed by
ranking facilities within each fiscal year and correlating percentile ranks for
exact adjacent-year pairs, avoiding dependence on the outcome's absolute scale.

Two engineering-oriented outcomes add convergent validation in the 4,971-row
plausible-value frame. The gross thermal-conversion proxy is

$$
T_{it} = \frac{q^{raw}_{it}\times 3.6}{\text{heating value}_{it}},
$$

where the 3.6 factor converts MWh to GJ and the numerical MJ/kg heating value is
equivalent to GJ/t. A second outcome uses reported generation efficiency. Their
logged values correlate at 0.8636, and technology-adjusted models preserve
negative age/vintage and positive capacity and utilization associations. Because
the outcomes share administrative inputs, this is convergent rather than
independent validation.

### S5.1 Installed-capacity entry robustness

The main entry result is estimated as an exact one-fiscal-year lagged
discrete-time logit hazard with fiscal-year indicators, actual elapsed at-risk
duration, and facility-clustered standard errors. The saturated year-plus-
prefecture fixed-effects model is
retained as sensitivity evidence because entry events are sparse: it
has 64 estimated parameters and 1.53 events per parameter, compared with 19
estimated parameters and 5.16 events per parameter in the primary model. The
broader previous-observed-coded-row model is also retained only as sensitivity
evidence because official facility codes are missing for FY2010-FY2012. Several
robustness variants preserve the main sign pattern:

- previous-observed-coded-row logit
- saturated exact-year logit with year and prefecture fixed effects
- exact-year logit with prefecture fixed effects only
- exact-year logit with age and capacity only
- lagged complementary log-log
- lagged linear probability model
- exact-year positive-prior-throughput active-conversion model
- exact-year model with prior observed technology profiles
- positive-electricity-output event definition
- p99-capped capacity and log-capacity forms

Across broad-frame variants, age AMEs remain negative and capacity remains
positive. The positive-output event contains 10,937 rows and 146 events; its age
AMEs are -2.57, -3.03, and -2.03 pp and capacity is +0.64 pp. Capping capacity
at p99 gives +0.87 pp per 100 t/day, while log(1 + t/day) remains positive
(coefficient 1.414, p < 0.001). Adding prior technology profiles leaves capacity
at +0.34 pp.

The main duration coefficient, measured per ten elapsed fiscal years, is -1.134
(p = 0.0006). It controls duration dependence but is not interpreted as a theory
of waiting. More importantly, the active-conversion model preserves capacity at
+0.44 pp while attenuating age AMEs to -0.67, -0.56, and -0.29 pp. The latter
two age estimates are not conventionally significant. Robust scale selectivity
therefore travels across risk sets; a universal operating-plant age gradient
does not.

The robustness checks are interpreted as sign-pattern checks. They are not used
to claim that the entry estimates are policy effects or that the event path
is uniquely identified as replacement, refurbishment, or new construction.

#### S5.1a Post-entry operating bridge

The installed-capacity event is linked forward to observed output and to the
canonical generator frame. Of 141 events, 128 report positive electricity
output in the event year, 135 by one year, and 138 within the observed
event-to-three-year window. Only 3 reverse the positive-capacity flag in an
observed next year, and 137 appear in the canonical operating-generator frame
within three years.

| Years from capacity event | Generator rows | Events represented | Mean MWh/t | Median MWh/t |
|--:|--:|--:|--:|--:|
| 0 | 125 | 125 | 0.324 | 0.351 |
| 1 | 102 | 102 | 0.338 | 0.366 |
| 2 | 91 | 91 | 0.325 | 0.361 |
| 3 | 71 | 71 | 0.339 | 0.360 |

The event-time comparison uses same-year incumbents and within-year percentile
ranks to avoid confusing entrant timing with common year conditions. An
incumbent has no observed entry event or an event before the comparison fiscal
year:

| Event time | Events | Entrant mean MWh/t | Mean percentile | Incumbent mean MWh/t | Difference |
|--:|--:|--:|--:|--:|--:|
| 0 | 125 | 0.324 | 51.5 | 0.329 | -0.006 |
| 1 | 102 | 0.338 | 54.8 | 0.328 | +0.009 |
| 2 | 91 | 0.325 | 52.1 | 0.335 | -0.010 |
| 3 | 71 | 0.339 | 52.9 | 0.340 | -0.001 |

Across 389 observations and 137 events, entrants are near the middle of the
same-year distribution on average. At event time zero, entrants operating in the
prior year average the 45.7th percentile, compared with 51.4 for zero/missing
prior throughput and 60.8 for events with no exact prior-year row. Follow-up is
selected and declines to 71 events by time three, so subgroup paths are
descriptive clues rather than entry effects. At first canonical-frame appearance,
entrant and incumbent means both round to 0.328 MWh/t; this validates operational
relevance without implying superior performance.

#### S5.1b Competing panel-exit diagnostic

The exit hazard uses the same pre-event age bands and capacity scale as the entry
hazard. Its age-30+ AME is +2.60 pp (SE 0.85), and its capacity AME is -1.63 pp
per 100 t/day (SE 0.32). The age 10-20 and age 20-30 estimates are -0.42 pp and
+0.18 pp and are not statistically distinguishable from zero. These estimates
describe final coded-panel disappearance before FY2024, not verified closure.

### S5.2 Electricity-recovery estimator note

The primary model is year- and technology-adjusted OLS. Its focal coefficients
are -0.0329 for age/vintage, +0.1103 for capacity per 100 t/day, and +0.7600 for
utilization; all have p < 0.001. Heating value is +0.0032 with p = 0.119. The
model contains 5,683 observations across 1,016 facilities and has R-squared
0.3830. The base year-adjusted model without technology controls gives -0.0348,
+0.1051, and +0.7760, with R-squared 0.3699.

Pooled OLS, year-indicator OLS, random effects, and year-indicator plus random-
effects models form a supplemental ladder. They preserve cross-facility
structure under different representations of common-year and persistent
heterogeneity. None is interpreted as a strict structural parameter, and a
facility-fixed-effects-only model would answer a different within-facility
question while absorbing durable scale and vintage structure.

The within-between sensitivity adds another check on this choice. It separates
facility-level means from within-facility deviations and includes year
indicators. The between-facility component remains aligned with the main paper:
facility age is negative (-0.0359), capacity is positive (+0.1140), and
utilization is positive (+0.8646). Within-facility deviations also retain the
same signs for the three core variables, but age is mechanically related to
calendar time in an unbalanced panel. Those terms are not used as causal aging
effects.

The unbounded raw-ratio log models also preserve the pattern. Pooled estimates
are -0.0274 for age, +0.0891 for capacity, and +0.7526 for utilization; adding
year indicators gives -0.0346, +0.1090, and +0.7761, respectively. The bounded
outcome therefore controls extreme administrative ratios without determining
the result.

Technology-adjusted thermal-conversion and reported-efficiency models in the
4,971-row plausible-value frame yield age/vintage coefficients of -0.0326 and
-0.0329, capacity coefficients of +0.0768 and +0.0747, and utilization
coefficients of +0.5353 and +0.4817. An exact-adjacent-year lagged-predictor model
on 4,368 observations gives -0.0361, +0.1040, and +0.6074. All nine focal
coefficients have p < 0.01.

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
| Prior-year age 10-20 yrs | -1.41 | 0.21 | -1.43 | 0.21 |
| Prior-year age 20-30 yrs | -1.45 | 0.33 | -1.45 | 0.33 |
| Prior-year age 30+ yrs | -0.83 | 0.35 | -0.85 | 0.35 |
| Prior-year capacity per 100 t/day | 0.45 | 0.15 | 0.46 | 0.16 |

| ID rule | Observations | Facilities | Events | Pseudo-R2 |
|:--|--:|--:|--:|--:|
| Official code | 10,823 | 1,911 | 98 | 0.1920 |
| Composite sensitivity | 10,850 | 1,931 | 99 | 0.1862 |

**Panel B. Electricity-recovery sensitivity**

| Specification | Variable | Official coef. | Composite coef. |
|:--|:--|--:|--:|
| Pooled OLS | Facility age | -0.0277*** | -0.0277*** |
| Pooled OLS | Capacity (100 t/day) | 0.0853*** | 0.0853*** |
| Pooled OLS | Capacity utilization | 0.7462*** | 0.7462*** |
| Year indicators | Facility age | -0.0348*** | -0.0348*** |
| Year indicators | Capacity (100 t/day) | 0.1051*** | 0.1051*** |
| Year indicators | Capacity utilization | 0.7760*** | 0.7760*** |

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
- that broad asset entry and active operating-plant conversion have the same age
  association or represent the same population
- that official facility identifiers perfectly track all real-world plant
  histories
- that heating value is measured with engineering-grade precision
- that age coefficients isolate vintage effects from all durable facility,
  municipal, or technology characteristics
- that the generator-frame estimates generalize to uncoded operating-generator
  rows excluded from the canonical panel comparison
- that final coded-panel disappearance is physical closure
- that installed capacity is continuously usable capacity or that gross
  generation equals net export
- that high adjacent-year rank persistence rules out meaningful plant-specific
  operational gains
- that the selected post-entry trajectory estimates a treatment effect or
  represents entrants that disappear from follow-up

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
| "Is this just saying newer and larger plants perform better?" | No. Scale selectivity survives both risk sets, but the age gradient attenuates among active non-generators; entrants also begin near the middle of the same-year generator distribution. | Introduction, Sections 4.1 and 4.3, Discussion |
| "Why not one model for the full fleet?" | Non-generators and generators answer different questions. Adoption requires an at-risk transition frame; performance requires positive output and identifiable panel rows. | Section 3, Table 1, S2 |
| "Does entry mean physical retrofit or output?" | Not necessarily. The main event is first positive installed capacity; a positive-output event and post-entry bridge preserve the result and demonstrate operational follow-through. | Section 4.1, S3, S5.1a |
| "Are 98 hazard events enough?" | The broad model is parsimonious at 5.16 events per parameter; the 58-event active model is explicitly treated as sparse sensitivity evidence, and saturated models are not headlined. | Section 3, S5.1 |
| "Why use random effects?" | RE is no longer the primary RQ2 estimator. The primary model is year- and technology-adjusted OLS; RE remains one descriptive rung in the supplement. | Section 3, S5.0, S5.2 |
| "Could missing FY2010-FY2012 codes bias period claims?" | Yes, which is why period language is bounded and the generator frame is called canonical identifiable rather than a census. | Section 3, Section 4.2, S2.4 |
| "Are non-entrants assumed to remain open?" | No. A separate panel-exit hazard makes administrative disappearance explicit but does not equate it with closure. | Section 4.1, S2.3, S5.1b |
| "Is persistence inferred only from low within variance?" | No. The paper also reports a 0.9325 pooled adjacent-year percentile-rank correlation across 4,368 exact pairs. | Section 4.2, S2.2, S5.2 |
| "Is heating value too noisy?" | Heating value is a control, not a key interpreted outcome; plausible-value restrictions leave the core sign pattern stable. | S5.3 |
| "Is MWh/t an engineering performance measure?" | It is a gross operational intensity, not net or total efficiency. Thermal-conversion and reported-efficiency checks preserve the focal signs in a plausible-value frame. | Section 3, S5.0, S5.2 |
| "Does entry improve performance?" | The trajectory is descriptive: entrants average near the same-year distribution middle, with attrition from 125 to 71 events. No entry treatment effect is claimed. | Section 4.3, S5.1a |
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
