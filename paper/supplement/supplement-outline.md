# Supplement Outline

## Purpose

Keep the main paper readable while making provenance, identity reconstruction,
sample construction, sparse-event inference, engineering decomposition,
robustness, and publication-integrity controls fully auditable.

## Fixed Section Order

1. Purpose, scope, interpretation rules, and abbreviations
2. Raw data provenance and workbook schema reconstruction
3. Stable administrative-lineage reconstruction and executable guardrails
4. Fleet, event-risk-set, and pathway sample construction
5. Firth discrete-time entry model, lineage bootstrap, and continuity/linkage sensitivities
6. Engineering variables, accounting identity, component models, and sizing diagnostic
7. Full robustness ladder
8. Post-entry bridge and trajectory caveats
9. Reproducibility and generated-evidence trace
10. Ethics, data availability, COPE-facing controls, and AI declaration
11. Residual limitations
12. Selected references already used by the manuscript

## Canonical Evidence Snapshot

- 20 MOE workbooks spanning FY2005-FY2024, with full SHA-256 and schema maps;
  checkout mtime unavailable, with last-Git-commit time recorded separately.
- 23,599 parsed rows; 23,593 unique records after six exact-duplicate collapses.
- 1,690 stable administrative lineages; 1,767 asset episodes; zero duplicate lineage-years.
- FY2010-FY2012 official codes absent; FY2019-FY2020 code overlap 0 versus 1,064 audited lineage links.
- 16 accepted uncertain links exposed with two-sided margins plus golden-link and invariance guardrails.
- 55 descriptive entry events; 35 broad exact-year, 33 prior-operation, and 24 same-episode events; identity-certain retains 35.
- Firth bias reduction, 499 complete stable-lineage cluster-bootstrap replications, and four estimand/sensitivity frames.
- 6,511 engineering-valid generating observations across 493 lineages.

## Mandatory Technical Content

- State the exact event definition and distinguish the two separate 35-event counts.
- Show the Firth objective and the discrete-time risk specification.
- Cite Firth (1993) and Heinze and Schemper (2002) for bias reduction and sparse separation.
- Define `G`, `T`, `K`, `C_w`, `U`, generator design intensity, and electrical capacity factor.
- Show `G/T = [K/C_w] x [G/(K x 8.76)] x [8.76/(365U)]`.
- Report predeclared engineering bounds without presenting trimmed values as observed values.
- Include calendar, weighting, bound, FE, first-difference, link-function, and bootstrap checks.
- Keep pathway evidence descriptive and explicitly disclose small cells and follow-up conditioning.
- Keep data, authorship, AI, correction, and related-publication responsibilities explicit.

## Prohibited Framing

- Do not use annual official codes as persistent identities.
- Do not infer a physical intervention from first reported installed capacity.
- Do not label gross MWh/t as net, thermal, lifecycle, or stand-alone technical performance.
- Do not present age or waste utilization as independent gross-output results after generator sizing.
- Do not make causal claims from pathway labels, cohort contrasts, FE models, or first differences.
- Do not restore superseded samples, counts, or analyses from earlier drafts.

## Evidence Sources

All quantitative text must trace to current generated files in `output/`, especially
the raw provenance, facility identity, identifier-gap, sample-definition,
data-quality, adoption, pathway, fleet-decomposition, component-regression, and
robustness artifacts. Stage manifests under `output/manifests/` are the canonical
machine-readable metadata layer.
