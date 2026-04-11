# Regression Results: Determinants of Energy Recovery Efficiency

DV: log(MWh per tonne processed)

| Variable | Model 1 (Pooled OLS) | Model 2 (Year FE) | Model 3 (RE) |
|:---------|:--------------------:|:-----------------:|:------------:|
| facility_age | -0.0284*** | -0.0353*** | -0.0199*** |
| capacity_100t | 0.0795*** | 0.0953*** | 0.0363*** |
| capacity_utilization | 0.6375*** | 0.6837*** | 0.5314*** |
| heating_value_1000kj | -0.0009 | 0.0011 | 0.0000 |
| grid_ef_kgco2_kwh | 0.3854* | -0.4116 | 1.7509*** |
| R-squared | 0.2940 | 0.4585 | 0.2322 |
| N | 5604 | 5604 | 5604 |
