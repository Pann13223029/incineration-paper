# Claim-to-Evidence Map

Curated bridge between the defended thesis claims and the canonical generated outputs.

Use this alongside `output/claim_verification.md`: the verifier confirms wording is synchronized, while this map explains which artifact supports which defended claim.

## Claim 1: The thesis is empirically two-part

Defended claim: the fleet transition question must be split into an extensive-margin adoption layer and an intensive-margin generator-efficiency layer.

Evidence spine:
- `output/adoption_results.md`: observed first-adoption risk set of 13,770 facility-years across 2,035 facilities, with 141 observed transition events.
- `output/regression_results.md`: canonical generator frame of 5,683 facility-years across 1,016 facilities.
- `thesis/thesis.tex` Chapters 1, 3, and 4: architecture is framed explicitly as extensive margin first, intensive margin second.

## Claim 2: Observed transition into generation is selective rather than diffuse

Defended claim: among coded facilities first observed without generation, younger and larger facilities are more likely to record observed transition into generation.

Evidence spine:
- `output/adoption_results.md`: lagged logit hazard on 11,717 facility-years across 1,915 facilities and 140 retained events.
- `output/adoption_results.md`: prior-year age effects range from −1.76 to −1.13 percentage points relative to age 0-10.
- `output/adoption_results.md`: prior-year capacity effect is +0.50 percentage points per 100 t/day.
- `output/adoption_results.md` event-rate tables: event rates collapse after age 10 and rise sharply across capacity quartiles.

## Claim 3: Capital-reset-like modernization is empirically prominent, but not uniquely identified

Defended claim: the pathway audit supports a calibrated mechanism claim, not a proof that replacement is the only pathway.

Evidence spine:
- `output/adoption_results.md`: pathway audit counts 82 reset/rebuild-like, 38 continuity/in-place-upgrade-like, 20 forward-dated/placeholder, 1 unresolved.
- `output/adoption_results.md`: explicit rule set based on `year_started` reset, mature-to-new age reset, continuity, and unresolved placeholder cases.
- `research/notes/what-this-thesis-does-not-claim.md`: the non-claims note keeps the mechanism language calibrated.

## Claim 4: Conditional generator performance is shaped more by cross-facility structure than by large within-facility movement

Defended claim: within the generator sample, age, scale, and utilization matter strongly, while within-facility responsiveness remains bounded.

Evidence spine:
- `output/regression_results.md`: age coefficients remain negative, capacity positive, and utilization positive across the four main specifications.
- `output/claim_verification.md`: within/total ratio is 0.1499, with 0.1795 pre-Fukushima and 0.0956 post-Fukushima.
- `output/robustness_results.md`: sign pattern remains stable across the defended robustness set.
- `output/data_quality_sensitivity.md`: duplicate-ID and heating-value sensitivity checks preserve the same headline sign pattern.

## Claim 5: The thesis supports a policy hierarchy, not an exclusive mechanism claim

Defended claim: capital-side modernization and consolidation likely matter more for the weakest segment than operating-side fine-tuning alone, while operations still matter within the design envelope.

Evidence spine:
- `output/adoption_results.md`: old and small facilities rarely record observed transition into generation.
- `output/regression_results.md`: utilization is strongly positive, so operational levers are preserved rather than dismissed.
- `research/notes/what-this-thesis-does-not-claim.md`: the thesis explicitly avoids claiming causal proof, exclusive replacement, full lifecycle accounting, or heat-recovery evaluation.

## Reviewer Use

1. Start with `research/notes/executive-summary-for-supervisor.md` for the one-page narrative.
2. Use `output/claim_verification.md` to confirm the current wording matches the generated artifacts.
3. Use this file to see which exact output anchors each defended claim.
4. Use `research/notes/what-this-thesis-does-not-claim.md` to keep the scope disciplined during review or viva prep.
