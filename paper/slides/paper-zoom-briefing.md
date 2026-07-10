---
marp: true
paginate: true
theme: paper-zoom
size: 16:9
title: Where Energy Recovery Stalls
description: Audience-facing Zoom briefing deck for the Japan waste-incineration facility-panel study.
---

<!-- _class: hero -->

# Where Energy Recovery Stalls

## Two margins and one crucial risk-set distinction

<div class="hero-title-card">
  <p class="hero-title-label">Paper title</p>
  <p class="hero-paper-title">Selective Entry and Structured Electricity-Recovery Performance in Japan's Waste-Incineration Fleet: A Facility-Level Panel Study</p>
</div>

<div class="pill-row">
  <span class="pill">15-18 minute route</span>
  <span class="pill">Data + method</span>
  <span class="pill">Results + limits</span>
</div>

<div class="meta">
  Pann Phetra<br/>
  Paper discussion briefing
</div>

<!--
Script cue: Set expectation. This is an audience-facing route: problem, method, results, limits, and feedback questions.
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
      <p class="mini-text">In FY2024, 415 of 991 facilities (41.9%) generated electricity in the official summary.</p>
    </div>
  </div>
</div>

<div class="callout">
  <p>The same waste-treatment process can either recover useful power or miss that energy-recovery opportunity.</p>
</div>

<!--
Script cue: Start from practical stakes before methodology.
-->

---

# The Real Question

<div class="card single-card center">
  <p class="eyebrow">Expected part</p>
  <p class="reader-line">Scale may matter, but the age story depends on which facilities count as candidates.</p>
</div>

<div class="callout">
  <p>The paper tests broad asset entry, conversion of active plants, and performance after entry as distinct outcomes.</p>
</div>

<!--
Script cue: Defuse the "common sense" objection early.
-->

---

# Two Questions, One Fleet

<div class="card single-card center">
  <p class="eyebrow">Core logic</p>
  <p class="reader-line">One fleet average hides two different bottlenecks.</p>
</div>

<div class="two-col">
  <div class="card">
    <p class="eyebrow">Question 1</p>
    <p class="big">Which plants start generating electricity?</p>
    <p class="small">This is the entry bottleneck.</p>
  </div>
  <div class="card">
    <p class="eyebrow">Question 2</p>
    <p class="big">Among generators, who produces more electricity per tonne?</p>
    <p class="small">This is the performance bottleneck.</p>
  </div>
</div>

<div class="term-row">
  <div class="term-chip"><strong>Entry</strong> = a facility first reports positive installed generation capacity.</div>
  <div class="term-chip"><strong>MWh/t</strong> = electricity produced per tonne of waste processed.</div>
  <div class="term-chip"><strong>Bottleneck</strong> = the step where improvement is most constrained.</div>
</div>

<!--
Script cue: Define the terms before using them.
-->

---

# What the Data Can See

<table class="source-table">
  <thead>
    <tr>
      <th>Observed layer</th>
      <th>Observed fields</th>
      <th>Analytical role</th>
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
      <td>Installed capacity/output, throughput, design capacity, start year/age, furnace and operation type</td>
      <td>Entry risk set and generator-output comparison</td>
    </tr>
    <tr>
      <td>Context and plausibility controls</td>
      <td>Heating value and reported generation efficiency</td>
      <td>Comparability and engineering-oriented validation</td>
    </tr>
  </tbody>
</table>

<div class="callout">
  <p>The panel observes facility reporting patterns well. It does not directly observe internal retrofit contracts, municipal bargaining, or full lifecycle emissions.</p>
</div>

<!--
Script cue: Say what the dataset can and cannot observe.
-->

---

# How the Panel Becomes Two Frames

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
    <p class="kpi-note">Broad universe: 141 events. Exact model: 98. Active conversion: 58.</p>
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
  <p>The design distinguishes broad asset entry, conversion among active non-generators, and performance after entry.</p>
</div>

<!--
Script cue: The sample split is a substantive choice, not just a data-cleaning detail.
-->

---

# Why Two Samples Are Needed

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
      <td>Who first reports installed capacity?</td>
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

# Method: First Entry Into Generation

<div class="method-grid">
  <div class="formula-card">
    <p class="eyebrow">Plain model</p>
    <p class="formula">Pr(first installed capacity in year t) = f(prior age, prior capacity, year, elapsed time at risk)</p>
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
    <p class="eyebrow">Two estimands</p>
    <p class="big">Broad assets and active plants.</p>
    <p class="small">The active model requires positive throughput in the prior fiscal year.</p>
  </div>
</div>

<div class="callout">
  <p>Plain question: among facilities still outside power generation, who first reports generation in the next fiscal year?</p>
</div>

<!--
Script cue: This is where the method becomes more than common sense.
-->

---

# Method: Output Among Generators

<div class="method-grid">
  <div class="formula-card">
    <p class="eyebrow">Outcome model</p>
    <p class="formula">log(MWh per tonne) = age/vintage + capacity + utilization + heating value + year + technology</p>
  </div>
  <div class="card">
    <p class="eyebrow">Outcome</p>
    <p class="big">Electricity recovered per tonne processed.</p>
    <p class="small">This measures output intensity, not just the existence of a generator.</p>
  </div>
  <div class="card">
    <p class="eyebrow">Primary model</p>
    <p class="big">Year + technology OLS.</p>
    <p class="small">Furnace type, operating mode, facility type, and furnace count are observed controls.</p>
  </div>
  <div class="card">
    <p class="eyebrow">Interpretation</p>
    <p class="big">This is diagnostic, not causal.</p>
    <p class="small">It compares generators within common years without claiming an intervention effect.</p>
  </div>
</div>

<div class="callout">
  <p>The coefficient is an age/vintage comparison across facilities, not the causal effect of making one plant older.</p>
</div>

<!--
Script cue: Move the discussion from "old plants are worse" to "do generators converge after entry?"
-->

---

# Result 1: Scale Is Robust; Age Depends on the Frame

<div class="figure-card figure-wide">
  <img src="../figures/figure2_selective_transition.png" alt="Observed adoption event rates by age and capacity" />
</div>

<div class="callout">
  <p>Capacity predicts entry in both frames (+0.45 and +0.44 pp per 100 t/day); age differences shrink among active plants.</p>
</div>

<!--
Script cue: Say the two numbers slowly, but do not stop at counts.
-->

---

# Interpretation: The Risk Set Changes the Story

<div class="three-col">
  <div class="kpi-card">
    <p class="eyebrow">Broad asset entry</p>
    <p class="kpi">98</p>
    <p class="kpi-label">exact-year events</p>
    <p class="kpi-note">Age AMEs: -1.41, -1.45, -0.83 pp.</p>
  </div>
  <div class="kpi-card">
    <p class="eyebrow">Active conversion</p>
    <p class="kpi">58</p>
    <p class="kpi-label">exact-year events</p>
    <p class="kpi-note">Age AMEs attenuate to -0.67, -0.56, -0.29 pp.</p>
  </div>
  <div class="kpi-card">
    <p class="eyebrow">Scale result</p>
    <p class="kpi">+0.45 / +0.44</p>
    <p class="kpi-label">pp per 100 t/day</p>
    <p class="kpi-note">Positive and precisely estimated in both frames.</p>
  </div>
</div>

<div class="callout">
  <p>40 of 98 broad events follow zero or missing prior-year throughput. Commissioning and rebuild pathways materially affect the broad age result.</p>
</div>

<!--
Script cue: This answers the obviousness objection.
-->

---

# Entry Pathways: Modernization, Not One Mechanism

<div class="three-col">
  <div class="kpi-card">
    <p class="eyebrow">Reset / rebuild-like</p>
    <p class="kpi">50</p>
    <p class="kpi-label">observed events</p>
    <p class="kpi-note">Capital-side modernization is empirically present.</p>
  </div>
  <div class="kpi-card">
    <p class="eyebrow">Continuity / upgrade-like</p>
    <p class="kpi">36</p>
    <p class="kpi-label">observed events</p>
    <p class="kpi-note">Some cases remain consistent with in-place upgrade.</p>
  </div>
  <div class="kpi-card">
    <p class="eyebrow">Ambiguous / other</p>
    <p class="kpi">55</p>
    <p class="kpi-label">observed events</p>
    <p class="kpi-note">12 placeholder, 42 non-adjacent, and 1 unresolved event.</p>
  </div>
</div>

<div class="callout">
  <p>The audit bounds possible pathways, but it does not prove that replacement is the only mechanism.</p>
</div>

<!--
Script cue: This slide shows critical restraint.
-->

---

# Result 2: Generation Status Is Not Enough

<div class="figure-card figure-wide">
  <img src="../figures/figure3_efficiency_structure.png" alt="Generator efficiency structure by age and variance ratio" />
</div>

<div class="callout">
  <p>Among generators, output intensity still differs sharply: age 0-10 averages 0.400 MWh/t, while age 30+ averages 0.183 MWh/t.</p>
</div>

<!--
Script cue: Do not imply older plants cannot improve; say the observed hierarchy persists.
-->

---

# Interpretation: Ranks Persist Across Coded Years

<div class="three-col">
  <div class="kpi-card">
    <p class="eyebrow">Full sample</p>
    <p class="kpi">0.1499</p>
    <p class="kpi-label">within-to-total variance ratio</p>
    <p class="kpi-note">Most generator-output variation is between facilities.</p>
  </div>
  <div class="kpi-card">
    <p class="eyebrow">Coded windows</p>
    <p class="kpi">0.1795 &rarr; 0.0956</p>
    <p class="kpi-label">within-to-total ratio</p>
    <p class="kpi-note">FY2005-09 versus FY2013-24.</p>
  </div>
  <div class="kpi-card">
    <p class="eyebrow">Adjacent-year ranks</p>
    <p class="kpi">0.9325</p>
    <p class="kpi-label">pooled correlation</p>
    <p class="kpi-note">4,368 exact pairs across 915 facilities.</p>
  </div>
</div>

<div class="callout">
  <p>FY2010-FY2012 official codes are missing, so the paper uses FY2005-FY2009 and FY2013-FY2024 as coded windows, not a Fukushima treatment design.</p>
</div>

<!--
Script cue: This makes result 2 more critical and less obvious.
-->

---

# Stress Tests: The Pattern Survives

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
      <td>Active-conversion risk set</td>
      <td>Removes zero/missing prior-throughput pathways</td>
      <td>Scale persists; the age gradient attenuates</td>
    </tr>
    <tr>
      <td>Technology-adjusted primary model</td>
      <td>Controls observed furnace and operating configuration</td>
      <td>Age/vintage stays negative; scale and utilization stay positive</td>
    </tr>
    <tr>
      <td>Engineering outcomes + lagged predictors</td>
      <td>Checks outcome definition and same-year simultaneity</td>
      <td>Thermal conversion, reported efficiency, and lagged models agree</td>
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

# Data Limits: Disclosed and Tested

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
  <p>These limits are disclosed and stress-tested. The evidence maps bottlenecks; it does not claim a perfect engineering census or fully identified causal mechanism.</p>
</div>

<!--
Script cue: Make limits sound like research discipline, not weakness.
-->

---

# What Happens After Entry?

<div class="figure-card figure-wide">
  <img src="../figures/figure4_post_entry_trajectories.png" alt="Post-entry electricity-recovery trajectory and within-year generator ranks" />
</div>

<div class="callout">
  <p>Entrants begin near the middle of the same-year generator distribution. Follow-up falls from 125 events at time zero to 71 at time three, so this is descriptive, not an entry effect.</p>
</div>

<!--
Script cue: This is the empirical bridge between entry and later performance.
-->

---

# Contribution: Two Margins, Clear Boundaries

<div class="two-col">
  <div class="claim-card boundary">
    <p class="eyebrow">Weak version</p>
    <p class="big">Newer and larger plants have advantages.</p>
    <p class="small">This is plausible but not enough for a paper by itself.</p>
  </div>
  <div class="claim-card good">
    <p class="eyebrow">Stronger version</p>
    <p class="big">The result has clear boundaries.</p>
    <p class="small">Scale is robust, age depends on the risk set, and entry does not guarantee a frontier position.</p>
  </div>
</div>

<div class="callout">
  <p>Planning should distinguish broad asset entry, active conversion, and generator performance before choosing an intervention.</p>
</div>

<!--
Script cue: This is the publishability pitch.
-->

---

# Next Step: Test Mechanisms

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
  <p>The next research step is moving from diagnostic mapping to mechanism testing.</p>
</div>

<!--
Script cue: Be honest that future work is proposed, not completed.
-->

---

<!-- _class: close -->

# Discussion Questions

<p class="subtitle">Three linked outcomes shape the story: asset entry, active conversion, and generator performance.</p>

<div class="close-line">
  <p>Is the three-outcome framing convincing, and is the broad-versus-active entry distinction clear enough? Which mechanism should future work test first?</p>
</div>

<!--
Script cue: Ask for targeted feedback, then stop.
-->
