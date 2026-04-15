# Thesis Architecture — Final Reference

**Title:** Carbon Lock-in or Circular Transition? Heterogeneity in Japan's Waste Incineration Fleet and Net-Zero Compatibility

**Author:** Pann Phetra (Student ID: 13223029)
**Supervisor:** Prof. Han Ji
**Institution:** Ritsumeikan Asia Pacific University, College of Sustainability and Tourism
**Year:** 2026

---

## Executive Summary

Japan operates ~1,000 waste incinerators — the most of any country. The literature treats this fleet as monolithic. It is not. This thesis uses a 20-year facility-level panel (23,599 observations, 2,948 unique facilities, FY2005–FY2024) to separate two linked questions: which coded facilities first observed without generation make an observed transition into power generation, and conditional on power generation, which facility characteristics predict energy recovery efficiency. The canonical analysis pipeline now writes an explicit sample-definition report, adoption results, an event-level pathway audit, and stage manifests so the published outputs are tied to one reproducible empirical design. In the extensive-margin adoption risk set (13,770 facility-years, 2,035 facilities, 141 observed first-adoption events), the lagged model frame contains 11,717 facility-years across 1,915 facilities and 140 events; under the main complementary log-log hazard, facilities older than 10 years in the prior observed year are 2.3–3.2 percentage points less likely to transition into generation, while each additional 100 t/day of prior-year capacity raises transition probability by about 0.39 percentage points. A conservative pathway audit classifies 82 observed transitions as reset/rebuild-like, 38 as continuity/in-place-upgrade-like, 20 as forward-dated or placeholder entries, and 1 as unresolved. In the canonical generator regression frame (5,683 facility-years, 1,016 facilities), the pooled within/total variance ratio of log-efficiency is 0.1499, falling from 0.1795 pre-Fukushima to 0.0956 post-Fukushima. Together these results are strongly consistent with a sector in which capital-side modernization matters more than operating-side fine-tuning, while the adoption data themselves do not collapse that modernization pattern into one identified mechanism such as replacement alone.

---

## Research Question

**RQ:** What predicts observed transition into power generation among coded facilities first seen without it, and conditional on power generation, what predicts energy recovery efficiency among power-generating incinerators?

**Sub-questions:**

1. Which coded facilities first seen without generation later make an observed transition into power generation within the panel window?
2. Does design capacity predict both adoption and conditional efficiency?
3. How does facility age structure the adoption margin and the efficiency margin?
4. How stable are the conditional efficiency relationships across the pre- and post-Fukushima subsamples and across model specifications?

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

## Two Linked Samples

The dataset now uses two linked analytical frames:

| Population | Obs in full panel | % of total | Role in analysis |
|------------|:-----------------:|:----------:|------------------|
| **Coded full-fleet frame** | 19,827 | 84.0% | Extensive-margin transition analysis on all facilities with official codes |
| **Generator operating sample** | 6,660 | 28.2% | Conditional descriptive and regression work for facilities with positive throughput and positive output |

Within the coded full-fleet frame, the observed first-adoption risk set is built on 13,770 facility-years across 2,035 facilities first observed without power generation. Facilities already generating power in their first observed year (913 facilities) are treated as left-censored for the adoption model. The lagged model frame is smaller, 11,717 facility-years across 1,915 facilities, because the first observed at-risk year for each facility is dropped when prior-year predictors are required. The persistence of the non-power-generating segment remains a key descriptive fact: 598 of the 1,014 active FY2024 facilities generate no electricity.

---

## Methodology

**Design:** Two-part empirical architecture.

1. **Extensive margin:** lagged observed first-adoption complementary log-log hazard on coded, initially non-generating facilities, with prior-year age-band indicators, prior-year capacity, year fixed effects, prefecture fixed effects, and facility-clustered standard errors; reported as average marginal effects, with lagged logit and lagged linear probability versions retained as robustness checks.
2. **Intensive margin:** generator-efficiency panel regression with cluster-robust standard errors, four main specifications plus eight robustness specifications.

**Why not facility fixed effects?** The natural candidate for a panel setting is the two-way facility-and-year fixed-effects estimator, but it is inappropriate here for two reasons:

1. **Identification problem.** Facility age increases deterministically by one unit per year, making it nearly collinear with year fixed effects in a two-way FE specification. The age coefficient — the primary variable of interest — is poorly identified within the FE framework.
2. **Variance problem.** The pooled within-to-total variance ratio of log-efficiency in the canonical regression frame is 0.1499, and the post-Fukushima ratio is lower still at 0.0956. Facility FE therefore leans on the smaller part of the signal, even before confronting the age/year identification problem.

A Hausman test formally rejects the RE null in favour of FE (χ²≈173, p<0.0001) and is disclosed in §3.5.3, but does not drive the estimator choice: the Hausman test presumes that the FE specification can cleanly recover the parameters of interest, which fails for both reasons above. Pooled OLS and RE are therefore reported as primary; FE is referenced only to document that within-facility variation is negligible.

**Primary estimators:** Complementary log-log adoption hazard (extensive margin), plus Pooled OLS (Model 1), Pooled OLS with year fixed effects (Model 2), Random Effects (Model 3), and Random Effects with year fixed effects (Model 4) for the generator sample. All use facility-clustered standard errors, and the shared analysis frames are built once in `code/scripts/panel_utils.py`.

**Panel window:** FY2005–FY2024 (20 years, post-dioxin regulatory stabilisation of Japan's fleet).

**Dependent variables:**

- Extensive margin: `adopt_power_this_year`, the observed first adoption of power generation among coded facilities first seen without it
- Intensive margin: log(energy recovery efficiency), where efficiency is MWh electricity generated per tonne of waste processed among generators

**Key independent variables:**

- Facility age (years since year_started, floored at zero for one-year commissioning mismatches)
- Design capacity (per 100 t/day)
- Capacity utilization (throughput ÷ capacity × 365, capped at 1.0 at analysis time)
- Heating value of waste input (MJ/kg)
- Regional grid emission factor (kg-CO₂/kWh)

**Robustness design (8 specifications):**

- R1–R4: Models 1 and 2 estimated separately on pre-Fukushima (FY2005–FY2011) and post-Fukushima (FY2012–FY2024) subsamples
- R5–R6: Models estimated on small and large capacity tercile endpoints (middle tercile omitted by construction)
- R7–R8: Raw (untransformed) winsorized efficiency as dependent variable, in pooled OLS and year-FE variants

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
| 3 | Methodology | Data source, panel construction, two-part variable design, adoption hazard, why pooled OLS + RE over FE for the generator sample, robustness design |
| 4 | Results | Fleet-evolution descriptives, adoption hazard, 4 main generator-efficiency specifications, avoided emissions calculation, 8 robustness specifications |
| 5 | Discussion | Extensive-margin modernization, bounded responsiveness in the generator sample, scale and consolidation policy, Fukushima effect, net-zero implications, limitations |
| 6 | Conclusion | Summary, theoretical contributions, policy recommendations, future research, closing statement |

---

## Key Empirical Findings

| Finding | Magnitude | Significance |
|---------|-----------|--------------|
| Adoption hazard, prior-year age bands | Facilities older than 10 years are 1.5–2.2 pp less likely than 0–10-year facilities to record transition in the next observed year | p < 0.05 in every reported age-band coefficient |
| Adoption hazard, prior-year capacity | +1.47 pp per 100 t/day | p < 0.001 |
| Facility age effect | −0.019 to −0.035 in the four main specifications; −0.025 to −0.043 across robustness | p < 0.001 in every reported specification |
| Design capacity effect | +0.041 to +0.103 in the four main specifications | Positive in every main specification |
| Capacity utilization effect | +0.541 to +0.779 in the four main specifications | Positive in every main specification |
| Heating value effect | Approximately zero in the canonical main models | Not significant in any of the four main specifications |
| Grid emission factor effect | Sign-unstable across specifications | Uninterpretable as causal effect |
| Within/total variance ratio | 0.1499 pooled / 0.1795 pre-Fuku / 0.0956 post-Fuku | Between-facility variation still dominates |
| Mean efficiency by age cohort | 0.400 MWh/t (0–10 yrs) → 0.183 MWh/t (30+ yrs) | Monotonic decline in the canonical regression frame |
| Fleet consolidation (FY2005–FY2024) | 1,318 → 1,014 facilities (−23%) | ~15 closures/year |
| Power-generating share | 21.6% → 41.1% | Nearly doubled |
| FY2024 gross avoided CO₂ | ~4.6 Mt-CO₂ (upper bound) | Excludes process emissions from combustion |

---

## Assets

| Category | Count |
|----------|:-----:|
| Python scripts | 10 (00 probe, 01 download, 02 parse, 03 grid, 04 eda, 05a adoption, 05 regression, 06 robustness, 07 rebuild, shared panel utils) |
| Raw data files | 20 (one per fiscal year) |
| Processed panel | 23,599 rows × 28 columns |
| Enriched panel (with grid factors) | 23,599 rows × 28 columns (100% grid-factor match) |
| Regression sample (canonical frame) | 5,683 rows × 1,016 facilities |
| Figures | 2 (establishing shot + heterogeneity shot) |
| Tables in thesis.tex | 7 (fleet evolution, adoption hazard, efficiency by age, efficiency by capacity, regression results, avoided-emissions calculation, robustness) |
| Equations in thesis.tex | 4 (log efficiency, baseline regression, avoided CO₂ formula, avoided CO₂ computation) |
| Bibliography entries | 26 (all DOI/URL-verified, all cited in text, 0 orphans) |
| Expert panel review rounds | 3 hostile-attack rounds (r1: ~40 items; r2: ~21 items; r3: ~6 items) + 1 holistic grade/direction round + 1 A-push execution round |
| Thesis body word count | ~13,600 words (text + equations + tables + bibliography) |

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
04_eda_facility.py               -> figures + EDA report + pre_regression_decision.md
05a_power_adoption.py            -> adoption_results.md + extensive-margin manifest
05_panel_regression.py           -> sample_definition.md + 4 main regression specifications
06_robustness.py                 -> 8 robustness specifications
07_rebuild_analysis.py           -> one-command local rebuild from checked-in raw data
```

---

## Confidence: HIGH

Data is strong (near-census administrative panel, 20 years). RQ is estimable and has been answered with coefficients that are stable across 12 distinct specifications. Methodology pivot from FE to pooled OLS + RE is substantively justified (collinearity of age with year FE; variance-ratio power problem) rather than ad hoc, and the Hausman rejection is disclosed openly. All 26 references verified against Crossref or publisher catalogs; 0 fabricated citations remain. Three rounds of expert-panel review have cleared all HIGH, MEDIUM, LOW, and NITS items flagged; round 3 in particular softened "lock-in proven" language to "strongly consistent with lock-in," reframed the Fukushima subsample result as bounded (rather than absent) responsiveness, and unified the retrofit framing across §5.2 and §5.5.1 from "cannot be converted" to "unlikely under foreseeable economics." A subsequent holistic panel grade round converged on a 良/優 consensus (mean 85.4/100) with the supervisor giving 優/90; a targeted A-push round added three surgical discussion sections (§5.3.1 heat-integration institutional case, §5.5.1 retrofit break-even calculation, §5.5.2 declining grid-EF sensitivity) that close the consensus weaknesses identified by the panel without touching the empirical core, targeting a re-graded band of 89–93 across all panelists.

---

*Last updated: 2026-04-14. Reflects the two-part adoption + generator-efficiency architecture and the current local thesis state.*
