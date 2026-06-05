---
marp: true
paginate: true
theme: paper-zoom
size: 16:9
title: Simple Briefing on the Waste-Incineration Paper
description: Streamlined paper-only Zoom briefing deck for the Japan waste-incineration facility-panel study.
---

<!-- _class: hero -->

# Explaining the Paper Simply

## Japan's waste-incineration energy-recovery paper

<div class="pill-row">
  <span class="pill">10-12 minute Zoom briefing</span>
  <span class="pill">Paper only</span>
  <span class="pill">Simple main route</span>
</div>

<div class="meta">
  Pann Phetra<br/>
  Paper briefing for discussion and feedback
</div>

<!--
Script cue: Set expectation. This is a simple explanation of the paper's claim, evidence, and requested feedback.
-->

---

# The Whole Argument

<div class="card single-card center">
  <p class="eyebrow">Core claim</p>
  <p class="reader-line">Do not read Japan's incineration fleet as one average transition curve.</p>
</div>

<div class="three-col">
  <div class="card">
    <p class="eyebrow">Part 1</p>
    <p class="big">Some plants do not generate electricity.</p>
    <p class="small">This is the entry problem.</p>
  </div>
  <div class="card">
    <p class="eyebrow">Part 2</p>
    <p class="big">Generators perform unevenly.</p>
    <p class="small">This is the performance problem.</p>
  </div>
  <div class="card">
    <p class="eyebrow">Contribution</p>
    <p class="big">Separate the two problems.</p>
    <p class="small">The paper uses one national facility panel to read them together.</p>
  </div>
</div>

<!--
Script cue: If the listener remembers one thing, it should be entry first, performance second.
-->

---

# Why This Matters

<div class="diagram-card">
  <div class="flow">
    <div class="flow-step">
      <p class="step-number">1</p>
      <p class="mini-title">Waste is burned</p>
      <p class="mini-text">Japan relies heavily on municipal waste incineration.</p>
    </div>
    <div class="flow-arrow">&rarr;</div>
    <div class="flow-step">
      <p class="step-number">2</p>
      <p class="mini-title">Heat is produced</p>
      <p class="mini-text">Heat exists whether or not electricity is recovered.</p>
    </div>
    <div class="flow-arrow">&rarr;</div>
    <div class="flow-step">
      <p class="step-number">3</p>
      <p class="mini-title">Power is optional</p>
      <p class="mini-text">In FY2024, only 41.1% of panel facilities are flagged as power-generating.</p>
    </div>
  </div>
</div>

<div class="callout">
  <p>The paper asks where energy recovery appears inside the existing fleet, not whether incineration itself is always good or bad.</p>
</div>

<!--
Script cue: Keep this non-technical. The question is where useful electricity recovery appears.
-->

---

# The Design Choice

<div class="two-col">
  <div class="card">
    <p class="eyebrow">Group A</p>
    <p class="big">Facilities not yet generating</p>
    <p class="small">Question: which facilities first enter electricity generation?</p>
  </div>
  <div class="card">
    <p class="eyebrow">Group B</p>
    <p class="big">Facilities already generating</p>
    <p class="small">Question: how well do generators recover electricity per tonne?</p>
  </div>
</div>

<div class="callout">
  <p>A single fleet average mixes these two groups, so it hides the bottleneck.</p>
</div>

<!--
Script cue: This is the core logic. Avoid model vocabulary unless asked.
-->

---

# Data and Scope

<div class="kpi-grid two">
  <div class="kpi-card">
    <p class="eyebrow">Data source</p>
    <p class="kpi">FY2005-FY2024</p>
    <p class="kpi-label">Japan municipal facility panel</p>
    <p class="kpi-note">Ministry of the Environment General Waste Treatment Survey.</p>
  </div>
  <div class="kpi-card">
    <p class="eyebrow">Facilities</p>
    <p class="kpi">2,948</p>
    <p class="kpi-label">identifiable facilities</p>
    <p class="kpi-note">National facility-level evidence, not a small case study.</p>
  </div>
  <div class="kpi-card">
    <p class="eyebrow">Entry evidence</p>
    <p class="kpi">141</p>
    <p class="kpi-label">first-adoption events</p>
    <p class="kpi-note">Observed first reports of power generation.</p>
  </div>
  <div class="kpi-card">
    <p class="eyebrow">Generator evidence</p>
    <p class="kpi">5,683</p>
    <p class="kpi-label">generator observations</p>
    <p class="kpi-note">Used for conditional performance models.</p>
  </div>
</div>

<!--
Script cue: Say only enough data detail to build trust. Appendix has the full model details.
-->

---

# Result 1: Entry Is Selective

<div class="figure-card figure-wide">
  <img src="../figures/figure2_selective_transition.png" alt="Observed adoption event rates by age and capacity" />
</div>

<div class="callout">
  <p>First adoption into power generation is concentrated among younger and larger facilities.</p>
</div>

<!--
Script cue: Let the chart be visual evidence. Do not over-explain the axes.
-->

---

# Result 1 in Plain Numbers

<div class="two-col">
  <div class="kpi-card">
    <p class="eyebrow">Age pattern</p>
    <p class="kpi">102 / 141</p>
    <p class="kpi-label">events come from age 0-10 facilities</p>
    <p class="kpi-note">Older facilities account for far fewer first-adoption events.</p>
  </div>
  <div class="kpi-card">
    <p class="eyebrow">Capacity pattern</p>
    <p class="kpi">99 / 141</p>
    <p class="kpi-label">events are in the largest capacity quartile</p>
    <p class="kpi-note">The smallest quartile records only one event.</p>
  </div>
</div>

<div class="callout">
  <p>Plain meaning: adoption is not spreading evenly across the fleet.</p>
</div>

<!--
Script cue: These are the two numbers to say slowly.
-->

---

# Result 2: Performance Is Uneven

<div class="figure-card figure-wide">
  <img src="../figures/figure3_efficiency_structure.png" alt="Generator efficiency structure by age and variance ratio" />
</div>

<div class="callout">
  <p>Among generators, older facilities recover less electricity per tonne, and most variation is between facilities.</p>
</div>

<!--
Script cue: Avoid fatalistic wording. This is structured unevenness, not proof that improvement is impossible.
-->

---

# Result 2 in Plain Words

<div class="three-col">
  <div class="card">
    <p class="eyebrow">Age</p>
    <p class="big">Older generators tend to perform worse.</p>
    <p class="small">Age likely bundles design, equipment, and operating history.</p>
  </div>
  <div class="card">
    <p class="eyebrow">Scale</p>
    <p class="big">Larger generators tend to perform better.</p>
    <p class="small">Scale can support steadier operation.</p>
  </div>
  <div class="card">
    <p class="eyebrow">Operations</p>
    <p class="big">Utilization still matters.</p>
    <p class="small">Operations help, but they do not erase large facility gaps.</p>
  </div>
</div>

<!--
Script cue: Translate coefficients into intuitive drivers.
-->

---

# What This Means

<div class="diagram-card">
  <div class="flow">
    <div class="flow-step">
      <p class="step-number">A</p>
      <p class="mini-title">Non-generators</p>
      <p class="mini-text">Ask whether energy recovery is a plausible asset path.</p>
    </div>
    <div class="flow-arrow">&rarr;</div>
    <div class="flow-step">
      <p class="step-number">B</p>
      <p class="mini-title">Generators</p>
      <p class="mini-text">Ask how far performance can improve within existing constraints.</p>
    </div>
    <div class="flow-arrow">&rarr;</div>
    <div class="flow-step">
      <p class="step-number">C</p>
      <p class="mini-title">Planning</p>
      <p class="mini-text">Treat fleet triage and generator optimization as different tasks.</p>
    </div>
  </div>
</div>

<!--
Script cue: This is the practical interpretation. Keep it non-prescriptive.
-->

---

# What the Paper Does Not Claim

<div class="two-col">
  <div class="claim-card boundary">
    <p class="eyebrow">Boundaries</p>
    <ul class="simple-list">
      <li>No strict causal policy-effect claim.</li>
      <li>No proof that replacement is the only pathway.</li>
      <li>No complete lifecycle climate accounting.</li>
      <li>No claim that the generator frame is a perfect census.</li>
    </ul>
  </div>
  <div class="claim-card good">
    <p class="eyebrow">Defended claim</p>
    <p class="big">This is a diagnostic fleet decomposition.</p>
    <p class="small">It shows two bottlenecks: selective entry into generation and uneven performance among generators.</p>
  </div>
</div>

<!--
Script cue: Limits should sound disciplined, not apologetic.
-->

---

<!-- _class: close -->

# Closing and Feedback Ask

<p class="subtitle">The paper's message is simple: first ask which facilities enter energy recovery, then ask how well generators perform after entry.</p>

<div class="close-line">
  <p>Useful feedback: is this two-part story clear, defensible, and worth using as the paper's main pitch?</p>
</div>

<!--
Script cue: Stop here. Use appendices only if the listener asks.
-->

---

<!-- _class: appendix dense -->

# Appendix A: Model Details

<div class="two-col">
  <div class="card">
    <p class="eyebrow">Adoption model</p>
    <p class="body">Lagged discrete-time logit hazard among facilities still at risk of first observed generation.</p>
    <ul class="simple-list">
      <li>Outcome: first report of power generation in the next observed year.</li>
      <li>Predictors: prior-year age band and design capacity.</li>
      <li>Controls: fiscal-year fixed effects and prefecture fixed effects.</li>
      <li>Uncertainty: facility-clustered standard errors.</li>
    </ul>
  </div>
  <div class="card">
    <p class="eyebrow">Efficiency model</p>
    <p class="body">Descriptive panel models among identifiable operating generators.</p>
    <ul class="simple-list">
      <li>Outcome: winsorized log electricity generated per tonne processed.</li>
      <li>Predictors: age, capacity, utilization, heating value, grid-emission control.</li>
      <li>Models: pooled OLS, year FE, RE, and year FE plus RE.</li>
      <li>Uncertainty: facility-clustered standard errors.</li>
    </ul>
  </div>
</div>

---

<!-- _class: appendix dense -->

# Appendix B: Key Numbers

| Evidence item | Number | Interpretation |
|:--|--:|:--|
| FY2024 facilities flagged as power-generating | 41.1% | Most facilities remain outside electricity generation in the panel. |
| Source panel | 23,599 | Facility-year observations across FY2005-FY2024. |
| Adoption risk-set size | 13,770 | Facility-years first observed without generation. |
| Observed first-adoption events | 141 | Events used to describe entry into generation. |
| Events from age 0-10 facilities | 102 | Adoption is concentrated among young facilities. |
| Events in largest capacity quartile | 99 | Adoption is concentrated among large facilities. |
| Generator regression frame | 5,683 | Identifiable operating-generator observations. |
| Within-to-total variance ratio | 0.1499 | Most generator-efficiency variation is between facilities. |

---

<!-- _class: appendix dense -->

# Appendix C: Pathway Audit

<div class="three-col">
  <div class="kpi-card">
    <p class="eyebrow">Reset / rebuild-like</p>
    <p class="kpi">82</p>
    <p class="kpi-label">observed events</p>
  </div>
  <div class="kpi-card">
    <p class="eyebrow">Continuity / upgrade-like</p>
    <p class="kpi">38</p>
    <p class="kpi-label">observed events</p>
  </div>
  <div class="kpi-card">
    <p class="eyebrow">Placeholder / forward-dated</p>
    <p class="kpi">20</p>
    <p class="kpi-label">observed events</p>
  </div>
</div>

<div class="callout">
  <p><strong>Safe wording:</strong> selective modernization with capital-intensive evidence, not proof that replacement is the only pathway.</p>
</div>

---

<!-- _class: appendix dense -->

# Appendix D: File Map

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
    <p class="eyebrow">Checklist</p>
    <p class="big">paper/slides/paper-zoom-presentation-checklist.md</p>
    <p class="small">Run sheet for a simple, direct presentation.</p>
  </div>
  <div class="card">
    <p class="eyebrow">Build command</p>
    <p class="big">npm run slides:paper:pdf</p>
    <p class="small">Regenerates the shareable PDF.</p>
  </div>
</div>
