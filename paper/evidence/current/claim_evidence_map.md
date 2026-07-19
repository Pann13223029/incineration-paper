# Claim-to-Evidence Map

This map identifies the generated artifacts behind the paper's defensible claims. It does not elevate descriptive associations into causal effects.

## Raw Sources And Longitudinal Identity

Claim: the panel contains 1,690 reconstructed stable administrative lineages and 1,767 asset episodes; official codes are not persistent across the FY2019-FY2020 regime break. Across FY2009-FY2013, 882 official codes overlap while 1,135 administrative lineages are linked.

Evidence: `output/raw_data_manifest.csv`, `output/raw_workbook_schema_map.csv`, `output/raw_data_provenance.md`, `data/processed/facility_identity_crosswalk.csv`, `output/facility_identity_audit.md`, and `output/identity_low_margin_links.csv`.

## Fleet Coverage And Endpoint Composition

Claim: installed capacity appears in 41.1% of all records and 46.4% of positive-throughput records; positive output appears in 40.4% and 46.6%, respectively. Positive-output facilities handle 80.1% of recorded throughput; installed-generation facilities hold 70.5% of waste-processing design capacity. From FY2005 to FY2024, all-record installed prevalence rises 19.50 points, compared with 2.19 among 732 endpoint-common lineages and 0.88 among 678 endpoint-common same-episode lineages.

Evidence: `output/fleet_decomposition.csv`, `output/fleet_turnover_decomposition.csv`, `output/fleet_turnover_decomposition.md`, `output/fy2024_fleet_segments.csv`, and `output/fleet_decomposition.md`.

## First Reported Installed-Generation Capacity

Claim: Firth bias-reduced hazards use 35 exact-year events in the broad frame, 33 following positive prior-lineage operation, and 24 in the same-episode sensitivity. The identity-certain sensitivity retains 35 events after excluding every lineage containing an accepted uncertain link. The revision-frozen five-parameter primary 300-versus-100 t/day OR is 6.72 (95% lineage-bootstrap interval 4.31-12.46). Event attacks retain 6.12-7.30; alternative capacity transforms retain 4.22-5.01; and leave-one-event-prefecture fits retain 6.14-7.18. Standardized annual entry is 2.53 versus 16.66 per 1,000 facility-years; the flexible temporal-form OR is 6.13. The 300-t/day level is at the 98.98th empirical percentile, with 315 risk rows and 4 events at or above it; predictions at 24/60/120 t/day are 0.68/1.37/3.29 per 1,000. The nested frames and diagnostics are not interpreted as independent equivalence tests.

Evidence: `output/revised_entry_results.csv`, `output/revised_entry_bootstrap.csv`, `output/revised_entry_influence.csv`, `output/revised_entry_robustness.csv`, `output/entry_standardized_risk.csv`, `output/entry_capacity_support.csv`, `output/entry_design_diagnostics.csv`, `output/entry_specification_summary.csv`, `output/entry_sample_flow.csv`, `output/entry_state_audit.csv`, and `output/scientific_revision_results.md`. The earlier eleven-parameter estimates remain labeled sensitivity evidence in `output/adoption_results.md`.

## Generator Design And Annual Operation

Claim: the primary generator analysis separates generator design intensity from electrical capacity factor on 6,511 engineering-valid rows across 493 stable administrative lineages. After generator sizing is added, the age coefficient is -0.0020 (p=0.2977); model R-squared changes from 0.4737 to 0.8131. Only 5 retained capacity-factor rows exceed 1.00 under the audited 1.20 administrative bound.
Under identical controls, the pre-1990 design, capacity-factor, and negative-utilization components are -1.565, 0.016, and 0.299; they sum exactly to the direct log gross-intensity gap of -1.250.

Evidence: `output/generator_component_results.csv`, `output/common_control_component_decomposition.csv`, `output/table2_generator_components_by_cohort.md`, `output/figure3_persistence.csv`, and `output/regression_results.md`.

## Prohibited Interpretations

- Do not infer closure or exit from disappearance of an official facility code.
- Do not treat the prior-operation sensitivity as a separately identified active-conversion process.
- Do not interpret a blank installed-capacity field as verified physical absence.
- Do not label gross MWh/t as net efficiency, useful heat, R1 efficiency, or lifecycle benefit.
- Do not present age or waste-processing utilization as independent gross-performance effects after generator sizing.
