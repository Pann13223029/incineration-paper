# Major-Revision Scientific Results

## Lower-Degree-Of-Freedom Entry Model

The revision-frozen primary model uses five parameters including the intercept and 1,999 deterministic whole-lineage bootstrap replications per frame.

| Model                             |   odds_ratio_300_vs_100 |   bootstrap_ci_low |   bootstrap_ci_high |
|:----------------------------------|------------------------:|-------------------:|--------------------:|
| Broad reduced-DF frame            |                  6.7233 |             4.3122 |             12.4614 |
| Prior-operation reduced-DF frame  |                  7.0875 |             4.0842 |             13.7642 |
| Same-episode reduced-DF frame     |                  7.1510 |             4.4385 |             14.0512 |
| Identity-certain reduced-DF frame |                  6.7648 |             4.2296 |             12.2973 |

## Standardized Absolute Annual Entry Risk

| estimand                                                 |   capacity_t_day |   probability |   events_per_1000_facility_years |   bootstrap_ci_low |   bootstrap_ci_high |   bootstrap_ci_low_per_1000 |   bootstrap_ci_high_per_1000 | standardization_population   |   bootstrap_repetitions |
|:---------------------------------------------------------|-----------------:|--------------:|---------------------------------:|-------------------:|--------------------:|----------------------------:|-----------------------------:|:-----------------------------|------------------------:|
| standardized_annual_probability                          |        24.000000 |      0.000682 |                         0.682403 |           0.000349 |            0.001081 |                    0.348597 |                     1.081353 | Broad exact-year risk rows   |                    1999 |
| standardized_annual_probability                          |        60.000000 |      0.001374 |                         1.373724 |           0.000843 |            0.001966 |                    0.842539 |                     1.965731 | Broad exact-year risk rows   |                    1999 |
| standardized_annual_probability                          |       100.000000 |      0.002532 |                         2.532416 |           0.001728 |            0.003520 |                    1.727814 |                     3.519685 | Broad exact-year risk rows   |                    1999 |
| standardized_annual_probability                          |       120.000000 |      0.003287 |                         3.287146 |           0.002285 |            0.004574 |                    2.284535 |                     4.574058 | Broad exact-year risk rows   |                    1999 |
| standardized_annual_probability                          |       300.000000 |      0.016659 |                        16.658775 |           0.009515 |            0.029657 |                    9.514510 |                    29.657436 | Broad exact-year risk rows   |                    1999 |
| standardized_annual_probability_difference_300_minus_100 |       nan        |      0.014126 |                        14.126359 |           0.007382 |            0.026773 |                    7.382316 |                    26.772510 | Broad exact-year risk rows   |                    1999 |

Probabilities average predictions over the observed broad-frame age, calendar-year, and elapsed-risk distribution while setting processing capacity to the stated level for every risk row. They are descriptive model standardizations, not causal intervention effects.

## Entry-Capacity Support

| capacity_label              |   capacity_t_day |   empirical_percentile_pct |   risk_rows_at_or_above |   risk_share_at_or_above_pct |   modeled_events_at_or_above |   modeled_event_share_at_or_above_pct |   standardized_events_per_1000 |   bootstrap_ci_low_per_1000 |   bootstrap_ci_high_per_1000 |
|:----------------------------|-----------------:|---------------------------:|------------------------:|-----------------------------:|-----------------------------:|--------------------------------------:|-------------------------------:|----------------------------:|-----------------------------:|
| Risk-frame 25th percentile  |          24.0000 |                    25.4322 |                   11381 |                      75.1023 |                           35 |                              100.0000 |                         0.6824 |                      0.3486 |                       1.0814 |
| Risk-frame median           |          60.0000 |                    52.9827 |                    7690 |                      50.7457 |                           32 |                               91.4286 |                         1.3737 |                      0.8425 |                       1.9657 |
| Frozen contrast lower level |         100.0000 |                    70.8856 |                    4848 |                      31.9916 |                           26 |                               74.2857 |                         2.5324 |                      1.7278 |                       3.5197 |
| Risk-frame 75th percentile  |         120.0000 |                    77.4119 |                    4056 |                      26.7652 |                           26 |                               74.2857 |                         3.2871 |                      2.2845 |                       4.5741 |
| Frozen contrast upper level |         300.0000 |                    98.9772 |                     315 |                       2.0787 |                            4 |                               11.4286 |                        16.6588 |                      9.5145 |                      29.6574 |

The 300 t/day level is retained as the revision-frozen headline contrast, but it lies near the upper tail of the observed risk frame. The quartile-based levels show absolute risk where empirical support is denser.

## Entry-Design Collinearity Audit

| term                    |   minimum |   maximum |    mean |   standard_deviation |   variance_inflation_factor |   correlation_with_calendar_time |   correlation_with_log_elapsed_risk |   standardized_design_condition_number |
|:------------------------|----------:|----------:|--------:|---------------------:|----------------------------:|---------------------------------:|------------------------------------:|---------------------------------------:|
| age_per_10y             |    0.0000 |    5.5000 |  2.1071 |               0.9387 |                      1.3896 |                           0.3923 |                              0.4561 |                                 5.0170 |
| log_processing_capacity |    0.0000 |    2.3026 |  0.5191 |               0.3705 |                      1.1018 |                           0.0126 |                              0.0394 |                                 5.0170 |
| calendar_per_5y         |   -1.7000 |    1.9000 | -0.0917 |               1.0741 |                      5.7627 |                           1.0000 |                              0.9086 |                                 5.0170 |
| log_elapsed_risk        |    1.0986 |    3.0445 |  2.2177 |               0.5673 |                      6.1477 |                           0.9086 |                              1.0000 |                                 5.0170 |

Calendar time and elapsed risk are moderately collinear. Processing scale is not, so the diagnostic limits interpretation of the temporal terms rather than overturning the scale ordering.

## Consolidated Entry Specification Audit

| specification                                                | purpose                                       |   observations |   lineages |   events |   odds_ratio_300_vs_100 |   ci_low |   ci_high |   range_low |   range_high |   fits | uncertainty                                |
|:-------------------------------------------------------------|:----------------------------------------------|---------------:|-----------:|---------:|------------------------:|---------:|----------:|------------:|-------------:|-------:|:-------------------------------------------|
| Broad reduced-DF frame                                       | Frozen primary                                |     15154.0000 |  1137.0000 |  35.0000 |                  6.7233 |   4.3122 |   12.4614 |    nan      |     nan      |      1 | 1,999 whole-lineage bootstrap replications |
| Prior-operation reduced-DF frame                             | Requires positive prior throughput            |     13072.0000 |  1019.0000 |  33.0000 |                  7.0875 |   4.0842 |   13.7642 |    nan      |     nan      |      1 | 1,999 whole-lineage bootstrap replications |
| Same-episode reduced-DF frame                                | Excludes episode-boundary transitions         |     15095.0000 |  1135.0000 |  24.0000 |                  7.1510 |   4.4385 |   14.0512 |    nan      |     nan      |      1 | 1,999 whole-lineage bootstrap replications |
| Identity-certain reduced-DF frame                            | Excludes uncertain-link lineages              |     15107.0000 |  1130.0000 |  35.0000 |                  6.7648 |   4.2296 |   12.2973 |    nan      |     nan      |      1 | 1,999 whole-lineage bootstrap replications |
| Flexible era/duration Firth sensitivity                      | 11-parameter temporal-form check              |     15154.0000 |  1137.0000 |  35.0000 |                  6.1296 |   3.9197 |   11.2142 |    nan      |     nan      |      1 | 499 whole-lineage bootstrap replications   |
| Log of one plus t/day                                        | Functional Form                               |     15154.0000 |  1137.0000 |  35.0000 |                  5.0149 |   2.8479 |    8.8309 |    nan      |     nan      |      1 | Model-based                                |
| Linear t/day per 100                                         | Functional Form                               |     15154.0000 |  1137.0000 |  35.0000 |                  4.2195 |   2.6947 |    6.6072 |    nan      |     nan      |      1 | Model-based                                |
| Two prior observed years without positive capacity or output | Reporting State                               |     14000.0000 |  1110.0000 |  30.0000 |                  6.2082 |   3.2624 |   11.8139 |    nan      |     nan      |      1 | Model-based                                |
| Leave-one-event-prefecture fits                              | Geographic influence, not confounding control |       nan      |   nan      | nan      |                nan      | nan      |  nan      |      6.1430 |       7.1821 |     21 | Range across deletion fits                 |
| Leave-one-event reclassification                             | Single-event influence                        |       nan      |   nan      | nan      |                nan      | nan      |  nan      |      6.1162 |       7.2978 |     35 | Range across deletion fits                 |
| Leave-one-event-lineage deletion                             | Single-event influence                        |       nan      |   nan      | nan      |                nan      | nan      |  nan      |      6.1322 |       7.2961 |     35 | Range across deletion fits                 |

## Entry Sample Flow

|   order | stage                                                   |   facility_year_rows |   lineages |   events | role                          |
|--------:|:--------------------------------------------------------|---------------------:|-----------:|---------:|:------------------------------|
|       1 | All reconstructed administrative lineages               |                23593 |       1690 |      nan | Starting panel                |
|       2 | Left-censored: positive capacity in first observed year |                  nan |        467 |      nan | Excluded from entry risk set  |
|       3 | Observed non-generator risk set                         |                16519 |       1223 |       55 | Descriptive first-entry frame |
|       4 | Exact-year complete-covariate model                     |                15154 |       1137 |       35 | Frozen primary frame          |
|       5 | Positive-prior-throughput sensitivity                   |                13072 |       1019 |       33 | Nested operating frame        |

| model                             | term        |   coefficient |   standard_error_model_based |   p_value_model_based |   bootstrap_ci_low |   bootstrap_ci_high |   observations |   lineages |   events |   bootstrap_repetitions |
|:----------------------------------|:------------|--------------:|-----------------------------:|----------------------:|-------------------:|--------------------:|---------------:|-----------:|---------:|------------------------:|
| Broad reduced-DF frame            | age_per_10y |       -0.3274 |                       0.2144 |                0.1268 |            -0.7743 |              0.0701 |          15154 |       1137 |       35 |                    1999 |
| Prior-operation reduced-DF frame  | age_per_10y |       -0.3228 |                       0.2307 |                0.1618 |            -0.7928 |              0.1471 |          13072 |       1019 |       33 |                    1999 |
| Same-episode reduced-DF frame     | age_per_10y |       -0.7510 |                       0.2711 |                0.0056 |            -1.3639 |             -0.2059 |          15095 |       1135 |       24 |                    1999 |
| Identity-certain reduced-DF frame | age_per_10y |       -0.3276 |                       0.2144 |                0.1264 |            -0.7907 |              0.0652 |          15107 |       1130 |       35 |                    1999 |

## Exact Modeled-Event Composition

| calendar_era   |   Continuity-lineage entry |   Rebuild/replacement-like entry |
|:---------------|---------------------------:|---------------------------------:|
| FY2005-2009    |                          5 |                                2 |
| FY2010-2014    |                          2 |                                2 |
| FY2015-2019    |                         12 |                                2 |
| FY2020-2024    |                          5 |                                5 |

| Pathway                        |   Events |
|:-------------------------------|---------:|
| Continuity-lineage entry       |       24 |
| Rebuild/replacement-like entry |       11 |

## Event Influence

| deletion              |    min |   median |    max |
|:----------------------|-------:|---------:|-------:|
| event_lineage_removed | 6.1322 |   6.7095 | 7.2961 |
| event_reclassified    | 6.1162 |   6.7054 | 7.2978 |

The deletion range is diagnostic. It does not convert event histories into independent observations.

## Entry Robustness Beyond Event Deletion

| check_type      | model                                                        | scale_transform         | omitted_group   |   observations |   lineages |   events |   capacity_coefficient |   odds_ratio_300_vs_100 |   ci_low_model_based |   ci_high_model_based |   p_value_model_based | converged   |
|:----------------|:-------------------------------------------------------------|:------------------------|:----------------|---------------:|-----------:|---------:|-----------------------:|------------------------:|---------------------:|----------------------:|----------------------:|:------------|
| reference       | Frozen primary point model                                   | log1p_capacity_per_100  |                 |          15154 |       1137 |       35 |                 2.7492 |                  6.7233 |               3.7556 |               12.0362 |                0.0000 | True        |
| functional_form | Log of one plus t/day                                        | log1p_capacity_t_day    |                 |          15154 |       1137 |       35 |                 1.4766 |                  5.0149 |               2.8479 |                8.8309 |                0.0000 | True        |
| functional_form | Linear t/day per 100                                         | linear_capacity_per_100 |                 |          15154 |       1137 |       35 |                 0.7199 |                  4.2195 |               2.6947 |                6.6072 |                0.0000 | True        |
| reporting_state | Two prior observed years without positive capacity or output | log1p_capacity_per_100  |                 |          14000 |       1110 |       30 |                 2.6342 |                  6.2082 |               3.2624 |               11.8139 |                0.0000 | True        |

Across leave-one-event-prefecture-out fits, the 300-versus-100 t/day odds ratio ranges from 6.1430 to 7.1821. These fits are diagnostics with model-based intervals, not replacements for the whole-lineage bootstrap primary inference.

## Installed-Capacity Reporting-State Audit

The panel contains 49 rows with positive gross output but blank or zero reported installed capacity, spanning 6 administrative lineages. None of the exact modeled events reports positive output in the immediately prior year. The stricter two-prior-year state frame retains 14,000 rows, 1,110 lineages, and 30 events. A blank field is therefore described as no reported positive capacity, not verified physical absence.

## Raw-Quantity Engineering Models

| outcome                   | term               |   coefficient |   standard_error |   ci_low |   ci_high |   p_value |   observations |   lineages |   r_squared |
|:--------------------------|:-------------------|--------------:|-----------------:|---------:|----------:|----------:|---------------:|-----------:|------------:|
| log_installed_capacity_kw | cohort_Before 1990 |       -1.5647 |           0.0844 |  -1.7300 |   -1.3993 |    0.0000 |           6511 |        493 |      0.7862 |
| log_installed_capacity_kw | cohort_1990-1999   |       -0.8827 |           0.0635 |  -1.0071 |   -0.7583 |    0.0000 |           6511 |        493 |      0.7862 |
| log_installed_capacity_kw | cohort_2000-2009   |       -0.2674 |           0.0430 |  -0.3516 |   -0.1831 |    0.0000 |           6511 |        493 |      0.7862 |
| log_installed_capacity_kw | log_capacity_t_day |        1.5320 |           0.0435 |   1.4467 |    1.6173 |    0.0000 |           6511 |        493 |      0.7862 |

The installed-kW model is the raw-quantity primary representation. With identical controls, subtracting log processing capacity from its outcome yields the design-intensity parameterization; this translation is algebraic rather than independent corroboration.

## Common-Control Cohort Component Decomposition

| sample                    |   observations |   lineages | cohort      | reference_cohort   |   log_design_component |   log_capacity_factor_component |   log_waste_utilization_difference |   negative_log_utilization_component |   component_sum_log_gross_intensity |   direct_log_gross_intensity_difference |   direct_standard_error |   direct_ci_low |   direct_ci_high |   identity_error |
|:--------------------------|---------------:|-----------:|:------------|:-------------------|-----------------------:|--------------------------------:|-----------------------------------:|-------------------------------------:|------------------------------------:|----------------------------------------:|------------------------:|----------------:|-----------------:|-----------------:|
| Primary engineering frame |           6511 |        493 | Before 1990 | 2010 or later      |                -1.5647 |                          0.0159 |                            -0.2989 |                               0.2989 |                             -1.2499 |                                 -1.2499 |                  0.0777 |         -1.4021 |          -1.0977 |           0.0000 |
| Primary engineering frame |           6511 |        493 | 1990-1999   | 2010 or later      |                -0.8827 |                          0.0203 |                            -0.1725 |                               0.1725 |                             -0.6899 |                                 -0.6899 |                  0.0568 |         -0.8012 |          -0.5786 |           0.0000 |
| Primary engineering frame |           6511 |        493 | 2000-2009   | 2010 or later      |                -0.2674 |                         -0.0940 |                            -0.0892 |                               0.0892 |                             -0.2722 |                                 -0.2722 |                  0.0362 |         -0.3431 |          -0.2012 |           0.0000 |
| Stable-cohort sensitivity |           6291 |        479 | Before 1990 | 2010 or later      |                -1.6235 |                          0.0078 |                            -0.3097 |                               0.3097 |                             -1.3061 |                                 -1.3061 |                  0.0786 |         -1.4602 |          -1.1519 |           0.0000 |
| Stable-cohort sensitivity |           6291 |        479 | 1990-1999   | 2010 or later      |                -0.8823 |                          0.0094 |                            -0.1714 |                               0.1714 |                             -0.7016 |                                 -0.7016 |                  0.0585 |         -0.8162 |          -0.5869 |           0.0000 |
| Stable-cohort sensitivity |           6291 |        479 | 2000-2009   | 2010 or later      |                -0.2717 |                         -0.0984 |                            -0.0897 |                               0.0897 |                             -0.2803 |                                 -0.2803 |                  0.0374 |         -0.3537 |          -0.2070 |           0.0000 |

For every cohort and sample, the log design contribution plus the log capacity-factor contribution minus the log waste-utilization difference equals the directly fitted log gross-intensity difference. This shared-control decomposition is distinct from the primary capacity-factor model, which conditions on waste utilization and answers an equal-utilization comparison.

Administrative proxy exceptions retained within the audited 1.20 upper bounds: 5 capacity-factor rows and 7 utilization rows.
