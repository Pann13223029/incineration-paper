# Claim Verification Report

This report verifies generated evidence first, then checks the manuscript, LaTeX, supplement, and professor lineage against the resulting canonical metrics.

## Result: PASS

- Passed checks: 80
- Failed checks: 0

## Canonical Evidence

- Identity: 23,593 retained rows from 23,599 raw rows, 1,690 stable administrative lineages, 1,767 asset episodes, 0 duplicate lineage-years.
- FY2019-FY2020 continuity: 0 official-code overlap versus 1,064 administrative-lineage overlap.
- FY2024 fleet: 41.1% facility participation, 80.1% throughput coverage, 70.5% installed design-capacity share.
- Firth entry frames: 15,154/1,137/35 broad and 13,072/1,019/33 prior-operation and 15,095/1,135/24 same-episode and 15,107/1,130/35 identity-certain rows/lineages/events.
- Entry inference: OR 6.13 for 300 versus 100 t/day; lineage-bootstrap joint-age p-values are 0.380 broad, 0.186 prior-operation, and 0.051 same-episode, and 0.357 identity-certain.
- Components: 6,511 rows across 493 stable administrative lineages; sizing-adjusted age -0.0020 (p=0.2977); R-squared 0.4737 to 0.8131.

## Failures

- None

## Passed Checks

- `evidence_integrity::core_manifest_python` [n/a]: Core manifest Python versions: 3.12.12
- `evidence_integrity::canonical_stage_hashes` [n/a]: All canonical stage script, analysis-code, input, and output hashes match.
- `evidence_integrity::raw_workbook_hashes` [n/a]: Recomputed SHA-256 for 20 workbooks; mismatches: none
- `evidence_integrity::raw_schema_grain` [n/a]: Schema-map duplicate year-fields: 0; fields per year: [19]
- `evidence_integrity::retrieval_time_boundary` [n/a]: Original retrieval time and volatile checkout mtime are explicitly unavailable; deterministic repository commit timestamps are separate.
- `evidence_integrity::provenance_manifest_sync` [n/a]: Provenance CSV has 20/20 present/configured; stage manifest agrees.
- `evidence_integrity::stable_site_unique_grain` [n/a]: Duplicate stable-lineage-year rows: 0
- `evidence_integrity::identity_duplicate_and_episode_guards` [n/a]: Collapsed exact duplicate rows: 6; unique canonical record IDs: True; continued episode start-year resets >=3 years: 0.
- `evidence_integrity::identity_executable_guardrails` [n/a]: Golden, permutation, insertion, threshold, two-sided-margin, and uncertainty-exposure guardrails agree; 16 accepted uncertain links across 14 lineages are exposed exactly once.
- `evidence_integrity::identity_manifest_sync` [n/a]: Recomputed 23,593 retained records, 1690 stable administrative lineages, 1767 asset episodes, and FY2019-FY2020 overlaps 0 official/1064 stable.
- `evidence_integrity::official_code_regime_break` [n/a]: FY2019-FY2020 official-code overlap is 0; administrative-lineage overlap is 1064.
- `evidence_integrity::fy2024_fleet_arithmetic` [n/a]: FY2024 recomputed facility/throughput/valid-throughput shares: 41.124260/80.098728/79.671588%.
- `evidence_integrity::fleet_decomposition_identity` [n/a]: Maximum fleet decomposition identity error: 0.000e+00
- `evidence_integrity::fy2024_segment_totals` [n/a]: FY2024 segment rows sum to 1014; facility shares sum to 100.000000%.
- `evidence_integrity::fleet_manifest_sync` [n/a]: FY2024 fleet CSV and stage manifest headline metrics agree.
- `evidence_integrity::firth_method_and_sample_sync` [n/a]: Firth samples are 15154/1137/35 broad and 13072/1019/33 prior-operation and 15095/1135/24 same-episode and 15107/1130/35 identity-certain rows/lineages/events.
- `evidence_integrity::adoption_estimand_configuration` [n/a]: Primary entry is broad administrative-lineage entry; same-episode sensitivity excludes 59 rows and 11 events.
- `evidence_integrity::firth_convergence` [n/a]: Firth convergence metadata: {'broad': {'converged': True, 'iterations': 18}, 'identity_certain': {'converged': True, 'iterations': 18}, 'prior_operation': {'converged': True, 'iterations': 21}, 'same_episode_continuity': {'converged': True, 'iterations': 28}}
- `evidence_integrity::firth_estimates_finite` [n/a]: All 16 focal Firth estimates and uncertainty fields are finite.
- `evidence_integrity::cluster_bootstrap_joint_tests` [n/a]: Cluster-bootstrap joint tests: {'broad_cluster_bootstrap_covariance': [3.076452, 3, 0.3799873, 499], 'broad_model_based': [4.784085, 3, 0.1883077], 'identity_certain_cluster_bootstrap_covariance': [3.236333, 3, 0.3566027, 499], 'identity_certain_model_based': [4.793329, 3, 0.1875714], 'prior_operation_cluster_bootstrap_covariance': [4.809944, 3, 0.1862548, 499], 'prior_operation_model_based': [5.807285, 3, 0.1213721], 'same_episode_cluster_bootstrap_covariance': [7.779455, 3, 0.05079653, 499], 'same_episode_model_based': [11.36422, 3, 0.009910937]}
- `evidence_integrity::cluster_bootstrap_sync` [n/a]: Stable-lineage bootstrap repetitions by model: {'broad': 499, 'identity_certain': 499, 'prior_operation': 499, 'same_episode_continuity': 499}
- `evidence_integrity::pathway_and_bridge_sync` [n/a]: Pathway events: 55 descriptive, 55 exact; bridge rows: 55.
- `evidence_integrity::post_entry_trajectory_sync` [n/a]: Event-time-one pathway rows and component ranks match adoption metadata.
- `evidence_integrity::component_sample_sync` [n/a]: Component output has 9 terms on 6511 engineering-valid rows and 493 stable administrative lineages.
- `evidence_integrity::component_estimates_finite` [n/a]: All component-model focal estimates and uncertainty fields are finite.
- `evidence_integrity::diagnostic_manifest_sync` [n/a]: Generated diagnostic coefficients and p-values match the stage manifest for 4 terms.
- `document_presence::manuscript_md_present` [paper/manuscript/paper.md]: Required document exists.
- `document_presence::manuscript_tex_present` [paper/manuscript/paper.tex]: Required document exists.
- `document_presence::supplement_present` [paper/supplement/supplement.md]: Required document exists.
- `document_presence::professor_lineage_present` [paper/notes/positioning/professor-comparator-method-lineage.md]: Optional lineage checked when present.
- `required_claim::stable_site_identity` [paper/manuscript/paper.md]: Explain administrative-lineage identity and report 1,690 lineages and 1,767 asset episodes.
- `required_claim::official_code_break` [paper/manuscript/paper.md]: Disclose the FY2019-FY2020 official-code regime break and explain why official codes are not longitudinal identities.
- `required_claim::fy2024_count_volume` [paper/manuscript/paper.md]: Report the FY2024 count-volume contrast: 41.1% facilities, 80.1% throughput, and 70.5% design capacity.
- `required_claim::firth_method_and_frames` [paper/manuscript/paper.md]: Name Firth/Jeffreys-prior bias reduction and report broad frame 15,154/1,137/35 plus prior-operation frame 13,072/1,019/33 and same-episode sensitivity 15,095/1,135/24; identity-certain sensitivity 15,107/1,130/35, with 499 lineage bootstraps.
- `required_claim::adoption_joint_inference_and_scale` [paper/manuscript/paper.md]: Report lineage-bootstrap joint-age p-values for broad, prior-operation, same-episode, and identity-certain frames (0.380/0.186/0.051/0.357) and scale contrast OR=6.13.
- `required_claim::engineering_components` [paper/manuscript/paper.md]: Separate generator design intensity from electrical capacity factor and report 6,511 engineering-valid rows across 493 stable administrative lineages.
- `required_claim::sizing_diagnostic_conclusion` [paper/manuscript/paper.md]: State that the sizing-adjusted age coefficient is -0.0020 (p=0.2977) and that R-squared changes from 0.4737 to 0.8131.
- `required_claim::post_entry_pathway_results` [paper/manuscript/paper.md]: Report event-time-one pathway counts and ranks from the generated trajectory table.
- `required_claim::stable_site_identity` [paper/manuscript/paper.tex]: Explain administrative-lineage identity and report 1,690 lineages and 1,767 asset episodes.
- `required_claim::official_code_break` [paper/manuscript/paper.tex]: Disclose the FY2019-FY2020 official-code regime break and explain why official codes are not longitudinal identities.
- `required_claim::fy2024_count_volume` [paper/manuscript/paper.tex]: Report the FY2024 count-volume contrast: 41.1% facilities, 80.1% throughput, and 70.5% design capacity.
- `required_claim::firth_method_and_frames` [paper/manuscript/paper.tex]: Name Firth/Jeffreys-prior bias reduction and report broad frame 15,154/1,137/35 plus prior-operation frame 13,072/1,019/33 and same-episode sensitivity 15,095/1,135/24; identity-certain sensitivity 15,107/1,130/35, with 499 lineage bootstraps.
- `required_claim::adoption_joint_inference_and_scale` [paper/manuscript/paper.tex]: Report lineage-bootstrap joint-age p-values for broad, prior-operation, same-episode, and identity-certain frames (0.380/0.186/0.051/0.357) and scale contrast OR=6.13.
- `required_claim::engineering_components` [paper/manuscript/paper.tex]: Separate generator design intensity from electrical capacity factor and report 6,511 engineering-valid rows across 493 stable administrative lineages.
- `required_claim::sizing_diagnostic_conclusion` [paper/manuscript/paper.tex]: State that the sizing-adjusted age coefficient is -0.0020 (p=0.2977) and that R-squared changes from 0.4737 to 0.8131.
- `required_claim::post_entry_pathway_results` [paper/manuscript/paper.tex]: Report event-time-one pathway counts and ranks from the generated trajectory table.
- `required_claim::supplement_identity_audit` [paper/supplement/supplement.md]: Document identity audit counts, including official/stable FY2019-FY2020 overlaps 0/1,064 and duplicate lineage-years.
- `required_claim::supplement_raw_provenance` [paper/supplement/supplement.md]: Reference SHA-256 raw-file provenance, explicitly unavailable retrieval timestamps, and workbook schema/header mappings.
- `required_claim::supplement_firth_inference` [paper/supplement/supplement.md]: Document Firth estimation, 499 cluster-bootstrap repetitions, broad joint-age p=0.380, and continuity sensitivity p=0.051.
- `required_claim::supplement_component_diagnostic` [paper/supplement/supplement.md]: Document both engineering components and the non-significant sizing-adjusted age result.
- `required_claim::lineage_current_design` [paper/notes/positioning/professor-comparator-method-lineage.md]: Explain the current administrative-lineage, Firth, design-intensity, and capacity-factor design.
- `required_claim::lineage_current_headlines` [paper/notes/positioning/professor-comparator-method-lineage.md]: Report current count-volume, joint-age, continuity, and sizing-diagnostic headline values in the professor lineage packet.
- `stale_phrase::panel_exit_claim` [paper/manuscript/paper.md]: Panel-exit evidence is invalid after the official-code regime break and must not remain.
- `stale_phrase::active_conversion_frame` [paper/manuscript/paper.md]: The old active-conversion frame is replaced by the prior-operation sensitivity.
- `stale_phrase::coded_longitudinal_frame` [paper/manuscript/paper.md]: Officially coded rows must not be framed as stable longitudinal units.
- `stale_phrase::stale_exact_event_count` [paper/manuscript/paper.md]: The superseded exact-code hazard sample must be removed.
- `stale_phrase::stale_active_sample` [paper/manuscript/paper.md]: The superseded active-conversion sample must be removed.
- `high_risk_claim::official_code_as_stable_id` [paper/manuscript/paper.md]: Official facility codes cannot be asserted as stable longitudinal IDs.
- `high_risk_claim::causal_regression_interpretation` [paper/manuscript/paper.md]: Observational regression terms must not be presented as causal effects.
- `stale_phrase::panel_exit_claim` [paper/manuscript/paper.tex]: Panel-exit evidence is invalid after the official-code regime break and must not remain.
- `stale_phrase::active_conversion_frame` [paper/manuscript/paper.tex]: The old active-conversion frame is replaced by the prior-operation sensitivity.
- `stale_phrase::coded_longitudinal_frame` [paper/manuscript/paper.tex]: Officially coded rows must not be framed as stable longitudinal units.
- `stale_phrase::stale_exact_event_count` [paper/manuscript/paper.tex]: The superseded exact-code hazard sample must be removed.
- `stale_phrase::stale_active_sample` [paper/manuscript/paper.tex]: The superseded active-conversion sample must be removed.
- `high_risk_claim::official_code_as_stable_id` [paper/manuscript/paper.tex]: Official facility codes cannot be asserted as stable longitudinal IDs.
- `high_risk_claim::causal_regression_interpretation` [paper/manuscript/paper.tex]: Observational regression terms must not be presented as causal effects.
- `stale_phrase::panel_exit_claim` [paper/supplement/supplement.md]: Panel-exit evidence is invalid after the official-code regime break and must not remain.
- `stale_phrase::active_conversion_frame` [paper/supplement/supplement.md]: The old active-conversion frame is replaced by the prior-operation sensitivity.
- `stale_phrase::coded_longitudinal_frame` [paper/supplement/supplement.md]: Officially coded rows must not be framed as stable longitudinal units.
- `stale_phrase::stale_exact_event_count` [paper/supplement/supplement.md]: The superseded exact-code hazard sample must be removed.
- `stale_phrase::stale_active_sample` [paper/supplement/supplement.md]: The superseded active-conversion sample must be removed.
- `high_risk_claim::official_code_as_stable_id` [paper/supplement/supplement.md]: Official facility codes cannot be asserted as stable longitudinal IDs.
- `high_risk_claim::causal_regression_interpretation` [paper/supplement/supplement.md]: Observational regression terms must not be presented as causal effects.
- `stale_phrase::panel_exit_claim` [paper/notes/positioning/professor-comparator-method-lineage.md]: Panel-exit evidence is invalid after the official-code regime break and must not remain.
- `stale_phrase::active_conversion_frame` [paper/notes/positioning/professor-comparator-method-lineage.md]: The old active-conversion frame is replaced by the prior-operation sensitivity.
- `stale_phrase::coded_longitudinal_frame` [paper/notes/positioning/professor-comparator-method-lineage.md]: Officially coded rows must not be framed as stable longitudinal units.
- `stale_phrase::stale_exact_event_count` [paper/notes/positioning/professor-comparator-method-lineage.md]: The superseded exact-code hazard sample must be removed.
- `stale_phrase::stale_active_sample` [paper/notes/positioning/professor-comparator-method-lineage.md]: The superseded active-conversion sample must be removed.
- `high_risk_claim::official_code_as_stable_id` [paper/notes/positioning/professor-comparator-method-lineage.md]: Official facility codes cannot be asserted as stable longitudinal IDs.
- `high_risk_claim::causal_regression_interpretation` [paper/notes/positioning/professor-comparator-method-lineage.md]: Observational regression terms must not be presented as causal effects.
