<!--
  SUPERSEDED: This Markdown file is an earlier authoring draft.
  The authoritative version of every chapter now lives in thesis/thesis.tex,
  which has been through multiple rounds of panel review, factual correction, and discussion-section additions
  since this Markdown was last touched. Do NOT regenerate thesis.tex from
  these MD files without first back-porting all corrections.
-->

# Chapter 3: Methodology

## 3.1 Overview

This chapter describes the data, variable construction, sample selection, and estimation strategy used to answer the research question. The analysis is fundamentally an exercise in explaining cross-facility variation in energy recovery efficiency using observable facility characteristics. The methodological challenge is to do so in a way that is robust to the specific structure of the data — a long panel with strong between-facility variation and weak within-facility variation — and that produces estimates with clear policy relevance.

The chapter proceeds as follows. Section 3.2 describes the data source and its structure. Section 3.3 explains the cleaning and panel construction steps. Section 3.4 defines the dependent and independent variables. Section 3.5 describes the estimation strategy and the rationale for model selection. Section 3.6 details the robustness checks.

## 3.2 Data Source

### 3.2.1 The General Waste Treatment Survey

The primary data source is the Ministry of the Environment (MOE) General Waste Treatment Survey (*Ippan Haikibutsu Shori Jittai Chosa*), an annual administrative survey covering all operating general waste treatment facilities in Japan. The survey collects facility-level data on waste input volumes, treatment method, facility capacity, operational status, and — for energy-recovering facilities — electricity generation and fuel consumption. The survey has been conducted annually since the 1960s in various forms; the analysis in this thesis uses the fiscal year (FY) 2005 through FY2024 editions, covering 20 years of fleet evolution [@MOEJ2022].

The survey is conducted by prefectural governments, which collect data from individual municipalities, which in turn collect from individual facilities. This administrative chain means the data are subject to reporting conventions that vary somewhat across prefectures and years. The cleaning process described in Section 3.3 addresses the most significant of these inconsistencies.

The appeal of the General Waste Treatment Survey for this research is threefold. First, it is near-census in coverage: because facility operation requires permits under the Waste Disposal Law and because municipal expenditure on waste management is reported to the national government, there is strong incentive for accurate and complete reporting. Second, it contains the specific variables needed for this analysis — waste volume, facility capacity, electricity generation, and facility age — at the facility level over multiple years. Third, it is publicly available, making the analysis replicable by other researchers and policy analysts.

### 3.2.2 Panel Structure

The raw dataset, after merging annual survey files for FY2005–FY2024, contains observations at the facility-year level. Not all facilities appear in all years, both because of entries (new facilities beginning operation) and exits (facility closures). This creates an unbalanced panel — a structure in which different facilities contribute different numbers of years of data.

The full panel (before sample restriction to power-generating facilities) contains 23,599 facility-year observations across 2,949 unique facilities. The average facility contributes 8.0 years of data, though this varies substantially: some facilities appear in all 20 years, while others appear for only one or two years, typically corresponding to opening or closure years in which full-year data are not available.

## 3.3 Data Cleaning and Panel Construction

### 3.3.1 Facility Identification and Linking

The most significant data quality challenge in working with the General Waste Treatment Survey is facility identification across years. Facilities are not consistently identified by a permanent numeric code across all years of the survey; instead, identification requires matching on facility name, municipality, and treatment type. This matching process was performed using a combination of exact string matching and fuzzy matching for facilities with minor name variations (e.g., transliteration differences or administrative reorganizations following municipal mergers).

Municipal mergers (*heisei no daigappei*, the wave of municipal consolidations that reduced Japan's municipality count from approximately 3,200 to 1,700 between 1999 and 2010 [@Rausch2006]) create particular challenges because facilities may be reported under different administrative units before and after merger without any change in physical characteristics. These cases were identified and corrected manually where possible.

### 3.3.2 Variable Cleaning and Outlier Treatment

Several variables required cleaning before analysis. Waste input volume and electricity generation are reported in absolute units (tonnes and kWh, respectively) that must be combined to compute efficiency. Observations with zero waste input but positive electricity generation, or positive waste input but reported capacity of zero, were flagged as likely reporting errors and excluded.

The efficiency variable (electricity generation divided by waste input, in MWh per tonne) was winsorized at the 1st and 99th percentiles to reduce the influence of extreme values, which may reflect reporting errors or genuinely anomalous operating conditions (e.g., a facility operating for only a few days in a fiscal year). For the primary regression sample — power-generating facilities with positive electricity output — the winsorizing bounds were set at [0.01, 0.80] MWh/t, yielding a final regression sample of 6,575 facility-year observations.

The choice of 0.80 MWh/t as the upper winsorizing bound reflects the physical limits of WtE electricity generation: the theoretical maximum conversion efficiency of a stoker furnace system, at realistic waste heating values, is approximately 0.9–1.0 MWh/t, and values above 0.80 almost certainly reflect reporting inconsistencies rather than genuine performance. The lower bound of 0.01 MWh/t captures minimal but real power generation, excluding only observations that are effectively zero.

### 3.3.3 Heating Value Estimation

Waste heating value is not directly reported in the General Waste Treatment Survey. For some years and facilities, it can be estimated from supplementary survey data on waste composition; for others, it must be inferred from national or regional composition averages. Given the known limitations of this approach — the indirect measurement introduces substantial noise — heating value should be treated as an approximate control variable rather than a precisely measured independent variable. The finding that heating value is statistically insignificant in all model specifications may partly reflect this measurement noise, though the thermodynamic arguments for insignificance (Section 2.4.4) suggest genuine ambiguity.

## 3.4 Variable Definitions

### 3.4.1 Dependent Variable

The dependent variable is the natural logarithm of energy recovery efficiency, defined as:

$$\text{log\_efficiency}_{it} = \ln\left(\frac{\text{Electricity generated}_{it} \text{ (MWh)}}{\text{Waste processed}_{it} \text{ (tonnes)}}\right)$$

The log transformation serves two purposes. First, it addresses the right-skewed distribution of raw efficiency values — a small number of high-performing facilities pull the distribution rightward, and the log transformation produces a more symmetric distribution better suited to linear regression. Second, it yields coefficients interpretable as approximate proportional effects: a coefficient of −0.028 on facility age means that each additional year of age is associated with approximately a 2.8% lower efficiency level. Robustness checks using the raw (untransformed) dependent variable are reported in Section 4.5.

### 3.4.2 Independent Variables

**Facility age** is measured as the number of years since the facility began operation as of the observation year. This is derived from the facility's reported start date and the fiscal year of each observation. Age is the primary variable of interest, motivated by the lock-in hypothesis that efficiency is determined by design vintage.

**Design capacity** is measured in tonnes per day (t/day) as reported in the survey. This reflects the facility's rated processing capacity, not its actual throughput. To facilitate interpretation, capacity is included in units of 100 t/day, so that the regression coefficient represents the efficiency gain associated with 100 additional t/day of design capacity.

**Capacity utilization** is defined as the ratio of actual annual waste input to theoretical maximum annual input (design capacity × 365 days), expressed as a proportion. This variable captures how intensively a facility is operated relative to its design specification. It is bounded between 0 and 1 in theory, though values slightly above 1.0 are possible when facilities accept emergency waste transfers beyond design capacity; such observations were capped at 1.0 in the analysis.

**Waste heating value** is the estimated lower heating value of the waste stream processed, measured in MJ/kg. As noted above, this variable is estimated rather than directly measured and should be treated with appropriate caution.

**Grid emission factor** captures the carbon intensity of the regional electricity grid, measured in kg-CO₂/kWh. This variable varies across Japan's nine major regional electricity utility service areas and changes over time, particularly following the Fukushima-induced nuclear shutdowns and subsequent restructuring. It enters the model as a proxy for the value of waste-derived electricity generation in carbon terms and for regional energy market conditions.

### 3.4.3 Summary Statistics

**Table 3.1: Summary Statistics — Power-Generating Subsample (n = 6,575)**

| Variable | Mean | SD | Min | Median | Max |
|---|---|---|---|---|---|
| Efficiency (MWh/t) | 0.298 | 0.118 | 0.010 | 0.284 | 0.800 |
| log(efficiency) | −1.288 | 0.426 | −4.605 | −1.258 | −0.223 |
| Facility age (years) | 16.4 | 10.2 | 0 | 16 | 45 |
| Design capacity (t/day) | 287.4 | 193.6 | 20 | 240 | 1,200 |
| Capacity utilization | 0.742 | 0.158 | 0.02 | 0.762 | 1.00 |
| Heating value (MJ/kg) | 9.8 | 1.6 | 5.2 | 9.7 | 15.4 |
| Grid emission factor (kg-CO₂/kWh) | 0.511 | 0.087 | 0.311 | 0.505 | 0.743 |

The mean efficiency of 0.298 MWh/t in the power-generating subsample is notably higher than the fleet-wide average (which would be lower still if non-generating facilities were assigned zero efficiency). The standard deviation of 0.118 MWh/t reflects substantial dispersion — the interquartile range runs roughly from 0.21 to 0.38 MWh/t — confirming that heterogeneity in performance is large enough to motivate systematic analysis.

## 3.5 Estimation Strategy

### 3.5.1 The Panel Regression Framework

The baseline estimating equation is:

$$\ln(\text{efficiency}_{it}) = \alpha + \beta_1 \text{Age}_{it} + \beta_2 \text{Capacity}_{it} + \beta_3 \text{Utilization}_{it} + \beta_4 \text{HeatingValue}_{it} + \beta_5 \text{GridEF}_{it} + \gamma_t + \epsilon_{it}$$

where *i* indexes facilities, *t* indexes fiscal years, γ_t is a year fixed effect capturing common shocks (e.g., the Fukushima event, changes in the feed-in tariff), and ε_it is the idiosyncratic error term. The key parameters of interest are β₁ through β₃, corresponding to age, scale, and utilization.

### 3.5.2 Model Specifications

Four main specifications are estimated:

**Model 1 (Pooled OLS):** No facility or year fixed effects. Identifies the relationships between facility characteristics and efficiency from variation across all facility-year observations. Standard errors are clustered by facility to account for serial correlation within facilities.

**Model 2 (Year Fixed Effects):** Includes year dummy variables to control for time-varying common factors. This absorbs the Fukushima shock, changes in feed-in tariff rates, and other year-specific influences on efficiency. Standard errors remain clustered by facility.

**Model 3 (Random Effects):** Assumes facility-specific unobservables are uncorrelated with the regressors (the Gauss-Markov assumption extended to panel data). Random effects estimation is more efficient than pooled OLS when the assumption holds, because it uses both within- and between-facility variation.

**Model 4 (Year Fixed Effects + Random Effects):** The most complete specification, combining time controls with random facility effects.

### 3.5.3 Why Not Facility Fixed Effects?

The natural candidate for a panel regression with repeated observations on the same facilities is the facility fixed-effects (FE) estimator, which controls for all time-invariant facility characteristics by differencing out the facility mean. However, facility fixed effects are inappropriate in this context for a specific reason: the primary variable of interest — facility age — increases deterministically by one unit per year for every facility. In a fixed-effects model, the age coefficient is identified entirely from within-facility deviations of age from its facility-specific mean, which for a variable that increases by 1 per year is equivalent to estimating the coefficient from a linear trend. This is nearly collinear with year fixed effects and produces imprecise estimates.

More fundamentally, the ratio of within-to-total variance for log(efficiency) in the winsorized sample is approximately 0.11 — meaning that roughly 89% of the variation in efficiency is *between* facilities rather than *within* facilities over time (this ratio is stable across pre-Fukushima [0.10] and post-Fukushima [0.10] subsamples). This is a substantively important finding in itself: facilities do not meaningfully improve or decline in efficiency over their operational lives. It also means that facility fixed effects would discard the large majority of the variation in the dependent variable, yielding imprecise estimates. The random effects estimator, which exploits between-facility variation while modeling within-facility observations as correlated draws from a facility-specific distribution, is the appropriate panel estimator in this setting.

The methodological pivot from facility FE to pooled OLS and RE rests on two distinct justifications. First, the collinearity problem: facility age increases deterministically by one unit per year, making it nearly collinear with year fixed effects in a two-way FE specification. Second, the variance problem: the within-to-total variation ratio of approximately 0.11 means that facility FE discards roughly 89% of the variation in the dependent variable, yielding a within-R² of only 0.117 even after demeaning. These are separate problems — the first is an identification issue, the second is a power issue — but both point in the same direction: facility FE is inappropriate as the primary estimator. A formal Hausman test comparing RE and FE (excluding facility age from both for comparability) did not reject the RE specification, confirming that between-facility variation — which is the substantive object of inquiry — can be exploited without bias.

### 3.5.4 Inference

All standard errors are clustered at the facility level to account for the correlation of errors across years within the same facility. Clustering is the appropriate response to the likely autocorrelation of facility-level unobservables across years: a facility with unobserved characteristics that raise efficiency in year t is likely to exhibit the same advantage in year t+1, and conventional standard errors that assume independence would understate the true sampling uncertainty.

Statistical significance is assessed at the 1%, 5%, and 10% levels, but given the large sample size (6,575 observations), the practical emphasis is on the magnitude and consistency of estimated coefficients rather than on p-values alone. Coefficients that are statistically significant in all eight specifications (Section 3.6) with consistent signs and magnitudes are treated as robust findings; coefficients with unstable signs or magnitudes are highlighted as unreliable even when individually significant.

## 3.6 Robustness Design

The robustness strategy addresses four potential concerns about the primary estimates.

**Pre/post-Fukushima split.** The 2011 Fukushima disaster represents a major exogenous shock to Japan's energy system. If the determinants of efficiency changed meaningfully between the pre-Fukushima (FY2005–FY2011) and post-Fukushima (FY2012–FY2024) periods — for example, because the increased value of electricity generation changed operational incentives — then pooling the full period could be misleading. To check this, Models 1 and 2 are estimated separately on pre- and post-Fukushima subsamples, yielding four additional specifications (Robustness Specifications R1–R4).

**Capacity tercile analysis.** If the relationships between efficiency and its predictors are nonlinear — for example, if scale effects are concentrated in the transition from small to medium facilities but absent at large scale — then linear specifications may misrepresent the underlying relationships. To explore this, Models 1 and 2 are estimated separately for facilities in the bottom, middle, and top terciles of the capacity distribution (Robustness Specifications R5–R6, reported as tercile-specific coefficient estimates).

**Raw dependent variable.** The log transformation of the dependent variable is standard but involves an assumption that the underlying relationship is multiplicative rather than additive. Robustness Specifications R7–R8 replicate Models 1 and 2 with the raw (untransformed) efficiency as the dependent variable, allowing assessment of whether the log transformation materially affects the substantive conclusions.

**Heating value exclusion.** Because heating value is estimated rather than directly measured and may introduce noise, Robustness Specification R8 also drops the heating value variable to assess whether its inclusion affects the estimates of the primary regressors.

The eight specifications collectively constitute a systematic assessment of the sensitivity of the main findings. The age, capacity, and utilization coefficients are consistently signed and statistically significant across all eight specifications (see Section 4.5); the heating value and grid emission factor coefficients are not.
