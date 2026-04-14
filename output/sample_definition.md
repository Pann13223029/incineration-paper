# Analysis Sample Definition

This report documents the canonical descriptive and regression samples used by the analysis scripts.

- Full panel: 23,599 rows
- Power-generation rows flagged by MOE (`has_power_gen == True`): 6,950
- Operating power-generation sample (positive throughput and positive output): 6,660
- Operating sample rows missing official facility codes: 907
- Raw efficiency below 0.01 MWh/t before winsorization: 51
- Raw efficiency above 0.80 MWh/t before winsorization: 34
- Negative facility-age rows floored to zero: 52

## Regression Frame

- Regression observations: 5,683 (1,016 facilities)
- Fiscal years: FY2005 to FY2024
- Within/total variance ratio (pooled log-efficiency): 0.1499
- Pre-Fukushima ratio (FY2005-FY2011): 0.1795
- Post-Fukushima ratio (FY2012-FY2024): 0.0956
