# Chapter 4: Results

## 4.1 Overview

This chapter presents the empirical findings in three sections. Section 4.2 documents the descriptive evolution of Japan's incineration fleet from FY2005 to FY2024, establishing the fleet trends that form the backdrop for the regression analysis. Section 4.3 presents the regression results for the primary model specifications, with discussion of each coefficient. Section 4.4 presents the avoided emissions calculation. Section 4.5 summarizes the robustness checks. All regression tables report cluster-robust standard errors.

## 4.2 Fleet Evolution: Descriptive Findings

### 4.2.1 Consolidation and Modernization

Japan's incineration fleet has undergone substantial structural change over the two decades covered by this analysis. Two trends dominate: consolidation (reduction in total facility count) and modernization (increase in the share of facilities generating electricity).

**Table 4.1: Japan's Incineration Fleet, Selected Years FY2005–FY2024**

| Fiscal Year | Total Facilities | Power-Generating | % Power-Gen | Fleet Avg Efficiency (MWh/t, power-gen only) |
|---|---|---|---|---|
| 2005 | 1,318 | 285 | 21.6% | 0.243 |
| 2008 | 1,261 | 312 | 24.7% | 0.255 |
| 2011 | 1,199 | 358 | 29.9% | 0.267 |
| 2014 | 1,127 | 392 | 34.8% | 0.278 |
| 2017 | 1,080 | 402 | 37.2% | 0.285 |
| 2020 | 1,046 | 412 | 39.4% | 0.291 |
| 2024 | 1,014 | 416 | 41.1% | 0.298 |

Total facility count declined from 1,318 in FY2005 to 1,014 in FY2024, a reduction of 304 facilities (23.1%) over 20 years. This rate of consolidation — roughly 15 facilities per year — is driven primarily by the closure of small, ageing, non-generating facilities in rural municipalities, where demographic decline has reduced waste volumes below the threshold required to justify facility maintenance and renewal.

The power-generating share increased from 21.6% to 41.1% over the same period. This represents near-doubling of the penetration rate and reflects both the addition of new power-generating facilities and the selective retirement of non-generating ones. However, the absolute number of power-generating facilities has grown only from 285 to 416 — an increase of 131 facilities over two decades — while the non-generating segment has contracted from 1,033 to 598. The persistence of 598 non-power-generating facilities in FY2024, representing 59% of the active fleet, is a central empirical observation. These facilities burn waste without recovering its energy value, representing a substantial opportunity cost in terms of both electricity generation and avoided carbon emissions.

### 4.2.2 Efficiency Distribution by Age Cohort

The efficiency gradient across facility age cohorts is striking and forms the central empirical pattern of the analysis.

**Table 4.2: Mean Energy Recovery Efficiency by Facility Age Cohort**

| Age Cohort | n (facility-years) | Mean Efficiency (MWh/t) | SD | 25th Percentile | 75th Percentile |
|---|---|---|---|---|---|
| 0–10 years | 1,421 | 0.397 | 0.112 | 0.318 | 0.468 |
| 11–20 years | 2,083 | 0.328 | 0.108 | 0.251 | 0.398 |
| 21–30 years | 1,876 | 0.264 | 0.098 | 0.192 | 0.330 |
| 31+ years | 1,195 | 0.179 | 0.081 | 0.121 | 0.231 |

The efficiency decline across age cohorts is monotonic and substantial. Facilities aged 0–10 years achieve a mean efficiency of 0.397 MWh/t — more than twice the 0.179 MWh/t average of facilities over 30 years old. The interquartile ranges show that the distributions are partially overlapping but clearly shifted: the 25th percentile of the youngest cohort (0.318 MWh/t) exceeds the 75th percentile of the oldest cohort (0.231 MWh/t). This non-overlap in the tails reinforces the conclusion that age cohort is a strong determinant of efficiency — not merely a statistical association but a substantive distributional shift.

The standard deviation within cohorts is notable: even among the youngest facilities (0–10 years), the SD is 0.112 MWh/t, indicating substantial heterogeneity that cannot be explained by age alone. This within-cohort variation is accounted for in the regression by the capacity and utilization variables.

### 4.2.3 Efficiency Distribution by Capacity Category

**Table 4.3: Mean Energy Recovery Efficiency by Facility Capacity Category**

| Capacity (t/day) | n (facility-years) | Mean Efficiency (MWh/t) | % of Fleet (FY2024 active) |
|---|---|---|---|
| < 100 | 834 | 0.198 | 18% |
| 100–299 | 2,614 | 0.271 | 41% |
| 300–499 | 1,847 | 0.321 | 27% |
| ≥ 500 | 1,280 | 0.378 | 14% |

Scale effects are similarly strong. Facilities with design capacity below 100 t/day achieve mean efficiency of 0.198 MWh/t, compared to 0.378 MWh/t for those at or above 500 t/day — a factor of 1.9. The largest capacity category represents only 14% of active facilities but, given its size advantage, contributes disproportionately to aggregate electricity generation from the fleet.

### 4.2.4 Within-Facility Efficiency Dynamics

A crucial descriptive finding — one that motivates the choice of random effects over facility fixed effects and that directly speaks to the lock-in hypothesis — is the near-complete absence of within-facility efficiency change over time.

The ratio of within-facility variance to total variance for log(efficiency) in the winsorized sample is approximately 0.11. This means that roughly 89% of all variation in efficiency in the dataset is *between* facilities (explained by differences in age, scale, design, and operating conditions at construction) and only about 11% is *within* facilities over time. This ratio is stable across subsamples: 0.10 in the pre-Fukushima period (FY2005-2010) and 0.10 in the post-Fukushima period (FY2014-2024). In practical terms, if you know a facility's efficiency in one year, you can predict its efficiency in subsequent years with high accuracy — it will not meaningfully improve or decline.

This is the empirical signature of lock-in. Facility performance is determined at the point of construction and embedded in the physical design of the boiler, turbine, and control systems. Operational management can optimize around this fixed performance ceiling, but cannot transcend it.

## 4.3 Regression Results: Efficiency Determinants

### 4.3.1 Main Specifications

**Table 4.4: Regression Results — Determinants of log(Efficiency) Among Power-Generating Incinerators**

| Variable | Model 1 (Pooled OLS) | Model 2 (Year FE) | Model 3 (RE) | Model 4 (Year FE + RE) |
|---|---|---|---|---|
| Facility age (years) | −0.039*** | −0.038*** | −0.043*** | −0.042*** |
| | (0.003) | (0.003) | (0.002) | (0.002) |
| Capacity (per 100 t/day) | +0.089*** | +0.091*** | +0.097*** | +0.098*** |
| | (0.011) | (0.011) | (0.009) | (0.009) |
| Capacity utilization | +0.613*** | +0.621*** | +0.583*** | +0.591*** |
| | (0.071) | (0.072) | (0.063) | (0.064) |
| Heating value (MJ/kg) | −0.008 | −0.006 | −0.011 | −0.009 |
| | (0.012) | (0.013) | (0.010) | (0.011) |
| Grid emission factor | +0.142 | −0.218* | +0.089 | −0.194 |
| | (0.098) | (0.112) | (0.091) | (0.107) |
| Year FE | No | Yes | No | Yes |
| Random Effects | No | No | Yes | Yes |
| Observations | 6,575 | 6,575 | 6,575 | 6,575 |
| Facilities | 947 | 947 | 947 | 947 |
| R² (within) | 0.186 | 0.203 | — | — |
| R² (between) | 0.574 | 0.561 | — | — |
| R² (overall) | 0.412 | 0.419 | 0.408 | 0.416 |

*Note: Cluster-robust standard errors in parentheses, clustered at facility level. *** p < 0.001, ** p < 0.01, * p < 0.05. Constant included but not reported.*

### 4.3.2 Facility Age

Facility age is the most consistent and substantively important predictor of energy recovery efficiency. Across the four main specifications, the coefficient on age ranges from −0.038 to −0.043 and is statistically significant at the 0.1% level in all cases. The estimates are stable across model specifications — the range of 0.005 log-units across specifications — confirming that the age effect is not an artifact of particular modeling choices.

The economic and engineering interpretation of a coefficient of −0.040 (taking the approximate midpoint) is that each additional year of facility age is associated with approximately 4.0% lower efficiency, holding capacity, utilization, and other covariates constant. Over the range from a new facility (age = 0) to a 30-year-old facility (age = 30), this implies a total efficiency reduction of approximately 70% on the log scale, or a reduction to about 50% of original efficiency in proportional terms. This estimate from the regression is consistent with but slightly larger than the raw cohort differences in Table 4.2, because the regression controls for capacity differences across cohorts — newer facilities tend also to be larger, so the raw cohort comparison confounds age and scale effects.

The age effect captures primarily the vintage of engineering design rather than physical degradation. This interpretation is supported by the near-zero within-facility variation: if the age coefficient reflected degradation, we would expect to see efficiency declining within individual facilities over time. The data show no such pattern. Instead, the coefficient reflects the fact that facilities built in the 1980s embody 1980s technology, while facilities built in the 2010s embody 2010s technology — a vintage effect that cannot be changed through operational intervention.

### 4.3.3 Design Capacity

Design capacity exerts a strong positive effect on efficiency. The coefficient per 100 t/day of design capacity ranges from +0.089 to +0.098 across the four main specifications, all significant at the 0.1% level. A facility with 300 t/day of design capacity is predicted to have approximately 18–20% higher efficiency than an otherwise comparable facility with 100 t/day, holding age and utilization constant.

This scale effect reflects the engineering economics of boiler and turbine design discussed in Section 2.4.1. At larger scale, fixed costs of higher-pressure boiler systems are amortized over more tonnes processed, and the minimum efficient scale of turbine-generator sets becomes achievable. The coefficient magnitude suggests that scale effects are strong throughout the observed capacity range — there is no indication of diminishing returns within the distribution of Japanese facilities.

The policy implication is direct: consolidating waste flows from multiple small facilities into fewer large ones would improve system-level efficiency, holding the age distribution constant. The challenge, as discussed in Chapter 5, is that this consolidation requires inter-municipal coordination that the current governance structure makes difficult.

### 4.3.4 Capacity Utilization

Capacity utilization is a consistently strong positive predictor of efficiency. Coefficients range from +0.583 to +0.621, significant at the 0.1% level in all four specifications. Moving from 60% utilization to 80% utilization — a 20 percentage point increase — is associated with approximately 12% higher efficiency. Moving from 50% to 90% utilization is associated with approximately 25% higher efficiency.

This finding reflects thermodynamic realities: facilities operating near their design capacity maintain more stable combustion conditions and steam parameters, maximizing electricity output per tonne of waste. At low utilization rates, facilities may operate in partial-load regimes that reduce boiler efficiency, or may shut down boiler systems entirely during low-input periods, reducing effective electricity generation relative to waste processed.

The utilization finding also has an important distributional dimension. High-capacity-utilization facilities are concentrated in urban areas with dense and stable waste streams; rural and suburban facilities serving smaller or declining populations tend toward lower utilization. This means that the efficiency advantage of urban areas is not merely compositional (larger facilities in cities) but also operational (higher utilization of those larger facilities).

### 4.3.5 Heating Value

Heating value is not statistically significant in any of the four main specifications. The point estimates are small and negative (ranging from −0.006 to −0.011), but with standard errors of comparable magnitude, none approaches conventional significance thresholds. This null result is robust across model specifications and is confirmed in all robustness checks.

The insignificance of heating value is theoretically plausible, for reasons discussed in Section 2.4.4: modern combustion control systems buffer the relationship between waste energy content and boiler output, and high-LHV waste may require cooling interventions that reduce net recovery. However, measurement noise — the fact that heating value is estimated from composition surveys rather than direct measurement — cannot be ruled out as a contributing factor. The policy implication is that managing waste composition to increase heating value is unlikely to be an effective strategy for improving incineration efficiency, and monitoring resources allocated to this purpose might be better directed elsewhere.

### 4.3.6 Grid Emission Factor

The grid emission factor coefficient is unstable across specifications in a way that makes it uninterpretable as a causal effect. In Model 1 (pooled OLS without year fixed effects), the coefficient is positive (+0.142) and marginally insignificant; in Model 2 (with year fixed effects), it flips to negative (−0.218) and is significant at the 5% level. This sign reversal suggests that the grid emission factor is not measuring a stable causal relationship but is instead a proxy for other year-varying factors that affect efficiency. When year fixed effects absorb these common trends, the estimated relationship reverses, indicating that the Model 1 coefficient reflects omitted variable bias rather than a genuine effect of grid emission factors on facility efficiency.

This finding is consistent with the conceptual argument that grid emission factors should not, in principle, affect the physical conversion efficiency of waste combustion into electricity. That they appear to in some specifications is an artifact of their correlation with time trends in fleet composition and energy policy.

## 4.4 Avoided Emissions Calculation

### 4.4.1 Method

The avoided CO₂ emissions attributable to waste-to-energy generation are calculated as:

$$\text{Avoided CO}_2 = \text{Electricity generated (MWh)} \times \text{Grid emission factor (t-CO}_2/\text{MWh)}$$

This calculation credits WtE with displacing grid electricity that would otherwise have been generated from the average fuel mix in the regional grid, at the prevailing emission factor. It does not account for the process emissions from waste combustion itself, which involve both biogenic CO₂ (from organic waste) and fossil CO₂ (from plastic, synthetic textiles, and other petroleum-derived materials). The gross avoided emissions calculation presented here is therefore an upper bound on the net climate benefit of waste-to-energy electricity generation.

### 4.4.2 FY2024 Fleet-Level Estimates

In FY2024, Japan's 416 power-generating incineration facilities collectively generated approximately 9.3 billion kWh (9.3 TWh) of electricity from approximately 31 million tonnes of waste processed <!-- VERIFY: citation needed -->. Applying the average regional grid emission factor of 0.49 t-CO₂/MWh yields:

$$\text{Avoided CO}_2 \approx 9,300 \text{ GWh} \times 0.49 \text{ t-CO}_2/\text{MWh} \approx 4.56 \text{ million t-CO}_2$$

Rounding to one significant figure: approximately **4.6 million t-CO₂** in gross avoided emissions in FY2024. This figure represents an upper bound on the net climate benefit, as it does not deduct process CO₂ from waste combustion (both biogenic and fossil fractions). The net benefit depends on the fossil carbon content of the waste stream, which is not available at the facility level in this dataset.

### 4.4.3 Distribution of Avoided Emissions

This aggregate figure conceals extreme concentration. The top 10% of facilities by electricity generation (approximately 42 facilities) account for an estimated 55–60% of total avoided emissions, reflecting the combination of large capacity, high utilization, and recent vintage that characterizes the high-efficiency segment of the fleet. The bottom 50% of power-generating facilities — predominantly small, older installations — collectively contribute approximately 15% of avoided emissions despite representing half the facility count.

This concentration has direct policy implications. Improving the efficiency of the few largest, most modern facilities — or simply preventing their retirement — has a larger climate impact than upgrading dozens of small facilities. Conversely, the closure of the 598 non-power-generating facilities in the fleet would not reduce avoided emissions at all (they generate none), but would reduce process emissions associated with combustion at those sites.

## 4.5 Robustness Checks

**Table 4.5: Robustness Check Summary — Age, Capacity, and Utilization Coefficients**

| Specification | Age Coeff. | Capacity Coeff. | Utilization Coeff. | Age p-value |
|---|---|---|---|---|
| R1: Pre-Fukushima, Pooled OLS | −0.041 | +0.086 | +0.597 | <0.001 |
| R2: Pre-Fukushima, Year FE | −0.040 | +0.088 | +0.605 | <0.001 |
| R3: Post-Fukushima, Pooled OLS | −0.036 | +0.094 | +0.631 | <0.001 |
| R4: Post-Fukushima, Year FE | −0.035 | +0.096 | +0.639 | <0.001 |
| R5: Small capacity tercile | −0.028 | +0.081 | +0.533 | <0.001 |
| R6: Large capacity tercile | −0.037 | +0.080 | +0.829 | <0.001 |
| R7: Raw DV, Pooled OLS | −0.006 | +0.018 | +0.147 | <0.001 |
| R8: Raw DV, Year FE (no HV) | −0.006 | +0.019 | +0.149 | <0.001 |

*Note: R7 and R8 use raw (untransformed) efficiency as DV; coefficients are not comparable in magnitude to log-DV specifications but signs and significance are consistent.*

The age coefficient ranges from −0.028 to −0.043 across the eight robustness specifications, always significant at the 0.1% level. The sign and significance are invariant to the period of analysis (pre/post-Fukushima), the size segment of the fleet, and the choice of dependent variable transformation. Capacity and utilization coefficients are similarly consistent. This consistency across eight distinct specification choices provides strong evidence that these are stable structural relationships in the data, not artifacts of particular modeling decisions.

The pre- versus post-Fukushima comparison (R1–R4) reveals a slight reduction in the age coefficient magnitude in the post-Fukushima period (−0.036 vs. −0.041) and a slight increase in the capacity and utilization coefficients. This is consistent with the hypothesis that the post-Fukushima energy environment — in which grid electricity was scarcer and more valuable — provided stronger incentives for efficient operation, particularly for larger facilities. However, the magnitudes of these changes are modest, suggesting that the core efficiency determinants are not fundamentally altered by energy market conditions.

The capacity tercile analysis (R5–R6) reveals an interesting asymmetry: the utilization coefficient is substantially larger for large-capacity facilities (+0.829) than for small-capacity ones (+0.533). This suggests that the efficiency return to high utilization is greater when a facility has a large, modern boiler system capable of extracting more energy from waste at design operating conditions. For small, older facilities, the efficiency ceiling is lower regardless of utilization.
