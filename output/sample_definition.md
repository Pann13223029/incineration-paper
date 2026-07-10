# Analysis Sample Definition

This report documents the stable administrative-lineage descriptive and model samples used by the analysis scripts.

- Full panel: 23,593 rows
- Stable administrative-lineage fleet frame: 23,593 rows across 1,690 administrative lineages and 1,767 reported asset episodes
- Power-generation rows flagged by MOE (`has_power_gen == True`): 6,950
- FY2024 analytic-panel positive-capacity share: 417 of 1,014 rows (41.1%)
- Operating power-generation sample (positive throughput and positive output): 6,660 rows across 504 stable administrative lineages
- Operating sample rows missing official facility codes: 907
- Raw gross generation intensity below 0.01 MWh/t: 51
- Raw gross generation intensity above 0.80 MWh/t: 34
- Operating rows outside predeclared engineering bounds: 149
- Negative reported-age rows excluded rather than floored: 52

## Extensive-Margin Adoption Frame

- Left-censored facilities already generating power in their first observed year: 467
- Adoption risk-set observations: 16,519 (1,223 facilities)
- Observed first-adoption events in the panel window: 55
- Exact-year lagged adoption-model observations: 15,154 (1,137 facilities; 35 events)
- Entry following prior-lineage operation: 13,072 observations (1,019 lineages; 33 events)
- Main-frame events with zero or missing prior-year throughput: 2
- Exact-lag rows where elapsed fiscal duration differs from observed-row count: 156
- Broader previous-observed-site-row frame before exact-year restriction: 15,176 observations (1,137 facilities; 35 events)
- Non-exact lag rows excluded from the main adoption model: 22 (0 events)
- First observed at-risk years dropped because lagged predictors are required: 1,223
- Additional rows dropped for missing lagged age/capacity: 120 (71 facilities)

## Engineering Component Frame

- Engineering-valid observations: 6,511 across 493 stable administrative lineages
- Fiscal years: FY2005 to FY2024
- Within/total variance ratio (log gross MWh/t): 0.1059
- Early-window ratio (FY2005-FY2009): 0.0872
- Later-window ratio (FY2013-FY2024): 0.0689

## FY2024 Coverage Diagnostics

- Facilities with installed generation capacity: 41.1% of analytical rows
- Waste throughput handled by positive-output facilities: 80.1%
- Waste-processing design capacity at installed-generation facilities: 70.5%
