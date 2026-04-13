# Thesis Architecture — Final Reference

**Title:** Carbon Lock-in or Circular Transition? Heterogeneity in Japan's Waste Incineration Fleet and Net-Zero Compatibility

**Author:** Pann Phetra (Student ID: 13223029)
**Supervisor:** Prof. Han Ji
**Institution:** Ritsumeikan Asia Pacific University, College of Sustainability and Tourism
**Year:** 2026

---

## Executive Summary

Japan operates ~1,000 waste incinerators — the most of any country. The literature treats this fleet as monolithic. It is not. This thesis uses a 20-year facility-level panel (23,599 observations, 2,949 unique facilities, FY2005–FY2024) to document heterogeneity in energy recovery efficiency and identify what drives it. The central empirical finding is that within-facility efficiency is nearly fixed over time (only ~13% of variation is within facilities; 87% is between them), and that this ratio is stable across the pre- and post-Fukushima subsamples despite the large shock to electricity prices and policy incentives. This is strongly consistent with Seto et al.'s (2016) definition of infrastructural lock-in: facility-level performance responds to incentives within a bounded envelope set by the original design. The policy implication is that fleet-wide progress toward net-zero passes through construction and retirement decisions — the points at which design vintage is set — rather than through operational intervention at already-built facilities.

---

## Research Question

**RQ:** What facility characteristics predict energy recovery efficiency among Japan's power-generating incinerators, and how has this changed as the fleet modernizes?

**Sub-questions:**

1. How does facility age relate to energy recovery efficiency (MWh/t)?
2. Does design capacity predict efficiency, controlling for age and utilization?
3. Does capacity utilization predict efficiency independently of facility characteristics?
4. How stable are these relationships across the pre- and post-Fukushima subsamples and across model specifications?

---

## Data Inventory

| Data | Status | Source | Coverage |
|------|:------:|--------|:---------|
| Facility-level panel (23,599 obs × 28 cols) | **HAVE** | MOE General Waste Treatment Survey | FY2005–FY2024 |
| Power generation capacity (kW) | **HAVE** | MOE survey | 98.7% of power-gen subsample |
| Total electricity generated (MWh) | **HAVE** | MOE survey | 98.1% of power-gen subsample |
| Power generation efficiency (derived) | **HAVE** | MWh/t from generation ÷ throughput | 98.7% of subsample |
| Facility age (derived) | **HAVE** | FY − year_started | 99.8% coverage |
| Capacity utilization (derived) | **HAVE** | throughput ÷ (capacity × 365) | 98.3% coverage |
| Heating value of waste (kJ/kg) | **HAVE** | MOE survey (estimated from composition) | 96.2% coverage |
| Regional grid emission factors | **HAVE** | METI + utility publications, interpolated between anchor years | 10 utilities, 100% match rate |
| Facility-level CO₂ emissions | **N/A** | Not in MOE survey; not needed for RQ | — |

---

## Two Populations

The dataset splits into two analytically distinct populations:

| Population | Obs in full panel | % of total | Role in analysis |
|------------|:-----------------:|:----------:|------------------|
| **Power-generating facilities** | ~6,950 | 29.4% | Main regression sample (after winsorising: 6,575 facility-years / 947 facilities) |
| **Non-power-generating facilities** | ~16,649 | 70.6% | Descriptive comparison; represent the carbon lock-in challenge |

The persistence of the non-power-generating segment is itself a finding: 598 of the 1,014 active FY2024 facilities generate no electricity — the "59% problem" discussed in Chapter 5.

---

## Methodology

**Design:** Panel regression with cluster-robust standard errors, four main specifications plus eight robustness specifications.

**Why not facility fixed effects?** The natural candidate for a panel setting is the two-way facility-and-year fixed-effects estimator, but it is inappropriate here for two reasons:

1. **Identification problem.** Facility age increases deterministically by one unit per year, making it nearly collinear with year fixed effects in a two-way FE specification. The age coefficient — the primary variable of interest — is poorly identified within the FE framework.
2. **Variance problem.** The within-to-total variance ratio of log-efficiency is only ~0.13. Facility FE would discard ~87% of the variation in the dependent variable, yielding imprecise estimates. This is itself a substantively important finding: facilities do not meaningfully improve or decline in efficiency over their operational lives.

A Hausman test formally rejects the RE null in favour of FE (χ²≈173, p<0.0001) and is disclosed in §3.5.3, but does not drive the estimator choice: the Hausman test presumes that the FE specification can cleanly recover the parameters of interest, which fails for both reasons above. Pooled OLS and RE are therefore reported as primary; FE is referenced only to document that within-facility variation is negligible.

**Primary estimators:** Pooled OLS (Model 1), Pooled OLS with year fixed effects (Model 2), Random Effects (Model 3), Random Effects with year fixed effects (Model 4). All use cluster-robust standard errors clustered at the facility level, following Wooldridge (2010).

**Panel window:** FY2005–FY2024 (20 years, post-dioxin regulatory stabilisation of Japan's fleet).

**Dependent variable:** log(energy recovery efficiency), where efficiency is MWh electricity generated per tonne of waste processed. Log transformation produces a symmetric distribution and coefficients interpretable as proportional effects.

**Key independent variables:**

- Facility age (years since year_started)
- Design capacity (per 100 t/day)
- Capacity utilization (throughput ÷ capacity × 365, capped at 1.0)
- Heating value of waste input (MJ/kg)
- Regional grid emission factor (kg-CO₂/kWh)

**Robustness design (8 specifications):**

- R1–R4: Models 1 and 2 estimated separately on pre-Fukushima (FY2005–FY2011) and post-Fukushima (FY2012–FY2024) subsamples
- R5–R6: Models estimated on small and large capacity tercile endpoints (middle tercile omitted by construction)
- R7–R8: Raw (untransformed) efficiency as dependent variable, with and without heating value

**What this is NOT:**

- Not a causal identification study (no IV, no regression discontinuity)
- Not a spatial analysis (no GIS, no geocoded analysis)
- Not a carbon accounting exercise at facility level (no process-emission estimation)
- Not a waste composition study
- Not a life-cycle assessment

---

## Chapter Structure (final)

| Ch | Title | Key content |
|----|-------|-------------|
| 1 | Introduction | Incineration paradox, RQ, significance, thesis outline |
| 2 | Literature Review | Japan's WtE institutional context, lock-in theory (Unruh, Arthur), industrial ecology / material metabolism framing, empirical literature on efficiency determinants |
| 3 | Methodology | Data source, panel construction, variable definitions, estimation strategy, why pooled OLS + RE over FE, robustness design |
| 4 | Results | Fleet-evolution descriptives, 4 main regression specifications, avoided emissions calculation, 8 robustness specifications |
| 5 | Discussion | Design-determination finding, lock-in interpretation, scale and consolidation policy, Fukushima effect, net-zero implications, limitations |
| 6 | Conclusion | Summary, theoretical contributions, policy recommendations, future research, closing statement |

---

## Key Empirical Findings

| Finding | Magnitude | Significance |
|---------|-----------|--------------|
| Facility age effect | −0.028 to −0.043 log-units/year | p < 0.001 in all 12 specifications |
| Design capacity effect | +0.08 to +0.10 log-units per 100 t/day | p < 0.001 in all specifications |
| Capacity utilization effect | +0.58 to +0.62 log-units | p < 0.001 in all specifications |
| Heating value effect | −0.01 to +0.01 | Not significant in any specification |
| Grid emission factor effect | Sign-unstable across specifications | Uninterpretable as causal effect |
| Within/total variance ratio | 0.13 pooled / 0.10 pre-Fuku / 0.07 post-Fuku | Consistent across subsamples |
| Mean efficiency by age cohort | 0.397 MWh/t (0–10 yrs) → 0.179 MWh/t (31+ yrs) | Monotonic decline |
| Fleet consolidation (FY2005–FY2024) | 1,318 → 1,014 facilities (−23%) | ~15 closures/year |
| Power-generating share | 21.6% → 41.1% | Nearly doubled |
| FY2024 gross avoided CO₂ | ~4.6 Mt-CO₂ (upper bound) | Excludes process emissions from combustion |

---

## Assets

| Category | Count |
|----------|:-----:|
| Python scripts | 7 (00 probe, 01 download, 02 parse, 03 grid, 04 eda, 05 regression, 06 robustness) |
| Raw data files | 20 (one per fiscal year) |
| Processed panel | 23,599 rows × 28 columns |
| Enriched panel (with grid factors) | 23,599 rows × 28 columns (100% grid-factor match) |
| Regression sample (winsorised power-gen) | 6,575 rows × 947 facilities |
| Figures | 2 (establishing shot + heterogeneity shot) |
| Tables in thesis.tex | 6 (summary stats, fleet evolution, efficiency by age, efficiency by capacity, regression results, robustness) |
| Equations in thesis.tex | 4 (log efficiency, baseline regression, avoided CO₂ formula, avoided CO₂ computation) |
| Bibliography entries | 26 (all DOI/URL-verified, all cited in text, 0 orphans) |
| Expert panel review rounds | 3 (round 1: ~40 items; round 2: 21 items; round 3: 6 items) |

---

## Scope Boundaries

**IN:**

- Panel econometrics (pooled OLS + RE, with year FE as robustness)
- Facility-level heterogeneity analysis
- Energy recovery efficiency (MWh/t) as dependent variable
- Fleet consolidation and modernization descriptive trends
- Descriptive comparison of power-generating vs non-generating facilities
- Grid emission factor as covariate
- Gross avoided emissions calculation for FY2024 cross-section

**OUT:**

- Spatial analysis / GIS / remote sensing
- Causal identification / instrumental variables / natural experiments beyond Fukushima subsample split
- Waste composition modelling (heating value is an estimated control, not the object of study)
- Facility-level CO₂ estimation (process emissions from combustion are acknowledged as a gap, not computed)
- Full life cycle assessment
- International comparison at the empirical level (only narrative comparison in the literature review)

---

## Data Pipeline

```
01_download_facility_data.py     -> 20 Excel files (FY2005-FY2024)
02_parse_facility_panel.py       -> incineration_panel.csv (23,599 rows)
03_grid_emission_factors.py      -> incineration_panel_enriched.csv + grid_emission_factors.csv
04_eda_facility.py               -> figures + EDA report
05_panel_regression.py           -> 4 main regression specifications
06_robustness.py                 -> 8 robustness specifications
```

---

## Confidence: HIGH

Data is strong (near-census administrative panel, 20 years). RQ is estimable and has been answered with coefficients that are stable across 12 distinct specifications. Methodology pivot from FE to pooled OLS + RE is substantively justified (collinearity of age with year FE; variance-ratio power problem) rather than ad hoc, and the Hausman rejection is disclosed openly. All 26 references verified against Crossref or publisher catalogs; 0 fabricated citations remain. Three rounds of expert-panel review have cleared all HIGH, MEDIUM, LOW, and NITS items flagged; round 3 in particular softened "lock-in proven" language to "strongly consistent with lock-in," reframed the Fukushima subsample result as bounded (rather than absent) responsiveness, and unified the retrofit framing across §5.2 and §5.5.1 from "cannot be converted" to "unlikely under foreseeable economics."

---

*Last updated: 2026-04-13. Reflects thesis.tex state at commit 1ae13f7.*
