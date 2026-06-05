# Paper Zoom Briefing: Presentation Script

Use this script with `paper/share/paper-zoom-briefing.pdf`. The deck has 20 live slides. It is designed for a 15-18 minute supervisor-facing discussion.

## Delivery Rule

Reset the audience with this sentence:

> The paper is not asking whether young and large plants have advantages. It asks whether modernization spreads broadly through the lagging fleet or remains selective and bounded.

The listener should leave understanding four things:

- Why the topic matters: incineration creates heat, but energy recovery is uneven.
- What the paper argues: one fleet average hides two different questions.
- Why the method matters: risk-set framing and generator-only comparison prevent the two questions from being mixed.
- What feedback is needed: whether the two-question design is strong enough and which limitation or future-work path matters most.

## Timing Plan

| Segment | Slides | Target time |
|:--|:--|:--|
| Motivation and framing | 1-4 | 3 minutes |
| Data and method | 5-9 | 5 minutes |
| Results and interpretation | 10-14 | 5 minutes |
| Robustness, limits, and future work | 15-19 | 5 minutes |
| Feedback ask | 20 | 1 minute |

## Slide 1: Explaining the Paper Clearly

Thank you for joining. This is a paper briefing, not a full thesis defense. I will explain the data, method, key results, limitations, and future directions.

The main goal is to test whether the current paper pitch is clear and defensible.

## Slide 2: Why This Matters

Japan relies heavily on municipal waste incineration. Incineration creates heat. Some facilities use that heat to generate electricity, but many do not.

In FY2024, only 41.1 percent of panel facilities are flagged as power-generating. That means the same waste-treatment process can either recover useful power or miss that opportunity.

The paper asks where useful electricity recovery appears inside the existing fleet.

## Slide 3: The Claim Is Not the Obvious Part

This slide is important because the result could sound too obvious if phrased badly.

I am not asking the listener to be surprised that young and large plants have advantages. That part is expected.

The stronger question is whether modernization spreads broadly through older and smaller lagging facilities, or whether it mostly appears where conditions are already favorable.

## Slide 4: Main Idea in Plain Words

The main idea is that one fleet average hides two different questions.

First, which plants start generating electricity? That is the entry question.

Second, among generators, who produces more electricity per tonne? That is the performance question.

The paper is built around keeping these two questions separate and then reading them together.

## Slide 5: Data Sources: What Is Observed

The data source is Japan's Ministry of the Environment General Waste Treatment Survey.

The panel covers FY2005 to FY2024 and uses facility-level municipal waste-treatment records. The main fields are power-generation status, electricity output, throughput, facility age, design capacity, fiscal year, prefecture, heating value, and grid-emission context.

The important point is that this is national facility-level evidence, not one local case. But I should also be clear about the boundary: the administrative panel does not directly observe internal retrofit contracts, municipal bargaining, or full lifecycle emissions.

## Slide 6: From Data to Analysis Frames

The full analytical starting point is 23,599 facility-year rows.

Within the coded full-fleet frame, there are 2,948 identifiable facilities.

The start-generating frame has 13,770 at-risk facility-years across facilities first observed without generation. It contains 141 first-entry events.

The generator-output frame has 5,683 observations among identifiable operating generators.

This split is methodological. The first frame studies crossing into electricity generation. The second frame studies output intensity after a facility is already inside generation.

## Slide 7: Two Samples Because There Are Two Questions

The two samples are linked but not identical.

For the start-generating question, the sample is facilities first observed without generation. The outcome is first report of power generation.

For the generator-output question, the sample is already-operating generators. The outcome is electricity generated per tonne processed.

One model for everything would mix the gate into generation with performance after entry. That would make the paper less clear because it would hide where the bottleneck actually sits.

## Slide 8: Method 1: Who Had a Chance to Start?

The first method is a risk-set design.

Only non-generators can first start generating. Facilities already generating in their first observed year are left-censored for this question.

The model asks for the probability of first generation in a given year using prior-year age and prior-year capacity, plus year and prefecture controls. This matters because it describes the facility before first entry, not after entry.

In plain language, the model asks: among facilities still outside power generation, who first reports generation in the next observed year?

## Slide 9: Method 2: How Generator Output Is Compared

The second method is a generator-only comparison.

The outcome is electricity recovered per tonne processed. This focuses on output intensity, not just whether a plant has any power generation.

The models compare age, scale, utilization, heating value, grid context, and year structure. The paper checks pooled OLS, year fixed effects, random effects, and year fixed effects plus random effects.

The interpretation is diagnostic, not causal. The critical question is whether operating generators converge enough to erase inherited facility differences.

## Slide 10: Result 1: Starting Generation Is Selective

The first result is selective entry.

The figure shows that facilities first starting electricity generation are mostly young and large.

Out of 141 observed first-entry events, 102 come from facilities aged 0 to 10 years, and 99 are in the largest capacity quartile.

## Slide 11: What Result 1 Rules Out

This slide explains why the result is more than common sense.

Young facilities have a much higher annual event rate: 5.94 percent for age 0 to 10.

Facilities age 30 or more have an annual event rate of only 0.27 percent. On the capacity side, the smallest quartile has an annual event rate of 0.03 percent, while the largest quartile has 3.11 percent.

The smallest capacity quartile records only one first-entry event, while the largest quartile records 99.

So the evidence does not look like broad late-life catch-up across the whole fleet. It looks like selective modernization.

## Slide 12: What Kind of Entry Was This?

The pathway audit helps avoid overclaiming.

Eighty-two observed first-entry events look reset- or rebuild-like. Thirty-eight look consistent with continuity or in-place upgrade. Twenty are placeholder or forward-dated entries.

The safe interpretation is that capital-side modernization is present, but the paper does not prove replacement is the only pathway.

## Slide 13: Result 2: Entry Is Not the Finish Line

The second result looks inside the generating segment.

Older generators recover less electricity per tonne, and existing generators remain uneven after entry.

The point is not that older plants can never improve. The point is that entering electricity generation does not erase generator hierarchy.

## Slide 14: Generator Convergence Is Limited

The within-to-total variance ratio is 0.1499 in the full sample. In plain terms, most output variation is between facilities rather than movement within the same facility over time.

The post-2011 ratio is even lower at 0.0956.

This is why the result is framed as bounded responsiveness: generator performance does not appear to converge enough to erase inherited gaps.

## Slide 15: Robustness: What I Tried to Break

This slide shows why the pattern is not just a fragile coding artifact.

For adoption, I checked composite facility identifiers and alternative adoption models. The age penalties and positive capacity pattern remain.

For generator output, I checked pre/post-Fukushima splits, capacity terciles, raw-outcome checks, and heating-value restrictions. Age remains negative, while capacity and utilization remain positive.

These checks do not make the estimates causal, but they make the diagnostic pattern more credible.

## Slide 16: Data Limitations Are Real

The data have real limits.

There are 39 official codes with same-year duplicate issues, affecting 444 source rows. There are also 907 operating-generator rows missing official facility codes, mainly around FY2010 to FY2012, so they cannot support the canonical facility-clustered regression frame.

Heating-value data also need plausibility checks: 569 regression-frame rows are outside 3 to 25 megajoules per kilogram.

These limitations discipline the claim. The paper maps bottlenecks and stress-tests data issues; it does not claim a perfect engineering census or a fully identified causal mechanism.

## Slide 17: Decision Logic

If the two bottlenecks are different, planning questions should also differ.

For non-generators, ask whether the plant can start recovering electricity. For generators, ask whether the plant can recover more electricity from the same waste.

Renewal, starting generation, and generator optimization are not the same task.

## Slide 18: Weak Claim vs Defensible Claim

The weak claim is: newer and larger plants generate more. That sounds plausible, but it is not enough for a paper.

The defensible claim is: the fleet has two bottlenecks. Starting generation is selective, and generator output remains uneven after entry.

That is the paper's contribution: mapping where the bottleneck sits.

## Slide 19: Future Work: Mechanisms Not Yet Tested

Future work would move from diagnostic mapping to mechanism testing.

I have not started these extensions yet. The next step could link facility histories to investment and rebuild records, retrofit histories, municipal governance, waste-routing decisions, heat recovery, lifecycle emissions, or comparative fleet data.

The most publishable future direction is probably the one that best explains why some facilities start generation while others do not.

## Slide 20: Feedback Ask

The paper's message is: first ask who starts generating electricity, then ask who generates well after starting.

The feedback I need is targeted.

Is the two-question design strong enough as the paper's main contribution? Which limitation most needs to become a robustness check? Which future-work path is most publishable: capital renewal, governance, lifecycle accounting, or comparative fleet evidence?
