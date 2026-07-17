# Major-Revision Scientific Results

## Lower-Degree-Of-Freedom Entry Model

The prespecified primary model uses five parameters including the intercept and 1,999 deterministic whole-lineage bootstrap replications per frame.

| Model                             |   odds_ratio_300_vs_100 |   bootstrap_ci_low |   bootstrap_ci_high |
|:----------------------------------|------------------------:|-------------------:|--------------------:|
| Broad reduced-DF frame            |                  6.7233 |             4.3122 |             12.4614 |
| Prior-operation reduced-DF frame  |                  7.0875 |             4.0842 |             13.7642 |
| Same-episode reduced-DF frame     |                  7.1510 |             4.4385 |             14.0512 |
| Identity-certain reduced-DF frame |                  6.7648 |             4.2296 |             12.2973 |

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

Administrative proxy exceptions retained within the audited 1.20 upper bounds: 5 capacity-factor rows and 7 utilization rows.
