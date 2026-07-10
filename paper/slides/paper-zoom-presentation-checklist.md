# Paper Zoom Presentation Checklist

Use this checklist to keep the presentation critical but still easy to follow. The goal is not to show every detail in the paper. The goal is to make the listener understand why the paper is more than the obvious claim that newer and larger plants have advantages.

## Core Rule

- [ ] Say the paper in one sentence: "The paper separates broad asset entry, active conversion, and generator performance."
- [ ] Keep the live presentation to slides 1-20.
- [ ] Assume no prior knowledge unless the audience clearly signals otherwise.
- [ ] Define key terms once: entry, MWh/t, bottleneck, fleet, robustness check, and causal claim.
- [ ] Do not explain every coefficient.
- [ ] Repeat the skeptical framing when needed: "Scale is robust, age depends on the candidate population, and entry does not guarantee top performance."
- [ ] Stop after slide 20 and ask for targeted feedback.

## One-Day-Before Checklist

- [ ] Open `paper/share/paper-zoom-briefing.pdf` and confirm it has 20 slides.
- [ ] Open `paper/slides/paper-zoom-script.md` on a second screen or print it.
- [ ] Practice once with a timer and stop at slide 20.
- [ ] Confirm slide 1 includes the formal paper title.
- [ ] Target 15-18 minutes for the main presentation.
- [ ] Mark any slide that takes more than 70 seconds and shorten the spoken explanation.
- [ ] Check that the data-source table, sample pipeline, method boxes, Figures 2-4, and main result cards are readable at Zoom screen-share size.
- [ ] Prepare one answer for each likely question: causality, broad versus active entry, replacement, data quality, old-plant improvement, why not one model, and why the code gap overlaps Fukushima.

## Live Delivery Checklist

- [ ] Start with purpose in the script, not on the slide: "This is a paper briefing and I want feedback on the main contribution."
- [ ] Translate jargon before using it heavily.
- [ ] Explain why the issue matters before showing methods.
- [ ] Say clearly that the paper is not trying to make age and scale sound surprising.
- [ ] Spend enough time on slides 5-9; these are the methodological credibility slides.
- [ ] Say the adoption numbers slowly on slide 10.
- [ ] Use slide 11 to explain why the result is not just common sense.
- [ ] Use slide 15 to show robustness without reading every test.
- [ ] Use slide 16 to show limitations without sounding apologetic.
- [ ] Stop at slide 20 and ask for feedback.

## Slide-By-Slide Checklist

| Slide | Must-say message | Do not do |
|:--|:--|:--|
| 1 | The talk title is plain language; the formal paper title is also shown. | Do not start with regression terms. |
| 2 | Incineration creates heat, but electricity recovery is uneven. | Do not debate all pros/cons of incineration. |
| 3 | The real question is which patterns survive across asset, active-plant, and generator frames. | Do not oversell obvious findings. |
| 4 | One average hides two margins; define entry, MWh/t, and bottleneck. | Do not use jargon without defining it. |
| 5 | The data are national facility-level administrative records with clear limits. | Do not imply retrofit contracts or lifecycle emissions are observed. |
| 6 | The sample pipeline creates two analysis frames for two questions. | Do not treat sample construction as boring. |
| 7 | Two samples are necessary because the outcomes differ. | Do not use one-model language. |
| 8 | The adoption method follows facilities still at risk and uses lagged predictors. | Do not forget pre-event timing. |
| 9 | Generator output is compared after entry using output intensity. | Do not claim causal effects. |
| 10 | Scale predicts entry in both risk sets; age attenuates in the active frame. | Do not universalize the broad age result. |
| 11 | Forty broad events follow zero or missing prior throughput. | Do not equate broad asset entry with active retrofit. |
| 12 | Entry pathway evidence supports modernization, not one mechanism. | Do not say replacement is the only pathway. |
| 13 | Generation status alone does not mean high performance. | Do not say old generators cannot improve. |
| 14 | Ranks persist across coded years, but persistence does not bound improvement. | Do not overexplain variance decomposition. |
| 15 | Robustness checks stress-test identifiers, model form, period, scale, outcome coding, and heating value. | Do not say robustness proves causality. |
| 16 | Data limitations are disclosed with counts and sensitivity logic. | Do not hide data caveats. |
| 17 | Entrants begin near the same-year distribution middle; the trajectory is selected. | Do not claim an entry treatment effect. |
| 18 | The contribution is the boundary across scale, age, and post-entry position. | Do not present common sense as novelty. |
| 19 | Future work should test mechanisms. | Do not pretend mechanisms are already tested. |
| 20 | Ask discussion questions. | Do not keep presenting after the ask. |

## Simple Q&A Answers

- [ ] Causality: "No, the paper identifies patterns and bottlenecks. It does not prove strict policy effects."
- [ ] Code gap/Fukushima: "FY2010-FY2012 official codes are missing, so the early/later coded windows are descriptive and cannot identify a Fukushima treatment effect."
- [ ] Replacement: "No, the pathway audit shows many reset/rebuild-like events, but also continuity upgrades and unresolved entries."
- [ ] Data quality: "The administrative data have duplicate-code, missing-code, and heating-value issues; sensitivity checks do not overturn the headline pattern."
- [ ] Old plants: "The paper does not say old active plants cannot convert. The age gradient attenuates when positive prior-year throughput is required."
- [ ] One model: "One model would mix asset entry, active conversion, and generator performance, so it would answer an unclear question."
- [ ] Contribution: "The contribution is robust scale selectivity, a frame-dependent age result, and a post-entry trajectory in one national panel."

## After-Meeting Checklist

- [ ] Write down whether the supervisor accepted the two-margin contribution and risk-set distinction.
- [ ] Record which limitation sounded most serious.
- [ ] Record which future-work direction sounded most publishable.
- [ ] Record whether the methodology explanation was clear or still too technical.
- [ ] Decide the next paper revision based on the strongest feedback, not every side comment.
