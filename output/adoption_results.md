# Extensive-Margin Results: Observed Transition Into Power Generation

This stage models the observed first transition into power generation among coded facilities first observed without it, separating the extensive margin from conditional generator efficiency.

## Risk Set

- Coded full-fleet frame: 19,827 observations across 2,948 facilities
- Left-censored facilities already generating in first observed year: 913
- Adoption risk set: 13,770 facility-years across 2,035 facilities
- Observed first-adoption events in FY2005-FY2024: 141
- First-adoption events concentrated in FY2013-FY2019: 109 of 141

## Adoption Model Frame

- Lagged model frame: 11,717 observations across 1,915 facilities
- Events retained in lagged model frame: 140
- First observed at-risk years dropped because lagged predictors are required: 2,035
- Additional rows dropped for missing lagged age/capacity: 18 (12 facilities)

## Event Rates by Facility Age Band

| Age band   |   Risk-set obs |   First adoptions |   Mean capacity (t/day) |   Annual event rate (%) |
|:-----------|---------------:|------------------:|------------------------:|------------------------:|
| 0-10 yrs   |           1717 |               102 |                    59.4 |                    5.94 |
| 10-20 yrs  |           4027 |                14 |                    65.1 |                    0.35 |
| 20-30 yrs  |           5071 |                17 |                    87.1 |                    0.34 |
| 30+ yrs    |           2933 |                 8 |                   114.2 |                    0.27 |

## Event Rates by Capacity Quartile

| Capacity quartile   |   Risk-set obs |   First adoptions |   Mean capacity (t/day) |   Annual event rate (%) |
|:--------------------|---------------:|------------------:|------------------------:|------------------------:|
| Q1 (smallest)       |           3493 |                 1 |                    10.9 |                    0.03 |
| Q2                  |           3763 |                 3 |                    41.7 |                    0.08 |
| Q3                  |           3289 |                38 |                    92.6 |                    1.16 |
| Q4 (largest)        |           3186 |                99 |                   200.7 |                    3.11 |

## Adoption Hazard Model

Main specification: lagged discrete-time logit hazard with prior-year age band and prior-year design capacity, plus year fixed effects, prefecture fixed effects, and facility-clustered standard errors. Reported effects are average marginal effects in percentage points. Baseline prior-year age band: 0-10 years.

| Variable                            | AME (pp)   | SE (pp)   |
|:------------------------------------|:-----------|:----------|
| Prior-year age 10-20 yrs (vs 0-10)  | -1.76***   | (0.28)    |
| Prior-year age 20-30 yrs (vs 0-10)  | -1.72***   | (0.42)    |
| Prior-year age 30+ yrs (vs 0-10)    | -1.13**    | (0.39)    |
| Prior-year capacity (per 100 t/day) | 0.50*      | (0.20)    |

- Observations: 11,717
- Facilities: 1,915
- First-adoption events: 140
- Pseudo-R-squared (deviance-based): 0.1842
- Robustness: lagged complementary log-log and lagged linear probability specifications return the same sign pattern on all reported terms; capacity remains positive in both (cloglog coef. 0.345, p=1.67e-07; LPM coef. 1.47 pp, p=5.03e-07).

## Transition Pathway Audit

A conservative event-level audit classifies each observed adoption using continuity in `year_started`, facility age, design capacity, and naming. The goal is not to prove the mechanism of modernization, but to bound what the panel can and cannot support.

Rule set: `reset / rebuild-like` requires an observed `year_started` reset or a mature-to-new age reset; `continuity / in-place upgrade` requires no such reset on the observed event row; forward-dated or placeholder entries remain unresolved rather than forced into a stronger mechanism claim.

| Category                                 |   Events |   Share (%) |
|:-----------------------------------------|---------:|------------:|
| Reset / rebuild-like transition          |       82 |        58.2 |
| In-place upgrade / continuity transition |       38 |        27   |
| Forward-dated / placeholder entry        |       20 |        14.2 |
| Unresolved / insufficient continuity     |        1 |         0.7 |

*Interpretation: the largest observed pathway bucket is reset- or rebuild-like, a meaningful minority retain continuity consistent with in-place upgrades, and a nontrivial set are forward-dated or placeholder entries that should not be forced into a stronger mechanism claim than the data support.*

### Event Year Distribution

|   fiscal_year |   First adoptions |
|--------------:|------------------:|
|          2006 |                 5 |
|          2007 |                 4 |
|          2008 |                 2 |
|          2009 |                 2 |
|          2013 |                30 |
|          2014 |                 3 |
|          2015 |                21 |
|          2016 |                17 |
|          2017 |                12 |
|          2018 |                10 |
|          2019 |                16 |
|          2021 |                 6 |
|          2022 |                 8 |
|          2023 |                 2 |
|          2024 |                 3 |

*Interpretation: observed transition into power generation is more common among facilities that were younger and larger in the prior year. Under the stronger hazard specification, the age penalty remains negative and the capacity effect remains positive, while the pathway audit suggests that capital-side modernization is empirically present but not reducible to one identified mechanism such as replacement alone.*
