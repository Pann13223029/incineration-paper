# Defense Slide Outline

Lean oral-defense deck for a bachelor's thesis defense or committee conversation. Target: `5-7` slides, `8-12` minutes, with the appendix or Q&A bank carrying anything extra.

Use this as a speaking outline, not as a content dump. Each slide should have one claim, one visual or compact table, and one transition sentence.

---

## Slide 1. Question and contribution

**Title:** Why Japan's incinerator fleet must be split into two questions

**Core message:** The thesis shows that Japan's incineration transition is empirically two-part: observed entry into power generation is an extensive-margin modernization problem, while efficiency among generators is an intensive-margin performance problem.

**Keep on slide**

- 23,599 facility-year observations
- 2,948 facilities
- FY2005-FY2024
- Research question:
  - What predicts observed transition into power generation?
  - Conditional on generation, what predicts energy recovery efficiency?

**Visual**

- Reuse the fleet split graphic from [readme_fleet_split.svg](/Users/openclaw/incineration-thesis/docs/figures/readme_fleet_split.svg:1) or a simplified version

**Say aloud**

- The older version of the thesis over-asked a generator-only sample to explain the whole fleet.
- The redesign fixes that by separating adoption from conditional efficiency.

---

## Slide 2. Data and empirical architecture

**Title:** One dataset, two linked analytical frames

**Core message:** The design is strong because it uses one administrative panel but answers two different empirical questions with two different frames.

**Keep on slide**

- Coded full-fleet frame: `19,827` observations
- Adoption risk set: `13,770` facility-years, `2,035` facilities, `141` observed first-adoption events
- Lagged adoption model frame: `11,717` facility-years, `1,915` facilities, `140` retained events
- Generator regression frame: `5,683` facility-years, `1,016` facilities

**Visual**

- Simple two-box architecture diagram:
  - `Observed transition into generation`
  - `Conditional efficiency among generators`

**Say aloud**

- The adoption model is lagged to avoid same-year redesign contamination.
- The generator model is not asked to explain who generates at all.

---

## Slide 3. Extensive-margin result

**Title:** Transition into generation is selective, not diffuse

**Core message:** Old and small facilities rarely record observed transition into power generation in the coded panel.

**Keep on slide**

- Prior-year age `10-20`: `-1.76` pp
- Prior-year age `20-30`: `-1.72` pp
- Prior-year age `30+`: `-1.13` pp
- Prior-year capacity: `0.50` pp per `100 t/day`
- `109` of `141` observed adoption events occur in FY2013-FY2019

**Visual**

- Compact hazard table from [adoption_results.md](/Users/openclaw/incineration-thesis/output/adoption_results.md:41)

**Say aloud**

- The thesis does not show widespread late conversion among old small plants.
- Transition is already concentrated among facilities that were younger and larger before the event year.

---

## Slide 4. Pathway audit and calibration

**Title:** The observed modernization wave is mostly capital-reset-like

**Core message:** The event-level audit strengthens the policy interpretation without pretending to identify one unique mechanism.

**Keep on slide**

- Reset/rebuild-like: `82`
- Continuity/in-place-upgrade-like: `38`
- Forward-dated/placeholder: `20`
- Unresolved: `1`

**Visual**

- One stacked bar or four-category bar chart using [adoption_pathway_audit.csv](/Users/openclaw/incineration-thesis/output/adoption_pathway_audit.csv:1)

**Say aloud**

- This supports “capital-side modernization is empirically prominent.”
- It does **not** justify “replacement uniquely identified” or “retrofit never happens.”

---

## Slide 5. Intensive-margin result

**Title:** Conditional efficiency is shaped by age, scale, and bounded responsiveness

**Core message:** Once facilities are already generating, the largest differences are between facilities, not within the same facility over time.

**Keep on slide**

- Facility age: `-0.019` to `-0.035`
- Capacity: `+0.040` to `+0.103`
- Utilization: `+0.541` to `+0.779`
- Within/total ratio: `0.1499`
- Pre-Fukushima: `0.1795`
- Post-Fukushima: `0.0956`

**Visual**

- The main regression table plus a one-line within/total ratio callout

**Say aloud**

- This is why the thesis argues for bounded responsiveness rather than pure operational reversibility.
- It is the strongest lock-in-related finding, but still framed as “strongly consistent with,” not “causally proven.”

---

## Slide 6. What the thesis claims and does not claim

**Title:** Stronger because narrower

**Core message:** The thesis is more defensible because it now draws a hard boundary around its claims.

**Keep on slide**

- Does claim:
  - two-part architecture
  - selective observed transition into generation
  - bounded responsiveness within generators
  - capital-side modernization likely matters more than operations alone
- Does not claim:
  - strict causal proof
  - replacement is the only pathway
  - full net climate accounting
  - heat-recovery or district-heating evaluation

**Visual**

- Two-column “claims / non-claims” mini table pulled from [what-this-thesis-does-not-claim.md](/Users/openclaw/incineration-thesis/research/notes/what-this-thesis-does-not-claim.md:1)

**Say aloud**

- The narrower claim is not weaker. It is stronger because it matches the evidence.

---

## Slide 7. Policy takeaway and closing

**Title:** What follows for Japan's fleet

**Core message:** The evidence points toward a policy hierarchy: capital-side modernization and regional consolidation first, operations second, with explicit limits on what the thesis can identify.

**Keep on slide**

- Old and small facilities rarely record observed transition into generation
- Among generators, vintage and scale gaps remain large
- Reset/rebuild-like events are the largest observed pathway bucket
- Therefore:
  - capital-side modernization
  - retirement / major refurbishment
  - regional consolidation
  - routing and utilization as secondary levers

**Final sentence**

Japan's incineration transition is happening, but it is selective and slower than a net-zero-compatible fleet transformation would require.

---

## Delivery notes

- Spend the most time on Slides `2-5`.
- If time is cut, compress Slides `6-7`, not Slides `2-5`.
- If challenged early on causality, jump directly to Slide `6`.
- If challenged on policy overreach, jump directly to Slide `4` then Slide `6`.
