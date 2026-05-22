---
marp: true
paginate: true
theme: paper-zoom
size: 16:9
title: Explaining the Waste-Incineration Paper Clearly
description: Paper-only Zoom briefing deck for the Japan waste-incineration facility-panel study.
---

<!-- _class: hero -->

# Explaining the Paper Clearly

## Selective modernization and bounded responsiveness in Japan's waste-incineration fleet

<div class="pill-row">
  <span class="pill">10-15 minute Zoom briefing</span>
  <span class="pill">Paper only</span>
  <span class="pill">Full script available</span>
</div>

<div class="meta">
  Pann Phetra<br/>
  Paper briefing deck generated from the reproducible paper workspace
</div>

<!--
Script cue: Start by saying this is not a general lecture on waste incineration. It is a focused explanation of one paper: what problem it studies, how the evidence is organized, what it finds, and what claim boundary makes it defensible.
-->

---

# The 30-Second Version

<div class="three-col">
  <div class="claim-card good">
    <p class="eyebrow">Problem</p>
    <p class="big">Japan burns waste widely, but electricity recovery is uneven.</p>
    <p class="small">By FY2024, only 41.1% of facilities in the panel are flagged as power-generating.</p>
  </div>
  <div class="claim-card good">
    <p class="eyebrow">Design</p>
    <p class="big">The paper separates two questions that averages mix together.</p>
    <p class="small">First, which non-generators enter power generation? Second, how well do generators perform once they exist?</p>
  </div>
  <div class="claim-card good">
    <p class="eyebrow">Finding</p>
    <p class="big">Entry is selective; generator performance remains structured.</p>
    <p class="small">Younger and larger facilities are more likely to enter; older, smaller, less utilized generators recover less electricity per tonne.</p>
  </div>
</div>

<div class="callout">
  <p><strong>One-line takeaway:</strong> Japan's incineration transition should not be summarized as one average fleet problem.</p>
</div>

<!--
Script cue: Give the listener the destination first. The paper is about a diagnostic split: entry into generation versus performance after entry.
-->

---

# Why This Issue Matters

<div class="two-col wide-left">
  <div class="diagram-card">
    <div class="flow">
      <div class="flow-step">
        <p class="step-number">1</p>
        <p class="mini-title">Waste is burned</p>
        <p class="mini-text">Incineration reduces waste volume and supports hygienic municipal disposal.</p>
      </div>
      <div class="flow-arrow">→</div>
      <div class="flow-step">
        <p class="step-number">2</p>
        <p class="mini-title">Heat is produced</p>
        <p class="mini-text">The plant already creates heat; the question is whether useful energy is recovered.</p>
      </div>
      <div class="flow-arrow">→</div>
      <div class="flow-step">
        <p class="step-number">3</p>
        <p class="mini-title">Electricity may be generated</p>
        <p class="mini-text">Only some facilities convert waste heat into reported electricity generation.</p>
      </div>
    </div>
  </div>
  <div class="card">
    <p class="eyebrow">Plain-language context</p>
    <p class="body">The policy issue is not simply whether Japan uses incineration. Japan already relies heavily on incineration. The sharper issue is whether facilities recover useful energy from that system, and whether old or small facilities can realistically catch up.</p>
  </div>
</div>

<div class="callout">
  <p>This makes the paper a fleet-diagnosis study, not a broad argument that incineration itself is always good or bad.</p>
</div>

<!--
Script cue: Use this slide to orient non-specialists. Explain the physical intuition before describing the econometrics.
-->

---

# The Main Trap: One Average Fleet

<div class="two-col">
  <div class="card">
    <p class="eyebrow">What an average hides</p>
    <p class="big">A single fleet average mixes two different bottlenecks.</p>
    <ul>
      <li>Some facilities do not generate electricity at all.</li>
      <li>Some facilities generate, but recover electricity less efficiently.</li>
      <li>Averages blur the difference between entering generation and performing well after entry.</li>
    </ul>
  </div>
  <div class="diagram-card">
    <div class="matrix">
      <div class="cell warning">
        <p class="eyebrow">Non-generators</p>
        <p class="mini-title">Entry problem</p>
        <p class="mini-text">Do they ever report power generation?</p>
      </div>
      <div class="cell safe">
        <p class="eyebrow">Generators</p>
        <p class="mini-title">Performance problem</p>
        <p class="mini-text">How much electricity per tonne do they recover?</p>
      </div>
      <div class="cell secondary">
        <p class="eyebrow">Weak shortcut</p>
        <p class="mini-title">One average</p>
        <p class="mini-text">Looks simple, but loses the bottleneck location.</p>
      </div>
      <div class="cell primary">
        <p class="eyebrow">Paper design</p>
        <p class="mini-title">Two linked margins</p>
        <p class="mini-text">Separate the gate into generation from performance within generation.</p>
      </div>
    </div>
  </div>
</div>

<!--
Script cue: This is the conceptual heart of the presentation. Do not rush it.
-->

---

# Research Questions

<div class="three-col">
  <div class="card">
    <p class="eyebrow">RQ1: Adoption</p>
    <p class="big">Who enters electricity generation?</p>
    <p class="small">Among facilities first observed without generation, which ones later first report power generation?</p>
  </div>
  <div class="card">
    <p class="eyebrow">RQ2: Efficiency</p>
    <p class="big">Who performs better after entry?</p>
    <p class="small">Among identifiable operating generators, how much electricity is recovered per tonne processed?</p>
  </div>
  <div class="card">
    <p class="eyebrow">RQ3: Synthesis</p>
    <p class="big">Do both margins tell one story?</p>
    <p class="small">Or does the fleet contain different modernization problems at different points?</p>
  </div>
</div>

<div class="callout">
  <p><strong>Translation:</strong> First ask who gets through the door. Then ask how well they do once they are inside.</p>
</div>

<!--
Script cue: Make clear that the paper is organized around questions, not around methods for their own sake.
-->

---

# Data and Sample Architecture

<div class="kpi-grid two">
  <div class="kpi-card">
    <p class="eyebrow">Administrative source</p>
    <p class="kpi">FY2005-FY2024</p>
    <p class="kpi-label">Ministry of the Environment General Waste Treatment Survey</p>
    <p class="kpi-note">A national facility-level panel covering Japanese municipal waste incineration facilities.</p>
  </div>
  <div class="kpi-card">
    <p class="eyebrow">Full source panel</p>
    <p class="kpi">23,599</p>
    <p class="kpi-label">facility-year observations</p>
    <p class="kpi-note">2,948 identifiable facilities across 47 prefectures.</p>
  </div>
  <div class="kpi-card">
    <p class="eyebrow">Adoption frame</p>
    <p class="kpi">13,770</p>
    <p class="kpi-label">at-risk facility-years</p>
    <p class="kpi-note">2,035 facilities first observed without generation, with 141 observed first-adoption events.</p>
  </div>
  <div class="kpi-card">
    <p class="eyebrow">Generator frame</p>
    <p class="kpi">5,683</p>
    <p class="kpi-label">canonical generator rows</p>
    <p class="kpi-note">1,016 identifiable operating generators used for conditional-efficiency models.</p>
  </div>
</div>

<!--
Script cue: Do not list every cleaning rule orally. Emphasize why two samples are necessary.
-->

---

# Design Logic in One Diagram

<div class="two-col wide-right">
  <div class="figure-card">
    <img src="../figures/figure1_two_part_framework.png" alt="Two-part analytical framework" />
  </div>
  <div class="stack">
    <div class="card">
      <p class="eyebrow">Extensive margin</p>
      <p class="big">Transition into generation</p>
      <p class="small">Estimated with a lagged discrete-time hazard among facilities still at risk of first reported generation.</p>
    </div>
    <div class="card">
      <p class="eyebrow">Intensive margin</p>
      <p class="big">Efficiency among generators</p>
      <p class="small">Estimated with descriptive panel models for electricity generated per tonne processed.</p>
    </div>
  </div>
</div>

<div class="callout">
  <p>The samples are linked but not identical because they answer different questions.</p>
</div>

<!--
Script cue: This is where you justify the architecture. A single sample would be cleaner-looking but wrong for the research question.
-->

---

# Result 1: Adoption Is Selective

<div class="two-col wide-right">
  <div class="figure-card">
    <img src="../figures/figure2_selective_transition.png" alt="Observed adoption event rates by age and capacity" />
  </div>
  <div class="stack">
    <div class="card">
      <p class="eyebrow">By age</p>
      <p class="big">Events collapse after age 10.</p>
      <p class="small">Facilities aged 0-10 account for 102 of 141 first-adoption events.</p>
    </div>
    <div class="card">
      <p class="eyebrow">By capacity</p>
      <p class="big">Events concentrate in large plants.</p>
      <p class="small">The largest capacity quartile accounts for 99 first-adoption events; the smallest quartile records only 1.</p>
    </div>
  </div>
</div>

<!--
Script cue: The figure should carry the visual result. Your spoken explanation should translate the pattern: adoption is not spreading evenly across the fleet.
-->

---

# Result 1 in Plain English

<div class="two-col">
  <div class="card">
    <p class="eyebrow">Hazard model summary</p>
    <p class="big">Older at-risk facilities are less likely to first report generation.</p>
    <ul>
      <li>Age 10-20: about <strong>-1.76 percentage points</strong>.</li>
      <li>Age 20-30: about <strong>-1.72 percentage points</strong>.</li>
      <li>Age 30+: about <strong>-1.13 percentage points</strong>.</li>
      <li>Capacity: each extra 100 t/day adds about <strong>+0.50 percentage points</strong>.</li>
    </ul>
  </div>
  <div class="card">
    <p class="eyebrow">Pathway audit</p>
    <p class="big">The observed event mix looks capital-intensive, but not one single mechanism.</p>
    <ul>
      <li>82 reset/rebuild-like transitions.</li>
      <li>38 continuity or in-place upgrade-like transitions.</li>
      <li>20 forward-dated or placeholder entries.</li>
    </ul>
  </div>
</div>

<div class="callout">
  <p><strong>Defensible wording:</strong> selective modernization, not proof that replacement is the only pathway.</p>
</div>

<!--
Script cue: Explain percentage points carefully. These are changes in annual probability of first reporting generation, not changes in engineering efficiency.
-->

---

# Result 2: Generator Performance Is Structured

<div class="two-col wide-right">
  <div class="figure-card">
    <img src="../figures/figure3_efficiency_structure.png" alt="Generator efficiency structure by age and variance ratio" />
  </div>
  <div class="stack">
    <div class="card">
      <p class="eyebrow">Performance gradient</p>
      <p class="big">Older generators recover less electricity per tonne.</p>
      <p class="small">The pattern is descriptive, but stable across main model variants.</p>
    </div>
    <div class="card">
      <p class="eyebrow">Variance structure</p>
      <p class="big">Most differences are between facilities.</p>
      <p class="small">The within-to-total variance ratio is 0.1499, and only 0.0956 after 2011.</p>
    </div>
  </div>
</div>

<!--
Script cue: Do not overclaim irreversibility. Say performance is bounded and structured, not impossible to improve.
-->

---

# Result 2 in Plain English

<div class="three-col">
  <div class="card">
    <p class="eyebrow">Age</p>
    <p class="big">Older plants tend to perform worse.</p>
    <p class="small">This likely reflects durable design, inherited equipment, and institutional constraints, not age alone as a magic cause.</p>
  </div>
  <div class="card">
    <p class="eyebrow">Scale</p>
    <p class="big">Larger plants tend to perform better.</p>
    <p class="small">Scale can support better energy recovery and steadier operation, although the paper does not prove a single mechanism.</p>
  </div>
  <div class="card">
    <p class="eyebrow">Utilization</p>
    <p class="big">Better-loaded plants perform better.</p>
    <p class="small">Operations still matter, but they do not erase the larger cross-facility hierarchy.</p>
  </div>
</div>

<div class="callout">
  <p>The generator result is not "nothing can be improved." It is "improvement happens within a performance envelope shaped by facility characteristics."</p>
</div>

<!--
Script cue: This slide protects the paper from sounding fatalistic.
-->

---

# The Combined Story

<div class="diagram-card">
  <div class="flow">
    <div class="flow-step">
      <p class="step-number">A</p>
      <p class="mini-title">Non-generating segment</p>
      <p class="mini-text">The first problem is whether facilities enter electricity recovery at all.</p>
    </div>
    <div class="flow-arrow">→</div>
    <div class="flow-step">
      <p class="step-number">B</p>
      <p class="mini-title">Generating segment</p>
      <p class="mini-text">The second problem is how much electricity generators recover per tonne.</p>
    </div>
    <div class="flow-arrow">→</div>
    <div class="flow-step">
      <p class="step-number">C</p>
      <p class="mini-title">Planning implication</p>
      <p class="mini-text">Fleet triage and generator optimization should be treated as separate tasks.</p>
    </div>
  </div>
</div>

<div class="two-col">
  <div class="card">
    <p class="eyebrow">If a plant does not generate</p>
    <p class="big">Ask renewal, consolidation, or entry questions.</p>
  </div>
  <div class="card">
    <p class="eyebrow">If a plant already generates</p>
    <p class="big">Ask utilization, routing, and upgrade questions.</p>
  </div>
</div>

<!--
Script cue: This is the policy bridge. Keep it practical and avoid prescribing one universal solution.
-->

---

# What Makes the Paper Original

<div class="three-col">
  <div class="card">
    <p class="eyebrow">Originality 1</p>
    <p class="big">Same national panel, two linked margins.</p>
    <p class="small">The paper studies both observed entry into generation and conditional performance after entry.</p>
  </div>
  <div class="card">
    <p class="eyebrow">Originality 2</p>
    <p class="big">It exposes what aggregate fleet views hide.</p>
    <p class="small">The evidence distinguishes selective entry from persistent generator hierarchy.</p>
  </div>
  <div class="card">
    <p class="eyebrow">Originality 3</p>
    <p class="big">It is careful about claim boundaries.</p>
    <p class="small">The paper does not pretend to identify one causal modernization mechanism.</p>
  </div>
</div>

<div class="callout">
  <p>The publication pitch is not "Japan is understudied." It is "entry and conditional performance should be separated before the fleet is interpreted."</p>
</div>

<!--
Script cue: This answers the question: why does this deserve to be a paper rather than just a thesis chapter?
-->

---

# What the Paper Does Not Claim

<div class="two-col">
  <div class="claim-card boundary">
    <p class="eyebrow">Boundaries</p>
    <ul>
      <li>It does not estimate a strict causal effect of age, scale, or policy.</li>
      <li>It does not prove replacement is the only modernization pathway.</li>
      <li>It does not calculate complete lifecycle climate benefits.</li>
      <li>It does not treat the generator frame as a full census of all generation activity.</li>
    </ul>
  </div>
  <div class="claim-card good">
    <p class="eyebrow">Defended claim</p>
    <p class="big">The paper is a diagnostic fleet decomposition.</p>
    <p class="small">Its strength is showing where the bottleneck appears in the data: selective entry into generation and bounded performance among operating generators.</p>
  </div>
</div>

<!--
Script cue: Use this slide to sound rigorous, not defensive. Good papers are clear about what they do not identify.
-->

---

# Likely Zoom Questions

<div class="stack">
  <div class="q-card">
    <p><strong>Q: Is this causal?</strong> No. It is a structured diagnostic analysis with explicit sample limits and robustness checks.</p>
  </div>
  <div class="q-card">
    <p><strong>Q: Why not one model for the whole fleet?</strong> Because non-generators and generators answer different questions; one model would mix entry with performance.</p>
  </div>
  <div class="q-card">
    <p><strong>Q: Does this mean old plants cannot improve?</strong> No. It means broad late-life catch-up is not what dominates the observed data.</p>
  </div>
  <div class="q-card">
    <p><strong>Q: What should municipalities do?</strong> First separate asset-renewal screening for non-generators from optimization of existing generators.</p>
  </div>
</div>

<!--
Script cue: Keep answers short. Invite detailed methods questions only if the audience wants them.
-->

---

<!-- _class: close -->

# Closing Takeaway

<p class="subtitle">The paper argues that Japan's incineration fleet should be read as a two-part modernization problem, not as one average transition curve.</p>

<div class="close-line">
  <p>First ask which facilities enter energy recovery. Then ask how well generators perform after entry. The policy diagnosis changes when those margins are separated.</p>
</div>

<!--
Script cue: End with the one sentence you want remembered. Then stop and invite questions.
-->

---

<!-- _class: appendix dense -->

# Appendix A: Model Details

<div class="two-col">
  <div class="card">
    <p class="eyebrow">Adoption model</p>
    <p class="body">Lagged discrete-time logit hazard among facilities still at risk of first observed generation.</p>
    <ul>
      <li>Outcome: first report of power generation in the next observed year.</li>
      <li>Predictors: prior-year age band and design capacity.</li>
      <li>Controls: fiscal-year fixed effects and prefecture fixed effects.</li>
      <li>Uncertainty: facility-clustered standard errors.</li>
    </ul>
  </div>
  <div class="card">
    <p class="eyebrow">Efficiency model</p>
    <p class="body">Descriptive panel models among identifiable operating generators.</p>
    <ul>
      <li>Outcome: winsorized log electricity generated per tonne processed.</li>
      <li>Predictors: age, capacity, utilization, heating value, grid-emission control.</li>
      <li>Models: pooled OLS, year fixed effects, random effects, year fixed effects plus random effects.</li>
      <li>Uncertainty: facility-clustered standard errors.</li>
    </ul>
  </div>
</div>

---

<!-- _class: appendix dense -->

# Appendix B: Key Numbers to Remember

| Evidence item | Number | Interpretation |
|:--|--:|:--|
| FY2024 facilities flagged as power-generating | 41.1% | Most facilities remain outside electricity generation in the panel. |
| Adoption risk-set size | 13,770 | Facility-years first observed without generation. |
| Observed first-adoption events | 141 | Events used to describe entry into generation. |
| Events from age 0-10 facilities | 102 | Adoption is concentrated among young facilities. |
| Events in largest capacity quartile | 99 | Adoption is concentrated among large facilities. |
| Generator regression frame | 5,683 | Identifiable operating-generator observations. |
| Within-to-total variance ratio | 0.1499 | Most generator-efficiency variation is between facilities. |

---

<!-- _class: appendix dense -->

# Appendix C: File Map

<div class="kpi-grid two">
  <div class="card">
    <p class="eyebrow">Slides</p>
    <p class="big">paper/slides/paper-zoom-briefing.md</p>
    <p class="small">Editable source deck.</p>
  </div>
  <div class="card">
    <p class="eyebrow">Script</p>
    <p class="big">paper/slides/paper-zoom-script.md</p>
    <p class="small">Full speaking script and timing guide.</p>
  </div>
  <div class="card">
    <p class="eyebrow">PDF</p>
    <p class="big">paper/share/paper-zoom-briefing.pdf</p>
    <p class="small">Shareable screen-sharing file after export.</p>
  </div>
  <div class="card">
    <p class="eyebrow">Build command</p>
    <p class="big">npm run slides:paper:pdf</p>
    <p class="small">Regenerates the PDF from the Markdown source.</p>
  </div>
</div>

