# Executive Summary for Supervisor

**To:** Prof. Han Ji
**From:** Pann Phetra (Student ID: 13223029)
**Date:** 2026-04-15
**Re:** Bachelor's thesis — current defended draft

---

## One-page brief

**Title:** *Carbon Lock-in or Circular Transition? Heterogeneity in Japan's Waste Incineration Fleet and Net-Zero Compatibility*

**Research question:** What predicts observed transition into power generation among coded facilities first seen without generation, and conditional on power generation, what predicts energy recovery efficiency among Japan's power-generating incinerators?

**Data:** 20-year facility-level panel from MOE's General Waste Treatment Survey, FY2005-FY2024.

- Full panel: 23,599 facility-year observations across 2,948 facilities
- Coded full-fleet frame: 19,827 observations across 2,948 facilities
- Extensive-margin adoption risk set: 13,770 facility-years across 2,035 facilities, with 141 observed first-adoption events
- Lagged adoption model frame: 11,717 facility-years across 1,915 facilities and 140 retained events
- Canonical generator-efficiency frame: 5,683 facility-years across 1,016 facilities

**Method:** Two-part empirical design.

1. Extensive margin: lagged discrete-time logit hazard for observed first transition into power generation, with prior-year age bands, prior-year capacity, year fixed effects, prefecture fixed effects, and facility-clustered standard errors.
2. Intensive margin: four main generator-efficiency specifications (Pooled OLS, Year FE, RE, Year FE + RE) plus eight robustness specifications.

**Why not facility fixed effects as the primary model?** Two reasons.

1. Facility age rises mechanically with year, so age is poorly identified in a two-way FE setup once year effects are included.
2. The within-to-total variance ratio of log-efficiency in the canonical generator frame is only 0.1499, falling to 0.0956 post-Fukushima, so FE would lean on the smaller part of the signal while also weakening identification of the main variable of interest.

---

## Main findings

### 1. Transition into power generation is selective, not diffuse

- Facilities older than 10 years in the prior observed year are about 1.1-1.8 percentage points less likely to record transition into power generation than 0-10 year facilities.
- Each additional 100 t/day of prior-year design capacity raises annual transition probability by about 0.5 percentage points.
- The coded panel therefore does not show widespread late conversion among old small plants.

### 2. The observed modernization pathway is usually capital-reset-like, but not exclusively so

- A conservative event-level audit classifies 82 of 141 observed transitions as reset/rebuild-like.
- 38 transitions preserve continuity consistent with in-place upgrading.
- 20 entries are forward-dated or placeholder cases and are left unresolved rather than forced into a stronger mechanism claim.

This supports a calibrated claim: capital-side modernization is empirically prominent in the observed transition wave, but the thesis does **not** claim that replacement is the only pathway or that retrofit never occurs.

### 3. Conditional on generation, efficiency is strongly structured by age, scale, and utilization

| Determinant | Main-model range | Interpretation |
|:------------|:-----------------|:---------------|
| Facility age | -0.019 to -0.035 log-units/year | Older generators are consistently less efficient |
| Design capacity | +0.040 to +0.103 log-units per 100 t/day | Larger facilities capture engineering scale advantages |
| Capacity utilization | +0.541 to +0.779 | Operating closer to design load improves performance |

Heating value is not significant in the main models. Grid emission factor is sign-unstable and not interpreted causally.

### 4. The deepest finding is bounded responsiveness within the generator sample

- Within/total variation ratio of log-efficiency: 0.1499
- Pre-Fukushima ratio: 0.1795
- Post-Fukushima ratio: 0.0956

This pattern is strongly consistent with bounded infrastructural responsiveness: operational changes matter, but they appear too small to erase design- and vintage-based differences once a facility is already in the generating regime.

---

## Theoretical contribution

The thesis now makes two linked contributions rather than one overextended one.

1. It shows that Japan's incineration transition is empirically two-part: observed entry into power generation is an extensive-margin modernization problem, while efficiency differences among generators are an intensive-margin performance problem.
2. It provides facility-level evidence strongly consistent with bounded infrastructural lock-in within the generating segment, in the narrower and more defensible sense emphasized by Seto et al. (2016): performance responds to incentives, but within an envelope shaped by prior capital design.

The claim is therefore not "lock-in proven causally," but "multiple pieces of evidence line up with a bounded-responsiveness lock-in interpretation."

---

## Policy implication

The defended policy implication is now narrower and cleaner than the earlier draft:

- old and small facilities rarely record observed transition into generation in the coded panel
- among generators, operating-side improvements appear bounded relative to vintage and scale gaps
- the observed modernization wave contains more reset/rebuild-like events than continuity-type upgrades

So the thesis argues that Japan's largest fleet-wide gains are more likely to come from capital-side modernization, retirement, replacement, major refurbishment, and regional consolidation than from operating-side fine-tuning alone. It does **not** argue that operations are irrelevant, or that replacement has been uniquely identified as the sole mechanism.

---

## What I would most like feedback on

- Whether the two-part architecture reads as a genuine strengthening of the thesis rather than a narrowing retreat.
- Whether the lock-in framing in Chapters 5 and 6 is now appropriately calibrated: strong, but no longer overstated.
- Whether the policy section now strikes the right balance between actionable interpretation and overreach.
- Whether the thesis reads more like a disciplined quantitative paper and less like a broad undergraduate survey.

---

## State of the manuscript and repo

| Item | Status |
|:-----|:-------|
| Authoritative thesis source | `thesis/thesis.tex` |
| Canonical analysis rebuild | `.venv/bin/python code/scripts/07_rebuild_analysis.py` |
| Repo-level claim/evidence verifier | `.venv/bin/python code/scripts/08_verify_claims.py` |
| Claim verification report | `output/claim_verification.md` |
| Bibliography | 26 entries, DOI/URL-verified |
| Expert-panel hardening | completed through redesign, adoption hardening, wording calibration, and verifier gate |
| Current repo state | analysis rebuild and claim verifier pass |

---

## Supporting files

- Thesis source: `thesis/thesis.tex`
- Technical blueprint: `ARCHITECTURE.md`
- Repo summary and reproduction guide: `README.md`
- Examiner risk register: `research/notes/examiner-risk-register.md`
- Claim verification report: `output/claim_verification.md`
- Extensive-margin output: `output/adoption_results.md`
- Intensive-margin output: `output/regression_results.md`

This brief now reflects the current two-part architecture and verified thesis-facing numbers, rather than the earlier generator-only draft.
