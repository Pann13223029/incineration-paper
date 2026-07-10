# Claim-to-Evidence Map

Curated bridge between the paper's claims and the canonical generated outputs.

Use this alongside `output/claim_verification.md`: the verifier confirms wording is synchronized, while this map explains which artifact supports which defended claim.

## Claim 1: The paper is empirically two-part

Paper claim: the fleet transition question must be split into an installed-capacity entry layer and a conditional generator-performance layer.

Evidence spine:
- `output/adoption_results.md`: installed-capacity entry risk set of 13,770 facility-years across 2,035 facilities, with 141 entry events.
- `output/regression_results.md`: canonical generator frame of 5,683 facility-years across 1,016 facilities.
- `paper/manuscript/paper.md` Sections 1, 3, and 4: architecture is framed explicitly as extensive margin first, intensive margin second.

## Claim 2: Entry is scale-selective while its age pattern depends on the risk set

Paper claim: prior-year scale predicts entry in both the broad asset and active-conversion frames, while the broad age gradient attenuates when positive prior-year throughput is required.

Evidence spine:
- `output/adoption_results.md`: lagged logit hazard on 10,823 facility-years across 1,911 facilities and 98 retained events.
- `output/adoption_results.md`: 40 of 98 exact-year events have zero or missing prior-year throughput.
- `output/adoption_results.md`: active conversion uses 9,215 rows, 1,663 facilities, and 58 events.
- `output/adoption_results.md`: capacity is +0.45 pp broad and +0.44 pp active per 100 t/day.
- `output/adoption_results.md`: broad age AMEs −1.41/−1.45/−0.83 pp attenuate to −0.67/−0.56/−0.29 pp.
- `output/adoption_results.md` event-rate tables use exact-lag prior-year profiles and show strongly increasing rates across capacity quartiles.
- `output/identifier_gap_audit.md`: exact one-fiscal-year lags are the main adoption frame; previous-observed-coded-row estimates are sensitivity evidence only.
- `output/adoption_results.md`: the positive-output alternative retains 146 exact-year events and a +0.64 percentage-point capacity AME.

## Claim 3: Capacity entry maps to operation but not automatically to superior performance

Paper claim: capacity entry is usually followed by positive output, entrants begin near the middle of the same-year generator distribution on average, and non-entry cannot be treated as continuous observation through FY2024.

Evidence spine:
- `output/post_adoption_bridge.csv`: 135 of 141 entrants report positive output by the following year; 137 enter the canonical generator frame within three years.
- `output/post_adoption_trajectories.csv`: 389 observations across 137 events; mean same-year percentile is 51.5 at event time zero and 52.9 at time three.
- `output/adoption_results.md`: 1,305 of 1,894 non-entrants (68.9%) are last observed before FY2024.
- `output/figure2_transition_effects.csv`: age 30+ panel-exit AME +2.60 pp and capacity AME −1.63 pp per 100 t/day.

## Claim 4: Capital-reset-like modernization is empirically prominent, but not uniquely identified

Paper claim: the pathway audit supports a calibrated mechanism claim, not a proof that replacement is the only pathway.

Evidence spine:
- `output/adoption_results.md`: pathway audit counts 50 reset/rebuild-like, 36 continuity/in-place-upgrade-like, 12 forward-dated/placeholder, 42 timing-ambiguous, 1 unresolved.
- `output/adoption_results.md`: explicit rule set based on `year_started` reset, mature-to-new age reset, continuity, timing ambiguity, and unresolved placeholder cases.
- `paper/notes/claim-stack.md`: the claim stack keeps mechanism language calibrated.

## Claim 5: Conditional generator performance is structured after observed-technology adjustment

Paper claim: within common fiscal years, gross MWh/t is lower at older-vintage plants and higher at larger, more utilized plants after adjustment for observed technology configuration.

Evidence spine:
- `output/regression_results.md`: primary coefficients are age/vintage −0.0329, capacity +0.1103, and utilization +0.7600.
- `output/claim_verification.md`: within/total ratio is 0.1499, with 0.1795 in the early coded window (FY2005–FY2009) and 0.0956 in the later coded window (FY2013–FY2024).
- `output/figure3_persistence.csv`: pooled adjacent-year within-year rank correlation is 0.9325 across 4,368 exact pairs.
- `output/robustness_results.md`: engineering validation uses 4,971 plausible rows; logged thermal conversion and reported efficiency correlate at 0.8636 and preserve the focal signs.
- `output/data_quality_sensitivity.md`: duplicate-ID and heating-value sensitivity checks preserve the same headline sign pattern.
- `output/identifier_gap_audit.md`: the canonical generator regression frame is an identifiable coded-generator panel, not a complete census of all operating generator rows.

## Claim 6: The paper supports planning diagnostics, not an exclusive mechanism claim

Paper claim: planning assessments should distinguish facilities outside electricity recovery from operating generators because the observable constraints differ across those two groups.

Evidence spine:
- `output/adoption_results.md`: scale selectivity survives both risk sets, age is frame-dependent, and older/smaller facilities are more likely to exit the coded panel.
- `output/regression_results.md`: utilization is strongly positive, so operational levers are preserved rather than dismissed.
- `paper/supplement/supplement.md`: the supplement explicitly records the data-quality caveats and identification limits.

## Reviewer Use

1. Start with `paper/manuscript/paper.md` for the active narrative.
2. Use `output/claim_verification.md` to confirm the current wording matches the generated artifacts.
3. Use this file to see which exact output anchors each paper claim.
4. Use `paper/supplement/supplement.md` and `paper/notes/claim-stack.md` to keep the scope disciplined during review.
