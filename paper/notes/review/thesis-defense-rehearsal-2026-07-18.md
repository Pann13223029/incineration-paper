# Thesis Defense Rehearsal

Status: current professor-facing graduation thesis, 18 July 2026.

This is a preparation aid, not actual supervisor or examiner feedback. It is
synchronized to the five-parameter primary entry model and the current
professor-facing thesis.

## One-Sentence Thesis

Electricity recovery in Japan's municipal-incineration fleet looks materially
different when measured as facility coverage, first reported entry, and
installed generator design versus annual use; this thesis reconstructs those
three margins without turning administrative associations into causal claims.

## Sixty-Second Opening

The usual facility count gives an incomplete picture of electricity recovery.
In FY2024, 41.1% of retained records reported installed electrical capacity, but
positive-output facilities handled 80.1% of recorded throughput and installed-
capacity facilities represented 70.5% of processing design capacity. The
all-record installed-capacity share rose 19.50 percentage points since FY2005,
but only 2.19 points among 732 lineages observed at both endpoints. First
reported capacity entry was rare and positively associated with processing
scale, although the model does not identify a physical retrofit or causal
mechanism. Among operating generators, older reported start-year cohorts had
much smaller adjusted installed kW but not uniformly lower capacity factors.
The thesis contribution is therefore a three-margin measurement architecture:
separate counts from covered activity, administrative entry from physical
projects, and installed design from annual use.

## Main Defense Attacks And Answers

### 1. Is this one thesis or three unrelated analyses?

It is one measurement argument applied at three sequential margins. RQ1 defines
fleet coverage, RQ2 studies first reported entry among observed non-generators,
and RQ3 examines design and annual use only within the generating segment. A
result from one population is not allowed to answer a question belonging to
another.

### 2. Is it not obvious that larger facilities are more likely to generate?

The direction is intuitive; the evidence was not established for a reconstructed
national risk set. The contribution is the quantified absolute rarity, the
support-aware gradient, and its stability across continuity, reporting-state,
functional-form, prefecture-influence, and event-influence checks. Scale remains
a descriptive profile, not a mechanism.

### 3. Why should the reconstructed lineages be trusted?

Official codes are missing in FY2010-FY2012 and have zero overlap between
FY2019 and FY2020. The resolver therefore combines normalized names,
municipalities, start years, scale, configuration, and available codes under
one-to-one assignment. It includes contradiction vetoes, duplicate collapse,
golden link/separation cases, uncertain-link exclusion, and permutation and
insertion invariance tests. These checks support administrative reconstruction,
not verified physical continuity. Independent clerical review remains open.

### 4. Why use Firth regression?

The primary model has only 35 events. Firth's penalized likelihood reduces
first-order small-sample bias and avoids infinite estimates under separation.
The predictor set is limited to five parameters, and 1,999 whole-lineage
bootstrap replications represent repeated observations. Firth and bootstrapping
do not remove confounding or create missing project information.

### 5. What does the 6.72 odds ratio mean?

It compares fitted first-entry odds at 300 and 100 t/day while retaining the
observed age, calendar, and elapsed-risk distribution. It does not mean that
enlarging a 100 t/day facility would multiply its entry odds. Because 300 t/day
is near the 99th percentile, the representative translation is the increase
from 0.68 to 3.29 entries per 1,000 facility-years across the support-rich
24-120 t/day range.

### 6. Why are throughput and design-capacity coverage defined differently?

Throughput coverage uses positive annual output because installed equipment does
not guarantee generation in that year. Design-capacity coverage uses positive
installed kW because it asks where nominal waste-processing capacity is located
relative to installed generation equipment. The thesis also reports a matched
two-by-two facility matrix so numerator-state and denominator effects are not
confused.

### 7. Is the RQ3 decomposition only a mathematical identity?

The exact component sum is algebra, not independent evidence. The empirical
evidence comes first from separate adjusted models of raw installed kW and
annual electrical capacity factor. The identity then prevents gross MWh/t from
being misread as a single operating-efficiency measure by showing how installed
sizing, annual capacity use, and waste loading combine.

### 8. Why allow capacity factors above 1.00?

The source is an annual administrative survey, so reporting periods and
denominators can be imperfectly aligned. The 1.20 bound permits moderate proxy
mismatch rather than treating 1.00 as error-free. Only 5 of 6,511 retained
capacity-factor rows exceed 1.00, and conservative-bound sensitivity preserves
the principal component conclusions.

### 9. Why not use facility fixed effects for the main cohort models?

Reported start-year cohort and generator sizing are predominantly between-asset
attributes, so facility fixed effects would remove the main estimand. The thesis
uses lineage-clustered uncertainty, year controls, lineage-equal weighting,
period splits, bound sensitivities, and within-episode models only for operating
components that vary meaningfully over time.

### 10. Did Fukushima or the feed-in tariff cause the observed changes?

The thesis does not identify either effect. Calendar controls prevent the scale
coefficient from absorbing a simple panel-time pattern, but facility-level policy
exposure and a credible comparison design are unavailable. A causal policy study
would require verified project timing, eligibility, finance, and comparison
units.

### 11. Are older facilities inefficient?

No. Reported facility start year is not a generator installation date. Older
cohorts have much smaller adjusted installed kW, but their annual capacity
factors are not uniformly lower. Gross MWh/t is a composite administrative
ratio, not thermodynamic, lifecycle, or economic efficiency.

### 12. What practical decision follows from the thesis?

Monitoring should report facility, throughput, and design-capacity coverage
together. Processing scale can prioritize further feasibility investigation but
cannot rank investments. Existing generators should be compared after separating
installed design from annual use. Project decisions still require cost, grid,
heat, outage, emissions, and waste-supply evidence.

## Answers That Fail The Defense

- "The model proves that larger plants adopt generation."
- "The reconstructed lineages are verified physical facilities."
- "The 6.72 odds ratio is the effect of increasing capacity."
- "Newer facilities are more efficient."
- "The accounting identity proves that sizing causes performance."
- "Fukushima or the feed-in tariff caused the observed trend."
- "The remaining 19.9% of throughput is recoverable potential."

## Evidence Anchors To Memorize

| Topic | Anchor |
|:--|:--|
| Administrative panel | 23,593 records; 1,690 lineages; 1,767 episodes |
| FY2024 coverage | 41.1% facility participation; 80.1% throughput; 70.5% design capacity |
| Endpoint composition | 19.50-point all-record rise; 2.19 points among 732 endpoint-common lineages |
| Entry model | 15,154 risk rows; 1,137 lineages; 35 events; five parameters |
| Support-rich risks | 0.68, 1.37, and 3.29 entries per 1,000 at 24, 60, and 120 t/day |
| Tail contrast | OR 6.72; 95% bootstrap interval 4.31-12.46; 300 t/day near 99th percentile |
| Generator frame | 6,511 rows; 493 lineages |
| Capacity-factor proxy exceptions | 5 retained rows above 1.00 under the 1.20 bound |
| Human validation | Blinded packet generated; independent review not completed |

## Remaining Actions

1. A second person must complete and adjudicate the blinded linkage packet by
   following the [human-review handoff](human-linkage-review-handoff.md).
2. The supervisor must decide whether Appendix A remains in the submitted thesis.
3. The supervisor or university must confirm the required AI-disclosure wording.
4. Rehearse the sixty-second opening and twelve answers without reading notes.
