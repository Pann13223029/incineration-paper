# Selective Entry and Structured Electricity-Recovery Performance in Japan's Waste-Incineration Fleet: A Facility-Level Panel Study

## Abstract

Japan relies heavily on municipal waste incineration, but only 415 of 991
facilities (41.9%) generated electricity in fiscal year (FY) 2024 according to
the official national summary. Fleet averages blur two different margins:
entry into electricity recovery and performance among facilities that already
generate. Using Ministry of the Environment facility records for
FY2005-FY2024, this paper examines both margins in one linked national panel.
The entry event is first observed reporting of positive installed generation
capacity. In a broad coded-asset risk set, larger prior-year capacity predicts
entry and facilities older than ten years have lower adjusted entry
probabilities than the 0-10-year reference group. Requiring positive prior-year
throughput leaves the positive scale association intact but substantially
attenuates the age gradient. This distinction matters because 40 of 98 exact-
year events follow zero or missing prior-year throughput and may represent
commissioning, rebuild, or inactive-asset pathways rather than conversion of an
operating plant. Among identifiable operating generators, year- and technology-
adjusted gross electricity generation per tonne is lower at older-vintage
facilities and higher at larger, more fully utilized facilities. Adjacent-year
performance ranks correlate at 0.93, while entrants occupy approximately the
middle of the same-year generator distribution during their first four observed
years. These are descriptive associations, not causal effects of retrofit,
aging, or entry. They show that asset entry, active-plant conversion,
administrative attrition, and post-entry performance are related but distinct
fleet outcomes that should not be managed as one average segment.

**Keywords:** waste incineration; waste-to-energy; Japan; energy recovery;
facility panel; transition

## 1. Introduction

Japan operates one of the world's most incineration-dependent municipal waste
systems, yet many facilities still burn waste without generating electricity
from the heat they produce (Ministry of the Environment Japan, 2026; Uno, 2015;
Tabata & Tsai, 2016; Sakai et al., 2011). In fiscal year (FY) 2024, the official
national summary reports that 415 of 991 incineration facilities, or 41.9%,
generated electricity (Ministry of the Environment Japan, 2026). Most
facilities therefore remained outside electricity generation. This is not a
marginal technical detail. For
decades, Japanese municipal waste governance has relied on thermal treatment for
hygienic disposal, volume reduction, and local waste autonomy, while limited
landfill space and strict environmental controls pushed municipalities toward
sophisticated incineration infrastructure (Brunner & Rechberger, 2015; Sakai et
al., 2011). Sectoral planning now treats the remaining electricity-generation
gap as part of the waste sector's decarbonization challenge (Yamada et al.,
2023; Greenhouse Gas Inventory Office of Japan & Ministry of the Environment
Japan, 2024). The transition problem is therefore not whether Japan uses
incineration. It is whether observed entry into electricity recovery is
patterned across facilities and how electricity recovery intensity varies once
generation is present.

Aggregate fleet summaries flatten two distinct questions. One is extensive:
which facilities first report installed power-generation capacity? The
other is intensive: among plants that already generate, which facilities achieve
high electricity recovery per tonne? The system can therefore look uniformly
slow in the mean while combining selective entry at one end of the fleet with
persistent performance hierarchy at the other.

### Research questions

This paper asks two descriptive empirical questions and one interpretive
synthesis question. In the table, RQ denotes research question; the synthesis
row states how the two empirical results are read together:

| RQ | Margin | Question |
|:--|:--|:--|
| RQ1 | Entry margin | Among coded facilities first observed without installed power-generation capacity, which prior-year age and capacity profiles are associated with first reporting positive capacity in the following fiscal year, and how do those associations change when the risk set is restricted to facilities with positive prior-year throughput? |
| RQ2 | Generator-performance margin | Among identifiable operating generators, how is gross electricity generated per tonne associated with facility age/vintage, design capacity, utilization, heating value, and observed technology configuration within common fiscal years? |
| Synthesis | Interpretive synthesis | Taken together, do the observed entry pattern and generator-frame performance associations support one average-fleet modernization interpretation, or do they indicate distinct adoption and performance problems within the same incineration system? |

The contribution is not a causal estimate of retrofit effects or a technical
optimization model. It is a linked facility-panel decomposition that shows why
observed entry into installed generation capacity and conditional generator performance should be
modeled separately before being interpreted together. The paper uses two linked
samples: one follows facilities without installed generation capacity until they
first report positive capacity, and the other compares identifiable operating
generators over time. The first sample further distinguishes broad coded-asset
entry from conversion among facilities that were demonstrably operating in the
prior year. Scale selectivity appears in both entry frames, whereas the age
gradient is pronounced in the broad asset frame but weaker in the active-
conversion frame. In the second sample, electricity recovery intensity is
strongly structured by age/vintage, scale, and utilization, while within-
facility movement remains limited relative to between-facility heterogeneity.
The same fleet can therefore look merely slow in aggregate while containing
different problems: entry into generation, conversion of active plants, and
uneven performance after entry. For municipal planning, that distinction
changes the first diagnostic step. Facilities outside electricity recovery and
mature generators should be evaluated as different asset-management questions
before they are summarized as one fleet.

A natural expectation is that larger and newer facilities will have advantages.
The analysis does not present that expectation as a discovery by itself. It
tests where the apparent advantage appears, whether it survives changes in the
risk-set definition, and whether entry is followed by convergence within the
generator distribution. The robust result at the entry margin is scale
selectivity. The age result is conditional on whether the model describes all
coded assets or operating non-generators specifically. After entry, generators
remain stratified, but recent entrants begin near the middle of the same-year
distribution rather than at an obvious performance frontier. That sequence is
what an aggregate fleet mean or generator-only study would miss.

![Figure 1. Analytical design separating the source panel into entry and generator-performance margins before interpreting both margins together.](../figures/figure1_two_part_framework.png)

The gap addressed here is narrower than a generic claim that Japan has been
understudied. Waste-to-energy research can describe fleet trajectories, and
generator-only studies can explain conditional performance once plants already
operate as generators. What remains uncommon is one linked municipal-fleet
analysis that estimates both margins and asks whether they point to the same
modernization bottleneck. Japan makes that contrast visible because persistent
non-generators, old small plants, and a more modern generating segment coexist
in the same administrative system. In such mixed fleets, adoption and
conditional performance should be modeled separately before they are interpreted
together.

The rest of the paper proceeds as follows. Section 2 positions the paper against
the literature most relevant to the analytical split. Section 3 introduces the
two linked analytical frames and the main estimation choices. Section 4 reports
the adoption and electricity-recovery results in sequence, then ties them
together. Section 5 interprets the combined finding, explains what the data
still cannot identify, and states a short set of evidence-consistent
implications. Section 6 concludes.

## 2. Literature Positioning

This paper speaks to three literatures that often meet in practice but start
from different empirical positions: waste-to-energy systems, facility-level
performance analysis, and infrastructure lock-in. The review is organized around
the paper's central split between entry into generation and conditional
performance after entry. The relevant gap is not simply that Japan needs another
case study. It is that existing studies often describe fleets in aggregate or
explain generator performance conditional on operation, yet rarely estimate both
margins in one linked municipal-fleet design.

Work on waste-to-energy systems often documents national trajectories,
technology choices, or lifecycle implications of thermal treatment (Astrup et
al., 2009; Astrup et al., 2015; Brunner & Rechberger, 2015; Sun et al., 2018).
Japan-specific work has emphasized technology upgrading, heat-use constraints,
and sectoral decarbonization scenarios (Uno, 2015; Tabata & Tsai, 2016; Yamada
et al., 2023). Two closer empirical comparators clarify the remaining gap.
Sasao (2018) analyzes heat and electricity production at 635 Japanese waste-to-
energy plants over FY2007-FY2015 using random-effects Tobit models and a broad
set of policy, technology, and demographic correlates. Shino (2019) evaluates
Japanese incinerator power-generation performance and supports electricity
generation per unit waste input as an observable performance measure while
showing why thermal-efficiency interpretation depends on calorific-value data.
Neither study follows the annual first-reporting transition from no installed
capacity into positive capacity and then links that transition to early post-
entry position in the generator distribution. Policy-facing work reaches a similar
conclusion from a different angle: waste-to-energy is treated as useful only
when embedded in a wider waste hierarchy and resource-recovery strategy rather
than as a stand-alone justification for thermal treatment (European Commission,
2017; Sakai et al., 2011). This literature is indispensable for understanding
why energy recovery matters, but it usually treats the incineration fleet as a
sectoral category. It can show whether energy recovery is expanding, whether
heat supply remains constrained, or whether the sector matters for net-zero
planning. It is less well suited to distinguishing facilities that enter
generation from those that do not.

Facility-level performance studies are closer to the present design, but they
typically begin after entry has already occurred. Studies in Taiwan, for
example, evaluate operating incinerators by decomposing waste-treatment,
electricity-generation, or revenue performance within existing plants (Chen et
al., 2012; Yeh, 2020). Other work focuses on energy-recovery criteria, plant
scale, heat use, and the system consequences of different waste-to-energy
configurations (Grosso et al., 2010; Münster & Meibom, 2010). Recent Chinese
plant-level work is also highly informative about performance differentials
inside the generating segment and the effectiveness of upgrading strategies at
scale (Cui et al., 2026; Liu et al., 2025; Han et al., 2025). Those studies
help define the intensive-margin question. They do not directly answer which
non-generating facilities enter generation in the first place.

The present paper therefore uses those comparator papers as a method-positioning
map rather than as templates to copy. The table below makes the adaptation logic
explicit.

**Comparator adaptation of research logic**

| Source family | Borrowed logic | Japan-specific adaptation | Not claimed here |
|:--|:--|:--|:--|
| Cui et al. (2026) | Incinerators form a performance hierarchy, not a set of interchangeable plants | The Japan panel is read through facility heterogeneity and persistent hierarchy | No optimization frontier or ranking of Japanese plants on the same technical frontier |
| Liu et al. (2025) | Waste-energy systems should be judged by effectiveness, not expansion alone | Effectiveness is split into entry into generation and performance after entry | No China-style waste-energy-carbon development model |
| Sasao (2018) | Japanese plant-level heat and electricity outcomes can be related to policy, technology, and local context in panel data | The present paper retains facility-level panel comparison but changes the first outcome to annual entry into installed generation capacity and separates it from post-entry MWh/t | No Tobit production function and no claim that the available policy covariates identify entry mechanisms |
| Shino (2019) | Electricity generation per unit waste input is a useful observable performance indicator; thermal interpretation requires attention to heating value | Gross MWh/t is the primary operational outcome, with a heating-value-based conversion proxy and reported efficiency used as convergent validation | No claim that gross MWh/t equals net export, overall energy recovery, or a complete thermodynamic efficiency measure |
| Han et al. (2025) | Resource recovery and sustainability depend on upgrade pathways, not incineration alone | The generator model adjusts for available furnace type, operating mode, facility type, and furnace count | No pollutant-control technology model because comparable plant-level control variables are unavailable |
| Chen et al. (2012) and Yeh (2020) | Facility-level incinerator performance can be compared empirically after operation begins | The generator frame models electricity recovered per tonne across identifiable plants | No data envelopment analysis frontier or electricity-revenue inefficiency model |
| Grosso et al. (2010) and Münster and Meibom (2010) | Energy recovery should be interpreted in a wider energy-system context | The paper uses gross electricity generation per tonne as an applied recovery measure | No full R1 efficiency calculation, net-export measure, lifecycle balance, or energy-system optimization model |

This matters for interpretation because the paper is not trying to be a weaker
version of any one comparator. Its foundation is a deliberate combination:
facility heterogeneity from high-profile incineration studies, transition timing
from event-history methods, and conditional performance comparison from prior
Japanese and international plant-level analyses. The originality claim is
modest but clear: the paper changes the unit of inquiry from production among
plants already observed with energy recovery to first observed entry among
non-generators, then reconnects entrants to their early generator performance.
This is an adaptation of established methods to a different estimand, not a
claim to have invented logit hazards or panel performance regression.

The lock-in literature adds a different expectation. Infrastructure performance
may be shaped by durable design choices, inherited scale, and institutional
arrangements rather than by frequent late-life reversals at mature facilities
(Unruh, 2000; Geels, 2004; Seto et al., 2016). The useful implication here is
not that incineration plants are literally irreversible. It is that
cross-facility differences may matter more than repeated performance resets. In
municipal infrastructure, that persistence can also be institutional rather than
purely technical: plant networks are shaped by jurisdictional boundaries,
merger histories, charging regimes, and the political difficulty of
reorganizing service territories (Rausch, 2006; Sakai et al., 2008; Sakai et
al., 2011). That expectation is only partially visible if entry into generation
and performance within generation are never separated.

Read together, the literatures imply a practical identification problem for
fleet studies. Fleet-level work can show aggregate progress but cannot tell
whether low average performance reflects many non-generators, weak generator
performance, or both. Generator-only work can estimate performance correlates
after entry, but not who stays outside generation. Lock-in work explains why
mature infrastructure may remain stratified, but not whether the key margin lies
before or after entry. The contribution of this paper is to use one linked panel
to expose those blind spots without treating them as one average process.

## 3. Data and Design

The analysis uses the Ministry of the Environment's General Waste Treatment
Survey for FY2005-FY2024 (Ministry of the Environment Japan, 2026; e-Stat,
n.d.). From 23,599 facility-year rows, the coded frame retains 19,827
observations across 2,948 identifiable facilities. The paper then separates two
linked samples because one sample cannot answer both parts of the transition
problem. Those frames are not
only data filters. They are the analytic structure that keeps observed entry
into installed generation capacity separate from conditional performance after
entry. The survey is
useful for this purpose because it covers both generating and non-generating
facilities inside the same administrative system. That makes it possible to ask
a question that many sector studies cannot ask cleanly: which facilities record
observed entry into installed generation capacity, and how do facilities perform once they are
already inside the generating segment?
The two samples differ because the questions differ: non-generators reveal who
enters electricity recovery, while generators reveal performance differences
after entry.

The official FY2024 summary and the reconstructed analytical panel should not be
treated as interchangeable denominators. The official publication reports 415
electricity-generating facilities among 991 incineration facilities (41.9%). In
the row-level analytical reconstruction, 417 of 1,014 FY2024 rows have positive
installed generation capacity (41.1%). The difference reflects reconstruction
and classification boundaries in the facility-level files. The official 41.9%
is used for national context; the 41.1% analytical share is reported only as a
reproducibility diagnostic and is not presented as the official statistic.

The design intentionally combines established empirical building blocks rather
than inventing a new estimator. The adoption layer follows discrete-time
event-history logic for a binary transition observed in annual administrative
data (Allison, 1982; Beck et al., 1998). The generator layer follows
facility-level performance studies that compare operating incinerators after
entry, while using panel regressions to summarize persistent cross-facility
structure (Chen et al., 2012; Yeh, 2020; Wooldridge, 2010). What is different
here is the way those pieces are linked: the paper first models observed entry
into installed generation capacity, then separately models electricity generated per tonne among
identifiable generators, and only then asks whether a single average-fleet
interpretation is adequate. This makes the framework similar in spirit to
plant-level optimization and performance papers, but distinct in its
Japan-specific two-margin diagnostic focus.

Several modeling choices follow from that alignment between question and
sample. The entry model is deliberately narrow because the event of interest is
first observed reporting of positive installed generation capacity, not every
capital investment or every first unit of electricity output that
may have occurred before or outside the panel. The generator model is also
deliberately narrow because it compares identifiable operating generators, not
all facilities and not uncoded generator rows that cannot be followed reliably
as facility panels. The paper therefore uses the same administrative source for
both questions but does not force both questions into the same sample or the
same estimator.

**Research-question-to-model bridge**

| Research question | Empirical frame | Main model | What it can show | What it cannot show |
|:--|:--|:--|:--|:--|
| RQ1: entry | Broad coded-asset risk set; active-operation restriction as a required sensitivity | Exact one-fiscal-year lagged logit hazard with fiscal-year indicators and actual elapsed time at risk | Which prior-year age and capacity profiles are associated with first reporting positive installed capacity, and which associations survive when prior throughput must be positive | A causal retrofit effect, a verified first operating date, a full capital-history mechanism, or unrestricted fleet-wide modernization |
| RQ2: generator performance | Identifiable operating generators with positive throughput and power output | Year- and technology-adjusted OLS for logged bounded MWh/t, with facility-clustered uncertainty | How generator performance differs across age/vintage, scale, utilization, heating value, and observed technology profiles within common fiscal years | Net electricity export, complete thermodynamic efficiency, a facility fixed-effects estimate, or the causal effect of changing a plant attribute |
| Synthesis | The two linked but non-identical frames read together | Joint interpretation of entry and generator-performance evidence | Whether one average-fleet interpretation hides two different bottlenecks | A strict causal chain from adoption into generation to later generator performance |

The first frame is the coded installed-capacity entry frame. A facility is
classified as having generation capacity when reported installed power capacity
is positive. Facilities first observed without that capacity remain at risk
until they first report a positive value or until their last coded observation.
After excluding 913 left-censored facilities already reporting positive capacity
in their first observed year, the risk set contains 13,770 facility-years across
2,035 facilities, with 141 observed installed-capacity entry events.
That 141-event count is the descriptive adoption universe used for event-rate
summaries and the pathway audit. The main hazard model below uses a stricter
exact one-fiscal-year lagged subset with 98 retained events; the 42
timing-ambiguous non-adjacent events and 1 unresolved event remain in pathway
and sensitivity evidence rather than being forced into the headline hazard.

In practical terms, the entry model asks whether a facility that reported no
installed generation capacity in one fiscal year first reports positive
capacity in the next. Technically, it is an exact one-fiscal-year lagged,
discrete-time logit hazard estimated on 10,823 observations across 1,911
facilities and 98 retained events. Predictors are prior-year age band and design
capacity, fiscal-year indicators, and actual elapsed fiscal time since the
facility first entered the at-risk set. Facility-clustered standard errors
recognize that repeated observations from the same facility are not independent
draws. Elapsed time is measured from fiscal-year values rather than by counting
observed rows. This matters because missing official facility codes create gaps:
for 4,055 exact-lag observations, elapsed fiscal duration differs from the number
of observed coded rows.

The main model estimates 19 parameters, or 5.16 events per parameter. A more
saturated year-plus-prefecture fixed-effects model is retained as sensitivity
evidence because it estimates 64 parameters with 98 events, or 1.53 events per
parameter. The headline model therefore favors a smaller, auditable event-
history specification over a geographically saturated model with severe sparse-
event pressure. The exact-year restriction is also important because official
facility codes are missing in FY2010-FY2012; estimates using the previous
observed coded row are reported as sensitivity evidence rather than interpreted
as exact annual transitions. The design follows grouped event-history logic:
each coded facility-year contributes to the risk set until first event occurrence
(Allison, 1982; Beck et al., 1998). This is an observed-transition model, not a
continuous engineering model or a complete account of modernization pathways.
The lagged predictor structure ensures that facility profiles are measured
before the observed event rather than on the event row itself.

Formally, let \(A_{it}=1\) if facility \(i\) first reports positive installed
power-generation capacity in fiscal year \(t\), conditional on still being in
the at-risk set \(R_{it}=1\). The main entry model is:

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

Here, \(i\) indexes facilities, \(t\) indexes fiscal years, and \(I(\cdot)\) is
an indicator equal to 1 when the stated condition is true. The omitted age group
is 0-10 years. \(\gamma_t\) is a set of fiscal-year indicators that absorbs
conditions common to all observed facilities in each year,
\(\text{Capacity100}\) measures design capacity in 100 tonnes per day (t/day)
units, and \(D_{it}\) is actual elapsed at-risk duration in ten-fiscal-year
units. Table 2 reports average marginal effects (AMEs) in percentage points
(pp), not log-odds coefficients. For example, the broad-frame AME of -1.41 pp
for ages 10-20 means that the model-averaged annual entry probability is 1.41
percentage points lower than for the 0-10-year reference group, holding the
listed profiles and time terms at their observed values. The +0.45 pp capacity
AME is the corresponding average change associated with 100 additional t/day.
Neither number is a causal retrofit effect.

Age and capacity are therefore treated as observable pre-event facility
profiles, not isolated causal mechanisms. They may also proxy for unobserved
municipal finance, procurement timing, consolidation, routing arrangements,
technology vintage, or renewal planning. The adoption model is useful because
those profiles describe which facilities are most likely to appear in observed
installed-capacity entry; it cannot determine which institutional or engineering
channel produced that association. Age deserves particular caution because a
reported starting-year reset can make a rebuilt or recommissioned asset appear
young. The model therefore uses the prior-year profile and does not describe an
event by its potentially reset event-year age.

The broad model is an asset-entry estimand, not automatically an operating-plant
retrofit estimand. Of the 98 exact-year events, 40 have zero or missing
throughput in the prior fiscal year. They may include commissioning, rebuild,
inactive-asset, or reporting pathways. A required active-operation sensitivity
therefore restricts the risk set to positive prior-year throughput. It contains
9,215 facility-years across 1,663 facilities and 58 events and uses the same year
indicators, elapsed-duration term, and clustered uncertainty. Comparing the two
frames is part of the interpretation: an association that appears only in the
broad frame should not be generalized to conversion among operating non-
generators.

Four diagnostics bound this event definition. First, an alternative hazard
defines entry by positive electricity output rather than installed capacity; it
retains 146 exact-year events and preserves the negative age and positive scale
pattern. Second, a prior-technology sensitivity adds continuous-operation
status, gasification/melting status, and furnace count. Third, a post-entry
bridge checks whether capacity entrants become
operating generators: 128 of 141 report positive output in the event year, 135
by the following year, and 138 within the observed event-to-three-year window.
Fourth, a competing-outcome diagnostic models final disappearance from the coded
panel before FY2024. It is labelled panel exit rather than closure because code
changes, consolidation, and reporting loss cannot be ruled out.

The second frame is the canonical generator frame. It contains operating
facilities with positive throughput and positive power output, after standard
cleaning and electricity-recovery bounding. The operating-generation sample contains
6,660 rows before identifier and regression cleaning. Of those, 907 rows lack
official facility codes and are excluded from the canonical regression frame,
leaving 5,683 observations across 1,016 facilities. The dependent variable is
log gross electricity generated per tonne processed. Main predictors are
facility age, design capacity, capacity utilization, and waste heating value;
the primary model also adjusts for normalized furnace type, operating mode,
facility type, and number of furnaces.
The raw ratio divides reported electricity generation in megawatt-hours (MWh)
by reported waste throughput in tonnes. It is clipped to 0.01-0.80 MWh/t and
then log-transformed so that a few unusual administrative records do not
dominate the comparison. Capacity utilization equals annual throughput divided
by design capacity times 365 days and is capped at 1.0. The main outcome is
therefore a bounded gross electricity-recovery intensity, not net electricity
exported, revenue, overall energy recovery including heat, or full thermodynamic
efficiency. An unclipped-log sensitivity uses the positive raw MWh/t ratio
directly and preserves the main coefficient pattern.

Let \(q_{it}\) be the clipped electricity recovery ratio and let
\(y_{it}=\log(q_{it})\). The primary RQ2 model is:

$$
y_{it}
= \alpha + X_{it}'\beta + Z_{it}'\theta + \gamma_t + \varepsilon_{it},
$$

where \(X_{it}\) contains facility age, design capacity in 100 t/day units,
capped capacity utilization, and heating value; \(Z_{it}\) contains the observed
technology-configuration controls. Fiscal-year indicators \(\gamma_t\) absorb
conditions common to the observed fleet in each year. Ordinary least squares
(OLS) is used because RQ2 asks for a transparent, year-adjusted cross-facility
comparison, not a causal within-facility effect. Standard errors are clustered
by facility (Wooldridge, 2010).

Facility age is calculated from fiscal year and reported starting year. Once
fiscal-year indicators are included, its coefficient primarily contrasts
facilities of different age and technology vintage observed in the same year.
It cannot isolate biological-style aging from design vintage, durable technology,
maintenance history, or governance. The paper therefore labels it an
age/vintage association and does not interpret the coefficient as the effect of
making one plant one year older. Similarly, capacity and technology are durable
facility attributes that may be correlated with unobserved municipal choices.

A supplemental estimator ladder reports pooled OLS, OLS with year indicators,
random effects (RE), and year-indicator plus RE models. These variants show how
the associations behave under different representations of common-year and
persistent facility heterogeneity; they do not make RE exogeneity assumptions
credible by repetition. A within-between sensitivity separates facility-level
means from within-facility deviations. It is retained as a diagnostic, not a
replacement estimand, because age is mechanically related to calendar time and
because a facility fixed-effects model would absorb much of the durable scale
and vintage structure that RQ2 is explicitly designed to describe.

As a direct persistence check, the analysis also computes each facility's
percentile rank in MWh/t within each fiscal year and correlates ranks across
adjacent years. This quantity asks whether a relatively high-performing plant
usually remains relatively high-performing one year later without assuming that
the exact MWh/t level is unchanged.

Because the dependent variable is logged, small coefficients can be read as
approximate proportional differences. In the primary model, the age/vintage
coefficient of -0.0329 corresponds to approximately 3.2% lower gross MWh/t per
additional age year in a conditional cross-facility comparison. The capacity
coefficient of 0.1103 corresponds to approximately 11.7% higher gross MWh/t per
additional 100 t/day using \(100[\exp(0.1103)-1]\). These are model-based
comparisons, not forecasts of the gain from changing one facility's age or
capacity.

The electricity-recovery results should therefore be read as conditional patterns within
the canonical regression frame, not as estimates for the entire generating
fleet. This frame is intentionally narrower than the operating-generator
universe because the argument depends on facility-level comparison over time.
Rows without official facility codes cannot support that comparison. The frame
is better understood as the canonical identifiable generator sample than as a
census of all generation activity. The supplement compares included and
uncoded operating-generator rows; the uncoded rows are concentrated in
FY2010-FY2012, so period comparisons are treated as coded-window diagnostics
rather than as a clean Fukushima-era identification design. The paper also uses
a bounded electricity-recovery metric because the empirical question is not
boiler thermodynamics in isolation, but administrative performance in
electricity recovered per tonne processed. That puts the paper closer to applied
energy-recovery studies than to plant-level engineering optimization alone
(Grosso et al., 2010; Münster & Meibom, 2010; Shino, 2019).

Two administrative-data checks are reported in the supplement. First, a small
set of official facility codes appears more than once within the same fiscal
year, so a composite identifier (ID) sensitivity appends facility names to
affected duplicate codes. Second, heating value is treated as a noisy control
and is checked under plausible-value restrictions. The resulting validation
frame contains 4,971 rows. Two convergent outcomes are modeled with year and
technology controls: a gross thermal-conversion proxy, calculated as gross
MWh/t times 3.6 divided by heating value in MJ/kg, and the survey's reported
generation-efficiency measure. Their logged values correlate at 0.8636 and both
preserve the negative age/vintage and positive scale and utilization
associations. An exact-adjacent-year model using lagged predictors also preserves
the pattern. These are robustness checks, not independent experiments: both
engineering outcomes derive from related administrative fields. The checks are
reported as disclosure and convergent validation rather than as an attempt to
remove all uncertainty from the source panel.

Generative AI tools were used during code development and review to suggest
implementations, test cases, documentation structure, and reproducibility
checks. The author executed the pipeline, inspected source records and generated
outputs, checked reported quantities against machine-readable manifests, and
retained responsibility for all variable definitions, model choices,
interpretations, and revisions. The tools did not autonomously acquire, alter,
or validate the underlying administrative data.

The two layers belong in one paper because they answer complementary parts of the
same modernization problem. The adoption layer identifies which coded assets
appear to enter the generating regime and tests whether the result changes when
attention is limited to active non-generators. The electricity-recovery layer
identifies whether performance differences remain once facilities are inside
that regime. Without the first layer, the paper would reduce transition to
generator performance alone. Without the second, it would say who enters
generation but not where entrants sit in the later performance distribution.

The design is diagnostic rather than structural. It models observed transition
within the coded risk set, not unrestricted fleet-wide modernization, and it
models conditional generator performance within the canonical identifiable
generator frame, not a causal effect of changing age, scale, utilization, or
technology. The low within-facility variance ratio is used only to describe the
data structure; it does not resolve omitted-variable concerns or turn any model
into a causal estimate. The defended claim is therefore narrower: under explicit
sample limits, the frames reveal different observed margins in the same fleet.

**Table 1. Linked analytical framework**

| Margin | Linked sample | Empirical question | Paper role |
|:--|:--|:--|:--|
| Installed-capacity entry margin | Broad coded risk set: 13,770 facility-years, 2,035 facilities, 141 observed events; exact-year model: 10,823 rows and 98 events | Which prior-year profiles predict broad coded-asset entry? | Identifies robust scale selectivity and a broad-frame age gradient |
| Active-conversion sensitivity | Positive-prior-throughput exact-year frame: 9,215 rows, 1,663 facilities, 58 events | Do entry associations persist among facilities demonstrably operating one year earlier? | Shows that scale persists while the age gradient attenuates |
| Electricity-recovery margin | Canonical generator frame: 5,683 observations across 1,016 operating generators | How does gross electricity generated per tonne vary once generation already exists? | Shows whether mature generator performance remains structured |
| Synthesis | Two linked but non-identical analytical frames | Would one average-fleet view misstate the modernization bottleneck? | Shows why entry and mature performance should not be read as one average process |

*Note: entry is estimated with lagged discrete-time hazards. Generator
performance is estimated primarily with year- and technology-adjusted OLS;
pooled, year-indicator, and random-effects (RE) variants are supplementary. The
year indicators are not facility fixed effects.*

## 4. Results

### 4.1 Installed-capacity entry is selective rather than diffuse

The most stable entry result is scale selectivity. In the exact-year risk set,
annual event rates rise from 0.15% in the smallest prior-year capacity quartile
to 2.49% in the largest; the largest quartile contains 62 of the 98 modeled
events. Raw prior-year age rates are less simple: 1.97% at ages 0-10, 0.18% at
10-20, 0.72% at 20-30, and 1.68% at 30 or more. The older raw rate partly
reflects the broad asset risk set and should not be read as an adjusted or active-
conversion effect. Events are also clustered in time: 109 of all 141 events
occur in FY2013-FY2019. This is reported as an administrative-panel feature, not
an identified policy shock; the hazard includes fiscal-year indicators.

In the broad coded-asset model, adjusted age-band AMEs are negative relative to
the 0-10-year reference: -1.41 percentage points (pp) at ages 10-20, -1.45 pp at
20-30, and -0.83 pp at 30 or more. Each additional 100 t/day of prior-year
design capacity is associated with a +0.45 pp annual entry probability. The
model contains actual elapsed at-risk duration and has a deviance-based pseudo-
R-squared of 0.1920. These quantities refer to first reporting positive
installed capacity, not to changes in electricity output or engineering
efficiency.

The active-operation sensitivity changes the interpretation of age but not
scale. After requiring positive prior-year throughput, the capacity AME remains
+0.44 pp and is precisely estimated. The age differences shrink to -0.67 pp,
-0.56 pp, and -0.29 pp; only the first is conventionally significant at the 1%
level, the second has p=0.064, and the oldest group has p=0.329. The defensible
headline is therefore not that operating older plants universally fail to
convert. It is that entry is consistently scale-selective, while the age
gradient depends on whether the estimand includes commissioning, rebuild, or
inactive-asset pathways.

Other checks preserve the central distinction. Adding prior observed technology
profiles to the broad model leaves the capacity AME positive (+0.34 pp) and the
broad-frame age AMEs negative. Defining the event by first positive electricity
output also preserves negative age and positive capacity associations. The
saturated year-plus-prefecture model, broader previous-observed-row frame, p99
capacity cap, and log-capacity form do not reverse the scale result. These checks
reduce concern that scale selectivity is created by one capacity tail or by the
installed-capacity field alone; they do not make the event mechanism causal.

The pathway audit bounds rather than identifies mechanism. Of 141 events, 50
are reset- or rebuild-like adjacent-year events, 36 are adjacent-year
continuity-type upgrades, 12 are forward-dated or placeholder entries, 42 are
timing-ambiguous non-adjacent coded-row events, and 1 is unresolved. The mix is
consistent with heterogeneous capital pathways, but it cannot establish
replacement, major refurbishment, new build, or reporting change as the unique
mechanism. The result is therefore selective observed entry, not technological
inevitability or proof that older plants cannot upgrade.

Panel disappearance is an important competing observed path. Among 1,894
facilities with no installed-capacity event, 1,305 (68.9%) are last observed
before FY2024. In a separate next-year hazard, facilities aged 30 years or more
are 2.60 pp more likely than the 0-10-year group to record final coded-panel
exit, whereas each additional 100 t/day of capacity is associated with a 1.63
pp lower exit probability. The younger age bands are not statistically
distinguishable from the reference group. Panel exit is not verified physical
closure because identifier change, consolidation, and reporting loss remain
possible. It nevertheless shows why every non-entrant cannot be assumed to
remain continuously observed and operating through FY2024.

![Figure 2. Average marginal effects and facility-clustered 95% confidence intervals for broad coded-asset entry, active conversion requiring positive prior-year throughput, and final coded-panel exit. Entry hazards use exact one-fiscal-year lags, fiscal-year indicators, and actual elapsed at-risk duration. Panel exit is not equivalent to verified closure.](../figures/figure2_selective_transition.png)

**Table 2. Lagged hazard results for broad entry, active conversion, and coded-panel exit**

| Variable | Broad asset-entry AME (pp) | Active-conversion AME (pp) | Panel-exit AME (pp) |
|:--|--:|--:|--:|
| Prior-year age 10-20 years (versus 0-10) | -1.41 (0.21) | -0.67 (0.21) | -0.42 (0.54) |
| Prior-year age 20-30 years (versus 0-10) | -1.45 (0.33) | -0.56 (0.30) | 0.18 (0.57) |
| Prior-year age 30+ years (versus 0-10) | -0.83 (0.35) | -0.29 (0.30) | 2.60 (0.85) |
| Prior-year capacity (per 100 t/day) | 0.45 (0.15) | 0.44 (0.09) | -1.63 (0.32) |

| Model summary | Broad asset entry | Active conversion |
|:--|--:|--:|
| Observations | 10,823 | 9,215 |
| Facilities | 1,911 | 1,663 |
| Installed-capacity entry events | 98 | 58 |
| Pseudo-R-squared | 0.1920 | Not used for comparison |

*Note: entries are AMEs in pp, with facility-clustered standard errors in
parentheses. The first two columns are exact one-fiscal-year lagged logit hazards
with fiscal-year indicators and actual elapsed at-risk duration. The active-
conversion column additionally requires positive prior-year throughput. The 98
broad events are the exact-year subset; the descriptive audit contains 141. The
panel-exit diagnostic uses 12,108 facility-years, 2,022 facilities, and 1,285
final coded-panel exits before FY2024. Exit is an administrative-panel outcome,
not verified physical closure.*

### 4.2 Electricity recovery within generation is strongly structured

Within the canonical regression frame, generators differ persistently from one
another. The within-to-total variance ratio of pooled log electricity-recovery
intensity is 0.1499, so most observed variation lies between facilities rather
than within the same facility over time. More directly, 4,368 exact
adjacent-year pairs across 915 facilities have a pooled within-year percentile-
rank correlation of 0.9325; the median annual correlation is 0.9323, with a
range of 0.8848-0.9763. A high-performing facility therefore usually remains
high-ranked one year later, even though its exact MWh/t can change.

The variance ratio remains low in both the early and later coded windows,
falling from 0.1795 in FY2005-FY2009 to 0.0956 in FY2013-FY2024. This is not a
Fukushima identification design because FY2010-FY2012 operating-generator rows
lack official facility codes. These diagnostics show persistence in relative
performance, not that operations never change or that vintage has been causally
isolated from technology, governance, maintenance, or other durable plant
characteristics.

The primary coefficient patterns point in the same direction. Within common
fiscal years and conditional on observed furnace type, operating mode, facility
type, and furnace count, gross electricity recovery is lower at older-vintage
facilities and higher at larger and more fully utilized facilities. The
age/vintage coefficient is -0.0329, the capacity coefficient is +0.1103 per 100
t/day, and the utilization coefficient is +0.7600. Heating value is not
statistically distinguishable from zero in this specification. The base model
without technology controls yields nearly the same coefficients, while the
added controls increase R-squared from 0.3699 to 0.3830.

The emphasis is on structured conditional association rather than on a forecast
of what would happen if policy changed one plant's age, capacity, or utilization.
This is consistent with earlier facility-level work showing that energy-recovery
performance is uneven across operating incinerators and that plant scale and
operational intensity matter for output performance (Chen et al., 2012; Sasao,
2018; Shino, 2019; Yeh, 2020; Grosso et al., 2010). The supplemental within-
between analysis preserves the same direction in the cross-facility component:
between-facility age/vintage is negative, while between-facility capacity and
utilization are positive.

![Figure 3. Mean bounded gross electricity generation per tonne by facility-age group with facility-clustered 95% confidence intervals, and adjacent-year within-year percentile-rank correlations.](../figures/figure3_efficiency_structure.png)

The electricity-recovery margin therefore looks structured rather than static.
Facilities vary through utilization and operating conditions, but age/vintage
and scale differences remain strong in the observed data. This is where the paper
diverges from a simple engineering-upgrade narrative. Recent large-scale Chinese
studies show that substantial gains can still be unlocked through technology
upgrades, pollutant control, waste classification, and load-rate improvements,
but they do so within already-generating systems rather than at the point of
first entry (Liu et al., 2025; Han et al., 2025). The present results are
consistent with a persistent observed generator ranking rather than automatic
convergence after entry.

This is why the intensive margin cannot be inferred from the entry margin alone.
A facility can report installed capacity and produce electricity while still
occupying a different relative performance position from its peers. The data do
not establish how much a specific operational intervention could close those
gaps. They show that observed generator performance is structured and highly
persistent rather than a simple continuation of capacity entry.

For interpretation, this matters as much as the adoption result. If the paper
only documented selective entry, a reader could infer that the main task was
simply to push more facilities into generation. If it only documented generator
hierarchy, a reader could infer that non-generators were just lagging versions
of the same problem. The linked result makes both shortcuts inadequate. The fleet appears
divided between a segment that still struggles to enter generation and a segment
where entry has occurred but performance remains uneven and structured.

**Table 3. Primary electricity-recovery specifications in the canonical generator frame**

| Variable | Base year-adjusted OLS | Primary year + technology OLS |
|:--|--:|--:|
| Facility age/vintage (years) | -0.0348 (0.0023) | -0.0329 (0.0023) |
| Capacity (100 t/day) | 0.1051 (0.0087) | 0.1103 (0.0101) |
| Capacity utilization | 0.7760 (0.1351) | 0.7600 (0.1319) |
| Heating value (MJ/kg) | 0.0033 (0.0021) | 0.0032 (0.0020) |
| Fiscal-year indicators | Yes | Yes |
| Technology-configuration controls | No | Yes |
| Observations | 5,683 | 5,683 |
| Facilities | 1,016 | 1,016 |
| R-squared | 0.3699 | 0.3830 |

*Note: OLS means ordinary least squares and MJ/kg means megajoules per kilogram.
Technology controls are normalized furnace type, operating mode, facility type,
and number of furnaces. Standard errors are clustered by facility and reported
in parentheses. In both columns, age, capacity, and utilization have p < 0.001;
heating value has p > 0.10. Fiscal-year indicators are not facility fixed
effects. Coefficients are conditional associations rather than structural
causal parameters. The pooled and random-effects estimator ladder is reported in
the supplement.*

Engineering-oriented outcome checks support, but do not independently prove,
the same pattern. In the 4,971-row plausible-value frame, models of the thermal-
conversion proxy and reported generation efficiency retain negative age/vintage
and positive capacity and utilization coefficients after year and technology
adjustment. The two logged validation outcomes correlate at 0.8636 because they
are constructed from related survey fields. An exact-adjacent-year model using
lagged predictors also preserves all three signs. These checks show that the main
result is not unique to the clipping rule or same-year MWh/t specification; they
do not identify an engineering intervention effect.

### 4.3 Why the two results belong together

Read together, the two margins change the modernization story without forming a
strict causal chain. The entry analysis shows robust scale selectivity and a
risk-set-dependent age pattern. The generator analysis shows durable cross-
facility performance structure after entry. A one-average-fleet model would
obscure where each observation sits: outside generation, newly entering, or
already generating. The evidence does not establish how far a particular
facility could move under an intervention.

The post-entry trajectory makes the empirical connection observable. Of 141
installed-capacity entrants, 137 appear in the canonical operating-generator
frame within three years, contributing 389 event-time observations. At event
time zero, 125 observed entrants average 0.324 MWh/t versus 0.329 MWh/t among
same-year incumbent generators, and their mean within-year percentile is 51.5.
Here, an incumbent is a generator with no observed entry event or with an event
in an earlier fiscal year.
At event times one, two, and three, mean entrant percentiles are 54.8, 52.1, and
52.9. The corresponding entrant-minus-incumbent mean differences are +0.009,
-0.010, and -0.001 MWh/t. On average, entrants therefore appear near the middle
of the contemporaneous generator distribution rather than entering at either an
obvious frontier or a persistent bottom position.

The trajectory is descriptive and increasingly selected. Events represented
fall from 125 at event time zero to 71 at event time three, and confidence
intervals widen. Entrants that were operating in the prior year begin below the
median generator rank, whereas entrants with zero/missing prior throughput or no
exact prior-year row begin higher. The pathway audit likewise places in-place
continuity entrants below reset/rebuild-like entrants at event time zero. These
subgroup contrasts are clues that commissioning and in-place conversion are not
interchangeable pathways, but they are not causal estimates: the groups are
small, selected, and defined from administrative continuity rules.

![Figure 4. Early post-entry performance. Panel A compares entrants with same-year incumbent generators in gross MWh/t. Panel B reports entrants' mean within-year generator percentile by prior operating status. Points show means and bars show 95% confidence intervals; event counts decline over time.](../figures/figure4_post_entry_trajectories.png)

Only three entrants reverse the capacity flag in an observed next year, and 135
of 141 report positive output by the following year. Installed-capacity entry is
therefore usually followed by measurable operation, but neither the event nor
the trajectory proves that entry itself causes a facility's subsequent rank.

The panel-exit diagnostic completes the interpretation on the other side. Some
facilities observed without capacity enter, some remain observed without entry,
and many disappear from the coded panel before its endpoint. Because the data do
not verify closure, these are three observed administrative paths rather than a
complete physical fate model. Recognizing all three prevents the paper from
mistaking sample attrition for permanent non-adoption or from treating capacity
entry as the same outcome as subsequent performance.

## 5. Discussion

The paper's main interpretive claim is methodological and empirical: broad asset
entry, conversion of an operating non-generator, and performance after entry
are not interchangeable outcomes. Modeling them separately prevents a national
fleet share from being mistaken for a single modernization process. It also
reveals where an apparently intuitive result is robust and where it is not.

On the entry margin, larger prior-year design capacity predicts first reporting
of generation capacity in both the broad asset frame and the positive-prior-
throughput frame. The broad model also shows lower adjusted entry among older
age bands, but that gradient attenuates sharply among operating non-generators.
This is substantively important: 40 of 98 exact-year events do not follow
positive prior-year throughput, so commissioning, rebuild, and inactive-asset
pathways materially shape the broad result. On the generator margin,
age/vintage, scale, and utilization remain associated with gross MWh/t after
common-year and observed-technology adjustment, and adjacent-year ranks are
highly correlated. The post-entry trajectory adds a third observation: entrants
appear near the middle of the same-year generator distribution on average, not
at an automatic performance frontier. Panel exit remains a competing observed
administrative outcome, especially for the oldest non-generating assets.

This is why the contribution is not merely the common-sense statement that new
or large plants perform better. The analysis tests that expectation against
alternative populations and outcomes. It finds a stable scale pattern, a frame-
sensitive age pattern, and no automatic post-entry ranking advantage. Those
boundaries are more informative for future causal or engineering work than a
single fleet-average association.

This makes the paper useful as a planning diagnostic rather than as an
intervention ranking. The practical value is triage: deciding which part of the
fleet needs an entry-side asset question and which part needs a generator-side
performance question. Table 4 translates the empirical patterns into defensible
planning questions while keeping the claim boundaries explicit.
In practical terms, the design gives planners a screening sequence: first decide
whether a facility is an entry-side asset problem or an already-generating
performance problem, then decide which more detailed engineering, governance, or
capital-history review is worth pursuing.

**Table 4. Planning diagnostic implied by the two-margin evidence**

| Empirical pattern | Planning use | Boundary condition |
|:--|:--|:--|
| Scale-selective entry in both risk sets | Examine whether small non-generators have sufficient waste supply and system scale before assuming an electricity-recovery project is comparable to a large-plant project | The association does not prove that increasing capacity would cause entry |
| Broad-frame age gradient attenuates among active plants | Separate commissioning/rebuild cases from conversion of an operating plant before using age to screen options | Older operating plants are not proven unable to convert |
| Mixed event pathways | Check asset histories before treating adoption as one retrofit mechanism | The audit does not distinguish replacement, refurbishment, and reporting change with certainty |
| Older/smaller panel exit | Verify closure, recoding, consolidation, or reporting status before interpreting continued non-entry | Administrative disappearance is not verified physical closure |
| Structured generator performance | Compare generators with similar age, scale, and utilization before judging improvement room | Coefficients are conditional associations, not causal effects |
| Entrants begin near the middle of the generator distribution | Evaluate entry and later operational performance as separate milestones | The event-time trajectory is selected and does not estimate an entry effect |

The interpretation has clear limits. The 58-event active-conversion model is
sparse, and changing the risk set changes both the estimand and the population;
the attenuation is not a formal test that the broad and active coefficients are
equal. The pathway audit cannot prove replacement, refurbishment, or
commissioning as a unique mechanism. The generator regression adjusts for
observed technology configuration but not municipal finance, contracting,
maintenance quality, waste composition, or complete retrofit history. Installed
capacity may not describe usable capacity, gross output does not equal net
electricity export, heat recovery is not measured, and panel exit is not verified
closure. Post-entry follow-up declines from 125 events at time zero to 71 at time
three, so the trajectory is vulnerable to selective observation. The defended
claim is therefore narrower: scale-selective observed entry, a frame-dependent
age association, and structured post-entry performance are documented outcomes,
not a uniquely identified mechanism or intervention hierarchy. The supplement
makes these limits auditable through pathway rules, identifier checks, outcome
validation, and estimator variants.

The results do not identify the best intervention for any individual
municipality. They indicate that planning assessments should first distinguish
facilities outside electricity recovery from operating generators, because the
observable constraints differ across those groups. For non-generators, the
evidence supports checking scale, prior operation, and capital history before
deciding whether renewal, consolidation, conversion, or continued non-generation
is plausible. For the already-generating segment, the
evidence supports a different diagnostic question: whether an existing generator
has realistic room for operational or capital improvement within its observed
age, scale, and utilization context.

That distinction is administrative as well as technical. Japanese waste systems
are organized through municipalities whose planning boundaries do not always
align with efficient waste sheds, and intermunicipal reorganization has its own
political costs and institutional legacies (Rausch, 2006; Sakai et al., 2008).
In that setting, collapsing non-generators and generators into one average
segment risks hiding the difference between entry-side asset decisions, which
are lumpy and governance-heavy, and generator performance assessment, which is
more incremental and operational.

If entry and performance were one common process, a single fleet-average
modernization story would be adequate. The evidence instead points to three
diagnostic starting points: whether the record represents an asset entry or an
active conversion, whether scale makes the project structurally comparable, and
how performance should be evaluated after generation begins.

The analytical split is potentially transferable beyond Japan, but the
coefficients are not. It is most relevant to systems where administrative data
contain both facilities without energy-recovery equipment and repeated output
records for operating generators. Replication elsewhere would require locally
valid identifiers, capacity definitions, closure histories, electricity-use
boundaries, and governance variables. In systems where nearly every plant
already generates or where net heat and electricity exports are measured
jointly, the relevant margins and outcome definitions would differ.

The broader policy context points in the same direction. Comparative waste
policy studies and European framework discussions both treat waste-to-energy as
valuable only when embedded inside a wider hierarchy that preserves prevention,
reuse, and recycling priorities (Sakai et al., 2011; European Commission,
2017). The empirical split helps explain why those hierarchies matter. A
municipal system can have real energy-recovery gains available at the
non-generating margin while still facing a different, narrower set of decisions
inside the already-generating segment.

For climate interpretation, the relevant question is not simply whether a plant
generates, but what kind of generator it is and how much improvement remains
inside that segment. Waste-to-energy performance is judged against both an
internal engineering standard and the emissions profile of the broader energy
system, including the avoided-emissions logic built into carbon accounting
(Astrup et al., 2009; Münster & Meibom, 2010). In Japan's current
decarbonization setting, where national inventories and scenario work track
sectoral emissions and energy mix changes, the two-part design is useful
because it keeps those questions separate (Greenhouse Gas Inventory Office of
Japan & Ministry of the Environment Japan, 2024; Yamada et al., 2023).

That separation is also what makes the paper more understandable for a planning
audience. Municipal systems rarely choose among abstract technological ideals.
They decide whether to renew an aging non-generator, coordinate waste routing
toward a larger plant, maintain an existing generator, or invest in an upgrade
for a plant that already produces electricity. Those are related decisions, but
they are not interchangeable. Keeping the extensive and intensive margins
separate helps planners locate the bottleneck without relying on one blended
fleet mean.

## 6. Conclusion

In the observed facility panel, Japan's electricity-recovery modernization does
not appear as one smooth fleet-wide process. First reporting of positive
installed capacity is consistently scale-selective, but its age pattern depends
on whether the risk set includes all coded assets or only facilities operating in
the prior year. Final coded-panel exit is a competing administrative outcome.
Among identifiable generators, gross MWh/t remains associated with age/vintage,
scale, and utilization after common-year and observed-technology adjustment,
and adjacent-year ranks are highly correlated. Most capacity entrants soon
report positive output and, on average, enter near the middle of the same-year
generator distribution; this does not imply that entry causes their rank. The
paper does not identify one pathway or best intervention. It shows why fleet
assessment should first distinguish asset entry from active conversion and then
evaluate post-entry performance separately. That sequence provides a more
defensible foundation for later engineering, capital-history, and causal work
than one blended fleet average.

## Acknowledgements

The author thanks Prof. Han Ji for supervision and critical feedback during the
development of the underlying thesis project from which this paper is derived.

## Funding

This research did not receive any specific grant from funding agencies in the
public, commercial, or not-for-profit sectors.

## Contributor Roles Taxonomy (CRediT) Authorship Contribution Statement

Pann Phetra: Conceptualization, Data curation, Formal analysis, Investigation,
Methodology, Visualization, Writing - original draft, Writing - review &
editing.

## Declaration of Competing Interest

The author declares no known competing financial interests or personal
relationships that could have appeared to influence the work reported in this
paper.

## Ethical Approval

This study uses publicly released administrative facility data and does not
involve human participants, animal subjects, or private personal data.

## Data Availability

The facility-level source data are derived from the Ministry of the Environment
Japan General Waste Treatment Survey, which is publicly released by the Ministry
of the Environment. Subject to source-file redistribution conditions, the author
will deposit the analysis code, machine-readable result manifests, derived
tables, figure-generation scripts, and manuscript figures in a versioned
repository associated with the submitted paper. Raw source workbooks can be
obtained from the Ministry and e-Stat portals.

## Declaration of Generative AI and AI-Assisted Technologies in the Manuscript Preparation Process

During the preparation of this manuscript, the author used OpenAI Codex and
Anthropic Claude for language revision, manuscript organization, and assistance
with code development and review. The author executed the analyses, inspected
the source data and generated outputs, independently checked the reported
results, reviewed and edited all AI-assisted material, and takes full
responsibility for the content. These tools were not used as authors and did not
replace author judgment or accountability.

## References

Allison, P. D. (1982). Discrete-time methods for the analysis of event histories.
*Sociological Methodology*, *13*, 61-98. https://doi.org/10.2307/270718

Astrup, T., Møller, J., & Fruergaard, T. (2009). Incineration and
co-combustion of waste: Accounting of greenhouse gases and global warming
contributions. *Waste Management & Research*, *27*(8), 789-799.
https://doi.org/10.1177/0734242X09343774

Astrup, T. F., Tonini, D., Turconi, R., & Boldrin, A. (2015). Life cycle
assessment of thermal waste-to-energy technologies: Review and recommendations.
*Waste Management*, *37*, 104-115.
https://doi.org/10.1016/j.wasman.2014.06.011

Beck, N., Katz, J. N., & Tucker, R. (1998). Taking time seriously:
Time-series-cross-section analysis with a binary dependent variable. *American
Journal of Political Science*, *42*(4), 1260-1288.
https://doi.org/10.2307/2991857

Brunner, P. H., & Rechberger, H. (2015). Waste to energy - key element for
sustainable waste management. *Waste Management*, *37*, 3-12.
https://doi.org/10.1016/j.wasman.2014.02.003

Cui, J., Cui, Y., Li, J., Gao, X., Wei, W., Chen, Y., Ma, W., Zhu, N., Geng,
Y., Zhao, Y., & Lou, Z. (2026). Efficiency hierarchy and optimization of waste
incineration in China to balance disposal and energy supply. *Nature
Communications*, *17*(1), Article 3069.
https://doi.org/10.1038/s41467-026-69897-w

Chen, P.-C., Chang, C.-C., Yu, M.-M., & Hsu, S.-H. (2012). Performance
measurement for incineration plants using multi-activity network data
envelopment analysis: The case of Taiwan. *Journal of Environmental
Management*, *93*(1), 95-103. https://doi.org/10.1016/j.jenvman.2011.08.011

e-Stat. (n.d.). *Nation Survey on the State of Discharge and Treatment of
Municipal Solid Waste* (Statistics code 00650101). Portal Site of Official
Statistics of Japan. https://www.e-stat.go.jp/en/statistics/00650101 (accessed
10 July 2026).

European Commission. (2017). *The role of waste-to-energy in the circular
economy* (COM(2017) 34 final). European Commission.
https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52017DC0034

Geels, F. W. (2004). From sectoral systems of innovation to socio-technical
systems: Insights about dynamics and change from sociology and institutional
theory. *Research Policy*, *33*(6-7), 897-920.
https://doi.org/10.1016/j.respol.2004.01.015

Greenhouse Gas Inventory Office of Japan & Ministry of the Environment Japan.
(2024). *National greenhouse gas inventory report of Japan 2024*. Center for
Global Environmental Research, National Institute for Environmental Studies.
https://cger.nies.go.jp/publications/report/i170/en/

Grosso, M., Motta, A., & Rigamonti, L. (2010). Efficiency of energy recovery
from waste incineration, in the light of the new Waste Framework Directive.
*Waste Management*, *30*(7), 1238-1243.
https://doi.org/10.1016/j.wasman.2010.02.036

Han, Q.-l., Liu, H.-q., Gong, Y.-y., Tao, J.-y., Sun, Y.-n., Wei, G.-x., Zhu,
Y.-w., & Chen, G.-y. (2025). Strengthening pollutant control and resource
recovery can enhance sustainable waste incineration in China. *Communications
Earth & Environment*, *6*, Article 863.
https://doi.org/10.1038/s43247-025-02859-0

Liu, B., Wang, P., Zhou, J., Guo, Y., Ma, S., Chen, W.-Q., Li, J., & Chang,
V. W.-C. (2025). Refocusing on effectiveness over expansion in urban
waste-energy-carbon development in China. *Nature Energy*, *10*, 215-225.
https://doi.org/10.1038/s41560-024-01683-8

Ministry of the Environment Japan. (2026). *General Waste Treatment Survey
results: FY2024 municipal solid waste treatment survey*. Environmental
Management Bureau, Ministry of the Environment Japan.
https://www.env.go.jp/recycle/waste_tech/ippan/ (accessed 10 July 2026).

Münster, M., & Meibom, P. (2010). Long-term affected energy production of waste
to energy technologies identified by use of energy system analysis.
*Waste Management*, *30*(12), 2510-2519.
https://doi.org/10.1016/j.wasman.2010.04.015

Rausch, A. (2006). The Heisei Dai Gappei: A case study for understanding the
municipal mergers of the Heisei era. *Japan Forum*, *18*(1), 133-156.
https://doi.org/10.1080/09555800500498558

Sakai, S., Ikematsu, T., Hirai, Y., & Yoshida, H. (2008). Unit-charging
programs for municipal solid waste in Japan. *Waste Management*, *28*(12),
2815-2825. https://doi.org/10.1016/j.wasman.2008.07.010

Sakai, S., Yoshida, H., Hirai, Y., Asari, M., Takigami, H., Takahashi, S.,
Tomoda, K., Peeler, M. V., Wejchert, J., Schmid-Unterseh, T., Douvan, A. R.,
Hathaway, R., Hylander, L. D., Fischer, C., Oh, G. J., Jinhui, L., & Chi, N.
K. (2011). International comparative study of 3R and waste management policy
developments. *Journal of Material Cycles and Waste Management*, *13*(2),
86-102. https://doi.org/10.1007/s10163-011-0009-x

Sasao, T. (2018). How does municipal solid waste policy affect heat and
electricity produced by incinerators? *Detritus*, *2*, 133-141.
https://doi.org/10.31025/2611-4135/2018.13650

Seto, K. C., Davis, S. J., Mitchell, R. B., Stokes, E. C., Unruh, G., &
Urge-Vorsatz, D. (2016). Carbon lock-in: Types, causes, and policy
implications. *Annual Review of Environment and Resources*, *41*(1), 425-452.
https://doi.org/10.1146/annurev-environ-110615-085934

Shino, Y. (2019). System analysis of MSW incinerator power generation
performance. *Journal of the Japan Society of Material Cycles and Waste
Management*, *30*, 113-121. https://doi.org/10.3985/jjsmcwm.30.113

Sun, L., Fujii, M., Tasaki, T., Dong, H., & Ohnishi, S. (2018). Improving waste
to energy rate by promoting an integrated municipal solid-waste management
system. *Resources, Conservation and Recycling*, *136*, 289-296.
https://doi.org/10.1016/j.resconrec.2018.05.005

Tabata, T., & Tsai, P. (2016). Heat supply from municipal solid waste
incineration plants in Japan: Current situation and future challenges. *Waste
Management & Research*, *34*(4), 345-351.
https://doi.org/10.1177/0734242X15617009

Uno, S. (2015). Trends in Waste-to-Energy Technologies for High Efficiency
Power Generation. *Material Cycles and Waste Management Research*, *26*(2),
114-119. https://doi.org/10.3985/mcwmr.26.114

Unruh, G. C. (2000). Understanding carbon lock-in. *Energy Policy*, *28*(12),
817-830. https://doi.org/10.1016/S0301-4215(00)00070-7

Wooldridge, J. M. (2010). *Econometric analysis of cross section and panel
data* (2nd ed.). MIT Press.

Yamada, K., Ii, R., Yamamoto, M., Ueda, H., & Sakai, S. (2023). Japan's
greenhouse gas reduction scenarios toward net zero by 2050 in the material
cycles and waste management sector. *Journal of Material Cycles and Waste
Management*, *25*(4), 1807-1823.
https://doi.org/10.1007/s10163-023-01650-7

Yeh, L.-T. (2020). Analysis of the dynamic electricity revenue inefficiencies
of Taiwan's municipal solid waste incineration plants using data envelopment
analysis. *Waste Management*, *107*, 28-35.
https://doi.org/10.1016/j.wasman.2020.03.040
