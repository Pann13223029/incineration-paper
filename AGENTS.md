# AGENTS.md

Repository-wide guidance for coding and writing assistants.

## Purpose

This is a paper-first workspace derived from a defended thesis. Develop the paper without creating a second empirical truth or treating administrative records as stronger physical evidence than they are.

## Source Hierarchy

| Need | Canonical source | Rule |
|:--|:--|:--|
| Raw provenance and parser schema | `output/raw_data_provenance.md`, `output/raw_data_manifest.csv`, `output/raw_workbook_schema_map.csv` | Verify workbook and field claims here. |
| Identity and panel grain | `output/facility_identity_audit.md`, `data/processed/facility_identity_crosswalk.csv` | Treat `stable_site_id` as an audited administrative lineage only. |
| Samples and fleet facts | `output/sample_definition.md`, `output/fleet_decomposition.md` | Verify counts and coverage before repeating them. |
| Entry results | `output/scientific_revision_results.md`, `output/revised_entry_results.csv`, `output/adoption_results.md` | Use the frozen five-parameter Firth model as primary; retain the higher-dimensional model as sensitivity. |
| Generator component results | `output/scientific_revision_results.md`, `output/raw_quantity_component_results.csv`, `output/generator_component_results.csv` | Lead with raw installed capacity and capacity factor; use ratio transformations only as supporting identities. |
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
8. Separate generator design intensity from annual electrical capacity factor.
9. Treat gross MWh/t as an administrative gross-output ratio, not net export, useful heat, lifecycle benefit, or independent efficiency.
10. Keep all claims observational unless a valid identification design is added.
11. Use the frozen five-parameter Firth entry model as primary; describe the earlier eleven-parameter model as sensitivity only.
12. Do not call the linkage independently validated until a second reviewer has completed the blinded packet and disagreements have been adjudicated.

## Current Sample Contract

- 23,599 parsed source rows become 23,593 unique retained records.
- The identity layer contains 1,690 stable administrative lineages and 1,767 asset episodes; 16 accepted uncertain links are exposed.
- FY2019-FY2020 has zero official-code overlap and 1,064 restored lineage links.
- The descriptive installed-capacity entry universe contains 55 events.
- The broad exact-year Firth frame contains 15,154 rows, 1,137 lineages, and 35 events.
- The prior-operation Firth frame contains 13,072 rows, 1,019 lineages, and 33 events.
- The same-episode sensitivity contains 15,095 rows, 1,135 lineages, and 24 events.
- The identity-certain sensitivity contains 15,107 rows, 1,130 lineages, and 35 events.
- The frozen primary entry specification has five parameters and 1,999 complete whole-lineage bootstrap replications per frame.
- The broad 300-versus-100 t/day odds ratio is 6.72 (95% bootstrap interval 4.31-12.46); all event attacks retain 6.12-7.30.
- The exact modeled events comprise 24 continuity-lineage and 11 rebuild/replacement-like entries.
- The generator component frame contains 6,511 engineering-valid rows across 493 lineages.
- The raw installed-kW processing-scale elasticity is 1.532; older cohorts have smaller adjusted kW but not lower annual capacity factors.
- FY2024 coverage is 41.1% by facility participation, 80.1% by throughput, and 70.5% by waste-processing design capacity.

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
