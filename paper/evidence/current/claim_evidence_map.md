# Claim-to-Evidence Map

Curated bridge between the paper's claims and the canonical generated outputs.

Use this alongside `output/claim_verification.md`: the verifier confirms wording is synchronized, while this map explains which artifact supports which defended claim.

## Claim 1: The thesis is empirically two-part

Paper claim: the fleet transition question must be split into an extensive-margin adoption layer and a conditional generator-performance layer.

Evidence spine:
- `output/adoption_results.md`: observed first-adoption risk set of 13,770 facility-years across 2,035 facilities, with 141 observed transition events.
- `output/regression_results.md`: canonical generator frame of 5,683 facility-years across 1,016 facilities.
- `paper/manuscript/paper.md` Sections 1, 3, and 4: architecture is framed explicitly as extensive margin first, intensive margin second.

## Claim 2: Observed transition into generation is selective rather than diffuse

Paper claim: among coded facilities first observed without generation, younger and larger facilities are more likely to record observed transition into generation.

Evidence spine:
- `output/adoption_results.md`: lagged logit hazard on 10,823 facility-years across 1,911 facilities and 98 retained events.
- `output/adoption_results.md`: prior-year age effects range from −2.31 to −1.59 percentage points relative to age 0-10.
- `output/adoption_results.md`: prior-year capacity effect is +0.40 percentage points per 100 t/day.
- `output/adoption_results.md` event-rate tables: event rates collapse after age 10 and rise sharply across capacity quartiles.

## Claim 3: Capital-reset-like modernization is empirically prominent, but not uniquely identified

Paper claim: the pathway audit supports a calibrated mechanism claim, not a proof that replacement is the only pathway.

Evidence spine:
- `output/adoption_results.md`: pathway audit counts 50 reset/rebuild-like, 36 continuity/in-place-upgrade-like, 12 forward-dated/placeholder, 42 timing-ambiguous, 1 unresolved.
- `output/adoption_results.md`: explicit rule set based on `year_started` reset, mature-to-new age reset, continuity, timing ambiguity, and unresolved placeholder cases.
- `paper/notes/claim-stack.md`: the claim stack keeps mechanism language calibrated.

## Claim 4: Conditional generator performance is shaped more by cross-facility structure than by large within-facility movement

Paper claim: within the generator sample, age, scale, and utilization matter strongly, while most observed variation remains between facilities rather than within facilities over time.

Evidence spine:
- `output/regression_results.md`: age coefficients remain negative, capacity positive, and utilization positive across the four main specifications.
- `output/claim_verification.md`: within/total ratio is 0.1499, with 0.1795 in the early coded window (FY2005–FY2009) and 0.0956 in the later coded window (FY2013–FY2024).
- `output/robustness_results.md`: sign pattern remains stable across the reported robustness set.
- `output/data_quality_sensitivity.md`: duplicate-ID and heating-value sensitivity checks preserve the same headline sign pattern.

## Claim 5: The paper supports planning diagnostics, not an exclusive mechanism claim

Paper claim: planning assessments should distinguish facilities outside electricity recovery from operating generators because the observable constraints differ across those two groups.

Evidence spine:
- `output/adoption_results.md`: old and small facilities rarely record observed transition into generation.
- `output/regression_results.md`: utilization is strongly positive, so operational levers are preserved rather than dismissed.
- `paper/supplement/supplement.md`: the supplement explicitly records the data-quality caveats and identification limits.

## Reviewer Use

1. Start with `paper/manuscript/paper.md` for the active narrative.
2. Use `output/claim_verification.md` to confirm the current wording matches the generated artifacts.
3. Use this file to see which exact output anchors each paper claim.
4. Use `paper/supplement/supplement.md` and `paper/notes/claim-stack.md` to keep the scope disciplined during review.
