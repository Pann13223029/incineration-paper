# Data-Quality and Identifier-Sensitivity Checks

This report audits two non-core but reviewer-relevant data-quality issues: 
same-year duplicate official facility codes and noisy heating-value controls.
The checks are sensitivity diagnostics; they do not replace the main specification.

## Duplicate Official Facility Codes

- Official codes with at least one same-year duplicate: 39
- Source rows using those affected codes: 444

| Frame | ID rule | Rows | Facilities | Duplicate facility-year pairs | Duplicate rows | Max rows/pair | Same-year lag events |
|:--|:--|--:|--:|--:|--:|--:|--:|
| Adoption model | Official code | 11,717 | 1,915 | 53 | 110 | 4 | 5 |
| Adoption model | Composite sensitivity | 11,720 | 1,935 | 42 | 84 | 2 | 3 |
| Regression | Official code | 5,683 | 1,016 | 11 | 69 | 22 | - |
| Regression | Composite sensitivity | 5,683 | 1,050 | 3 | 6 | 2 | - |

## Operating-Generator Inclusion Audit

This audit compares operating power-generation rows with official facility codes to operating rows missing those codes. Rows without official facility codes are excluded from the canonical regression frame because they cannot support facility-level clustering or panel comparison.

- Operating-generator rows with official facility codes: 5,753
- Operating-generator rows missing official facility codes: 907
- Additional coded operating rows dropped for complete model covariates: 70
- Canonical regression rows: 5,683

| Group | Rows | Facility proxy | FY range | Mean capacity (t/day) | Median capacity | Mean throughput (t/year) | Mean power (MWh) | Mean bounded efficiency (MWh/t) | Median bounded efficiency | Mean age |
|:--|--:|--:|:--|--:|--:|--:|--:|--:|--:|--:|
| Official facility code present | 5,753 | 1,018 | FY2005-FY2024 | 332.1 | 280.0 | 71,617.9 | 47,156.4 | 0.330 | 0.331 | 15.0 |
| Official facility code missing | 907 | 316 | FY2008-FY2012 | 359.0 | 300.0 | 76,469.4 | 24,868.7 | 0.296 | 0.298 | 13.4 |

**Year-by-year code availability among operating generators**

| Fiscal year | Coded rows | Missing-code rows | Missing-code share (%) |
|--:|--:|--:|--:|
| 2005 | 274 | 0 | 0.0 |
| 2006 | 280 | 0 | 0.0 |
| 2007 | 285 | 0 | 0.0 |
| 2008 | 283 | 4 | 1.4 |
| 2009 | 293 | 4 | 1.3 |
| 2010 | 0 | 295 | 100.0 |
| 2011 | 0 | 300 | 100.0 |
| 2012 | 0 | 304 | 100.0 |
| 2013 | 306 | 0 | 0.0 |
| 2014 | 314 | 0 | 0.0 |
| 2015 | 328 | 0 | 0.0 |
| 2016 | 345 | 0 | 0.0 |
| 2017 | 354 | 0 | 0.0 |
| 2018 | 361 | 0 | 0.0 |
| 2019 | 370 | 0 | 0.0 |
| 2020 | 375 | 0 | 0.0 |
| 2021 | 384 | 0 | 0.0 |
| 2022 | 394 | 0 | 0.0 |
| 2023 | 399 | 0 | 0.0 |
| 2024 | 408 | 0 | 0.0 |

## Composite-ID Adoption Sensitivity

The composite sensitivity appends facility name to official codes that repeat within at least one fiscal year. Residual duplicates remain when the source reports multiple lines under the same code and name.

| Variable | Official AME (pp) | Official SE | Composite AME (pp) | Composite SE |
|:--|--:|--:|--:|--:|
| Prior-year age 10-20 yrs | -1.76 | 0.28 | -1.78 | 0.28 |
| Prior-year age 20-30 yrs | -1.72 | 0.42 | -1.76 | 0.42 |
| Prior-year age 30+ yrs | -1.13 | 0.39 | -1.15 | 0.39 |
| Prior-year capacity per 100 t/day | 0.50 | 0.20 | 0.50 | 0.19 |

| ID rule | Observations | Facilities | Events | Pseudo-R2 |
|:--|--:|--:|--:|--:|
| Official code | 11,717 | 1,915 | 140 | 0.1842 |
| Composite sensitivity | 11,720 | 1,935 | 138 | 0.1847 |

## Composite-ID Efficiency Sensitivity

| Specification | Variable | Official coef. | Composite coef. |
|:--|:--|--:|--:|
| Pooled OLS | Facility age | -0.0279*** | -0.0279*** |
| Pooled OLS | Capacity (100 t/day) | 0.0874*** | 0.0874*** |
| Pooled OLS | Capacity utilization | 0.7468*** | 0.7468*** |
| Year FE | Facility age | -0.0348*** | -0.0348*** |
| Year FE | Capacity (100 t/day) | 0.1030*** | 0.1030*** |
| Year FE | Capacity utilization | 0.7789*** | 0.7789*** |

## Heating-Value Plausibility Sensitivity

- Heating-value rows <= 0 in the canonical regression frame: 512
- Heating-value rows > 30 MJ/kg in the canonical regression frame: 17
- Heating-value rows outside 3-25 MJ/kg: 569

| Sample | N | Facilities | Pooled age | Pooled capacity | Pooled utilization | Year-FE age | Year-FE capacity | Year-FE utilization |
|:--|--:|--:|--:|--:|--:|--:|--:|--:|
| Main frame | 5,683 | 1,016 | -0.0279 | 0.0874 | 0.7468 | -0.0348 | 0.1030 | 0.7789 |
| HV > 0 and <= 30 MJ/kg | 5,154 | 960 | -0.0281 | 0.0876 | 0.7575 | -0.0351 | 0.1043 | 0.7932 |
| HV 3-25 MJ/kg | 5,114 | 958 | -0.0282 | 0.0857 | 0.7601 | -0.0349 | 0.1029 | 0.7937 |

## Interpretation

The duplicate-code issue is a real data-structure concern and should be disclosed or appendix-tested. The sensitivity checks do not overturn the headline claims: adoption remains selective toward younger and larger facilities, while efficiency remains lower with age and higher with scale and utilization. Heating-value noise is likewise not driving the core age, scale, and utilization patterns because those coefficients are stable after plausible-value restrictions.
