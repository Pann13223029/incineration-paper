# Robustness Checks

All models use the canonical regression frame and facility-clustered standard errors.

| Specification | N | Facilities | R² | facility_age | capacity_100t | cap_utilization |
|:---|---:|---:|---:|---:|---:|---:|
| R1: Pre-Fukushima pooled OLS (FY2005-FY2011) | 1400 | 335 | 0.359 | -0.0418*** | 0.0847*** | 0.6310*** |
| R2: Pre-Fukushima year FE (FY2005-FY2011) | 1400 | 335 | 0.381 | -0.0427*** | 0.0857*** | 0.7417*** |
| R3: Post-Fukushima pooled OLS (FY2012-FY2024) | 4283 | 878 | 0.330 | -0.0317*** | 0.1033*** | 0.8308*** |
| R4: Post-Fukushima year FE (FY2012-FY2024) | 4283 | 878 | 0.354 | -0.0331*** | 0.1104*** | 0.8159*** |
| R5: Small capacity tercile | 1938 | 414 | 0.208 | -0.0329*** | 0.4521*** | 1.2493*** |
| R6: Large capacity tercile | 1885 | 320 | 0.341 | -0.0251*** | 0.0464*** | 0.5969** |
| R7: Raw DV pooled OLS | 5683 | 1016 | 0.309 | -0.0071*** | 0.0210*** | 0.1716*** |
| R8: Raw DV year FE | 5683 | 1016 | 0.519 | -0.0091*** | 0.0256*** | 0.1778*** |
