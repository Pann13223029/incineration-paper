# Paper Zoom Briefing: Presentation Script

Use this script with `paper/share/paper-zoom-briefing.pdf`. The deck has 20 live slides. It is designed for a 15-18 minute discussion and assumes the audience may not know waste-management or statistics vocabulary.

## Delivery Rule

Reset the audience with this sentence:

> The paper tests where scale and age patterns survive: across all coded assets, among active non-generators, and after facilities enter generation.

The audience should leave understanding four things:

- Why the topic matters: incineration creates heat, but energy recovery is uneven.
- What the paper argues: one fleet average hides two different questions.
- Why the method matters: risk-set framing and generator-only comparison prevent the two questions from being mixed.
- What feedback is needed: whether the two-margin framing and broad-versus-active distinction are convincing, and which future-work path matters most.

## Audience Calibration

Use the same slides, but adjust the speaking depth:

- Default to no prior knowledge. Explain the practical problem first, then define technical terms only when they become necessary.
- If the audience has prior knowledge of waste management or energy policy, move faster through slides 2-4 and spend more time on slides 5-9, because the design choice is the main defensibility point.
- If the audience knows Japanese energy policy, explain that FY2010-FY2012 official codes are missing; the early/later coded windows overlap the Fukushima period but do not identify a Fukushima effect.
- If the audience is statistically trained, describe the models as diagnostic panel regressions and robustness checks, not causal identification.
- If time is short, keep the core route: slides 1-4, 6-9, 10-11, 13-15, 18-20.

## Jargon To Translate Out Loud

Use these plain-language translations whenever the audience looks uncertain:

- Waste incineration: burning municipal waste in a controlled facility.
- Energy recovery: using heat from incineration to make useful electricity.
- Fleet: the whole group of facilities being studied, not one plant.
- Entry: a facility first reports positive installed generation capacity in the observed data.
- Generator: a facility that reports electricity generation.
- MWh/t: megawatt-hours of electricity per tonne of waste processed; in plain terms, electricity output per amount of waste.
- Throughput: how much waste a facility processes.
- Capacity: how much waste a facility is designed to process.
- Risk set: the facilities that still have a chance to newly start generating.
- Robustness check: a stress test to see whether the result survives alternative reasonable choices.
- Causal claim: a claim that one thing directly caused another. This paper does not make that kind of strong claim.

## Timing Plan

| Segment | Slides | Target time |
|:--|:--|:--|
| Motivation and framing | 1-4 | 3 minutes |
| Data and method | 5-9 | 5 minutes |
| Results and interpretation | 10-14 | 5 minutes |
| Robustness, limits, and future work | 15-19 | 5 minutes |
| Feedback ask | 20 | 1 minute |

## Slide 1: Where Energy Recovery Stalls

Thank you for joining. This is a paper briefing, not a full thesis defense. The formal paper title is on the slide, but the plain-language version is simpler: where does energy recovery stall inside Japan's waste-incineration fleet?

I will explain the problem, the data, the method, the two main results, and the limits of the claim. The main goal is to test whether the two-margin story and the broad-versus-active entry distinction are clear and defensible.

Transition: I will start with why this matters, then move quickly into how the data are structured.

## Slide 2: Why This Matters

Japan relies heavily on municipal waste incineration. In plain language, that means municipalities burn waste in controlled facilities instead of only landfilling it.

Burning waste creates heat. Some facilities use that heat to generate electricity. Others burn waste but do not recover electricity from the heat.

In FY2024, the official national summary reports that 415 of 991 facilities, or 41.9 percent, generated electricity. The reconstructed analytical panel has a slightly different denominator, so I use 41.9 percent for national context.

The paper asks where useful electricity recovery appears inside the existing fleet.

If the audience already knows Japan relies heavily on incineration, do not dwell here. Move to the bottleneck question.

## Slide 3: The Real Question

This slide is important because the result could sound too obvious if phrased badly.

I am not asking the listener to be surprised that scale or technology vintage may matter. The stronger question is whether those associations survive when I change the candidate population.

The paper distinguishes broad asset entry from conversion among plants that were actually operating in the prior year, then asks where entrants sit in the generator distribution.

Transition: That leads to the paper's structure: one fleet, but two questions.

## Slide 4: Two Questions, One Fleet

The main idea is that one fleet average hides two different bottlenecks. By "fleet," I mean the whole group of municipal incineration facilities in the data.

First, which facilities first report positive installed generation capacity? That is the entry margin. Capacity reporting usually maps to output, but the event itself is not a verified retrofit date.

Second, among generators, who produces more electricity per tonne? That is the performance bottleneck. "MWh per tonne" means electricity output per amount of waste processed.

The slide includes these definitions because the rest of the presentation uses them repeatedly. The paper is built around keeping these two questions separate and then reading them together.

Transition: To do that, the data need to be split carefully rather than pushed into one average.

## Slide 5: What the Data Can See

The data source is Japan's Ministry of the Environment General Waste Treatment Survey. This is administrative data, meaning it comes from official facility reporting rather than from interviews or a small case study.

The panel covers FY2005 to FY2024 and uses facility-level municipal waste-treatment records. A panel means repeated observations over time. The main fields are installed generation capacity, electricity output, throughput, facility age, design capacity, fiscal year, heating value, furnace type, operating mode, facility type, and furnace count.

If needed, define two terms here. Throughput means how much waste the facility processes. Capacity means how much waste the facility is designed to process.

The important point is that this is national facility-level evidence, not one local case. But I should also be clear about the boundary: the administrative panel does not directly observe internal retrofit contracts, municipal bargaining, or full lifecycle emissions.

For a technical audience, add: this is why the paper is framed as diagnostic mapping, not causal mechanism proof.

## Slide 6: How the Panel Becomes Two Frames

The full analytical starting point is 23,599 facility-year rows. One facility-year means one facility observed in one fiscal year.

Within the coded full-fleet frame, there are 2,948 identifiable facilities.

The broad entry frame has 13,770 at-risk facility-years and 141 observed events. The exact-year model retains 98 events. Because 40 of those follow zero or missing prior-year throughput, I also estimate an active-conversion frame with 9,215 rows and 58 events.

The generator-output frame has 5,683 observations among identifiable operating generators.

This split is methodological, but the idea is simple. The first comparison studies broad asset entry, the second narrows entry to active plants, and the generator frame studies output intensity after entry.

Transition: The split prevents the analysis from mixing adoption with performance.

## Slide 7: Why Two Samples Are Needed

The two samples are linked but not identical. A sample is just the group of observations used to answer a particular question.

For the entry question, the sample is facilities first observed without positive installed capacity. The outcome is first positive capacity, with a narrower model for facilities processing waste in the prior year.

For the generator-output question, the sample is already-operating generators. The outcome is electricity generated per tonne processed.

One model for everything would mix the gate into generation with performance after entry. That would make the result less clear because it would hide where the bottleneck actually sits.

For a methods-aware audience, phrase it this way: the two samples correspond to different estimands, so combining them would answer a muddier question.

## Slide 8: Method: First Entry Into Generation

The first method is a risk-set design. The plain meaning of "risk set" is: which facilities still have a chance to newly start generating?

Only non-generators can first start generating. Facilities already generating in their first observed year are left-censored for this question.

The model asks for the probability of first installed capacity in a given year using prior-year age and capacity, fiscal-year indicators, and actual elapsed fiscal time at risk. This matters because it describes the facility before entry and handles gaps in observed facility codes correctly.

In plain language, the model asks: among facilities still outside power generation, who first reports generation in the next fiscal year?

The broad model can include commissioning, rebuild, or inactive-asset pathways. The active model requires positive throughput in the previous fiscal year. Do not overexplain the equation; emphasize that these are different candidate populations.

## Slide 9: Method: Output Among Generators

The second method is a generator-only comparison. In plain language, after looking at who starts generating, the paper then looks only at plants that already generate electricity.

The outcome is electricity recovered per tonne processed. This focuses on output intensity, not just whether a plant has any power generation.

The primary model compares age/vintage, scale, utilization, and heating value within common fiscal years while adjusting for furnace type, operating mode, facility type, and furnace count.

If the audience is technical, add: the primary specification is year- and technology-adjusted OLS with facility-clustered standard errors; pooled and random-effects models are a supplemental estimator ladder.

The interpretation is diagnostic, not causal. Age is an age/vintage comparison across plants in the same year, not the effect of making one plant older.

For a technical audience, add: the robustness checks ask whether the age, scale, and utilization pattern survives alternative model structures.

## Slide 10: Result 1: Scale Is Robust; Age Depends on the Frame

Figure 2 shows three outcomes side by side. In the broad asset-entry model,
capacity has a +0.45 percentage-point average marginal effect per 100 tonnes per
day. In the active-conversion model, it is +0.44. Scale selectivity is therefore
the stable entry result.

The broad age differences are -1.41, -1.45, and -0.83 percentage points relative
to ages zero to ten. In the active frame they shrink to -0.67, -0.56, and -0.29.
Only the first active age difference is clearly distinguishable from zero.

Transition: The next slide explains why changing the candidate population changes
the age story.

## Slide 11: Interpretation: The Risk Set Changes the Story

Forty of the 98 broad exact-year events follow zero or missing prior-year
throughput. These can include commissioning, rebuild, inactive-asset, or
reporting pathways rather than conversion of a plant that was actively processing
waste one year earlier.

This is the contribution beyond common sense. Scale remains important across
both populations, but the statement that older operating plants rarely convert
is too strong. The age gradient partly reflects which pathways are admitted to
the broad risk set.

Use this sentence if challenged: the paper does not merely report an age
advantage; it demonstrates that the age result is population-dependent while the
scale result is robust.

## Slide 12: Entry Pathways: Modernization, Not One Mechanism

The pathway audit helps avoid overclaiming. This is a manual or rule-based check of what kind of transition each first-entry event seems to represent.

Fifty observed first-entry events are reset- or rebuild-like adjacent-year cases. Thirty-six look consistent with continuity or in-place upgrade. Twelve are placeholder or forward-dated entries, 42 are timing-ambiguous non-adjacent coded-row events, and one remains unresolved.

The safe interpretation is that capital-side modernization is present, but the paper does not prove replacement is the only pathway. In simpler terms: many cases look like major renewal, but some may be upgrades of existing plants.

Transition: The first bottleneck is who starts generation. The second is whether generators actually perform similarly after starting.

## Slide 13: Result 2: Generation Status Is Not Enough

The second result looks inside the generating segment.

Older generators recover less electricity per tonne, and existing generators remain uneven after entry. The age 0 to 10 group averages about 0.400 MWh per tonne, while the 30-plus group averages about 0.183 MWh per tonne.

The point is not that older plants can never improve. The point is that simply entering electricity generation does not erase generator hierarchy.

Transition: The next slide checks whether performance gaps are mostly within the same facilities over time, or mostly between different facilities.

## Slide 14: Interpretation: Ranks Persist Across Coded Years

The within-to-total variance ratio is 0.1499 in the full sample. That phrase sounds technical, so translate it immediately: only about 15 percent of output variation is movement within the same facility over time. Most variation is between different facilities.

Official facility codes are missing in FY2010 to FY2012. The paper therefore
compares an early coded window, FY2005 to FY2009, with a later coded window,
FY2013 to FY2024. The within-to-total ratio falls from 0.1795 to 0.0956.

This gap overlaps the period around the Great East Japan Earthquake and Fukushima
Daiichi accident, but it is not a pre/post Fukushima treatment design. The code
gap prevents that causal interpretation.

The more direct persistence check is the adjacent-year within-year rank
correlation: 0.9325 across 4,368 exact pairs. This shows stable observed ranking,
not an upper bound on how much an intervention could improve a plant.

## Slide 15: Stress Tests: The Pattern Survives

This slide shows why the pattern is not just a fragile coding artifact. A robustness check means repeating the analysis in reasonable alternative ways to see whether the main pattern survives.

For entry, I checked composite identifiers, alternative links, capacity forms,
prior technology, and the active-conversion risk set. Scale remains positive;
the age result is deliberately reported as risk-set-dependent.

For generator output, the primary model adjusts for observed technology. I also
check unclipped MWh per tonne, a thermal-conversion proxy, reported generation
efficiency, and exact-adjacent-year lagged predictors. Age/vintage remains
negative, while capacity and utilization remain positive.

These checks do not make the estimates causal, but they make the diagnostic pattern more credible.

If the audience knows the Fukushima context, say: the missing-code years mean the
paper cannot identify a Fukushima treatment effect; early and later coded windows
are descriptive robustness checks only.

## Slide 16: Data Limits: Disclosed and Tested

The data have real limits.

There are 39 official codes with same-year duplicate issues, affecting 444 source rows. There are also 907 operating-generator rows missing official facility codes, mainly around FY2010 to FY2012, so they cannot support the canonical facility-clustered regression frame.

Heating-value data also need plausibility checks: 569 regression-frame rows are outside 3 to 25 megajoules per kilogram.

For a general audience, translate this slide as: the data are useful, but not perfect. The paper is honest about what the data can and cannot support.

These limitations discipline the claim. The paper maps bottlenecks and stress-tests data issues; it does not claim a perfect engineering census or a fully identified causal mechanism.

Transition: These limits matter because they shape what kind of decision logic the paper can support.

## Slide 17: What Happens After Entry?

The post-entry trajectory is the bridge between the two analyses. At event time
zero, 125 entrants average 0.324 MWh per tonne versus 0.329 among same-year
incumbents. Their mean same-year percentile is 51.5. Through event time three,
the average percentile remains close to the middle of the distribution.

This does not estimate an entry effect. Follow-up declines from 125 events to 71,
and the prior-operating groups differ. The safe conclusion is that entry usually
leads to measurable operation but does not guarantee a frontier position.

## Slide 18: Contribution: Clear Empirical Boundaries

The weak claim is that newer and larger plants have advantages. The stronger
claim is that the evidence has useful boundaries: scale selectivity survives
both entry frames, the age gradient depends on the risk set, and entry does not
automatically place a facility at the top of the generator distribution.

For planning, broad asset entry, active conversion, and post-entry performance
should be treated as separate diagnostic questions before choosing an
intervention.

Transition: The current paper maps the bottlenecks. The next research step would test mechanisms.

## Slide 19: Next Step: Test Mechanisms

Future work would move from diagnostic mapping to mechanism testing.

I have not started these extensions yet. The next step could link facility histories to investment and rebuild records, retrofit histories, municipal governance, waste-routing decisions, heat recovery, lifecycle emissions, or comparative fleet data.

The most publishable future direction is probably the one that best explains why some facilities start generation while others do not.

Do not overpromise here. Present these as next research paths, not completed results.

## Slide 20: Discussion Questions

The paper's message is: distinguish broad asset entry from active conversion, then evaluate performance after generation begins.

The feedback I need is targeted.

Is the three-outcome framing convincing? Is the broad-versus-active entry distinction clear enough? Which future-work path is most publishable: capital renewal, governance, lifecycle accounting, or comparative fleet evidence?
