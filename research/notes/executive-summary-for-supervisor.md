# Executive Summary for Supervisor

**To:** Prof. Han Ji
**From:** Pann Phetra (Student ID: 13223029)
**Date:** 2026-04-13
**Re:** Bachelor's thesis — draft ready for review

---

## One-page brief

**Title:** *Carbon Lock-in or Circular Transition? Heterogeneity in Japan's Waste Incineration Fleet and Net-Zero Compatibility*

**Research question:** What facility characteristics predict energy recovery efficiency among Japan's power-generating incinerators, and how has this changed as the fleet modernizes?

**Data:** 20-year facility-level panel from MOE's General Waste Treatment Survey — 23,599 observations across 2,949 unique facilities (FY2005–FY2024). The regression sample after restricting to power-generating facilities and winsorising efficiency at [0.01, 0.80] MWh/t is 6,575 facility-years across 947 facilities.

**Method:** Panel regression with four main specifications (Pooled OLS, Year FE, Random Effects, Year FE + RE) plus eight robustness specifications (pre/post-Fukushima splits, capacity tercile endpoints, raw-DV replications). All specifications use cluster-robust standard errors clustered at the facility level. Following Wooldridge (2010); Niessen (2010) for the engineering background.

**Why not facility fixed effects?** Two substantive reasons. First, facility age increases deterministically by one unit per year, making it nearly collinear with year fixed effects in a two-way FE specification. Second, the within-to-total variance ratio of log-efficiency is only ~0.13, so facility FE would discard 87% of the variation in the dependent variable and yield imprecise estimates. The low variance ratio is itself the central empirical finding of the thesis.

---

## Findings (robust across all 12 specifications)

| Determinant | Coefficient | Interpretation |
|:------------|:------------|:---------------|
| Facility age | −0.028 to −0.043 per year (p < 0.001) | Each additional year ≈ 2.8–4.3% lower efficiency, holding other factors constant |
| Design capacity | +0.08 to +0.10 log-units per 100 t/day (p < 0.001) | Engineering economics of boiler and turbine systems at scale |
| Capacity utilization | +0.58 to +0.62 (p < 0.001) | Thermodynamic gains from operating near design conditions |
| **Within/total variance ratio** | **0.13 pooled, 0.10 pre-Fuku, 0.07 post-Fuku** | **The signature finding: 87% of variation is between facilities, not within them over time** |

**Null results:** Heating value is not significant in any specification. Grid emission factor is sign-unstable across specifications and is not interpretable as a causal effect.

**Headline fleet numbers:** Facility count fell from 1,318 (FY2005) to 1,014 (FY2024), a 23% decline. Power-generating share nearly doubled from 21.6% to 41.1%. But 598 facilities (59% of the active fleet) still generate no electricity. Gross avoided CO₂ emissions from waste-to-energy were approximately 4.6 Mt-CO₂ in FY2024 — an upper bound, since process emissions from combustion are not deducted.

---

## Theoretical contribution

This is unusually clean empirical evidence for Unruh's (2000) carbon lock-in hypothesis in the waste sector. Lock-in theory predicts that infrastructure systems exhibit low within-facility variation in performance over time because physical capital embeds past design decisions. The prediction is confirmed: facilities that were efficient in 2005 remain efficient in 2024; facilities that were inefficient remain inefficient. In a dataset spanning 20 years and covering nearly a thousand facilities, the absence of within-facility efficiency trends is a systematic property of the data. The literature cited includes Arthur (1989) on technological lock-in, Geels (2004) on socio-technical transitions, and Caldecott et al. (2016) on stranded-asset framing. The waste-sector-specific context draws on Sakai et al. (2008, 2011), Sun et al. (2018), Tabata & Tsai (2016), and the MOE survey data itself.

---

## Policy implication

Because efficiency is locked in at the design stage, fleet-wide improvement cannot come from operational intervention. Four recommendations, developed in Chapter 6:

1. **Accelerate targeted retirement** of the ~277 pre-1995 non-power-generating facilities still operating in FY2024.
2. **Scale regional consolidation planning** from the municipal to the prefectural level, backed by national coordination grants.
3. **Redesign monitoring** to serve fleet planning (vintage register, retirement calendar) rather than facility-level efficiency auditing, since within-facility efficiency is effectively fixed.
4. **Concentrate WtE capital incentives** on new-build and major-refurbishment decisions — the points at which design vintage is actually set — rather than operating-side subsidies for already-built facilities.

---

## What I would like feedback on

- **Methodological framing in Chapter 3.** The pivot away from two-way FE to pooled OLS + RE is justified on two grounds (collinearity + variance-ratio), but I want to confirm this framing is legible to an industrial-ecology audience and does not read as avoiding the "default" panel estimator.
- **Chapter 5 discussion of the 59% non-power-generating problem.** I argue these facilities cannot be converted in place and must be replaced via regional consolidation. I would welcome your view on whether this framing is too pessimistic, or whether it matches what you see in the policy literature on Japanese WtE.
- **The "modernizing vanguard vs ageing majority" framing in §5.5.** The thesis uses this split to organise the policy discussion. The vanguard count (137 facilities: built after 2000, capacity > 200 t/day) and the pre-1995 power-gen count (54) are drawn directly from the FY2024 cross-section of the dataset. Please let me know if the framing reads as too binary.
- **The null result on heating value** is argued in Section 2.4.4 to be consistent with combustion-control technology buffering the input–output relationship, though measurement noise cannot be ruled out since heating value is estimated rather than directly measured. I would value your view on whether the Chapter 5 discussion gives this null result appropriate weight.

---

## State of the manuscript

| Item | Status |
|:-----|:-------|
| Thesis body word count | ~13,500 words (~15,200 including tables, equations, bibliography) |
| Chapters drafted | 7 of 7 (Abstract + Ch 1–6) |
| Authoritative source file | `thesis/thesis.tex` — Overleaf-compileable |
| Bibliography | 23 entries, all DOI/URL-verified, 0 orphans, 0 fabricated |
| Tables | 6 (summary stats, fleet evolution, efficiency by age, efficiency by capacity, main regression, robustness) |
| Figures | 2 (establishing shot + heterogeneity shot, in `thesis/figures/`) |
| Expert panel review | 2 rounds completed; all HIGH, MEDIUM, LOW items addressed |
| Ready for supervisor read | **Yes** |

---

## How to access

- **Overleaf-ready LaTeX:** `thesis/thesis.tex` + `thesis/figures/` in the repository at <https://github.com/Pann13223029/incineration-thesis>
- **Full supporting documentation:** `README.md` (research journey with diagrams), `ARCHITECTURE.md` (technical blueprint)
- **Code pipeline:** `code/scripts/` — seven numbered Python scripts that reproduce the full analysis from the raw MOE downloads through the regression tables

I am happy to provide a printed copy of the PDF or a specific chapter if that would help the review.

---

**Contact:** Pann Phetra (Student ID: 13223029)
