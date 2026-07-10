# Analysis Sample Definition

This report documents the canonical descriptive and regression samples used by the analysis scripts.

- Full panel: 23,599 rows
- Coded full-fleet frame (facility identifier present): 19,827 rows (2,948 facilities)
- Power-generation rows flagged by MOE (`has_power_gen == True`): 6,950
- FY2024 analytic-panel positive-capacity share: 417 of 1,014 rows (41.1%)
- Operating power-generation sample (positive throughput and positive output): 6,660
- Operating sample rows missing official facility codes: 907
- Raw efficiency below 0.01 MWh/t before winsorization: 51
- Raw efficiency above 0.80 MWh/t before winsorization: 34
- Negative facility-age rows floored to zero: 52

## Extensive-Margin Adoption Frame

- Left-censored facilities already generating power in their first observed year: 913
- Adoption risk-set observations: 13,770 (2,035 facilities)
- Observed first-adoption events in the panel window: 141
- Exact-year lagged adoption-model observations: 10,823 (1,911 facilities; 98 events)
- Positive-prior-throughput conversion sensitivity: 9,215 observations (1,663 facilities; 58 events)
- Main-frame events with zero or missing prior-year throughput: 40
- Exact-lag rows where elapsed fiscal duration differs from observed-row count: 4,055
- Broader previous-observed-coded-row adoption frame before exact-year restriction: 11,717 observations (1,915 facilities; 140 events)
- Non-exact lag rows excluded from the main adoption model: 894 (42 events)
- First observed at-risk years dropped because lagged predictors are required: 2,035
- Additional rows dropped for missing lagged age/capacity: 18 (12 facilities)

## Regression Frame

- Regression observations: 5,683 (1,016 facilities)
- Fiscal years: FY2005 to FY2024
- Within/total variance ratio (pooled log-efficiency): 0.1499
- Early coded-window ratio (FY2005-FY2009): 0.1795
- Later coded-window ratio (FY2013-FY2024): 0.0956
