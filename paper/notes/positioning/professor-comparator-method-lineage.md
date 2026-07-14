# Professor Method-Lineage And Orientation Packet

Last updated: 2026-07-14

## Purpose

This packet explains the corrected paper to a professor who needs to assess its
intellectual foundation, empirical design, originality, limitations, and best
next direction. It is not a history of earlier drafts. All sample counts,
estimands, equations, and interpretations below refer to the current
administrative-lineage analysis.

The paper combines established ideas rather than claiming a new estimator. It
adapts facility-hierarchy and decomposition logic from waste-incineration
research, annual transition logic from event-history research, and bias-
reduced logistic estimation for sparse events. Its Japan panel, longitudinal
identity reconstruction, variables, event definitions, estimands, code,
figures, tables, and numerical results are original to this project.

No wording, code, data, estimates, tables, or figures are copied from the
comparator papers. The intellectual ideas and standard methods that influenced
the design are identified and cited explicitly.

## Executive Orientation

### One-sentence description

> The paper asks how widely electricity generation is distributed across
> Japan's municipal waste-incineration fleet, which continuously observed
> non-generating lineages first report installed generation capacity, and how
> generator sizing and annual loading jointly produce the observed electricity
> generated per tonne.

### Why the paper is not just an "old versus new plant" comparison

The corrected paper has three linked but distinct empirical layers:

| Layer | Question | Current evidence | Interpretation |
|:--|:--|:--|:--|
| Fleet coverage | Does the number of generating facilities represent the waste volume handled by generators? | In FY2024, installed-generation facilities are 41.1% of facility records, positive-output facilities handle 80.1% of throughput, and installed-generation facilities hold 70.5% of waste-processing design capacity. | Facility counts and system volume answer different questions. |
| First reported entry | Among lineages observed without installed generation, which characteristics precede the first positive installed-capacity report? | There are 55 descriptive first entries, 35 broad exact-year model events, 33 after positive prior-year operation, and 24 under same-episode continuity. The frozen five-parameter model gives a 300-versus-100 t/day odds ratio of 6.72 (bootstrap 95% CI 4.31-12.46); all event attacks leave it between 6.12 and 7.30. | Entry is strongly scale-selective, while the continuous-age estimate is imprecise and continuity-sensitive; the model does not identify why entry occurs. |
| Generator components | Among positive-output generators, what produces gross MWh/t differences? | The primary engineering frame contains 6,511 rows across 493 stable administrative lineages. Adjusted installed capacity is 79.1%, 58.6%, and 23.5% lower in the three older reported start-year cohorts than in 2010-or-later records, whereas adjusted capacity factors are 35.3%, 22.0%, and 1.5% higher. | The apparent cohort hierarchy is primarily generator sizing, not uniformly better annual use. Reported start year is not a verified generator vintage. |

### Current central argument

The defensible argument is distributional and diagnostic, not causal:

1. Generation is less common by facility count than by the share of waste
   throughput handled.
2. First reported entry into installed generation is concentrated among larger
   waste-processing lineages.
3. Within the generating segment, gross MWh/t must be decomposed into installed
   generator sizing, electrical capacity factor, and waste loading before age
   or operational variables are interpreted.

These findings matter because a single fleet average can confuse three policy
questions: how many facilities generate, how much waste is processed where
generation occurs, and how generating facilities are technically sized and
loaded.

### What the paper does not claim

- It does not estimate the causal effect of plant age, scale, utilization,
  subsidies, municipal policy, or a retrofit.
- It does not equate first positive reported capacity with a verified retrofit,
  construction date, or investment decision.
- It does not treat an administrative facility code as a permanent physical-
  plant identifier.
- It does not call gross MWh/t net electrical efficiency, thermodynamic
  efficiency, useful-energy recovery, electricity export, or lifecycle benefit.
- It does not infer closure from the disappearance of an administrative record.
- It does not treat the nested prior-operation frame as an independent group or
  use its two excluded events as an equality or equivalence test.
- It does not reproduce the optimization, data-envelopment-analysis, emissions,
  or policy models used by the comparator papers.

## Recommended Reading Order For A Professor

1. Read the executive orientation and the research-question map.
2. Read the comparator lineage matrix to see exactly what is adapted.
3. Read the equations and sample construction to assess the estimands.
4. Read the interpretation limits and challenge agenda before suggesting a
   stronger causal or engineering claim.
5. Use the pivot options to decide whether the current paper should be kept
   narrow or expanded with new data.

## Research Questions And Estimands

### RQ1: Fleet distribution

**Question:** How different are facility-count participation, throughput
coverage, and waste-processing design-capacity coverage in the incineration
fleet?

**Estimands:** Annual descriptive shares. These are accounting quantities, not
regression effects.

**Current answer:** In FY2024, the three shares are 41.1%, 80.1%, and 70.5%,
respectively. The count-volume difference is the result. The 41.1% facility
share must not be described as the share of Japanese waste that misses
generation.

### RQ2: First reported installed-capacity entry

**Question:** Among stable administrative lineages observed without installed
electrical-generation capacity, which prior-year characteristics are associated
with the first positive capacity report?

**Estimand:** A conditional annual transition probability within the observed
at-risk population. The main coefficient contrast compares otherwise modeled
lineage-years with different prior-year waste-processing design capacities.

**Current answer:** Scale selectivity is the robust result. The frozen
five-parameter Firth model gives a 300-versus-100 t/day odds ratio of 6.72 in
the broad frame (1,999-lineage-bootstrap 95% CI 4.31-12.46), 7.09 in the
prior-operation frame, 7.15 under same-episode continuity, and 6.76 after
uncertain lineages are excluded. Reclassifying any one event or deleting its
whole lineage leaves the scale contrast between 6.12 and 7.30. The continuous
age coefficient is -0.327 per decade in the broad frame (bootstrap CI -0.774 to
0.070) but -0.751 under same-episode continuity (-1.364 to -0.206), which has
only 24 events. Age is therefore a continuity-sensitive secondary result, not
a general barrier headline.

### RQ3: Generator design and annual operation

**Question:** Among engineering-valid positive-output generator observations,
how do generator design intensity and electrical capacity factor structure
gross electricity generation per tonne?

**Estimands:** Conditional associations in component-specific pooled panel
models, plus a specification diagnostic comparing a gross-intensity model with
and without generator sizing.

**Current answer:** The primary analysis is the 6,511-row raw-quantity
decomposition. Installed kW has a processing-capacity elasticity of 1.532 (95%
CI 1.447-1.617). Relative to 2010-or-later records and conditional on observed
controls, installed capacity is 79.1%, 58.6%, and 23.5% lower in pre-1990,
1990s, and 2000s cohorts. Their capacity factors are 35.3%, 22.0%, and 1.5%
higher, with the 2000s interval spanning zero. A direct gross-output model gives
throughput and installed-kW elasticities of 0.638 and 0.576. The separate
5,806-row sizing diagnostic remains useful: adding generator design intensity
raises `R^2` from 0.4737 to 0.8131 and leaves age at -0.0020 (`p = 0.2977`).
That is specification evidence, not causal mediation.

## Data And Longitudinal Identity

### Source frame

The source is an annual Japanese municipal waste-treatment administrative
panel covering FY2005-FY2024. After exact duplicate source records are
collapsed, the analysis retains 23,593 facility-year records.

The raw-data provenance manifest records recoverable source configuration,
file hashes, byte sizes, and workbook schema mappings. The original retrieval
timestamp is unavailable. Checkout filesystem modification time (mtime) is
unavailable/not persisted because it is volatile. Last Git commit time records
repository history, not retrieval or acquisition time.

### Why identity reconstruction is part of the method

Official facility codes cannot be assumed to persist longitudinally. Some
years lack usable official codes, and the code system changes across part of
the panel. A naive code-based lag can therefore connect the wrong record,
break a real history, or manufacture a transition.

The corrected pipeline constructs:

- 1,690 **stable administrative lineages**, called administrative lineages in
  the prose and stored as `stable_site_id`, intended to connect the
  same continuing site-level administrative entity across years; and
- 1,767 **asset episodes**, which split a lineage when reported start year or
  major configuration evidence indicates a possible replacement or reset.

Matching uses annual one-to-one constraints and evidence from normalized
facility name, municipality, reported start year, waste-processing design
capacity, furnace count, and available configuration fields. Adjacent years
are resolved before short gaps. Official codes are supporting fields rather
than conclusive identities.

Sub-threshold and weak ambiguous candidate edges are removed before assignment.
The resolver evaluates both the current row's alternative and the prior
record's competing claimant. Sixteen accepted links across 14 lineages remain
uncertain under this two-sided margin rule, but all retain exact-name or
official-code evidence and are exposed individually. Whole-lineage
identity-certain sensitivities exclude all affected lineages; the entry model
retains 15,107 rows, 1,130 lineages, and all 35 events, while the component
model retains 6,450 rows across 487 lineages.

### Identity terminology that must remain precise

| Term | Meaning in this paper | Meaning it does not establish |
|:--|:--|:--|
| Facility-year record | One retained administrative observation in one fiscal year | A uniquely verified boiler, turbine, or legal entity |
| Stable administrative lineage | Records linked as a continuing site-level administrative history | Proof that physical equipment never changed |
| Asset episode | A segment separated when the record indicates a material start-year or configuration reset | A fully externally verified rebuild date |
| Exact continuity-lineage event | Positive capacity first appears in the adjacent year while stable-lineage and asset-episode continuity are preserved | A proven retrofit decision |

### Remaining identity limitation

Deterministic record linkage creates an auditable longitudinal grain; it does
not eliminate all linkage uncertainty. A professor should treat linkage as a
measurement layer that supports annual comparisons, not as ground truth about
physical ownership or equipment continuity. Any future causal or project-level
study would require external validation from facility histories, procurement
records, permits, or operator documents.

## Notation

For stable administrative lineage `i` in fiscal year `t`:

| Symbol | Definition | Unit |
|:--|:--|:--|
| `W_it` | Waste-processing design capacity | tonnes/day |
| `Q_it` | Recorded annual waste throughput | tonnes/year |
| `K_it` | Installed electrical-generation capacity | kW |
| `E_it` | Recorded gross electricity generation | MWh/year |
| `A_it` | Reported facility age or age band | years/category |
| `Z_it` | Available furnace and facility configuration controls | vector |
| `O_i,t-1` | Indicator for positive prior-year waste throughput | binary |
| `Y_it` | First positive installed-capacity report while at risk | binary |

The terms "waste-processing design capacity" (`W`) and "installed electrical-
generation capacity" (`K`) must never be shortened to the same word without a
qualifier.

## Equation Set 1: Fleet Coverage

Define `I_it^K = 1[K_it > 0]` for positive installed electrical capacity and
`I_it^E = 1[E_it > 0 and Q_it > 0]` for positive-output operation.

The facility participation share is:

$$
P_t = \frac{\sum_i I_{it}^{K}}{N_t}.
$$

The positive-output throughput coverage share is:

$$
V_t = \frac{\sum_i I_{it}^{E} Q_{it}}{\sum_i Q_{it}}.
$$

The installed-generation share of waste-processing design capacity is:

$$
C_t = \frac{\sum_i I_{it}^{K} W_{it}}{\sum_i W_{it}}.
$$

These equations deliberately use different indicators and denominators. A
facility can report installed generation capacity without positive annual
output, and a large operating generator can account for far more throughput
than a small non-generator.

For engineering-valid positive-output rows, the fleet gross-intensity identity
is:

$$
\frac{\sum_{i \in \mathcal{G}_t} E_{it}}{\sum_i Q_{it}}
=
\left(\frac{\sum_{i \in \mathcal{G}_t} Q_{it}}{\sum_i Q_{it}}\right)
\left(\frac{\sum_{i \in \mathcal{G}_t} E_{it}}
{\sum_{i \in \mathcal{G}_t} Q_{it}}\right),
$$

where `G_t` is the engineering-valid generator set. In words:

> Fleet gross MWh per total tonne equals generator-throughput coverage times
> conditional generator gross MWh/t.

This is an exact accounting identity. It is adapted in spirit from the
decomposition and hierarchy emphasis of Cui et al. (2026), but the variables,
Japan panel, validity screen, and calculated shares are this project's own.

## Equation Set 2: Sparse Annual Entry Hazard

### Event construction

`Y_it = 1` only in the first fiscal year when a lineage reports `K_it > 0`
after an observed history with no installed generation. A lineage leaves the
risk set after that first event. Lineages already generating in their first
observed year are left-censored for entry and do not contribute a witnessed
first transition.

The event hierarchy is:

| Sample | Purpose | Current events |
|:--|:--|--:|
| Descriptive first-entry inventory | Retains all first positive reports for auditing and pathway description | 55 |
| Exact continuity-lineage model | Requires an adjacent-year transition in the same stable lineage and asset episode | 35 |
| Prior-operation subset | Additionally requires positive prior-year throughput | 33 |

The broad exact-year sample is primary because annual covariates should predict
an annual transition, not a change observed across an unknown multi-year gap.
The prior-operation and same-episode subsets ask whether the scale pattern
survives stricter operating and continuity definitions. They are nested
sensitivity frames, not separately identified retrofit populations.

### Model

The annual hazard is modeled as:

$$
\operatorname{logit}(h_{it}) =
\alpha
+ \beta_A\frac{A_{i,t-1}}{10}
+ \beta_C \log\left(1 + \frac{W_{i,t-1}}{100}\right)
+ \beta_T\frac{t-2014.5}{5}
+ \beta_R\log(1+R_{it}),
$$

where:

- `h_it = Pr(Y_it = 1 | Y_i,t-1 = 0, X_i,t-1)` is the conditional annual
  probability of first reported entry;
- age is measured per ten reported years;
- calendar time is centered and measured per five fiscal years; and
- `R_it` is elapsed observed time at risk.

Calendar terms absorb broad period differences in reporting and system context.
Duration terms address event dependence: a lineage's hazard may differ after
one year versus many years in the observed non-generating state. Neither set of
terms creates causal identification.

### Firth bias reduction

With only 35 exact events and 33 prior-operation events, ordinary maximum-
likelihood logit can have severe small-event bias or separation. The model uses
Firth's Jeffreys-prior penalized likelihood:

$$
\ell_F(\boldsymbol{\theta}) =
\ell(\boldsymbol{\theta})
+ \frac{1}{2}\log\left|\mathcal{I}(\boldsymbol{\theta})\right|,
$$

where `ell` is the ordinary binomial log-likelihood and `I(theta)` is the
expected information matrix. Firth (1993) provides the bias-reduction basis;
Heinze and Schemper (2002) explain its practical value when logistic-regression
data exhibit complete or quasi-complete separation. The method reduces first-
order maximum-likelihood bias and helps when covariates nearly separate rare
events. It does not add information, repair omitted variables, or transform an
observational hazard into a causal model.

The coefficient table labels fitted-model uncertainty as model-based. Primary
repeated-observation uncertainty uses 1,999 deterministic bootstrap replications
that resample whole stable lineages, preserving within-lineage dependence.
Predictors are centered and scaled internally for numerical stability, then
coefficients are returned to their original units. Every requested replication
must converge and return all focal coefficients; no failed draw is discarded.
The former 11-parameter age/calendar/risk-band model is retained only as a
sensitivity.

### Interpretable capacity contrast

Because waste-processing capacity is transformed, the reported contrast is not
the exponentiated coefficient for an arbitrary one-unit change. For 300 versus
100 t/day:

$$
OR_{300:100} =
\exp\left\{\beta
\left[\log(1 + 300/100) - \log(1 + 100/100)\right]\right\}.
$$

This gives 6.72 in the broad exact-year frame and 7.09 in the prior-operation
frame, with corresponding same-episode and identity-certain estimates of 7.15
and 6.76. These are conditional odds ratios, not risk ratios, predicted
probabilities, or benefit-cost estimates, and they cannot show what enlarging a
plant would cause.

### Four estimand and sensitivity frames

The broad exact-year model requires an adjacent-year lag in the same stable
administrative lineage but permits an inferred asset-episode change. It asks
about first administrative-lineage entry. Three specified sensitivities then
change one condition at a time:

1. The prior-operation frame requires positive prior-year throughput and
   contains 13,072 rows, 1,019 lineages, and 33 events.
2. The same-episode continuity frame excludes 59 cross-episode rows, including
   11 events, and contains 15,095 rows, 1,135 lineages, and 24 events.
3. The identity-certain frame excludes each lineage containing an accepted
   uncertain link and contains 15,107 rows, 1,130 lineages, and 35 events.

The broad frame contains 15,154 rows, 1,137 lineages, and 35 events. Its scale
contrast is 6.72 (bootstrap CI 4.31-12.46), and all event reclassifications or
whole-event-lineage deletions leave it between 6.12 and 7.30. The broad
continuous-age coefficient is -0.327 per decade (CI -0.774 to 0.070), compared
with -0.751 (CI -1.364 to -0.206) in the 24-event same-episode frame. This
divergence makes age continuity-sensitive. The nested prior-operation frame has
only two fewer events than the broad frame and is not treated as an independent
group or an equality test.

## Equation Set 3: Generator Engineering Components

### Why gross MWh/t needs decomposition

For positive-output generators, define:

$$
G_{it} = \frac{E_{it}}{Q_{it}}
\quad \text{(gross generation intensity, MWh/t)},
$$

$$
D_{it} = \frac{K_{it}}{W_{it}}
\quad \text{(generator design intensity, kW per t/day)},
$$

$$
F_{it} = \frac{E_{it}}{8.76K_{it}}
\quad \text{(electrical capacity factor)},
$$

and

$$
U_{it} = \frac{Q_{it}}{365W_{it}}
\quad \text{(waste-processing utilization)}.
$$

One kW operating continuously for 8,760 hours produces 8.76 MWh per year. These
definitions imply:

$$
G_{it} = \frac{8.76}{365}
\frac{D_{it}F_{it}}{U_{it}}.
$$

This identity is the key correction. Gross MWh/t is jointly structured by how
much electrical capacity is installed relative to waste-processing capacity,
how intensively that electrical capacity is used, and how much waste passes
through the denominator. It is therefore unsafe to label a regression of gross
MWh/t on plant age and utilization as an independent efficiency model while
omitting generator sizing.

### Engineering-valid sample

The component analysis uses 6,511 facility-year rows across 493 stable
administrative lineages. The screen applies specified plausible ranges to
gross MWh/t, electrical capacity factor, waste-processing utilization, generator
design intensity, and reported age. Invalid rows are excluded rather than
clipped into range. This limits obvious unit or reporting errors but does not
guarantee engineering measurement accuracy.

### Component models

Generator design intensity is modeled as:

$$
\log D_{it} =
\alpha_D
+ \boldsymbol{\kappa}_D'\text{Cohort}_i
+ \beta_D \log W_{it}
+ \boldsymbol{\eta}_D'Z_{it}
+ \tau_{Dt}
+ \varepsilon_{Dit}.
$$

Electrical capacity factor is modeled as:

$$
\log F_{it} =
\alpha_F
+ \boldsymbol{\kappa}_F'\text{Cohort}_i
+ \beta_F \log W_{it}
+ \gamma_F U_{it}
+ \boldsymbol{\eta}_F'Z_{it}
+ \tau_{Ft}
+ \varepsilon_{Fit}.
$$

`Cohort` is based on reported facility start year, not a verified turbine or
boiler commissioning year. `Z_it` contains the available coarse furnace and
facility configuration controls, including furnace count. Fiscal-year
indicators absorb common annual differences. Standard errors are clustered by
stable administrative lineage.

A direct gross-output check models:

$$
\log E_{it} =
\alpha_E
+ \eta_Q \log Q_{it}
+ \eta_K \log K_{it}
+ \boldsymbol{\kappa}_E'\text{Cohort}_i
+ \boldsymbol{\eta}_E'Z_{it}
+ \tau_{Et}
+ \varepsilon_{Eit}.
$$

These equations describe conditional panel associations. They do not estimate
the electricity gain from changing turbine size, throughput, or configuration.

### Omitted-sizing diagnostic

The former gross-intensity specification can be represented as:

$$
\log G_{it} =
\alpha + \beta_A A_{it} + \beta_W W_{it}
+ \beta_U U_{it} + \beta_H H_{it} + \boldsymbol{\eta}'Z_{it}
+ \tau_t + \epsilon_{it}.
$$

Here `H_it` is reported heating value. Both specifications use the same 5,806
engineering-valid rows with plausible heating value and explicitly control
heating value; this frame is distinct from the 6,511-row primary component
models. In the legacy model, age is -0.0349, waste-processing capacity is
+0.1001, and utilization is +0.6699 (all `p < 0.001`). The corrected diagnostic
adds `log D_it`; age becomes -0.0020 (`p = 0.2977`), capacity -0.0092
(`p = 0.1991`), utilization -0.0995 (`p = 0.2038`), and generator sizing is
+0.7532 (`p < 0.001`). Model fit rises from 0.4737 to 0.8131. This is evidence
that the earlier model omitted a central design component. It is a specification
diagnostic, not a causal mediation analysis, and the `R^2` change does not prove
that generator sizing is exogenous.

## Comparator And Method-Lineage Matrix

| Source | Idea or method adapted | How it appears here | What is deliberately different |
|:--|:--|:--|:--|
| Cui et al. (2026) | Facility hierarchy and decomposition: incinerators should not be treated as interchangeable units. | The Japan fleet is separated into participation, throughput coverage, conditional generator output, generator design intensity, and electrical capacity factor. | No Chinese plant or line data, optimization frontier, technical-potential simulation, or ranking on Cui et al.'s frontier is reproduced. |
| Liu et al. (2025) | Effectiveness should be distinguished from expansion alone. | Installed-capacity participation is not treated as sufficient; the paper separately measures waste-volume coverage and conditional generator components. | No urban waste-energy-carbon expansion model, scenario analysis, or causal evaluation of expansion is attempted. |
| Han et al. (2025) | Plant conclusions should acknowledge configuration and upgrade differences. | Available furnace type, facility type, and furnace count enter the generator models, and asset resets are not silently treated as unchanged equipment. | The Japan data do not support Han et al.'s pollutant-control, resource-recovery, or detailed upgrade-technology analysis. |
| Sasao (2018) | Japanese incinerators can be studied as an unbalanced plant panel rather than a national aggregate. | The current study uses a Japan facility-year panel and controls repeated observations at the reconstructed lineage level. | The outcome is first reported installed-capacity entry plus engineering components, not Sasao's heat/electricity Tobit production model or policy-effect specification. |
| Shino (2019) | Electricity generated per unit waste input is observable and useful, but thermal interpretation depends on calorific value and system boundaries. | Gross MWh/t is reported transparently and then decomposed; calorific-value plausibility is used as a caution and check. | Gross MWh/t is not called net efficiency, useful heat recovery, or a complete thermodynamic measure. |
| Chen et al. (2012) | Operating incinerators can be compared as heterogeneous multi-activity facilities. | Generator observations are compared only after positive output is observed, with configuration-aware panel models. | No network data-envelopment-analysis frontier, efficiency score, or Taiwan data are used. |
| Yeh (2020) | Electricity-related performance varies across operating incinerators and over time. | The generator layer studies repeated gross-output and component measures among operating generators. | No dynamic data-envelopment analysis, electricity-revenue inefficiency, price model, or Taiwan institutional result is transferred. |
| Allison (1982) | A transition observed in annual intervals can be modeled using discrete-time event-history data. | Each eligible lineage-year is a risk-set row; only the first observed entry is an event. | The application concerns first reported installed generation in a reconstructed Japanese administrative panel. |
| Beck, Katz, and Tucker (1998) | Binary time-series-cross-section analysis must account for temporal dependence. | Flexible elapsed-risk duration and calendar terms are included rather than treating all lineage-years as exchangeable. | The paper does not claim a general political-event model or rely on their exact application. |
| Firth (1993) | Jeffreys-prior penalization reduces first-order maximum-likelihood bias. | Firth logit is used because exact entry events are sparse and may approach separation. | Penalization is treated as an estimation safeguard, not a substitute for events, covariates, design, or causal identification. |
| Heinze and Schemper (2002) | Bias-reduced likelihood provides a practical response to complete or quasi-complete separation in logistic regression. | The sparse-entry rationale distinguishes separation control from substantive identification. | The paper does not treat estimator convergence as evidence that the event sample is large or unconfounded. |

## Detailed Intellectual Lineage

### Cui et al. (2026): hierarchy and decomposition

Cui et al. is the nearest conceptual comparator, not a template that this paper
replicates. The transferable insight is that national waste-incineration
performance emerges from a hierarchy of heterogeneous facilities and technical
configurations. That insight motivates two choices here.

First, the paper does not infer system coverage from a simple count of
generating plants. Facility share, waste-throughput share, and design-capacity
share are calculated separately. Second, gross MWh/t is not treated as a
primitive facility trait. It is decomposed into installed generator sizing,
electrical capacity factor, and waste loading.

The boundary is equally important. The present study does not use Cui et al.'s
data, optimization objective, technical frontier, plant ranking, or estimated
improvement potential. Its decomposition is an accounting and regression
framework built from the Japanese administrative variables actually observed.
The appropriate sentence is "inspired by facility-hierarchy logic," not "uses
Cui et al.'s model."

### Liu et al. (2025): effectiveness versus expansion

Liu et al. motivates a conceptual separation between adding or reporting
capacity and demonstrating effective system use. In this paper, the analogue
is intentionally modest. Installed electrical capacity establishes
participation; positive-output throughput coverage shows how much recorded
waste passes through operating generators; component measures show how the
generating segment is designed and loaded.

This is not Liu et al.'s China development framework. The paper does not model
urban expansion, carbon-system feedback, or future capacity scenarios. The
adaptation is the logic of not equating more capacity with more effective
service, not the data or estimator.

### Han et al. (2025): configuration-aware facility evidence

Han et al. demonstrates why configuration and upgrading matter when evaluating
incineration systems. The current paper applies the narrow lesson that facility
comparisons should condition on available technical configuration and should
not assume that a site history represents unchanged equipment. Coarse furnace
and facility controls enter the component models, while asset episodes mark
reported resets.

The available Japan panel lacks equivalent plant-level pollutant-control and
resource-recovery technology detail. Therefore, the paper cannot estimate the
environmental benefits of a specific upgrade bundle or compare control
technologies. Citing Han et al. supports configuration awareness, not an
emissions conclusion.

### Sasao (2018): the closest Japan panel predecessor

Sasao is essential because it prevents an inflated novelty claim. Sasao already
showed that Japanese plant-level heat and electricity production can be studied
with an unbalanced facility panel and related to policy, technology, and local
covariates. The present project inherits the plant-panel level of analysis.

It differs in four concrete ways. It reconstructs longitudinal administrative
lineages across code gaps and resets; defines a first positive installed-
capacity event among previously observed non-generators; separates facility
participation from throughput coverage; and decomposes generator output into
design intensity and electrical capacity factor. It does not replicate Sasao's
random-effects Tobit outcome, policy variables, or policy-effect interpretation.

The novelty claim should therefore be relational: the paper extends the Japan
facility-panel tradition to a corrected transition-and-component design. It
should never imply that no prior Japanese plant panel exists.

### Shino (2019): observable output and thermal caution

Shino supports using electricity generated per unit waste input as a transparent
administrative performance indicator. Shino also explains why interpretation
depends on calorific value and conversion boundaries. The current paper follows
both lessons.

Gross MWh/t is useful because the numerator and denominator are observed across
the panel. It remains a gross output ratio, not a net export or complete
efficiency measure. Heating value, own-use electricity, useful heat, steam
conditions, downtime, and waste composition can change the engineering meaning
of the same MWh/t. The component identity narrows the interpretation but does
not supply missing thermodynamic data.

### Chen et al. (2012) and Yeh (2020): post-entry comparison

Chen et al. and Yeh establish that incinerator performance is heterogeneous and
can be compared empirically after plants are operating. They motivate the
decision to analyze the generating segment separately rather than mix zeros
from non-generators into a continuous output model.

The estimator is different. Chen et al. uses multi-activity network data
envelopment analysis, and Yeh uses dynamic data envelopment analysis focused on
electricity-revenue inefficiency. The current paper uses observable engineering
ratios and regression diagnostics. It does not estimate an efficiency frontier,
revenue loss, or best-practice score.

### Allison (1982) and Beck et al. (1998): annual transition logic

Allison provides the foundation for representing annual event histories as
lineage-year risk rows. Beck et al. reinforces that repeated binary observations
have temporal dependence and should not be modeled as independent cross-
sections. These ideas justify the first-event risk set, lagged covariates,
elapsed-duration terms, and calendar controls.

The critical adaptation is to the administrative observation process. The event
is first reported installed capacity, not necessarily the physical decision or
commissioning date. Exact adjacent-year lineage continuity is required for the
primary model, while same-episode continuity is a stricter sensitivity.
Event-history structure improves timing discipline; it does not validate the
event's substantive mechanism.

### Firth (1993) and Heinze and Schemper (2002): sparse-event estimation

Firth bias reduction is an estimator-level adaptation. It addresses bias and
separation risk when only a small number of transitions is observed relative to
the covariate pattern. The paper implements the penalized likelihood directly,
reports interpretable capacity contrasts, uses a continuous age term in the
frozen primary model, and checks uncertainty by resampling stable lineages.

The two citations serve different roles. Firth (1993) establishes the
Jeffreys-prior bias-reduction method. Heinze and Schemper (2002) supports its
use as a solution to separation in logistic regression. Together they justify
the estimator choice, not the substantive event definition or covariate set.

The method should not be oversold. With 35 and 33 modeled events, precision is
inherently limited. Firth estimation can stabilize coefficients; it cannot make
the age result precise, reveal omitted investment determinants, or prove a
counterfactual effect of plant scale.

## Originality And Attribution Boundary

| Component | Intellectual source | Project-specific contribution |
|:--|:--|:--|
| Facility heterogeneity | Cui; Chen; Yeh; Han | Japan-specific fleet shares, stable-lineage data, component variables, and estimates |
| Effectiveness versus expansion | Liu | Separation of installed participation, positive-output throughput coverage, and generator components |
| Japan facility panel | Sasao; Shino | FY2005-FY2024 assembly, corrected identity layer, current outcomes, and current code |
| Annual first-event logic | Allison; Beck et al. | First reported positive-capacity event, exact continuity rule, and Japan risk sets |
| Sparse-event bias reduction and separation control | Firth; Heinze and Schemper | Implementation, stable-lineage bootstrap, contrasts, and current estimates |
| Post-entry comparison | Chen; Yeh | Regression-based engineering decomposition rather than a DEA frontier |
| Configuration awareness | Han | Available Japanese furnace/facility controls and separate asset episodes |

The paper's originality rests on the combination and application, not on
claiming ownership of standard methods. The following are original project
outputs:

- the cleaned 23,593-record analytical panel;
- the 1,690 stable administrative lineages and 1,767 asset episodes;
- the first-reported-capacity event and nested continuity samples;
- the FY2024 count-volume-capacity decomposition;
- the generator design-intensity and electrical-capacity-factor construction;
- the model code, diagnostics, robustness checks, figures, tables, and prose;
- the numerical results reported in this packet.

Transparent citation is the protection against both plagiarism and exaggerated
novelty. A method can be adapted legitimately when its source is cited, its
scope is described accurately, and the new data, estimand, implementation, and
results are distinguishable. That is the intended standard here.

## Identification And Interpretation Limits

### Limits common to all three layers

- The data are observational administrative records.
- Reporting accuracy and definitions may vary over time and across facilities.
- Stable-lineage matching is audited but not externally verified for every site.
- Available controls do not capture all municipal finances, contracts, policy
  incentives, grid conditions, waste composition, or engineering constraints.
- Standard errors and bootstrap intervals address sampling dependence under the
  model; they do not address all measurement or linkage uncertainty.

### Limits specific to fleet coverage

- Facility, throughput, and design-capacity shares are descriptive accounting
  measures.
- Positive gross output does not show net export, useful heat, avoided
  emissions, or economic efficiency.
- A throughput-weighted result gives more influence to large facilities by
  design. It answers a system-volume question, not an equity or local-impact
  question.

### Limits specific to first entry

- Entry means first positive reported installed capacity within the observed
  window.
- Already-generating first observations are left-censored and cannot reveal
  their entry timing.
- Thirty-five exact events constrain model complexity and precision.
- Prior waste-processing capacity may proxy for unobserved urban scale,
  financing ability, technology, waste contracts, or project feasibility.
- The 6.72 broad-frame odds ratio does not imply that increasing a plant from
  100 to 300 t/day would multiply its entry probability by that value.
- The broad age interval spans zero, while the same-episode estimate does not;
  this is continuity-sensitive evidence, not proof that age always matters.

### Limits specific to generator components

- `K_it` is reported installed electrical capacity, not independently verified
  turbine capability.
- Reported start-year cohort is not the installation date of each generator,
  boiler, or control system.
- Gross MWh/t is sensitive to the waste denominator and does not include useful
  heat or plant own-use electricity.
- Electrical capacity factor summarizes annual use of reported electrical
  capacity; it does not isolate downtime, dispatch, fuel quality, or conversion
  technology.
- The `R^2` increase diagnoses omitted generator sizing but does not establish a
  causal channel.
- Conditioning on positive-output generators creates a selected post-entry
  population; results do not automatically generalize to non-generators.

## What A Professor Should Challenge

The most useful supervision is not a request for stronger wording. It is a test
of whether each estimand answers a worthwhile and supportable question.

1. **Identity validity:** Are the linkage evidence and asset-episode reset rules
   convincing enough for the 35 exact events and lineage-clustered models?
2. **Event meaning:** Should the paper call the outcome "first reported
   installed-capacity entry" throughout, or can any events be externally
   verified as commissioning or retrofit projects?
3. **Risk-set eligibility:** Is the observed non-generating history long enough
   to make the event meaningful, and should a minimum pre-event history be a
   sensitivity check?
4. **Sparse-event complexity:** Is the frozen five-parameter model parsimonious
   enough for 35 and 33 events, and is the older 11-parameter model properly
   confined to sensitivity analysis?
5. **Capacity functional form:** Does `log(1 + W/100)` adequately represent
   scale, or should splines or prespecified categories be shown descriptively?
6. **Confounding:** Which municipal finance, population, policy, or waste-flow
   variables would most plausibly explain both processing scale and generation
   entry?
7. **Count-volume contribution:** Is the 41.1% versus 80.1% contrast framed as a
   correction to system interpretation rather than as evidence that the
   non-generating segment is unimportant?
8. **Component identity:** Are the units and the factor `8.76/365` communicated
   clearly enough that a reader can reproduce the decomposition?
9. **Configuration adequacy:** Are the available furnace and facility controls
   sufficient for descriptive comparison, and are their missing categories
   documented?
10. **Outcome language:** Does every use of "performance" specify gross output,
    generator design intensity, or electrical capacity factor rather than imply
    complete technical efficiency?
11. **Age interpretation:** Has every old claim of an independent adverse age
    association been removed after the sizing diagnostic?
12. **External validity:** Does the administrative fleet represent the intended
    policy population, and what facilities or energy pathways remain outside
    the data?
13. **Mechanism evidence:** Which proposed explanation is directly measured,
    which is consistent with the pattern, and which is speculation?
14. **Scope discipline:** Would the paper become clearer if post-entry pathway
    description remained supplemental rather than carrying a separate causal
    claim?

If these challenges cannot be answered with current evidence, the correct
response is to narrow the claim or collect new data, not to add stronger
rhetoric.

## Pivot Options

### Option A: Retain the corrected three-layer diagnostic

**Recommended with current data.** Keep RQ1 as the count-volume accounting
result, RQ2 as a sparse first-reported-entry hazard, and RQ3 as an engineering
component decomposition. Center the paper on scale selectivity and omitted
generator sizing. Treat all results as descriptive or associational.

This option is the most defensible because it matches the information content
of the current panel. Its limitation is that mechanisms remain unresolved.

### Option B: Build an externally validated entry-project sample

Collect facility histories, procurement notices, permits, subsidy records,
operator reports, and equipment commissioning dates for the 55 descriptive
events. Reclassify each event as verified new facility, rebuild, retrofit,
administrative recode, delayed reporting, or unresolved.

This would strengthen event meaning and may support pathway-specific analysis.
It would likely reduce the usable sample and should be pursued for validity,
not to force statistical significance.

### Option C: Add municipal decision determinants

Link population served, municipal fiscal capacity, intermunicipal cooperation,
waste contracts, electricity prices, subsidies, and policy eligibility to the
risk set. This could test why processing scale predicts entry rather than
treating scale itself as the mechanism.

This option requires careful temporal alignment and a prespecified causal
diagram. Adding contemporaneous controls without a decision model could create
post-treatment or collider bias.

### Option D: Move toward a causal policy design

Identify a policy rule, funding threshold, phased eligibility change, or other
plausibly exogenous source of variation. Then define treatment timing,
comparison units, anticipation, and outcome windows before estimation.

No such design is established by the current paper. This pivot should occur
only if institutional evidence supports the identifying assumptions.

### Option E: Move toward a full engineering-performance paper

Collect net electricity export, own-use demand, useful heat, lower heating
value, steam conditions, turbine and boiler specifications, downtime, and
waste composition. These data could support net-efficiency or exergy-oriented
questions that gross administrative MWh/t cannot answer.

This would be a different empirical paper. It should not be simulated by
renaming the current gross-output ratio.

## Recommended Decision Sequence

1. Validate the stable-lineage and asset-episode assignments for all 55
   descriptive events.
2. Ask whether external project records can classify enough events to justify
   Option B.
3. If not, retain Option A and keep the event interpretation explicitly
   administrative.
4. Decide whether municipal determinants can be obtained with valid prior-year
   timing before adding them.
5. Keep the generator component identity regardless of pivot; it prevents a
   return to the misspecified age-performance model.
6. Add a causal or engineering claim only after the corresponding new data and
   identification assumptions exist.

## Defense-Ready Questions And Answers

### "Isn't it obvious that larger facilities are more likely to generate?"

The direction may be intuitive, but the paper's contribution is not the slogan
"large plants generate." It constructs a valid annual risk set through unstable
administrative identifiers, quantifies the scale gradient under rare-event
bias reduction, shows that the contrast persists in the prior-operation subset,
and separates this entry pattern from the amount of waste handled by generators.
The result remains an association and should be presented as such.

### "What is new relative to Sasao?"

Sasao is the closest Japan panel predecessor and must be acknowledged. The
current paper adds longitudinal identity reconstruction across code breaks, a
first-reported installed-capacity risk set, separate count and throughput
coverage, and an engineering decomposition of gross MWh/t. It does not claim to
replace or reproduce Sasao's production model.

### "Did this paper copy Cui et al.?"

No. Cui et al. supplies the high-level insight that heterogeneous facilities
form a performance hierarchy that should be decomposed. This project uses a
different national dataset, reconstructed administrative identities, different
outcomes, different equations, and independently written code. It does not use
Cui et al.'s optimization model, frontier, data, numerical results, text, or
figures. The conceptual adaptation is stated and cited.

### "Why use Firth logit?"

The exact models contain 35 and 33 events. In sparse binary data, ordinary
maximum-likelihood logit can be biased or fail under separation. Firth's
penalized likelihood reduces that bias and stabilizes estimation. It does not
solve confounding or make the estimates causal.

### "Why not claim that age prevents entry?"

The broad continuous-age estimate is -0.327 per decade, but its bootstrap
interval spans zero (-0.774 to 0.070). The 24-event same-episode estimate is
more negative and its interval excludes zero. That contrast is evidence that
the age result depends on how physical continuity is approximated. The
defensible headline is scale selectivity, not a universal age barrier.

### "Why did the earlier age-performance result disappear?"

Gross MWh/t mechanically combines generator sizing, electrical loading, and
waste loading. The earlier model omitted generator design intensity. Adding it
in a separate 5,806-row plausible-heating-value frame that controls heating
value raises `R^2` from 0.4737 to 0.8131. Legacy age, capacity, and utilization
estimates of -0.0349, +0.1001, and +0.6699 become -0.0020 (`p = 0.2977`),
-0.0092 (`p = 0.1991`), and -0.0995 (`p = 0.2038`), while sizing is +0.7532
(`p < 0.001`). This specification diagnostic is distinct from the 6,511-row
primary component models and is not causal mediation. The correction is a
strength because it removes a misleading interpretation.

### "Why not call MWh/t efficiency?"

Gross MWh/t does not account for net export, plant own-use electricity, useful
heat, heating value, steam conditions, or lifecycle impacts. Shino supports its
use as an observable per-input indicator while warning about thermal
interpretation. The paper therefore calls it gross generation intensity and
decomposes it rather than relabeling it.

### "Do the 41.1% and 80.1% figures contradict each other?"

No. They use different denominators. The first is a facility-count share based
on installed capacity. The second is a throughput-weighted share based on
positive-output facilities. Their difference shows that generation is
concentrated in larger-throughput facilities.

### "What would most improve confidence in the paper?"

External validation of the 55 first-entry records would have the highest
immediate value. It would test the administrative event definition and clarify
which entries represent continuing-site installations, replacements, new
facilities, delayed reports, or recodes.

## Language Control For The Manuscript

### Preferred terms

- stable administrative lineage
- asset episode
- first reported installed-generation-capacity entry
- waste-processing design capacity
- installed electrical-generation capacity
- positive-output generator
- gross generation intensity (MWh/t)
- generator design intensity (kW per t/day)
- electrical capacity factor
- conditional association
- descriptive accounting identity

### Terms requiring qualification or removal

- "facility identity" without "administrative" or a linkage caveat
- "adoption" without explaining that the event is first reported capacity
- "retrofit" unless externally verified
- "efficiency" when the measure is gross MWh/t
- "age coefficient" without stating that the estimate is observational or not independently
  significant after sizing
- "utilization coefficient" when generator sizing is omitted
- "closure" inferred from record disappearance
- Do not use "caused," "led to," "increased," or "reduced" for the current regressions

## Professor Sign-Off Checklist

- [ ] The three research questions are distinct and each has one defined
  estimand.
- [ ] The 23,593 records, 1,690 stable administrative lineages, and 1,767 asset
  episodes are used consistently.
- [ ] The FY2024 figures always appear as 41.1% facility participation, 80.1%
  positive-output throughput coverage, and 70.5% installed-generation share of
  waste-processing design capacity.
- [ ] The event hierarchy is 55 descriptive, 35 broad exact-year, 33
  prior-operation, and 24 same-episode events; identity-certain retains 35.
- [ ] The scale contrasts are 6.72 broad, 7.09 prior-operation, 7.15
  same-episode, and 6.76 identity-certain, with a 6.12-7.30 event-attack range.
- [ ] The broad age coefficient is -0.327 per decade (CI -0.774 to 0.070),
  compared with -0.751 (-1.364 to -0.206) in the 24-event same-episode frame.
- [ ] The generator frame is 6,511 rows across 493 stable administrative
  lineages.
- [ ] Installed-kW elasticity is 1.532, and cohort contrasts separately report
  installed capacity (79.1%, 58.6%, 23.5% lower) and capacity factor (35.3%,
  22.0%, 1.5% higher).
- [ ] The separate sizing diagnostic uses 5,806 engineering-valid rows with
  plausible heating value and explicitly controls heating value.
- [ ] Legacy age -0.0349, capacity +0.1001, and utilization +0.6699 become age
  -0.0020 (`p = 0.2977`), capacity -0.0092 (`p = 0.1991`), and utilization
  -0.0995 (`p = 0.2038`) after sizing; sizing is +0.7532 (`p < 0.001`).
- [ ] The `R^2` change from 0.4737 to 0.8131 is called a specification
  diagnostic, not causal mediation.
- [ ] Age and waste-processing utilization are not described as independent
  gross-intensity drivers after generator sizing is included.
- [ ] Cui, Liu, Han, Sasao, Shino, Chen, Yeh, Allison, Beck et al., and Firth are
  cited for the specific ideas actually adapted; Heinze and Schemper are cited
  specifically for the separation rationale.
- [ ] No comparator's data, estimator, result, wording, table, figure, or code is
  represented as this project's own.
- [ ] Gross MWh/t is never presented as net export, useful heat, complete
  thermodynamic efficiency, or lifecycle benefit.

## References Central To This Lineage

- Allison, P. D. (1982). Discrete-time methods for the analysis of event
  histories. *Sociological Methodology*, *13*, 61-98.
  https://doi.org/10.2307/270718
- Beck, N., Katz, J. N., & Tucker, R. (1998). Taking time seriously:
  Time-series-cross-section analysis with a binary dependent variable.
  *American Journal of Political Science*, *42*(4), 1260-1288.
  https://doi.org/10.2307/2991857
- Chen, P.-C., Chang, C.-C., Yu, M.-M., & Hsu, S.-H. (2012). Performance
  measurement for incineration plants using multi-activity network data
  envelopment analysis: The case of Taiwan. *Journal of Environmental
  Management*, *93*(1), 95-103.
  https://doi.org/10.1016/j.jenvman.2011.08.011
- Cui, J., Cui, Y., Li, J., Gao, X., Wei, W., Chen, Y., Ma, W., Zhu, N., Geng,
  Y., Zhao, Y., & Lou, Z. (2026). Efficiency hierarchy and optimization of
  waste incineration in China to balance disposal and energy supply. *Nature
  Communications*, *17*(1), Article 3069.
  https://doi.org/10.1038/s41467-026-69897-w
- Firth, D. (1993). Bias reduction of maximum likelihood estimates.
  *Biometrika*, *80*(1), 27-38. https://doi.org/10.1093/biomet/80.1.27
- Han, Q.-l., Liu, H.-q., Gong, Y.-y., Tao, J.-y., Sun, Y.-n., Wei, G.-x., Zhu,
  Y.-w., & Chen, G.-y. (2025). Strengthening pollutant control and resource
  recovery can enhance sustainable waste incineration in China.
  *Communications Earth & Environment*, *6*, Article 863.
  https://doi.org/10.1038/s43247-025-02859-0
- Heinze, G., & Schemper, M. (2002). A solution to the problem of separation in
  logistic regression. *Statistics in Medicine*, *21*(16), 2409-2419.
  https://doi.org/10.1002/sim.1047
- Liu, B., Wang, P., Zhou, J., Guo, Y., Ma, S., Chen, W.-Q., Li, J., & Chang,
  V. W.-C. (2025). Refocusing on effectiveness over expansion in urban
  waste-energy-carbon development in China. *Nature Energy*, *10*, 215-225.
  https://doi.org/10.1038/s41560-024-01683-8
- Sasao, T. (2018). How does municipal solid waste policy affect heat and
  electricity produced by incinerators? *Detritus*, *2*, 133-141.
  https://doi.org/10.31025/2611-4135/2018.13650
- Shino, Y. (2019). System analysis of MSW incinerator power generation
  performance. *Journal of the Japan Society of Material Cycles and Waste
  Management*, *30*, 113-121. https://doi.org/10.3985/jjsmcwm.30.113
- Yeh, L.-T. (2020). Analysis of the dynamic electricity revenue inefficiencies
  of Taiwan's municipal solid waste incineration plants using data envelopment
  analysis. *Waste Management*, *107*, 28-35.
  https://doi.org/10.1016/j.wasman.2020.03.040

## Bottom Line For Supervision

The strongest current paper is not a claim that older incinerators are
inefficient or that a particular policy caused generation entry. It is a
carefully bounded facility-panel diagnosis:

> Generating facilities are a minority by count but handle most recorded waste
> throughput; first reported entry is strongly concentrated among larger
> processing lineages; and gross MWh/t differences are primarily interpretable
> only after generator sizing is separated from annual electrical and waste
> loading.

That argument is useful if its administrative event definition, observational
limits, and engineering boundaries remain explicit. The next substantive gain
would come from validating entry projects or adding correctly timed decision
determinants, not from restoring discarded age claims or adding more complex
models to the same sparse events.
