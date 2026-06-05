# Paper Zoom Briefing: Presentation Script

Use this script with `paper/share/paper-zoom-briefing.pdf`. The deck has 20 live slides. It is designed for a 15-18 minute supervisor-facing discussion.

## Delivery Rule

Reset the audience with this sentence:

> The paper is not asking whether young and large plants have advantages. It asks whether modernization spreads broadly through the lagging fleet or remains selective and bounded.

The audience should leave understanding four things:

- Why the topic matters: incineration creates heat, but energy recovery is uneven.
- What the paper argues: one fleet average hides two different questions.
- Why the method matters: risk-set framing and generator-only comparison prevent the two questions from being mixed.
- What feedback is needed: whether the two-bottleneck explanation is strong enough and which limitation or future-work path matters most.

## Audience Calibration

Use the same slides, but adjust the speaking depth:

- If the audience has little background, spend more time on slides 2-4 and define "entry" as "starting electricity generation for the first time in the observed panel."
- If the audience has prior knowledge of waste management or energy policy, move faster through slides 2-4 and spend more time on slides 5-9, because the design choice is the main defensibility point.
- If the audience knows Japanese energy policy, mention that the 2011 split is around the Great East Japan Earthquake and Fukushima Daiichi nuclear accident, but avoid turning the presentation into a Fukushima policy talk.
- If the audience is statistically trained, describe the models as diagnostic panel regressions and robustness checks, not causal identification.
- If time is short, keep the core route: slides 1-4, 6-9, 10-11, 13-15, 18-20.

## Timing Plan

| Segment | Slides | Target time |
|:--|:--|:--|
| Motivation and framing | 1-4 | 3 minutes |
| Data and method | 5-9 | 5 minutes |
| Results and interpretation | 10-14 | 5 minutes |
| Robustness, limits, and future work | 15-19 | 5 minutes |
| Feedback ask | 20 | 1 minute |

## Slide 1: Where Energy Recovery Stalls

Thank you for joining. This is a paper briefing, not a full thesis defense. I will explain the problem, the data, the method, the two main results, and the limits of the claim.

The main goal is to test whether the paper's two-bottleneck story is clear and defensible.

Transition: I will start with why this matters, then move quickly into how the data are structured.

## Slide 2: Why This Matters

Japan relies heavily on municipal waste incineration. Incineration creates heat. Some facilities use that heat to generate electricity, but many do not.

In FY2024, only 41.1 percent of panel facilities are flagged as power-generating. That means the same waste-treatment process can either recover useful power or miss that opportunity.

The paper asks where useful electricity recovery appears inside the existing fleet.

If the audience already knows Japan relies heavily on incineration, do not dwell here. Move to the bottleneck question.

## Slide 3: The Real Question

This slide is important because the result could sound too obvious if phrased badly.

I am not asking the listener to be surprised that young and large plants have advantages. That part is expected.

The stronger question is whether energy-recovery modernization spreads broadly through older and smaller lagging facilities, or whether it mostly appears where conditions are already favorable.

Transition: That leads to the paper's structure: one fleet, but two questions.

## Slide 4: Two Questions, One Fleet

The main idea is that one fleet average hides two different bottlenecks.

First, which plants start generating electricity? That is the entry bottleneck.

Second, among generators, who produces more electricity per tonne? That is the performance bottleneck.

The paper is built around keeping these two questions separate and then reading them together.

Transition: To do that, the data need to be split carefully rather than pushed into one average.

## Slide 5: What the Data Can See

The data source is Japan's Ministry of the Environment General Waste Treatment Survey.

The panel covers FY2005 to FY2024 and uses facility-level municipal waste-treatment records. The main fields are power-generation status, electricity output, throughput, facility age, design capacity, fiscal year, prefecture, heating value, and grid-emission context.

The important point is that this is national facility-level evidence, not one local case. But I should also be clear about the boundary: the administrative panel does not directly observe internal retrofit contracts, municipal bargaining, or full lifecycle emissions.

For a technical audience, add: this is why the paper is framed as diagnostic mapping, not causal mechanism proof.

## Slide 6: How the Panel Becomes Two Frames

The full analytical starting point is 23,599 facility-year rows.

Within the coded full-fleet frame, there are 2,948 identifiable facilities.

The start-generating frame has 13,770 at-risk facility-years across facilities first observed without generation. It contains 141 first-entry events.

The generator-output frame has 5,683 observations among identifiable operating generators.

This split is methodological. The first frame studies crossing into electricity generation. The second frame studies output intensity after a facility is already inside generation.

Transition: The split prevents the analysis from mixing adoption with performance.

## Slide 7: Why Two Samples Are Needed

The two samples are linked but not identical.

For the start-generating question, the sample is facilities first observed without generation. The outcome is first report of power generation.

For the generator-output question, the sample is already-operating generators. The outcome is electricity generated per tonne processed.

One model for everything would mix the gate into generation with performance after entry. That would make the result less clear because it would hide where the bottleneck actually sits.

For a methods-aware audience, phrase it this way: the two samples correspond to different estimands, so combining them would answer a muddier question.

## Slide 8: Method: First Entry Into Generation

The first method is a risk-set design.

Only non-generators can first start generating. Facilities already generating in their first observed year are left-censored for this question.

The model asks for the probability of first generation in a given year using prior-year age and prior-year capacity, plus year and prefecture controls. This matters because it describes the facility before first entry, not after entry.

In plain language, the model asks: among facilities still outside power generation, who first reports generation in the next observed year?

Do not overexplain the model. The important point is timing: predictors are measured before entry.

## Slide 9: Method: Output Among Generators

The second method is a generator-only comparison.

The outcome is electricity recovered per tonne processed. This focuses on output intensity, not just whether a plant has any power generation.

The models compare age, scale, utilization, heating value, grid context, and year structure. I check pooled OLS, year fixed effects, random effects, and year fixed effects plus random effects.

The interpretation is diagnostic, not causal. The critical question is whether operating generators converge enough to erase inherited facility differences.

For a technical audience, add: the robustness checks ask whether the age, scale, and utilization pattern survives alternative model structures.

## Slide 10: Result 1: Entry Clusters in Young, Large Facilities

The first result is selective entry.

The figure shows that facilities first starting electricity generation are mostly young and large.

Out of 141 observed first-entry events, 102 come from facilities aged 0 to 10 years, and 99 are in the largest capacity quartile.

The audience-facing interpretation is simple: the entry margin is not evenly spread across the fleet.

Transition: The next slide explains why this is not merely the obvious point that newer plants are better.

## Slide 11: Interpretation: Not Broad Fleet Catch-Up

This slide explains why the result is more than common sense.

Young facilities have a much higher annual event rate: 5.94 percent for age 0 to 10.

Facilities age 30 or more have an annual event rate of only 0.27 percent. On the capacity side, the smallest quartile has an annual event rate of 0.03 percent, while the largest quartile has 3.11 percent.

The smallest capacity quartile records only one first-entry event, while the largest quartile records 99.

So the evidence does not look like broad late-life catch-up across the whole fleet. It looks like selective modernization.

The key wording for the meeting is: this is not "new plants are better"; it is "catch-up is not broad across lagging plants."

If the audience challenges the obviousness of the result, use this sentence: the expected part is age and scale advantage; the contribution is showing that the lagging fleet does not broadly catch up on the entry margin.

## Slide 12: Entry Pathways: Modernization, Not One Mechanism

The pathway audit helps avoid overclaiming.

Eighty-two observed first-entry events look reset- or rebuild-like. Thirty-eight look consistent with continuity or in-place upgrade. Twenty are placeholder or forward-dated entries.

The safe interpretation is that capital-side modernization is present, but the paper does not prove replacement is the only pathway.

Transition: The first bottleneck is who starts generation. The second is whether generators actually perform similarly after starting.

## Slide 13: Result 2: Generation Status Is Not Enough

The second result looks inside the generating segment.

Older generators recover less electricity per tonne, and existing generators remain uneven after entry. The age 0 to 10 group averages about 0.400 MWh per tonne, while the 30-plus group averages about 0.183 MWh per tonne.

The point is not that older plants can never improve. The point is that simply entering electricity generation does not erase generator hierarchy.

Transition: The next slide checks whether performance gaps are mostly within the same facilities over time, or mostly between different facilities.

## Slide 14: Interpretation: Performance Gaps Persist

The within-to-total variance ratio is 0.1499 in the full sample. In plain terms, only about 15 percent of output variation is movement within the same facility over time. Most variation is between facilities.

The 2011 split needs one sentence of context. The split is around the Great East Japan Earthquake and Fukushima Daiichi nuclear accident, which changed Japan's energy-system context after 2011. In this deck, the comparison is FY2005 to FY2011 versus FY2012 to FY2024.

The post-2011 ratio is lower, at 0.0956. That means the same basic pattern remains after the Fukushima-era energy-system shock: most variation still sits between facilities.

Be careful with the wording. This is not a causal claim that Fukushima caused the pattern. It is a robustness and context check showing that the performance-gap story is not limited to only one period.

The audience-facing version is: becoming a generator is not the finish line; performance remains structurally uneven.

## Slide 15: Stress Tests: The Pattern Survives

This slide shows why the pattern is not just a fragile coding artifact.

For adoption, I checked composite facility identifiers and alternative adoption models. The age penalties and positive capacity pattern remain.

For generator output, I checked period splits around the 2011 Fukushima shock, capacity terciles, raw-outcome checks, and heating-value restrictions. Age remains negative, while capacity and utilization remain positive.

These checks do not make the estimates causal, but they make the diagnostic pattern more credible.

If the audience knows the Fukushima context, say: the paper is not identifying a Fukushima treatment effect; the split is used to see whether the generator-performance pattern survives a major energy-system breakpoint.

## Slide 16: Data Limits: Disclosed and Tested

The data have real limits.

There are 39 official codes with same-year duplicate issues, affecting 444 source rows. There are also 907 operating-generator rows missing official facility codes, mainly around FY2010 to FY2012, so they cannot support the canonical facility-clustered regression frame.

Heating-value data also need plausibility checks: 569 regression-frame rows are outside 3 to 25 megajoules per kilogram.

These limitations discipline the claim. The paper maps bottlenecks and stress-tests data issues; it does not claim a perfect engineering census or a fully identified causal mechanism.

Transition: These limits matter because they shape what kind of decision logic the paper can support.

## Slide 17: Why the Split Matters for Decisions

If the two bottlenecks are different, planning questions should also differ.

For non-generators, ask whether the plant can start recovering electricity. For generators, ask whether the plant can recover more electricity from the same waste.

Renewal, starting generation, and generator optimization are not the same task.

For a policy-aware audience, emphasize that this is not a single policy recommendation. It is a diagnostic that separates where different interventions might be needed.

## Slide 18: Contribution: Two Bottlenecks in One Fleet

The weak claim is: newer and larger plants generate more. That sounds plausible, but it is not enough for a paper.

The defensible claim is: the fleet has two bottlenecks. Starting generation is selective, and generator output remains uneven after entry.

That is the paper's contribution: mapping where the bottleneck sits.

Transition: The current paper maps the bottlenecks. The next research step would test mechanisms.

## Slide 19: Next Step: Test Mechanisms

Future work would move from diagnostic mapping to mechanism testing.

I have not started these extensions yet. The next step could link facility histories to investment and rebuild records, retrofit histories, municipal governance, waste-routing decisions, heat recovery, lifecycle emissions, or comparative fleet data.

The most publishable future direction is probably the one that best explains why some facilities start generation while others do not.

Do not overpromise here. Present these as next research paths, not completed results.

## Slide 20: Discussion Questions

The paper's message is: first ask who starts generating electricity, then ask who generates well after starting.

The feedback I need is targeted.

Is the two-bottleneck explanation strong enough as the paper's central contribution? Which limitation most needs to become a robustness check? Which future-work path is most publishable: capital renewal, governance, lifecycle accounting, or comparative fleet evidence?
