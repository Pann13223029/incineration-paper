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

Main specification: lagged linear probability hazard with prior-year age band and prior-year design capacity, plus year fixed effects, prefecture fixed effects, and facility-clustered standard errors. Baseline age band: 0-10 years.

| Variable                            | Coef. (pp)   | SE (pp)   |
|:------------------------------------|:-------------|:----------|
| Prior-year age 10-20 yrs (vs 0-10)  | -2.17***     | (0.42)    |
| Prior-year age 20-30 yrs (vs 0-10)  | -1.98***     | (0.49)    |
| Prior-year age 30+ yrs (vs 0-10)    | -1.52*       | (0.59)    |
| Prior-year capacity (per 100 t/day) | 1.47***      | (0.29)    |

- Observations: 11,717
- Facilities: 1,915
- First-adoption events: 140
- R-squared: 0.0305
- Discrete-time logit robustness: same sign pattern for all reported terms; capacity remains positive (coef. 0.453, p=0.011).

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

*Interpretation: observed transition into power generation is more common among facilities that were younger and larger in the prior year. This pattern is consistent with modernization occurring mainly at the capital or investment margin rather than through diffuse late conversion of old small facilities, but the data do not distinguish retrofit from replacement or new build at the same site.*
