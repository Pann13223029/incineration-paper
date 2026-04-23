# Selective Modernization and Bounded Responsiveness in Japan's Waste-Incineration Fleet: A Facility-Level Panel Study

## Abstract

Japan relies heavily on municipal waste incineration, yet a large share of its
incineration fleet still does not convert waste heat into electricity. A
one-average-fleet view therefore risks treating all plants as though they face
one modernization problem, even though non-generators must first enter
generation and mature generators must improve conditional performance.
Fleet-average studies blur those margins, while generator-only studies miss the
extensive margin altogether. Using Ministry of the Environment data for
FY2005-FY2024, this paper estimates both within one national facility panel. It
first models observed transition into generation among coded facilities first
seen without it, then models energy recovery efficiency within a canonical
regression frame of operating generators. Within the coded at-risk frame,
transition is selective rather than diffuse: older facilities are less likely
than 0-10 year facilities to record transition in the next observed year, while
larger facilities are more likely to do so. Within the canonical regression
frame, efficiency is lower at older plants and higher at larger, more fully
utilized ones, while between-facility heterogeneity dominates within-facility
movement. A one-average-fleet view therefore understates both the selectivity
of entry and the persistence of performance hierarchy. These patterns are
descriptive within the paper's linked samples rather than causal estimates of a
single modernization mechanism. For municipal fleet planning, non-generators
and mature generators should not be managed as one average segment.

**Keywords:** waste incineration; waste-to-energy; Japan; energy recovery;
facility panel; transition

## 1. Introduction

Japan operates one of the world's most incineration-dependent municipal waste
systems, yet a large share of the fleet still burns waste without generating
electricity from the heat it produces (Ministry of the Environment Japan, 2022;
Uno, 2015; Tabata & Tsai, 2016; Sakai et al., 2011). This reliance is not an
accident of recent policy fashion. For decades, municipal waste governance in
Japan has treated thermal treatment as a core option for hygienic disposal,
volume reduction, and local waste autonomy, while limited landfill space and
strict environmental control pushed municipalities toward increasingly
sophisticated incineration infrastructure (Brunner & Rechberger, 2015; Sakai et
al., 2011). Sectoral planning now treats the remaining gap in electricity
generation not only as an engineering issue but also as part of the waste
sector's decarbonization challenge (Yamada et al., 2023; Greenhouse Gas
Inventory Office of Japan & Ministry of the Environment Japan, 2024). The
transition problem is therefore not whether incineration exists, but which
facilities move into useful energy recovery and what performance looks like
once they do.

That pattern is easy to flatten into one average fleet story. But the relevant
questions are not the same. One is extensive: which facilities record observed
transition into power generation at all? The other is intensive: among plants
that already generate, which facilities achieve high energy recovery
efficiency? An average-fleet view can therefore make the system look uniformly
slow, when the real pattern may be selective entry at one end of the fleet and
persistent performance hierarchy at the other.

This paper estimates both margins in one national facility-level panel. Its
contribution is not simply that it studies Japan, but that it does what
fleet-average studies and generator-only studies usually do not: it uses one
linked dataset to estimate observed transition into generation and conditional
performance within generation side by side. Fleet-average studies blur entry
and performance, while generator-only studies miss who enters generation at
all. Within the coded at-risk frame, observed transition is selective toward
younger and larger facilities. Within the canonical regression frame,
efficiency is strongly structured by age, scale, and utilization, while
within-facility movement remains limited relative to between-facility
heterogeneity. The contribution is therefore empirical and design-based rather
than rhetorical: it shows that the same fleet can appear merely slow in the
aggregate while actually containing one selective transition problem and one
bounded-performance problem.

The gap addressed here is narrower than a generic claim that Japan has been
understudied. Waste-to-energy research can describe fleet trajectories, and
generator-only studies can explain conditional performance once plants already
operate as generators. What remains uncommon is one linked municipal-fleet
analysis that estimates both margins and asks whether they point to the same
modernization bottleneck. Japan makes that contrast especially visible because
a substantial non-generating segment remains active alongside a smaller modern
generating segment. The broader claim is correspondingly narrow: in fleets that
mix non-generators and mature generators, adoption and conditional performance
should be modeled separately before they are interpreted together.

Japan is also analytically useful because it sits between two stylized fleet
stories. It is not a context where waste-to-energy is absent, so the paper does
not need to ask whether incineration should exist at all. But it is also not a
case where nearly every facility already operates as a modern high-efficiency
generator. The coexistence of persistent non-generators, old small plants, and
a more modern generating segment makes it possible to observe both margins in
the same administrative system. That mixed fleet structure is exactly what
makes a one-average-fleet summary misleading: it can conceal whether the policy
problem is failure to enter generation, weak performance after entry, or both.

The rest of the paper proceeds as follows. Section 2 positions the paper against
the literature most relevant to the analytical split. Section 3 introduces the
two linked analytical frames and the main estimation choices. Section 4 reports
the adoption and efficiency results in sequence, then ties them together.
Section 5 interprets the combined finding, explains what the data still cannot
identify, and states a short set of evidence-consistent implications. Section 6
concludes.

## 2. Literature Positioning

This paper speaks to three overlapping literatures: waste-to-energy systems,
facility-level efficiency analysis, and infrastructure lock-in. The point is
not to survey them exhaustively, because the paper's contribution is narrower
than that. The relevant gap is that existing studies often describe fleets in
aggregate or explain generator performance conditional on operation, yet rarely
estimate both margins in one linked municipal-fleet design.

Work on waste-to-energy systems often documents national trajectories,
technology choices, or lifecycle implications of thermal treatment (Astrup et
al., 2009; Astrup et al., 2015; Brunner & Rechberger, 2015; Sun et al., 2018).
Japan-specific work has mostly emphasized
technology upgrading, heat-use constraints, and sectoral decarbonization
scenarios rather than facility-level transition modeling (Uno, 2015; Tabata &
Tsai, 2016; Yamada et al., 2023). Policy-facing work reaches a similar
conclusion from a different angle: waste-to-energy is treated as useful only
when embedded in a wider waste hierarchy and resource-recovery strategy rather
than as a stand-alone justification for thermal treatment (European Commission,
2017; Sakai et al., 2011). That literature is indispensable for understanding
why energy recovery matters, but it usually treats the incineration fleet as a
sectoral category. It can show whether energy recovery is expanding, whether
heat supply remains constrained, or whether the sector matters for net-zero
planning, but it is less well suited to distinguishing facilities that enter
generation from those that do not.

Facility-level efficiency studies are closer to the present paper, but they
typically begin after entry has already occurred. Studies in Taiwan, for
example, evaluate the efficiency of operating incinerators by decomposing
waste-treatment, electricity-generation, or revenue performance within existing
plants (Chen et al., 2012; Yeh, 2020). Other work focuses more directly on
energy-recovery criteria, plant scale, heat use, and the system consequences of
different waste-to-energy configurations (Grosso et al., 2010; Munster &
Meibom, 2010). Recent Chinese plant-level work is likewise highly informative
about performance differentials inside the generating segment and the
effectiveness of upgrading strategies at scale (Cui et al., 2026; Liu et al.,
2025; Han et al., 2025), but it does not directly address the modernization
margin between non-generating and generating facilities. In that sense, such
studies answer the intensive-margin question while leaving the extensive-margin
question open.

The lock-in literature adds a different empirical expectation. Infrastructure
performance may be shaped by durable design choices, inherited scale, and
institutional arrangements rather than by frequent large reversals at mature
facilities (Unruh, 2000; Geels, 2004; Seto et al., 2016). The useful
implication here is not that incineration plants must be literally irreversible,
but that cross-facility differences may matter more than repeated late-life
performance resets. In municipal infrastructure, that persistence can also be
institutional rather than purely technical: plant networks are shaped by
jurisdictional boundaries, merger histories, charging regimes, and the
political difficulty of reorganizing service territories (Rausch, 2006; Sakai
et al., 2008; Sakai et al., 2011). That expectation is only partially visible
if entry into generation and performance within generation are never separated.

These literatures overlap in practice, but their empirical starting points are
different. Fleet-level work can show whether energy recovery is spreading,
generator-only work can show what shapes performance once generation already
exists, and lock-in work can motivate why mature performance may remain
hierarchical. What remains uncommon is a single facility panel that estimates
both margins and tests whether they point to the same modernization bottleneck.
This paper contributes that linked design.

Stated differently, each comparator literature omits something the present
design needs. Fleet-average work can describe aggregate progress but cannot tell
whether low average performance reflects many non-generators, weak generator
performance, or both. Generator-only work can estimate the correlates of
efficiency once entry has already occurred, but it cannot show who stays
outside generation or whether entry itself is selective. Lock-in work explains
why mature infrastructure may remain stratified, but it does not by itself show
whether the main modernization margin lies before or after entry into the
generating regime. The paper's contribution is therefore not simply to combine
three literatures in one narrative; it is to use one linked panel to show why
their distinct starting points lead to different empirical blind spots.

## 3. Data and Design

The analysis uses the Ministry of the Environment's General Waste Treatment
Survey for FY2005-FY2024 (Ministry of the Environment Japan, 2022). The full
panel contains 23,599 facility-year rows.
Within that, the coded full-fleet frame contains 19,827 observations across
2,948 facilities with usable identifiers. This paper uses two linked samples
because one sample cannot answer both parts of the transition problem. The
survey is unusually useful for this purpose because it covers both generating
and non-generating facilities inside the same administrative system. That makes
it possible to ask a question that many sector studies cannot ask cleanly:
which facilities record observed transition into generation at all, and how do
facilities perform once they are already inside the generating segment?

The first analytical frame is the coded adoption frame. It includes facilities
first observed without power generation and follows them until they either
record observed transition into generation or remain non-generating in the panel
window. After excluding left-censored facilities already generating in their
first observed year, the adoption risk set contains 13,770 facility-years across
2,035 facilities, with 141 observed first-adoption events. The main adoption
model is a lagged discrete-time logit hazard estimated on 11,717 observations
across 1,915 facilities and 140 retained events. Predictors are prior-year age
band and prior-year design capacity, with year fixed effects, prefecture fixed
effects, and facility-clustered standard errors. This is an observed-transition
model, not a complete structural model of all possible modernization pathways.
The design follows the logic of grouped event-history analysis, where each
facility-year contributes one observation to the risk set until first event
occurrence (Allison, 1982; Beck et al., 1998). That matters here because the
paper is not estimating a continuous engineering retrofit process. It is
estimating the probability that a facility first records entry into power
generation in the next observed year, conditional on still being at risk. The
lagged predictor structure is important for the same reason: it ensures that
age band and capacity are measured before the observed event rather than on the
event row itself.

The second analytical frame is the canonical generator frame. It contains
operating facilities with positive throughput and positive power output, after
standard cleaning and a bounded efficiency measure. The operating generation
sample contains 6,660 rows before identifier and regression cleaning. Of those,
907 rows lack official facility codes and are excluded from the canonical
regression frame, which leaves 5,683 observations across 1,016 facilities. The
dependent variable is winsorized log electricity generated per tonne processed.
Main predictors are facility age, design capacity, capacity utilization, waste
heating value, and a grid-emission control. The main specifications are pooled
OLS, year fixed effects, random effects, and year fixed effects plus random
effects, all used as structured descriptive models rather than clean structural
estimates (Wooldridge, 2010). The efficiency results should therefore be read
as conditional patterns within the canonical regression frame, not as estimates
for the entire generating fleet. This regression frame is intentionally narrower
than the operating-generator universe because the argument depends on
facility-level comparison over time. Rows without official facility codes cannot
support that comparison. The resulting frame is therefore better thought of as
the canonical identifiable generator sample than as a census of all generation
activity. The paper also uses a bounded efficiency metric because the empirical
question is not boiler thermodynamics in isolation, but administrative
performance in electricity recovered per tonne processed. That puts the paper
closer to the applied energy-recovery literature than to plant-level engineering
optimization alone (Grosso et al., 2010; Munster & Meibom, 2010).

The two layers belong in one paper because they answer sequential parts of the
same modernization problem. The adoption layer identifies which facilities
appear to enter the generating regime at all. The efficiency layer identifies
whether large gains remain available once facilities are already inside that
regime. Without the first layer, the paper would reduce transition to generator
performance alone. Without the second, it would say who enters generation but
not whether large efficiency gaps remain inside the generating segment. The two
samples are linked but non-identical, so they should not be read as one causal
pathway. They are instead the extensive-margin gate and the
conditional-performance layer of the same modernization problem.

This linked design also clarifies what the paper is not trying to do. It is not
estimating a single structural law of fleet modernization, and it is not asking
whether one estimator dominates all others in abstract econometric terms.
Instead, it asks what can be learned when a municipal fleet is partitioned into
the margin where generation first appears and the margin where generating plants
continue to differ. That framing matters for interpretation. If the extensive
margin looks selective while the intensive margin remains hierarchical, then the
relevant practical conclusion is not that the fleet is uniformly lagging. It is
that different parts of the fleet face different modernization tasks.

The main identification limits are explicit. In the adoption layer, the paper
models observed transition within the coded risk set, not unrestricted fleet-
wide modernization. In the efficiency layer, age is closely tied to time and
within-facility movement is limited, so the defended interpretation is one of
structured conditional association rather than strict causal identification. The
paper therefore aims for disciplined inference rather than maximal causal reach.
All reported effects should be read as conditional associations within the
specified samples, not as estimates of structural causality or policy effects.
The paper does not claim that the low within-facility variance ratio resolves
all fixed-effects concerns; instead, it uses that variance structure to
motivate why a cross-facility descriptive model remains substantively useful
for the question at hand. This is the point at which the paper differs from a
methods-first estimator comparison. The question is not whether fixed effects
can be forced into the design, but whether a cross-facility descriptive model
still conveys substantive information once the sample and the interpretation are
kept explicit. The answer defended here is yes: the variance structure and the
stable sign pattern make the descriptive models useful, but not structural.

**Table 1. Linked analytical framework**

| Margin | Linked sample | Empirical question | Paper role |
|:--|:--|:--|:--|
| Adoption margin | Coded at-risk frame: 13,770 facility-years, 2,035 facilities, 141 observed first-adoption events | Which facilities record observed transition into generation? | Shows whether entry into generation is selective rather than diffuse |
| Efficiency margin | Canonical generator frame: 5,683 observations across 1,016 operating generators | How does performance vary once generation already exists? | Shows whether mature generator performance remains bounded |
| Synthesis | Two linked but non-identical analytical frames | Would one average-fleet view misstate the modernization bottleneck? | Shows why entry and mature performance should not be read as one average process |

*Note: the adoption margin is estimated with a lagged discrete-time hazard. The
efficiency margin is estimated with descriptive pooled, year-FE, and RE panel
specifications.*

## 4. Results

### 4.1 Adoption into generation is selective rather than diffuse

The adoption results show a strongly selective transition pattern. In the risk
set, annual event rates collapse after age 10 and rise sharply across capacity
quartiles. Facilities aged 0-10 years account for 102 first-adoption events,
while the three older age bands together account for only 39. By capacity, the
largest quartile accounts for 99 first-adoption events, whereas the smallest
quartile records only 1.

The discrete-time logit hazard compresses that pattern into a clear main result.
Relative to 0-10 year facilities, plants aged 10-20 years are about 1.76
percentage points less likely to record transition in the next observed year,
plants aged 20-30 years are about 1.72 percentage points less likely, and plants
aged 30 years or more are about 1.13 percentage points less likely. Each
additional 100 t/day of prior-year design capacity raises annual transition
probability by about 0.50 percentage points. The sign pattern is stable in the
complementary log-log and linear probability robustness variants.

These effects should be read within the coded at-risk frame, not as a model of
all modernization activity in the Japanese fleet. Even within that narrower
observed-transition frame, however, the pattern is not one of broad late-life
conversion among the old small-plant segment. Observed transition is
concentrated among facilities that were already younger and larger before the
event year. Older plants do still transition in some cases, but they do so far
less often and do not define the main event pattern. The extensive margin
therefore looks like selective modernization rather than broad catch-up across
the whole fleet. That matters because a descriptive fleet mean could easily be
read as gradual modernization delayed by inertia, when the event pattern is
actually more selective than gradual. The results therefore speak less to
uniform diffusion and more to which segment of the fleet is still empirically
positioned to enter generation.

The pathway audit supports that interpretation without turning it into a stronger
mechanism claim than the data earn. Among the 141 observed adoption events, 82
are classified as reset- or rebuild-like, 38 as continuity-type upgrades, 20 as
forward-dated or placeholder entries, and 1 as unresolved. This is descriptive
pathway evidence, not mechanism identification. The event mix is more consistent
with capital-intensive pathways than with diffuse late-life catch-up, but it
does not uniquely identify replacement, major refurbishment, or new build as
the single pathway. In the main text, the audit therefore functions as a
credibility guard rather than as a coequal source of originality.

That distinction is important because the adoption margin could otherwise be
overread as a simple story of technological inevitability. The event pattern
does not imply that older plants never upgrade, nor does it imply that small
facilities have no role in local waste management. It implies something more
specific: within the coded at-risk frame, recorded entry into generation is not
empirically centered in the segment most likely to be described as lagging in
simple fleet summaries. The modernization margin that remains visible in the
data is therefore selective from the start.

![Figure 2. Observed adoption event rates by age band and capacity quartile in the coded at-risk frame.](../figures/figure2_selective_transition.png)

**Table 2. Main lagged hazard results for observed transition into generation**

| Variable | AME (pp) | SE (pp) |
|:--|--:|--:|
| Prior-year age 10-20 yrs (vs 0-10) | -1.76 | 0.28 |
| Prior-year age 20-30 yrs (vs 0-10) | -1.72 | 0.42 |
| Prior-year age 30+ yrs (vs 0-10) | -1.13 | 0.39 |
| Prior-year capacity (per 100 t/day) | 0.50 | 0.20 |

| Model summary | Value |
|:--|--:|
| Observations | 11,717 |
| Facilities | 1,915 |
| First-adoption events | 140 |
| Pseudo-R-squared | 0.1842 |

*Note: entries are average marginal effects in percentage points from the main
lagged logit hazard with year and prefecture fixed effects and facility-clustered
standard errors.*

### 4.2 Performance within generation is bounded and strongly structured

The generator results tell a different but complementary story. Within the
canonical regression frame, efficiency is consistently associated with lower
values at older facilities and higher values at larger and more fully utilized
ones. Across the main specifications, the age coefficient remains negative, the
capacity coefficient remains positive, and the utilization coefficient remains
positive. The magnitudes differ across models, but the sign pattern is stable,
and the emphasis stays on structured conditional association rather than on any
single structural parameter. This pattern is consistent with earlier
facility-level work showing that energy recovery performance is not evenly
distributed across operating incinerators and that plant scale and operational
intensity matter for output performance (Chen et al., 2012; Yeh, 2020; Grosso
et al., 2010). What this paper adds is the linked comparison to the
non-generating segment: the same fleet that shows selective entry at one margin
also shows a stable hierarchy among mature generators at the other.

The strongest descriptive result is not one coefficient but the variance
structure. The within-to-total variance ratio of pooled log-efficiency is
0.1499. In other words, the large majority of variation in the dependent
variable is between facilities rather than within facilities over time. The
ratio remains low in both the pre-Fukushima and post-Fukushima windows, falling
from 0.1795 before 2011 to 0.0956 after 2011. That pattern does not prove
irreversibility, but it is hard to reconcile with a world in which mature
generators frequently undergo large late-life reversals that reshape the fleet
distribution. It also does not identify vintage effects separately from all
other durable plant characteristics; more narrowly, it supports cross-facility
descriptive comparison, not clean causal isolation of vintage itself.

![Figure 3. Mean efficiency declines across generator age groups, while the within-to-total variance ratio stays low in the full sample and in pre/post-Fukushima splits.](../figures/figure3_efficiency_structure.png)

The efficiency margin therefore looks bounded rather than static. Facilities do
respond within a design envelope, especially through utilization and
operational discipline, but the cross-sectional hierarchy remains strong. Within
the canonical regression frame, older facilities are associated with lower
efficiency, larger plants are associated with higher efficiency, and utilization
matters more as a supporting lever within the generating segment than as a
fleet-wide equalizer. This is also where the paper diverges from a simple
engineering-upgrade narrative. Recent large-scale Chinese studies show that
substantial gains can still be unlocked through technology upgrades, pollutant
control, waste classification, and load-rate improvements, but they do so
within already-generating systems rather than at the point of first entry (Liu
et al., 2025; Han et al., 2025). The present results are consistent with that
kind of bounded improvement logic rather than with the idea that mature
generator performance naturally converges once plants enter generation.

This is why the intensive margin cannot be inferred from the adoption margin
alone. A facility can be inside generation without being close to the frontier,
yet the evidence also suggests that operations alone are unlikely to erase large
vintage and scale gaps once plants are mature. Conditional performance is
therefore a bounded-performance problem rather than a simple continuation of the
entry problem.

For interpretation, this matters just as much as the adoption result. If the
paper only documented selective entry, a reader could still infer that the main
remaining task was simply to push more facilities into generation. If it only
documented generator hierarchy, a reader could still infer that non-generators
were just lagging versions of the same problem. The linked result rejects both
shortcuts. The fleet appears divided between a segment that still struggles to
enter generation at all and a segment where entry has already occurred but
performance remains uneven and bounded.

**Table 3. Core conditional-efficiency specifications in the canonical generator frame**

| Variable | Model 1 Pooled OLS | Model 2 Year FE | Model 3 RE | Model 4 Year FE + RE |
|:--|--:|--:|--:|--:|
| Facility age (years) | -0.0279*** | -0.0348*** | -0.0188*** | -0.0332*** |
|  | (0.0022) | (0.0022) | (0.0025) | (0.0021) |
| Capacity (100 t/day) | 0.0874*** | 0.1030*** | 0.0405*** | 0.0519*** |
|  | (0.0083) | (0.0086) | (0.0083) | (0.0096) |
| Capacity utilization | 0.7468*** | 0.7789*** | 0.6199*** | 0.5411*** |
|  | (0.1421) | (0.1346) | (0.0997) | (0.0943) |
| Heating value (MJ/kg) | 0.0010 | 0.0032 | 0.0006 | 0.0012 |
|  | (0.0023) | (0.0021) | (0.0012) | (0.0010) |
| Grid EF (kg-CO2/kWh) | 0.3182 | -0.4466 | 1.6333*** | -0.1951 |
|  | (0.2219) | (0.2714) | (0.1965) | (0.2101) |
| Observations | 5,683 | 5,683 | 5,683 | 5,683 |
| Facilities | 1,016 | 1,016 | 1,016 | 1,016 |
| R-squared | 0.2470 | 0.3721 | 0.1647 | 0.3076 |

*Note: standard errors are in parentheses. `***` p < 0.01. Coefficients are
reported as structured conditional associations rather than as strict structural
parameters.*

### 4.3 Why the two results belong together

Read together, the two margins change the story the fleet appears to tell. The
adoption results show that entry into generation is already selective before
conditional efficiency is considered, while the efficiency results show that
large performance gaps inside the generating segment are not easily erased
through within-facility movement alone. A one-average-fleet model would flatten
those margins into a single modernization narrative and would therefore
understate both the selectivity of entry and the persistence of cross-facility
performance differences. The point is not that the two samples form one strict
causal chain, but that they identify different constraints within the same
fleet. One concerns who gets into generation at all; the other concerns how far
operating generators can move once they are already there.

## 5. Discussion

The paper's main interpretive claim is methodological: in this fleet, entry
into generation and performance within generation are linked but distinct
estimands. Modeling them separately shows that the weakest part of the fleet
and the mature generating segment are constrained in different ways. That point
matters because municipal fleets often contain both non-generators and mature
generators at the same time. If those segments are averaged together, the
analyst can see only a muted fleet mean rather than the combination of selective
entry and persistent hierarchy that actually structures the system.

The substantive interpretation is correspondingly two-part. On the adoption
margin, the data do not support broad late conversion among old small plants.
Observed transition within the coded at-risk frame is concentrated among
younger and larger facilities, and the pathway audit is more consistent with a
capital-intensive event mix than with diffuse late-life catch-up. On the
efficiency margin, age, scale, and utilization still matter strongly within
the canonical regression frame, while within-facility movement remains modest
relative to the cross-sectional hierarchy. Read together, the evidence points
more toward selective entry into the generating regime and bounded
responsiveness within generation than toward easy convergence once entry has
occurred.

That interpretation should remain calibrated. The pathway audit does not prove
that replacement is the unique pathway of modernization. The regression results
do not provide strict causal estimates of vintage lock-in or clean estimates
for all operating generators in Japan. Alternative interpretations remain
possible, including reporting compression, unobserved retrofit histories,
unmeasured governance differences, and institutional constraints that limit
operational responses. The defended claim is therefore narrower: the data
support a selective modernization process and a bounded performance envelope,
not a uniquely identified mechanism or a full causal hierarchy.

These are evidence-consistent implications, not estimated policy rankings. For
the weakest segment, especially older non-generators and small plants, the
evidence points more toward capital-renewal planning than toward diffuse
late-life operational improvement. For the already-generating segment,
utilization, routing, and selective upgrading remain real levers, but they
appear more likely to preserve or modestly improve performance within the
existing envelope than to eliminate large inherited gaps. For municipal waste
planners, the practical takeaway is to separate fleet triage from generator
optimization: first identify which non-generators plausibly warrant renewal,
then identify which operating generators still have room for incremental gains.
That distinction is not only technical; it is administrative. Japanese waste
systems are organized through municipalities whose planning boundaries do not
always align with efficient waste sheds, and intermunicipal reorganization has
its own political costs and institutional legacies (Rausch, 2006; Sakai et al.,
2008). In that setting, a paper that collapses non-generators and generators
into one average segment risks obscuring the difference between asset renewal,
which is lumpy and governance-heavy, and generator optimization, which is more
incremental and operational.

The broader policy context points in the same direction. Comparative waste
policy studies and European framework discussions both treat waste-to-energy as
valuable only when embedded inside a wider hierarchy that preserves prevention,
reuse, and recycling priorities (Sakai et al., 2011; European Commission,
2017). The present paper does not estimate those policy hierarchies directly,
but its empirical split helps explain why they matter. A municipal system can
have real energy-recovery gains available at the non-generating margin while
still facing a different, narrower set of decisions inside the already-
generating segment.

This matters for climate interpretation as well. Waste-to-energy performance is
not judged only against an internal engineering standard; it is also judged
against the emissions profile of the broader energy system and the avoided
emissions logic built into carbon accounting (Astrup et al., 2009; Munster &
Meibom, 2010). In Japan's current decarbonization setting, where national
inventories and scenario work increasingly track sectoral emissions and energy
mix changes, the relevant question is not simply whether a plant generates, but
what kind of generator it is and how much improvement remains inside that
segment (Greenhouse Gas Inventory Office of Japan & Ministry of the Environment
Japan, 2024; Yamada et al., 2023). The paper's two-part design is useful
precisely because it keeps those questions separate.

That separation is also what makes the paper more understandable for a planning
audience. Municipal systems rarely choose among abstract technological ideals.
They decide whether to renew an aging non-generator, coordinate waste routing
toward a larger plant, maintain an existing generator, or invest in an upgrade
for a plant that already produces electricity. Those are related decisions, but
they are not interchangeable. A paper that keeps the extensive and intensive
margins separate is therefore easier to use for practical reasoning than a
paper that reports one blended fleet mean and leaves the reader to infer where
the bottleneck actually sits.

## 6. Conclusion

Japan's incineration transition is not one smooth modernization process. Within
the coded adoption frame, observed entry into generation is selective rather
than diffuse. Within the canonical generator frame, performance remains
stratified by age, scale, and utilization, with limited within-facility
movement relative to between-facility differences. Read together, those
margins show why a one-average-fleet view can misstate the modernization
bottleneck. The paper does not identify one unique pathway or intervention
hierarchy, but it does show why municipal fleet studies gain by separating
adoption from conditional performance. For readers of municipal waste systems,
the practical point is simple: the transition problem at the non-generating end
of the fleet is not the same problem as performance management within the
already-generating segment, and the two should not be planned as though they
were one average task.

## Acknowledgements

The author thanks Prof. Han Ji for supervision and critical feedback during the
development of the underlying thesis project from which this paper is derived.

## Funding

This research did not receive any specific grant from funding agencies in the
public, commercial, or not-for-profit sectors.

## CRediT Authorship Contribution Statement

Pann Phetra: Conceptualization, Data curation, Formal analysis, Investigation,
Methodology, Visualization, Writing - original draft, Writing - review &
editing.

## Declaration of Competing Interest

The author declares no known competing financial interests or personal
relationships that could have appeared to influence the work reported in this
paper.

## Data Availability

The facility-level source data are derived from the Ministry of the Environment
Japan General Waste Treatment Survey. Processed study outputs, manuscript
figures, and the associated reproducible analysis workspace can be provided by
the author on reasonable request.

## Generative AI And AI-Assisted Technologies Statement

During the preparation of this manuscript, the author used OpenAI Codex and
Anthropic Claude to support drafting, language revision, and organizational
planning. After using these tools, the author reviewed and edited the content as
needed and takes full responsibility for the content of the manuscript.

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

Ministry of the Environment Japan. (2022). *General waste treatment survey:
Summary report FY2021*. Environmental Management Bureau, Ministry of the
Environment Japan. https://www.env.go.jp/recycle/waste_tech/ippan/r3/index.html
(accessed 18 April 2026).

Münster, M., & Meibom, P. (2010). Long-term affected energy products of waste
to energy, a consequential approach. *Waste Management*, *30*(12), 2510-2519.
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

Seto, K. C., Davis, S. J., Mitchell, R. B., Stokes, E. C., Unruh, G., &
Urge-Vorsatz, D. (2016). Carbon lock-in: Types, causes, and policy
implications. *Annual Review of Environment and Resources*, *41*(1), 425-452.
https://doi.org/10.1146/annurev-environ-110615-085934

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
