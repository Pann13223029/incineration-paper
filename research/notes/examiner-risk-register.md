# Examiner Risk Register

Compact map of the strongest remaining attack surfaces after the redesign, adoption hardening, and claim-verification pass.

This is not a replacement for `defense-q-and-a.md`. It is a higher-level reviewer tool:

- what the strongest criticism is
- why it does not break the defended thesis
- which artifact anchors the mitigation

Use it before supervisor review, before packet freeze, and before viva rehearsal.

| Risk area | Strongest attack | Why it does not break the thesis | Supporting artifact |
|:----------|:-----------------|:---------------------------------|:--------------------|
| Extensive-margin scope | The adoption model still does not reconstruct the full historical modernization path of the whole fleet. | True, and the thesis no longer claims that it does. The defended claim is limited to the coded, initially non-generating subset and observed first transitions inside that panel. | `research/notes/what-this-thesis-does-not-claim.md`, `output/adoption_results.md` |
| Non-causal design | The thesis does not identify a clean causal effect of age, capacity, or utilization. | Correct. The thesis is defended as a disciplined observational panel study, not an IV or natural-experiment paper. Its strongest language is “strongly consistent with,” not “causally proves.” | `thesis/thesis.tex`, `research/notes/defense-q-and-a.md` |
| Adoption mechanism ambiguity | The pathway audit does not cleanly distinguish replacement, new build, and major refurbishment. | Correct, and that limitation is explicit. The audit is used to bound plausible pathways, not to identify one unique capital-history mechanism. | `output/adoption_results.md`, `research/notes/what-this-thesis-does-not-claim.md` |
| Fixed-effects challenge | A quantitative examiner may still argue that FE is the default and should dominate the design. | The thesis has a principled reason not to treat two-way FE as the main specification: age is mechanically linked to time, and only 14.99% of generator-efficiency variation is within-facility in the canonical frame. | `output/claim_verification.md`, `research/notes/defense-q-and-a.md` |
| Generator-sample overreach | Generator-only results could still be read as if they describe the full fleet. | That was the earlier weakness, and the redesign fixes it by separating entry into generation from conditional generator efficiency. The thesis now has a two-part architecture rather than one overextended frame. | `output/claim_evidence_map.md`, `research/notes/executive-summary-for-supervisor.md` |
| Heating-value measurement | Heating value is noisy and may be too weakly measured to support strong interpretation. | Agreed. The thesis treats heating value as a noisy administrative control and does not build a main claim on its insignificance. | `thesis/thesis.tex`, `research/notes/defense-q-and-a.md` |
| Carbon accounting | The FY2024 avoided-CO2 figure could be mistaken for a full climate result. | The thesis explicitly presents it as a gross upper-bound displacement estimate, not a full life-cycle or net-emissions calculation. | `research/notes/what-this-thesis-does-not-claim.md`, `thesis/thesis.tex` |
| Heat-recovery omission | The thesis only analyzes electricity generation, not total energy recovery or district heating. | Correct. That is a data-support boundary, not a hidden omission. The thesis prefers a narrower, defensible electricity panel over a noisier total-energy claim it cannot support cleanly. | `research/notes/what-this-thesis-does-not-claim.md`, `research/notes/defense-q-and-a.md` |
| Japan-specific generalization | The findings may not travel directly outside Japan. | The thesis does not claim automatic external generalization. It presents Japan as a high-incineration facility-level case with cautious comparative relevance. | `research/notes/what-this-thesis-does-not-claim.md` |

## Fast reading

If someone presses hard, the clean summary is:

1. The strongest remaining weakness is mechanism resolution within the reset/rebuild-like bucket.
2. The strongest remaining non-weakness is that the thesis no longer overclaims past its sample or design.
3. The thesis is strongest when defended as a narrow, reproducible, two-part observational study rather than as a fully causal modernization history.

## Operating rule

If a reviewer comment lands on one of these rows, do not improvise a broader claim to “win” the point.

1. Acknowledge the limit directly.
2. Restate the narrower defended claim.
3. Point to the artifact that supports that calibrated version.
