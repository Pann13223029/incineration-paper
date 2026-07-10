# Generator Design And Operating Component Results

The primary analysis separates installed generator sizing from annual electrical capacity factor. Gross MWh/t is retained as a descriptive product of design intensity, electrical capacity factor, and waste loading; it is not labelled independent operational efficiency.

## Primary Component Models

| model            | label                                |   coefficient |   standard_error |   ci_low |   ci_high |   p_value |
|:-----------------|:-------------------------------------|--------------:|-----------------:|---------:|----------:|----------:|
| design_intensity | Reported start before 1990           |       -1.5647 |           0.0844 |  -1.7300 |   -1.3993 |    0.0000 |
| design_intensity | Reported start 1990-1999             |       -0.8827 |           0.0635 |  -1.0071 |   -0.7583 |    0.0000 |
| design_intensity | Reported start 2000-2009             |       -0.2674 |           0.0430 |  -0.3516 |   -0.1831 |    0.0000 |
| design_intensity | Log waste-processing design capacity |        0.5320 |           0.0435 |   0.4467 |    0.6173 |    0.0000 |
| capacity_factor  | Reported start before 1990           |        0.3020 |           0.0419 |   0.2199 |    0.3842 |    0.0000 |
| capacity_factor  | Reported start 1990-1999             |        0.1985 |           0.0325 |   0.1349 |    0.2621 |    0.0000 |
| capacity_factor  | Reported start 2000-2009             |        0.0149 |           0.0289 |  -0.0417 |    0.0715 |    0.6059 |
| capacity_factor  | Log waste-processing design capacity |       -0.1160 |           0.0236 |  -0.1623 |   -0.0697 |    0.0000 |
| capacity_factor  | Waste-processing utilization         |        1.6951 |           0.1259 |   1.4484 |    1.9419 |    0.0000 |

- Engineering-valid rows: 6,511 across 493 stable administrative lineages.
- Design-intensity model R-squared: 0.5493.
- Electrical-capacity-factor model R-squared: 0.3390.
- Direct gross-output model elasticities: throughput 0.638; installed electrical capacity 0.576.

## Why The Previous Gross-Intensity Regression Is Not Primary

A legacy-style gross-MWh/t model and the same model with installed generator sizing demonstrate what the former specification combined. Both use 5,806 rows with plausible reported heating value and include heating value as a control.

| term                           |   legacy_coefficient |   legacy_p_value |   sizing_adjusted_coefficient |   sizing_adjusted_p_value |
|:-------------------------------|---------------------:|-----------------:|------------------------------:|--------------------------:|
| facility_age_years             |              -0.0349 |           0.0000 |                       -0.0020 |                    0.2977 |
| capacity_100t                  |               0.1001 |           0.0000 |                       -0.0092 |                    0.1991 |
| capacity_utilization_raw       |               0.6699 |           0.0000 |                       -0.0995 |                    0.2038 |
| log_generator_design_intensity |             nan      |         nan      |                        0.7532 |                    0.0000 |

Gross-intensity model R-squared changes from 0.4737 to 0.8131 after generator sizing is included. This is a specification diagnostic, not a causal mediation analysis.

## Adjacent-Year Rank Persistence

- Gross Generation Intensity: r=0.9609 across 5,963 pairs and 470 lineages.
- Generator Design Intensity: r=0.9952 across 5,963 pairs and 470 lineages.
- Electrical Capacity Factor: r=0.8728 across 5,963 pairs and 470 lineages.

Models use fiscal-year indicators, coarse furnace/facility configuration controls, and stable-lineage-clustered standard errors. Associations remain descriptive and do not identify retrofit or operating interventions.
