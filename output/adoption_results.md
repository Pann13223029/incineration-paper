# First Reported Installed-Generation-Capacity Entry

The event is the first stable-lineage observation with positive installed electrical-generation capacity after an observed non-generating history. It is not automatically a retrofit, first operation, or new physical site.

## Stable Administrative-Lineage Risk Set

- Descriptive risk set: 16,519 rows across 1,223 lineages with 55 observed events.
- Exact-year model: 15,154 rows across 1,137 lineages with 35 events.
- Prior-operation model: 13,072 rows, 1,019 lineages, and 33 events.
- Same-asset-episode continuity sensitivity: 15,095 rows, 1,135 lineages, and 24 events.
- Identity-certain-lineage sensitivity: 15,107 rows, 1,130 lineages, and 35 events.
- Exact events without positive prior-year throughput: 2.

## Bias-Reduced Hazard Results

Models use Firth bias reduction, log waste-processing design capacity, four calendar eras, flexible duration bands, and 499 stable-lineage cluster bootstrap replications. Coefficients are log-odds; waste-processing capacity is transformed as log(1 + t/day / 100). Bootstrap percentile intervals and joint age tests use complete-lineage resampling; standard errors and p-values in the machine-readable coefficient table are explicitly labelled model-based.

| model                                     | term                    |   coefficient |   standard_error_model_based |   bootstrap_ci_low |   bootstrap_ci_high |   odds_ratio |   events |
|:------------------------------------------|:------------------------|--------------:|-----------------------------:|-------------------:|--------------------:|-------------:|---------:|
| Broad exact-year risk frame               | age_10-19 yrs           |       -1.2541 |                       0.6202 |            -2.4232 |              0.6642 |       0.2853 |       35 |
| Broad exact-year risk frame               | age_20-29 yrs           |       -1.1274 |                       0.5946 |            -2.1767 |              0.8694 |       0.3239 |       35 |
| Broad exact-year risk frame               | age_30+ yrs             |       -1.3091 |                       0.6715 |            -2.7015 |              0.6446 |       0.2701 |       35 |
| Broad exact-year risk frame               | log_processing_capacity |        2.6158 |                       0.4054 |             1.9707 |              3.4872 |      13.6779 |       35 |
| Prior-operation risk frame                | age_10-19 yrs           |       -1.3358 |                       0.6206 |            -2.4445 |              0.3110 |       0.2630 |       33 |
| Prior-operation risk frame                | age_20-29 yrs           |       -1.3892 |                       0.6119 |            -2.5051 |              0.2434 |       0.2493 |       33 |
| Prior-operation risk frame                | age_30+ yrs             |       -1.3096 |                       0.6774 |            -2.5941 |              0.4230 |       0.2699 |       33 |
| Prior-operation risk frame                | log_processing_capacity |        2.6444 |                       0.4465 |             1.9087 |              3.7149 |      14.0756 |       33 |
| Same-asset-episode continuity sensitivity | age_10-19 yrs           |       -1.6932 |                       0.6486 |            -3.1183 |             -0.0298 |       0.1839 |       24 |
| Same-asset-episode continuity sensitivity | age_20-29 yrs           |       -1.6656 |                       0.6271 |            -2.6437 |              0.1727 |       0.1891 |       24 |
| Same-asset-episode continuity sensitivity | age_30+ yrs             |       -2.6005 |                       0.7965 |            -4.5943 |             -0.6761 |       0.0742 |       24 |
| Same-asset-episode continuity sensitivity | log_processing_capacity |        2.7146 |                       0.5062 |             2.0411 |              3.6682 |      15.0987 |       24 |
| Identity-certain-lineage sensitivity      | age_10-19 yrs           |       -1.2541 |                       0.6199 |            -2.5990 |              0.4523 |       0.2853 |       35 |
| Identity-certain-lineage sensitivity      | age_20-29 yrs           |       -1.1270 |                       0.5946 |            -2.1997 |              0.7766 |       0.3240 |       35 |
| Identity-certain-lineage sensitivity      | age_30+ yrs             |       -1.3110 |                       0.6712 |            -2.6679 |              0.5910 |       0.2695 |       35 |
| Identity-certain-lineage sensitivity      | log_processing_capacity |        2.6235 |                       0.4056 |             1.9097 |              3.5373 |      13.7843 |       35 |

- Broad-frame lineage-bootstrap-covariance joint age test: chi-square=3.08, df=3, p=0.3800.
- Prior-operation lineage-bootstrap-covariance joint age test: chi-square=4.81, df=3, p=0.1863.
- Same-episode continuity lineage-bootstrap-covariance joint age test: chi-square=7.78, df=3, p=0.0508.
- Identity-certain lineage-bootstrap-covariance joint age test: chi-square=3.24, df=3, p=0.3566.
The prior-operation frame is a nested sensitivity, not an independent comparison group. The former two-event interaction contrast is not used as an equality or equivalence test.
- Odds ratio comparing 300 with 100 t/day: broad 6.13; prior operation 6.25.

## Observed Exact-Year Rates

### By prior reported age band

| lag_age_band   |   risk_rows |   events |   mean_processing_capacity_t_day |   event_rate_pct |
|:---------------|------------:|---------:|---------------------------------:|-----------------:|
| 0-9 yrs        |        1648 |        4 |                           47.425 |            0.243 |
| 10-19 yrs      |        5129 |        6 |                           65.877 |            0.117 |
| 20-29 yrs      |        5521 |       14 |                           87.203 |            0.254 |
| 30+ yrs        |        2856 |       11 |                          115.797 |            0.385 |

### By waste-processing design-capacity quartile

| capacity_quartile   |   risk_rows |   events |   mean_processing_capacity_t_day |   event_rate_pct |
|:--------------------|------------:|---------:|---------------------------------:|-----------------:|
| Q1 smallest         |        3854 |        1 |                           10.952 |            0.026 |
| Q2                  |        4175 |        2 |                           41.514 |            0.048 |
| Q3                  |        3702 |        9 |                           92.697 |            0.243 |
| Q4 largest          |        3423 |       23 |                          195.591 |            0.672 |

## Transition Pathways

| pathway_category                  |   events |
|:----------------------------------|---------:|
| Continuity-lineage entry          |       35 |
| Forward-dated / placeholder entry |        9 |
| Rebuild/replacement-like entry    |       11 |

`Continuity-lineage entry` requires an exact adjacent-year observation in the same administrative lineage and asset episode. `Rebuild/replacement-like` records an asset-episode or start-year reset; neither category proves a causal mechanism.

## Post-Entry Bridge

The bridge uses 55 exact-year events only. 47 report positive output in the event year, and 51 report positive output by the following observed fiscal year. Pathway-stratified first-complete-year component results are stored in `post_adoption_trajectories.csv`.

## Link Sensitivity

The complementary-log-log capacity coefficient is 2.6091; the conventional logit coefficient is 2.6258. These are specification checks, not additional hypotheses.

Administrative disappearance is not modeled because closure, recoding, consolidation, and reporting change cannot be separated without external facility histories.
