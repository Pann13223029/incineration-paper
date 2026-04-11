# Optimized Multi-Agent Discussion Protocol v2.0

*Synthesized from a 5-expert, 3-round optimization panel. Replaces v1.0.*

---

## 1. Final Recommended Structure

### Overview

Three rounds. Three to five agents. One human review at the end. Target wall-clock time: 5-6 minutes for parallel-capable orchestrators, 8-10 minutes for sequential execution.

### Round 1: Independent Brainstorm (Parallel)

- **Agents:** 3-5, each assigned a distinct persona via system prompt, because persona framing is one of the few levers that reliably shifts LLM output distribution.
- **Visibility:** None. Agents do not see each other's outputs, because independent generation maximizes diversity before convergence pressure sets in.
- **Word cap:** 300 words per agent, because this forces prioritization and keeps Round 2 context manageable.
- **Output format:** Structured claims. Each agent outputs 2-4 numbered positions, each consisting of a one-sentence claim and a one-sentence justification. No free-text essays, because structured claims survive handoffs with less information loss.
- **Timing:** All agents run in parallel. Target: 60-90 seconds.

### Round 2: Critique-with-Stakes (Parallel)

- **Agents:** Same 3-5 agents, same personas.
- **Visibility:** Every agent receives the full, unedited Round 1 outputs from all other agents, passed as direct context. No human summary, no intermediate ledger, because summarization is where information dies and the human is the bottleneck.
- **Adversarial requirement:** At least one agent must be assigned the Adversarial Critic role. This agent must attack the strongest consensus position from Round 1, even if it aligns with their persona's natural inclination, because unchallenged consensus among LLMs often reflects shared training data rather than independent validation. Remaining agents critique freely but must explicitly tag each Round 1 claim: ENDORSE / REJECT / MODIFY.
- **Word cap:** 400 words per agent, because critique requires engaging with others' positions.
- **Output format:** For each Round 1 claim addressed: ENDORSE / REJECT / MODIFY tag + one-sentence rationale. New claims tagged as NEW.
- **Timing:** All agents run in parallel. Target: 60-90 seconds.

### Conditional Early Exit Check

After Round 2, evaluate: Did all agents ENDORSE the same core claims AND were personas designed with genuinely divergent priors? If both conditions hold, proceed to synthesis with an early-consensus note. Because 70% of usable insight emerges in Round 1 and 20% in Round 2.

**Caveat:** LLM unanimous agreement may reflect shared training biases. Apply skepticism on topics where training corpora have narrow coverage.

### Round 3: Synthesis (Single Agent)

- **Agent:** One synthesis agent with a dedicated synthesizer persona.
- **Visibility:** Full Round 1 and Round 2 outputs from all agents, direct context.
- **Word cap:** 500 words, because the final output should be shorter than inputs.
- **Output requirements:**
  1. State the consensus position
  2. List surviving dissents with persona name and one-sentence summary
  3. Assign confidence level: HIGH / MEDIUM / LOW
- **Timing:** Target: 60-90 seconds.

### Human Review

The human reviews only the Round 3 synthesis. If unsatisfied, adjust persona prompts or constraints and re-run the entire protocol. No mid-stream steering, because partial intervention creates inconsistent context.

---

## 2. Why It Wins

The previous 5-round protocol spent three rounds on iterative debate yielding ~2% of insight while doubling execution time and tripling context usage. This 3-round version captures 90% of insight in half the time. Direct context passing eliminates information loss from human-mediated handoffs. The mandatory adversarial role preserves sharpening without a dedicated debate round. Conditional early exit avoids wasting compute when agreement is genuine.

---

## 3. What Was Rejected

- **5-round structure** — rounds 4-5 contributed ~2% of insight, doubled wall-clock time
- **Human-in-the-loop between rounds** — human was the throughput bottleneck
- **JSON evidence ledger** — structural overhead without improving short-protocol outcomes
- **Free-text essays in Round 1** — unstructured output loses information at handoffs
- **Rotating adversarial role across all agents** — diluted; single dedicated critic is sharper
- **Automated consensus-detection** — simple tag-counting achieves the same goal

---

## 4. When to Use a Lighter Version

Scale to **2 rounds** (brainstorm + synthesis, skip critique) when:
- The question is generative, not evaluative (brainstorm names vs. evaluate strategy)
- Time budget is under 3 minutes
- Topic is low-stakes and reversible

Scale to **2 agents** when scope is narrow and doesn't benefit from multiple perspectives.

---

## 5. When to Use a Stricter Version

Add **Round 2.5: Formal Defense** when:
- Decision is high-stakes, costly to reverse, or affects many people
- Round 2 surfaced a fundamental objection needing structured rebuttal
- Willing to spend 10-15 minutes instead of 5-6

Add a **structured evidence ledger** when:
- Output will be audited or requires regulatory traceability
- Protocol runs repeatedly on related questions and conclusions must be tracked over time

Scale to **6-7 agents** when topic spans multiple distinct domains.

---

## 6. Paste-Ready Protocol Template

```
=== MULTI-AGENT DISCUSSION PROTOCOL v2.0 ===

TOPIC: {{TOPIC}}
QUESTION: {{QUESTION}}
NUMBER OF AGENTS: {{N_AGENTS}}  (recommend 3-5)

--- ROUND 1: INDEPENDENT BRAINSTORM (run all agents in parallel) ---

System prompt for each agent:

"""
You are {{PERSONA_NAME}}, a {{PERSONA_DESCRIPTION}}.

Your task: Respond to the following question from your unique perspective.

Question: {{QUESTION}}

Rules:
- Output exactly 2-4 numbered positions.
- Each position: one sentence stating your claim, then one sentence
  justifying it.
- Maximum 300 words total.
- Do not hedge or qualify. State your positions clearly.
- You have not seen anyone else's response. Reason independently.
"""

--- ROUND 2: CRITIQUE-WITH-STAKES (run all agents in parallel) ---

System prompt for the Adversarial Critic (assign to exactly 1 agent):

"""
You are {{PERSONA_NAME}}, a {{PERSONA_DESCRIPTION}}.
You have been assigned the Adversarial Critic role for this round.

Below are all Round 1 responses from the panel:

{{ALL_ROUND_1_OUTPUTS}}

Your task: Identify the strongest consensus position from Round 1 and
argue against it, even if you originally agreed with it. Then evaluate
the remaining claims.

Rules:
- For each claim you address, tag it: ENDORSE / REJECT / MODIFY.
- After the tag, provide one sentence of rationale.
- You may introduce new claims, tagged as NEW.
- Maximum 400 words total.
- You must challenge at least one consensus position substantively.
"""

System prompt for all other Round 2 agents:

"""
You are {{PERSONA_NAME}}, a {{PERSONA_DESCRIPTION}}.

Below are all Round 1 responses from the panel:

{{ALL_ROUND_1_OUTPUTS}}

Your task: Evaluate each claim from Round 1. State what you endorse,
what you reject, and what you would modify.

Rules:
- For each claim you address, tag it: ENDORSE / REJECT / MODIFY.
- After the tag, provide one sentence of rationale.
- You may introduce new claims, tagged as NEW.
- Maximum 400 words total.
"""

--- EARLY EXIT CHECK ---

Count ENDORSE/REJECT/MODIFY tags across all agents. If ALL agents
endorsed the same core claims AND personas had divergent priors,
proceed to synthesis with early-consensus note.

Caveat: Unanimous LLM agreement may reflect training-data convergence.

--- ROUND 3: SYNTHESIS (single agent) ---

"""
You are a Synthesis Agent. Produce the panel's final authoritative answer.

Original question: {{QUESTION}}

Round 1 outputs (independent brainstorm):
{{ALL_ROUND_1_OUTPUTS}}

Round 2 outputs (critique and evaluation):
{{ALL_ROUND_2_OUTPUTS}}

Rules:
- State the consensus position clearly.
- List surviving dissents by persona name (one sentence each).
  Dissent is an output feature, not a flaw.
- Assign confidence: HIGH / MEDIUM / LOW.
- Maximum 500 words.
- Do not introduce new positions. Work only with panel output.
"""

--- HUMAN REVIEW ---

Review Round 3 synthesis. If unsatisfied, adjust personas or
constraints and re-run. Do not steer mid-protocol.

=== END PROTOCOL ===
```

---

## Protocol History

- **v1.0** (2026-04-06): 5-round protocol (brainstorm → cross-examination → debate → convergence → synthesis). Worked but verbose, polite, and slow.
- **v2.0** (2026-04-06): 3-round protocol optimized by 5-expert meta-panel. Collapsed cross-examination and debate into single Critique-with-Stakes round. Removed human bottleneck between rounds. Added structured output format, adversarial critic role, conditional early exit. 50% faster, ~90% of output quality retained.

**Named dissents preserved:**
- **Okafor:** 3-round structure loses the defense-move where attacked agents formally rebut. For high-stakes decisions, add Round 2.5.
- **Santos:** Early exit may reflect shared LLM training biases, not genuine independent agreement. Skepticism warranted.

---

*Full optimization panel transcripts: `research/notes/expert-panel/protocol-optimization/`*
