# AGENTS.md

Repository-wide guidance for coding and writing assistants.

## Purpose

This is a paper-first workspace derived from a defended thesis. Develop the paper without creating a second empirical truth or treating administrative records as stronger physical evidence than they are.

## Source Hierarchy

| Need | Canonical source | Rule |
|:--|:--|:--|
| Raw provenance and parser schema | `output/raw_data_provenance.md`, `output/raw_data_manifest.csv`, `output/raw_workbook_schema_map.csv` | Verify workbook and field claims here. |
| Identity and panel grain | `output/facility_identity_audit.md`, `data/processed/facility_identity_crosswalk.csv` | Treat `stable_site_id` as an audited administrative lineage only. |
| Samples and fleet facts | `output/sample_definition.md`, `output/fleet_decomposition.md`, `output/fleet_turnover_decomposition.md` | Verify counts, coverage, and endpoint composition before repeating them. |
| Entry results | `output/scientific_revision_results.md`, `output/revised_entry_results.csv`, `output/entry_standardized_risk.csv`, `output/entry_capacity_support.csv`, `output/entry_design_diagnostics.csv`, `output/entry_specification_summary.csv`, `output/entry_sample_flow.csv`, `output/revised_entry_robustness.csv`, `output/entry_state_audit.csv`, `output/adoption_results.md` | Use the revision-frozen five-parameter Firth model as primary; disclose support and temporal collinearity and retain the higher-dimensional model as sensitivity. |
| Generator component results | `output/scientific_revision_results.md`, `output/raw_quantity_component_results.csv`, `output/common_control_component_decomposition.csv`, `output/generator_component_results.csv` | Lead with raw installed capacity; distinguish the utilization-adjusted factor model from the shared-control identity decomposition. |
| Linkage validation | `output/linkage_validation_protocol.md`, `output/linkage_validation_packet.csv` | A generated blinded packet is not completed independent validation. Do not expose the answer key in paper-facing evidence. |
| Robustness and quality | `output/robustness_results.md`, `output/data_quality_sensitivity.md`, `output/identifier_gap_audit.md` | Keep limitations visible. |
| Claim synchronization | `output/claim_verification.md`, `output/claim_evidence_map.md` | Run `npm run claims:verify` after claim edits. |
| Public journal prose | `paper/manuscript/paper.md`, `paper/manuscript/paper.tex` | Keep Markdown and LaTeX semantically synchronized. |
| Professor prose | `paper/manuscript/professor/paper.md`, `paper/manuscript/professor/paper.tex` | Preserve comprehensive explanation while using the same empirical evidence. |
| Paper-facing evidence | `paper/evidence/current/` | Generated copies; never hand-edit. |
| Thesis baseline | `legacy/` | Reference-only unless explicitly targeted. |

## Non-Negotiable Empirical Rules

1. Do not key longitudinal analysis directly on official facility code. Codes are absent in FY2010-FY2012 and reset completely between FY2019 and FY2020.
2. Describe `stable_site_id` as an audited administrative facility lineage, not one proven immutable physical site.
3. Describe `asset_episode_id` as a reported configuration episode, not a verified engineering asset.
4. Define entry as the first reported positive installed electrical-generation capacity after observed non-generation. Do not automatically call it a retrofit, replacement, or commissioning date.
5. Use Firth bias reduction for the sparse entry models and preserve exact-year and prior-operation frame distinctions.
6. Do not model administrative disappearance as closure without external closure histories.
7. Separate facility participation, throughput coverage, and waste-processing design-capacity share.
8. Treat annual participation as a repeated cross-section; separate endpoint composition from within-lineage change and never call endpoint-only records verified openings or closures.
9. Separate generator design intensity from annual electrical capacity factor.
10. Treat gross MWh/t as an administrative gross-output ratio, not net export, useful heat, lifecycle benefit, or independent efficiency.
11. Keep all claims observational unless a valid identification design is added.
12. Use the revision-frozen five-parameter Firth entry model as primary; describe the earlier eleven-parameter model as sensitivity only.
13. Do not call the linkage independently validated until a second reviewer has completed the blinded packet and disagreements have been adjudicated.

## Current Sample Contract

- 23,599 parsed source rows become 23,593 unique retained records.
- The identity layer contains 1,690 stable administrative lineages and 1,767 asset episodes; 16 accepted uncertain links are exposed.
- FY2019-FY2020 has zero official-code overlap and 1,064 restored lineage links.
- The descriptive installed-capacity entry universe contains 55 events.
- The broad exact-year Firth frame contains 15,154 rows, 1,137 lineages, and 35 events.
- The prior-operation Firth frame contains 13,072 rows, 1,019 lineages, and 33 events.
- The same-episode sensitivity contains 15,095 rows, 1,135 lineages, and 24 events.
- The identity-certain sensitivity contains 15,107 rows, 1,130 lineages, and 35 events.
- The revision-frozen primary entry specification has five parameters and 1,999 complete whole-lineage bootstrap replications per frame; it was not externally preregistered.
- The broad 300-versus-100 t/day odds ratio is 6.72 (95% bootstrap interval 4.31-12.46); all event attacks retain 6.12-7.30.
- Standardized over the broad risk frame, annual entry is 2.53 versus 16.66 per 1,000 facility-years at 100 and 300 t/day, a difference of 14.13 per 1,000.
- The 300 t/day level is at the 98.98th empirical percentile, with 315 risk rows and four events at or above it; support-aware predictions at 24, 60, and 120 t/day are 0.68, 1.37, and 3.29 per 1,000.
- Calendar and logged elapsed risk correlate at 0.909 and have VIFs 5.76 and 6.15; the processing-scale VIF is 1.10.
- The earlier flexible eleven-parameter temporal specification gives an OR of 6.13 (95% lineage-bootstrap interval 3.92-11.21) and remains sensitivity evidence.
- Alternative capacity transforms retain odds ratios of 4.22-5.01; leave-one-event-prefecture fits retain 6.14-7.18; the 30-event two-prior-year reporting-state sensitivity gives 6.21.
- Forty-nine panel rows across six lineages report positive output without positive reported capacity; no modeled event has positive output in its immediately prior year.
- The exact modeled events comprise 24 continuity-lineage and 11 rebuild/replacement-like entries.
- The generator component frame contains 6,511 engineering-valid rows across 493 lineages.
- The raw installed-kW processing-scale elasticity is 1.532; older cohorts have smaller adjusted kW but not lower annual capacity factors.
- In the shared-control decomposition, sizing is the largest component of every older-cohort log gross-intensity gap; excluding 14 cohort-switching lineages retains 6,291 rows across 479 lineages and the same ordering.
- In FY2024, installed capacity appears in 41.1% of all records and 46.4% of 879 positive-throughput records; positive output appears in 40.4% and 46.6%, respectively. Positive-output facilities cover 80.1% of throughput, while installed-generation facilities hold 70.5% of waste-processing design capacity.
- From FY2005 to FY2024, all-record installed prevalence rises 19.50 points, compared with 2.19 among 732 endpoint-common lineages and 0.88 among 678 endpoint-common same-episode lineages.

If regenerated outputs disagree, stop and resolve the pipeline before updating prose.

## Editing Rules

1. Change analytical logic in `code/analysis/`, then regenerate `output/`.
2. Never hand-edit generated outputs, manifests, synchronized evidence, or submission exports to conceal drift.
3. Run `npm run paper:sync` after canonical evidence changes.
4. Add a verifier rule when adding a high-risk numerical or methodological claim.
5. Put essential definitions and limitations in the main text; move technical overflow to the supplement.
6. Preserve the `legacy/` boundary unless the task explicitly targets the thesis.
7. Do not revive superseded sample counts, code-keyed panel language, closure claims, or a one-equation gross-output efficiency interpretation.

## Workflow Gates

| Change | Required gate |
|:--|:--|
| Paths or navigation | `npm run repo:check` |
| Prose only | `npm run claims:verify`; rebuild the affected artifact |
| Empirical claim | Check canonical output; run `npm run claims:verify` |
| Analysis, identity, or sample logic | `npm run analysis:rebuild`, `npm run paper:sync`, `npm run paper:check`, `npm run claims:verify` |
| Public submission artifacts | `npm run paper:export:nopdf`, `npm run paper:build:latex` |
| Professor reading artifact | `npm run paper:build:professor` |
| Before push | `npm run repo:check`, `npm run paper:check`, `npm run claims:verify`, `git diff --check` |

`code/analysis/07_rebuild_analysis.py` is the canonical stage orchestrator. Do not maintain an alternative hidden stage sequence.

## Writing Defaults

- Audience: waste management, industrial ecology, environmental policy, and technically literate non-specialists.
- Contribution: a count-volume decomposition, a sparse-event entry model, and an engineering component decomposition in one national administrative panel.
- Language: precise, calibrated, and readable; define abbreviations and jargon on first use.
- Mechanisms: plausible interpretations, not identified causes.
- Generalization: Japan is the case; external validity must be argued rather than assumed.
- Climate claims: do not infer avoided emissions without an explicit counterfactual and verified net-output data.

When workflow boundaries change, update `README.md`, `ARCHITECTURE.md`, this file, `code/README.md`, `data/README.md`, and `paper/README.md` together.
