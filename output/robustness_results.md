# Robustness Checks

All models use the canonical identifiable generator frame and facility-clustered standard errors. Early/later coded-window checks avoid treating the FY2010-FY2012 official-code gap as a clean Fukushima identification split.

| Specification | N | Facilities | R² | facility_age | capacity_100t | cap_utilization |
|:---|---:|---:|---:|---:|---:|---:|
| R1: Early coded-window pooled OLS (FY2005-FY2009) | 1400 | 335 | 0.356 | -0.0415*** | 0.0875*** | 0.6410*** |
| R2: Early coded-window year FE (FY2005-FY2009) | 1400 | 335 | 0.376 | -0.0423*** | 0.0891*** | 0.7483*** |
| R3: Later coded-window pooled OLS (FY2013-FY2024) | 4283 | 878 | 0.315 | -0.0313*** | 0.1060*** | 0.8216*** |
| R4: Later coded-window year FE (FY2013-FY2024) | 4283 | 878 | 0.352 | -0.0331*** | 0.1122*** | 0.8089*** |
| R5: Small capacity tercile | 1938 | 414 | 0.204 | -0.0329*** | 0.4432*** | 1.2524*** |
| R6: Large capacity tercile | 1885 | 320 | 0.306 | -0.0247*** | 0.0440*** | 0.5647** |
| R7: Unclipped-log DV pooled OLS | 5683 | 1016 | 0.155 | -0.0274*** | 0.0891*** | 0.7526*** |
| R8: Unclipped-log DV with year indicators | 5683 | 1016 | 0.238 | -0.0346*** | 0.1090*** | 0.7761*** |
| R9: Within-between sensitivity with year FE | 5683 | 1016 | 0.380 | -0.0359*** | 0.1140*** | 0.8646*** |

## Within-between sensitivity

The within-between sensitivity separates facility-level means from within-facility deviations. It is reported as a reviewer shield for the descriptive random-effects interpretation, not as a replacement for the main models.

| Variable | Between-facility coefficient | Within-facility coefficient |
|:---|---:|---:|
| facility_age_years | -0.0359*** | -0.0294*** |
| capacity_100t | 0.1140*** | 0.0210** |
| capacity_utilization_capped | 0.8646*** | 0.5133*** |

*Interpretation: the between-facility columns preserve the cross-facility structure emphasized in the main paper, while the within-facility columns show how limited within-panel movement maps onto the same variables.*
