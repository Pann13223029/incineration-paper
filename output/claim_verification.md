# Claim Verification Report

Repo-level check that thesis-facing claims stay synchronized with canonical outputs.

- Core manifest Python: 3.12.12
- Full panel: 23,599 observations across 2,948 facilities
- Adoption frame: risk set 13,770 / 2,035; model 11,717 / 1,915 / 140 events
- Adoption effects: age 2.3–3.2 pp less likely; capacity +0.39 pp per 100 t/day
- Pathway audit: 82 reset/rebuild-like, 38 continuity-like, 20 forward-dated/placeholder, 1 unresolved
- Regression frame: 5,683 observations across 1,016 facilities; within/total ratio 0.1499 (0.1795 pre-Fuku, 0.0956 post-Fuku)

## Result: PASS

- Passed checks: 11
- Failed checks: 0

## Passed Checks

- `manifest_consistency` `source_manifest_python`: Core stage manifests share Python 3.12.12
- `claim` `readme_topline_paragraph`: All snippets present across 11 target checks.
- `claim` `readme_headline_table`: All snippets present across 4 target checks.
- `claim` `architecture_summary`: All snippets present across 6 target checks.
- `claim` `architecture_key_findings`: All snippets present across 5 target checks.
- `claim` `thesis_core_claims`: All snippets present across 6 target checks.
- `forbidden_pattern` `readme_mermaid`: Forbidden pattern absent: ```mermaid
- `forbidden_pattern` `dominant_pathway_language`: Forbidden pattern absent: dominant pathway
- `forbidden_pattern` `route_to_large_gains_language`: Forbidden pattern absent: route to large gains in this panel
- `forbidden_pattern` `stale_architecture_age_effect`: Forbidden pattern absent: 1.5–2.2 pp
- `forbidden_pattern` `stale_architecture_capacity_effect`: Forbidden pattern absent: +1.47 pp per 100 t/day

## Failures

- None
