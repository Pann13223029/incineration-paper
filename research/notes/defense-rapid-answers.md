# Rapid Defense Answers

Short spoken versions of the highest-risk answers. These are the answers to practice until they come out immediately and without defensive drift.

Use this file with:

- `research/notes/defense-question-order.md`
- `research/notes/defense-q-and-a.md`
- `research/slides/defense-deck.md`

---

## Tier 1

### Why is the thesis now a two-part design?

Because the earlier version asked a generator sample to explain the whole fleet. The redesign splits entry into generation from performance within generation, so each claim is now matched to the right sample.

### Why not two-way fixed effects?

Because age rises mechanically with year, so the main regressor is poorly identified in two-way FE. And only 14.99% of the efficiency signal is within-facility, so FE would lean on the smaller part of the data.

### Does the thesis make a causal claim?

No. It is a disciplined observational panel study. The defended language is "strongly consistent with bounded infrastructural responsiveness," not "causally proves lock-in."

### What exactly does the adoption model show?

Among coded facilities first observed without generation, transition into generation is concentrated among younger and larger plants. Old small plants rarely make that transition in the panel.

### What exactly does the 0.1499 ratio show?

It shows that efficiency moves much more across plants than within the same plant over time. Operations matter, but they usually do not erase the larger age- and scale-linked gaps.

---

## Tier 2

### Did you prove replacement?

No. The pathway audit shows reset/rebuild-like events are the largest observed bucket in this panel, but it does not cleanly distinguish replacement, new build, and major refurbishment inside that bucket.

### So can retrofit still matter?

Yes. The audit contains 38 continuity-type events consistent with in-place upgrading. The claim is comparative, not absolute: retrofit exists, but it is not the largest observed pattern in this panel.

### Are you saying operations do not matter?

No. Utilization is strongly positive. The point is that operational changes help, but they do not appear large enough to erase the bigger cross-facility gaps on their own.

### Why use logit rather than LPM?

Because the event is rare and discrete-time, but the main specification is a lagged logit hazard with average marginal effects in percentage points. The same sign pattern survives lagged cloglog and lagged LPM robustness checks.

### What is the weakest part of the data?

The panel does not directly observe capital-history mechanisms like retrofit investments, and heating value is an administrative estimate rather than a clean engineering measure.

---

## Tier 3

### Is the policy section too broad for the evidence?

Not in the revised version. The policy language is tied to the two-part architecture and presented as a hierarchy, not an exclusive mechanism claim.

### Is the 4.6 Mt-CO2 figure a full climate result?

No. It is a gross avoided-emissions upper bound based on displaced grid electricity, not a full life-cycle estimate.

### What is the single biggest remaining limitation?

The thesis still cannot directly separate replacement, new build, and major refurbishment inside the reset/rebuild-like bucket, because the panel is not a capital-history dataset.

---

## Closing lines

### Cleanest one-sentence contribution

Japan's incineration transition is empirically two-part: observed entry into generation is concentrated among younger and larger facilities, while conditional generator performance is strongly shaped by age, scale, and bounded within-facility responsiveness.

### Safest one-sentence limitation

This thesis provides disciplined observational evidence, not a single-mechanism causal identification design.

### Strongest one-sentence policy implication

Japan's biggest fleet-wide gains are more likely to come from capital-side modernization and regional consolidation than from operating-side fine-tuning alone.

---

## Hostile bridges

Use these when an answer starts to drift:

- `The narrow defended claim is...`
- `What the panel directly shows is...`
- `What it does not show on its own is...`
- `So the calibrated conclusion is...`
- `That is why the thesis is framed as observational and two-part.`
