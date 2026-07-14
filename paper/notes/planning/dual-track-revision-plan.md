# Dual-Track Scientific Revision Plan

**Status:** Implementation active; public-draft pass complete, P0 scientific validation pending

**Baseline:** `4ac9afe` on 14 July 2026

**Inputs:**

- [Simulated external peer review](../review/external-peer-review-2026-07-14.md)
- [Professor and reviewer rubric](../review/reviewer-rubric.md)
- [Defense red-team revision map](../review/defense-red-team-revision-map.md)
- [Current paper structure checklist](paper-structure-checklist.md)

## Objective

Revise the study toward a defensible *Waste Management* submission without
destroying the comprehensive professor-facing version needed to explain the
research foundation, comparator lineage, methods, decisions, and limitations.

The revision will maintain one empirical pipeline and two presentation
profiles:

1. **Professor-facing profile:** comprehensive explanation, method lineage,
   decision history, equations, diagnostics, and defense-oriented caveats.
2. **Journal-facing profile:** focused scientific contribution, concise
   literature gap, primary estimands, journal-compliant length, and only the
   strongest main-text analyses.

The two profiles may differ in explanation and placement. They may not differ
in data, model outputs, definitions, or empirical conclusions.

## Non-Negotiable Architecture

### One empirical truth

The following remain shared and canonical:

- `data/raw/` and the parser schema
- `code/analysis/` and the stage orchestrator
- `data/processed/` analytical files
- `output/` generated evidence and manifests
- `paper/evidence/current/` synchronized paper evidence
- figure and table generation code
- claim registry and numerical verification rules

No manuscript profile may contain a manually maintained alternative result.

### Two controlled prose profiles

The implemented ownership model is:

| Profile | Purpose | Current ownership |
|:--|:--|:--|
| Professor | Comprehensive review, supervision, oral defense, method explanation | `paper/manuscript/professor/` |
| Journal | Public, submission-oriented scientific article | `paper/manuscript/paper.md` and `paper/manuscript/paper.tex` |
| Shared supplement | Full audit trail and robustness evidence | `paper/supplement/` |
| Shared evidence | Generated results only | `output/`, `paper/evidence/current/` |

The root manuscript sources are the public journal profile. The professor
sources are preserved separately and build to a distinct reading PDF. Both are
checked against the same canonical outputs.

### Baseline preservation

Before scientific revisions begin:

1. Tag or otherwise freeze commit `4ac9afe` as the professor-review baseline.
2. Preserve its manuscript PDF, source, evidence manifest, and build metadata.
3. Record hashes so the baseline can be reproduced without relying on a mutable
   convenience PDF.
4. Do not overwrite the baseline when journal-profile exports are introduced.

## Revision Principles

1. Fix construct validity before improving prose.
2. Validate longitudinal identity before changing transition models.
3. Reduce model ambition rather than adding controls to sparse data.
4. Separate algebraic identities from empirical explanation.
5. Keep exploratory evidence out of the journal headline.
6. Preserve professor-facing explanation even when journal prose is compressed.
7. Add literature only when it defines a gap, method, interpretation, or
   limitation.
8. Rebuild every downstream artifact after an analytical change.
9. Use human verification where physical continuity or project history cannot
   be established from administrative fields alone.

## Workstreams

| ID | Workstream | Priority | Dependency | Current state |
|:--|:--|:--|:--|:--|
| W0 | Freeze baseline and implement dual-profile ownership | P0 | None | Complete |
| W1 | Independently validate administrative linkage | P0 | W0 | Pending |
| W2 | Decide and state the primary scientific contribution | P0 | W1 findings | Provisional public rewrite; final gate pending W1 |
| W3 | Simplify and stress-test sparse entry inference | P0 | W1 | Pending |
| W4 | Recast engineering models around raw quantities | P0 | W0 | Pending |
| W5 | Demote or strengthen pathway analysis | P1 | W1, W3 | Public-main-text demotion complete; scientific review pending |
| W6 | Rebuild novelty and comparator positioning | P1 | W2, W4 | Public gap rewrite complete; systematic search pending |
| W7 | Revise figures, tables, and reader explanation | P1 | W3-W6 | Public placement pass complete; Figure 3 uncertainty redesign pending |
| W8 | Produce professor and journal manuscripts in parallel | P1 | W2-W7 | Profiles and builds complete; final scientific reconciliation pending |
| W9 | Resolve public release and reproducibility governance | P1 | W0 | Availability aligned; licensing and fresh-clone work pending |
| W10 | Full validation, external-style rereview, and decision | P0 final gate | W1-W9 | Pending |

## W0 - Freeze Baseline And Establish Dual Profiles

### Purpose

Protect the current professor-facing manuscript while allowing journal-focused
restructuring without maintaining two analytical pipelines.

### Actions

1. Freeze the current source, PDF, supplement, figures, and evidence manifest.
2. Introduce explicit professor and journal build targets.
3. Make professor and journal PDFs visually distinguishable in filenames and
   title-page metadata.
4. Extend claim verification to scan both profiles for shared high-risk
   numbers, sample definitions, estimands, and prohibited causal wording.
5. Extend repository validation to require both profiles after migration.
6. Document which content may differ:
   - explanation depth
   - literature-table placement
   - robustness detail
   - figure placement
   - word count
7. Document which content must remain identical:
   - data period and sample counts
   - variable definitions and units
   - event definitions
   - model specifications and estimates
   - uncertainty results
   - limitations attached to empirical claims

### Acceptance gate

- The baseline PDF remains reproducible.
- Both profile builds can consume the same generated evidence.
- A deliberate numerical mismatch between profiles causes verification to fail.
- No analytical script branches on professor versus journal profile.

## W1 - Independent Administrative-Linkage Validation

### Scientific problem

Current tests establish deterministic and internally auditable linkage. They do
not estimate agreement with external facility history or detect confidently
wrong links outside the algorithm's uncertainty flags.

### Validation packet

Build a human-review packet with source fields but initially hide algorithmic
scores and final labels. Include:

1. Every one of the 55 descriptive entry transitions.
2. Every accepted uncertain link.
3. Every fuzzy-name accepted link, subject to deduplication with the sets above.
4. A stratified random sample of at least 150 additional links covering:
   - code plus exact-name links
   - code with non-exact supporting evidence
   - exact-name links without code
   - gap links
   - FY2009-FY2013 bridges
   - FY2019-FY2020 recode bridges
   - inferred asset-episode resets
5. A sample of rejected high-scoring candidate links to assess false
   separation, not only false joining.

For each pair, reviewers should classify:

- same administrative facility history
- different facility history
- indeterminate from available evidence
- same lineage but probable asset/configuration reset

### Human role

The author performs one review. A second human reviewer, preferably the
professor or a Japanese-reading research assistant, reviews the high-impact
entry set and a blinded validation subset. Disagreements are adjudicated and
retained in the audit log. Internet or municipal archive evidence may support a
decision but must be cited and archived.

### Analyses

1. Report agreement by linkage class and transition regime.
2. Report false-join, false-separation, and indeterminate counts.
3. Identify which modeled entry events rely on each linkage class.
4. Re-estimate key results after excluding:
   - all indeterminate reviewed links
   - all fuzzy links
   - all gap links
   - all event transitions not positively validated
5. Rebuild the identity layer if any confirmed error changes a lineage or event.

### Decision rules

- Any confirmed error affecting a modeled event triggers identity correction
  and a complete downstream rebuild.
- Material disagreement concentrated in a linkage class triggers resolver
  revision or exclusion of that class from the primary transition estimand.
- If physical history remains indeterminate, retain administrative-lineage
  language and do not upgrade pathway labels.

### Professor-facing treatment

Show the validation design, examples, disagreement resolution, and what the
algorithm can and cannot establish.

### Journal-facing treatment

Report the validation sample, agreement/error summary, event exposure, and
result sensitivity concisely. Put pair-level evidence in the supplement.

### Acceptance gate

- All 35 broad modeled events have an explicit human linkage-review status.
- Validation decisions and supporting evidence are reproducible.
- Identity-dependent results are regenerated after every accepted correction.

## W2 - Define One Primary Scientific Contribution

### Proposed narrative spine

> National waste-to-energy diagnosis changes when fleet denominators,
> administrative transitions, and engineering components are defined before
> interpreting facility counts or gross output ratios.

The Japan panel demonstrates that measurement architecture through three
ordered findings:

1. facility participation is not waste-volume coverage;
2. first reported entry is rare and concentrated among larger processing
   facilities in the observed risk population;
3. gross MWh/t combines installed sizing, capacity use, and waste loading and
   should not be interpreted as an independent efficiency measure.

### Actions

1. Rewrite the contribution statement before rewriting the abstract.
2. Keep three ordered RQs, but remove the pathway comparison from formal RQ3.
3. Make the pathway analysis explicitly exploratory and supplemental.
4. State the transferable contribution as measurement and state-definition
   discipline, not a universal Japan policy ranking.
5. Test the narrative with three readers:
   - professor/examiner
   - waste-management editor
   - technically literate non-specialist

### Pivot decision

If the professor or external-style reviewer cannot state the integrated
contribution after the abstract and introduction, narrow the journal profile to
coverage plus engineering components and retain entry as a separate future
paper or supplement. The professor profile may continue documenting all three
analyses.

### Acceptance gate

- One contribution sentence appears consistently in abstract, introduction,
  discussion, conclusion, cover letter, and highlights.
- Each RQ has one estimand, sample, method, result, and limitation.

## W3 - Simplify And Stress-Test Sparse Entry Inference

### Scientific problem

The broad model uses 35 events for approximately 11 coefficients. Firth bias
reduction addresses likelihood bias and separation, but not weak information,
collinearity, or influential events.

### Design stage before refitting

Write and freeze a short model-decision memo before comparing new estimates.
The memo must specify:

- primary estimand and selected risk population
- essential scale term
- age representation
- baseline hazard representation
- calendar-period adjustment
- maximum permitted degrees of freedom
- influence and sensitivity checks

Candidate specifications should reduce degrees of freedom. Selection must be
based on estimand clarity and design, not on which model produces the strongest
p-value.

### Required outputs

1. Event table for the exact 35-event sample by:
   - calendar era
   - age band
   - processing-capacity category
   - pathway label
   - linkage class
   - episode-boundary status
2. Lower-degree-of-freedom primary Firth model.
3. Current 11-coefficient model retained as a sensitivity if still defensible.
4. At least 1,999 whole-lineage bootstrap replications for final intervals.
5. Leave-one-event and leave-one-event-lineage influence results for the
   300-versus-100 t/day contrast.
6. Sensitivities excluding forward-dated/placeholder transitions and
   non-validated linkage transitions.
7. Stability across defensible calendar and duration representations.
8. Conventional logit and complementary-log-log retained only as link checks.

### Interpretation rules

- Do not headline a p-value near 0.05.
- Do not call non-significance evidence of no age relationship.
- Do not translate the capacity association into an enlargement effect.
- Always state that the risk population excludes 467 lineages already
  generating when first observed.

### Professor-facing treatment

Explain why each model term is present, show the model-decision memo, event
composition, influence findings, and comparison with the earlier model.

### Journal-facing treatment

Show the final primary specification and one compact sensitivity ladder.
Detailed coefficients, bootstrap diagnostics, and influence plots go to the
supplement.

### Acceptance gate

- The scale contrast retains a defensible direction and useful precision under
  the prespecified lower-degree-of-freedom and influence checks.
- If it does not, revise the headline to descriptive scale concentration.
- All requested bootstrap fits converge or failures are explicitly handled and
  explained.

## W4 - Recast Engineering Models Around Raw Quantities

### Scientific problem

Gross MWh/t, design intensity, capacity factor, and utilization are linked by
an exact accounting identity. Ratio regressions can create mechanical
association and should not be presented as if they independently identify
engineering mechanisms.

### Primary model redesign

1. Model installed electrical capacity directly:

   `log(K) = cohort + log(C) + configuration + fiscal-year effects + error`

   Translate the processing-capacity elasticity into the implied design-
   intensity relationship rather than making `log(K/C)` the only primary
   regression.
2. Retain the direct gross-output model:

   `log(G) = log(W) + log(K) + cohort + configuration + fiscal-year effects + error`

3. Treat electrical capacity factor and waste utilization primarily as
   descriptive operating components, with conditional models clearly labelled
   as mechanically related diagnostics.
4. Keep the exact engineering identity as a definition, not a causal model.
5. Reassess whether the legacy R-squared jump adds scientific information. If
   retained, quantify or explain its mechanical component; otherwise move it
   to the supplement.

### Additional diagnostics

- cohort-by-fiscal-year overlap table
- missingness and engineering-exclusion table by cohort and period
- cluster influence and residual diagnostics for primary raw-variable models
- lineage-equal weighting
- identity-certain lineages
- predefined engineering bounds
- asset-episode fixed effects or first differences only where within-episode
  variation supports the estimand

### Interpretation rules

- Use "expressed mainly through reported generator sizing," not a causal claim
  that sizing produces the cohort hierarchy.
- Do not describe reported start-year cohorts as verified generator vintages.
- Do not interpret survival of older cohorts as technological degradation.
- Distinguish gross generation from net export, useful heat, thermal input,
  lifecycle benefit, and economic performance.

### Professor-facing treatment

Show the algebra, raw-variable model, ratio translation, and why mechanical
coupling changes interpretation.

### Journal-facing treatment

Lead with the raw installed-kW and gross-MWh models. Use the identity to explain
constructs and move the legacy diagnostic details to the supplement.

### Acceptance gate

- The sizing conclusion is supported in raw-variable and ratio translations.
- The main text no longer uses R-squared changes as independent evidence of a
  mechanism.
- Cohort interpretation remains stable under overlap and weighting checks.

## W5 - Pathway Analysis Decision

### Default decision

Move Section 4.4 and Figure 4 out of the journal main text. Retain them in the
professor profile and supplement as hypothesis-generating evidence.

### If retained anywhere

1. Show individual event observations or interval estimates.
2. Report follow-up eligibility, positive-output conditioning, and engineering-
   validity exclusions by pathway.
3. Include the forward-dated/placeholder category in a table even if it is not
   plotted.
4. Do not label differences as effects.
5. Keep physical mechanism language out unless external project histories are
   added.

### Acceptance gate

- Journal abstract, RQs, conclusion, and highlights do not depend on the small
  pathway contrast.
- Professor profile clearly marks the comparison exploratory.

## W6 - Rebuild Literature Gap And Comparator Positioning

### Literature review questions

1. Which studies use repeated Japanese facility data?
2. Which studies model electricity, heat, generation intensity, or installed
   capacity?
3. Which studies distinguish facility count from waste-volume coverage?
4. Which studies reconstruct longitudinal facility identity across code breaks?
5. Which studies model first observed WtE entry with sparse-event methods?
6. Which studies decompose gross output into installed sizing and annual use?
7. What richer engineering questions do Cui, Liu, Han, Shino, Sasao, Chen, and
   Yeh answer that this dataset cannot?

### Outputs

- search log with databases, terms, dates, and inclusion rules
- comparator matrix with unit, country, period, sample, outcome, method,
  identity treatment, engineering fields, and contribution
- verified DOI and bibliographic metadata
- focused gap synthesis for the journal profile
- comprehensive inspiration-and-adaptation explanation for the professor
  profile
- method references for record linkage, assignment validation, clustered
  resampling, Firth influence, and ratio interpretation

### Writing distinction

**Professor profile:** retain a transparent explanation of what was learned
from each comparator and how the design was adapted.

**Journal profile:** remove language suggesting that high-profile papers were
templates. State the unresolved empirical gap and cite comparators where they
define that gap.

### Acceptance gate

- Novelty does not rest on national setting, later endpoint, repository rigor,
  or the phrase "to our knowledge" alone.
- The closest Japan studies receive direct substantive comparison.

## W7 - Figures, Tables, And Reader Explanation

### Journal main-text target

1. **Figure 1:** retain the denominator-specific coverage trend.
2. **Figure 2:** retain the final sparse-entry estimates with event counts,
   selected risk population, and final bootstrap intervals.
3. **Figure 3:** replace unadorned cohort medians with distributions or adjusted
   estimates and uncertainty.
4. **Figure 4:** move pathway comparison to the supplement by default.

### Professor profile

May retain all four figures plus a compact method-flow diagram if it materially
improves explanation. It should not use extra figures as decoration.

### Table plan

| Content | Professor profile | Journal profile |
|:--|:--|:--|
| Comparator adaptation | Main text or appendix | Short gap synthesis; detailed matrix supplemental |
| Analytical frames | Main text | Main text, compressed |
| Entry estimates | Main text plus diagnostics | Main estimates only; diagnostics supplemental |
| Component estimates | Main text with equation explanation | Raw-variable primary estimates |
| Linkage validation | Detailed | Compact summary; pair-level audit supplemental |
| Pathways | Main or appendix, exploratory | Supplement |

### Readability requirements

- Define every abbreviation at first use in each profile.
- Follow each essential equation with a plain-language interpretation.
- Put denominators, units, years, sample sizes, and uncertainty in captions.
- Avoid titles that state stronger conclusions than the plotted evidence.
- Inspect every rendered page at final size for crop, overlap, and spacing.

### Acceptance gate

- A reader can explain each figure without reading repository files.
- Figures remain legible in color, grayscale, print, and common PDF viewers.

## W8 - Parallel Manuscript Revision

### Professor-facing profile jobs

- preserve comprehensive provenance and identity explanation
- explain model decisions and alternative specifications
- retain comparator inspiration and adaptation history
- explain equations for readers without advanced statistical background
- include defense questions, interpretation traps, and future data needs
- permit additional words where they improve comprehension

### Journal-facing profile jobs

- lead with one contribution and one narrative spine
- compress generic background and repository operations
- use a direct gap synthesis rather than an adaptation table
- make raw-variable engineering models primary
- move pathway and extended diagnostics to the supplement
- obey current *Waste Management* length and display limits
- remove professor-directed language from conclusion and discussion

### Synchronization protocol

After every empirical change:

1. regenerate canonical outputs;
2. synchronize paper evidence;
3. update the professor profile first with full explanation;
4. update the journal profile from the same evidence;
5. run cross-profile claim verification;
6. rebuild both PDFs;
7. inspect both visually.

Pure journal compression does not require changing the professor profile unless
it corrects an error or clarifies an empirical conclusion.

### Acceptance gate

- Professor profile can stand alone for supervision.
- Journal profile can stand alone for peer review.
- Neither profile relies on the other for definitions or limitations.
- Shared empirical claims are identical.

## W9 - Repository And Publication Governance

### Actions

1. Decide whether the GitHub repository should be public or private during
   professor review.
2. Align `current-status.md`, README links, and manuscript availability text
   with the actual state.
3. Confirm Ministry and e-Stat source-workbook redistribution terms.
4. Separate licenses or notices for:
   - analysis code
   - manuscript text
   - derived tables and figures
   - third-party raw workbooks
5. Add `CITATION.cff` after final author, title, repository, and release details
   are stable.
6. Improve fresh-clone preflight behavior for `claims:verify`.
7. Add focused tests for identity reconstruction, sample construction,
   prerequisite handling, and boundary cases.
8. Add a transitive dependency lock for archival reproducibility.

### Acceptance gate

- Availability statements describe the real repository state.
- No raw source is redistributed without a documented basis.
- A fresh clone either reproduces the required files or fails with a precise,
  actionable preflight message.

## W10 - Final Validation And Decision

### Scientific gates

- independent identity validation completed
- entry-model decision memo frozen and implemented
- sparse-event influence checks passed or conclusion weakened
- engineering raw-variable results reconciled with ratio identities
- pathway evidence correctly placed
- literature gap externally defensible
- all caveats attached to the claims they limit

### Reproducibility gates

```bash
npm run analysis:test
npm run analysis:rebuild
npm run paper:sync
npm run paper:check
npm run claims:verify
npm run paper:export:nopdf
npm run paper:build:latex
npm run repo:check
git diff --check
```

The dual-profile implementation should add explicit professor and journal build
commands to this gate.

### Human gates

1. Professor reads the comprehensive profile and confirms the estimands,
   comparator lineage, and contribution.
2. A technically literate non-specialist explains Figure 1, the entry odds
   ratio, and the engineering identity without causal overstatement.
3. A waste-management reader challenges practical significance and confirms
   that the discussion answers it.
4. A fresh external-style review is run without using the internal rubric as
   the scoring key.

### Final decisions

| Outcome | Action |
|:--|:--|
| All P0 scientific gates pass | Prepare journal submission package |
| Linkage validation changes events materially | Rebuild and reconsider entry contribution |
| Scale result is influence-dependent | Downgrade entry to descriptive evidence |
| Raw-variable models weaken sizing interpretation | Rewrite RQ3 around the accounting identity only |
| Integrated contribution remains unclear | Narrow journal profile; preserve full professor profile |
| Professor requests new causal or engineering claims | Require new data/design rather than stronger prose |

## Criticism-To-Action Matrix

| External-review finding | Primary response | Professor profile | Journal profile |
|:--|:--|:--|:--|
| Linkage lacks external truth | W1 human validation and event audit | Full method and examples | Compact validation plus supplement |
| Paper is diffuse | W2 one contribution and ordered RQs | Preserve explanatory breadth | Remove pathway from formal contribution |
| 35-event model is overextended | W3 lower-DF primary model and influence checks | Explain model decision | Show only final primary and sensitivity |
| Ratio models are mechanically coupled | W4 raw-variable primary models | Teach identity and translation | Lead with raw K and G models |
| Entry mixes administrative pathways | W1/W3 event composition and exclusions | Detailed pathway logic | Selected-risk caveat beside result |
| Pathway figure is underpowered | W5 demotion or uncertainty | Retain as exploratory | Supplement by default |
| Novelty gap is weak | W6 focused comparator review | Inspiration map retained | Direct gap synthesis |
| Cohort comparisons face survivor effects | W4 overlap and composition checks | Explain fully | Add concise limitation and diagnostics |
| Figure 3 lacks uncertainty | W7 redesign | Detailed descriptive plus adjusted view | Adjusted or distributional figure |
| Repository statements conflict | W9 governance alignment | Actual review-access instructions | Submission-ready availability statement |

## Recommended Execution Order

1. W0 - freeze and dual-profile architecture
2. W1 - linkage validation packet and human review
3. W2 - contribution decision
4. W3 - entry-model redesign and stress tests
5. W4 - engineering-model recast
6. W5 - pathway placement decision
7. W6 - literature and novelty synthesis
8. W7 - figures and tables
9. W8 - parallel manuscript revision
10. W9 - governance and reproducibility cleanup
11. W10 - full rebuild, professor review, and external-style rereview

W3 and W4 can proceed in parallel after W1 establishes whether identity changes
are required. W6 can begin earlier as discovery, but final novelty prose must
wait for the primary analyses to stabilize.

## Immediate Next Action

Begin W1: generate the blinded administrative-linkage validation packet,
prioritizing all modeled entry events, uncertain links, major code-break
bridges, and a stratified comparison sample. Do not change the primary model
until human linkage review establishes whether any lineage or event must be
corrected.
