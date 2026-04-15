---
marp: true
paginate: true
theme: default
size: 16:9
---

# Carbon Lock-in or Circular Transition?

## Heterogeneity in Japan's Waste Incineration Fleet and Net-Zero Compatibility

Pann Phetra  
Bachelor's Thesis Defense  
Ritsumeikan Asia Pacific University, 2026

**Core contribution:** Japan's incineration transition is empirically two-part:

- observed entry into power generation is an extensive-margin modernization problem
- conditional generator efficiency is an intensive-margin performance problem

<!--
Open with the architecture shift, not with policy.
If time is very short, use this slide to state the research question and jump straight to Slide 3.
-->

---

# 1. Research Question and Motivation

**Question**

What predicts observed transition into power generation among coded facilities first seen without generation, and conditional on power generation, what predicts energy recovery efficiency among power-generating incinerators?

**Why this matters**

- Japan still incinerates most municipal waste
- 59% of active FY2024 incinerators generate no electricity
- the literature often treats the fleet as one system, even though it is highly heterogeneous

![width:900px](../../docs/figures/readme_fleet_split.svg)

<!--
Say explicitly that the thesis is not about whether incineration is normatively ideal in the full waste hierarchy.
It is about heterogeneity inside the residual-waste tier that Japan still incinerates.
-->

---

# 2. One Dataset, Two Analytical Frames

**Administrative panel**

- `23,599` facility-year observations
- `2,948` facilities
- FY2005-FY2024

**Frame A: extensive margin**

- coded full-fleet frame: `19,827` observations
- adoption risk set: `13,770` facility-years, `2,035` facilities, `141` observed first-adoption events
- lagged model frame: `11,717` facility-years, `1,915` facilities, `140` retained events

**Frame B: intensive margin**

- canonical generator-efficiency frame: `5,683` facility-years, `1,016` facilities

**Why split the design**

- the adoption question is not the same as the conditional-efficiency question
- a generator-only sample cannot carry the whole fleet transition story

<!--
This is the key architecture slide.
If challenged on redesign, say the earlier version over-asked a selected sample to explain the whole fleet.
-->

---

# 3. Extensive-Margin Result: Transition Is Selective

**Main adoption hazard**

| Variable | Effect |
|:--|--:|
| Prior-year age `10-20` vs `0-10` | `-3.19` pp |
| Prior-year age `20-30` vs `0-10` | `-2.82` pp |
| Prior-year age `30+` vs `0-10` | `-2.26` pp |
| Prior-year capacity per `100 t/day` | `+0.39` pp |

**Other facts**

- `109` of `141` observed adoption events occur in FY2013-FY2019
- the coded panel does **not** show widespread late conversion among old small plants
- observed transition into generation is concentrated among facilities already younger and larger before the event year

**Interpretation**

Observed entry into generation is selective rather than diffuse.

<!--
If pressed on why cloglog: rare discrete-time event, stronger than the earlier LPM, same sign pattern as lagged logit and lagged LPM robustness.
-->

---

# 4. Pathway Audit: Capital-Side Modernization Is Prominent

**Event-level audit of `141` observed transitions**

| Category | Events | Share |
|:--|--:|--:|
| Reset / rebuild-like | `82` | `58.2%` |
| Continuity / in-place upgrade | `38` | `27.0%` |
| Forward-dated / placeholder | `20` | `14.2%` |
| Unresolved | `1` | `0.7%` |

**Rule basis**

- reset/rebuild-like requires observed `year_started` reset or mature-to-new age reset
- continuity-type transitions do not show that reset
- placeholder/forward-dated rows are left unresolved rather than forced into a stronger mechanism story

**Interpretation**

The largest observed pathway bucket is capital-reset-like, but the thesis does **not** claim that replacement is uniquely identified or that retrofit never happens.

<!--
This slide is the policy-calibration shield.
Use it whenever you sense the discussion drifting toward "so you proved replacement."
-->

---

# 5. Intensive-Margin Result: Bounded Responsiveness

**Main generator-efficiency relationships**

| Variable | Main-model range |
|:--|:--|
| Facility age | `-0.019` to `-0.035` |
| Design capacity | `+0.040` to `+0.103` |
| Capacity utilization | `+0.541` to `+0.779` |

**Deepest finding**

- within/total variance ratio: `0.1499`
- pre-Fukushima: `0.1795`
- post-Fukushima: `0.0956`

**Meaning**

- efficiency differs much more across facilities than within the same facility over time
- operating-side changes matter, but they appear too small to erase design- and vintage-based gaps once a facility is already in the generating regime

<!--
If asked whether this "proves lock-in," say no: it is descriptive evidence that is strongly consistent with bounded infrastructural responsiveness.
-->

---

# 6. Why Not Two-Way Fixed Effects?

**Reason 1: identification**

- facility age rises mechanically with year
- once year effects are included, age is poorly identified in a two-way FE design

**Reason 2: variance structure**

- within/total variation ratio of log-efficiency is only `0.1499`
- post-Fukushima it falls further to `0.0956`
- FE would lean on the smaller part of the signal while discarding the between-facility variation the thesis is trying to interpret

**Position**

- the thesis is observational, not a strict quasi-experimental identification design
- estimator choice follows the substantive question, not a ritual preference for FE

<!--
This slide is here because a quantitatively literate examiner is likely to ask this.
If time is short, keep it in appendix but be ready to jump to it immediately.
-->

---

# 7. What the Thesis Claims, and Does Not Claim

## Does claim

- Japan's incineration transition is empirically two-part
- observed transition into generation is selective
- conditional generator performance is strongly shaped by age, scale, and bounded within-facility responsiveness
- capital-side modernization likely matters more than operations alone for the weakest segment

## Does not claim

- strict causal proof
- replacement as the only modernization pathway
- full net climate accounting
- heat-recovery or district-heating evaluation

**Bottom line**

The revised thesis is stronger because it is narrower and better matched to the evidence.

<!--
This is the overclaim-defense slide.
Use it if challenged on causality, mechanism, or policy scope.
-->

---

# 8. Policy Takeaway and Closing

**What follows from the evidence**

- old and small facilities rarely record observed transition into generation
- among generators, vintage and scale gaps remain large
- reset/rebuild-like events are the largest observed pathway bucket

**Policy hierarchy**

1. capital-side modernization
2. retirement / major refurbishment
3. regional consolidation
4. routing and utilization as secondary levers

**Closing sentence**

Japan's incineration transition is happening, but it is selective and slower than a net-zero-compatible fleet transformation would require.

<!--
End on hierarchy, not absolutism.
The cleanest close is: operations matter, but they do not appear large enough to carry the whole transition by themselves.
-->

---

# Appendix A. Short Answer to the Hardest Methods Question

**Q: Why not two-way fixed effects?**

**A:**

- age is mechanically linked to year, so the main regressor is poorly identified in a two-way FE setup
- the within-to-total ratio is only `0.1499`, so FE would lean on the smaller part of the signal
- the thesis question is about how age, scale, and utilization structure heterogeneity, not about purging all between-facility information from the design

---

# Appendix B. Short Answer to the Hardest Scope Question

**Q: Did you prove that replacement is the dominant mechanism?**

**A:**

- no
- the pathway audit shows that reset/rebuild-like events are the largest observed bucket in this panel
- it does not cleanly distinguish replacement, new build, and major refurbishment inside that bucket
- the defended claim is therefore comparative and calibrated, not absolute

---

# Appendix C. Short Answer to the Hardest Theory Question

**Q: Did you prove lock-in?**

**A:**

- no, not causally
- the thesis shows that low within-facility variation, stable age/scale relationships, and bounded Fukushima response are strongly consistent with bounded infrastructural responsiveness
- that is the defended contribution

<!--
If you later want a polished visual deck, this markdown file is the source script.
The fastest path is to import it into Marp or copy slide-by-slide into your preferred presentation tool.
-->
