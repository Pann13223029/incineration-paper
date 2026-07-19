# Defense Red-Team Review And Revision Map

> **Historical review record.** This paper-oriented map contains estimates from
> an earlier model revision and must not be used for the current thesis defense.
> Use [Thesis Defense Rehearsal](thesis-defense-rehearsal-2026-07-18.md), which
> is synchronized to the five-parameter primary model and the current thesis.

Status: post-identity-remediation review for the professor-facing paper.

## Executive Verdict

The paper now has a coherent, defensible descriptive contribution:

- FY2024 generation participation is 41.1% by facility count but covers 80.1%
  of recorded waste throughput and 70.5% of waste-processing design capacity.
- First reported installed-capacity entry is rare and strongly scale-selective
  in Firth bias-reduced models.
- Joint tests do not support age as a general entry headline or a difference in
  the age pattern between the two prespecified frames.
- Among generators, reported vintage differences are concentrated in installed
  generator design intensity; age, processing capacity, and utilization are no
  longer independently significant after sizing is included in the separate
  specification diagnostic.

This is suitable for professor review after the manuscript, supplement, TeX,
tables, and figures all pass the same claim checks. It is not evidence of a
causal retrofit mechanism, thermodynamic efficiency, or an optimal policy.

## Current Evidence Baseline

| Item | Audited anchor |
|:--|:--|
| Longitudinal data | 23,593 retained records, 1,690 stable administrative lineages, 1,767 asset episodes; 16 accepted uncertain links exposed |
| FY2024 coverage | 41.1% facilities, 80.1% throughput, 70.5% design capacity |
| Descriptive entries | 55 first observed installed-capacity events |
| Broad exact-year Firth model | 15,154 lineage-years, 1,137 lineages, 35 events |
| Prior-operation Firth model | 13,072 lineage-years, 1,019 lineages, 33 events |
| Same-episode / identity-certain | 15,095/1,135/24 and 15,107/1,130/35 rows/lineages/events |
| Scale result | Odds ratio 6.13 and 6.25 for 300 versus 100 t/day |
| Age inference | Lineage-bootstrap joint p=0.380/0.186/0.051/0.357 across broad/prior/same-episode/identity-certain frames |
| Generator components | 6,511 engineering-valid rows, 493 stable administrative lineages |
| Sizing diagnostic | Separate 5,806-row, heating-value-plausible frame with heating value controlled: legacy age -0.0349, capacity +0.1001, utilization +0.6699; after sizing, age -0.0020 (p=0.2977), capacity -0.0092 (p=0.1991), utilization -0.0995 (p=0.2038), sizing +0.7532 (p<0.001), and R-squared 0.4737 to 0.8131; specification diagnostic, not causal mediation |

## Panel Protocol

| Persona | Primary attack | Required response |
|:--|:--|:--|
| Administrative-data auditor | Are reconstructed site histories real or an artifact of source coding and row order? | Show the six linkage remediations, audit tables, and executable invariance tests |
| Applied econometrician | Can 35 events support ordinary logistic claims or many interactions? | Use parsimonious Firth models, stable-lineage bootstrap intervals, and joint tests |
| Waste-to-energy engineer | Does gross MWh/t measure engineering efficiency? | Separate installed design intensity, electrical capacity factor, and waste loading |
| Waste Management editor | Does 41.1% imply most waste is processed without generation? | Lead with the 80.1% throughput and 70.5% design-capacity denominators |
| Professor/examiner | Which prior papers supplied the framework, and what is original? | Provide an explicit comparator-by-comparator adaptation map |
| Causal-inference skeptic | Do coefficients identify retrofit, policy, or aging effects? | State observational estimands and evidence boundaries at every conclusion point |
| Municipal reader | Does the paper rank investment targets? | Explain that it diagnoses fleet structure but does not estimate technical feasibility or intervention returns |

## Resolved Identity Blockers

These were blocking flaws in the first reconstructed identity layer. They are
retained here as resolved audit history because they changed the analytical
sample and claim set.

| ID | Red-team attack | Implemented fix | Executable acceptance condition |
|:--|:--|:--|:--|
| I1 | Reused or reassigned source facility codes could force unrelated names into one lineage | Added a **code-contradiction veto**: code agreement cannot override strongly conflicting name, start-year, capacity, or configuration evidence | Golden separation cases remain separate; contradiction cases are surfaced in the audit |
| I2 | A stale multi-year candidate could defeat an identical adjacent-year record, especially across the FY2019-FY2020 code reset | Match **adjacent years before gap candidates**, then apply explicit gap and recency penalties with deterministic tie-breaking | Golden continuity links cross the reset correctly; overlap and gap bridges are reported by year |
| I3 | Asset episodes split only on forward start-year changes and could miss backward resets or major asset changes | Use **symmetric episode resets** for material start-year changes plus major technology or capacity discontinuities | Episode-reset diagnostics contain no unexplained large backward jumps within an episode |
| I4 | Exact duplicate source rows could be assigned different lineage identities | Build canonical source-record fingerprints, **collapse exact duplicates**, and retain source multiplicity for audit | Exact duplicate signatures cannot produce multiple analytical lineage-years |
| I5 | Site IDs depended on source-row order and mutable row attributes | Seed deterministic IDs from **canonical fingerprints** and add shuffle and insertion invariance checks | Reordering rows or inserting unrelated rows leaves existing lineage assignments unchanged |
| I6 | Global assignment could accept sub-threshold or one-sided ambiguous links | Exclude sub-threshold and weak ambiguous edges before assignment, use unique unmatched choices, calculate current-row and prior-competitor margins, and expose every strong-evidence uncertain link | Zero accepted sub-threshold/weak ambiguous links; 16 accepted uncertain links appear exactly once in the generated audit and whole-lineage sensitivities |

The current identity layer retains 23,593 records in 1,690 lineages and 1,767
episodes. Passing these tests means deterministic administrative reconstruction,
not proof of physical continuity or unchanged ownership.

Primary audit sources:

- [facility identity audit](../../../output/facility_identity_audit.md)
- [identifier-gap audit](../../../output/identifier_gap_audit.md)
- [data-quality sensitivity](../../../output/data_quality_sensitivity.md)
- [raw-data provenance](../../../output/raw_data_provenance.md)

## Remaining Red-Team Findings

### R1 - High: sparse entry limits precision

The exact model has 35 events and the prior-operation model has 33. Firth bias
reduction addresses small-sample likelihood bias and separation, but it does not
create information. Bootstrap intervals and joint tests must remain visible.

Decision:

- keep the predictor set parsimonious
- headline the stable scale contrast
- report age coefficients but interpret the joint p-values
- compare the specified continuity and identity frames without treating nested samples as independent groups

### R2 - High: the scale association is not a capacity intervention effect

An odds ratio of 6.13 or 6.25 for 300 versus 100 t/day describes differences
between observed site profiles. It does not say that enlarging a 100 t/day site
would multiply its entry odds.

Decision:

- use `associated with` rather than `causes`
- explain likely selection channels as hypotheses only
- reserve mechanism tests for external project and facility histories

### R3 - High: generator constructs must remain separate

Gross MWh/t combines installed electrical sizing, annual generator use, and
waste loading. Calling it efficiency would confound design choice with operation
and fuel conditions.

Decision:

- make the engineering identity central
- use design intensity and electrical capacity factor as the primary outcomes
- label gross MWh/t an administrative gross-output ratio
- state that net export, useful heat, parasitic load, and lifecycle emissions are
  outside the measure

### R4 - Medium-High: reported start year is a vintage proxy

Year indicators and start-year cohorts support cross-facility vintage
comparisons, not clean within-plant physical aging effects. The sizing-added
diagnostic removes the earlier independent age result.

Decision:

- use `reported start-year cohort` or `vintage`, not degradation
- report age -0.0020 (p=0.2977) after sizing in the separate 5,806-row frame
  with plausible heating value and heating value controlled
- distinguish this specification diagnostic from the 6,511-row primary
  component models and do not describe it as causal mediation
- do not claim that aging has no physical effect; state only that this model does
  not isolate one

### R5 - Medium: count-volume divergence changes, but does not erase, the problem

The 80.1% throughput share shows that generating facilities already process most
recorded waste. The remaining 19.9% is not automatically recoverable because
technical, contractual, heat-demand, grid, and economic feasibility are absent.

Decision:

- frame 41.1% as participation, not national underperformance
- treat volume coverage as a denominator correction
- avoid multiplying non-generator tonnes by generator averages to claim a
  recoverable potential

### R6 - Medium: pathway labels are not physical histories

Continuity-lineage and rebuild/replacement-like categories are useful for bounding
interpretation. They are generated from administrative continuity and reset
signals, not permits, construction records, or engineering inspections.

Decision:

- keep pathway results descriptive
- state pathway sample sizes in every figure or table
- use external histories for any mechanism-centered follow-up

### R7 - Medium: comparator lineage must be demonstrable

A professor should see which questions, constructs, and presentation principles
were learned from close papers and how they were changed for this dataset.

Decision:

- retain the [professor comparator and method lineage](../positioning/professor-comparator-method-lineage.md)
- cite original methods for Firth bias reduction and close Japan studies
- distinguish adaptation from replication and from unsupported novelty claims

## Revision, Addition, And Removal Plan

| Priority | Action | Status | Acceptance gate |
|:--|:--|:--|:--|
| P0 | Repair identity reconstruction and rerun all dependent analyses | Complete | Six identity blockers have executable tests and generated audit evidence |
| P1 | Align research questions, abstract, methods, results, tables, and conclusion | In progress | Every active number matches generated evidence and every construct has one meaning |
| P2 | Make Firth inference and engineering equations professor-readable | In progress | A non-specialist can explain why each model and denominator is used |
| P3 | Remove obsolete models and interpretations from all public-facing artifacts | In progress | Repository-wide stale-term and stale-number scans pass |
| P4 | Rebuild synchronized evidence, TeX, and PDF | Pending full integration | Claim verification, repository checks, build logs, and visual inspection pass |
| P5 | Conduct professor-facing defense rehearsal | Pending | Answers below can be delivered without overstating the evidence |

Add:

- one explicit identity-reconstruction paragraph and supplement audit
- one plain-language Firth explanation beside the equation
- one engineering accounting identity and construct table
- one comparator adaptation paragraph
- one future-data paragraph naming external histories and engineering measures

Remove:

- any model whose outcome is merely absence from the next survey year
- any treatment of source facility codes as longitudinal site units
- old sample counts and event totals
- age-centered entry conclusions unsupported by joint tests
- gross-MWh/t efficiency language
- generic policy rankings and unsupported potential calculations

## Defense Questions

**Why does the paper matter if generating facilities already handle 80.1% of
throughput?**

Because the 41.1% count alone exaggerates the uncovered activity margin, while
the remaining margin is concentrated in different facilities. Correct
denominators change both the research question and the planning diagnosis.

**Is the main entry result just common sense that larger plants generate?**

The direction is intuitive; the contribution is the audited national risk set,
the magnitude under sparse-event inference, its stability across prespecified
frames, and the separation of entry scale from post-entry generator design.

**Why should I trust reconstructed identities?**

The source codes contain gaps and regime changes. The paper therefore uses
multiple administrative signals, explicit contradiction rules, deterministic
matching, duplicate collapse, low-margin disclosure, golden cases, and
permutation/insertion invariance tests. Residual linkage uncertainty is stated.

**Why use Firth regression?**

Only 35 and 33 events enter the two models. Firth's penalized likelihood reduces
small-sample bias and handles separation more reliably than ordinary maximum-
likelihood logistic regression, while bootstrap intervals show remaining
uncertainty.

**Does the paper show that old facilities are inefficient?**

No. Older reported cohorts have lower installed generator design intensity, but
in the separate 5,806-row diagnostic with plausible heating value and heating
value controlled, the age coefficient is -0.0020 with `p=0.2977` after sizing
is included. That specification check is not causal mediation and is distinct
from the 6,511-row primary component models. Gross MWh/t is not a thermodynamic
efficiency measure.

**What would justify a stronger causal paper?**

Verified construction and retrofit dates, policy eligibility, grid constraints,
fuel heating value, parasitic consumption, downtime, heat use, and project costs
would permit mechanism-specific or quasi-experimental designs.

## Pivot Triggers

Reframe or narrow the paper if any of these occurs:

- identity guardrails fail under a clean rebuild
- the scale association loses sign or practical magnitude under a justified
  sparse-event specification
- engineering-valid exclusions materially reverse cohort patterns
- comparator review reveals an existing study with the same national pre-entry
  risk set and component decomposition
- the professor cannot state the integrated contribution after reading the
  abstract and framework figure
