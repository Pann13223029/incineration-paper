# Supplementary Material

## S1. Purpose, Scope, And Reading Rules

This supplement documents the parts of the analysis that require more detail than
the main paper can carry: raw-file provenance, reconstruction of stable
administrative lineages, event-risk-set construction, sparse-event estimation,
engineering-variable definitions, robustness checks, and reproducibility and
publication-integrity controls.

The unit tracked over time is an audited administrative facility lineage. It is
not assumed to prove continuous ownership, an unchanged physical plant, or an
unchanged equipment configuration. A nested asset-episode identifier records
large reported configuration resets within a lineage.

The following interpretation rules apply throughout:

1. The entry event is the first observed report of positive installed
   electrical-generation capacity after an observed non-generating history. It
   is not, by itself, proof of the installation date or a specific physical
   intervention.
2. Reported start year is an administrative design-vintage marker, not a verified
   turbine or boiler commissioning date.
3. Gross electricity generated per tonne is an output-intensity ratio. It is not
   net export, useful heat recovery, R1 performance, lifecycle benefit, or a
   stand-alone thermodynamic measure.
4. Estimated coefficients are observational associations. The design does not
   identify causal effects of age, plant size, operating choices, or equipment
   changes.
5. Official facility codes are annual source fields and matching evidence. They
   are not assumed to identify the same lineage across years.

### S1.1 Abbreviations and notation

| Term | Meaning |
|:--|:--|
| FY | Japanese fiscal year |
| MOE | Ministry of the Environment Japan |
| MWh | Megawatt-hour |
| kW | Kilowatt of installed electrical-generation capacity |
| t/day | Tonnes of waste-processing design capacity per day |
| Firth logit | Logistic regression estimated with Jeffreys-prior bias reduction |
| WLS | Weighted least squares |
| FE | Fixed effects |
| CI | Confidence interval |
| SHA-256 | Cryptographic file digest used to identify an exact file byte stream |

## S2. Raw Data Provenance And Schema Reconstruction

### S2.1 Source coverage

The source archive contains 20 MOE General Waste Treatment Survey incineration
workbooks covering FY2005-FY2024. All 20 configured files are present. Their
combined size is 15,158,836 bytes, and all 20 have distinct SHA-256 digests. The
data source and survey context are described by the Ministry of the Environment
Japan (2026) and e-Stat (n.d.).

The provenance layer produces two machine-readable artifacts:

- `output/raw_data_manifest.csv` records fiscal year, configured MOE URL,
  filename, byte size, full SHA-256 digest, the explicit marker that checkout
  mtime is unavailable/not persisted, last Git commit time, timestamp basis,
  parser sheet, and detected data-start row for every workbook.
- `output/raw_workbook_schema_map.csv` records the standardized field, matched
  Japanese header text, sheet name, header coordinates, and parser-selected
  column for every year-field combination.

The schema map contains 19 standardized field slots for each of 20 years, or 380
year-field mappings. The parser reads the first workbook sheet and searches rows
0-5 for the first matching header keyword. The detected data-start row is Excel
row 3 for FY2005-FY2006 and row 7 for FY2007-FY2024. Seventeen fields are found in
FY2005-FY2017; the two unavailable fields are electricity sold and sales revenue.
All 19 fields are found from FY2018 onward.

### S2.2 Provenance boundary

The original retrieval timestamp is unavailable because the downloader did not
record it. Checkout filesystem modification time (mtime) is also
unavailable/not persisted because it is volatile across checkouts. The last Git
commit time for each workbook records repository history, not retrieval or
acquisition time, and the manifest labels that basis explicitly. The configured
URLs are reconstructed from the checked-in downloader configuration; the
provenance stage does not claim that each URL was revalidated when the manifest
was generated.

SHA-256 and byte size identify the exact files in the repository. They do not
establish publisher-side version history, HTTP response headers, or custody
before the files entered the workspace. These limits are part of the provenance
record rather than being filled with inferred dates.

## S3. Stable Administrative-Lineage Reconstruction

### S3.1 Exact-record collapse

The parsed source contains 23,599 rows. Before any cross-year matching, every
source row is canonicalized and hashed across all parsed source columns. The
resulting SHA-256-based `source_record_id` is independent of dataframe row order.
Six exact duplicate rows collapse to one retained record each, leaving 23,593
unique administrative records.

Duplicate collapse occurs before matching so repeated copies of the same source
record cannot be assigned to separate lineages. Source multiplicity remains in
the crosswalk for audit. The final analytical grain contains zero duplicate
stable-lineage-year observations.

### S3.2 Deterministic matching algorithm

The resolver applies the following sequence:

1. Normalize identifiers and text. Japanese text is Unicode NFKC-normalized,
   lowercased where applicable, stripped of spacing and punctuation variants,
   and compared within prefecture.
2. Resolve adjacent fiscal years first. Only records still unmatched are
   considered against two-, three-, and four-year gaps. This prevents a stale
   history from defeating an equally plausible immediately preceding record.
3. Construct candidate scores from exact or fuzzy facility name, municipality,
   official code, reported start year, waste-processing capacity, furnace count,
   and facility type. Exact name carries the largest positive weight. An official
   code contributes supporting weight but cannot decide a link by itself.
4. Apply a contradiction veto. A shared code is rejected when facility names are
   strongly inconsistent without corroborating configuration evidence, or when
   municipality and name evidence jointly contradict the proposed link.
5. Solve the eligible candidates as a one-to-one maximum-score assignment within
   prefecture using the Hungarian algorithm. The minimum accepted score is 90.
6. Reject a fuzzy candidate whose selected score is less than three points above
   its best local alternative unless an exact name or same-code key supplies
   strong evidence.
7. Seed every unmatched record as a new lineage. Its `stable_site_id` is a hash of
   the canonical seed-record fingerprint, not a row number. This makes IDs stable
   to source-row permutation and unrelated row insertion.

Candidate links below the minimum score are removed before global assignment.
For every remaining edge, the resolver computes both the current row's margin
over its next-best prior record and the prior record's margin over its next-best
current row. Weak ambiguous edges are removed before assignment unless an exact
name or official code provides a strong evidence override. Sixteen accepted
links across 14 lineages have a two-sided margin below three points; all 16 have
such strong evidence and are exposed in the identity audit. Exposure does not
certify or invalidate a link. It identifies the records where conclusions
should be least dependent on automated linkage.

### S3.3 Asset episodes

A stable lineage can contain more than one reported asset episode. A new episode
starts when adjacent observations show at least one of the following:

- an absolute reported start-year shift of at least three years;
- a mature-to-new reported-age reset, from at least 10 years to at most 3 years;
- a waste-processing capacity shift of at least 60% combined with a furnace,
  furnace-type, or facility-type change and a non-matching facility name.

The start-year rule is symmetric, so both forward and backward resets are
detected. Asset episodes prevent a large configuration discontinuity from being
silently treated as unchanged equipment while retaining the broader site-level
administrative lineage.

### S3.4 Identifier gaps and regime change

The resolved data contain 1,690 stable administrative lineages and 1,767 asset
episodes. No stable-lineage-year is duplicated, and the longest lineage contains
20 observed fiscal years.

Official facility codes are absent from all 3,716 records in FY2010-FY2012. The
FY2019-FY2020 transition is a complete code-regime change: the adjacent-year
official-code overlap is 0, whereas the audited lineage overlap is 1,064. The
2019-2020 match restores 97.3% of FY2019 lineages. These breaks are why event
lags, repeated-observation covariance, and pathway continuity use the audited
lineage identifier.

### S3.5 Executable identity guardrails

The identity stage fails rather than silently continuing when its invariants are
violated. Current checks include:

- three golden same-lineage checks, including known difficult FY2019-FY2020
  records;
- three golden separation checks for known code reuse or unrelated records;
- an asset-episode reset check for a known configuration discontinuity;
- row-permutation invariance across six difficult or duplicate-bearing
  prefectures;
- unrelated-row insertion invariance across the same six prefectures;
- zero duplicate stable-lineage-years;
- no history longer than the 20-year source window;
- at least 900 restored FY2019-FY2020 lineage links;
- zero accepted sub-threshold links;
- zero accepted weak ambiguous links;
- exact one-row exposure of every accepted uncertain link, with its two-sided
  margins and competing records.

These tests establish deterministic behavior and catch known failure modes. They
do not convert administrative record linkage into proof of physical identity.

## S4. Analytical Frames And Sample Construction

### S4.1 Fleet frame

The full-fleet frame retains all 23,593 unique administrative records. For
FY2024, 417 of 1,014 records report installed electrical-generation capacity,
giving facility participation of 41.1%. Facilities with positive gross output
handle 80.1% of recorded waste throughput, while facilities with installed
capacity account for 70.5% of waste-processing design capacity. Thus, a facility
count is not interpreted as a waste-volume share.

For engineering-valid generating records, the exact annual decomposition is:

`fleet gross MWh / total tonnes = valid generator-throughput share x conditional valid generator gross MWh/t`.

In FY2024, engineering-valid generators handle 79.7% of throughput, their
conditional gross generation intensity is 0.425 MWh/t, and the corresponding
fleet-wide gross generation intensity is 0.338 MWh per total tonne.

### S4.2 First reported installed-capacity entry

The descriptive event is the first observed positive installed
electrical-generation capacity in a lineage that was first observed without such
capacity. Lineages already generating in their first observed year are treated as
left-censored and do not enter the risk set. Once a lineage records the event, it
leaves the risk set.

| Frame | Rows | Stable lineages | Events | Purpose |
|:--|--:|--:|--:|:--|
| Descriptive risk set | 16,519 | 1,223 | 55 | Enumerate all observed first reports |
| Broad exact-year model | 15,154 | 1,137 | 35 | Require an adjacent-year lag in the same administrative lineage and complete lagged covariates |
| Prior-operation model | 13,072 | 1,019 | 33 | Nested sensitivity additionally requiring positive prior-year waste throughput |
| Same-asset-episode continuity | 15,095 | 1,135 | 24 | Exclude transitions across an inferred asset-episode boundary |
| Identity-certain lineages | 15,107 | 1,130 | 35 | Exclude every lineage containing an accepted uncertain link |

The exact-year model drops each lineage's first at-risk row because no lagged
predictor exists, excludes non-adjacent lags, and requires non-missing lagged age
band and waste-processing capacity. Two exact-year model events have zero or
missing prior-year throughput; this produces the 35-to-33 event difference.
The broad model permits a change in inferred asset episode because its estimand
is administrative-lineage entry. The continuity sensitivity excludes 59 such
rows, including 11 events. The identity-certain sensitivity removes whole
lineages rather than individual uncertain years; no modeled event is lost.

The two occurrences of the number 35 have different meanings and should not be
conflated. There are 35 complete-covariate exact-year model events. Separately,
the pathway audit classifies 35 of all 55 descriptive events as continuity-lineage
entries.

### S4.3 Event pathway audit

| Pathway label | Events | Administrative rule |
|:--|--:|:--|
| Continuity-lineage entry | 35 | Same lineage and asset episode in adjacent years, with no reset signal |
| Forward-dated / placeholder entry | 9 | Reported start year is in the future or the name signals a planned/new record |
| Rebuild/replacement-like entry | 11 | Asset episode, reported start year, or mature-to-new age resets at entry |

These labels organize source-record patterns. They are not verified engineering
histories and do not establish the mechanism that produced a change in reported
capacity.

## S5. Sparse-Event Model

### S5.1 Discrete-time risk specification

For lineage `i` in fiscal year `t`, let `Y_it=1` denote the first observed report
of positive installed electrical-generation capacity while the lineage remains
at risk. The model is:

```text
logit Pr(Y_it = 1 | at risk) = alpha
                              + sum_a beta_a AgeBand_i,t-1,a
                              + beta_C log(1 + C_i,t-1 / 100)
                              + calendar-era indicators
                              + elapsed-risk-duration indicators.
```

`C_i,t-1` is lagged waste-processing design capacity in t/day. The reference age
band is 0-9 years; comparison bands are 10-19, 20-29, and 30+ years. Calendar
eras are FY2005-FY2009, FY2010-FY2014, FY2015-FY2019, and FY2020-FY2024. Elapsed
risk duration is grouped as 1-4, 5-9, 10-14, and 15+ fiscal years. The setup
follows the discrete-time event-history logic described by Allison (1982) and
Beck et al. (1998), while the present implementation uses bias reduction because
events are sparse. The Jeffreys-prior correction follows Firth (1993), and its
use where sparse outcomes can produce separation or unstable maximum-likelihood
estimates follows the rationale in Heinze and Schemper (2002).

### S5.2 Firth bias reduction and uncertainty

The primary estimator maximizes the Jeffreys-prior penalized log likelihood:

```text
l_F(beta) = l(beta) + 0.5 log |I(beta)|,
```

where `l(beta)` is the ordinary binomial log likelihood and `I(beta)` is the
expected information matrix. Iteration uses the adjusted score, step limiting,
and step halving. Fits fail on non-finite information, divergent coefficients,
or an unusable solution rather than silently returning a result. This is the
bias-reduction method introduced by Firth (1993); in the present sparse-event
setting it also guards against the separation problem discussed by Heinze and
Schemper (2002).

The machine-readable coefficient table reports model-based standard errors,
confidence intervals, and term-level *p*-values under explicit labels. Primary
repeated-observation uncertainty uses 499 deterministic stable-lineage
cluster-bootstrap replications. Entire lineage histories are resampled with
replacement, preserving within-lineage dependence. Every replication must
converge and return all focal coefficients. Percentile intervals come from the
coefficient distributions, while each joint age test uses the covariance of the
three age coefficients across the same 499 replications.

### S5.3 Main entry estimates

| Model | Term | Coefficient | Bootstrap 95% interval | Events |
|:--|:--|--:|--:|--:|
| Broad exact-year | Age 10-19 years | -1.2541 | [-2.4232, 0.6642] | 35 |
| Broad exact-year | Age 20-29 years | -1.1274 | [-2.1767, 0.8694] | 35 |
| Broad exact-year | Age 30+ years | -1.3091 | [-2.7015, 0.6446] | 35 |
| Broad exact-year | Log processing capacity | 2.6158 | [1.9707, 3.4872] | 35 |
| Prior-operation | Age 10-19 years | -1.3358 | [-2.4445, 0.3110] | 33 |
| Prior-operation | Age 20-29 years | -1.3892 | [-2.5051, 0.2434] | 33 |
| Prior-operation | Age 30+ years | -1.3096 | [-2.5941, 0.4230] | 33 |
| Prior-operation | Log processing capacity | 2.6444 | [1.9087, 3.7149] | 33 |
| Same-episode continuity | Age 10-19 years | -1.6932 | [-3.1183, -0.0298] | 24 |
| Same-episode continuity | Age 20-29 years | -1.6656 | [-2.6437, 0.1727] | 24 |
| Same-episode continuity | Age 30+ years | -2.6005 | [-4.5943, -0.6761] | 24 |
| Same-episode continuity | Log processing capacity | 2.7146 | [2.0411, 3.6682] | 24 |
| Identity-certain | Age 10-19 years | -1.2541 | [-2.5990, 0.4523] | 35 |
| Identity-certain | Age 20-29 years | -1.1270 | [-2.1997, 0.7766] | 35 |
| Identity-certain | Age 30+ years | -1.3110 | [-2.6679, 0.5910] | 35 |
| Identity-certain | Log processing capacity | 2.6235 | [1.9097, 3.5373] | 35 |

Because the age specification is a three-coefficient family, the joint
age-band tests below are the primary inferential summary. The individual
percentile intervals are retained as stability diagnostics and are not
interpreted term by term.

The broad-frame joint age test is `chi-square=3.08`, 3 df, `p=0.3800`; the
prior-operation joint age test is `chi-square=4.81`, 3 df, `p=0.1863`; the
same-episode continuity joint age test is `chi-square=7.78`, 3 df, `p=0.0508`;
and the identity-certain joint age test is `chi-square=3.24`, 3 df, `p=0.3566`.
All four use lineage-bootstrap coefficient covariance. The same-episode
fitted-model covariance gives
`p=0.0099`, demonstrating that its age inference is sensitive to both the
continuity rule and within-lineage dependence. The evidence therefore does not
support a robust general independent age result.

Waste-processing scale is the stable entry correlate. The model-implied odds
ratio comparing 300 with 100 t/day is 6.13 in the exact-year frame and 6.25 in
the prior-operation frame. These are conditional odds contrasts, not causal
effects of enlarging a facility.

### S5.4 Why the frames are sensitivities, not group comparisons

The prior-operation frame is nested inside the broad frame, and only two broad
events do not follow positive prior-year throughput. A pooled interaction based
on that two-event contrast would not provide a defensible equality or
equivalence test. It is therefore not used. Instead, the four complete Firth
fits answer transparent sensitivity questions: whether prior operation,
same-episode continuity, or identity certainty changes the broad pattern.

As link-function checks, the processing-capacity coefficient is 2.6091 under a
complementary log-log model and 2.6258 under conventional logistic regression,
close to the broad Firth estimate of 2.6158.

## S6. Engineering Components And Accounting Identity

### S6.1 Variable definitions

For a generating lineage-year, define:

- `G`: gross electricity generated during the fiscal year, MWh;
- `T`: recorded waste throughput during the fiscal year, tonnes;
- `K`: installed electrical-generation capacity, kW;
- `C_w`: waste-processing design capacity, t/day;
- `U = T / (365 C_w)`: annual waste-processing utilization;
- `D = K / C_w`: generator design intensity, kW per t/day;
- `F = G / (8.76 K)`: electrical capacity factor, where 8.76 converts one kW
  operated for 8,760 hours to MWh/year;
- `I = G / T`: gross generation intensity, MWh/t.

The exact accounting identity is:

```text
G / T = [K / C_w] x [G / (K x 8.76)] x [8.76 / (365 U)]
      = D x F x 8.76 / (365 U).
```

The identity shows why `G/T` cannot be interpreted independently of installed
generator sizing, electrical capacity factor, and waste loading. It is an
algebraic decomposition, not a causal model.

### S6.2 Operating and engineering-valid samples

The operating-generator frame requires reported installed generation, positive
annual waste throughput, and positive gross electricity output. It contains
6,660 lineage-years. Records are not clipped into the primary model. Instead,
predeclared bounds are applied to the raw variables:

| Variable | Main lower bound | Main upper bound |
|:--|--:|--:|
| Gross generation intensity, MWh/t | 0.010 | 0.800 |
| Electrical capacity factor | 0.020 | 1.200 |
| Waste-processing utilization | 0.020 | 1.200 |
| Generator design intensity, kW per t/day | 0.100 | 100.000 |

Reported age must also be non-missing and non-negative. Negative reported ages
are converted to missing, not set to zero. Of 6,660 operating observations, 149
fail at least one primary engineering check, leaving 6,511 observations across
493 stable lineages.

Reported heating value of 3-25 MJ/kg is used only as a plausibility field. It is
not an inclusion condition for the primary component models. Among operating
records, 5,937 are in that range, 106 have missing heating value, and the
remainder fall outside the plausibility range.

### S6.3 Component models

Three related models are estimated with fiscal-year indicators, reported
start-year cohort indicators, coarse furnace/facility configuration controls,
and standard errors clustered by stable lineage:

```text
log(D_it) = cohort_i + log(C_w,it) + configuration_it + fiscal_year_t + error_it

log(F_it) = cohort_i + log(C_w,it) + U_it
            + configuration_it + fiscal_year_t + error_it

log(G_it) = log(T_it) + log(K_it)
            + cohort_i + configuration_it + fiscal_year_t + error_it.
```

The 2010-or-later reported start-year cohort is the reference group.

| Outcome | Term | Coefficient | Clustered SE | p-value |
|:--|:--|--:|--:|--:|
| Log generator design intensity | Start before 1990 | -1.5647 | 0.0844 | <0.0001 |
| Log generator design intensity | Start 1990-1999 | -0.8827 | 0.0635 | <0.0001 |
| Log generator design intensity | Start 2000-2009 | -0.2674 | 0.0430 | <0.0001 |
| Log generator design intensity | Log processing capacity | 0.5320 | 0.0436 | <0.0001 |
| Log electrical capacity factor | Start before 1990 | 0.3020 | 0.0419 | <0.0001 |
| Log electrical capacity factor | Start 1990-1999 | 0.1985 | 0.0325 | <0.0001 |
| Log electrical capacity factor | Start 2000-2009 | 0.0149 | 0.0289 | 0.6060 |
| Log electrical capacity factor | Log processing capacity | -0.1160 | 0.0236 | <0.0001 |
| Log electrical capacity factor | Waste-processing utilization | 1.6951 | 0.1259 | <0.0001 |
| Log gross output | Log annual throughput | 0.6378 | 0.0521 | <0.0001 |
| Log gross output | Log installed electrical capacity | 0.5758 | 0.0379 | <0.0001 |

The pooled design-intensity model has `R-squared=0.5493`, the capacity-factor
model has `R-squared=0.3390`, and the direct gross-output model has
`R-squared=0.9139`. Cohort coefficients describe conditional administrative
patterns and should not be read as effects of calendar age.

### S6.4 Cohort medians

| Reported start-year cohort | Observations | Lineages | Median gross MWh/t | Median kW per t/day | Median capacity factor |
|:--|--:|--:|--:|--:|--:|
| Before 1990 | 869 | 77 | 0.145 | 5.333 | 0.619 |
| 1990-1999 | 2,051 | 123 | 0.283 | 10.833 | 0.625 |
| 2000-2009 | 2,443 | 144 | 0.348 | 15.833 | 0.561 |
| 2010 or later | 1,148 | 162 | 0.475 | 20.588 | 0.664 |

Lineage counts are not additive because a lineage can contain more than one
reported asset episode or cohort classification over the observation window.

### S6.5 Generator-sizing diagnostic

A diagnostic reproduces a legacy-style regression of log gross generation
intensity and then adds log generator design intensity. Both specifications use
the same 5,806 engineering-valid observations with plausible reported heating
value and explicitly control heating value. This is a narrower, separate frame
from the 6,511 observations used in the primary component models. Before sizing
is added, the coefficients are -0.0349 for reported age, +0.1001 for
waste-processing capacity, and +0.6699 for waste-processing utilization (all
`p<0.001`). After sizing is included, the corresponding estimates are -0.0020
(`p=0.2977`), -0.0092 (`p=0.1991`), and -0.0995 (`p=0.2038`); the
generator-sizing coefficient is +0.7532 (`p<0.001`). Model `R-squared` changes
from 0.4737 to 0.8131.

This exercise demonstrates specification dependence. It is not a causal
mediation analysis and does not show that generator sizing is exogenous.

### S6.6 Adjacent-year persistence

Across 5,963 adjacent-year pairs from 470 stable lineages, pooled rank
correlations are 0.9609 for gross generation intensity, 0.9952 for generator
design intensity, and 0.8728 for electrical capacity factor. The very high
design-intensity persistence is consistent with its role as a slowly changing
installed attribute. Persistence is descriptive and does not validate all
reported measurements.

## S7. Robustness Ladder

The robustness design is ordered from data integrity to estimator and
specification dependence. No single check is treated as a substitute for the
others.

### S7.1 Data and identity checks

1. Recompute SHA-256 for all 20 raw workbooks and verify the schema-map grain.
2. Collapse exact source duplicates before matching.
3. Apply contradiction vetoes and adjacent-before-gap matching.
4. Expose all 16 accepted uncertain links with both assignment margins and
   competing records.
5. Require golden links, golden separations, row-permutation invariance, and
   unrelated-row insertion invariance.
6. Fail on duplicate stable-lineage-years or missing lineage and asset-episode
   IDs.

### S7.2 Entry-model checks

1. Compare the 55-event descriptive risk set with the 35-event complete-case
   exact-year frame.
2. Restrict further to the 33 events following positive prior-year throughput.
3. Use Firth bias reduction for sparse events.
4. Resample complete stable-lineage histories in 499 cluster-bootstrap
   replications.
5. Test age terms jointly rather than selecting individual coefficients.
6. Compare the broad, prior-operation, same-episode, and identity-certain
   frames without treating nested frames as independent groups.
7. Compare Firth, conventional logit, and complementary log-log scale
   coefficients.

### S7.3 Engineering-sample checks

| Specification | Rows | Lineages | Design `R-squared` | Capacity-factor `R-squared` | Gross-output `R-squared` |
|:--|--:|--:|--:|--:|--:|
| Main predeclared bounds | 6,511 | 493 | 0.5493 | 0.3390 | 0.9139 |
| FY2005-FY2014 | 2,882 | 356 | 0.5081 | 0.2967 | 0.9080 |
| FY2015-FY2024 | 3,629 | 444 | 0.5733 | 0.3795 | 0.9191 |
| Lineage-equal WLS | 6,511 | 493 | 0.5618 | 0.4595 | 0.9156 |
| Identity-certain lineages | 6,450 | 487 | 0.5475 | 0.3342 | 0.9133 |
| Conservative bounds | 6,432 | 490 | 0.5558 | 0.3364 | 0.9226 |
| Broad bounds | 6,535 | 496 | 0.5435 | 0.3297 | 0.9099 |

The conservative bounds are 0.02-0.70 MWh/t, 0.05-1.05 capacity factor,
0.05-1.10 waste utilization, and 0.25-75 kW per t/day. The broad bounds are
0.005-1.00 MWh/t, 0.01-1.50 capacity factor, 0.01-1.50 waste utilization, and
0.05-150 kW per t/day. These alternatives were fixed as sensitivity rules, not
selected from coefficient results.

### S7.4 Within-asset checks

Generator design intensity has little within-asset variation: its within/total
log-variance ratio is 0.0158, compared with 0.4260 for electrical capacity factor
and 0.0888 for gross generation intensity. Accordingly, within-asset models are
used for operational components, not to force identification of a mostly fixed
design attribute.

| Check | Outcome | Term | Coefficient | p-value |
|:--|:--|:--|--:|--:|
| Asset-episode FE | Log capacity factor | Waste utilization | 2.3813 | <0.0001 |
| Asset-episode FE | Log gross output | Log throughput | 1.1195 | <0.0001 |
| Asset-episode FE | Log gross output | Log installed kW | 0.6412 | 0.0002 |
| Adjacent-year first difference | Change in log capacity factor | Change in utilization | 2.6446 | <0.0001 |
| Adjacent-year first difference | Change in log gross output | Change in log throughput | 1.1406 | <0.0001 |
| Adjacent-year first difference | Change in log gross output | Change in log installed kW | 0.2082 | 0.0805 |

The within-asset checks absorb time-invariant asset-episode attributes, but
annual throughput, utilization, installed capacity, and output can still be
jointly determined. They remain operational descriptions rather than causal
intervention estimates.

## S8. Post-Entry Bridge And Trajectory Caveats

All 55 pathway-audited descriptive events have an adjacent prior-year lineage
record. Forty-seven report positive gross output in the event year, and 51 report
positive output by the following observed fiscal year. Component trajectories
require positive output and engineering-valid measurements, so their sample is
smaller: 37 event-year observations and 44 one-year observations.

At one year after entry, the descriptive pathway means are:

| Pathway | Valid observations | Mean gross MWh/t | Mean gross rank | Mean design rank | Mean capacity-factor rank |
|:--|--:|--:|--:|--:|--:|
| All exact-year entrants | 44 | 0.328 | 51.6% | 48.1% | 56.3% |
| Continuity-lineage entry | 27 | 0.260 | 40.2% | 36.8% | 53.8% |
| Forward-dated / placeholder entry | 6 | 0.422 | 64.7% | 65.7% | 50.5% |
| Rebuild/replacement-like entry | 11 | 0.442 | 72.5% | 66.1% | 65.5% |

These comparisons are descriptive. The source does not provide verified
intervention dates or uncertainty intervals for pathway labels. Small pathway
cells, right-censoring near FY2024, engineering-validity exclusions, and
conditioning on observed positive output all limit interpretation. A
continuity-lineage label does not prove unchanged machinery, and a reset-like label
does not prove a physical replacement.

## S9. Reproducibility And Evidence Trace

The supplement draws quantitative statements from generated artifacts rather
than manually transcribed private calculations. The primary evidence paths are:

| Topic | Generated evidence |
|:--|:--|
| Raw provenance | `output/raw_data_manifest.csv`; `output/raw_workbook_schema_map.csv`; `output/raw_data_provenance.md` |
| Lineage reconstruction | `data/processed/facility_identity_crosswalk.csv`; `output/facility_identity_audit.md`; `output/identifier_gap_audit.md` |
| Sample arithmetic | `output/sample_definition.md`; `output/data_quality_sensitivity.md` |
| Fleet decomposition | `output/fleet_decomposition.csv`; `output/fy2024_fleet_segments.csv`; `output/fleet_decomposition.md` |
| Entry model | `output/figure2_transition_effects.csv`; `output/adoption_bootstrap_coefficients.csv`; `output/adoption_results.md` |
| Pathways and follow-up | `output/adoption_pathway_audit.csv`; `output/post_adoption_bridge.csv`; `output/post_adoption_trajectories.csv` |
| Engineering components | `output/generator_component_results.csv`; `output/table2_generator_components_by_cohort.md`; `output/regression_results.md` |
| Robustness | `output/robustness_component_results.csv`; `output/robustness_results.md` |

Each analytical stage writes a JSON manifest under `output/manifests/` with its
inputs, outputs, software version, analysis configuration, and headline
metadata. These manifests support consistency checks but do not replace review
of source records, code, and assumptions.

## S10. Ethics, Data Availability, And Publication Integrity

### S10.1 Ethical scope

The study uses publicly released administrative facility data. It does not
involve human participants, animal subjects, or private personal data. The author
declares no known competing financial interests or personal relationships that
could have appeared to influence the work.

### S10.2 Data and code availability

The source workbooks can be obtained from the Ministry of the Environment and
e-Stat portals. Subject to source-file redistribution conditions, the submission
package will provide analysis code, machine-readable stage manifests, derived
tables, figure-generation scripts, and manuscript figures in a versioned
repository. The raw-file manifest provides full SHA-256 values so independently
obtained files can be compared byte for byte.

### S10.3 COPE-facing publication controls

The repository applies the following publication-integrity controls consistent
with the responsibilities emphasized in COPE guidance:

- the named human author retains responsibility for study design, analysis,
  interpretation, source verification, and the final text;
- automated tools are not listed as authors and cannot accept accountability;
- source provenance, transformations, exclusions, and analytical limitations are
  disclosed rather than reconstructed after submission;
- the manuscript and any later paper derived from the thesis must disclose
  overlap, avoid redundant publication, and cite the thesis or related output as
  required by the venue;
- citations must support the claim beside which they appear; no source is cited
  solely to increase apparent coverage;
- competing interests, funding, data availability, and material corrections must
  be disclosed in the submitted version;
- discovered material errors should trigger a corrected version and an editor
  notification when applicable, not silent replacement of the evidentiary
  record.

This checklist is a process commitment, not a claim of certification by COPE or
any journal.

### S10.4 Generative AI declaration

During preparation, the author used OpenAI Codex and Anthropic Claude for
language revision, manuscript organization, and assistance with code development
and review. The author executed the analyses, inspected source data and generated
outputs, independently checked reported results, reviewed and edited all
AI-assisted material, and takes full responsibility for the content. These tools
were not used as authors and did not replace author judgment or accountability.

## S11. Residual Limitations

1. Administrative lineage reconstruction is deterministic and audited but can
   still contain linkage error, especially among the 16 exposed uncertain
   assignments.
2. First reported positive capacity can lag physical installation or reflect a
   reporting correction.
3. Sparse events make age inference sensitive to continuity rules even with
   complete 499-replication lineage bootstraps.
4. Reported start year and configuration fields do not provide a complete
   engineering history.
5. Gross output is not net electricity export, useful heat, or lifecycle climate
   benefit.
6. Within-asset models reduce time-invariant confounding but do not resolve
   time-varying joint determination or measurement error.
7. Pathway comparisons condition on observed follow-up and valid component data;
   they are not controlled treatment comparisons.
8. The FY2005-FY2024 observation window cannot reveal histories before first
   observation or after FY2024.

## S12. Selected References

Allison, P. D. (1982). Discrete-time methods for the analysis of event histories.
*Sociological Methodology*, *13*, 61-98. https://doi.org/10.2307/270718

Beck, N., Katz, J. N., & Tucker, R. (1998). Taking time seriously:
Time-series-cross-section analysis with a binary dependent variable. *American
Journal of Political Science*, *42*(4), 1260-1288.
https://doi.org/10.2307/2991857

Firth, D. (1993). Bias reduction of maximum likelihood estimates. *Biometrika*,
*80*(1), 27-38. https://doi.org/10.1093/biomet/80.1.27

Heinze, G., & Schemper, M. (2002). A solution to the problem of separation in
logistic regression. *Statistics in Medicine*, *21*(16), 2409-2419.
https://doi.org/10.1002/sim.1047

e-Stat. (n.d.). *Nation Survey on the State of Discharge and Treatment of
Municipal Solid Waste* (Statistics code 00650101). Portal Site of Official
Statistics of Japan. https://www.e-stat.go.jp/en/statistics/00650101 (accessed
10 July 2026).

Ministry of the Environment Japan. (2026). *General Waste Treatment Survey
results: FY2024 municipal solid waste treatment survey*. Environmental
Management Bureau, Ministry of the Environment Japan.
https://www.env.go.jp/recycle/waste_tech/ippan/ (accessed 10 July 2026).

Wooldridge, J. M. (2010). *Econometric analysis of cross section and panel data*
(2nd ed.). MIT Press.
