# Claim-to-Evidence Map

This map identifies the generated artifacts behind the paper's defensible claims. It does not elevate descriptive associations into causal effects.

## Raw Sources And Longitudinal Identity

Claim: the panel contains 1,690 reconstructed stable administrative lineages and 1,767 asset episodes; official codes are not persistent across the FY2019-FY2020 regime break. Across FY2009-FY2013, 882 official codes overlap while 1,135 administrative lineages are linked.

Evidence: `output/raw_data_manifest.csv`, `output/raw_workbook_schema_map.csv`, `output/raw_data_provenance.md`, `data/processed/facility_identity_crosswalk.csv`, `output/facility_identity_audit.md`, and `output/identity_low_margin_links.csv`.

## FY2024 Count-Volume Contrast

Claim: installed-generation facilities are 41.1% of recorded facilities but positive-output facilities handle 80.1% of recorded throughput; installed-generation facilities hold 70.5% of waste-processing design capacity.

Evidence: `output/fleet_decomposition.csv`, `output/fy2024_fleet_segments.csv`, and `output/fleet_decomposition.md`.

## First Reported Installed-Generation Capacity

Claim: Firth bias-reduced hazards use 35 exact-year events in the broad frame, 33 following positive prior-lineage operation, and 24 in the same-episode sensitivity. The identity-certain sensitivity retains 35 events after excluding every lineage containing an accepted uncertain link. The 300-versus-100 t/day OR is 6.13; lineage-bootstrap joint-age p-values are 0.380, 0.186, and 0.051, with identity-certain p=0.357. The nested frames are not interpreted as an equivalence test.

Evidence: `output/figure2_transition_effects.csv`, `output/adoption_bootstrap_coefficients.csv`, `output/adoption_pathway_audit.csv`, and `output/adoption_results.md`.

## Generator Design And Annual Operation

Claim: the primary generator analysis separates generator design intensity from electrical capacity factor on 6,511 engineering-valid rows across 493 stable administrative lineages. After generator sizing is added, the age coefficient is -0.0020 (p=0.2977); model R-squared changes from 0.4737 to 0.8131.

Evidence: `output/generator_component_results.csv`, `output/table2_generator_components_by_cohort.md`, `output/figure3_persistence.csv`, and `output/regression_results.md`.

## Prohibited Interpretations

- Do not infer closure or exit from disappearance of an official facility code.
- Do not treat the prior-operation sensitivity as a separately identified active-conversion process.
- Do not label gross MWh/t as net efficiency, useful heat, R1 efficiency, or lifecycle benefit.
- Do not present age or waste-processing utilization as independent gross-performance effects after generator sizing.
