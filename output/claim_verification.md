# Claim Verification Report

Repo-level check that paper-facing claims stay synchronized with canonical outputs.

- Core manifest Python: 3.12.12
- Full panel: 23,599 observations across 2,948 facilities
- Capacity-entry frame: risk set 13,770 / 2,035; model 10,823 / 1,911 / 98 events
- Active-conversion frame: 9,215 / 1,663 / 58 events
- Entry effects: capacity +0.45 pp broad and +0.44 pp active; broad age −1.41/−1.45/−0.83 pp versus active age −0.67/−0.56/−0.29 pp
- Pathway audit: 50 reset/rebuild-like, 36 continuity-like, 12 forward-dated/placeholder, 42 timing-ambiguous, 1 unresolved
- Regression frame: 5,683 observations across 1,016 facilities; within/total ratio 0.1499 (0.1795 early coded, 0.0956 later coded)
- Primary generator model: age/vintage −0.0329, capacity +0.1103, utilization +0.7600; R2 0.3830
- Post-entry trajectory: 389 rows across 137 events

## Result: PASS

- Passed checks: 21
- Failed checks: 0

## Passed Checks

- `manifest_consistency` `source_manifest_python`: Core stage manifests share Python 3.12.12
- `claim` `readme_topline_paragraph`: All snippets present across 12 target checks.
- `claim` `readme_headline_table`: All snippets present across 8 target checks.
- `claim` `architecture_summary`: All snippets present across 12 target checks.
- `claim` `architecture_key_findings`: All snippets present across 4 target checks.
- `forbidden_pattern` `readme_mermaid`: Forbidden pattern absent: ```mermaid
- `forbidden_pattern` `stale_architecture_age_effect`: Forbidden pattern absent: 1.5–2.2 pp
- `forbidden_pattern` `stale_architecture_capacity_effect`: Forbidden pattern absent: +1.47 pp per 100 t/day
- `forbidden_pattern` `stale_readme_previous_observed_main_model`: Forbidden pattern absent: 11,717 facility-years across 1,915 facilities and 140 events
- `forbidden_pattern` `stale_readme_fukushima_shorthand`: Forbidden pattern absent: pre-Fuku
- `forbidden_pattern` `stale_manuscript_grid_control_md`: Forbidden pattern absent: grid-emission-factor control
- `forbidden_pattern` `stale_manuscript_grid_row_md`: Forbidden pattern absent: Grid EF
- `forbidden_pattern` `stale_manuscript_grid_row_tex`: Forbidden pattern absent: Grid EF
- `forbidden_pattern` `stale_supplement_grid_control`: Forbidden pattern absent: grid-emission factor
- `forbidden_pattern` `stale_universal_age_headline_md`: Forbidden pattern absent: younger and larger facilities
- `forbidden_pattern` `stale_universal_age_headline_tex`: Forbidden pattern absent: younger and larger facilities
- `forbidden_pattern` `stale_entry_pseudo_r2_md`: Forbidden pattern absent: 0.1829
- `forbidden_pattern` `stale_entry_pseudo_r2_tex`: Forbidden pattern absent: 0.1829
- `forbidden_pattern` `stale_persistence_overclaim_md`: Forbidden pattern absent: not easily erased
- `forbidden_pattern` `stale_official_share_md`: Forbidden pattern absent: only 41.1%
- `forbidden_pattern` `stale_official_share_tex`: Forbidden pattern absent: only 41.1\%

## Failures

- None
