# Table 3. Generator design and annual operating components

The engineering-valid frame contains 6,511 observations across 493 stable administrative lineages. Models include fiscal-year indicators, coarse furnace and facility configuration, furnace count, and stable-lineage-clustered standard errors. The reference reported start-year cohort is 2010 or later.

| Predictor | Log generator design intensity | Log electrical capacity factor |
|:--|--:|--:|
| Reported start before 1990 | -1.565 (0.084) | 0.302 (0.042) |
| Reported start 1990-1999 | -0.883 (0.064) | 0.199 (0.033) |
| Reported start 2000-2009 | -0.267 (0.043) | 0.015 (0.029) |
| Log waste-processing design capacity | 0.532 (0.044) | -0.116 (0.024) |
| Waste-processing utilization | - | 1.695 (0.126) |
| R-squared | 0.549 | 0.339 |

The separate specification diagnostic uses 5,806 engineering-valid rows with plausible heating value and explicitly controls heating value in both specifications; it is distinct from the 6,511-row primary component models above. The legacy coefficients are -0.0349 for age, +0.1001 for waste-processing capacity, and +0.6699 for waste-processing utilization (all p < 0.001). After generator design intensity is added, the corresponding estimates are -0.0020 (p = 0.2977), -0.0092 (p = 0.1991), and -0.0995 (p = 0.2038), while generator design intensity is +0.7532 (p < 0.001). R-squared rises from 0.4737 to 0.8131. This comparison diagnoses specification dependence; it is not a causal mediation analysis.

*Notes: gross MWh/t is an accounting outcome, not net export, useful heat, R1 performance, lifecycle benefit, or independent thermodynamic efficiency. Reported start year is a design-vintage marker rather than a verified turbine-installation date.*
