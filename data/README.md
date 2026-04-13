# Data

This directory contains the raw inputs and processed panels that reproduce the
regression results in `thesis/thesis.tex`.

## Source

All facility-level data come from Japan's Ministry of the Environment (MOE)
**General Waste Treatment Survey** (一般廃棄物処理実態調査), an annual
near-census survey of municipal solid waste treatment facilities operated by
or contracted to Japanese municipalities.

- **Publisher:** Environmental Management Bureau, Ministry of the Environment, Japan
- **Portal:** <https://www.env.go.jp/recycle/waste_tech/ippan/>
- **e-Stat mirror:** <https://www.e-stat.go.jp/en/statistics/00650101>
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
observations across 2,949 unique facilities, FY2005–FY2024, 28 columns covering
facility identification, design capacity, throughput, waste composition,
electricity generation, and facility age.

### `processed/incineration_panel_enriched.csv`

The authoritative analysis file, produced by `03_grid_emission_factors.py` from
the base panel. Adds regional grid emission factors (kg-CO₂/kWh) from METI and
regional utility publications, matched at 100% via the prefecture-to-utility
crosswalk below. This is the file consumed directly by the regression scripts
(`05_panel_regression.py`, `06_robustness.py`).

### `processed/grid_emission_factors.csv`

Manually constructed from METI annual energy reports and regional utility
disclosures. Ten Japanese utility areas × 20 fiscal years, with linear
interpolation between anchor years where direct publications were unavailable.
See `code/scripts/03_grid_emission_factors.py` for the full construction logic
and source citations per anchor.

### `processed/prefecture_utility_crosswalk.csv`

Static mapping of Japan's 47 prefectures to the 10 regional utility areas that
serve them for grid emission-factor assignment. Verified against utility
service-area maps and MOE regional classifications.

## Reproduction

Everything in `processed/` can be regenerated from `raw/facility_annual/` via
the numbered scripts in `code/scripts/`. The processed files are included here
so that readers can reproduce the regression results and tables in
`thesis/thesis.tex` without needing to re-run the parsing pipeline, which
involves year-specific column detection heuristics.

```bash
# From raw Excel to final regression output:
python code/scripts/02_parse_facility_panel.py     # raw -> incineration_panel.csv
python code/scripts/03_grid_emission_factors.py    # + grid factors -> enriched
python code/scripts/05_panel_regression.py         # main 4 specifications
python code/scripts/06_robustness.py               # 8 robustness specifications
```

## Attribution

When using these data, please cite both the MOE survey directly and this
thesis. Suggested citation for the thesis:

> Phetra, P. (2026). *Carbon Lock-in or Circular Transition? Heterogeneity in
> Japan's Waste Incineration Fleet and Net-Zero Compatibility* [Bachelor's
> thesis]. Ritsumeikan Asia Pacific University, College of Sustainability and
> Tourism.
