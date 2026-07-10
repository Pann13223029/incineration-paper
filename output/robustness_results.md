# Robustness Checks

All models use the canonical identifiable generator frame and facility-clustered standard errors. Early/later coded-window checks avoid treating the FY2010-FY2012 official-code gap as a clean Fukushima identification split.

| Specification | N | Facilities | R² | facility_age | capacity_100t | cap_utilization |
|:---|---:|---:|---:|---:|---:|---:|
| R1: Early coded-window pooled OLS (FY2005-FY2009) | 1400 | 335 | 0.359 | -0.0418*** | 0.0847*** | 0.6310*** |
| R2: Early coded-window year FE (FY2005-FY2009) | 1400 | 335 | 0.381 | -0.0427*** | 0.0857*** | 0.7417*** |
| R3: Later coded-window pooled OLS (FY2013-FY2024) | 4283 | 878 | 0.330 | -0.0317*** | 0.1033*** | 0.8308*** |
| R4: Later coded-window year FE (FY2013-FY2024) | 4283 | 878 | 0.354 | -0.0331*** | 0.1104*** | 0.8159*** |
| R5: Small capacity tercile | 1938 | 414 | 0.208 | -0.0329*** | 0.4521*** | 1.2493*** |
| R6: Large capacity tercile | 1885 | 320 | 0.341 | -0.0251*** | 0.0464*** | 0.5969** |
| R7: Raw DV pooled OLS | 5683 | 1016 | 0.309 | -0.0071*** | 0.0210*** | 0.1716*** |
| R8: Raw DV year FE | 5683 | 1016 | 0.519 | -0.0091*** | 0.0256*** | 0.1778*** |
| R9: Within-between sensitivity with year FE | 5683 | 1016 | 0.382 | -0.0358*** | 0.1110*** | 0.8707*** |

## Within-between sensitivity

The within-between sensitivity separates facility-level means from within-facility deviations. It is reported as a reviewer shield for the descriptive random-effects interpretation, not as a replacement for the main models.

| Variable | Between-facility coefficient | Within-facility coefficient |
|:---|---:|---:|
| facility_age_years | -0.0358*** | -0.0313*** |
| capacity_100t | 0.1110*** | 0.0219** |
| capacity_utilization_capped | 0.8707*** | 0.5096*** |

*Interpretation: the between-facility columns preserve the cross-facility structure emphasized in the main paper, while the within-facility columns show how limited within-panel movement maps onto the same variables.*
