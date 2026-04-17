# Supplementary Material

## S1. Purpose Of The Supplement

This supplement protects the main paper from technical overload. The main text
keeps the argument readable; the supplement carries the denser sample,
classification, robustness, and estimator-comparison detail that a skeptical
reviewer may still want to inspect.

## S2. Analytical Frames And Sample Construction

The analysis begins from a Ministry of the Environment facility panel covering
FY2005-FY2024. The full panel contains 23,599 facility-year rows. Within that,
the coded full-fleet frame contains 19,827 observations across 2,948
facilities.

### S2.1 Adoption frame

- Left-censored facilities already generating in their first observed year: 913
- Adoption risk-set observations: 13,770
- Adoption risk-set facilities: 2,035
- Observed first-adoption events in the panel window: 141
- Lagged adoption-model observations: 11,717
- Lagged adoption-model facilities: 1,915
- First-adoption events retained in the lagged model: 140

Interpretation: the main adoption model is a model of observed transition within
the coded at-risk frame, not an unrestricted fleet-wide modernization model.

### S2.2 Generator frame

- Canonical regression observations: 5,683
- Canonical regression facilities: 1,016
- Fiscal years covered: FY2005-FY2024
- Within/total variance ratio of pooled log-efficiency: 0.1499
- Pre-Fukushima ratio: 0.1795
- Post-Fukushima ratio: 0.0956

Interpretation: the intensive-margin models are designed to describe structured
conditional performance within the generating segment, not to identify a strict
causal policy effect.

## S3. Adoption Risk-Set Rules

The adoption frame includes facilities first observed without power generation.
Facilities already generating in their first observed year are excluded as
left-censored for the adoption question. The lagged hazard specification then
requires prior-year age band and prior-year design capacity, which removes the
first observed at-risk year for each facility and a small number of additional
rows with missing lagged predictors.

## S4. Pathway-Audit Rule Set

The pathway audit is designed to bound mechanism language, not to prove a unique
modernization pathway.

### S4.1 Categories

- `Reset / rebuild-like transition`
- `In-place upgrade / continuity transition`
- `Forward-dated / placeholder entry`
- `Unresolved / insufficient continuity`

### S4.2 Rule logic

- `Reset / rebuild-like` requires an observed reset in `year_started` or a
  mature-to-new age reset before adoption.
- `In-place upgrade / continuity` requires no such reset on the observed event
  row and continuity of the facility record into the adoption event.
- `Forward-dated / placeholder` captures cases where the event row appears to be
  forward-dated or placeholder-like and should not be forced into a stronger
  mechanism claim.
- `Unresolved` is reserved for events without a usable continuity row.

### S4.3 Category counts

- Reset / rebuild-like: 82
- In-place upgrade / continuity: 38
- Forward-dated / placeholder: 20
- Unresolved: 1

Interpretation: the pathway distribution is supportive descriptive evidence for
selective modernization, but it does not uniquely identify replacement, major
refurbishment, or new build as the dominant mechanism.

## S5. Robustness And Estimator Notes

### S5.1 Adoption robustness

The main adoption result is estimated as a lagged discrete-time logit hazard
with year and prefecture fixed effects plus facility-clustered standard errors.
Two robustness variants preserve the main sign pattern:

- lagged complementary log-log
- lagged linear probability model

In both variants, older facilities remain less likely to record observed
transition and larger facilities remain more likely to do so.

### S5.2 Efficiency estimator note

The main efficiency results are presented through four compact specifications:

- pooled OLS
- year fixed effects
- random effects
- year fixed effects plus random effects

The paper keeps these models because the intensive-margin question is largely
about structured cross-facility differences inside the generating segment. The
coefficients are therefore interpreted as structured conditional associations,
not as strict structural parameters.

## S6. Additional Descriptive Material

Useful descriptive tables already synchronized into the paper workspace include:

- [sample_definition.md](../evidence/current/sample_definition.md)
- [adoption_results.md](../evidence/current/adoption_results.md)
- [regression_results.md](../evidence/current/regression_results.md)
- [table1_summary_stats.md](../evidence/current/table1_summary_stats.md)
- [table2_efficiency_by_age.md](../evidence/current/table2_efficiency_by_age.md)

These files remain part of the paper's evidence layer and can be converted into
appendix tables if a target journal asks for additional detail.
