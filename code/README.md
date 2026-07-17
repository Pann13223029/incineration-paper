# Code Workspace

The code layer has three responsibilities: `analysis/` creates canonical
evidence, `publishing/` turns existing evidence and manuscript sources into
review artifacts, and `review/` runs explicitly noncanonical workflow
simulations.

## Directory Roles

| Path | Responsibility | Main entry point |
|:--|:--|:--|
| `analysis/` | Parse sources, document provenance, reconstruct longitudinal identity, estimate models, run audits, and verify claims | `analysis/07_rebuild_analysis.py` |
| `publishing/` | Synchronize evidence, export submission files, build journal/thesis PDFs and slides, and validate repository format gates | npm commands in `package.json` |
| `review/` | Simulate reviewer workflows and conservative stress cases without changing canonical evidence | `npm run review:simulate:linkage` |

## Canonical Analysis Order

| Order | Script | Responsibility |
|:--|:--|:--|
| 1 | `02b_build_raw_data_manifest.py` | Preflight exactly 20 nonempty FY2005-FY2024 workbooks, then record hashes, byte sizes, URLs, sheets, headers, and selected columns. |
| 2 | `02_parse_facility_panel.py` | Parse the preflighted MOE workbooks into 23,599 source rows and fail on any missing or duplicate year. |
| 3 | `02a_build_facility_identity.py` | Collapse exact duplicates and construct 23,593 unique records, 1,690 stable administrative lineages, and 1,767 asset episodes; expose uncertain links. |
| 4 | `02c_build_linkage_validation_packet.py` | Build the blinded clerical-review packet and separate answer key. |
| 5 | `04_eda_facility.py` | Build descriptive summaries and audit model-frame inputs. |
| 6 | `05_fleet_decomposition.py` | Separate facility participation, throughput coverage, and design-capacity share. |
| 7 | `05a_power_adoption.py` | Retain the higher-dimensional sparse-entry specification and pathway outputs as sensitivities. |
| 8 | `05_panel_regression.py` | Build component frames and legacy component sensitivities. |
| 9 | `05b_scientific_revision.py` | Fit the frozen five-parameter entry models, 1,999 bootstraps, event, functional-form, geographic, and reporting-state diagnostics, and raw-kW models. |
| 10 | `06_robustness.py` | Test component results across windows, weights, bounds, and within-episode designs. |
| 11 | `06a_data_quality_sensitivity.py` | Audit sample flow, ages, engineering bounds, heating values, and duplicates. |
| 12 | `06b_identifier_gap_audit.py` | Audit official-code gaps, code-regime resets, and restored lineage continuity. |
| 13 | `08_verify_claims.py` | Verify registered paper-facing claims and stale-language guards. |

The numbering is historical; the order in `07_rebuild_analysis.py` is authoritative.
`03_grid_emission_factors.py` remains available only as a noncanonical contextual
stage and is not evidence for the current paper.

## Shared Contracts

- `analysis/identity_utils.py` owns deterministic identity matching and asset-episode rules.
- `analysis/panel_utils.py` owns sample definitions, engineering validity, and model-frame construction.
- `analysis/rare_event_utils.py` owns Firth logistic fitting and stable-lineage bootstrap routines.
- `stable_site_id` is an audited administrative lineage, not proof of one immutable physical site.
- Official facility code cannot serve as a persistent panel key: it is absent in FY2010-FY2012 and has zero overlap from FY2019 to FY2020.
- Administrative disappearance is not modeled as physical closure.
- Gross MWh/t is a descriptive output ratio, not an independent efficiency outcome.

## Commands

```bash
npm run analysis:rebuild
npm run review:simulate:linkage
npm run paper:sync
npm run paper:check
npm run claims:verify
npm run paper:export:nopdf
npm run paper:build:latex
npm run paper:build:professor
npm run repo:check
```

Do not hand-edit `output/`, `output/manifests/`, `paper/evidence/current/`, or generated submission files to compensate for code changes. Rebuild the evidence, synchronize the paper snapshot, and resolve any claim-check failure at its source.

Review simulations write only under `paper/notes/review/simulations/`. They are
not evidence, do not enter stage manifests, and must never be described as
human validation or peer review.
