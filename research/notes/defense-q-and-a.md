# Defense Q&A Bank

Short hostile questions and disciplined answers for oral defense, revision, or application discussions. All answers are calibrated to the current verified repo state in `output/claim_verification.md`.

---

## Architecture

### 1. Why is this thesis no longer just a generator-efficiency panel?

Because the strongest criticism of the earlier version was scope leakage. A generator-only model can say something about efficiency conditional on generation, but it cannot carry the whole fleet-level transition story. The redesign splits the question into two parts: observed transition into generation on the coded full-fleet frame, and conditional efficiency among generators.

### 2. Does the new adoption model solve the external-validity problem completely?

No. It solves the biggest part of it by separating entry into generation from conditional efficiency, but it still identifies observed first adoption only within the coded, initially non-generating subset. That is why the thesis now speaks in terms of the coded panel and observed transitions, not an omniscient fleet history.

### 3. Why use a complementary log-log hazard?

Because the event is rare and discrete-time. A cloglog hazard is a stronger main specification than the earlier linear probability framing, while still yielding interpretable average marginal effects in percentage points. The sign pattern also survives lagged logit and lagged LPM robustness checks.

### 4. Why are the adoption predictors lagged?

To avoid mixing predictors with same-year redesign. Capacity and age can move in the transition year, especially around rebuild-like events. Using prior-year values makes the extensive-margin model a cleaner pre-adoption predictor rather than a contemporaneous restatement of the event.

---

## Identification

### 5. Does this thesis make a causal claim?

No. It is an observational panel study with strong descriptive and associational evidence, not an IV or natural-experiment identification design. The defended language is "strongly consistent with" bounded lock-in, not "causally proves" lock-in.

### 6. Why not two-way fixed effects?

Because facility age, the central variable of interest, rises mechanically with year, so age is poorly identified once year effects are added. Also, the within-to-total variation ratio of log-efficiency is only 0.1499 in the canonical frame, so FE would lean on the smaller part of the signal while discarding the cross-facility variation the thesis is actually trying to interpret.

### 7. Doesn't the Hausman rejection force you into FE?

No. A Hausman rejection says FE and RE differ under that comparison; it does not by itself make FE the substantively right design when the main regressor is mechanically linked to time and within-facility variation is limited. The estimator choice is driven by the thesis question and identification structure, not by a ritual preference for FE.

### 8. Does the 0.1499 ratio prove lock-in?

No. By itself it is descriptive. What the thesis argues is that the low within-to-total ratio, its persistence across pre/post-Fukushima windows, and the stable age/scale relationships together are strongly consistent with bounded infrastructural responsiveness. That is a much narrower and stronger claim than "lock-in proven."

---

## Pathways

### 9. Do you prove that replacement is the dominant mechanism?

No. The pathway audit is rule-based and conservative. It shows that the largest observed bucket in the panel is reset/rebuild-like (82 of 141 events), with 38 continuity-type upgrades and 20 unresolved forward-dated or placeholder entries. That supports "capital-side modernization is empirically prominent," not "replacement uniquely identified."

### 10. Then what exactly does the pathway audit add?

It prevents the policy section from outrunning the data. Without it, the adoption model only shows that transition is more common among younger and larger facilities. The audit adds bounded mechanism evidence by showing that many observed transitions coincide with start-year or age resets rather than continuity-only upgrades.

### 11. So can retrofit still matter?

Yes. The thesis explicitly leaves room for selective retrofit and in-place upgrading, and the audit contains 38 continuity-type events consistent with that. The defended claim is comparative: retrofit exists, but the observed transition wave is not dominated by diffuse late-life conversion of old small plants.

---

## Policy

### 12. Are you saying operations do not matter?

No. Capacity utilization is strongly positive across the main and robustness models, and the thesis preserves routing, utilization, and selective retrofit as real levers. The claim is that these levers appear bounded relative to the larger gaps associated with age, scale, and the extensive-margin modernization problem.

### 13. Why not recommend pure operational optimization first?

Because the evidence suggests it cannot carry the whole burden. Old and small facilities rarely record observed transition into generation, and among generators the largest performance differences are between facilities rather than within facilities over time. That points to a policy hierarchy where operations matter, but capital-side modernization matters more for the weakest segment.

### 14. Isn't the policy section too broad for the evidence?

It would be, if it claimed replacement alone was identified or if it generalized from the generator sample to the whole fleet without an extensive-margin layer. The revised thesis avoids both. The policy section is now tied to a two-part architecture and carefully distinguishes what the panel shows from what it does not show.

### 15. Are you endorsing waste-to-energy as a circular-economy ideal?

No. The thesis does not argue that WtE should outrank waste reduction, reuse, or recycling. It asks a narrower empirical question: given that Japan still incinerates most municipal waste, which facilities recover energy, and which design features predict better energy recovery among generators?

---

## Data and measurement

### 16. What is the weakest variable in the model?

Heating value. It is an administrative estimate and should be treated as a noisy control rather than a clean engineering measurement. Its null result is therefore interpreted cautiously.

### 17. Is the avoided-CO2 result a full climate accounting?

No. The FY2024 avoided-CO2 calculation is a gross upper bound based on displaced grid electricity. It does not deduct process emissions from combustion and is not presented as a full life-cycle assessment.

### 18. Why focus only on electricity and not heat recovery?

Because the MOE panel gives reliable electricity-generation information, while facility-level heat recovery and district heating utilization are not measured in a way that supports a comparable panel design here. The thesis flags heat integration as a real future-work question rather than pretending to answer it.

### 19. Could unobserved retrofit histories explain some of the age effect?

Yes, in part. The thesis does not claim to observe retrofit investments directly. That is why the interpretation stays at the level of bounded responsiveness and design-conditioned performance, not a pure vintage effect cleanly separated from retrofit history.

---

## Framing

### 20. What is the single cleanest sentence describing the thesis contribution?

Japan's incineration transition is empirically two-part: observed entry into power generation is concentrated among younger and larger facilities on the extensive margin, and conditional generator performance is strongly shaped by age, scale, and bounded within-facility responsiveness on the intensive margin.

### 21. What is the safest one-sentence answer if pressed on overclaim risk?

This thesis does not prove one causal mechanism; it shows, with a reproducible two-part design, that Japan's observed modernization wave is selective and that generator performance appears strongly constrained by design and vintage rather than easily reversed by operational changes alone.

### 22. What is the biggest remaining weakness if an examiner keeps pushing?

The thesis still cannot directly distinguish replacement, new build, and major refurbishment within the reset/rebuild-like bucket, because the administrative panel was not designed as a capital-history dataset. That limitation is explicit, and the claims are calibrated around it.
