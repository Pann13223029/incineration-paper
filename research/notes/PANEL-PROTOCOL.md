# Optimized Multi-Agent Discussion Protocol v2.6

*Dual-mode protocol: `Fast / Decision` for clean, quick convergence and `High-Output / Discovery` for maximum idea yield. v2.6 adds a claim-normalization stage on top of v2.5 so converged Round 1 ideas are critiqued cleanly instead of wasting budget on duplicates.*

---

## 1. Protocol Contract

### Purpose

Use this protocol to extract better answers from multiple agents than a single-pass response would produce. Choose the mode based on the real objective:

- `Fast / Decision`: converge on the best defended answer quickly.
- `High-Output / Discovery`: maximize distinct useful hypotheses, risks, and next moves.

### Inputs

- `TOPIC`
- `QUESTION`
- `MODE`
- `N_AGENTS`
- `PERSONAS`
- `TIME_BUDGET`

### Standard Outputs

- `Executive synthesis`
- `Normalized claim ledger with scores`
- `Named dissents`
- `Recommended next action`
- `Closure block`

### Non-Negotiables

- No human steering between rounds.
- No human-written summaries between rounds.
- All claims use stable IDs.
- Every claim must state its evidence or basis.
- Persona divergence must be explicit, not implied.
- Final synthesis may compress, but the claim ledger must preserve what survived, what failed, and why.

### Persona Divergence Contract

For each persona, define:

- one assumption it tends to trust
- one assumption it tends to distrust
- one kind of evidence or argument it discounts

This makes "divergent priors" observable instead of aspirational.

### Orchestrator Responsibilities

The orchestrator must:

- run preflight before choosing mode
- decide whether evidence intake is required before Round 1
- define coverage axes before Round 1
- normalize overlapping Round 1 claims before assigning critique
- assign critique so agents do not review their own claims
- update the claim ledger after every round
- apply scoring, truncation, and ranking rules consistently
- reopen a single disputed claim when that is cheaper than rerunning the whole protocol

---

## 2. Preflight, Question Type, And Mode Selection

### Preflight Gate

Before selecting mode, answer:

- Is the question answerable as written?
- Is this primarily a reasoning problem, an evidence-retrieval problem, or both?
- What specific outcome would make the run valid?
- What condition would make the run invalid even if the panel converges?

If the question is not answerable as written, rewrite it before running the panel.

If the question is evidence-dependent and the evidence is missing, do not use the panel to simulate knowledge you do not have. Run evidence intake first.

### Question Taxonomy

Use the taxonomy below to choose a default path:

- `Decision`: choose among known options. Default to `Fast / Decision`.
- `Brainstorming`: generate options or directions. Default to `High-Output / Discovery`.
- `Diagnosis`: find root causes or bottlenecks. Default to `High-Output / Discovery`.
- `Prioritization`: rank fixes or actions. Use `Fast / Decision` if the option set is known; otherwise start in `High-Output / Discovery`.
- `Red-team`: attack a plan, claim, or protocol. Default to `High-Output / Discovery` with a strong failure-oriented critic.
- `Synthesis`: compress a fixed source set into a recommendation. Default to `Fast / Decision` unless major blind spots remain.

### Mode Selection

Use `Fast / Decision` when:

- the question is evaluative and bounded
- the decision is reversible or low-cost
- time budget is under 6 minutes for parallel execution
- clean answer quality matters more than exploration breadth

Use `High-Output / Discovery` when:

- the goal is brainstorming, option generation, or hidden-risk discovery
- the topic has multiple plausible directions or blind spots
- the output will feed future work, repeated runs, or strategy formation
- losing minority ideas would be costly

Escalate either mode with a formal defense step when:

- the decision is costly to reverse
- a disputed claim materially changes the recommendation
- the output must be audit-friendly

### Mid-Run Mode Switch And Abort Rules

Escalate from `Fast / Decision` to `High-Output / Discovery` when:

- the option set is incomplete
- multiple `OPEN` claims sit on critical axes
- the critic uncovers a blind spot large enough to change the answer
- synthesis would otherwise hide unresolved disagreement

Downgrade from `High-Output / Discovery` to `Fast / Decision` when:

- the top options are already clear
- novelty has saturated
- additional rounds are adding volume, not distinct signal
- the decision now depends more on choosing than on exploring

Abort the run instead of continuing when:

- the question remains ill-posed after preflight
- required evidence is missing and no evidence intake was done
- the ledger is not being maintained
- the operator cannot explain why the current mode still matches the task

---

## 3. Shared Setup Rules

### Agent Count

- `Fast / Decision`: 3-5 agents
- `High-Output / Discovery`: 5-7 agents when the topic actually has multiple separable angles; otherwise stay at 4-5

### Coverage Design

Personas alone are not enough. Before Round 1, define 4-6 coverage axes. Typical axes:

- feasibility
- failure modes
- contrarian thesis
- implementation path
- second-order effects
- edge cases or neglected populations

In `High-Output / Discovery`, each agent must own at least one axis.

### Evidence Intake

Evidence intake is mandatory when:

- the question is factual, time-sensitive, or high-stakes
- the answer depends on specific external evidence rather than reasoning over fixed local context
- the operator would reject unsupported claims even if they are internally coherent

Create a compact evidence pack before Round 1:

- `Source or artifact`
- `Date or version`
- `What it supports`
- `What remains uncertain`

If no evidence pack exists, claims must be treated as inference, not fact. In mixed runs, evidenced claims outrank equally actionable unevidenced claims.

### Fresh-Agent Policy

Prefer fresh agents for recombination or final synthesis when:

- early rounds showed strong anchoring
- the critic was weak
- the operator suspects polite convergence
- the run is high-stakes and a second-pass view is cheap enough

Prefer reusing agents when:

- domain context is expensive to reload
- the question is narrow and bounded
- continuity matters more than reframing

If a fresh synthesis agent is not used on a high-stakes run, record why.

### Claim Record Format

Use durable claim IDs such as `A1-C1`, `A1-C2`, `A2-C1`.

Every claim should carry:

- `Claim`
- `Why it matters`
- `Evidence / basis`
- `Assumption / constraint`
- `Confidence`

### Claim Normalization

After Round 1 and before critique, merge duplicate or near-duplicate claims into normalized claims whenever two or more claims:

- imply the same next action
- rely on the same underlying mechanism or evidence basis
- differ mainly in wording, emphasis, or confidence

Do not merge claims just because they live in the same theme. Keep them separate if they differ materially in:

- next action
- evidence basis
- stakeholder impact
- risk profile

Each normalized claim must record:

- normalized ID such as `N1`, `N2`
- alias source claim IDs
- originating agents
- merged claim text
- distinct caveats or variants worth preserving

Critique assignment happens against normalized IDs, not raw Round 1 IDs.

If a narrow question causes heavy early convergence, normalize aggressively. If more than half of Round 1 claims collapse into 1-3 normalized claims, critique the normalized set directly rather than pretending the duplicates are independent signal.

### Lightweight Claim Ledger

Track at minimum:

- `Claim ID`
- `Coverage axis`
- `Originating agent`
- `Evidence / basis`
- `Current status`: `SURVIVES / REJECTED / MODIFIED / OPEN`
- `Evidence score`
- `Support score`
- `Novelty score`
- `Actionability score`
- `Objection severity`
- `Strongest counterpoint`
- `Next action or test`

Do not default to a heavy JSON evidence ledger. The goal is persistence without procedural drag.

The orchestrator updates the ledger after every round. Keep one row per claim ID. If two claims are substantively duplicates, merge them under the oldest surviving claim ID and record the others as aliases.

### Scoring Rules

Use a simple `0-2` scale:

- `Evidence score`
  - `0`: assertion only
  - `1`: mechanism, example, or plausible inference
  - `2`: concrete source, observed case, or specific causal basis
- `Support score`
  - `0`: mostly rejected
  - `1`: mixed, modified, or weakly carried forward
  - `2`: clearly endorsed by multiple non-originating agents
- `Novelty score`
  - `0`: redundant
  - `1`: useful reframing
  - `2`: genuinely new angle or non-obvious move
- `Actionability score`
  - `0`: abstract
  - `1`: clear decision implication
  - `2`: concrete next step, test, or experiment
- `Objection severity`
  - `0`: no material objection
  - `1`: bounded objection
  - `2`: objection could overturn the claim

Use these working definitions:

- `Core claim`: `Support >= 2`, `Evidence >= 1`, `Objection severity <= 1`
- `Surviving claim`: not rejected, and either `Support >= 1` or `Novelty = 2`, with `Objection severity <= 1`
- `Major blind spot`: coverage axis with no surviving claim, or any `OPEN` claim with `Actionability >= 2` and `Objection severity = 2`

### Context Budget Rule

Normalize claims before applying truncation.

If the normalized Round 1 set produces 15 claims or fewer, pass full outputs forward.

If the normalized Round 1 set produces more than 15 claims:

- pass all claim IDs and one-line claim summaries
- pass full text only for the highest provisional-priority claims across the whole panel, not per-agent quotas
- compute provisional priority as `Evidence + Novelty + Actionability`
- retain at least one full-text claim per coverage axis
- cap full-text carry-forward at 10 claims unless context budget clearly allows more
- keep lower-value rejected claims ledger-only

This avoids context collapse in repeated use.

---

## 4. Fast / Decision Mode

### Overview

Three rounds. One human review at the end. Target wall-clock time: 5-6 minutes for parallel-capable orchestrators, 8-10 minutes for sequential execution.

### Round 1: Independent Brainstorm

- Agents do not see each other's outputs.
- Each agent outputs 2-4 claims.
- Maximum 300 words total.
- Format each claim as:
  - `Claim ID`
  - `Claim`
  - `Why`
  - `Evidence / basis`
  - `Assumption / constraint`
  - `Confidence: low / medium / high`

### Round 2: Critique-with-Stakes

- Same agents, same personas.
- One agent is the `Adversarial Critic`.
- Each claim must be reviewed by at least 2 non-originating agents.
- Agents do not critique claims they originated.
- Every response must reference claim IDs directly.
- Allowed tags: `ENDORSE / REJECT / MODIFY / NEW`.
- For every addressed claim, include:
  - `Claim ID`
  - `Tag`
  - `Rationale`
  - `Counterevidence / basis`
  - `Exact requested change` when using `MODIFY`
- Maximum 450 words total.

After Round 2, the orchestrator updates the ledger scores and statuses.

### Early Exit Gate

Early exit is allowed only if all conditions hold:

- one or more claims meet the `Core claim` definition
- all non-originating reviewers of those claims tagged them `ENDORSE` or `MODIFY`, with no `REJECT`
- persona divergence was explicitly defined up front
- at least one agent articulated a concrete failure mode for the consensus claim
- that failure mode was addressed, not ignored
- no `OPEN` claim remains on a critical axis
- no unresolved assumption would change the recommended answer

If any condition fails, continue to synthesis without early-exit language.

### Round 3: Synthesis

One synthesis agent produces:

1. `Consensus position`
2. `Material dissents by persona`
3. `Unresolved assumptions`
4. `Recommended final answer`
5. `Confidence: HIGH / MEDIUM / LOW`
6. `Closure block`: owner, next action, reopen trigger, and what evidence would change the answer

Maximum 500 words. No new positions may be introduced.

### Human Review Checklist

Check:

- Did the synthesis preserve the strongest claim and strongest objection?
- Does the recommendation actually answer the question asked?
- Did any unresolved assumption get hidden by compression?
- Was `Fast / Decision` the right mode?

If no, rerun with better personas or switch to `High-Output / Discovery`.

If one disputed claim is the blocker, reopen only that claim instead of rerunning the whole protocol.

---

## 5. High-Output / Discovery Mode

### Overview

Use this mode when the objective is maximum output, not fast consensus. The process is coverage-first and anti-compression by design.

### Round 1: Orthogonal Exploration

- Agents do not see each other's outputs.
- Each agent owns a distinct coverage axis.
- Each agent outputs 3-5 claims.
- Maximum 450 words total.
- Each claim must include `Evidence / basis`.
- Each agent must include:
  - one surprising but defensible claim
  - one claim explaining why the likely consensus may be wrong
  - one concrete test, experiment, or next move

### Round 2: Critique + Gap Mining

- Same agents, same personas.
- One agent remains the `Adversarial Critic`.
- Each claim is assigned to exactly 2 non-originating reviewers.
- Each agent critiques only an assigned subset of 4-6 claims, not the entire pool.
- Each agent must evaluate claims by ID using `ENDORSE / REJECT / MODIFY / NEW`.
- Each agent must also add:
  - `2-3 missing ideas or blind spots`
  - `1 weak-but-interesting claim worth rescuing`
- For every addressed claim, include:
  - `Claim ID`
  - `Tag`
  - `Rationale`
  - `Counterevidence / basis`
  - `Exact requested change` when using `MODIFY`
- Maximum 550 words total.

Round 2 is not only a pruning step. It is a second discovery pass.

After Round 2, the orchestrator updates the ledger scores and statuses.

### Novelty / Coverage Gate

Do not use early consensus as the stop rule in discovery mode.

Proceed only when:

- every planned coverage axis has at least one `Surviving claim` or an explicitly logged blind spot
- at least 20% of surviving claims have `Novelty = 2`
- at least one non-consensus idea remains live
- no `Major blind spot` remains unresolved

If not, run a targeted gap-fill pass with 1-2 agents focused only on uncovered space.

### Optional Round 2.5: Formal Defense

Add this step when one disputed claim materially changes the output portfolio.

Use 3 roles:

- `Originator`: gives the best version of the claim
- `Critic`: gives the best objection
- `Adjudicator`: states what evidence would resolve it and whether the claim remains `OPEN` or becomes `MODIFIED`

Update the ledger after this step.

### Round 3: Recombination

Use 2 agents:

- `Integrator`: combine surviving claims into 2-3 coherent composite strategies
- `Risk mapper`: build a failure matrix for the strongest surviving claims

Prefer agents that did not originate the top-ranked claims. Recombination should run on the deduplicated ledger, not on raw unfiltered transcripts.

This round exists because high-yield panels usually produce better ideas through recombination, not just elimination.

### Round 4: Portfolio Synthesis

One synthesis agent produces:

1. `Top 3 surviving ideas or strategies, ranked`
2. `Why each survives`
3. `Strongest dissent or unresolved objection`
4. `Most important blind spot still open`
5. `Best next experiments or decision rules`
6. `Confidence by idea: HIGH / MEDIUM / LOW`
7. `Closure block`: owner, next action, reopen trigger, and what evidence would change the ranking

Rank ideas using `Portfolio score = Evidence + Support + Novelty + Actionability - Objection severity`.

Break ties by:

1. wider coverage-axis reach
2. lower objection severity
3. more concrete next test

The goal is not one authoritative answer. The goal is a ranked portfolio with usable follow-through.

### Human Review Checklist

Check:

- Did every major axis produce at least one usable idea?
- Did the synthesis preserve dissent instead of laundering it?
- Did any rescued weak idea become strategically interesting?
- Are the next experiments concrete enough to run?
- Should one claim be reopened rather than rerunning the whole protocol?

---

## 6. Why This Version Wins

v2.0 was optimized for speed and reasonable convergence. v2.1 separates that goal from idea maximization instead of forcing one protocol to do both badly.

The main upgrades are:

- explicit mode choice
- explicit persona divergence
- coverage axes instead of vague "different personas"
- claim IDs and a lightweight ledger
- evidence fields and explicit scoring
- claim normalization before critique when convergence happens early
- cross-assigned critique instead of self-anchored critique
- a discovery path that mines gaps and recombines surviving ideas
- stricter conditions on early exit
- default persona packs and a miniature worked example for operators
- a run sheet and failure-recovery playbook for repeated use
- preflight, evidence intake, mode-switch rules, closure, and fresh-agent policy

This keeps the fast path lean while giving brainstorming runs a protocol that does not compress too early.

---

## 7. What Was Rejected

- `Always-on 5-round debate` — too slow for default use
- `Human steering between rounds` — inconsistent context and throughput loss
- `Heavy JSON evidence ledger by default` — too much operational overhead
- `Free-text essays in Round 1` — weak handoff fidelity
- `Consensus as the main success metric for brainstorming` — wrong target
- `Persona diversity without explicit divergence rules` — performs variety without creating it

---

## 8. Paste-Ready Protocol Templates

### Template A: Fast / Decision

```text
=== MULTI-AGENT DISCUSSION PROTOCOL v2.6 / FAST-DECISION ===

TOPIC: {{TOPIC}}
QUESTION: {{QUESTION}}
QUESTION TYPE: {{QUESTION_TYPE}}
MODE: FAST_DECISION
NUMBER OF AGENTS: {{N_AGENTS}}  (recommend 3-5)
TIME BUDGET: {{TIME_BUDGET}}

--- PREFLIGHT ---

ANSWERABLE AS WRITTEN:
REASONING / EVIDENCE / BOTH:
VALID RUN IF:
INVALID EVEN IF CONVERGED IF:

--- EVIDENCE INTAKE ---

EVIDENCE PACK PROVIDED: YES / NO
KEY SOURCES OR ARTIFACTS:
KNOWN GAPS:

PERSONA DIVERGENCE CONTRACT:
- Persona: {{PERSONA_NAME}}
- Trusts: {{TRUSTED_ASSUMPTION}}
- Distrusts: {{DISTRUSTED_ASSUMPTION}}
- Discounts: {{DISCOUNTED_EVIDENCE}}

--- ROUND 1: INDEPENDENT BRAINSTORM ---

"""
You are {{PERSONA_NAME}}, a {{PERSONA_DESCRIPTION}}.

Question: {{QUESTION}}

Rules:
- Output exactly 2-4 claims.
- Use stable IDs: {{AGENT_ID}}-C1, {{AGENT_ID}}-C2, etc.
- For each claim provide:
  Claim ID:
  Claim:
  Why:
  Evidence/Basis:
  Assumption/constraint:
  Confidence: low / medium / high
- Maximum 300 words total.
- Reason independently. You have not seen other agents.
"""

--- CLAIM NORMALIZATION + LEDGER UPDATE AFTER ROUND 1 ---

Orchestrator action:
- Create one ledger row per raw claim.
- Merge duplicate or near-duplicate claims into normalized IDs (`N1`, `N2`, ...).
- Preserve alias source IDs and originating agents for every normalized claim.
- Score provisional `Evidence`, `Novelty`, and `Actionability`.
- Assign critique against normalized IDs, not raw claim IDs.
- If normalized claim count exceeds 15, carry forward all IDs plus summaries and the highest provisional-priority full texts across the whole panel.

--- ROUND 2: CRITIQUE-WITH-STAKES ---

"""
You are {{PERSONA_NAME}}, a {{PERSONA_DESCRIPTION}}.
{{OPTIONAL_ADVERSARIAL_LINE}}

Assigned normalized claim IDs:
{{ASSIGNED_CLAIM_IDS}}

Normalized claim ledger:
{{NORMALIZED_CLAIM_LEDGER}}

Round 1 raw outputs:
{{ALL_ROUND_1_OUTPUTS}}

Rules:
- Respond by claim ID.
- Do not critique claims you originated.
- Allowed tags: ENDORSE / REJECT / MODIFY / NEW.
- For each addressed claim provide:
  Claim ID:
  Tag:
  Rationale:
  Counterevidence/Basis:
  Exact requested change if MODIFY:
- Maximum 450 words total.
- If you are the Adversarial Critic, challenge at least one consensus claim substantively.
"""

--- LEDGER UPDATE AFTER ROUND 2 ---

Orchestrator action:
- Update `Support`, `Objection severity`, and final status for each claim.
- Mark a claim as `Core` only if `Support >= 2`, `Evidence >= 1`, and `Objection severity <= 1`.

--- ROUND 3: SYNTHESIS ---

"""
You are a Synthesis Agent.

Original question: {{QUESTION}}
Ledger:
{{CLAIM_LEDGER}}
Round 1 outputs:
{{ALL_ROUND_1_OUTPUTS}}
Round 2 outputs:
{{ALL_ROUND_2_OUTPUTS}}

Output exactly:
1. Consensus position
2. Material dissents by persona
3. Unresolved assumptions
4. Recommended final answer
5. Confidence: HIGH / MEDIUM / LOW
6. Closure block:
   - Owner:
   - Next action:
   - Reopen trigger:
   - Evidence that would change the answer:

Do not introduce new positions.
Maximum 500 words.
"""

=== END PROTOCOL ===
```

### Template B: High-Output / Discovery

```text
=== MULTI-AGENT DISCUSSION PROTOCOL v2.6 / HIGH-OUTPUT-DISCOVERY ===

TOPIC: {{TOPIC}}
QUESTION: {{QUESTION}}
QUESTION TYPE: {{QUESTION_TYPE}}
MODE: HIGH_OUTPUT_DISCOVERY
NUMBER OF AGENTS: {{N_AGENTS}}  (recommend 5-7 when coverage warrants it)
TIME BUDGET: {{TIME_BUDGET}}
COVERAGE AXES: {{AXIS_1}}, {{AXIS_2}}, {{AXIS_3}}, {{AXIS_4}}

--- PREFLIGHT ---

ANSWERABLE AS WRITTEN:
REASONING / EVIDENCE / BOTH:
VALID RUN IF:
INVALID EVEN IF CONVERGED IF:

--- EVIDENCE INTAKE ---

EVIDENCE PACK PROVIDED: YES / NO
KEY SOURCES OR ARTIFACTS:
KNOWN GAPS:

PERSONA DIVERGENCE CONTRACT:
- Persona: {{PERSONA_NAME}}
- Owns axis: {{COVERAGE_AXIS}}
- Trusts: {{TRUSTED_ASSUMPTION}}
- Distrusts: {{DISTRUSTED_ASSUMPTION}}
- Discounts: {{DISCOUNTED_EVIDENCE}}

--- ROUND 1: ORTHOGONAL EXPLORATION ---

"""
You are {{PERSONA_NAME}}, a {{PERSONA_DESCRIPTION}}.
You own this coverage axis: {{COVERAGE_AXIS}}.

Question: {{QUESTION}}

Rules:
- Output exactly 3-5 claims.
- Use stable IDs: {{AGENT_ID}}-C1, {{AGENT_ID}}-C2, etc.
- For each claim provide:
  Claim ID:
  Claim:
  Why it matters:
  Evidence/Basis:
  Assumption/constraint:
  Confidence: low / medium / high
- Include at least:
  one surprising but defensible claim
  one claim explaining why likely consensus may be wrong
  one concrete test or next move
- Maximum 450 words total.
- Do not repeat generic points. Explore your assigned axis.
"""

--- CLAIM NORMALIZATION + LEDGER UPDATE AFTER ROUND 1 ---

Orchestrator action:
- Create one ledger row per raw claim with axis, basis, and provisional scores.
- Merge duplicate or near-duplicate claims into normalized IDs (`N1`, `N2`, ...).
- Preserve alias source IDs and originating agents for every normalized claim.
- Assign critique against normalized IDs, not raw claim IDs.
- If normalized claim count exceeds 15, carry forward all IDs plus summaries and only the highest provisional-priority full texts, with at least one per axis.

--- ROUND 2: CRITIQUE + GAP MINING ---

"""
You are {{PERSONA_NAME}}, a {{PERSONA_DESCRIPTION}}.
{{OPTIONAL_ADVERSARIAL_LINE}}

Assigned normalized claim IDs:
{{ASSIGNED_CLAIM_IDS}}

Normalized claim ledger:
{{NORMALIZED_CLAIM_LEDGER}}

Round 1 raw outputs:
{{ALL_ROUND_1_OUTPUTS}}

Rules:
- Critique only the assigned claims. Do not critique claims you originated.
- Evaluate claims by ID using ENDORSE / REJECT / MODIFY / NEW.
- For each addressed claim provide:
  Claim ID:
  Tag:
  Rationale:
  Counterevidence/Basis:
  Exact requested change if MODIFY:
- Also provide:
  2-3 missing ideas or blind spots
  1 weak-but-interesting claim worth rescuing
- Maximum 550 words total.
"""

--- LEDGER UPDATE AFTER ROUND 2 ---

Orchestrator action:
- Update `Support`, `Objection severity`, and final status for each claim.
- Identify `Surviving claims`, `OPEN claims`, and `Major blind spots`.

--- OPTIONAL ROUND 2.5: FORMAL DEFENSE ---

Use only for a disputed high-value claim.

Roles:
- Originator
- Critic
- Adjudicator

Output:
- Best version of the claim
- Best objection
- What evidence would resolve it
- Ledger status: OPEN or MODIFIED

--- ROUND 3: RECOMBINATION ---

Give one fresh or non-originating agent the Integrator role and one the Risk Mapper role.

Inputs:
- Deduplicated ledger
- Surviving claims
- OPEN claims that still matter materially

--- ROUND 4: PORTFOLIO SYNTHESIS ---

"""
You are a Synthesis Agent.

Original question: {{QUESTION}}
Ledger:
{{CLAIM_LEDGER}}
Round outputs:
{{ALL_ROUND_OUTPUTS}}

Output exactly:
1. Top 3 surviving ideas or strategies, ranked
2. Why each survives
3. Strongest dissent or unresolved objection
4. Most important blind spot still open
5. Best next experiments or decision rules
6. Confidence by idea: HIGH / MEDIUM / LOW
7. Closure block:
   - Owner:
   - Next action:
   - Reopen trigger:
   - Evidence that would change the ranking:

Rank ideas with:
Portfolio score = Evidence + Support + Novelty + Actionability - Objection severity

Do not collapse everything into one answer unless the panel truly converged.
"""

=== END PROTOCOL ===
```

---

## 9. Default Persona Preset Packs

### Pack A: Fast / Decision

Use this as the default 4-agent pack when the question is bounded and you want a clean recommendation quickly.

- `Implementation Realist`
  Trusts: operational constraints, sequencing, ownership.
  Distrusts: strategy that has no clear execution path.
  Discounts: elegant framing with no delivery mechanism.
- `Adversarial Auditor`
  Trusts: failure evidence, counterexamples, stress cases.
  Distrusts: early consensus and hand-wavy optimism.
  Discounts: intention, branding, and untested assurances.
- `Systems Synthesizer`
  Trusts: interaction effects, dependencies, second-order tradeoffs.
  Distrusts: single-cause explanations.
  Discounts: isolated anecdotes that do not generalize.
- `Stakeholder Proxy`
  Trusts: incentive alignment, user friction, political or organizational reality.
  Distrusts: solutions that look good only from the operator's perspective.
  Discounts: expert-only framing that ignores adoption costs.

Optional fifth persona:

- `Domain Specialist`
  Trusts: domain mechanisms and field-specific constraints.
  Distrusts: generic best practices imported without adaptation.
  Discounts: abstract analogy.

Default assignment rule:

- Make `Adversarial Auditor` the Round 2 critic unless another persona has the stronger natural objection.

### Pack B: High-Output / Discovery

Use this as the default 5-agent pack when the goal is exploration breadth.

- `Mechanist / Feasibility Lead`
  Coverage axis: feasibility.
  Trusts: constraints, mechanism, operational reality.
  Distrusts: magic levers and frictionless transitions.
  Discounts: motivational rhetoric.
- `Failure Hunter`
  Coverage axis: failure modes.
  Trusts: breakpoints, reversals, and edge-collapse scenarios.
  Distrusts: happy-path plans.
  Discounts: average-case reasoning.
- `Contrarian Strategist`
  Coverage axis: contrarian thesis.
  Trusts: asymmetry, neglected alternatives, unpopular but coherent moves.
  Distrusts: surface consensus.
  Discounts: conformity pressure.
- `Operator / Implementer`
  Coverage axis: implementation path.
  Trusts: sequence, resourcing, ownership, and rollout details.
  Distrusts: end-state talk without transition logic.
  Discounts: abstract ideals.
- `Externalities Scout`
  Coverage axis: second-order effects.
  Trusts: spillovers, displacement effects, and unintended consequences.
  Distrusts: local optima presented as global wins.
  Discounts: short time horizons.

Optional sixth persona:

- `Edge-Case Advocate`
  Coverage axis: neglected populations or edge conditions.
  Trusts: tail risks and atypical users or cases.
  Distrusts: representative-user assumptions.
  Discounts: average metrics that hide distributional harm.

Default assignment rule:

- Make `Failure Hunter` the Round 2 critic by default.
- If the real blind spot is conformity rather than failure, swap the critic role to `Contrarian Strategist`.

---

## 10. Worked Example

### Example Question

`What should be fixed first to make a thesis codebase reproducible before submission?`

Question type: `Prioritization`

Recommended mode: `High-Output / Discovery`

Why:

- the question is not just evaluative; it has multiple plausible bottlenecks
- losing minority ideas is costly
- the output should feed real implementation work

### Example Coverage Axes

- environment/bootstrap
- sample-construction consistency
- artifact provenance
- manuscript/output drift
- verification and smoke testing

### Example Persona Assignment

- `Mechanist / Feasibility Lead` -> environment/bootstrap
- `Failure Hunter` -> verification and failure modes
- `Contrarian Strategist` -> manuscript/output drift
- `Operator / Implementer` -> artifact provenance
- `Externalities Scout` -> sample-construction consistency

### Example Round 1 Claims

- `A1-C1`
  Claim: Freeze Python version and legacy parser dependencies before any further analysis work.
  Why it matters: a pipeline that cannot bootstrap cleanly is not reproducible no matter how good the downstream code is.
  Evidence / basis: raw historical `.xls` inputs often require explicit parser support and fail in fresh environments.
  Assumption / constraint: raw-data rebuild remains part of the canonical workflow.
- `A5-C1`
  Claim: Move all sample restrictions and derived-variable rules into one shared module before touching regression outputs.
  Why it matters: contradictory tables and models usually come from duplicated filtering logic, not from estimation itself.
  Evidence / basis: when multiple scripts rebuild analysis frames independently, silent sample drift is common.
  Assumption / constraint: the codebase currently recomputes analysis filters in more than one place.
- `A4-C1`
  Claim: Add a one-command rebuild plus per-artifact manifest before investing in full CI.
  Why it matters: provenance usually creates more immediate reliability than a complex automation layer built on drifting manual steps.
  Evidence / basis: manual multi-script workflows tend to produce stale markdown outputs and undocumented intermediate states.
  Assumption / constraint: the immediate need is reproducibility by one operator, not multi-platform industrial CI.

### Example Round 2 Critique Excerpts

- Review of `A1-C1`: `ENDORSE`
  Rationale: bootstrap failures block every other fix and have strong downstream leverage.
  Counterevidence / basis: none material.
- Review of `A5-C1`: `MODIFY`
  Rationale: centralizing sample logic should happen together with an explicit sample-definition report, otherwise the new shared module still hides attrition.
  Counterevidence / basis: centralized code alone does not guarantee interpretability.
  Exact requested change: require generated sample documentation as part of the same fix.
- Blind spot added in Round 2:
  Even after code is corrected, thesis text and tables may retain stale counts unless manuscript-facing artifacts are regenerated in the same workflow.
- Weak-but-interesting claim rescued:
  Add CI, but only as a smoke test that runs the canonical rebuild entry point and validates artifact presence, not as a heavy full-data job.

### Example Ledger Snapshot

| Claim ID | Axis | Status | Evidence | Support | Novelty | Actionability | Objection | Next action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `A1-C1` | environment/bootstrap | `SURVIVES` | 2 | 2 | 1 | 2 | 0 | Pin runtime and parser deps in one install path |
| `A5-C1` | sample consistency | `MODIFIED` | 2 | 2 | 2 | 2 | 0 | Build shared sample module plus generated sample-definition artifact |
| `A4-C1` | provenance | `SURVIVES` | 2 | 1 | 1 | 2 | 1 | Add one-command rebuild and per-artifact manifest |
| `A2-C1` | verification | `OPEN` | 1 | 1 | 1 | 2 | 2 | Revisit after canonical rebuild path exists |

### Example Portfolio Synthesis

1. Canonicalize sample construction and emit a generated sample-definition artifact.
   Why it survives: strongest mix of evidence, support, novelty, and actionability; it removes the highest source of silent contradiction.
2. Freeze the environment and parser/tooling dependencies.
   Why it survives: bootstrap reliability is prerequisite infrastructure for every later step.
3. Add a one-command rebuild with artifact manifests.
   Why it survives: provenance converts a one-off fix into a repeatable pipeline.

Strongest dissent:

- Full CI may be premature until the canonical rebuild path is cheap enough to run predictably.

Best next experiment:

- Implement steps 1 and 2 in the same change set, rerun the pipeline, then reopen only the `verification` claim to decide whether smoke-test CI is now justified.

Example closure block:

- Owner: thesis repo maintainer
- Next action: implement the top 2 ranked fixes in one change set
- Reopen trigger: regression sample counts still disagree across outputs after rebuild
- Evidence that would change the ranking: proof that the pipeline is already bootstrappable and sample logic is already centralized

What this example shows:

- the ledger preserves a useful `OPEN` claim instead of forcing premature consensus
- ranking is driven by evidence, support, and actionability, not by verbosity
- discovery mode is most useful when it ends in an implementation sequence, not just a list of ideas

---

## 11. Minimal Run Sheet

Use this as the smallest repeatable operator form before starting any panel run.

```text
RUN ID:
DATE:
TOPIC:
QUESTION:
QUESTION TYPE:
MODE: FAST_DECISION / HIGH_OUTPUT_DISCOVERY
TIME BUDGET:

PREFLIGHT:
- Answerable as written:
- Reasoning / Evidence / Both:
- Valid run if:
- Invalid even if converged if:

EVIDENCE INTAKE:
- Required: Yes / No
- Evidence pack:
- Known gaps:

SUCCESS CONDITION:
- What specific output should exist at the end of the run?

FAILURE CONDITION:
- What result would mean the run was low-signal or misleading?

COVERAGE AXES:
1.
2.
3.
4.

PERSONA PACK:
- Fast pack / Discovery pack / Custom

NORMALIZATION RULE:
- Merge if same next action + same mechanism/evidence.
- Keep separate if materially different action, evidence, stakeholder impact, or risk.

CRITIC ROLE:
- Which persona is the adversarial critic and why?

RECOMBINATION RULE:
- Needed / Not needed

FRESH-AGENT RULE:
- Fresh synthesis / Reused synthesis / Why

LEDGER OWNER:
- Who updates the ledger after each round?

TRUNCATION RULE:
- Full carry-forward threshold:
- Max full-text claims after truncation:

REOPEN RULE:
- Which single disputed claim would be reopened instead of rerunning the whole protocol?

CLOSURE OWNER:
- Who owns the next action after the panel ends?
```

### Minimal Ledger Template

Use this minimal table unless the run genuinely requires more detail.

| Claim ID | Axis | Origin | Status | Evidence | Support | Novelty | Actionability | Objection | Counterpoint | Next action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `A1-C1` |  |  | `OPEN` |  |  |  |  |  |  |  |

Operator rule:

- If the ledger is not updated after each round, the protocol is not actually being run as designed.

---

## 12. Failure Signatures And Recovery Moves

### 1. Polite Convergence

Signature:

- multiple agents say the same thing in different language
- the critic raises only soft objections
- synthesis looks clean but unsurprising

Recovery:

- swap the critic to the strongest natural dissenter
- add one more contrarian or edge-case axis
- reopen one consensus claim and require best-case and failure-case versions

### 2. Performative Scoring

Signature:

- scores are assigned, but they do not change any prioritization
- high scores cluster around verbose claims rather than grounded ones

Recovery:

- force every high-ranked claim to cite its `Evidence / basis` explicitly
- downscore any claim whose evidence is only rephrased confidence
- compare the top 3 claims with scores hidden, then re-rank and inspect the mismatch

### 3. Context Overload

Signature:

- Round 2 outputs become shallow or generic
- agents stop referencing claim IDs consistently
- blind-spot additions are repetitive

Recovery:

- lower the number of carried full-text claims
- preserve summaries plus ledger rows, not raw transcripts
- reduce the number of claims reviewed per agent

### 3.5. Duplicate Flood

Signature:

- Round 1 produces many claims, but most collapse into the same few ideas
- critique budget gets spent restating overlaps rather than testing differences

Recovery:

- normalize claims before critique
- preserve alias IDs and caveats in the ledger
- critique the normalized set directly on narrow questions

### 4. False Novelty

Signature:

- many claims receive `Novelty = 2`, but most are restatements with cosmetic framing changes

Recovery:

- merge duplicates aggressively in the ledger
- require novelty to mean either a new mechanism, a new stakeholder impact, or a new decision path
- if two claims imply the same next action, they are probably not both novel

### 5. Weak Evidence Inflation

Signature:

- surprising claims dominate the ranking without enough basis
- `Evidence = 1` claims crowd out `Evidence = 2` claims

Recovery:

- raise the temporary portfolio threshold to require `Evidence >= 1` and `Actionability >= 1`
- require the critic to target the highest-ranked low-evidence claim first
- move speculative but interesting claims to `OPEN` instead of `SURVIVES`

### 6. Axis Starvation

Signature:

- one or more coverage axes produce no useful surviving claims
- synthesis still pretends the portfolio is complete

Recovery:

- mark the axis as a `Major blind spot`
- run a targeted gap-fill pass on only that axis
- do not synthesize a final portfolio until the blind spot is either filled or explicitly accepted

### 7. Synthesis Laundering

Signature:

- the final answer is cleaner than the ledger justifies
- dissent disappears even though objections remain `OPEN`

Recovery:

- synthesize from the ledger first, raw text second
- force the synthesis to list the strongest unresolved objection before any recommendation
- reopen the highest-objection claim if it materially changes the ranking

### 8. Over-Engineering The Run

Signature:

- the protocol work exceeds the value of the question
- setup consumes more time than reasoning

Recovery:

- switch to `Fast / Decision`
- reduce to 3-4 agents
- drop recombination unless the question truly benefits from portfolio output

### 9. Evidence-Free Confidence

Signature:

- the panel sounds precise but has no actual evidence pack
- factual claims are treated as settled because they are repeated cleanly

Recovery:

- stop the run and do evidence intake
- relabel unsupported claims as inference
- rerun only the affected claims if the rest of the ledger is still valid

### 10. Mode Drift

Signature:

- the run started in one mode, but the operator cannot explain why it is still there
- the process keeps going out of habit rather than because the mode still fits

Recovery:

- answer the preflight questions again mid-run
- either switch modes explicitly or stop
- record the switch or abort reason in the closure block

Operator rule:

- If two failure signatures appear at once, stop adding process and simplify the run before continuing.
- If one failure signature is `Evidence-Free Confidence`, do not continue reasoning until evidence intake is done.

---

## 13. Protocol History

- `v1.0` (2026-04-06): 5-round protocol. Worked but was verbose, polite, and slow.
- `v2.0` (2026-04-06): 3-round protocol optimized for speed and convergence.
- `v2.1` (2026-04-14): dual-mode rewrite. Preserved the fast path, added a true high-output discovery path, made persona divergence explicit, replaced early-exit logic in discovery mode with novelty and coverage gates, and added claim IDs plus a lightweight ledger.
- `v2.2` (2026-04-14): attack-driven hardening pass. Added evidence fields, explicit ledger updates, scoring rules, cross-assigned critique, operational definitions for gates and rankings, and tighter recombination and defense rules.
- `v2.3` (2026-04-14): operator scaffolding pass. Added default persona preset packs and a worked example so the protocol is easier to run consistently without inventing setup structure from scratch each time.
- `v2.4` (2026-04-14): execution scaffolding pass. Added a minimal run sheet, a copyable ledger template, and a failure-signatures recovery playbook for real repeated use.
- `v2.5` (2026-04-14): flow-control pass. Added preflight, question taxonomy, evidence intake, explicit mode-switch and abort rules, closure blocks, and a fresh-agent policy.
- `v2.6` (2026-04-14): normalization pass. Added an explicit claim-normalization stage between Round 1 and critique, preserved alias IDs/origins in the ledger, and wired normalization into the templates, run sheet, and failure-recovery playbook.

### Named Dissents Preserved

- `Okafor`: some high-stakes decisions still need formal defense, not just critique.
- `Santos`: unanimous LLM agreement can reflect shared training bias rather than independent validation.

---

*Note: the original optimization transcripts referenced by v2.0 are not currently checked into this repo.*
