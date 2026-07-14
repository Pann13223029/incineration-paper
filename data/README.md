# Data

This directory contains the Ministry of the Environment (MOE) source workbooks and reproducible processed data used by the paper.

## Source

The facility records come from Japan's MOE **General Waste Treatment Survey** (一般廃棄物処理実態調査), an annual administrative survey of municipal solid-waste treatment facilities operated by or contracted to municipalities.

- Publisher: Environmental Management Bureau, Ministry of the Environment, Japan
- MOE portal: <https://www.env.go.jp/recycle/waste_tech/ippan/>
- e-Stat portal: <https://www.e-stat.go.jp/en/statistics/00650101>
- Coverage used here: FY2005-FY2024
- Provenance outputs: [`../output/raw_data_provenance.md`](../output/raw_data_provenance.md), [`../output/raw_data_manifest.csv`](../output/raw_data_manifest.csv), and [`../output/raw_workbook_schema_map.csv`](../output/raw_workbook_schema_map.csv)

The manifest records SHA-256 hashes, file sizes, configured source URLs, sheet names, header locations, and parser-selected fields. Use it rather than relying on filenames alone.

## Directory Contents

### `raw/facility_annual/`

Twenty annual Excel workbooks, one for each fiscal year from FY2005 through FY2024. MOE publication formats and column layouts change across years, so `code/analysis/02_parse_facility_panel.py` detects each workbook's sheet, header, and field mapping.

Run `code/analysis/01_download_facility_data.py` only when intentionally refreshing source files. A refresh changes provenance and requires a full rebuild and review.

### `processed/incineration_panel.csv`

The direct parser output: 23,599 source rows in a normalized annual schema. This file precedes exact-duplicate collapse and longitudinal identity reconstruction.

### `processed/incineration_panel_identified.csv`

The identity-audited analytical panel: 23,593 unique retained records across 1,690 stable administrative facility lineages and 1,767 asset episodes. Sixteen accepted uncertain links are exposed in [`../output/identity_low_margin_links.csv`](../output/identity_low_margin_links.csv) for whole-lineage sensitivity analysis.

`stable_site_id` is a deterministic administrative lineage reconstructed from annual evidence. It does not establish one immutable physical site, continuous ownership, unchanged machinery, or physical closure. `asset_episode_id` separates reported configuration resets within a lineage but is not a verified equipment registry.

### `processed/facility_identity_crosswalk.csv`

Record-level mapping from parsed source rows to stable lineages and asset episodes, including match diagnostics. Official facility code is supporting evidence, not a persistent key: codes are entirely absent in FY2010-FY2012 and FY2019-FY2020 has zero code overlap, while audited linkage restores 1,064 lineages across that transition.

### `processed/incineration_panel_enriched.csv`

An optional legacy/context derivative containing regional grid fields. It is not
the input to the current paper models and is not rebuilt by the canonical
pipeline.

### Contextual files

- `processed/grid_emission_factors.csv` retains a legacy contextual regional series; it is not a core covariate in the current models.
- `processed/prefecture_utility_crosswalk.csv` maps prefectures to regional utility areas for that contextual series.

Any future carbon-accounting analysis should independently verify annual factors and add an explicit counterfactual. Gross generation alone is not avoided emissions.

The fleet, entry, and generator-component stages read
`processed/incineration_panel_identified.csv` directly.

## Reproduction

From the repository root:

```bash
npm run analysis:rebuild
```

The orchestrator runs parsing, provenance, identity, enrichment, descriptive analysis, fleet decomposition, Firth entry models, generator component models, robustness and data-quality audits, identifier audits, and claim verification.

Generated analytical facts belong in `output/`; selected paper-facing copies belong in `paper/evidence/current/` after `npm run paper:sync`. Do not hand-edit processed or generated files to force agreement with manuscript prose.

The public journal and professor-facing manuscript profiles consume the same
processed data and canonical outputs. No profile-specific data or model branch
is permitted.

## Attribution

Cite the MOE survey and e-Stat statistics code `00650101` when using the source records. Cite the paper for the derived identity reconstruction, samples, and analysis.
