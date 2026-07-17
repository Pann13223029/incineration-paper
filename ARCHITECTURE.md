# Paper Repository Architecture

This document defines ownership, data flow, and verification boundaries. Use [`README.md`](README.md) for the public-facing overview.

## Design Contract

1. Maintain one canonical empirical pipeline.
2. Separate administrative identity reconstruction from physical-asset claims.
3. Keep paper prose and exports downstream of generated evidence.
4. Make every high-risk headline traceable to an output artifact.
5. Keep the defended thesis behind an explicit archive boundary.

## Ownership Layers

| Layer | Paths | Responsibility | Edit rule |
|:--|:--|:--|:--|
| Raw and processed data | `data/` | Checked-in source workbooks and reproducible analytical data | Change only through an explicit data or parsing task. |
| Analysis | `code/analysis/` | Parsing, provenance, identity, estimation, audits, and claim verification | This layer defines empirical logic. |
| Canonical evidence | `output/`, `output/manifests/` | Generated facts, tables, diagnostics, and stage manifests | Never hand-edit to repair prose. |
| Paper-facing evidence | `paper/evidence/current/` | Synchronized copies selected from `output/` | Regenerate with `npm run paper:sync`. |
| Active paper | `paper/manuscript/`, `paper/supplement/`, `paper/figures/` | Reader-facing interpretation and presentation | Claims must remain downstream of canonical evidence. |
| Distribution | `paper/submission/`, `paper/share/` | Review and submission artifacts | Build outputs, not analytical sources. |
| Publication tooling | `code/publishing/` | Sync, export, PDF, slide, and repository checks | Change when build behavior changes. |
| Archived thesis | `legacy/` | Defended baseline and historical support material | Reference-only unless explicitly targeted. |
| Guidance | `README.md`, `ARCHITECTURE.md`, `AGENTS.md` | Navigation and workflow contracts | Update when boundaries or commands change. |

## Source Hierarchy

When two files disagree, use this order:

1. Raw workbooks plus `output/raw_data_manifest.csv` and `output/raw_workbook_schema_map.csv` establish source provenance.
2. `data/processed/incineration_panel_identified.csv` and `data/processed/facility_identity_crosswalk.csv` establish the audited analytical grain and lineage fields.
3. Generated `output/*.md`, `output/*.csv`, and `output/manifests/*.json` establish samples, estimates, and diagnostics.
4. `paper/evidence/current/*` is a byte-synchronized convenience copy of selected output files.
5. The public and professor manuscript profiles plus the shared supplement interpret the evidence.
6. `paper/submission/*` and `paper/share/*` are distribution artifacts only.

Each profile's Markdown and LaTeX sources must agree semantically. Both profiles
use the same canonical evidence; neither may override a generated result.

The root `paper/manuscript/paper.*` sources own the public journal draft.
`paper/manuscript/professor/paper.*` preserves the comprehensive supervision
content and presents it through an A4 graduation-thesis profile. The profiles
may differ in explanation and placement, but not in
definitions, estimates, uncertainty, or evidence boundaries.

## Canonical Stage Flow

`code/analysis/07_rebuild_analysis.py` is the stage orchestrator and runs this order:

```text
data/raw/facility_annual/*
  -> 02b_build_raw_data_manifest.py
       hash workbooks and record URLs, sheets, headers, and selected columns
  -> 02_parse_facility_panel.py
       parse 23,599 source rows
  -> 02a_build_facility_identity.py
       collapse exact duplicates; retain 23,593 records; build audited lineages
  -> 02c_build_linkage_validation_packet.py
       generate a blinded clerical-review packet and separate answer key
  -> 04_eda_facility.py
       audit descriptive and model-frame inputs
  -> 05_fleet_decomposition.py
       separate facility participation, throughput coverage, and design capacity
  -> 05a_power_adoption.py
       estimate first reported installed-capacity entry with Firth logistic models
  -> 05_panel_regression.py
       estimate generator design-intensity and electrical-capacity-factor components
  -> 05b_scientific_revision.py
       fit the frozen five-parameter entry models, event attacks, and raw-kW models
  -> 06_robustness.py
  -> 06a_data_quality_sensitivity.py
  -> 06b_identifier_gap_audit.py
       test model stability, data bounds, and identifier continuity
  -> 08_verify_claims.py
       verify registered paper-facing claims and stale-language guards
  -> output/*
```

Stage numbering preserves historical filenames; execution order is authoritative.

`03_grid_emission_factors.py` is a retained optional legacy/context stage. It is
not called by the canonical paper rebuild because its regional factors and
counterfactual carbon interpretation are outside the current paper's verified
estimands.

## Identity Contract

The base survey cannot be treated as a ready-made panel keyed by official facility code:

- Official codes are completely absent in FY2010-FY2012.
- FY2019 and FY2020 have zero official-code overlap because the code regime changes.
- Audited record linkage restores 1,064 FY2019-FY2020 administrative-lineage links.
- Six exact duplicate source rows are collapsed, leaving 23,593 unique retained records.
- The current crosswalk contains 1,690 `stable_site_id` lineages and 1,767 `asset_episode_id` episodes.
- Sixteen accepted uncertain links are exposed with two-sided margins; whole-lineage sensitivities exclude their 14 lineages.

`stable_site_id` means an audited administrative facility lineage based on names, geography, reported start year, capacity, configuration, and code evidence. It does not prove one immutable physical site, continuous ownership, unchanged equipment, or physical closure. `asset_episode_id` marks reported configuration discontinuities within a lineage; it is not an engineering asset registry.

No model uses administrative disappearance as a physical closure outcome.

## Analytical Contracts

| Block | Current frame | Interpretation boundary |
|:--|:--|:--|
| Fleet coverage | FY2024: 41.1% facility participation, 80.1% throughput coverage, 70.5% design-capacity share | Count, flow, and capacity shares are distinct. |
| Descriptive installed-capacity entry | 55 events | First reported positive installed electrical-generation capacity after observed non-generation. |
| Broad exact-year Firth entry | 15,154 rows, 1,137 lineages, 35 events | Bias-reduced observational association with exact one-year administrative-lineage lags. |
| Prior-operation Firth entry | 13,072 rows, 1,019 lineages, 33 events | Nested sensitivity requiring positive prior operation. |
| Same-episode Firth entry | 15,095 rows, 1,135 lineages, 24 events | Continuity sensitivity excluding inferred asset-episode changes. |
| Identity-certain Firth entry | 15,107 rows, 1,130 lineages, 35 events | Linkage sensitivity excluding every lineage containing an accepted uncertain link. |
| Revised entry inference | 1,999 lineage bootstraps per frame; broad scale OR 6.72 (4.31-12.46) | Five-parameter primary model; all event attacks retain OR 6.12-7.30. |
| Generator components | 6,511 engineering-valid rows, 493 lineages | Leads with raw installed kW and separates installed design from annual capacity factor. |

Gross MWh/t is retained only as a descriptive accounting ratio and specification diagnostic. It is not named or interpreted as independent plant efficiency.

## Evidence Snapshot Contract

`code/publishing/20_sync_paper_assets.py` copies the following canonical outputs into `paper/evidence/current/`:

| Group | Synced files |
|:--|:--|
| Provenance | `raw_data_provenance.md`, `raw_data_manifest.csv`, `raw_workbook_schema_map.csv` |
| Identity and fleet | `facility_identity_audit.md`, `identity_low_margin_links.csv`, `linkage_validation_packet.csv`, `linkage_validation_protocol.md`, `fleet_decomposition.md`, `fleet_decomposition.csv`, `fy2024_fleet_segments.csv` |
| Core models | `sample_definition.md`, `scientific_revision_results.md`, `revised_entry_results.csv`, `revised_entry_bootstrap.csv`, `revised_entry_influence.csv`, `revised_entry_robustness.csv`, `entry_state_audit.csv`, `adoption_event_composition.csv`, `raw_quantity_component_results.csv`, `figure3_adjusted_components.csv`, `adoption_results.md`, `regression_results.md` |
| Robustness and quality | `robustness_results.md`, `robustness_component_results.csv`, `data_quality_sensitivity.md`, `data_quality_sample_flow.csv`, `data_quality_engineering_bounds.csv`, `data_quality_official_code_duplicates.csv` |
| Identifier audits | `identifier_gap_audit.md`, `identifier_overlap_by_year.csv`, `identifier_gap_bridges.csv`, `identifier_duplicates_by_year.csv` |
| Claim and summary outputs | `claim_evidence_map.md`, `claim_verification.md`, `panel_summary.md`, `table1_summary_stats.md`, `table2_generator_components_by_cohort.md` |
| Entry and trajectory detail | `adoption_pathway_audit.csv`, `figure2_transition_effects.csv`, `adoption_bootstrap_coefficients.csv`, `post_adoption_bridge.csv`, `post_adoption_trajectories.csv`, `figure3_persistence.csv` |

If a source changes, run `npm run paper:sync`; do not edit its copy. `npm run paper:check` compares source and copy bytes.

## Build And Verification Contracts

| Command | Contract |
|:--|:--|
| `npm run analysis:rebuild` | Execute the full empirical stage sequence and regenerate canonical evidence. |
| `npm run analysis:test` | Run closed-form and independent-optimizer benchmarks for the custom Firth estimator. |
| `npm run paper:sync` | Refresh the selected paper-facing evidence snapshot. |
| `npm run paper:check` | Fail on missing or stale snapshot files. |
| `npm run claims:verify` | Check registered numerical claims, required disclosures, and stale wording. |
| `npm run paper:export:nopdf` | Export Markdown, HTML, and DOCX from the Markdown manuscript. |
| `npm run paper:build:latex` | Build figures and the LaTeX reading PDF. |
| `npm run paper:build:professor` | Build the A4 professor-facing graduation-thesis PDF. |
| `npm run repo:check` | Check ownership paths, Markdown links, and journal-format gates. |

The public reading PDF is built from `paper/manuscript/paper.tex` and copied to
`paper/share/waste-management-manuscript-latex.pdf`. The professor thesis PDF
is built from `paper/manuscript/professor/paper.tex` and copied to
`paper/share/professor-review-thesis.pdf`; the former
`paper/share/professor-review-manuscript-latex.pdf` path remains a compatibility
alias. The HTML/DOCX export follows
the public Markdown profile.

CI should call the same orchestrator and package commands rather than duplicate a private stage list. Platform-sensitive figure binaries and convenience PDFs may differ at the byte level; source data, analytical tables, and claim checks must not drift.

## Change Gates

| Change | Minimum gate |
|:--|:--|
| Navigation or path change | `npm run repo:check` |
| Paper prose without empirical changes | `npm run claims:verify` and the relevant artifact build |
| New or revised empirical claim | Confirm `output/*`, then run `npm run claims:verify` |
| Sample, identity, or model change | `npm run analysis:rebuild`, `npm run paper:sync`, `npm run paper:check`, `npm run claims:verify` |
| Estimator implementation change | `npm run analysis:test`, then the full sample/model gate above |
| Public submission refresh | `npm run paper:export:nopdf` and `npm run paper:build:latex` |
| Professor reading refresh | `npm run paper:build:professor` |
| Pre-push | `npm run repo:check`, `npm run paper:check`, `npm run claims:verify`, `git diff --check` |

## Verification Boundary

Claim verification checks registered high-risk statements and stale-language patterns. It does not prove that every interpretation is correct, replace source inspection, validate physical identity, or turn observational estimates into causal effects. New high-risk claims require both generated evidence and a deliberate verifier rule.

The archived `legacy/` tree is outside the active claim gate unless a task explicitly targets it.
