# Regression Results: Determinants of Energy Recovery Efficiency

DV: winsorized log(MWh per tonne processed)

All reported standard errors are clustered by facility.

Canonical regression frame: 5,683 observations across 1,016 facilities.

Sample definition: `sample_definition.md`

| Variable | Model 1 (Pooled OLS) | Model 2 (Year FE) | Model 3 (RE) | Model 4 (Year FE + RE) |
|:---------|:--------------------:|:--------------------:|:--------------------:|:--------------------:|
| facility_age_years | -0.0279*** | -0.0348*** | -0.0188*** | -0.0332*** |
| SE | (0.0022) | (0.0022) | (0.0025) | (0.0021) |
| capacity_100t | 0.0874*** | 0.1030*** | 0.0405*** | 0.0519*** |
| SE | (0.0083) | (0.0086) | (0.0083) | (0.0096) |
| capacity_utilization_capped | 0.7468*** | 0.7789*** | 0.6199*** | 0.5411*** |
| SE | (0.1421) | (0.1346) | (0.0997) | (0.0943) |
| heating_value_mj_kg | 0.0010 | 0.0032 | 0.0006 | 0.0012 |
| SE | (0.0023) | (0.0021) | (0.0012) | (0.0010) |
| grid_ef_kgco2_kwh | 0.3182 | -0.4466 | 1.6333*** | -0.1951 |
| SE | (0.2219) | (0.2714) | (0.1965) | (0.2101) |
| Observations | 5,683 | 5,683 | 5,683 | 5,683 |
| Facilities | 1,016 | 1,016 | 1,016 | 1,016 |
| R-squared | 0.2470 | 0.3721 | 0.1647 | 0.3076 |
