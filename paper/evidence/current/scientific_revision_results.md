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

## Raw-Quantity Engineering Models

| outcome                   | term               |   coefficient |   standard_error |   ci_low |   ci_high |   p_value |   observations |   lineages |   r_squared |
|:--------------------------|:-------------------|--------------:|-----------------:|---------:|----------:|----------:|---------------:|-----------:|------------:|
| log_installed_capacity_kw | cohort_Before 1990 |       -1.5647 |           0.0844 |  -1.7300 |   -1.3993 |    0.0000 |           6511 |        493 |      0.7862 |
| log_installed_capacity_kw | cohort_1990-1999   |       -0.8827 |           0.0635 |  -1.0071 |   -0.7583 |    0.0000 |           6511 |        493 |      0.7862 |
| log_installed_capacity_kw | cohort_2000-2009   |       -0.2674 |           0.0430 |  -0.3516 |   -0.1831 |    0.0000 |           6511 |        493 |      0.7862 |
| log_installed_capacity_kw | log_capacity_t_day |        1.5320 |           0.0435 |   1.4467 |    1.6173 |    0.0000 |           6511 |        493 |      0.7862 |

The installed-kW model is the raw-quantity primary representation. With identical controls, subtracting log processing capacity from its outcome yields the design-intensity parameterization; this translation is algebraic rather than independent corroboration.

Administrative proxy exceptions retained within the audited 1.20 upper bounds: 5 capacity-factor rows and 7 utilization rows.
