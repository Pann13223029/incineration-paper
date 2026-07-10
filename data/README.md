# Data

This directory contains the raw inputs and processed panels that reproduce the
paper-facing regression and robustness results.

## Source

All facility-level data come from Japan's Ministry of the Environment (MOE)
**General Waste Treatment Survey** (一般廃棄物処理実態調査), an annual
near-census survey of municipal solid waste treatment facilities operated by
or contracted to Japanese municipalities.

- **Publisher:** Environmental Management Bureau, Ministry of the Environment, Japan
- **Portal:** <https://www.env.go.jp/recycle/waste_tech/ippan/>
- **e-Stat mirror:** <https://www.e-stat.go.jp/en/statistics/00650101>
- **Current paper citation:** Ministry of the Environment Japan (2026) for the
  FY2024 General Waste Treatment Survey results, with e-Stat statistics code
  `00650101` as the official statistics portal reference.
- **Licence:** Public Japanese government statistics, reproducible with attribution.
  Cite as `MOEJ (YYYY)` following APA 7 conventions; see the thesis bibliography.

## Contents

### `raw/facility_annual/`

Twenty annual Excel workbooks downloaded from the MOE portal, one per fiscal
year from FY2005 through FY2024. File format is `.xls` through FY2013 and
`.xlsx` from FY2014 onward, reflecting the MOE's own change in publication
format. Column positions, header rows, and Japanese/English labelling vary
year-to-year; `code/scripts/02_parse_facility_panel.py` auto-detects these
per-file and normalises them into a single schema.

Files are reproduced verbatim from the MOE portal. To re-download from scratch,
run `code/scripts/01_download_facility_data.py`.

### `processed/incineration_panel.csv`

The base panel produced by `02_parse_facility_panel.py`. 23,599 facility-year
observations across 2,948 coded facilities, FY2005–FY2024, 28 columns covering
facility identification, design capacity, throughput, waste composition,
electricity generation, and facility age.

### `processed/incineration_panel_enriched.csv`

The authoritative analysis file, produced by `03_grid_emission_factors.py` from
the base panel. It retains the facility variables used by the entry and
generator-performance models and also contains a legacy contextual grid-factor
series. The current main regressions do not use that interpolated grid series;
fiscal-year indicators absorb common annual conditions without asking the grid
factor to carry a facility-performance interpretation.

### `processed/grid_emission_factors.csv`

Contextual series for ten Japanese utility areas across twenty fiscal years,
with linear interpolation where direct annual values were unavailable. It is
retained for legacy comparability and exploratory climate context, not as a core
covariate or paper result. Any future carbon-accounting use should replace or
independently verify the anchors against primary annual disclosures.

### `processed/prefecture_utility_crosswalk.csv`

Static mapping of Japan's 47 prefectures to the 10 regional utility areas that
serve them for grid emission-factor assignment. Verified against utility
service-area maps and MOE regional classifications.

## Reproduction

Everything in `processed/` can be regenerated from `raw/facility_annual/` via
the numbered scripts in `code/scripts/`. The processed files are included here
so that readers can reproduce the regression results and tables in
`paper/manuscript/paper.md` without needing to re-run the parsing pipeline, which
involves year-specific column detection heuristics.

```bash
# From raw Excel to final regression output:
python code/scripts/02_parse_facility_panel.py     # raw -> incineration_panel.csv
python code/scripts/03_grid_emission_factors.py    # + grid factors -> enriched
python code/scripts/05a_power_adoption.py          # capacity entry and exit hazards
python code/scripts/05_panel_regression.py         # main 4 specifications
python code/scripts/06_robustness.py               # robustness specifications
```

## Attribution

When using these data, cite the MOE survey directly. If referring to this
derived analysis workspace, cite the paper/manuscript that uses the processed
panel.
