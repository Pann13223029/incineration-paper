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
