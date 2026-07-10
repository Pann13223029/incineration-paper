# Regression Results: Structured Electricity Recovery

DV: log of bounded gross electricity generation per tonne processed

All reported standard errors are clustered by facility.

Canonical regression frame: 5,683 observations across 1,016 facilities.

Sample definition: `sample_definition.md`

## Primary RQ2 Specification

The primary estimand is a year-adjusted cross-facility comparison: how gross MWh/t differs across generator age/vintage, scale, utilization, heating value, and observed plant-configuration profiles within common fiscal years. It is not a causal within-plant aging effect. Both columns use facility-clustered standard errors.

| Variable | Base year-adjusted model | Primary year + technology model |
|:--|--:|--:|
| facility_age_years | -0.0348*** (0.0023) | -0.0329*** (0.0023) |
| capacity_100t | 0.1051*** (0.0087) | 0.1103*** (0.0101) |
| capacity_utilization_capped | 0.7760*** (0.1351) | 0.7600*** (0.1319) |
| heating_value_mj_kg | 0.0033 (0.0021) | 0.0032 (0.0020) |
| Observations | 5,683 | 5,683 |
| Facilities | 1,016 | 1,016 |
| R-squared | 0.3699 | 0.3830 |

Technology controls in the primary model are normalized furnace type, operating mode, facility type, and number of furnaces. Fiscal-year indicators are included in both columns.

## Supplemental Estimator Ladder

| Variable | Model 1 (Pooled OLS) | Model 2 (Year indicators) | Model 3 (RE) | Model 4 (Year indicators + RE) |
|:---------|:--------------------:|:--------------------:|:--------------------:|:--------------------:|
| facility_age_years | -0.0277*** | -0.0348*** | -0.0136*** | -0.0332*** |
| SE | (0.0022) | (0.0023) | (0.0025) | (0.0021) |
| capacity_100t | 0.0853*** | 0.1051*** | 0.0340*** | 0.0522*** |
| SE | (0.0083) | (0.0087) | (0.0084) | (0.0096) |
| capacity_utilization_capped | 0.7462*** | 0.7760*** | 0.5801*** | 0.5434*** |
| SE | (0.1417) | (0.1351) | (0.1086) | (0.0939) |
| heating_value_mj_kg | 0.0008 | 0.0033 | -0.0001 | 0.0012 |
| SE | (0.0023) | (0.0021) | (0.0013) | (0.0010) |
| Observations | 5,683 | 5,683 | 5,683 | 5,683 |
| Facilities | 1,016 | 1,016 | 1,016 | 1,016 |
| R-squared | 0.2453 | 0.3699 | 0.1148 | 0.3074 |

## Adjacent-Year Rank Persistence

- Exact adjacent-year facility pairs: 4,368
- Facilities represented: 915
- Pooled adjacent-year rank correlation: 0.9325
- Median annual rank correlation: 0.9323
- Annual range: 0.8848 to 0.9763
