# Identifier Gap And Lag-Continuity Audit

This audit documents the official facility-code gap that affects facility-level tracking.
It is designed to answer a reviewer concern directly: whether the adoption model uses true prior-year lags or merely the previous observed coded row.

## Bottom Line

- The source panel has 3,718 rows without official facility codes in FY2010-FY2012.
- The broader previous-observed-coded-row adoption frame contains 11,717 rows and 140 events.
- The main exact-year adoption model keeps 10,823 rows and 98 events.
- Non-exact lag rows excluded from the main adoption model: 894 rows and 42 events (5 same-year duplicate-code events; 37 multi-year-gap events).
- Operating-generator rows missing official codes in FY2010-FY2012: 899; these rows are excluded from the canonical regression frame.

Interpretation: the main adoption specification should be described as an exact one-fiscal-year lagged observed-transition model. The broader previous-observed-coded-row frame is useful as a sensitivity check but should not be used for the main prior-year claim.

## Official Facility-Code Coverage By Fiscal Year

|   fiscal_year |   rows |   coded_rows |   missing_code_rows |   coded_share_pct |
|--------------:|-------:|-------------:|--------------------:|------------------:|
|          2005 |   1318 |         1318 |                   0 |             100   |
|          2006 |   1301 |         1301 |                   0 |             100   |
|          2007 |   1307 |         1307 |                   0 |             100   |
|          2008 |   1307 |         1279 |                  28 |              97.9 |
|          2009 |   1310 |         1284 |                  26 |              98   |
|          2010 |   1245 |            0 |                1245 |               0   |
|          2011 |   1251 |            0 |                1251 |               0   |
|          2012 |   1222 |            0 |                1222 |               0   |
|          2013 |   1199 |         1199 |                   0 |             100   |
|          2014 |   1207 |         1207 |                   0 |             100   |
|          2015 |   1192 |         1192 |                   0 |             100   |
|          2016 |   1154 |         1154 |                   0 |             100   |
|          2017 |   1139 |         1139 |                   0 |             100   |
|          2018 |   1128 |         1128 |                   0 |             100   |
|          2019 |   1093 |         1093 |                   0 |             100   |
|          2020 |   1087 |         1087 |                   0 |             100   |
|          2021 |   1060 |         1060 |                   0 |             100   |
|          2022 |   1038 |         1038 |                   0 |             100   |
|          2023 |   1027 |         1027 |                   0 |             100   |
|          2024 |   1014 |         1014 |                   0 |             100   |

## Adoption Lag Gaps In Previous-Observed-Coded-Row Frame

|   lag_gap_years |   rows |   events |   facilities |
|----------------:|-------:|---------:|-------------:|
|               0 |     67 |        5 |           29 |
|               1 |  10823 |       98 |         1911 |
|               2 |     14 |        1 |           14 |
|               3 |      1 |        0 |            1 |
|               4 |    716 |       24 |          714 |
|               5 |      3 |        1 |            3 |
|               6 |     69 |        4 |           69 |
|               7 |     12 |        2 |           12 |
|               8 |      4 |        2 |            4 |
|               9 |      4 |        2 |            4 |
|              10 |      2 |        0 |            2 |
|              11 |      2 |        1 |            2 |

## Operating-Generator Code Coverage By Fiscal Year

|   fiscal_year |   operating_rows |   coded_operating_rows |   mean_efficiency_mwh_t |   missing_code_rows |   missing_code_share_pct |
|--------------:|-----------------:|-----------------------:|------------------------:|--------------------:|-------------------------:|
|          2005 |              274 |                    274 |                   0.26  |                   0 |                      0   |
|          2006 |              280 |                    280 |                   0.266 |                   0 |                      0   |
|          2007 |              285 |                    285 |                   0.271 |                   0 |                      0   |
|          2008 |              287 |                    283 |                   0.275 |                   4 |                      1.4 |
|          2009 |              297 |                    293 |                   0.279 |                   4 |                      1.3 |
|          2010 |              295 |                      0 |                   0.29  |                 295 |                    100   |
|          2011 |              300 |                      0 |                   0.296 |                 300 |                    100   |
|          2012 |              304 |                      0 |                   0.302 |                 304 |                    100   |
|          2013 |              306 |                    306 |                   0.307 |                   0 |                      0   |
|          2014 |              314 |                    314 |                   0.307 |                   0 |                      0   |
|          2015 |              328 |                    328 |                   0.312 |                   0 |                      0   |
|          2016 |              345 |                    345 |                   0.323 |                   0 |                      0   |
|          2017 |              354 |                    354 |                   0.333 |                   0 |                      0   |
|          2018 |              361 |                    361 |                   0.344 |                   0 |                      0   |
|          2019 |              370 |                    370 |                   0.363 |                   0 |                      0   |
|          2020 |              375 |                    375 |                   0.363 |                   0 |                      0   |
|          2021 |              384 |                    384 |                   0.374 |                   0 |                      0   |
|          2022 |              394 |                    394 |                   0.374 |                   0 |                      0   |
|          2023 |              399 |                    399 |                   0.378 |                   0 |                      0   |
|          2024 |              408 |                    408 |                   0.383 |                   0 |                      0   |

## Implications For The Paper

- Use exact one-fiscal-year lags as the main adoption model.
- Treat previous-observed-coded-row adoption estimates as sensitivity evidence only.
- Treat pathway-audit mechanism labels as strongest only for adjacent-year events.
- Describe the generator regression frame as an identifiable coded-generator panel, not a complete census of all operating generator rows.
- Avoid strong Fukushima-window identification language unless a proxy-ID sensitivity later restores FY2010-FY2012 continuity.
