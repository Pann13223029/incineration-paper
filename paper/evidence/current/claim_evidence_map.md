# Claim-to-Evidence Map

Curated bridge between the paper's claims and the canonical generated outputs.

Use this alongside `output/claim_verification.md`: the verifier confirms wording is synchronized, while this map explains which artifact supports which defended claim.

## Claim 1: The paper is empirically two-part

Paper claim: the fleet transition question must be split into an installed-capacity entry layer and a conditional generator-performance layer.

Evidence spine:
- `output/adoption_results.md`: installed-capacity entry risk set of 13,770 facility-years across 2,035 facilities, with 141 entry events.
- `output/regression_results.md`: canonical generator frame of 5,683 facility-years across 1,016 facilities.
- `paper/manuscript/paper.md` Sections 1, 3, and 4: architecture is framed explicitly as extensive margin first, intensive margin second.

## Claim 2: Installed-capacity entry is selective rather than diffuse

Paper claim: among coded facilities first observed without installed generation capacity, younger and larger facilities are more likely to first report positive capacity.

Evidence spine:
- `output/adoption_results.md`: lagged logit hazard on 10,823 facility-years across 1,911 facilities and 98 retained events.
- `output/adoption_results.md`: prior-year age effects range from −1.94 to −1.24 percentage points relative to age 0-10.
- `output/adoption_results.md`: prior-year capacity effect is +0.45 percentage points per 100 t/day.
- `output/adoption_results.md` event-rate tables: event rates collapse after age 10 and rise sharply across capacity quartiles.
- `output/identifier_gap_audit.md`: exact one-fiscal-year lags are the main adoption frame; previous-observed-coded-row estimates are sensitivity evidence only.
- `output/adoption_results.md`: the positive-output alternative retains 146 exact-year events and a +0.67 percentage-point capacity AME.

## Claim 3: Capacity entry usually maps to observed operation, while panel exit is a competing path

Paper claim: the capacity event is usually followed by positive output, but non-entry cannot be treated as continuous observation through FY2024.

Evidence spine:
- `output/post_adoption_bridge.csv`: 135 of 141 entrants report positive output by the following year; 137 enter the canonical generator frame within three years.
- `output/adoption_results.md`: 1,305 of 1,894 non-entrants (68.9%) are last observed before FY2024.
- `output/figure2_transition_effects.csv`: age 30+ panel-exit AME +2.60 pp and capacity AME −1.63 pp per 100 t/day.

## Claim 4: Capital-reset-like modernization is empirically prominent, but not uniquely identified

Paper claim: the pathway audit supports a calibrated mechanism claim, not a proof that replacement is the only pathway.

Evidence spine:
- `output/adoption_results.md`: pathway audit counts 50 reset/rebuild-like, 36 continuity/in-place-upgrade-like, 12 forward-dated/placeholder, 42 timing-ambiguous, 1 unresolved.
- `output/adoption_results.md`: explicit rule set based on `year_started` reset, mature-to-new age reset, continuity, timing ambiguity, and unresolved placeholder cases.
- `paper/notes/claim-stack.md`: the claim stack keeps mechanism language calibrated.

## Claim 5: Conditional generator performance is shaped more by cross-facility structure than by large within-facility movement

Paper claim: within the generator sample, age, scale, and utilization matter strongly, while most observed variation remains between facilities rather than within facilities over time.

Evidence spine:
- `output/regression_results.md`: age coefficients remain negative, capacity positive, and utilization positive across the four main specifications.
- `output/claim_verification.md`: within/total ratio is 0.1499, with 0.1795 in the early coded window (FY2005–FY2009) and 0.0956 in the later coded window (FY2013–FY2024).
- `output/figure3_persistence.csv`: pooled adjacent-year within-year rank correlation is 0.9325 across 4,368 exact pairs.
- `output/robustness_results.md`: sign pattern remains stable across the reported robustness set.
- `output/data_quality_sensitivity.md`: duplicate-ID and heating-value sensitivity checks preserve the same headline sign pattern.
- `output/identifier_gap_audit.md`: the canonical generator regression frame is an identifiable coded-generator panel, not a complete census of all operating generator rows.

## Claim 6: The paper supports planning diagnostics, not an exclusive mechanism claim

Paper claim: planning assessments should distinguish facilities outside electricity recovery from operating generators because the observable constraints differ across those two groups.

Evidence spine:
- `output/adoption_results.md`: installed-capacity entry is concentrated among younger and larger facilities, while older/smaller facilities are more likely to exit the coded panel.
- `output/regression_results.md`: utilization is strongly positive, so operational levers are preserved rather than dismissed.
- `paper/supplement/supplement.md`: the supplement explicitly records the data-quality caveats and identification limits.

## Reviewer Use

1. Start with `paper/manuscript/paper.md` for the active narrative.
2. Use `output/claim_verification.md` to confirm the current wording matches the generated artifacts.
3. Use this file to see which exact output anchors each paper claim.
4. Use `paper/supplement/supplement.md` and `paper/notes/claim-stack.md` to keep the scope disciplined during review.
