# Facility Identity Audit

Stable administrative facility lineages are resolved by deterministic one-to-one matching. Adjacent fiscal years are matched before short gaps; official codes are supporting evidence rather than conclusive keys and are rejected when names and configuration evidence contradict them. Exact source duplicates are collapsed before matching. Sub-threshold and weak ambiguous edges are excluded before assignment, and unique unmatched dummy choices keep rejected edges from changing accepted links. Asset episodes split at symmetric reported start-year resets or major configuration resets.

- Raw source rows: 23,599
- Unique retained source records: 23,593
- Collapsed exact duplicate rows: 6
- Stable administrative lineages: 1,690
- Asset episodes: 1,767
- Duplicate stable-lineage-years: 0
- Maximum observed fiscal years per lineage: 20
- Accepted uncertain links exposed: 16
- Accepted uncertain-link share: 0.073% of accepted links
- Sub-threshold candidate edges excluded before assignment: 3,092
- Weak ambiguous candidate edges excluded before assignment: 15,308
- FY2019-FY2020 official-code overlap: 0
- FY2019-FY2020 restored administrative-lineage overlap: 1,064

## Annual Continuity

|   fiscal_year |   rows |   stable_sites |   official_code_overlap_prior_year |   stable_site_overlap_prior_year |   stable_overlap_share_current_pct |   new_site_rows |   uncertain_link_rows |   missing_official_code_rows |
|--------------:|-------:|---------------:|-----------------------------------:|---------------------------------:|-----------------------------------:|----------------:|----------------------:|-----------------------------:|
|        2005.0 | 1318.0 |         1318.0 |                              nan   |                            nan   |                              nan   |          1318.0 |                   0.0 |                          0.0 |
|        2006.0 | 1301.0 |         1301.0 |                             1267.0 |                           1273.0 |                               97.8 |            28.0 |                   0.0 |                          0.0 |
|        2007.0 | 1306.0 |         1306.0 |                             1262.0 |                           1285.0 |                               98.4 |            21.0 |                   6.0 |                          0.0 |
|        2008.0 | 1305.0 |         1305.0 |                             1123.0 |                           1278.0 |                               97.9 |            24.0 |                   1.0 |                         28.0 |
|        2009.0 | 1309.0 |         1309.0 |                             1178.0 |                           1271.0 |                               97.1 |            32.0 |                   0.0 |                         26.0 |
|        2010.0 | 1244.0 |         1244.0 |                                0.0 |                           1229.0 |                               98.8 |            15.0 |                   0.0 |                       1244.0 |
|        2011.0 | 1250.0 |         1250.0 |                                0.0 |                           1230.0 |                               98.4 |            19.0 |                   0.0 |                       1250.0 |
|        2012.0 | 1222.0 |         1222.0 |                                0.0 |                           1205.0 |                               98.6 |            17.0 |                   0.0 |                       1222.0 |
|        2013.0 | 1199.0 |         1199.0 |                                0.0 |                           1169.0 |                               97.5 |            29.0 |                   0.0 |                          0.0 |
|        2014.0 | 1207.0 |         1207.0 |                             1184.0 |                           1185.0 |                               98.2 |            20.0 |                   1.0 |                          0.0 |
|        2015.0 | 1192.0 |         1192.0 |                             1159.0 |                           1158.0 |                               97.1 |            29.0 |                   0.0 |                          0.0 |
|        2016.0 | 1154.0 |         1154.0 |                             1138.0 |                           1138.0 |                               98.6 |            15.0 |                   1.0 |                          0.0 |
|        2017.0 | 1139.0 |         1139.0 |                             1112.0 |                           1112.0 |                               97.6 |            25.0 |                   2.0 |                          0.0 |
|        2018.0 | 1128.0 |         1128.0 |                             1101.0 |                           1104.0 |                               97.9 |            21.0 |                   2.0 |                          0.0 |
|        2019.0 | 1093.0 |         1093.0 |                             1077.0 |                           1081.0 |                               98.9 |            12.0 |                   1.0 |                          0.0 |
|        2020.0 | 1087.0 |         1087.0 |                                0.0 |                           1064.0 |                               97.9 |            20.0 |                   0.0 |                          0.0 |
|        2021.0 | 1060.0 |         1060.0 |                             1039.0 |                           1044.0 |                               98.5 |            14.0 |                   1.0 |                          0.0 |
|        2022.0 | 1038.0 |         1038.0 |                             1027.0 |                           1028.0 |                               99.0 |            10.0 |                   0.0 |                          0.0 |
|        2023.0 | 1027.0 |         1027.0 |                             1011.0 |                           1015.0 |                               98.8 |            10.0 |                   0.0 |                          0.0 |
|        2024.0 | 1014.0 |         1014.0 |                             1002.0 |                           1003.0 |                               98.9 |            11.0 |                   1.0 |                          0.0 |

## Match Families

| match_family                     |   rows |   uncertain_links |   strong_evidence_overrides |   min_score |   min_current_row_margin |   min_prior_record_margin |   min_margin |
|:---------------------------------|-------:|------------------:|----------------------------:|------------:|-------------------------:|--------------------------:|-------------:|
| exact_name_without_code          |   6204 |                 7 |                           7 |       145.0 |                    -12.0 |                       3.0 |        -12.0 |
| fuzzy_name_without_code          |    101 |                 0 |                           0 |        94.0 |                      3.4 |                       5.4 |          3.4 |
| new_site                         |   1690 |                 0 |                           0 |         0.0 |                    nan   |                     nan   |        nan   |
| official_code_and_exact_name     |  15324 |                 2 |                           2 |       175.0 |                      9.0 |                     -20.0 |        -20.0 |
| official_code_with_other_support |    274 |                 7 |                           7 |        99.3 |                    -27.1 |                     -39.1 |        -39.1 |

## Collapsed Exact Source Duplicates

| source_record_id            |   retained_rows |   source_multiplicity |   fiscal_year | prefecture   | facility_name   |
|:----------------------------|----------------:|----------------------:|--------------:|:-------------|:----------------|
| record_036840176500afad23eb |               1 |                     2 |          2008 | 宮城県          |                 |
| record_31ff4ef22fad70cd5c04 |               1 |                     2 |          2007 | 徳島県          | 三好市東祖谷一般廃棄物処理場  |
| record_62d7f8b530cacd38e6c4 |               1 |                     2 |          2009 | 徳島県          | 三好市東祖谷一般廃棄物処理場  |
| record_847425cb8aa30a63b01e |               1 |                     2 |          2008 | 徳島県          | 三好市東祖谷一般廃棄物処理場  |
| record_b3690680aaed1307e45d |               1 |                     2 |          2010 | 徳島県          | 三好市東祖谷一般廃棄物処理場  |
| record_eedfac8929516967aa7b |               1 |                     2 |          2011 | 徳島県          | 三好市東祖谷一般廃棄物処理場  |

## Accepted Two-Sided Low-Margin Links

These exact-name or official-code-supported links remain accepted even though the current-row alternative margin, prior-record competitor margin, or both are below 3 points. Every row is uncertainty-flagged for downstream sensitivity analysis and is canonically exposed in `output/identity_low_margin_links.csv`.

|   fiscal_year | prefecture   |   facility_code | facility_name       |   identity_match_score |   identity_match_current_row_margin |   identity_match_prior_record_margin |   identity_match_margin | identity_match_uncertainty_reason                         | identity_match_strong_evidence_override   | identity_match_method                                                               |
|--------------:|:-------------|----------------:|:--------------------|-----------------------:|------------------------------------:|-------------------------------------:|------------------------:|:----------------------------------------------------------|:------------------------------------------|:------------------------------------------------------------------------------------|
|          2007 | 三重県          |      2420101001 | 津市西部クリーンセンター        |                 195.00 |                              -10.00 |                                20.00 |                  -10.00 | low_current_row_margin                                    | True                                      | name_exact+municipality+start_year+capacity+furnaces+facility_type+gap=1            |
|          2007 | 岐阜県          |      2189501001 | 西濃環境保全センター          |                 195.00 |                                0.00 |                                30.00 |                    0.00 | low_current_row_margin                                    | True                                      | name_exact+municipality+start_year+capacity+furnaces+facility_type+gap=1            |
|          2007 | 栃木県          |      0921301001 | 黒磯清掃センター            |                 195.00 |                              -12.00 |                                18.00 |                  -12.00 | low_current_row_margin                                    | True                                      | name_exact+municipality+start_year+capacity+furnaces+facility_type+gap=1            |
|          2007 | 神奈川県         |      1481801001 | 高座清掃施設組合ごみ処理施設      |                 195.00 |                                0.00 |                                30.00 |                    0.00 | low_current_row_margin                                    | True                                      | name_exact+municipality+start_year+capacity+furnaces+facility_type+gap=1            |
|          2007 | 長野県          |      2036101001 | 下諏訪町清掃センター          |                 195.00 |                                2.00 |                                32.00 |                    2.00 | low_current_row_margin                                    | True                                      | name_exact+municipality+start_year+capacity+furnaces+facility_type+gap=1            |
|          2007 | 鹿児島県         |      4620101001 | 鹿児島市旧北部清掃工場         |                 171.67 |                               68.00 |                               -15.33 |                  -15.33 | low_prior_record_competitor_margin                        | True                                      | code+name_fuzzy=0.952+municipality+start_year+capacity+furnaces+facility_type+gap=1 |
|          2008 | 北海道          |      0120201001 | 函館市日乃出清掃工場          |                 205.00 |                               18.00 |                                -2.00 |                   -2.00 | low_prior_record_competitor_margin                        | True                                      | code+name_exact+municipality+capacity+furnaces+facility_type+gap=1                  |
|          2014 | 大分県          |      4483601002 | 藤ヶ谷清掃センター　高効率ごみ発電施設 |                 149.80 |                              inf    |                                -7.20 |                   -7.20 | low_prior_record_competitor_margin                        | True                                      | code+name_fuzzy=0.640+municipality+start_year+capacity+furnaces+facility_type+gap=1 |
|          2016 | 兵庫県          |      2810001005 | 港島クリーンセンター          |                 163.95 |                                1.95 |                                59.95 |                    1.95 | low_current_row_margin                                    | True                                      | code+name_fuzzy=0.842+municipality+start_year+capacity+furnaces+facility_type+gap=1 |
|          2017 | 鹿児島県         |      4630401004 | 十島村悪石島焼却施設          |                 195.00 |                                0.00 |                                50.00 |                    0.00 | low_current_row_margin                                    | True                                      | name_exact+municipality+start_year+capacity+furnaces+facility_type+gap=1            |
|          2017 | 鹿児島県         |      4630401005 | 十島村悪石島焼却施設          |                 175.00 |                               30.00 |                               -20.00 |                  -20.00 | low_prior_record_competitor_margin                        | True                                      | code+name_exact+municipality+gap=1                                                  |
|          2018 | 鹿児島県         |      4630401005 | 十島村諏訪之瀬島焼却施設        |                 105.91 |                              -26.36 |                               -39.09 |                  -39.09 | low_current_row_margin+low_prior_record_competitor_margin | True                                      | code+name_fuzzy=0.727+municipality+gap=1                                            |
|          2018 | 鹿児島県         |      4630401003 | 十島村悪石島焼却施設          |                 157.00 |                               -4.00 |                                34.00 |                   -4.00 | low_current_row_margin                                    | True                                      | name_exact+municipality+capacity+furnaces+facility_type+gap=1                       |
|          2019 | 鹿児島県         |      4630401006 | 十島村悪石島焼却施設          |                 163.95 |                              -27.05 |                                26.73 |                  -27.05 | low_current_row_margin                                    | True                                      | code+name_fuzzy=0.842+municipality+start_year+capacity+furnaces+facility_type+gap=1 |
|          2021 | 福井県          |         1810072 | 第１清掃センター            |                 105.00 |                                2.67 |                               inf    |                    2.67 | low_current_row_margin                                    | True                                      | code+name_fuzzy=0.000+municipality+start_year+capacity+furnaces+facility_type+gap=1 |
|          2024 | 北海道          |         0110689 | 札幌市駒岡清掃工場           |                 165.00 |                              -10.00 |                                50.00 |                  -10.00 | low_current_row_margin                                    | True                                      | code+name_fuzzy=0.857+municipality+start_year+capacity+furnaces+facility_type+gap=1 |

## Executable Guardrails

- Golden same link checks: 3
- Golden separation checks: 3
- Permutation invariance prefectures: 6
- Insertion invariance prefectures: 6
- Two sided margin rows checked: 21903
- Accepted subthreshold links: 0
- Accepted weak ambiguous links: 0
- Uncertain links exposed: 16

The audit is an administrative identity reconstruction, not proof of physical closure, ownership continuity, or unchanged equipment.
