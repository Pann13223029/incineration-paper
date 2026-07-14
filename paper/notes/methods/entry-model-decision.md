# Entry-Model Decision Memo

**Frozen:** 14 July 2026, before fitting the revised primary specification

**Purpose:** reduce information demand in the sparse first-reported-capacity
analysis without selecting a model for a favorable result.

## Primary estimand

The estimand is the conditional annual odds of first reporting positive
installed electrical capacity among administrative facility lineages first
observed without capacity. Predictors are measured in the immediately preceding
fiscal year. The model does not estimate physical commissioning, retrofit, or
capacity-expansion effects.

## Primary specification

The revised Firth model contains five parameters including the intercept:

1. prior processing design capacity as `log(1 + C/100)`;
2. prior reported age in decades;
3. centered fiscal year in five-year units;
4. `log(1 + elapsed years at risk)`; and
5. an intercept.

This replaces three age indicators, three calendar-era indicators, and three
elapsed-risk indicators with one term for each construct. With 35 broad-frame
events, the parameter-to-event burden improves from about 3.2 to 7.0 events per
coefficient. The functional forms are chosen for parsimony and interpretability,
not from revised-model p-values.

## Required uncertainty and influence checks

- Firth bias reduction remains the estimator.
- Final percentile intervals use 1,999 deterministic whole-lineage bootstrap
  replications in the broad, prior-operation, same-episode, and
  identity-certain frames.
- Event-deletion diagnostics reclassify each event once as a final censored
  observation while retaining its prior risk history.
- Lineage-deletion diagnostics remove the complete event lineage once.
- The 300-versus-100 t/day contrast is retained because it was defined before
  the revised fit and is easier to interpret than a one-unit transformed-scale
  coefficient.

## Sensitivity role of the previous model

The earlier 11-parameter age-band, era-band, and duration-band model is retained
as a sensitivity. It is no longer the primary inferential specification. Its
near-threshold same-episode age result cannot override the revised model or the
continuity sensitivity as a whole.

## Decision rules

- If the scale coefficient changes sign under any single event-lineage deletion,
  the public headline becomes descriptive scale concentration only.
- If the revised broad and same-episode bootstrap intervals do not remain
  positive, the paper does not claim continuity-robust scale association.
- If age inference changes materially across continuity frames, age remains a
  sensitivity finding rather than a general headline.
- No coefficient is interpreted as a treatment effect.
