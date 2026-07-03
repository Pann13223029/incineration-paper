# Professor Comparator And Method-Lineage Packet

Last updated: 2026-07-03

## Purpose

This note is designed for a supervisor or professor who wants to understand
where the paper comes from intellectually, which papers inspired it, which
methods it adapts, and how to give targeted feedback on the next direction.

The short answer is:

> The paper is inspired substantively by recent facility-level
> waste-to-energy and incineration-efficiency papers, especially Cui et al.
> (2026) and Liu et al. (2025), but its actual empirical method is a simpler
> and more defensible two-margin facility-panel design: a discrete-time
> adoption hazard for entry into power generation, followed by panel
> regressions for electricity recovered per tonne among generators.

## 2026-06-14 Method Hardening Note

A red-team methods review identified that FY2010-FY2012 source rows lack
official facility codes, which can turn a naive `shift(1)` lag into the
previous observed coded row rather than the previous fiscal year. The paper now
uses the stricter version as the main adoption model:

| Item | Current treatment |
|:--|:--|
| Main adoption model | Exact one-fiscal-year lagged discrete-time logit hazard |
| Main adoption frame | 10,823 observations, 1,911 facilities, 98 events |
| Sensitivity frame | Broader previous-observed-coded-row model: 11,717 observations, 1,915 facilities, 140 events |
| Non-exact lag rows | 894 rows and 42 events excluded from the main adoption model |
| Pathway audit | Strong mechanism labels kept only for adjacent-year events; non-adjacent events are timing-ambiguous |
| Generator panel | FY2010-FY2012 missing-code rows are disclosed; period checks are early/later coded-window diagnostics, not Fukushima causal tests |

This strengthens the paper's integrity position. The paper is still inspired by
high-profile facility-level waste-incineration papers, but its empirical claims
now rest on a stricter Japan-specific administrative-panel design rather than a
loose analogy to those papers.

## 2026-07-03 Sparse-Event Adoption Specification Note

A later methods pass tightened the main adoption model again. The exact-year
frame has 98 retained first-adoption events. A saturated model with both fiscal
year and prefecture fixed effects estimates 64 parameters, or 1.53 events per
parameter. That model is now retained as sensitivity evidence rather than used
as the primary estimate.

The main manuscript now uses a more parsimonious exact-year logit hazard with
fiscal-year fixed effects and facility-clustered standard errors as the primary
adoption model. This specification estimates 18 parameters, or 5.44 events per
parameter, while preserving annual transition timing. The professor-facing
interpretation should therefore be:

> The paper borrows established discrete-time event-history logic, but it keeps
> the main adoption model parsimonious because the event count is modest. The
> more saturated year-plus-prefecture model supports robustness of the sign
> pattern, not the headline estimate.

## 2026-07-03 Citation-Fit Check

A citation-fit pass checked whether the main manuscript's method and comparator
citations support the claims placed near them. The main local finding was that
all core method claims have nearby references: Allison (1982) and Beck et al.
(1998) support the discrete-time event-history layer, Chen et al. (2012) and
Yeh (2020) support facility-level incinerator performance comparison, and
Wooldridge (2010) supports the panel-regression framing.

The recent high-profile comparator DOIs were also checked against Crossref:
Cui et al. (2026), Liu et al. (2025), and Han et al. (2025) resolve to the
expected Nature-family articles. The Münster and Meibom (2010) reference title
was corrected to the Crossref title. No additional citation was needed for the
new methods-positioning paragraph because it reuses already-cited method and
facility-performance sources.

The paper does not copy one single paper. It combines three research families:

1. Waste-to-energy performance and efficiency studies.
2. Event-history or transition modeling for observed entry into a new state.
3. Panel regression for facility-level performance differences over time.

The contribution is not "we use the same method as Cui et al." The better
claim is:

> High-profile incineration papers show that facility-level hierarchy matters.
> This paper adds a Japan-specific two-margin design: it separates who enters
> electricity generation from how well generators perform after entry.

## How The Professor Should Use This Packet

Use this packet before commenting on the manuscript. It answers four questions:

1. Which papers are closest to this paper?
2. Which methods are borrowed or adapted?
3. What is genuinely different about this paper?
4. What feedback would be most useful before the paper is reframed?

Recommended reading order for a busy supervisor:

1. Read Section 1 of this packet: "One-page positioning summary."
2. Read Section 2: "Comparator map."
3. Read Section 4: "Method lineage."
4. Skim Section 7: "What feedback we need from the professor."

If the professor has more time, read Section 5 and Section 6 for the
paper-by-paper explanation.

## 1. One-Page Positioning Summary

### What This Paper Is

This paper is a facility-level empirical study of Japan's municipal
waste-incineration fleet from FY2005 to FY2024. It asks two linked questions:

1. Which non-generating facilities first report power generation?
2. Among facilities that already generate electricity, how much electricity is
   recovered per tonne of waste processed?

This is a two-margin paper:

| Margin | Plain question | Method | Main result |
|:--|:--|:--|:--|
| Adoption margin | Which plants enter power generation? | Lagged discrete-time logit hazard | Entry is selective toward younger and larger facilities |
| Performance margin | How well do generators perform after entry? | Panel regressions of logged MWh/t | Electricity recovered per tonne is lower at older plants and higher at larger, more utilized plants |
| Synthesis | Does one fleet average hide the bottleneck? | Interpret both margins together | Non-generators and existing generators should not be managed as one average segment |

### What This Paper Is Inspired By

The paper is mainly inspired by high-quality studies that treat incineration
plants as heterogeneous facilities rather than as one national average.

The closest inspiration papers are:

| Paper | Why it matters for this paper |
|:--|:--|
| Cui et al. (2026), Nature Communications | Shows that facility-level hierarchy and optimization matter in waste incineration |
| Liu et al. (2025), Nature Energy | Shows that waste-energy systems should be judged by effectiveness, not only expansion |
| Chen et al. (2012), Journal of Environmental Management | Shows how facility-level incinerator performance can be studied empirically |
| Yeh (2020), Waste Management | Shows that electricity-related incinerator performance can be decomposed across facilities |
| Grosso et al. (2010), Waste Management | Provides energy-recovery-efficiency framing for waste incineration |
| Allison (1982) and Beck et al. (1998) | Provide the event-history logic behind the adoption model |
| Wooldridge (2010) | Provides the panel-regression logic behind the performance models |

### What This Paper Does Differently

Most comparator papers start from operating generators or energy-recovery
systems. They ask how existing incinerators perform. This paper adds the
non-generator problem.

That matters because a fleet can fail in two different ways:

1. Many plants may not generate electricity at all.
2. Plants that do generate may still recover electricity unevenly.

The key difference is therefore not a more complex estimator. It is the
analytical split.

### Best One-Sentence Framing For The Professor

> This paper adapts facility-level waste-to-energy performance logic from the
> incineration-efficiency literature, but reframes the Japan case as a
> two-margin transition problem: selective entry into power generation and
> bounded performance among generators.

## 2. Comparator Map

### A. Closest High-Profile Substantive Comparators

| Comparator | Journal/status | What it studies | What we take from it | What we do differently |
|:--|:--|:--|:--|:--|
| Cui et al. (2026) | Nature Communications | China-wide waste-incineration efficiency hierarchy and optimization | Facility-level hierarchy, technical heterogeneity, performance classification | We do not build a technical optimization model; we study Japan's administrative panel and include non-generators |
| Liu et al. (2025) | Nature Energy | Waste-energy-carbon development in China, emphasizing effectiveness over expansion | Framing that capacity expansion alone is not enough | We use plant-level Japan data and distinguish entry from conditional performance |
| Han et al. (2025) | Communications Earth & Environment | Pollutant control and resource recovery in China's incineration system | System-level sustainability and upgrade framing | We do not model emissions-control technology directly because the Japan panel does not include equivalent technical detail |

### B. Closest Facility-Performance Papers

| Comparator | Journal | Method family | What we take from it | What we do differently |
|:--|:--|:--|:--|:--|
| Chen et al. (2012) | Journal of Environmental Management | Network DEA for Taiwan incinerators | Incinerators can be compared as multi-activity facilities | We use regression and panel structure, not DEA |
| Yeh (2020) | Waste Management | Dynamic DEA/electricity revenue inefficiency | Electricity-related incinerator performance can be decomposed | We use MWh/t, not electricity revenue inefficiency |
| Grosso et al. (2010) | Waste Management | Energy-recovery performance criteria | Energy recovery is a meaningful performance dimension | We use administrative MWh/t, not a full R1-style engineering efficiency standard |
| Münster and Meibom (2010) | Waste Management | Energy-system consequences of waste-to-energy | WTE performance depends on energy-system context | We control for grid emissions but do not run an energy-system optimization model |

### C. Closest Japan/System-Context Papers

| Comparator | Role in this paper | Why professor should know it |
|:--|:--|:--|
| Tabata and Tsai (2016) | Japan heat-supply and WTE context | Helps explain why energy recovery in Japan has practical constraints |
| Uno (2015) | Japan high-efficiency WTE technology trends | Helps connect the empirical pattern to Japanese technology discussions |
| Yamada et al. (2023) | Japan waste-sector net-zero scenarios | Helps justify why energy recovery matters for decarbonization planning |
| Sakai et al. (2011) | Comparative waste-policy context | Keeps the paper inside waste hierarchy and 3R policy thinking |
| European Commission (2017) | Circular-economy policy context | Prevents overclaiming that WTE is automatically good outside a waste hierarchy |

### D. Closest Methods References

| Method source | Method idea | Where it appears in our paper |
|:--|:--|:--|
| Allison (1982) | Discrete-time event-history modeling | Adoption hazard for first observed generation |
| Beck, Katz, and Tucker (1998) | Binary time-series-cross-section/event dependence logic | Robustness logic for transition modeling |
| Wooldridge (2010) | Panel regression, clustered SEs, FE/RE logic | Performance regressions among generators |

## 3. The Core Intellectual Lineage

The paper should be explained as a combination of these research lines:

### Line 1: Facility-Level Waste-To-Energy Performance

This line asks:

> How different are incinerators from each other once they are operating?

Representative papers:

- Cui et al. (2026)
- Chen et al. (2012)
- Yeh (2020)
- Grosso et al. (2010)

How our paper uses this line:

- We use the idea that incinerators are not interchangeable units.
- We compare electricity recovered per tonne among operating generators.
- We interpret age, capacity, and utilization as facility-structure variables.

What we do not take:

- We do not use DEA.
- We do not estimate an engineering frontier.
- We do not estimate technical optimization pathways.
- We do not claim to classify each plant into a full technology-efficiency
  hierarchy like Cui et al.

### Line 2: Transition / Adoption / Event-History Modeling

This line asks:

> When does a unit move from one state to another?

Representative papers:

- Allison (1982)
- Beck, Katz, and Tucker (1998)

How our paper uses this line:

- A non-generator enters the risk set.
- Each facility-year is observed until the facility first reports generation.
- The dependent variable is first observed adoption of generation.
- Predictors are lagged so that age and capacity are measured before the event.

What we do not take:

- We do not claim to identify the physical retrofit mechanism.
- We do not claim that observed reporting equals confirmed engineering
  conversion.
- We do not estimate a policy-shock treatment effect.

### Line 3: Panel Regression For Structured Facility Differences

This line asks:

> How do repeated observations of the same facility help describe performance?

Representative source:

- Wooldridge (2010)

How our paper uses this line:

- We estimate pooled OLS, year fixed effects, random effects, and year fixed
  effects plus random effects.
- We use facility-clustered standard errors.
- We interpret coefficients as structured conditional associations.

What we do not take:

- We do not treat the random-effects model as causal proof.
- We do not claim facility age is randomly assigned.
- We do not claim that changing a plant's age, capacity, or utilization by
  policy would mechanically reproduce the coefficient.

### Line 4: Infrastructure Lock-In And Municipal Governance

This line asks:

> Why might old infrastructure remain stratified rather than converge quickly?

Representative papers:

- Unruh (2000)
- Geels (2004)
- Seto et al. (2016)
- Rausch (2006)
- Sakai et al. (2008, 2011)

How our paper uses this line:

- It interprets persistent age and scale hierarchy as a plausible
  infrastructure pattern.
- It connects facility differences to municipal planning and asset renewal.

What we do not take:

- We do not prove carbon lock-in causally.
- We do not estimate municipal political mechanisms directly.
- We do not claim every old plant is technically impossible to upgrade.

## 4. Method Lineage In More Detail

### 4.1 Adoption Model

The adoption model is inspired by event-history analysis. The empirical
question is:

> Among facilities that are still non-generating, which ones first report power
> generation in the next observed fiscal year?

Main equation:

```text
Pr(A_it = 1 | R_it = 1)
  = logit^{-1}[
      alpha
      + beta_1 I(Age_i,t-1 = 10-20)
      + beta_2 I(Age_i,t-1 = 20-30)
      + beta_3 I(Age_i,t-1 >= 30)
      + beta_4 Capacity100_i,t-1
      + gamma_t
      + delta_p
    ]
```

Where:

| Symbol | Meaning |
|:--|:--|
| `A_it` | First observed report of power generation for facility `i` in fiscal year `t` |
| `R_it` | Facility is still at risk of first adoption |
| `Age_i,t-1` | Prior-year facility age band |
| `Capacity100_i,t-1` | Prior-year design capacity in 100 t/day units |
| `gamma_t` | Fiscal-year fixed effects |
| `delta_p` | Prefecture fixed effects |

Why this method is appropriate:

- The outcome is binary: a facility either first reports generation or does
  not.
- The data are observed annually, not continuously.
- Facilities can only have one first adoption event.
- A discrete-time hazard naturally represents annual first-entry probability.

What professor may ask:

- Should the model include a separate time-at-risk duration term?
- Are year fixed effects sufficient for temporal dependence?
- Should the main model be logit, complementary log-log, or linear probability?
- Should the adoption event be called "observed generation entry" rather than
  "adoption" to avoid overclaiming?

Current answer:

- The current model is defensible as a diagnostic transition model.
- It uses year fixed effects and lagged predictors.
- The supplement reports alternative event-model checks.
- But a duration/time-at-risk robustness check could strengthen the
  event-history lineage if the professor thinks reviewers will ask for it.

### 4.2 Electricity-Recovery Model

The performance model is inspired by facility-level efficiency and panel-data
studies. The empirical question is:

> Among identifiable operating generators, how does electricity recovered per
> tonne vary with age, scale, utilization, heating value, and grid context?

Outcome construction:

```text
raw electricity recovery = MWh generated / tonnes processed
clipped recovery         = clip(raw recovery, 0.01, 0.80)
y_it                     = log(clipped recovery)
```

Main equation:

```text
y_it = alpha + X_it' beta + gamma_t + u_i + epsilon_it
```

Where:

| Term | Meaning |
|:--|:--|
| `y_it` | Log electricity recovered per tonne |
| `X_it` | Age, capacity, utilization, heating value, grid EF |
| `gamma_t` | Fiscal-year fixed effects |
| `u_i` | Facility-specific random intercept |
| `epsilon_it` | Idiosyncratic error term |

Reported specifications:

| Model | Terms included | Why included |
|:--|:--|:--|
| Pooled OLS | `X_it` | Baseline cross-facility comparison |
| Year FE | `X_it + gamma_t` | Adjusts for common fiscal-year shocks |
| RE | `X_it + u_i` | Summarizes persistent facility-level differences |
| Year FE + RE | `X_it + gamma_t + u_i` | Combines year adjustment and facility heterogeneity |

Why this method is appropriate:

- The paper is not estimating a frontier.
- The paper asks whether observable facility characteristics structure
  electricity recovery.
- Panel regressions are transparent and easy for reviewers to audit.
- Facility-clustered standard errors account for repeated observations.

Why this is not DEA:

- DEA is useful for frontier performance measurement.
- This paper's main contribution is not frontier ranking.
- DEA would not solve the entry-margin question.
- DEA would also require careful decisions about inputs, outputs, undesirable
  outputs, and technology assumptions.
- A DEA extension could be a future side paper, not the cleanest current
  thesis-to-paper path.

Why this is not causal:

- Facility age is not randomly assigned.
- Capacity reflects long-term design decisions.
- Utilization may reflect waste routing, municipal demand, and operations.
- Random effects summarize persistent differences but do not prove exogeneity.

Best wording:

> The coefficients are structured conditional associations within the
> identifiable generator frame, not causal estimates of what would happen if a
> plant's age or capacity were changed by policy.

## 5. Paper-By-Paper Comparator Explanation

### 5.1 Cui et al. (2026), Nature Communications

Full citation:

> Cui, J., Cui, Y., Li, J., Gao, X., Wei, W., Chen, Y., Ma, W., Zhu, N.,
> Geng, Y., Zhao, Y., and Lou, Z. (2026). Efficiency hierarchy and optimization
> of waste incineration in China to balance disposal and energy supply.
> Nature Communications, 17(1), Article 3069.
> https://doi.org/10.1038/s41467-026-69897-w

Why it is important:

- This is the strongest high-profile comparator.
- It shows how an incineration paper can be elevated beyond a local case study.
- It treats incineration facilities as heterogeneous assets.
- It links efficiency hierarchy to optimization and system planning.

What we take from it:

- Facility-level hierarchy matters.
- Incinerators should not be summarized only by national totals.
- Energy recovery is a performance dimension, not just a yes/no technology
  label.
- High-profile papers make a broader planning argument from facility-level
  evidence.

What we do not take:

- We do not build a comprehensive technical database of incineration lines.
- We do not model detailed furnace design, flue-gas systems, or technology
  packages.
- We do not estimate optimization measures.
- We do not claim the same level of engineering mechanism identification.

How to explain our difference:

> Cui et al. show what high-profile facility-level waste-incineration
> performance research can look like when detailed technical data are
> available. Our Japan paper works with a different data structure: a national
> administrative facility panel. That allows us to study adoption and
> performance over time, including non-generators, but not to reproduce a full
> engineering optimization model.

What the professor can help with:

- Should we cite Cui et al. earlier in the introduction?
- Should we explicitly say our paper is a "Japan panel complement" rather than
  an optimization paper?
- Should we strengthen the comparison between China's facility hierarchy and
  Japan's selective modernization?
- Should "bounded responsiveness" be replaced with simpler wording such as
  "persistent generator hierarchy"?

### 5.2 Liu et al. (2025), Nature Energy

Full citation:

> Liu, B., Wang, P., Zhou, J., Guo, Y., Ma, S., Chen, W.-Q., Li, J., and
> Chang, V. W.-C. (2025). Refocusing on effectiveness over expansion in urban
> waste-energy-carbon development in China. Nature Energy, 10, 215-225.
> https://doi.org/10.1038/s41560-024-01683-8

Why it is important:

- It gives the paper a high-level framing: expansion is not enough.
- It supports the idea that "more capacity" or "more WTE" is not automatically
  the right performance question.
- It helps explain why generator performance after entry matters.

What we take from it:

- Effectiveness matters after infrastructure exists.
- Waste-energy-carbon systems should be assessed by performance, not only by
  scale or expansion.
- The policy conversation should move from "how much infrastructure exists" to
  "how well the infrastructure performs."

What we do differently:

- Liu et al. study China's waste-energy-carbon development.
- Our paper studies Japan's facility-level administrative panel.
- Our paper separates non-generator entry from generator performance.
- Our paper is diagnostic and descriptive, not a full carbon-development model.

How to explain our difference:

> Liu et al. inspire the "effectiveness over expansion" logic. Our paper applies
> a related idea to Japan: the key question is not only whether facilities
> exist, but whether non-generators enter electricity recovery and whether
> existing generators recover electricity effectively.

What the professor can help with:

- Should the introduction explicitly use the phrase "effectiveness over
  expansion"?
- Should the paper tie the adoption/performance split more strongly to carbon
  planning?
- Or should the carbon framing remain secondary to avoid overclaiming?

### 5.3 Chen et al. (2012), Journal of Environmental Management

Full citation:

> Chen, P.-C., Chang, C.-C., Yu, M.-M., and Hsu, S.-H. (2012). Performance
> measurement for incineration plants using multi-activity network data
> envelopment analysis: The case of Taiwan. Journal of Environmental
> Management, 93(1), 95-103.
> https://doi.org/10.1016/j.jenvman.2011.08.011

Why it is important:

- It is a close facility-performance comparator.
- It shows that incinerator performance can be decomposed empirically.
- It treats incineration plants as multi-activity production units.

What we take from it:

- Facility-level incinerator performance is a legitimate empirical object.
- Electricity generation can be part of performance measurement.
- Plant-level heterogeneity is meaningful for waste-management policy.

What we do differently:

- Chen et al. use network DEA.
- We use panel regression.
- Chen et al. evaluate operating plants.
- We also study non-generators entering generation.

How to explain our difference:

> Chen et al. are methodologically closer to facility performance measurement,
> but our method is intentionally simpler. We are not ranking plants by DEA
> efficiency. We are showing that Japan's fleet has two different margins:
> entry into generation and conditional electricity recovery after entry.

What the professor can help with:

- Would a DEA robustness extension improve publishability?
- Or would it distract from the two-margin contribution?
- Should DEA papers be discussed as "related but not the chosen method"?

### 5.4 Yeh (2020), Waste Management

Full citation:

> Yeh, L.-T. (2020). Analysis of the dynamic electricity revenue inefficiencies
> of Taiwan's municipal solid waste incineration plants using data envelopment
> analysis. Waste Management, 107, 28-35.
> https://doi.org/10.1016/j.wasman.2020.03.040

Why it is important:

- It is directly in the target-journal ecosystem.
- It focuses on electricity-related inefficiency in MSW incineration plants.
- It supports the idea that generator performance is uneven and measurable.

What we take from it:

- Electricity-related performance matters in incinerator evaluation.
- Dynamic facility comparison is relevant to Waste Management readers.

What we do differently:

- Yeh studies electricity revenue inefficiency, not MWh/t.
- Yeh uses DEA, not regression.
- Yeh does not address the non-generator adoption margin.

How to explain our difference:

> Yeh is a Waste Management precedent for studying electricity-related
> incinerator performance. Our paper complements that family by asking an
> earlier fleet question: which plants enter generation at all?

### 5.5 Grosso et al. (2010), Waste Management

Full citation:

> Grosso, M., Motta, A., and Rigamonti, L. (2010). Efficiency of energy recovery
> from waste incineration, in the light of the new Waste Framework Directive.
> Waste Management, 30(7), 1238-1243.
> https://doi.org/10.1016/j.wasman.2010.02.036

Why it is important:

- It anchors the energy-recovery-performance concept.
- It reminds readers that energy recovery is not just an operational detail.
- It connects incineration performance to policy criteria.

What we take from it:

- Electricity/energy recovery is a legitimate outcome dimension.
- Waste incinerators can be judged partly by recovery performance.

What we do differently:

- We do not calculate a full EU R1 recovery-efficiency criterion.
- We use administrative MWh/t because that is what the Japan panel supports.
- We frame the metric as "electricity recovery intensity" rather than a pure
  thermodynamic efficiency measure.

How to explain our difference:

> Grosso et al. support the importance of energy recovery, but our paper uses a
> practical administrative metric: electricity generated per tonne of waste.
> This is less engineering-complete but more feasible for national panel
> comparison.

### 5.6 Allison (1982)

Full citation:

> Allison, P. D. (1982). Discrete-time methods for the analysis of event
> histories. Sociological Methodology, 13, 61-98.
> https://doi.org/10.2307/270718

Why it is important:

- It supports the adoption-model logic.
- It explains how to model events observed in discrete time.

What we take from it:

- Each facility-year is a risk-set observation.
- The event is first observed entry into generation.
- A logit hazard is appropriate for annual event data.

What we do differently:

- We apply event-history logic to municipal incineration facilities.
- We keep interpretation descriptive because the event is administrative
  reporting of generation, not directly observed engineering retrofit.

### 5.7 Beck, Katz, and Tucker (1998)

Full citation:

> Beck, N., Katz, J. N., and Tucker, R. (1998). Taking time seriously:
> Time-series-cross-section analysis with a binary dependent variable.
> American Journal of Political Science, 42(4), 1260-1288.
> https://doi.org/10.2307/2991857

Why it is important:

- It is a classic reference for binary outcomes in time-series-cross-section
  data.
- It warns that time dependence matters when units are observed repeatedly.

What we take from it:

- Repeated facility-year binary outcomes should not be treated as simple
  independent cross-sections.
- Event timing and temporal controls matter.

What we do differently:

- We use the paper as methodological support, not as a full replication.
- We currently use year fixed effects and lagged predictors.
- A possible improvement is a time-at-risk robustness check if the professor
  thinks reviewers will expect it.

### 5.8 Wooldridge (2010)

Full citation:

> Wooldridge, J. M. (2010). Econometric analysis of cross section and panel
> data (2nd ed.). MIT Press.

Why it is important:

- It supports panel regression, fixed effects, random effects, and clustered
  standard errors.

What we take from it:

- Pooled and panel regressions are standard tools for repeated facility data.
- Clustered standard errors are appropriate when rows repeat by facility.
- Fixed effects and random effects answer different descriptive questions.

What we do differently:

- We do not claim the panel regressions identify causal treatment effects.
- We use the models as structured descriptive comparisons.

## 6. What The Paper Takes, Adapts, And Does Not Take

### 6.1 What We Take

| Source family | What we take | How it appears in the paper |
|:--|:--|:--|
| Cui/Liu high-profile WTE papers | Facility hierarchy and effectiveness framing | Two-margin interpretation and broader contribution |
| Taiwan DEA papers | Facility-level incinerator performance is measurable | Generator performance model |
| Energy-recovery literature | MWh/t and recovery performance matter | Electricity recovered per tonne outcome |
| Event-history literature | First-entry modeling in annual data | Adoption hazard |
| Panel-data literature | Repeated facility observations require panel-aware methods | Pooled/year FE/RE models and clustered SEs |
| Lock-in literature | Mature infrastructure can remain stratified | Discussion interpretation |

### 6.2 What We Adapt

| Borrowed idea | Adaptation |
|:--|:--|
| Facility efficiency hierarchy | We convert it into a Japan panel hierarchy of electricity recovered per tonne |
| Effectiveness over expansion | We convert it into "entry is not enough; generator performance also matters" |
| Event-history modeling | We apply it to first observed generation entry in administrative data |
| Panel regression | We use it as descriptive facility comparison, not causal proof |
| Infrastructure lock-in | We use it as interpretation, not as a mechanism test |

### 6.3 What We Do Not Take

| Method or claim not taken | Why not |
|:--|:--|
| Full optimization model like Cui et al. | Japan panel lacks detailed line-level technology and optimization variables |
| DEA as main method | It would answer a frontier-ranking question, not the two-margin adoption/performance question |
| Causal retrofit effect | Adoption events are observed reports, not verified physical retrofit records |
| Policy shock identification | Event timing is clustered but not cleanly identified as a policy shock |
| Full thermodynamic efficiency | Heating value is noisy and not enough for a full engineering efficiency measure |
| Universal global claim | The evidence is Japan-specific and sample-bounded |

## 7. What Feedback We Need From The Professor

The professor can help most by answering these questions.

### 7.1 Framing Questions

1. Should the paper be framed mainly as a Japan waste-management paper?
2. Should it be framed as a facility-level energy-recovery paper?
3. Should it be framed as a two-margin fleet-transition paper?
4. Should the title keep "bounded responsiveness" or use plainer wording such
   as "persistent generator hierarchy"?

Recommended current choice:

> Two-margin fleet-transition paper, written for Waste Management readers.

Why:

- It is more original than a generic Japan case study.
- It explains why the adoption and performance models belong in one paper.
- It avoids competing directly with engineering-optimization papers on their
  own terms.

### 7.2 Methods Questions

1. Is the adoption model defensible as a discrete-time logit hazard?
2. Should we add a time-at-risk robustness check?
3. Should we keep random effects as descriptive or move more emphasis to pooled
   OLS plus year fixed effects?
4. Should we add a facility fixed-effects sensitivity in the supplement, even
   if it is not the main model?
5. Should we avoid the word "efficiency" more aggressively and use
   "electricity recovery intensity" throughout?

Recommended current choice:

> Keep the current main models, but consider one extra robustness check:
> time-at-risk or spell-duration controls in the adoption model.

Why:

- It would strengthen the event-history lineage.
- It would not require changing the main argument.
- It answers a likely methodological reviewer question.

### 7.3 Literature Questions

1. Should Cui et al. (2026) be cited in the introduction rather than only the
   literature section?
2. Should Liu et al. (2025) be used to frame "effectiveness over expansion"?
3. Should the Taiwan DEA papers be described as a parallel method family rather
   than direct method parents?
4. Should Japan-specific sources be made more prominent so the paper does not
   look like a China-comparator paper?

Recommended current choice:

> Cite Cui et al. and Liu et al. as high-profile framing comparators, but make
> clear that the actual methods come from event-history and panel-data
> literature.

Why:

- This is honest.
- It avoids implying that we copied a Nature-style optimization model.
- It helps the professor understand the paper's ambition and limits.

### 7.4 Contribution Questions

1. Is the main contribution the Japan dataset, the two-margin design, or the
   policy implication?
2. Is the adoption margin strong enough to be a main contribution?
3. Is the generator-performance margin strong enough without DEA?
4. Should the paper emphasize "selective modernization" or "asset-management
   triage"?

Recommended current choice:

> The main contribution is the two-margin design applied to Japan's national
> facility panel.

Why:

- The Japan dataset matters, but "Japan case study" alone is weaker.
- The policy implication matters, but it is descriptive and should stay
  calibrated.
- The two-margin design is the clearest originality claim.

## 8. Suggested Meeting Script

This is a simple way to explain the paper to the professor.

### Opening

> I prepared this paper as a facility-level Japan study, but I do not want to
> present it as if it came from one single method paper. It is inspired by
> recent waste-incineration efficiency papers, especially Cui et al. in Nature
> Communications and Liu et al. in Nature Energy. Those papers show that WTE
> systems should be evaluated by facility-level performance and effectiveness,
> not just by total capacity.

### Method Explanation

> Methodologically, our paper is simpler and more defensible. It uses two
> linked models. First, a discrete-time logit hazard asks which non-generating
> facilities first report power generation. Second, panel regressions ask how
> much electricity per tonne is recovered among operating generators. The
> adoption model comes from event-history logic, while the performance models
> come from panel-regression logic.

### Contribution Explanation

> The main contribution is the split between the adoption margin and the
> performance margin. Many studies look only at operating generators. Our paper
> shows that in Japan, the fleet problem has two parts: some facilities still do
> not enter generation, and generators that already entered still differ
> strongly by age, scale, and utilization.

### Feedback Request

> I would like your feedback on whether this should be framed mainly as a
> Japan waste-management paper, a facility-performance paper, or a two-margin
> fleet-transition paper. I also want to know whether you think the methods are
> sufficient, or whether we should add one robustness check such as
> time-at-risk controls in the adoption model.

## 9. Recommended Reframing Options

### Option A: Waste Management Conventional Framing

Possible title direction:

> Separating generation entry and electricity recovery in Japan's municipal
> waste-incineration fleet

Strength:

- Clear for Waste Management readers.
- Less risky than abstract theory language.

Weakness:

- Less distinctive.
- May sound incremental.

Best if:

- The professor wants a safe submission-oriented paper.

### Option B: High-Profile Comparator Framing

Possible title direction:

> Selective modernization and performance hierarchy in Japan's
> waste-incineration fleet

Strength:

- Connects better to Cui et al. and Liu et al.
- Makes the paper feel more ambitious.

Weakness:

- Must be carefully bounded because we do not have their technical detail.

Best if:

- The professor wants the paper to aim higher and be more conceptually
  memorable.

### Option C: Policy And Asset-Management Framing

Possible title direction:

> From non-generator triage to generator optimization: Evidence from Japan's
> municipal waste-incineration fleet

Strength:

- Strong practical meaning.
- Easy for municipal-policy readers to understand.

Weakness:

- "Optimization" may imply stronger methods than we have.

Best if:

- The professor wants stronger planning relevance.

### Option D: Methods-First Two-Margin Framing

Possible title direction:

> Why fleet averages mislead: Adoption and conditional performance in Japan's
> waste-incineration fleet

Strength:

- Clear methodological contribution.
- Explains why both models belong in one paper.

Weakness:

- Less directly engineering-focused.

Best if:

- The professor thinks the originality is mainly analytical design.

## 10. Recommended Current Direction

My recommendation is Option D blended with Option B:

> A two-margin fleet-transition paper with high-profile facility-performance
> comparators.

Working frame:

> Recent high-profile waste-incineration studies show that facility-level
> efficiency hierarchy matters. This paper extends that logic to Japan by
> separating two margins that are often blended together: observed entry into
> electricity generation and electricity recovered per tonne among generators.

Why this is optimal:

- It is ambitious but defensible.
- It uses Cui et al. and Liu et al. as inspiration without pretending to use
  the same optimization methods.
- It explains why adoption and performance are both necessary.
- It avoids a weak "Japan has many incinerators" case-study framing.

## 11. What To Add To The Manuscript After Professor Feedback

These are possible additions, not changes to make blindly.

### High Priority

1. Add a short comparator paragraph in the introduction:

   > Recent facility-level waste-incineration studies increasingly emphasize
   > performance hierarchy and effectiveness rather than expansion alone. This
   > paper follows that facility-level logic but applies it to a different
   > problem: the coexistence of non-generators and uneven generator
   > performance in Japan.

2. Add one sentence distinguishing this paper from Cui et al.:

   > Unlike optimization studies based on detailed technical line-level data,
   > this paper uses an administrative facility panel to separate observed
   > generation entry from conditional electricity recovery.

3. Add one methodological bridge:

   > The design therefore joins event-history logic for the entry margin with
   > panel-regression logic for the performance margin.

### Medium Priority

1. Add a time-at-risk robustness check for adoption.
2. Add a short facility-fixed-effects sensitivity note for the generator model.
3. Rename more instances of "efficiency" to "electricity recovery intensity."
4. Add a supplement table comparing this paper to Cui, Liu, Chen, Yeh, and
   Grosso.

### Low Priority

1. Add a DEA appendix.
2. Build an optimization scenario model.
3. Add international comparison beyond Japan/China/Taiwan.

Why these are low priority:

- They may create a second paper rather than improve the current one.
- They require new assumptions and may delay submission.
- The current contribution is already clear if framed correctly.

## 12. Honest Boundaries To State To The Professor

The professor should know these boundaries before suggesting directions.

### Boundary 1: The Paper Is Not Cui et al.

It does not have:

- line-level furnace design data
- complete technology-package information
- detailed flue-gas treatment records
- waste-composition detail across all plants
- optimization-measure simulation

Therefore:

> The paper should not be framed as a Japan version of Cui et al. It should be
> framed as a Japan panel complement that studies transition and performance
> margins.

### Boundary 2: The Adoption Event Is Administrative

The event is:

- first observed report of power generation in the panel

It is not always:

- directly observed retrofit
- confirmed new turbine installation
- verified replacement project

Therefore:

> Use "observed transition into generation" rather than "retrofit" unless the
> pathway audit supports the specific case.

### Boundary 3: The Performance Outcome Is MWh/t

The outcome is:

- electricity generated per tonne of waste processed

It is not:

- full thermodynamic efficiency
- R1 recovery status
- total energy recovery including heat use

Therefore:

> Use "electricity recovery intensity" when precision matters. "Efficiency" can
> be used as shorthand only after defining the metric.

### Boundary 4: The Models Are Descriptive

The models show:

- conditional associations
- stable sign patterns
- facility hierarchy

They do not prove:

- causal effect of age
- causal effect of capacity
- policy treatment effect
- unique modernization mechanism

Therefore:

> The paper's strength is diagnostic decomposition, not causal identification.

## 13. Best Questions For The Professor To Answer

Bring these questions to the meeting.

### Question 1

Should the paper cite high-profile China papers in the introduction as framing
comparators, or keep them in the literature review to avoid making the paper
look like it is trying to compete directly with them?

Recommended default:

> Mention them briefly in the introduction and explain the difference clearly.

### Question 2

Is "selective modernization and bounded responsiveness" a good conceptual
frame, or should the paper use plainer wording?

Recommended default:

> Keep "selective modernization"; consider replacing "bounded responsiveness"
> with "persistent generator hierarchy" if the professor thinks the phrase is
> too abstract.

### Question 3

Does the adoption model need a duration/time-at-risk robustness check?

Recommended default:

> Add it if feasible. It is a clean methodological upgrade and should not
> disrupt the main story.

### Question 4

Should DEA be mentioned as related literature only, or added as an empirical
extension?

Recommended default:

> Mention DEA as related literature only. Save DEA for a future paper unless
> the professor strongly wants it.

### Question 5

Should the paper be submitted as a descriptive empirical paper, or should it
wait for stronger causal or optimization analysis?

Recommended default:

> Keep it as a descriptive empirical paper. The claim is already defensible if
> the framing is precise.

## 14. Suggested Email To Professor

Subject:

```text
Comparator papers and method lineage for the incineration paper
```

Body:

```text
Professor,

I prepared a short method-lineage note to clarify which papers inspired the
paper and which methods were adapted.

The paper is mainly inspired by recent facility-level waste-incineration
performance work, especially Cui et al. (2026) in Nature Communications and
Liu et al. (2025) in Nature Energy. However, I am not trying to replicate their
optimization methods. My paper uses a Japan administrative facility panel and
separates two margins:

1. observed entry into electricity generation among non-generators; and
2. electricity recovered per tonne among operating generators.

Methodologically, the first part follows discrete-time event-history logic, and
the second part uses panel regression with facility-clustered standard errors.

I would like your feedback on whether this should be framed as a Japan
waste-management paper, a facility-performance paper, or a two-margin
fleet-transition paper. I would also appreciate your view on whether we should
add one more robustness check, such as time-at-risk controls in the adoption
model.

Best regards,
Pann
```

## 15. Source List For The Professor

### High-Profile / Benchmark Papers

- Cui, J., Cui, Y., Li, J., Gao, X., Wei, W., Chen, Y., Ma, W., Zhu, N.,
  Geng, Y., Zhao, Y., and Lou, Z. (2026). Efficiency hierarchy and optimization
  of waste incineration in China to balance disposal and energy supply. Nature
  Communications, 17(1), Article 3069.
  https://doi.org/10.1038/s41467-026-69897-w
- Liu, B., Wang, P., Zhou, J., Guo, Y., Ma, S., Chen, W.-Q., Li, J., and
  Chang, V. W.-C. (2025). Refocusing on effectiveness over expansion in urban
  waste-energy-carbon development in China. Nature Energy, 10, 215-225.
  https://doi.org/10.1038/s41560-024-01683-8
- Han, Q.-l., Liu, H.-q., Gong, Y.-y., Tao, J.-y., Sun, Y.-n., Wei, G.-x.,
  Zhu, Y.-w., and Chen, G.-y. (2025). Strengthening pollutant control and
  resource recovery can enhance sustainable waste incineration in China.
  Communications Earth & Environment, 6, Article 863.
  https://doi.org/10.1038/s43247-025-02859-0

### Facility-Performance Papers

- Chen, P.-C., Chang, C.-C., Yu, M.-M., and Hsu, S.-H. (2012). Performance
  measurement for incineration plants using multi-activity network data
  envelopment analysis: The case of Taiwan. Journal of Environmental
  Management, 93(1), 95-103.
  https://doi.org/10.1016/j.jenvman.2011.08.011
- Yeh, L.-T. (2020). Analysis of the dynamic electricity revenue inefficiencies
  of Taiwan's municipal solid waste incineration plants using data envelopment
  analysis. Waste Management, 107, 28-35.
  https://doi.org/10.1016/j.wasman.2020.03.040
- Grosso, M., Motta, A., and Rigamonti, L. (2010). Efficiency of energy
  recovery from waste incineration, in the light of the new Waste Framework
  Directive. Waste Management, 30(7), 1238-1243.
  https://doi.org/10.1016/j.wasman.2010.02.036
- Münster, M., and Meibom, P. (2010). Long-term affected energy production of
  waste to energy technologies identified by use of energy system analysis.
  Waste Management, 30(12), 2510-2519.
  https://doi.org/10.1016/j.wasman.2010.04.015

### Japan Context

- Tabata, T., and Tsai, P. (2016). Heat supply from municipal solid waste
  incineration plants in Japan: Current situation and future challenges. Waste
  Management & Research, 34(4), 345-351.
  https://doi.org/10.1177/0734242X15617009
- Uno, S. (2015). Trends in Waste-to-Energy Technologies for High Efficiency
  Power Generation. Material Cycles and Waste Management Research, 26(2),
  114-119.
  https://doi.org/10.3985/mcwmr.26.114
- Yamada, K., Ii, R., Yamamoto, M., Ueda, H., and Sakai, S. (2023). Japan's
  greenhouse gas reduction scenarios toward net zero by 2050 in the material
  cycles and waste management sector. Journal of Material Cycles and Waste
  Management, 25(4), 1807-1823.
  https://doi.org/10.1007/s10163-023-01650-7

### Methods

- Allison, P. D. (1982). Discrete-time methods for the analysis of event
  histories. Sociological Methodology, 13, 61-98.
  https://doi.org/10.2307/270718
- Beck, N., Katz, J. N., and Tucker, R. (1998). Taking time seriously:
  Time-series-cross-section analysis with a binary dependent variable. American
  Journal of Political Science, 42(4), 1260-1288.
  https://doi.org/10.2307/2991857
- Wooldridge, J. M. (2010). Econometric analysis of cross section and panel
  data (2nd ed.). MIT Press.

## 16. Bottom-Line Recommendation

For the meeting, do not say:

> We copied the method from Cui et al.

Say instead:

> Cui et al. and Liu et al. inspired the ambition and facility-level framing.
> Chen, Yeh, and Grosso show that incinerator energy-recovery performance is a
> legitimate facility-level empirical object. Allison, Beck et al., and
> Wooldridge support the actual empirical methods. Our contribution is to join
> these lines in a Japan panel by separating observed generation entry from
> conditional generator performance.

This is the most honest, defensible, and useful way to help the professor give
feedback.
