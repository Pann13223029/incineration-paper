# Administrative-Lineage And Engineering Data-Quality Audit

## Enforced Grain

- Administrative rows: 23,593; audited stable administrative lineages: 1,690; asset episodes: 1,767.
- Missing administrative-lineage IDs: 0.
- Missing asset-episode IDs: 0.
- Duplicate stable-lineage-year rows: 0.
- Official facility codes are audited only within fiscal year. They are not used as longitudinal identifiers.

## Sample Arithmetic

| analysis   | stage                                  |   rows |   rows_removed_from_prior_stage |   stable_sites | events   |
|:-----------|:---------------------------------------|-------:|--------------------------------:|---------------:|:---------|
| generator  | Administrative panel                   |  23593 |                               0 |           1690 | NA       |
| generator  | Audited administrative-lineage fleet   |  23593 |                               0 |           1690 | NA       |
| generator  | Installed generation reported          |   6950 |                           16643 |            522 | NA       |
| generator  | Positive annual throughput             |   6694 |                             256 |            505 | NA       |
| generator  | Positive gross electricity output      |   6660 |                              34 |            504 | NA       |
| generator  | Passes all engineering bounds          |   6511 |                             149 |            493 | NA       |
| generator  | Component-model complete cases         |   6511 |                               0 |            493 | NA       |
| entry      | Observed non-generator risk set        |  16519 |                               0 |           1223 | 55       |
| entry      | Exact-year lag and complete covariates |  15154 |                            1365 |           1137 | 35       |
| entry      | Exact-year lag after prior operation   |  13072 |                            2082 |           1019 | 33       |

## Age Handling

The raw panel contains 36 missing and 355 negative reported ages. Negative values are converted to missing, not floored to zero. The constructed fleet has 391 missing and 0 negative analysis ages; the operating-generator sample has 52 missing and 0 negative analysis ages. The component-model frame has 0 missing ages.

## Engineering Bounds And Heating Values

| scope                            | metric                                    |   lower_bound |   upper_bound |   rows |   missing |   below_bound |   within_bounds |   above_bound |
|:---------------------------------|:------------------------------------------|--------------:|--------------:|-------:|----------:|--------------:|----------------:|--------------:|
| Operating generator rows         | Gross generation intensity (MWh/t)        |         0.010 |         0.800 |   6660 |         0 |            51 |            6575 |            34 |
| Operating generator rows         | Electrical capacity factor                |         0.020 |         1.200 |   6660 |         0 |            26 |            6616 |            18 |
| Operating generator rows         | Waste-processing utilization              |         0.020 |         1.200 |   6660 |         0 |             3 |            6650 |             7 |
| Operating generator rows         | Generator design intensity (kW per t/day) |         0.100 |       100.000 |   6660 |         0 |             0 |            6660 |             0 |
| Operating generator rows         | Heating value (MJ/kg; plausibility only)  |         3.000 |        25.000 |   6660 |       106 |           594 |            5937 |            23 |
| Engineering-valid component rows | Gross generation intensity (MWh/t)        |         0.010 |         0.800 |   6511 |         0 |             0 |            6511 |             0 |
| Engineering-valid component rows | Electrical capacity factor                |         0.020 |         1.200 |   6511 |         0 |             0 |            6511 |             0 |
| Engineering-valid component rows | Waste-processing utilization              |         0.020 |         1.200 |   6511 |         0 |             0 |            6511 |             0 |
| Engineering-valid component rows | Generator design intensity (kW per t/day) |         0.100 |       100.000 |   6511 |         0 |             0 |            6511 |             0 |
| Engineering-valid component rows | Heating value (MJ/kg; plausibility only)  |         3.000 |        25.000 |   6511 |       102 |           581 |            5806 |            22 |

Of 6,660 positive-throughput, positive-output generator rows, 149 fail at least one predeclared engineering check and 38 fail more than one. Heating value is within 3-25 MJ/kg for 5,937 rows. Heating value is a plausibility/control field, not a condition for the primary component decomposition.

## Same-Year Official-Code Duplicates

|   fiscal_year |   rows |   coded_rows |   unique_official_codes |   duplicate_code_year_groups |   rows_in_duplicate_code_year_groups |   max_rows_per_official_code |   stable_sites_in_duplicate_groups |
|--------------:|-------:|-------------:|------------------------:|-----------------------------:|-------------------------------------:|-----------------------------:|-----------------------------------:|
|          2005 |   1318 |         1318 |                    1315 |                            3 |                                    6 |                            2 |                                  6 |
|          2006 |   1301 |         1301 |                    1301 |                            0 |                                    0 |                            1 |                                  0 |
|          2007 |   1306 |         1306 |                    1287 |                           19 |                                   38 |                            2 |                                 38 |
|          2008 |   1305 |         1277 |                    1217 |                           31 |                                   91 |                           23 |                                 91 |
|          2009 |   1309 |         1283 |                    1225 |                           30 |                                   88 |                           23 |                                 88 |
|          2010 |   1244 |            0 |                       0 |                            0 |                                    0 |                            0 |                                  0 |
|          2011 |   1250 |            0 |                       0 |                            0 |                                    0 |                            0 |                                  0 |
|          2012 |   1222 |            0 |                       0 |                            0 |                                    0 |                            0 |                                  0 |
|          2013 |   1199 |         1199 |                    1199 |                            0 |                                    0 |                            1 |                                  0 |
|          2014 |   1207 |         1207 |                    1207 |                            0 |                                    0 |                            1 |                                  0 |
|          2015 |   1192 |         1192 |                    1192 |                            0 |                                    0 |                            1 |                                  0 |
|          2016 |   1154 |         1154 |                    1154 |                            0 |                                    0 |                            1 |                                  0 |
|          2017 |   1139 |         1139 |                    1139 |                            0 |                                    0 |                            1 |                                  0 |
|          2018 |   1128 |         1128 |                    1128 |                            0 |                                    0 |                            1 |                                  0 |
|          2019 |   1093 |         1093 |                    1093 |                            0 |                                    0 |                            1 |                                  0 |
|          2020 |   1087 |         1087 |                    1087 |                            0 |                                    0 |                            1 |                                  0 |
|          2021 |   1060 |         1060 |                    1060 |                            0 |                                    0 |                            1 |                                  0 |
|          2022 |   1038 |         1038 |                    1038 |                            0 |                                    0 |                            1 |                                  0 |
|          2023 |   1027 |         1027 |                    1027 |                            0 |                                    0 |                            1 |                                  0 |
|          2024 |   1014 |         1014 |                    1014 |                            0 |                                    0 |                            1 |                                  0 |

There are 83 duplicate official-code-year groups. These collisions do not create duplicate stable-lineage-year observations and are not resolved by treating official codes as persistent facility IDs.

## Identity-Uncertainty Exposure

The resolver accepts and explicitly exposes 16 uncertain links, all supported by a strong exact-name or official-code signal. Those links occur within 14 administrative lineages. Excluding every affected lineage leaves 15,107 exact-year entry-risk rows across 1,130 lineages and 35 events, versus 15,154/1,137/35 in the broad frame. The engineering-valid component sample retains 6,450 rows across 487 lineages after the same whole-lineage exclusion.

## Audit Conclusion

The model sample is a complete-case subset of the positive-output generator sample after explicit engineering exclusions. The audit supports administrative-lineage clustering and component interpretation; it does not establish measurement error absence or causal identification.
