# Paper Zoom Briefing: Presentation Script

Use this script with the exported `paper/share/paper-zoom-briefing.pdf`. The source deck has 18 audience-facing slides and is designed for a 16-18 minute professor discussion. The slides carry only the main logic; this script carries definitions, model detail, interpretation, and caveats.

## Delivery Rule

Reset the audience with this sentence:

> The paper separates three questions: how coverage changes with the denominator, which non-generators first report installed capacity, and which engineering components produce gross electricity per tonne.

The audience should leave with four conclusions:

- Facility participation is not waste-volume coverage: in FY2024 the analytical shares are 41.1% of facility records, 80.1% of throughput, and 70.5% of processing design capacity.
- First installed-capacity entry is rare and strongly associated with processing scale, but the joint age evidence is uncertain in both risk sets.
- Gross MWh/t is an accounting outcome produced by installed generator sizing, annual electrical capacity factor, and waste-processing utilization.
- The evidence is descriptive and diagnostic. It does not identify retrofit effects, pathway effects, or optimal investments.

## Audience Calibration

- Default to no prior knowledge. Explain the denominator problem before record linkage or regression.
- For a waste-management audience, move quickly through the practical motivation and spend more time on identity, entry definitions, and the limits of gross MWh/t.
- For a statistically trained audience, name the Firth/Jeffreys-prior estimator, the sparse event counts, joint tests, lineage bootstrap, and noncausal estimand.
- For an engineering audience, spend more time on the exact identity and distinguish installed sizing from annual capacity factor.
- If time is short, keep slides 1-8, 10, 12-14, and 16-18. Slides 9, 11, and 15 can be summarized in one sentence each.

## Jargon To Translate Out Loud

- Fleet: all municipal-incineration facility records being studied, not one plant.
- Facility participation: the share of retained facility records reporting positive installed electrical capacity.
- Throughput coverage: the share of recorded waste tonnes processed by facilities reporting positive gross electricity output.
- Design-capacity coverage: the share of waste-processing design capacity located at records with positive installed electrical capacity.
- Stable administrative lineage: a deterministically linked sequence of records judged to represent the same continuing administrative facility or site history. It is not proof that physical assets, ownership, or equipment stayed unchanged.
- Asset episode: a segment within a lineage that starts when reported evidence indicates a material asset or configuration reset.
- Entry: the first report of positive installed electrical-generation capacity after an observed non-generating history. It is not automatically a verified retrofit or commissioning date.
- Risk set: lineage-years that can still experience first reported entry.
- Firth regression: a bias-reduced logistic estimator that adds the Jeffreys-prior penalty; it reduces small-sample bias and keeps estimates finite when sparse data create separation.
- Odds ratio: a comparison of conditional odds, not a percentage-point difference or proof of causation.
- Joint test: one test of whether a group of related coefficients is collectively distinguishable from zero.
- Gross MWh/t: annual gross electricity generated divided by annual tonnes of waste processed. It is not net export, lifecycle benefit, or an independent efficiency score.
- Generator design intensity: installed electrical capacity in kW divided by waste-processing design capacity in t/day.
- Electrical capacity factor: annual gross generation relative to the output implied by installed electrical kW operating for all 8,760 hours.
- Waste-processing utilization: annual throughput divided by 365 times waste-processing design capacity.
- Specification diagnostic: a comparison showing whether an interpretation changes when an omitted accounting component is added. It is not causal mediation.

## Timing Plan

| Segment | Slides | Target time |
|:--|:--|:--|
| Framing and coverage | 1-4 | 4 minutes |
| Identity, frames, and entry method | 5-7 | 4 minutes |
| Entry result and interpretation | 8-9 | 2 minutes |
| Engineering identity and results | 10-15 | 6 minutes |
| Boundaries, contribution, and feedback | 16-18 | 3 minutes |

## Slide 1: Coverage, Entry, and Engineering Components

Thank you for meeting with me. The formal title is **Coverage, Entry, and Engineering Components of Electricity Recovery in Japan's Municipal Waste-Incineration Fleet, FY2005-FY2024**.

The paper is a national facility-level measurement and diagnostic study. It does not ask one vague question about whether waste-to-energy is successful. It separates three questions that require different denominators and samples: coverage across the fleet, first reporting of installed capacity, and the engineering components of gross electricity per tonne among operating generators.

My purpose today is to test whether that architecture is convincing and whether the boundaries of the evidence are clear enough for the manuscript.

Transition: I will begin with the three estimands, then show why a single facility percentage is incomplete.

## Slide 2: The Paper Asks Three Different Questions

RQ1 is a coverage question. A facility count gives every record equal weight, while throughput coverage weights the waste actually processed and design-capacity coverage describes where processing capacity is installed. These measures answer different questions.

RQ2 is an entry question. Among stable lineages observed without installed electrical capacity, which prior age and processing-scale profiles are associated with the first later report of positive capacity? A narrower frame asks the same question after requiring positive throughput in the prior year.

RQ3 begins only among positive-throughput, positive-output generators. It asks how installed generator sizing, annual electrical capacity factor, and waste-processing utilization combine to produce gross MWh/t, and whether the observed cohort hierarchy belongs mainly to design or annual operation.

The sequence is deliberate. Coverage establishes the denominator problem. Entry studies the transition into installed capacity. Component analysis studies variation after positive output exists. Combining these in one model would produce an unclear estimand.

Transition: The distinction begins with two FY2024 facility-count statistics that look similar but are not interchangeable.

## Slide 3: Two FY2024 Count Statistics, Not One

The Ministry's FY2024 national summary reports 415 electricity-generating facilities among 991 incineration facilities, or 41.9%. I use this as published national context.

The analytical panel uses a different definition and reconstructed denominator. It contains 1,014 retained FY2024 facility records, of which 417 report positive installed electrical capacity, or 41.1%.

The official numerator concerns facilities classified as generating electricity. The analytical numerator concerns retained records with positive installed capacity. The record universes also differ. Therefore, I do not use 415 over 991 inside the paper's analytical calculations and I do not present 417 over 1,014 as a reproduction of the Ministry statistic.

If asked why both are shown: the official figure gives recognizable national context, while the analytical figure is the internally consistent measure used with throughput and design capacity.

Transition: Once the analytical denominator is fixed, the volume contrast is much larger than the count contrast.

## Slide 4: Facility Counts Understate Waste Coverage

Figure 1 tracks three annual shares from FY2005 to FY2024. The blue line is facility participation based on positive installed capacity. The grey line is the share of recorded throughput handled by positive-output facilities. The orange line is the share of waste-processing design capacity located at installed-capacity facilities.

In FY2024, facility participation is 41.1%, but positive-output facilities process 80.1% of recorded throughput. Installed-capacity facilities hold 70.5% of processing design capacity. The gap is not a contradiction. Large facilities contribute one unit to a facility count but process much more waste than small facilities.

The trend is also visible over time. Facility participation rises from 21.6% in FY2005 to 41.1% in FY2024; throughput coverage rises from 60.5% to 80.1%; and design-capacity coverage rises from 56.0% to 70.5%.

The supported conclusion is denominator discipline. Most recorded waste is already processed at facilities with positive output even though installed capacity appears in fewer than half of retained records. This does not imply that every remaining non-generator is feasible or desirable to equip.

Transition: To study first entry rather than annual cross-sections, the records must be linked before any lag or event is created.

## Slide 5: Audited Identity Comes Before Transitions

The parser reads 23,599 raw rows from 20 annual workbooks. Six rows are exact duplicates of another standardized source record. Collapsing them leaves 23,593 retained facility-year records.

Official codes cannot serve as a complete longitudinal key. The resolver instead links records deterministically within prefecture using normalized facility name, municipality, reported start year, processing capacity, furnace count, facility type, and official code where available. It resolves adjacent years before short gaps and enforces one-to-one assignment.

The result is 1,690 stable administrative lineages and 1,767 asset episodes. A stable administrative lineage is a linked administrative history judged to represent the same continuing facility or site record. It does not mean that buildings, furnaces, ownership, or generators are physically unchanged. An asset episode is a segment within that lineage; a new episode begins when reported start year, age, name, or configuration evidence indicates a material reset.

The resolver rejects sub-threshold and weak ambiguous links before assignment. Sixteen accepted links across 14 lineages still have a low two-sided margin but retain exact-name or official-code evidence. Every one is exposed, and the models are rerun after excluding each affected lineage.

This distinction is essential. The broad entry lag uses the stable lineage and may cross an inferred episode boundary; a separate continuity sensitivity requires the same episode. Administrative absence is never interpreted as physical closure.

Transition: With identity established, each research question receives its own analytical frame.

## Slide 6: Analytical Frames Match the Estimands

The descriptive installed-capacity risk set has 16,519 rows across 1,223 lineages and contains 55 first reported entry events. This broad descriptive count is useful for pathway classification and the bridge from installed capacity to reported output.

The broad exact-year Firth model is narrower: 15,154 adjacent-year, complete-covariate risk rows across 1,137 lineages, with 35 events. The prior-operation Firth frame additionally requires positive prior-year throughput. It has 13,072 rows across 1,019 lineages and 33 events.

A same-episode sensitivity has 15,095 rows, 1,135 lineages, and 24 events. An identity-certain sensitivity has 15,107 rows, 1,130 lineages, and all 35 events. The low event counts, not the large row counts, govern inferential strength.

The engineering component frame is different again. It contains 6,511 positive-throughput, positive-output generator-years across 493 stable lineages after predefined engineering checks.

Entry is defined as first reporting positive installed electrical capacity. It is not automatically a physical project date. Installed capacity and output are closely related but not identical administrative states.

Transition: The sparse number of modeled entry events is why ordinary maximum-likelihood logistic regression is not the primary estimator.

## Slide 7: Why Firth for First Entry?

The entry analysis is a discrete-time event-history model. Each at-risk lineage-year has a binary outcome: did this lineage first report positive installed capacity in the next exact fiscal-year record?

The predictors are prior-year age band and prior-year processing design capacity, plus calendar-era indicators and flexible elapsed-risk-duration bands. Lagging the predictors keeps them on the pre-entry side of the transition. The capacity transform is log of one plus capacity divided by 100, which supports an interpretable 300-versus-100 t/day contrast.

Firth regression is a bias-reduced logistic estimator. It maximizes the ordinary binomial log-likelihood plus one-half the log determinant of the expected information matrix, which is the Jeffreys-prior penalty. In practical terms, it reduces first-order small-sample bias and avoids infinite coefficients when sparse events create separation.

The focal coefficient intervals use 499 deterministic bootstrap replications that resample whole stable lineages. All requested fits converge and return every focal coefficient. Joint age tests use the covariance of the age coefficients across those lineage bootstraps; machine-readable model-based uncertainty is labelled separately.

Firth solves an estimation problem; it does not solve an information problem. With 35 broad and 24 same-episode events, the model remains parsimonious and cannot identify unobserved finance, procurement, governance, or equipment mechanisms.

Transition: The model gives one clear entry result and one deliberately cautious result.

## Slide 8: Scale Selection Is Clear; Age Is Uncertain

Figure 2 reports conditional odds ratios from the exact-year and prior-operation Firth models. The scale contrast compares a facility with 300 t/day of processing design capacity against one with 100 t/day, conditional on age band, calendar era, and elapsed risk duration.

The scale odds ratios are 6.13 in the broad exact-year frame and 6.25 after requiring positive prior-year throughput. The corresponding capacity coefficients are 2.6158 and 2.6444, and both lineage-bootstrap intervals are wholly positive. Because the prior-operation frame is nested and excludes only two events, these are parallel sensitivity estimates, not an independent between-group comparison.

Age is weaker and continuity-sensitive evidence. The lineage-bootstrap joint age p-values are .3800 in the broad frame, .1863 after prior operation, .0508 under same-episode continuity, and .3566 after excluding identity-uncertain lineages. The same-episode frame has only 24 events, and its model-based covariance gives a stronger p-value than its lineage-bootstrap covariance.

The designated interpretation follows the lineage-bootstrap joint tests, not isolated point estimates or individual intervals. Therefore, the paper does not claim a general independent age pattern. The near-threshold continuity result is disclosed as sensitivity, not promoted as the preferred model.

An odds ratio near six does not mean a sixfold probability and does not show that increasing a facility from 100 to 300 t/day would cause entry. Entry is rare, and scale can proxy for many unobserved municipal, financial, and technical conditions.

Transition: The next slide separates the supported scale conclusion from the unsupported mechanism and age claims.

## Slide 9: What the Entry Result Supports

The supported RQ2 conclusion is narrow: first reporting of installed capacity is rare and strongly concentrated among larger processing facilities in both modeled risk sets.

The result does not support an age-only screening rule. Negative point estimates do not override the null broad and identity-certain tests or the sparse, near-threshold same-episode result.

The 55 descriptive events show multiple administrative pathways: 35 continuity-lineage events, 11 rebuild/replacement-like events, and nine forward-dated or placeholder events. In the bridge to output, 47 of the 55 report positive gross generation in the event year and 51 do so by the following observed fiscal year.

These pathway labels are evidence rules. A continuity event stays within the same lineage and asset episode across adjacent years without a reported reset. A rebuild/replacement-like event has a reported reset. A forward-dated event has future-start-year or placeholder evidence. None verifies a physical project mechanism.

Transition: After entry, gross electricity per tonne must be unpacked before it can be interpreted as performance.

## Slide 10: Gross MWh/t Is an Accounting Identity

Let gross MWh/t equal annual gross electricity generated, G, divided by annual waste throughput, W. It is an observable accounting intensity, not net electricity export and not an independent engineering-efficiency measure.

Generator design intensity, D, equals installed electrical capacity in kW divided by waste-processing design capacity in tonnes per day. It describes how large the installed generator is relative to the facility's waste-processing design scale.

Electrical capacity factor, F, equals annual gross generation divided by 8.76 times installed electrical kW. The factor 8.76 converts one kW operating for 8,760 hours into annual MWh. Capacity factor therefore describes annual use of installed electrical capacity, subject to the reporting boundaries of these data.

Waste-processing utilization, U, equals annual throughput divided by 365 times waste-processing design capacity. Substituting those definitions gives the exact facility-year identity:

> gross MWh/t = 0.024 × design intensity × capacity factor ÷ processing utilization.

This identity is arithmetic. It shows why the gross ratio cannot be interpreted independently of installed sizing, annual electrical use, and waste loading. It does not make any component exogenous, and the division by utilization should not be read as a recommendation to process less waste.

Transition: The primary generator analysis therefore models design intensity and capacity factor separately.

## Slide 11: Engineering Frame Separates Design From Operation

The initial operating-generator frame has 6,660 rows with positive throughput and positive gross output. The predefined checks exclude rather than clip 149 rows, leaving 6,511 engineering-valid generator-years across 493 stable lineages.

The checks require gross intensity between 0.01 and 0.80 MWh/t, electrical capacity factor between 0.02 and 1.20, processing utilization between 0.02 and 1.20, generator design intensity between 0.1 and 100 kW per t/day, and complete non-negative age and model fields.

The first component model explains log generator design intensity using reported start-year cohort, log processing design capacity, coarse technology and facility configuration, furnace count, and fiscal year. The second explains log electrical capacity factor using the same structure plus processing utilization. Standard errors are clustered by stable lineage.

Reported start year is treated as a design-vintage marker. It is not a verified boiler, turbine, or generator installation date. Design intensity is mainly a between-asset design attribute, while capacity factor is an annual operating component with more within-asset movement.

Transition: Figure 3 shows that the reported cohort hierarchy is much stronger for installed sizing than for annual capacity factor.

## Slide 12: The Cohort Hierarchy Is Mainly Generator Sizing

Figure 3 compares medians by reported facility start-year cohort. Median generator design intensity rises from 5.33 kW per t/day before 1990, to 10.83 in the 1990s, 15.83 in the 2000s, and 20.59 in 2010 or later.

Median gross MWh/t rises in parallel, from 0.145 to 0.283, 0.348, and 0.475. But electrical capacity factor does not show the same monotonic cohort gradient: the medians are 61.9%, 62.5%, 56.1%, and 66.4%.

The adjusted design-intensity model reinforces this pattern. Relative to the 2010-or-later cohort, log design-intensity coefficients are -1.565 before 1990, -0.883 for 1990-1999, and -0.267 for 2000-2009, all with p<.001. The processing-scale elasticity is 0.532, with a 95% interval from 0.447 to 0.617.

The capacity-factor model tells a different story. Conditional on observed scale, waste utilization, technology, furnace count, and year, older cohorts are not uniformly lower. The 2000s coefficient is 0.015 with p=.606.

The supported interpretation is a design-vintage and generator-sizing hierarchy, not a simple claim that older facilities operate less efficiently.

Transition: A heating-controlled specification diagnostic shows why that distinction changes the prior age interpretation.

## Slide 13: The Age Association Is Specification-Dependent

This diagnostic uses 5,806 engineering-valid rows with reported heating value in the plausible 3 to 25 MJ/kg range. Heating value is controlled in both specifications, so the comparison isolates what changes when generator design intensity is represented.

In the legacy-style gross-MWh/t model without design intensity, the reported-age coefficient is -0.0349, the processing-capacity coefficient is +0.1001, and the processing-utilization coefficient is +0.6699. All three have p<.001, and R-squared is .4737.

After adding log generator design intensity, the age coefficient becomes -0.0020 with p=.2977. The processing-capacity coefficient becomes -0.0092 with p=.1994, and utilization becomes -0.0995 with p=.2038. Design intensity enters at +0.7532 with p<.001, and R-squared rises to .8131.

The inference is specification dependence. The former age, processing-scale, and utilization associations with gross MWh/t are not stable after the omitted installed-sizing component is represented. This is not a causal mediation model and does not prove that design intensity causes the entire difference.

Transition: The observed entry pathways also begin at different positions, mainly along the sizing component.

## Slide 14: Observed Pathways Start at Different Ranks

Figure 4 asks where entrants sit in the first complete post-entry year relative to engineering-valid generators observed in the same fiscal year. Using within-year percentile ranks reduces fleet-wide time differences, but it does not solve selection into pathways.

For 27 continuity-lineage entrants, mean ranks are 40 for gross MWh/t, 37 for design intensity, and 54 for capacity factor. For 11 rebuild/replacement-like entrants, the corresponding mean ranks are 72, 66, and 65.

Six forward-dated or placeholder observations are omitted from the plotted contrast because that category is sparse and its administrative timing is hard to interpret. Across all 44 exact-year entrants with an available first-complete-year outcome, the pooled mean ranks are near the middle of the same-year generator distribution.

The continuity-versus-rebuild difference is largest for generator design intensity, with a smaller capacity-factor difference. That is consistent with the broader component result, but it is not an estimated pathway effect. The groups are small, pathway assignment is administrative, follow-up is selected, and there is no counterfactual matching.

Transition: The main component interpretation survives several predefined sensitivity checks, but those checks do not change its noncausal status.

## Slide 15: Stress Tests Preserve the Component Interpretation

The period split estimates the processing-scale coefficient in the design-intensity model at 0.474 in FY2005-FY2014 and 0.577 in FY2015-FY2024. The positive sizing relationship therefore appears in both halves of the study window.

Changing engineering bounds gives similar coefficients: 0.520 under conservative bounds and 0.536 under broad bounds. Giving each stable lineage equal total weight also preserves the reported start-year cohort hierarchy in generator sizing, so lineages with longer observed histories are not solely creating the result.

Excluding every identity-uncertain lineage leaves 6,450 rows across 487 lineages and gives a design-intensity scale coefficient of 0.533, nearly the main estimate of 0.532.

Within-asset-episode fixed effects and exact-adjacent first differences are used only for operating components that have meaningful within-asset variation. Those checks retain a positive association between processing utilization and electrical capacity factor. Design intensity is not promoted as a within-episode estimand because it is predominantly a between-asset design attribute.

The purpose of these checks is robustness of description. They do not make throughput, maintenance, installed capacity, or output exogenous, and they do not turn the accounting identity into a causal production function.

Transition: The final interpretation depends on stating those evidence boundaries directly.

## Slide 16: Evidence Boundaries Are Part of the Result

First, identity remains inferred. The resolver is deterministic, audited, and designed around code discontinuities and difficult links, but no physical-site registry verifies ownership, construction, equipment replacement, or closure histories. Administrative absence is not modeled as physical exit.

Second, entry is rare and partly left-censored. Firth estimation addresses bias and separation, but it cannot overcome 35 broad events or only 24 under same-episode continuity. The model lacks project finance, procurement, contracts, catchment agreements, maintenance histories, prices, and detailed equipment dates. Scale may proxy for these conditions.

Third, generator fields have strict boundaries. Gross generation is not net export. Useful heat and on-site electricity use are incomplete. The data do not provide a common lifecycle, emissions, cost, outage, or economic-welfare measure. Gross MWh/t is not an R1 measure or a complete thermodynamic efficiency score.

Fourth, annual throughput, capacity factor, maintenance, waste composition, and output can be jointly determined. Controls, clustered uncertainty, robustness checks, and exact identities do not create exogenous variation.

Therefore, the paper makes descriptive and diagnostic claims. It does not estimate the causal effect of a retrofit, enlarging processing capacity, replacement, pathway assignment, or policy.

Transition: Within those boundaries, the paper still changes how the fleet should be measured and how the next question should be chosen.

## Slide 17: Contribution: Measurement Before Mechanism

For monitoring, report facility participation, throughput coverage, and processing design-capacity coverage together. The FY2024 contrast between 41.1%, 80.1%, and 70.5% shows why one headline facility percentage is insufficient.

For entry screening, processing scale is a strong marker for further feasibility work, but the model does not support an age-only rule and does not rank projects. A project decision still requires technical, financial, municipal, and waste-system evidence.

For existing generators, decompose gross MWh/t before benchmarking. A low gross ratio can reflect smaller installed generator sizing, annual capacity-factor conditions, waste loading, or combinations of these. Reported design vintage must be separated from verified equipment history.

The paper's contribution is a measurement architecture: reconstruct stable lineages before transitions, keep count and volume denominators separate, use sparse-event methods for entry, and apply the exact engineering identity before interpreting hierarchy.

The next evidence should link procurement, construction, generator histories, net export, useful heat, outages, waste composition, finance, and municipal decisions to specific projects. That is the route from diagnostic mapping to mechanism testing.

Transition: I will stop with three questions for feedback.

## Slide 18: Discussion Questions

The first question is structural: is the three-estimand architecture convincing, or does the manuscript still feel like three analyses placed beside one another?

The second is explanatory: are the Firth entry design, the risk-set distinction, and the exact gross-MWh/t identity clear enough for a reader who is not a specialist in rare-event statistics or energy engineering?

The third is strategic: which missing project-level evidence should be prioritized next: verified capital and equipment histories, municipal governance and finance, or net export, heat use, outage, and waste-composition data?

Stop here. Do not add another result after asking for feedback.
