# Thesis Architecture — Quick Reference (v1, post-data-investigation)

**Title (working):** Carbon Lock-in or Circular Transition? Heterogeneity in
Japan's Waste Incineration Fleet and Net-Zero Compatibility

---

## Executive Summary

Japan operates ~1,000 waste incinerators — the most of any country. The
literature treats this fleet as monolithic. It is not. This thesis uses a
20-year facility-level panel (23,599 observations, 2,949 unique facilities,
FY2005-2024) to study heterogeneity in energy recovery efficiency and
what drives it.

---

## Research Question (v1 — post-data-investigation)

**RQ:** What facility characteristics predict energy recovery efficiency
among Japan's power-generating incinerators, and how has this changed as
the fleet modernizes?

**Sub-questions:**
1. How does facility age relate to energy recovery efficiency (MWh/t)?
2. Does capacity utilization predict efficiency, controlling for facility age?
3. How does the share of power-generating facilities vary by region, and does
   regional grid carbon intensity contextualize the contribution?

---

## What We Have vs. What We Need

| Data | Status | Source |
|------|:------:|--------|
| Facility-level panel (23,599 obs, 20 years) | **HAVE** | MOE General Waste Survey |
| Power generation capacity (kW) | **HAVE** | 35.4% of all facilities; 98.7% of power-gen subsample |
| Total electricity generated (MWh) | **HAVE** | 34.6% of all; 98.1% of subsample |
| Power generation efficiency (%) | **HAVE** | 98.7% of subsample |
| Facility age (derived) | **HAVE** | 99.8% coverage |
| Capacity utilization (derived) | **HAVE** | 98.3% coverage |
| Heating value of waste (kJ/kg) | **HAVE** | 96.2% coverage |
| Electricity sold externally (MWh) | **HAVE** | FY2018+ only (7.9% overall) |
| Regional grid emission factors | **NEED** | METI annual tables (9 utility areas) |
| Facility-level CO2 emissions | **DON'T HAVE** | Not in MOE survey; not required for current RQ |

---

## Two Populations

The dataset naturally splits into two analytically distinct populations:

| Population | N (obs) | % of total | Purpose |
|------------|:-------:|:----------:|---------|
| **Power-generating facilities** | 6,950 | 29.4% | Main analysis: energy recovery efficiency |
| **Non-power-generating facilities** | 16,649 | 70.6% | Descriptive comparison: what predicts adoption? |

This split is itself a finding: 70% of Japan's incinerators recover no
electricity. The thesis studies both *what makes generators efficient* and
*what distinguishes generators from non-generators*.

---

## Methodology

**Design:** Two-way fixed effects panel (facility FE + year FE)

**Panel window:** FY2005-2024 (20 years, post-Dioxin regulatory stabilization)

**Dependent variable:** Energy recovery efficiency (MWh per tonne processed)
among power-generating facilities

**Key independent variables:**
- Facility age (years since year_started)
- Capacity utilization (throughput / capacity × 365)
- Facility capacity (t/day)
- Heating value of waste input (kJ/kg)

**Moderator (robustness):** Regional grid emission factor (by utility area)

**What this is NOT:**
- Not a causal identification study (no IV)
- Not a spatial analysis (no GIS)
- Not a carbon accounting exercise (no facility-level CO2)
- Not a waste composition study

---

## Chapter Structure (planned)

| Ch | Title | Key content |
|----|-------|-------------|
| 1 | Introduction | The incineration question, RQ, significance |
| 2 | Literature Review | Waste-to-energy in Japan, lock-in theory, fleet heterogeneity gap |
| 3 | Methodology | Data sources, panel construction, FE design, variable definitions |
| 4 | Results | Descriptive stats, fleet trends, FE regression, subsample analysis |
| 5 | Discussion | What drives efficiency, policy implications, limitations |
| 6 | Conclusion | Contributions, implications for 2050 net-zero, future work |

---

## Key Trends Already Visible in the Data

1. **Fleet consolidation:** 1,318 facilities (2005) → 1,014 (2024) = 23% decline
2. **Modernization:** Power-generating share 21.6% → 41.1% over 20 years
3. **Heterogeneity:** ~70% of facilities have NO power generation at all

---

## Assets

| Category | Count |
|----------|:-----:|
| Python scripts | 3 (download, probe, parse) |
| Raw data files | 20 (one per FY) |
| Panel dataset | 23,599 rows × 24 cols |
| Power-gen subsample | 6,950 rows |
| Figures | TBD |
| BibTeX entries | TBD |

---

## Scope Boundaries

**IN:**
- Panel econometrics (two-way FE)
- Facility-level heterogeneity analysis
- Energy recovery efficiency as DV
- Fleet consolidation and modernization trends
- Descriptive comparison of generators vs non-generators
- Grid emission factor as robustness moderator

**OUT:**
- Spatial analysis / GIS / remote sensing
- Causal identification / instrumental variables
- Waste composition modeling
- Facility-level CO2 estimation
- Life cycle assessment
- International comparison

---

## Data Pipeline

```
01_download_facility_data.py     → 20 Excel files (FY2005-2024)
02_parse_facility_panel.py       → incineration_panel.csv (23,599 rows)
03_download_grid_factors.py      → [TODO] METI regional emission factors
04_eda_facility.py               → [TODO] Exploratory analysis + figures
05_panel_regression.py           → [TODO] Two-way FE regression
06_robustness.py                 → [TODO] Subsample analysis, grid moderation
```

---

## Confidence: MEDIUM-HIGH

Data is strong. RQ is estimable. Panel method is proven (student demonstrated
in first thesis). Main risk: ensuring the power-gen subsample (6,950 obs)
has sufficient within-facility variation for FE to work.
