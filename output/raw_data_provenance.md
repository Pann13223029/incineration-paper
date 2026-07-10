# Raw Data Provenance

This artifact records recoverable provenance for the raw MOE facility workbooks. URLs are reconstructed only from the checked-in downloader configuration; this stage does not claim that the URLs were revalidated at run time.

- Original retrieval timestamp: **unavailable** because the downloader did not record it.
- Filesystem modification time: **unavailable/not persisted** because checkout mtimes are volatile.
- Repository timestamp: last Git commit time for each workbook, not the original retrieval time.
- Parser sheet: first workbook sheet (`sheet_name=0`), matching the checked-in parser.
- Header mappings: reproduced with the parser's first-match keyword search over rows 0-5.
- Canonical preflight: **passed** for exactly one present, nonempty workbook per year.
- Canonical window: FY2005-FY2024.
- Configured fiscal years: 20
- Present workbooks: 20
- Total present bytes: 15,158,836

## Workbook Inventory

|   fiscal_year | era_code   | filename                 |   byte_size | sha256          | repository_commit_timestamp   | parser_sheet_name   |   raw_sheet_rows |   data_start_row_excel |   candidate_data_rows |   detected_standardized_fields |   unavailable_standardized_fields |
|--------------:|:-----------|:-------------------------|------------:|:----------------|:------------------------------|:--------------------|-----------------:|-----------------------:|----------------------:|-------------------------------:|----------------------------------:|
|          2005 | h17        | fy2005_incineration.xls  |      752640 | e4857ebc4105... | 2026-04-13T11:29:30+07:00     | 焼却                  |             1320 |                      3 |                  1318 |                             17 |                                 2 |
|          2006 | h18        | fy2006_incineration.xls  |      725504 | 44d89b3e6e8b... | 2026-04-13T11:29:30+07:00     | 焼却                  |             1303 |                      3 |                  1301 |                             17 |                                 2 |
|          2007 | h19        | fy2007_incineration.xls  |     1213952 | b3f3e72d4c42... | 2026-04-13T11:29:30+07:00     | 焼却                  |             1313 |                      7 |                  1307 |                             17 |                                 2 |
|          2008 | h20        | fy2008_incineration.xls  |      914432 | b8b04c53fd06... | 2026-04-13T11:29:30+07:00     | 焼却施設                |             1313 |                      7 |                  1307 |                             17 |                                 2 |
|          2009 | h21        | fy2009_incineration.xls  |     1134592 | 2b76252fcf5b... | 2026-04-13T11:29:30+07:00     | 焼却施設                |             1316 |                      7 |                  1310 |                             17 |                                 2 |
|          2010 | h22        | fy2010_incineration.xls  |     1057280 | 28344f9ecc7b... | 2026-04-13T11:29:30+07:00     | 焼却                  |             1251 |                      7 |                  1245 |                             17 |                                 2 |
|          2011 | h23        | fy2011_incineration.xls  |     1065984 | e1d4c67df441... | 2026-04-13T11:29:30+07:00     | 焼却                  |             1257 |                      7 |                  1251 |                             17 |                                 2 |
|          2012 | h24        | fy2012_incineration.xls  |     1037312 | 0d699fc19868... | 2026-04-13T11:29:30+07:00     | 焼却                  |             1228 |                      7 |                  1222 |                             17 |                                 2 |
|          2013 | h25        | fy2013_incineration.xls  |     1047040 | 34b5115c18e5... | 2026-04-13T11:29:30+07:00     | 焼却                  |             1205 |                      7 |                  1199 |                             17 |                                 2 |
|          2014 | h26        | fy2014_incineration.xlsx |      535530 | d5bed22b80ff... | 2026-04-13T11:29:30+07:00     | 焼却                  |             1213 |                      7 |                  1207 |                             17 |                                 2 |
|          2015 | h27        | fy2015_incineration.xls  |      927744 | ad5e8f903189... | 2026-04-13T11:29:30+07:00     | 焼却                  |             2059 |                      7 |                  2053 |                             17 |                                 2 |
|          2016 | h28        | fy2016_incineration.xlsx |      469560 | 6c5bacf2369a... | 2026-04-13T11:29:30+07:00     | 焼却                  |             1160 |                      7 |                  1154 |                             17 |                                 2 |
|          2017 | h29        | fy2017_incineration.xlsx |      471997 | 3f6de985079d... | 2026-04-13T11:29:30+07:00     | 焼却                  |             1145 |                      7 |                  1139 |                             17 |                                 2 |
|          2018 | h30        | fy2018_incineration.xlsx |      512040 | 8ce73f4d92ee... | 2026-04-13T11:29:30+07:00     | 焼却                  |             1134 |                      7 |                  1128 |                             19 |                                 0 |
|          2019 | r1         | fy2019_incineration.xlsx |      500707 | 3b4e7f961cbc... | 2026-04-13T11:29:30+07:00     | 焼却                  |             1099 |                      7 |                  1093 |                             19 |                                 0 |
|          2020 | r2         | fy2020_incineration.xlsx |      575863 | b5ebabeb9df7... | 2026-04-13T11:29:30+07:00     | 焼却                  |             1093 |                      7 |                  1087 |                             19 |                                 0 |
|          2021 | r3         | fy2021_incineration.xlsx |      553247 | 77a95fe0dbe5... | 2026-04-13T11:29:30+07:00     | 焼却                  |             1066 |                      7 |                  1060 |                             19 |                                 0 |
|          2022 | r4         | fy2022_incineration.xlsx |      537259 | 74bca0e94671... | 2026-04-13T11:29:30+07:00     | 焼却                  |             1044 |                      7 |                  1038 |                             19 |                                 0 |
|          2023 | r5         | fy2023_incineration.xlsx |      554292 | 8147f3233e4d... | 2026-04-13T11:29:30+07:00     | 焼却                  |             1033 |                      7 |                  1027 |                             19 |                                 0 |
|          2024 | r6         | fy2024_incineration.xlsx |      571861 | 3af23706820b... | 2026-04-13T11:29:30+07:00     | 焼却                  |             1020 |                      7 |                  1014 |                             19 |                                 0 |

## Mapping Coverage

The full field-by-field mapping, including matched Japanese header text and zero-based/Excel coordinates, is in `output/raw_workbook_schema_map.csv`.

Optional later-schema fields not detected by the configured parser search (all required fields passed preflight):

|   fiscal_year | standardized_field   |
|--------------:|:---------------------|
|          2005 | power_sold_mwh       |
|          2005 | sell_revenue_yen     |
|          2006 | power_sold_mwh       |
|          2006 | sell_revenue_yen     |
|          2007 | power_sold_mwh       |
|          2007 | sell_revenue_yen     |
|          2008 | power_sold_mwh       |
|          2008 | sell_revenue_yen     |
|          2009 | power_sold_mwh       |
|          2009 | sell_revenue_yen     |
|          2010 | power_sold_mwh       |
|          2010 | sell_revenue_yen     |
|          2011 | power_sold_mwh       |
|          2011 | sell_revenue_yen     |
|          2012 | power_sold_mwh       |
|          2012 | sell_revenue_yen     |
|          2013 | power_sold_mwh       |
|          2013 | sell_revenue_yen     |
|          2014 | power_sold_mwh       |
|          2014 | sell_revenue_yen     |
|          2015 | power_sold_mwh       |
|          2015 | sell_revenue_yen     |
|          2016 | power_sold_mwh       |
|          2016 | sell_revenue_yen     |
|          2017 | power_sold_mwh       |
|          2017 | sell_revenue_yen     |

## Audit Boundary

SHA-256 and byte size establish the identity of the files currently in the repository. They do not establish the date of download, HTTP response headers, publisher-side version history, or legal custody before the files entered this workspace; those fields are unavailable unless a separate acquisition log exists.
