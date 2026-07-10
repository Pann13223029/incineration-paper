# Extensive-Margin Results: Installed-Generation-Capacity Entry

This stage models first observed reporting of positive installed power-generation capacity among coded facilities first observed without it, separating the entry margin from conditional generator performance.

## Risk Set

- Coded full-fleet frame: 19,827 observations across 2,948 facilities
- Left-censored facilities already reporting positive capacity in first observed year: 913
- Installed-capacity entry risk set: 13,770 facility-years across 2,035 facilities
- Observed installed-capacity entry events in FY2005-FY2024: 141
- Installed-capacity entry events concentrated in FY2013-FY2019: 109 of 141
- Interpretation: the time clustering is reported as an event-timing feature of the administrative panel, not as evidence of a uniquely identified policy shock or reporting change. The main hazard includes fiscal-year indicators.

## Installed-Capacity Entry Model Frame

- Main exact-year lagged model frame: 10,823 observations across 1,911 facilities
- Events retained in lagged model frame: 98
- Broader previous-observed-coded-row frame before exact-year restriction: 11,717 observations across 1,915 facilities with 140 events
- Non-exact lag rows excluded from the main model: 894 rows (42 events)
- First observed at-risk years dropped because lagged predictors are required: 2,035
- Additional rows dropped for missing lagged age/capacity: 18 (12 facilities)

## Event Rates by Facility Age Band

| Age band   |   Risk-set obs |   Capacity-entry events |   Mean capacity (t/day) |   Annual event rate (%) |
|:-----------|---------------:|------------------------:|------------------------:|------------------------:|
| 0-10 yrs   |           1717 |                     102 |                    59.4 |                    5.94 |
| 10-20 yrs  |           4027 |                      14 |                    65.1 |                    0.35 |
| 20-30 yrs  |           5071 |                      17 |                    87.1 |                    0.34 |
| 30+ yrs    |           2933 |                       8 |                   114.2 |                    0.27 |

## Event Rates by Capacity Quartile

| Capacity quartile   |   Risk-set obs |   Capacity-entry events |   Mean capacity (t/day) |   Annual event rate (%) |
|:--------------------|---------------:|------------------------:|------------------------:|------------------------:|
| Q1 (smallest)       |           3493 |                       1 |                    10.9 |                    0.03 |
| Q2                  |           3763 |                       3 |                    41.7 |                    0.08 |
| Q3                  |           3289 |                      38 |                    92.6 |                    1.16 |
| Q4 (largest)        |           3186 |                      99 |                   200.7 |                    3.11 |

## Installed-Capacity Entry Hazard Model

Main specification: exact one-fiscal-year lagged discrete-time logit hazard with prior-year age band and prior-year design capacity, fiscal-year indicators, and facility-clustered standard errors. The more saturated year + prefecture fixed-effects model is retained as sensitivity evidence because entry events are sparse. Reported effects are average marginal effects in percentage points. Baseline prior-year age band: 0-10 years.

| Variable                            | AME (pp)   | SE (pp)   |
|:------------------------------------|:-----------|:----------|
| Prior-year age 10-20 yrs (vs 0-10)  | -1.67***   | (0.25)    |
| Prior-year age 20-30 yrs (vs 0-10)  | -1.94***   | (0.39)    |
| Prior-year age 30+ yrs (vs 0-10)    | -1.24**    | (0.38)    |
| Prior-year capacity (per 100 t/day) | 0.45**     | (0.15)    |

- Observations: 10,823
- Facilities: 1,911
- Installed-capacity entry events: 98
- Events per parameter: 5.44 (98 events / 18 parameters)
- Zero-event fiscal-year levels in main frame: 1 of 14
- Zero-event prefecture levels in main frame: 8 of 47
- Pseudo-R-squared (deviance-based): 0.1829
- Link robustness on the exact-year frame: complementary log-log and linear probability specifications return the same expected sign pattern on all reported terms; capacity remains positive in both (cloglog coef. 0.424; LPM coef. 1.39 pp).

- Duration robustness: adding elapsed at-risk duration in 10-year units to the exact-year year-FE hazard preserves the expected age and capacity sign pattern. The duration coefficient is -1.329** (p=0.00987).

### Adoption specification sensitivity

| Specification                                        | N      |   Events |   Parameters |   Events/parameter |   Age 10-20 AME (pp) |   Age 20-30 AME (pp) |   Age 30+ AME (pp) |   Capacity AME (pp) | Sign pattern   |
|:-----------------------------------------------------|:-------|---------:|-------------:|-------------------:|---------------------:|---------------------:|-------------------:|--------------------:|:---------------|
| Previous observed coded row: year FE + prefecture FE | 11,717 |      140 |           66 |               2.12 |                -1.76 |                -1.72 |              -1.13 |                0.5  | yes            |
| Exact-year: year FE + prefecture FE                  | 10,823 |       98 |           64 |               1.53 |                -1.82 |                -2.31 |              -1.59 |                0.4  | yes            |
| Exact-year: year FE + duration term                  | 10,823 |       98 |           19 |               5.16 |                -1.47 |                -1.55 |              -0.9  |                0.45 | yes            |
| Exact-year: prefecture FE only                       | 10,823 |       98 |           51 |               1.92 |                -1.39 |                -1.18 |              -0.58 |                0.35 | yes            |
| Exact-year: age and capacity only                    | 10,823 |       98 |            5 |              19.6  |                -1.34 |                -1.1  |              -0.48 |                0.4  | yes            |

*Interpretation: the exact-year year fixed-effects model is the main specification because it preserves annual transition timing while reducing sparse-event pressure. The saturated exact-year year + prefecture fixed-effects model and the broader previous-observed-coded-row model are reported as sensitivity checks.*

### Event-definition and capacity functional-form checks

The main event is first observed reporting of positive installed power-generation capacity. An alternative event definition uses positive electricity output. The positive-output risk set contains 13,963 facility-years across 2,110 facilities and 189 events. Its exact-year model retains 10,937 observations and 146 events. The alternative definition strengthens rather than reverses the main pattern:

| Variable                            |   Positive-output AME (pp) |   SE (pp) |
|:------------------------------------|---------------------------:|----------:|
| Prior-year age 10-20 yrs (vs 0-10)  |                      -3.06 |      0.3  |
| Prior-year age 20-30 yrs (vs 0-10)  |                      -3.92 |      0.43 |
| Prior-year age 30+ yrs (vs 0-10)    |                      -2.72 |      0.36 |
| Prior-year capacity (per 100 t/day) |                       0.67 |      0.15 |

Capacity functional-form checks also preserve the finding. Capping prior-year capacity at its model-frame 99th percentile gives a capacity AME of 0.88 pp per 100 t/day. Replacing linear capacity with log(1 + t/day) produces a positive coefficient of 1.424 (p = 3.49e-15), while all age-band coefficients remain negative. These are leverage and functional-form checks, not new headline specifications.

## Competing Panel-Exit Diagnostic

Among 1,894 facilities with no installed-capacity event, 1,305 (68.9%) are last observed before FY2024. A separate next-year hazard treats final disappearance from the coded panel before FY2024 as panel exit. It excludes known non-adjacent code-gap intervals rather than labeling them as exits. This diagnostic contains 12,108 facility-years across 2,022 facilities and 1,285 panel-exit events. The age-30+ AME is +2.60 pp, while the capacity AME is -1.63 pp per 100 t/day. Older non-generators are therefore more likely to disappear from the coded panel, and larger ones are less likely to do so. Panel exit is not equated with verified closure because identifier changes, consolidation, and reporting loss remain possible.

## Post-Adoption Bridge

Of 141 installed-capacity events, 128 record positive electricity output in the event year, 135 by one year, and 138 within the observed event-to-three-year window. Only 3 events reverse the capacity flag in an observed next year. Within three years, 137 events appear in the canonical operating-generator frame. Their first observed mean electricity recovery is 0.328 MWh/t, compared with a same-year incumbent-generator benchmark of 0.328 MWh/t. This closes the empirical bridge between the two margins without treating entry as a causal determinant of later performance.

|   Years from capacity event |   Generator rows |   Events represented |   Mean MWh/t |   Median MWh/t |
|----------------------------:|-----------------:|---------------------:|-------------:|---------------:|
|                           0 |              125 |                  125 |        0.324 |          0.351 |
|                           1 |              102 |                  102 |        0.338 |          0.366 |
|                           2 |               91 |                   91 |        0.325 |          0.361 |
|                           3 |               71 |                   71 |        0.339 |          0.36  |

## Transition Pathway Audit

A conservative event-level audit classifies each observed adoption using continuity in `year_started`, facility age, design capacity, and naming. The goal is not to prove the mechanism of modernization, but to bound what the panel can and cannot support.

Rule set: `reset / rebuild-like` requires an observed `year_started` reset or a mature-to-new age reset on an exact adjacent-year event; `continuity / in-place upgrade` requires no such reset on an exact adjacent-year event; forward-dated or placeholder entries remain weaker evidence; non-adjacent coded-row events are classified as timing-ambiguous rather than forced into a stronger mechanism claim.

| Category                                  |   Events |   Share (%) |
|:------------------------------------------|---------:|------------:|
| Reset / rebuild-like transition           |       50 |        35.5 |
| In-place upgrade / continuity transition  |       36 |        25.5 |
| Forward-dated / placeholder entry         |       12 |         8.5 |
| Timing-ambiguous / non-adjacent coded row |       42 |        29.8 |
| Unresolved / insufficient continuity      |        1 |         0.7 |

*Interpretation: exact adjacent-year events still contain reset/rebuild-like and continuity-type cases, but non-adjacent coded-row events are deliberately weakened to timing-ambiguous evidence. The audit supports selective observed entry, not a uniquely identified modernization mechanism.*

### Event Year Distribution

|   fiscal_year |   Capacity-entry events |
|--------------:|------------------------:|
|          2006 |                       5 |
|          2007 |                       4 |
|          2008 |                       2 |
|          2009 |                       2 |
|          2013 |                      30 |
|          2014 |                       3 |
|          2015 |                      21 |
|          2016 |                      17 |
|          2017 |                      12 |
|          2018 |                      10 |
|          2019 |                      16 |
|          2021 |                       6 |
|          2022 |                       8 |
|          2023 |                       2 |
|          2024 |                       3 |

*Interpretation: first reporting of positive installed generation capacity is more common among facilities that were younger and larger in the previous fiscal year under the exact-year model. The pathway audit suggests that capital-side modernization is empirically present in adjacent-year events, but the evidence is not reducible to one identified mechanism such as replacement alone.*
