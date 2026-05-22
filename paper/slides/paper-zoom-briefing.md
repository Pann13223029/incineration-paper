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
  <span class="pill">Supervisor-ready narrative</span>
</div>

<div class="meta">
  Pann Phetra<br/>
  Paper briefing for discussion and feedback
</div>

<!--
Script cue: This is a focused paper explanation: problem, design, evidence, contribution, and limits.
-->

---

# What the Paper Argues

<div class="card single-card center">
  <p class="eyebrow">Core claim</p>
  <p class="reader-line">Japan's waste-incineration transition should be read as a two-part modernization problem, not as one average fleet curve.</p>
</div>

<div class="three-col">
  <div class="card">
    <p class="eyebrow">Contribution 1</p>
    <p class="big">Separates entry from performance.</p>
    <p class="small">Non-generators and generators are analyzed as different empirical margins.</p>
  </div>
  <div class="card">
    <p class="eyebrow">Contribution 2</p>
    <p class="big">Uses one national facility panel.</p>
    <p class="small">The paper links FY2005-FY2024 administrative data across the same fleet.</p>
  </div>
  <div class="card">
    <p class="eyebrow">Contribution 3</p>
    <p class="big">Keeps claims calibrated.</p>
    <p class="small">The interpretation is diagnostic and descriptive, not a causal policy-effect claim.</p>
  </div>
</div>
<!--
Script cue: Put the contribution early so the supervisor knows what to evaluate.
-->

---

# Why This Matters

<div class="diagram-card">
  <div class="flow">
    <div class="flow-step">
      <p class="step-number">1</p>
      <p class="mini-title">Waste is burned</p>
      <p class="mini-text">Japan relies heavily on incineration for municipal waste treatment.</p>
    </div>
    <div class="flow-arrow">&rarr;</div>
    <div class="flow-step">
      <p class="step-number">2</p>
      <p class="mini-title">Heat is produced</p>
      <p class="mini-text">Thermal treatment creates heat regardless of whether electricity is recovered.</p>
    </div>
    <div class="flow-arrow">&rarr;</div>
    <div class="flow-step">
      <p class="step-number">3</p>
      <p class="mini-title">Electricity may be generated</p>
      <p class="mini-text">In FY2024, only 41.1% of panel facilities are flagged as power-generating.</p>
    </div>
  </div>
</div>

<div class="callout">
  <p>The paper asks where useful electricity recovery appears inside the existing fleet, not whether incineration itself is always good or bad.</p>
</div>

<!--
Script cue: Ground the paper in plain physical intuition before methods.
-->

---

# What to Listen For

<div class="two-col">
  <div class="card">
    <p class="eyebrow">Main diagnostic question</p>
    <p class="big">Where is the modernization bottleneck?</p>
    <p class="small">Is the problem mainly entry into generation, performance among generators, or both?</p>
  </div>
  <div class="card">
    <p class="eyebrow">Important scope boundary</p>
    <p class="big">This is not a causal policy evaluation.</p>
    <p class="small">The paper estimates structured patterns within linked samples and states what those patterns can and cannot prove.</p>
  </div>
</div>

<div class="callout">
  <p>Supervisor lens: judge whether the two-margin design makes the claim clearer and more defensible than a one-average fleet story.</p>
</div>

<!--
Script cue: This slide preempts the main methodological concern without sounding defensive.
-->

---

# Research Questions

<div class="three-col">
  <div class="card">
    <p class="eyebrow">RQ1: Adoption</p>
    <p class="big">Who enters electricity generation?</p>
    <p class="small">Facilities first observed without generation are followed until first reported generation.</p>
  </div>
  <div class="card">
    <p class="eyebrow">RQ2: Efficiency</p>
    <p class="big">Who performs better after entry?</p>
    <p class="small">Identifiable operating generators are compared by electricity recovered per tonne.</p>
  </div>
  <div class="card">
    <p class="eyebrow">RQ3: Synthesis</p>
    <p class="big">Do both margins tell one story?</p>
    <p class="small">The paper asks whether they reveal different modernization bottlenecks.</p>
  </div>
</div>

<!--
Script cue: The three questions map directly to the results section.
-->

---

# Data Architecture

<div class="kpi-grid two">
  <div class="kpi-card">
    <p class="eyebrow">Source panel</p>
    <p class="kpi">23,599</p>
    <p class="kpi-label">facility-year observations</p>
    <p class="kpi-note">FY2005-FY2024, 2,948 identifiable facilities, 47 prefectures.</p>
  </div>
  <div class="kpi-card">
    <p class="eyebrow">Adoption frame</p>
    <p class="kpi">13,770</p>
    <p class="kpi-label">at-risk facility-years</p>
    <p class="kpi-note">2,035 facilities first observed without generation; 141 observed first-adoption events.</p>
  </div>
  <div class="kpi-card">
    <p class="eyebrow">Hazard model frame</p>
    <p class="kpi">11,717</p>
    <p class="kpi-label">lagged model rows</p>
    <p class="kpi-note">1,915 facilities and 140 retained first-adoption events.</p>
  </div>
  <div class="kpi-card">
    <p class="eyebrow">Generator frame</p>
    <p class="kpi">5,683</p>
    <p class="kpi-label">canonical generator rows</p>
    <p class="kpi-note">1,016 identifiable operating generators used for conditional-efficiency models.</p>
  </div>
</div>

<!--
Script cue: Emphasize that two samples are necessary because the questions differ.
-->

---

# Two-Margin Design

<div class="diagram-card">
  <div class="flow">
    <div class="flow-step">
      <p class="step-number">1</p>
      <p class="mini-title">Full facility panel</p>
      <p class="mini-text">Start from the national administrative facility panel.</p>
    </div>
    <div class="flow-arrow">&rarr;</div>
    <div class="flow-step">
      <p class="step-number">2</p>
      <p class="mini-title">Split by question</p>
      <p class="mini-text">Non-generators reveal entry; generators reveal conditional performance.</p>
    </div>
    <div class="flow-arrow">&rarr;</div>
    <div class="flow-step">
      <p class="step-number">3</p>
      <p class="mini-title">Read together</p>
      <p class="mini-text">The fleet shows selective entry and bounded generator performance.</p>
    </div>
  </div>
</div>

<div class="callout">
  <p>The samples are linked but not identical because they answer different questions.</p>
</div>

<!--
Script cue: This is the design logic in one slide.
-->

---

# How Each Margin Is Estimated

<div class="two-col">
  <div class="card">
    <p class="eyebrow">Extensive margin</p>
    <p class="big">Transition into generation</p>
    <p class="small">Lagged discrete-time hazard among facilities still at risk of first reported generation.</p>
  </div>
  <div class="card">
    <p class="eyebrow">Intensive margin</p>
    <p class="big">Efficiency among generators</p>
    <p class="small">Descriptive panel models for electricity generated per tonne processed.</p>
  </div>
</div>

<div class="callout">
  <p><strong>Boundary:</strong> diagnostic fleet decomposition, not a single causal pathway model.</p>
</div>

<!--
Script cue: Keep the method explanation plain and short.
-->

---

# Result 1: Adoption Is Selective

<div class="figure-card figure-wide">
  <img src="../figures/figure2_selective_transition.png" alt="Observed adoption event rates by age and capacity" />
</div>

<div class="callout">
  <p>Observed first adoption is concentrated among younger and larger facilities, not spread evenly across the fleet.</p>
</div>

<!--
Script cue: Let the figure do the work, then state the result in one sentence.
-->

---

# Adoption Result in Numbers

<div class="two-col">
  <div class="kpi-card">
    <p class="eyebrow">Age pattern</p>
    <p class="kpi">102 / 141</p>
    <p class="kpi-label">first-adoption events are from age 0-10 facilities</p>
    <p class="kpi-note">The three older age bands together account for only 39 events.</p>
  </div>
  <div class="kpi-card">
    <p class="eyebrow">Capacity pattern</p>
    <p class="kpi">99 / 141</p>
    <p class="kpi-label">first-adoption events are in the largest capacity quartile</p>
    <p class="kpi-note">The smallest capacity quartile records only one event.</p>
  </div>
</div>

<div class="callout">
  <p>The hazard model confirms the pattern: older age bands are lower by about 1.13-1.76 pp; capacity is positive at about +0.50 pp per 100 t/day.</p>
</div>

<!--
Script cue: Explain that pp means percentage points in annual transition probability.
-->

---

# Pathway Audit

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
  <p><strong>Defensible wording:</strong> selective modernization with capital-intensive evidence, not proof that replacement is the only pathway.</p>
</div>

<!--
Script cue: The audit supports interpretation but does not identify one mechanism.
-->

---

# Result 2: Generator Performance

<div class="figure-card figure-wide">
  <img src="../figures/figure3_efficiency_structure.png" alt="Generator efficiency structure by age and variance ratio" />
</div>

<div class="callout">
  <p>Among generators, efficiency declines across age groups and most variation is between facilities rather than within the same facility over time.</p>
</div>

<!--
Script cue: Avoid saying impossible to improve; say structured and bounded.
-->

---

# Generator Drivers

<div class="three-col">
  <div class="card">
    <p class="eyebrow">Age</p>
    <p class="big">Older plants tend to perform worse.</p>
    <p class="small">Age likely bundles durable design, equipment, and institutional history.</p>
  </div>
  <div class="card">
    <p class="eyebrow">Scale</p>
    <p class="big">Larger plants tend to perform better.</p>
    <p class="small">Scale can support steadier operation and stronger energy recovery.</p>
  </div>
  <div class="card">
    <p class="eyebrow">Utilization</p>
    <p class="big">Better-loaded plants perform better.</p>
    <p class="small">Operations matter, but do not erase large cross-facility gaps.</p>
  </div>
</div>

<!--
Script cue: This is the non-specialist interpretation of the regression table.
-->

---

# Generator Result Boundary

<div class="card single-card center">
  <p class="eyebrow">What this means</p>
  <p class="reader-line">The generator result is not "nothing can improve."</p>
</div>

<div class="callout">
  <p>It means improvement appears bounded by persistent facility differences. Utilization matters, but the largest pattern is still the cross-facility hierarchy.</p>
</div>

<!--
Script cue: This protects the argument from sounding fatalistic.
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
    <div class="flow-arrow">&rarr;</div>
    <div class="flow-step">
      <p class="step-number">B</p>
      <p class="mini-title">Generating segment</p>
      <p class="mini-text">The second problem is how much electricity generators recover per tonne.</p>
    </div>
    <div class="flow-arrow">&rarr;</div>
    <div class="flow-step">
      <p class="step-number">C</p>
      <p class="mini-title">Planning implication</p>
      <p class="mini-text">Fleet triage and generator optimization should be treated as separate tasks.</p>
    </div>
  </div>
</div>

<!--
Script cue: Tie the two empirical results back to the claim.
-->

---

# Planning Implication

<div class="two-col">
  <div class="card">
    <p class="eyebrow">If a plant does not generate</p>
    <p class="big">Ask renewal, consolidation, or entry questions.</p>
    <p class="small">The issue is whether power generation is a plausible asset-management path.</p>
  </div>
  <div class="card">
    <p class="eyebrow">If a plant already generates</p>
    <p class="big">Ask utilization, routing, and upgrade questions.</p>
    <p class="small">The issue is how far the plant can move within its performance envelope.</p>
  </div>
</div>

<!--
Script cue: Keep the implication practical and non-prescriptive.
-->

---

# Why This Can Be a Paper

<div class="three-col">
  <div class="card">
    <p class="eyebrow">Article contribution</p>
    <p class="big">A linked two-margin design.</p>
    <p class="small">The paper does not reduce transition to generator performance alone.</p>
  </div>
  <div class="card">
    <p class="eyebrow">Evidence contribution</p>
    <p class="big">A clear empirical blind spot.</p>
    <p class="small">Aggregate fleet views hide selective entry and persistent generator hierarchy.</p>
  </div>
  <div class="card">
    <p class="eyebrow">Writing contribution</p>
    <p class="big">A narrower defensible claim.</p>
    <p class="small">The paper avoids overstating causality, mechanism, or climate accounting.</p>
  </div>
</div>

<!--
Script cue: This is the publishability pitch in supervisor language.
-->

---

# What the Paper Does Not Claim

<div class="two-col">
  <div class="claim-card boundary">
    <p class="eyebrow">Boundaries</p>
    <ul class="simple-list">
      <li>No strict causal effect of age, scale, or policy.</li>
      <li>No proof that replacement is the only pathway.</li>
      <li>No complete lifecycle climate accounting.</li>
      <li>No claim that the generator frame is a full census.</li>
    </ul>
  </div>
  <div class="claim-card good">
    <p class="eyebrow">Defended claim</p>
    <p class="big">The paper is a diagnostic fleet decomposition.</p>
    <p class="small">It shows where the bottleneck appears: selective entry into generation and bounded performance among operating generators.</p>
  </div>
</div>

<!--
Script cue: Make limits sound like research discipline, not weakness.
-->

---

# Likely Supervisor Questions

<div class="stack">
  <div class="q-card">
    <p><strong>Q: Is this causal?</strong> No. It is a structured diagnostic analysis with explicit sample limits and robustness checks.</p>
  </div>
  <div class="q-card">
    <p><strong>Q: Why not one model for the whole fleet?</strong> One model would mix entry with performance.</p>
  </div>
  <div class="q-card">
    <p><strong>Q: Does this mean old plants cannot improve?</strong> No. It means broad late-life catch-up does not dominate the observed data.</p>
  </div>
  <div class="q-card">
    <p><strong>Q: What feedback is most useful?</strong> Whether the two-margin claim is clear, defensible, and worth developing into the paper's main pitch.</p>
  </div>
</div>

<!--
Script cue: End the main body ready for discussion.
-->

---

<!-- _class: close -->

# Closing Takeaway

<p class="subtitle">The paper argues that Japan's incineration fleet should be read as a two-part modernization problem, not as one average transition curve.</p>

<div class="close-line">
  <p>First ask which facilities enter energy recovery. Then ask how well generators perform after entry.</p>
</div>

<!--
Script cue: Stop here unless the listener asks for appendix details.
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
