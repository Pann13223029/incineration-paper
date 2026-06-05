---
marp: true
paginate: true
theme: paper-zoom
size: 16:9
title: Critical Briefing on the Waste-Incineration Paper
description: Expanded paper-only Zoom briefing deck for the Japan waste-incineration facility-panel study.
---

<!-- _class: hero -->

# Explaining the Paper Clearly

## Why Japan's incineration energy-recovery pattern matters

<div class="pill-row">
  <span class="pill">15-18 minute route</span>
  <span class="pill">Paper only</span>
  <span class="pill">Methods + limits included</span>
</div>

<div class="meta">
  Pann Phetra<br/>
  Paper briefing for discussion and feedback
</div>

<!--
Script cue: Set expectation. This version is still simple, but more critical: data, method, robustness, limits, and future direction are included in the live route.
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
      <p class="mini-title">Heat already exists</p>
      <p class="mini-text">Incineration creates heat whether or not electricity is recovered.</p>
    </div>
    <div class="flow-arrow">&rarr;</div>
    <div class="flow-step">
      <p class="step-number">3</p>
      <p class="mini-title">Not all heat becomes electricity</p>
      <p class="mini-text">In FY2024, only 41.1% of panel facilities are flagged as power-generating.</p>
    </div>
  </div>
</div>

<div class="callout">
  <p>This matters because the same waste-treatment process can either recover useful power or miss that energy-recovery opportunity.</p>
</div>

<!--
Script cue: Start from practical stakes before methodology.
-->

---

# The Claim Is Not the Obvious Part

<div class="card single-card center">
  <p class="eyebrow">Skeptical framing</p>
  <p class="reader-line">The paper is not asking the listener to be surprised that young and large plants have advantages.</p>
</div>

<div class="callout">
  <p>The stronger question is whether modernization spreads broadly through the lagging fleet, or mostly appears where conditions are already favorable.</p>
</div>

<!--
Script cue: Defuse the "common sense" objection early.
-->

---

# Main Idea in Plain Words

<div class="card single-card center">
  <p class="eyebrow">Plain claim</p>
  <p class="reader-line">One fleet average hides two different questions.</p>
</div>

<div class="two-col">
  <div class="card">
    <p class="eyebrow">Question 1</p>
    <p class="big">Which plants start generating electricity?</p>
    <p class="small">This is the entry question.</p>
  </div>
  <div class="card">
    <p class="eyebrow">Question 2</p>
    <p class="big">Among generators, who produces more electricity per tonne?</p>
    <p class="small">This is the performance question.</p>
  </div>
</div>

<!--
Script cue: Define the terms before using them.
-->

---

# Data Sources: What Is Observed

<table class="source-table">
  <thead>
    <tr>
      <th>Source layer</th>
      <th>What it contributes</th>
      <th>How the paper uses it</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>MOE General Waste Treatment Survey</td>
      <td>National municipal waste-treatment facility records, FY2005-FY2024</td>
      <td>Base facility-year panel and power-generation outcome</td>
    </tr>
    <tr>
      <td>Facility identifiers and location</td>
      <td>Official code, facility name, prefecture, fiscal year</td>
      <td>Panel linkage, prefecture controls, clustered uncertainty, duplicate-code checks</td>
    </tr>
    <tr>
      <td>Facility operating attributes</td>
      <td>Power-generation flag/output, throughput, design capacity, start year/age</td>
      <td>Entry risk set and generator-output comparison</td>
    </tr>
    <tr>
      <td>Context and plausibility controls</td>
      <td>Heating value and grid-emission context</td>
      <td>Comparability checks, not the central contribution</td>
    </tr>
  </tbody>
</table>

<div class="callout">
  <p>This is broad administrative panel evidence. It observes facility reporting patterns well, but not internal retrofit contracts, municipal bargaining, or full lifecycle emissions.</p>
</div>

<!--
Script cue: Say what the dataset can and cannot observe.
-->

---

# From Data to Analysis Frames

<div class="pipeline">
  <div class="pipe-card">
    <p class="eyebrow">Starting panel</p>
    <p class="kpi">23,599</p>
    <p class="kpi-label">facility-year rows</p>
    <p class="kpi-note">Full analytical starting point.</p>
  </div>
  <div class="pipe-arrow">&rarr;</div>
  <div class="pipe-card">
    <p class="eyebrow">Coded fleet</p>
    <p class="kpi">2,948</p>
    <p class="kpi-label">identifiable facilities</p>
    <p class="kpi-note">Official identifiers support panel linkage.</p>
  </div>
  <div class="pipe-arrow">&rarr;</div>
  <div class="pipe-card">
    <p class="eyebrow">Entry frame</p>
    <p class="kpi">13,770</p>
    <p class="kpi-label">at-risk facility-years</p>
    <p class="kpi-note">2,035 initial non-generators; 141 first-entry events.</p>
  </div>
  <div class="pipe-arrow">&rarr;</div>
  <div class="pipe-card">
    <p class="eyebrow">Performance frame</p>
    <p class="kpi">5,683</p>
    <p class="kpi-label">generator observations</p>
    <p class="kpi-note">1,016 operating generators with covariates.</p>
  </div>
</div>

<div class="callout">
  <p>The split is methodological, not cosmetic: the paper first asks who crosses into generation, then asks how well generators perform after crossing.</p>
</div>

<!--
Script cue: The sample split is a substantive choice, not just a data-cleaning detail.
-->

---

# Two Samples Because There Are Two Questions

<table class="source-table">
  <thead>
    <tr>
      <th>Question</th>
      <th>Sample frame</th>
      <th>Outcome</th>
      <th>What it tests</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Who starts generating?</td>
      <td>Facilities first observed without power generation</td>
      <td>First report of electricity generation</td>
      <td>Whether energy recovery diffuses into the lagging fleet</td>
    </tr>
    <tr>
      <td>Who generates well?</td>
      <td>Identifiable operating generators</td>
      <td>MWh generated per tonne processed</td>
      <td>Whether performance converges after entry</td>
    </tr>
  </tbody>
</table>

<div class="callout">
  <p>One model for everything would mix the gate into generation with performance after entry, hiding where the bottleneck actually sits.</p>
</div>

<!--
Script cue: This slide prevents the audience from asking why there is not one model for everything.
-->

---

# Method 1: Who Had a Chance to Start?

<div class="method-grid">
  <div class="formula-card">
    <p class="eyebrow">Plain model</p>
    <p class="formula">Pr(first generation in year t) = f(prior age, prior capacity, year, prefecture)</p>
  </div>
  <div class="card">
    <p class="eyebrow">Risk set</p>
    <p class="big">Only initial non-generators are candidates.</p>
    <p class="small">Facilities already generating in their first observed year are left-censored for first-entry analysis.</p>
  </div>
  <div class="card">
    <p class="eyebrow">Timing discipline</p>
    <p class="big">Predictors are lagged.</p>
    <p class="small">Age and capacity are measured before first entry, not after the event.</p>
  </div>
  <div class="card">
    <p class="eyebrow">Comparability</p>
    <p class="big">Year and prefecture controls.</p>
    <p class="small">Uncertainty is clustered by facility, and alternative hazard forms are checked.</p>
  </div>
</div>

<div class="callout">
  <p>The model asks: among facilities still outside power generation, who first reports generation in the next observed year?</p>
</div>

<!--
Script cue: This is where the method becomes more than common sense.
-->

---

# Method 2: How Generator Output Is Compared

<div class="method-grid">
  <div class="formula-card">
    <p class="eyebrow">Outcome model</p>
    <p class="formula">log(MWh per tonne) = age + capacity + utilization + heating value + grid context + year structure</p>
  </div>
  <div class="card">
    <p class="eyebrow">Outcome</p>
    <p class="big">Electricity recovered per tonne processed.</p>
    <p class="small">This measures output intensity, not just the existence of a generator.</p>
  </div>
  <div class="card">
    <p class="eyebrow">Model family</p>
    <p class="big">Pooled OLS, year FE, RE, year FE + RE.</p>
    <p class="small">The paper checks whether the sign pattern survives alternative structures.</p>
  </div>
  <div class="card">
    <p class="eyebrow">Interpretation</p>
    <p class="big">This is diagnostic, not causal.</p>
    <p class="small">It tests whether generators converge enough to erase inherited facility differences.</p>
  </div>
</div>

<div class="callout">
  <p>The critical question after entry is whether generator performance converges enough to erase inherited facility differences.</p>
</div>

<!--
Script cue: Move the discussion from "old plants are worse" to "do generators converge after entry?"
-->

---

# Result 1: Starting Generation Is Selective

<div class="figure-card figure-wide">
  <img src="../figures/figure2_selective_transition.png" alt="Observed adoption event rates by age and capacity" />
</div>

<div class="callout">
  <p>Facilities that first start generating electricity are mostly young and large: 102/141 events are from age 0-10 facilities, and 99/141 are in the largest capacity quartile.</p>
</div>

<!--
Script cue: Say the two numbers slowly, but do not stop at counts.
-->

---

# What Result 1 Rules Out

<div class="rate-panels">
  <div class="rate-panel">
    <p class="eyebrow">Annual first-entry rate by age</p>
    <div class="bar-row">
      <span class="bar-label">0-10 yrs</span>
      <span class="bar-track"><span class="bar-fill" style="width: 100%;"></span></span>
      <span class="bar-value">5.94%</span>
    </div>
    <div class="bar-row">
      <span class="bar-label">10-20 yrs</span>
      <span class="bar-track"><span class="bar-fill muted-fill" style="width: 6%;"></span></span>
      <span class="bar-value">0.35%</span>
    </div>
    <div class="bar-row">
      <span class="bar-label">20-30 yrs</span>
      <span class="bar-track"><span class="bar-fill muted-fill" style="width: 6%;"></span></span>
      <span class="bar-value">0.34%</span>
    </div>
    <div class="bar-row">
      <span class="bar-label">30+ yrs</span>
      <span class="bar-track"><span class="bar-fill muted-fill" style="width: 5%;"></span></span>
      <span class="bar-value">0.27%</span>
    </div>
  </div>
  <div class="rate-panel">
    <p class="eyebrow">Annual first-entry rate by capacity</p>
    <div class="bar-row">
      <span class="bar-label">Q1 small</span>
      <span class="bar-track"><span class="bar-fill muted-fill" style="width: 1%;"></span></span>
      <span class="bar-value">0.03%</span>
    </div>
    <div class="bar-row">
      <span class="bar-label">Q2</span>
      <span class="bar-track"><span class="bar-fill muted-fill" style="width: 3%;"></span></span>
      <span class="bar-value">0.08%</span>
    </div>
    <div class="bar-row">
      <span class="bar-label">Q3</span>
      <span class="bar-track"><span class="bar-fill" style="width: 37%;"></span></span>
      <span class="bar-value">1.16%</span>
    </div>
    <div class="bar-row">
      <span class="bar-label">Q4 large</span>
      <span class="bar-track"><span class="bar-fill" style="width: 100%;"></span></span>
      <span class="bar-value">3.11%</span>
    </div>
  </div>
</div>

<div class="callout">
  <p>This rules out a simple broad-catch-up story: the smallest capacity quartile records only one first-entry event, while the largest quartile records 99.</p>
</div>

<!--
Script cue: This answers the obviousness objection.
-->

---

# What Kind of Entry Was This?

<div class="three-col">
  <div class="kpi-card">
    <p class="eyebrow">Reset / rebuild-like</p>
    <p class="kpi">82</p>
    <p class="kpi-label">observed events</p>
    <p class="kpi-note">Capital-side modernization is empirically present.</p>
  </div>
  <div class="kpi-card">
    <p class="eyebrow">Continuity / upgrade-like</p>
    <p class="kpi">38</p>
    <p class="kpi-label">observed events</p>
    <p class="kpi-note">Some cases remain consistent with in-place upgrade.</p>
  </div>
  <div class="kpi-card">
    <p class="eyebrow">Placeholder / forward-dated</p>
    <p class="kpi">20</p>
    <p class="kpi-label">observed events</p>
    <p class="kpi-note">Some entries should not be forced into a stronger mechanism claim.</p>
  </div>
</div>

<div class="callout">
  <p>The audit prevents overclaiming: the data support selective modernization, not proof that replacement is the only pathway.</p>
</div>

<!--
Script cue: This slide shows critical restraint.
-->

---

# Result 2: Entry Is Not the Finish Line

<div class="figure-card figure-wide">
  <img src="../figures/figure3_efficiency_structure.png" alt="Generator efficiency structure by age and variance ratio" />
</div>

<div class="callout">
  <p>Among plants that already generate, older facilities recover less electricity per tonne. Existing generators remain uneven after entry.</p>
</div>

<!--
Script cue: Do not imply older plants cannot improve; say the observed hierarchy persists.
-->

---

# Generator Convergence Is Limited

<div class="three-col">
  <div class="kpi-card">
    <p class="eyebrow">Full sample</p>
    <p class="kpi">0.1499</p>
    <p class="kpi-label">within-to-total variance ratio</p>
    <p class="kpi-note">Most generator-output variation is between facilities.</p>
  </div>
  <div class="kpi-card">
    <p class="eyebrow">Pre-2011</p>
    <p class="kpi">0.1795</p>
    <p class="kpi-label">within-to-total ratio</p>
    <p class="kpi-note">Within-facility movement is limited even before the post-2011 period.</p>
  </div>
  <div class="kpi-card">
    <p class="eyebrow">Post-2011</p>
    <p class="kpi">0.0956</p>
    <p class="kpi-label">within-to-total ratio</p>
    <p class="kpi-note">After 2011, most variation remains cross-facility hierarchy.</p>
  </div>
</div>

<div class="callout">
  <p>The critical point is not that older generators are worse; it is that operating generators do not appear to converge enough to erase inherited gaps.</p>
</div>

<!--
Script cue: This makes result 2 more critical and less obvious.
-->

---

# Robustness: What I Tried to Break

<table class="source-table">
  <thead>
    <tr>
      <th>Stress test</th>
      <th>Why it matters</th>
      <th>What survives</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Composite facility-ID sensitivity</td>
      <td>Checks whether duplicate official codes drive the adoption result</td>
      <td>Age penalties and positive capacity effect remain stable</td>
    </tr>
    <tr>
      <td>Alternative adoption models</td>
      <td>Checks whether logit hazard choice creates the result</td>
      <td>Complementary log-log and LPM keep the same sign pattern</td>
    </tr>
    <tr>
      <td>Generator-output stress tests</td>
      <td>Checks period, scale, and outcome-coding sensitivity</td>
      <td>Age stays negative; capacity and utilization stay positive</td>
    </tr>
    <tr>
      <td>Heating-value plausibility restrictions</td>
      <td>Checks whether noisy heat-value data drive model patterns</td>
      <td>Main age, scale, and utilization coefficients remain stable</td>
    </tr>
  </tbody>
</table>

<div class="callout">
  <p>These checks do not make the estimates causal. They show the diagnostic pattern is not a fragile artifact of one coding choice.</p>
</div>

<!--
Script cue: Use this to show the paper is more than descriptive common sense.
-->

---

# Data Limitations Are Real

<div class="three-col">
  <div class="kpi-card">
    <p class="eyebrow">Duplicate-code concern</p>
    <p class="kpi">39</p>
    <p class="kpi-label">official codes affected</p>
    <p class="kpi-note">444 source rows use codes that duplicate within at least one fiscal year.</p>
  </div>
  <div class="kpi-card">
    <p class="eyebrow">Missing-code concern</p>
    <p class="kpi">907</p>
    <p class="kpi-label">operating-generator rows</p>
    <p class="kpi-note">Rows missing official codes are excluded from the canonical regression frame.</p>
  </div>
  <div class="kpi-card">
    <p class="eyebrow">Plausibility concern</p>
    <p class="kpi">569</p>
    <p class="kpi-label">heating-value rows</p>
    <p class="kpi-note">Rows outside 3-25 MJ/kg are checked through sensitivity restrictions.</p>
  </div>
</div>

<div class="callout">
  <p>The paper discloses these limits and stress-tests them. It maps bottlenecks; it does not claim a perfect engineering census or a fully identified causal mechanism.</p>
</div>

<!--
Script cue: Make limits sound like research discipline, not weakness.
-->

---

# Decision Logic

<div class="diagram-card">
  <div class="flow">
    <div class="flow-step">
      <p class="step-number">A</p>
      <p class="mini-title">Non-generators</p>
      <p class="mini-text">Can this plant start recovering electricity?</p>
    </div>
    <div class="flow-arrow">&rarr;</div>
    <div class="flow-step">
      <p class="step-number">B</p>
      <p class="mini-title">Generators</p>
      <p class="mini-text">Can this plant recover more electricity from the same waste?</p>
    </div>
    <div class="flow-arrow">&rarr;</div>
    <div class="flow-step">
      <p class="step-number">C</p>
      <p class="mini-title">Planning</p>
      <p class="mini-text">Use different decisions for different bottlenecks.</p>
    </div>
  </div>
</div>

<div class="callout">
  <p>This matters because renewal, starting electricity generation, and generator optimization are not the same task.</p>
</div>

<!--
Script cue: This is the practical payoff.
-->

---

# Weak Claim vs Defensible Claim

<div class="two-col">
  <div class="claim-card boundary">
    <p class="eyebrow">Weak claim</p>
    <p class="big">Newer and larger plants generate more.</p>
    <p class="small">This is plausible but not enough for a paper by itself.</p>
  </div>
  <div class="claim-card good">
    <p class="eyebrow">Defensible claim</p>
    <p class="big">The fleet has two bottlenecks.</p>
    <p class="small">Starting generation is selective, and generator output remains uneven after entry.</p>
  </div>
</div>

<div class="callout">
  <p>The paper's contribution is mapping where the bottleneck sits, not pretending that age and scale are surprising.</p>
</div>

<!--
Script cue: This is the publishability pitch.
-->

---

# Future Work: Mechanisms Not Yet Tested

<div class="three-col">
  <div class="card">
    <p class="eyebrow">Capital renewal</p>
    <p class="big">Link entry to investment and rebuild histories.</p>
    <p class="small">This would test whether selective entry is mainly capital replacement or retrofit.</p>
  </div>
  <div class="card">
    <p class="eyebrow">Governance and routing</p>
    <p class="big">Link facilities to municipal decisions.</p>
    <p class="small">This could explain why some plants start generation or improve output.</p>
  </div>
  <div class="card">
    <p class="eyebrow">Climate and comparison</p>
    <p class="big">Add lifecycle or cross-fleet evidence.</p>
    <p class="small">This would move from energy-recovery diagnosis toward climate or international comparison.</p>
  </div>
</div>

<div class="callout">
  <p>These extensions have not started yet. They are the next step from diagnostic mapping to mechanism testing.</p>
</div>

<!--
Script cue: Be honest that future work is proposed, not completed.
-->

---

<!-- _class: close -->

# Feedback Ask

<p class="subtitle">The paper's message is: first ask who starts generating electricity, then ask who generates well after starting.</p>

<div class="close-line">
  <p>Is the two-question design strong enough as the paper's main contribution? Which limitation or future-work path should be prioritized?</p>
</div>

<!--
Script cue: Ask for targeted feedback, then stop.
-->
