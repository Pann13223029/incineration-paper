---
marp: true
paginate: true
theme: paper-zoom
size: 16:9
title: Coverage, Entry, and Engineering Components of Electricity Recovery in Japan's Municipal Waste-Incineration Fleet, FY2005-FY2024
description: Professor-facing Zoom briefing for the current canonical manuscript.
---

<!-- _class: hero -->

# Coverage, Entry, and Engineering Components

<p class="subtitle">Three denominators, sparse first entry, and an exact accounting identity</p>

<div class="hero-title-card">
  <p class="hero-title-label">Paper title</p>
  <p class="hero-paper-title">Coverage, Entry, and Engineering Components of Electricity Recovery in Japan's Municipal Waste-Incineration Fleet, FY2005-FY2024</p>
</div>

<div class="pill-row">
  <span class="pill">Professor briefing</span>
  <span class="pill">18-slide route</span>
  <span class="pill">Descriptive + diagnostic</span>
</div>

<div class="meta">
  Pann Phetra<br/>
  Paper discussion briefing
</div>

<!--
Script cue: State the formal title once, then give the three-part plain-language route.
-->

---

# The Paper Asks Three Different Questions

<div class="three-col">
  <div class="card">
    <p class="eyebrow">RQ1 · Coverage</p>
    <p class="big">How much of the fleet is covered?</p>
    <p class="small">Compare facility records, waste throughput, and processing design capacity.</p>
  </div>
  <div class="card">
    <p class="eyebrow">RQ2 · Entry</p>
    <p class="big">Which non-generators first report installed capacity?</p>
    <p class="small">Use an at-risk history and a sparse-event estimator.</p>
  </div>
  <div class="card">
    <p class="eyebrow">RQ3 · Components</p>
    <p class="big">What produces gross electricity per tonne?</p>
    <p class="small">Separate installed sizing, annual capacity factor, and waste loading.</p>
  </div>
</div>

<div class="callout">
  <p>One fleet average cannot answer all three questions: the denominators, candidate populations, and outcomes differ.</p>
</div>

<!--
Script cue: This is the organizing logic for the entire paper.
-->

---

# Two FY2024 Count Statistics, Not One

<div class="two-col">
  <div class="claim-card boundary">
    <p class="eyebrow">Published national context</p>
    <p class="kpi">415 / 991 = 41.9%</p>
    <p class="kpi-label">official electricity-generating facilities</p>
    <p class="kpi-note">The Ministry's published facility count and denominator.</p>
  </div>
  <div class="claim-card good">
    <p class="eyebrow">Analytical panel</p>
    <p class="kpi">417 / 1,014 = 41.1%</p>
    <p class="kpi-label">retained records with installed capacity</p>
    <p class="kpi-note">The paper's record definition and reconstructed denominator.</p>
  </div>
</div>

<div class="callout">
  <p>The 41.9% official statistic is context; it is not substituted for the paper's 41.1% analytical measure.</p>
</div>

<!--
Script cue: Explain why the numerators and denominators are intentionally distinct.
-->

---

# Facility Counts Understate Waste Coverage

<div class="two-col wide-left">
  <div class="figure-card">
    <img src="../figures/figure1_two_part_framework.png" alt="Facility, throughput, and design-capacity coverage from FY2005 to FY2024" />
  </div>
  <div class="stack">
    <div class="kpi-card">
      <p class="eyebrow">Facility participation</p>
      <p class="kpi">41.1%</p>
      <p class="kpi-note">Retained FY2024 records with installed capacity.</p>
    </div>
    <div class="kpi-card">
      <p class="eyebrow">Throughput coverage</p>
      <p class="kpi">80.1%</p>
      <p class="kpi-note">Recorded tonnes handled by positive-output facilities.</p>
    </div>
    <div class="kpi-card">
      <p class="eyebrow">Design-capacity coverage</p>
      <p class="kpi">70.5%</p>
      <p class="kpi-note">Processing capacity at installed-capacity facilities.</p>
    </div>
  </div>
</div>

<!--
Script cue: The key RQ1 result is denominator discipline, not a single coverage rate.
-->

---

# Audited Identity Comes Before Transitions

<div class="pipeline">
  <div class="pipe-card">
    <p class="eyebrow">Parsed source</p>
    <p class="kpi">23,599</p>
    <p class="kpi-label">raw rows</p>
    <p class="kpi-note">Twenty annual workbooks, FY2005-FY2024.</p>
  </div>
  <div class="pipe-arrow">&rarr;</div>
  <div class="pipe-card">
    <p class="eyebrow">Deduplicated</p>
    <p class="kpi">23,593</p>
    <p class="kpi-label">retained records</p>
    <p class="kpi-note">Six exact duplicate source records collapsed.</p>
  </div>
  <div class="pipe-arrow">&rarr;</div>
  <div class="pipe-card">
    <p class="eyebrow">Longitudinal identity</p>
    <p class="kpi">1,690</p>
    <p class="kpi-label">stable administrative lineages</p>
    <p class="kpi-note">Deterministically linked record histories.</p>
  </div>
  <div class="pipe-arrow">&rarr;</div>
  <div class="pipe-card">
    <p class="eyebrow">Configuration history</p>
    <p class="kpi">1,767</p>
    <p class="kpi-label">asset episodes</p>
    <p class="kpi-note">New episode when reported asset evidence resets.</p>
  </div>
</div>

<div class="callout">
  <p>A <strong>stable administrative lineage</strong> is an inferred administrative history, not proof of unchanged physical assets. All 16 accepted uncertain links are exposed and tested by whole-lineage exclusion.</p>
</div>

<!--
Script cue: Define lineage carefully; do not call it a verified physical plant identity.
-->

---

<!-- _class: dense -->

# Analytical Frames Match the Estimands

<table class="source-table">
  <thead>
    <tr>
      <th>Frame</th>
      <th>Rows</th>
      <th>Lineages</th>
      <th>Events</th>
      <th>Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Descriptive entry risk set</td>
      <td>16,519</td>
      <td>1,223</td>
      <td>55</td>
      <td>First reported installed-capacity events</td>
    </tr>
    <tr>
      <td>Broad exact-year Firth</td>
      <td>15,154</td>
      <td>1,137</td>
      <td>35</td>
      <td>Adjacent-year, complete-covariate entry model</td>
    </tr>
    <tr>
      <td>Prior-operation Firth</td>
      <td>13,072</td>
      <td>1,019</td>
      <td>33</td>
      <td>Exact frame plus positive prior throughput</td>
    </tr>
    <tr>
      <td>Same-episode / identity-certain</td>
      <td>15,095 / 15,107</td>
      <td>1,135 / 1,130</td>
      <td>24 / 35</td>
      <td>Continuity / linkage sensitivities</td>
    </tr>
    <tr>
      <td>Engineering components</td>
      <td>6,511</td>
      <td>493</td>
      <td>-</td>
      <td>Positive-throughput, positive-output generator-years within bounds</td>
    </tr>
  </tbody>
</table>

<div class="callout">
  <p>Entry means the <strong>first report of positive installed electrical capacity</strong>; it is not a verified retrofit or commissioning date.</p>
</div>

<!--
Script cue: Say rows, lineages, and events in that order for each modeled entry frame.
-->

---

# Why Firth for First Entry?

<div class="method-grid">
  <div class="formula-card">
    <p class="eyebrow">Sparse-event estimator</p>
    <p class="formula">Firth = bias-reduced logistic regression using a Jeffreys-prior penalty</p>
    <p class="small">It reduces first-order small-sample bias and keeps estimates finite under separation.</p>
  </div>
  <div class="card">
    <p class="eyebrow">Exact-year frame</p>
    <p class="big">Only adjacent records still at risk.</p>
    <p class="small">Prior age and processing capacity describe the lineage before entry.</p>
  </div>
  <div class="card">
    <p class="eyebrow">Prior-operation frame</p>
    <p class="big">Require positive prior-year throughput.</p>
    <p class="small">This is a nested sensitivity, not an independent comparison group.</p>
  </div>
  <div class="card">
    <p class="eyebrow">Interpretation</p>
    <p class="big">Association, not intervention effect.</p>
    <p class="small">All four models complete 499 whole-lineage bootstrap replications.</p>
  </div>
</div>

<!--
Script cue: Define Firth in one sentence, then return to the substantive risk-set distinction.
-->

---

# Scale Selection Is Clear; Age Is Uncertain

<div class="two-col wide-left">
  <div class="figure-card figure-wide">
    <img src="../figures/figure2_selective_transition.png" alt="Firth entry odds ratios for age bands and processing capacity in two risk sets" />
  </div>
  <div class="stack">
    <div class="kpi-card">
      <p class="eyebrow">Scale · 300 vs 100 t/day</p>
      <p class="kpi">OR 6.13 / 6.25</p>
      <p class="kpi-note">Strong positive association in both entry frames.</p>
    </div>
    <div class="kpi-card">
      <p class="eyebrow">Joint age evidence</p>
      <p class="kpi">.380 / .186</p>
      <p class="kpi-note">Broad / prior-operation joint age p-values. Same episode: .051; identity certain: .357.</p>
    </div>
  </div>
</div>

<!--
Script cue: Lead with the scale contrast, then state why the age evidence does not support a frame-dependent story.
-->

---

# What the Entry Result Supports

<div class="three-col">
  <div class="claim-card good">
    <p class="eyebrow">Supported</p>
    <p class="big">Entry is rare and strongly scale-selective.</p>
    <p class="small">A 300-versus-100 t/day contrast has about six times the conditional odds in both frames.</p>
  </div>
  <div class="claim-card boundary">
    <p class="eyebrow">Not supported</p>
    <p class="big">No defensible age-only rule.</p>
    <p class="small">Broad and identity-certain tests are null; the 24-event same-episode result is borderline.</p>
  </div>
  <div class="card">
    <p class="eyebrow">Observed pathways · 55 events</p>
    <p class="big">35 continuity · 11 rebuild-like · 9 forward-dated</p>
    <p class="small">Administrative classifications describe evidence patterns, not verified projects.</p>
  </div>
</div>

<div class="callout">
  <p>Processing scale is a screening marker for unobserved technical, financial, and municipal conditions, not the causal effect of enlarging a plant.</p>
</div>

<!--
Script cue: Keep the supported and unsupported claims equally explicit.
-->

---

# Gross MWh/t Is an Accounting Identity

<div class="formula-card">
  <p class="eyebrow">Exact facility-year identity</p>
  <p class="formula">gross MWh/t = 0.024 &times; design intensity &times; capacity factor &divide; processing utilization</p>
</div>

<div class="term-row">
  <div class="term-chip"><strong>Gross MWh/t</strong> = annual gross electricity generated divided by annual waste throughput.</div>
  <div class="term-chip"><strong>Design intensity</strong> = installed electrical kW per t/day of waste-processing design capacity.</div>
  <div class="term-chip"><strong>Capacity factor</strong> = annual gross output relative to installed kW operating for all 8,760 hours.</div>
</div>

<div class="callout">
  <p>Processing utilization is annual throughput divided by 365 times processing design capacity. The identity is exact, but it is not a causal decomposition or an independent efficiency score.</p>
</div>

<!--
Script cue: Define every component before interpreting cohort differences.
-->

---

# Engineering Frame Separates Design From Operation

<div class="three-col">
  <div class="kpi-card">
    <p class="eyebrow">Primary component frame</p>
    <p class="kpi">6,511</p>
    <p class="kpi-label">generator-years</p>
    <p class="kpi-note">Positive capacity, throughput, and output within predeclared engineering bounds.</p>
  </div>
  <div class="kpi-card">
    <p class="eyebrow">Repeated histories</p>
    <p class="kpi">493</p>
    <p class="kpi-label">stable lineages</p>
    <p class="kpi-note">Uncertainty is clustered by audited stable lineage.</p>
  </div>
  <div class="kpi-card">
    <p class="eyebrow">Two component models</p>
    <p class="kpi">D + F</p>
    <p class="kpi-label">installed sizing + annual use</p>
    <p class="kpi-note">Waste loading enters through processing utilization.</p>
  </div>
</div>

<div class="callout">
  <p>Reported start year is an administrative <strong>design-vintage marker</strong>, not a verified boiler or generator installation date.</p>
</div>

<!--
Script cue: Emphasize the distinction between a mostly fixed design attribute and an annual operating component.
-->

---

# The Cohort Hierarchy Is Mainly Generator Sizing

<div class="two-col wide-left">
  <div class="figure-card figure-wide">
    <img src="../figures/figure3_efficiency_structure.png" alt="Generator design intensity and electrical capacity factor by reported start-year cohort" />
  </div>
  <div class="stack">
    <div class="kpi-card">
      <p class="eyebrow">Design intensity</p>
      <p class="kpi">5.3 &rarr; 20.6</p>
      <p class="kpi-note">Median installed kW per t/day, oldest to newest reported cohort.</p>
    </div>
    <div class="kpi-card">
      <p class="eyebrow">Capacity factor</p>
      <p class="kpi">No monotonic gradient</p>
      <p class="kpi-note">Annual use of installed kW does not reproduce the pattern; the hierarchy is principally installed sizing.</p>
    </div>
  </div>
</div>

<!--
Script cue: Interpret the cohort pattern through installed sizing and annual capacity factor.
-->

---

# The Age Association Is Specification-Dependent

<div class="two-col">
  <div class="claim-card boundary">
    <p class="eyebrow">Heating-controlled legacy specification</p>
    <p class="kpi">age = -0.0349</p>
    <p class="kpi-label">p&lt;.001 · R&sup2;=.4737</p>
    <p class="kpi-note">Gross MWh/t appears lower with reported age when installed sizing is omitted.</p>
  </div>
  <div class="claim-card good">
    <p class="eyebrow">Add generator design intensity</p>
    <p class="kpi">age = -0.0020</p>
    <p class="kpi-label">p=.2977 · R&sup2;=.8131</p>
    <p class="kpi-note">Design intensity enters at +0.7532 (p&lt;.001).</p>
  </div>
</div>

<div class="callout">
  <p>The diagnostic uses <strong>5,806</strong> engineering-valid rows with plausible heating value. Scale and utilization also become non-significant after sizing is added.</p>
</div>

<!--
Script cue: Call this specification dependence, not causal mediation.
-->

---

# Observed Pathways Start at Different Ranks

<div class="two-col wide-left">
  <div class="figure-card figure-wide">
    <img src="../figures/figure4_post_entry_trajectories.png" alt="First-complete-year component ranks for continuity and rebuild-like entry pathways" />
  </div>
  <div class="stack">
    <div class="kpi-card">
      <p class="eyebrow">Continuity · n=27</p>
      <p class="kpi">40 / 37 / 54</p>
      <p class="kpi-note">Gross MWh/t / design intensity / capacity factor ranks.</p>
    </div>
    <div class="kpi-card">
      <p class="eyebrow">Rebuild-like · n=11</p>
      <p class="kpi">72 / 66 / 65</p>
      <p class="kpi-note">Same first-complete-year ranks. Descriptive selected contrast; six forward-dated observations are omitted.</p>
    </div>
  </div>
</div>

<!--
Script cue: Explain the rank denominator and the selected, noncausal pathway comparison.
-->

---

<!-- _class: dense -->

# Stress Tests Preserve the Component Interpretation

<table class="source-table">
  <thead>
    <tr>
      <th>Stress test</th>
      <th>Current evidence</th>
      <th>Interpretation</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Two ten-year windows</td>
      <td>Scale coefficient in the design-intensity model: 0.474 / 0.577</td>
      <td>The sizing relationship appears in both periods.</td>
    </tr>
    <tr>
      <td>Engineering bounds</td>
      <td>Conservative / broad scale coefficients: 0.520 / 0.536</td>
      <td>The result is not tied to one plausibility range.</td>
    </tr>
    <tr>
      <td>Lineage-equal weighting</td>
      <td>Design-vintage hierarchy remains</td>
      <td>Longer observed histories do not create the main pattern.</td>
    </tr>
    <tr>
      <td>Identity-certain lineages</td>
      <td>6,450 rows; scale coefficient 0.533</td>
      <td>Accepted uncertain links do not drive the component pattern.</td>
    </tr>
    <tr>
      <td>Within-episode operating models</td>
      <td>Utilization-capacity-factor association remains positive</td>
      <td>Used only for components with meaningful within-asset change.</td>
    </tr>
  </tbody>
</table>

<div class="callout">
  <p>Robustness strengthens the descriptive component result; it does not make throughput, maintenance, sizing, or output exogenous.</p>
</div>

<!--
Script cue: Summarize the purpose of each test rather than reading the table cell by cell.
-->

---

# Evidence Boundaries Are Part of the Result

<div class="three-col">
  <div class="claim-card boundary">
    <p class="eyebrow">Identity</p>
    <p class="big">Lineages are inferred.</p>
    <p class="small">No physical-site registry verifies ownership, equipment, replacement, or closure histories.</p>
  </div>
  <div class="claim-card boundary">
    <p class="eyebrow">Entry</p>
    <p class="big">35 broad; 24 same episode.</p>
    <p class="small">Firth and bootstrap intervals cannot replace missing project, finance, or contract data.</p>
  </div>
  <div class="claim-card boundary">
    <p class="eyebrow">Engineering</p>
    <p class="big">Gross output is not net benefit.</p>
    <p class="small">No complete net export, useful heat, cost, outage, or lifecycle-emissions measure.</p>
  </div>
</div>

<div class="callout">
  <p>All estimates are descriptive or diagnostic associations. The paper does not identify retrofit effects, pathway effects, or an optimal investment policy.</p>
</div>

<!--
Script cue: State the noncausal boundary without weakening the measurement contribution.
-->

---

# Contribution: Measurement Before Mechanism

<div class="three-col">
  <div class="claim-card good">
    <p class="eyebrow">Coverage</p>
    <p class="big">Report counts and volumes together.</p>
    <p class="small">A 41.1% record share coexists with 80.1% throughput coverage.</p>
  </div>
  <div class="claim-card boundary">
    <p class="eyebrow">Entry</p>
    <p class="big">Use scale for screening, not an age-only rule.</p>
    <p class="small">Scale is strongly associated with entry; joint age evidence is uncertain.</p>
  </div>
  <div class="card">
    <p class="eyebrow">Generators</p>
    <p class="big">Decompose before benchmarking.</p>
    <p class="small">Gross MWh/t should be read through sizing, capacity factor, and waste loading.</p>
  </div>
</div>

<div class="callout">
  <p>The next evidence should link procurement, construction, generator history, net export, heat use, outages, waste composition, and finance to specific projects.</p>
</div>

<!--
Script cue: Present the contribution as a defensible measurement architecture.
-->

---

<!-- _class: close -->

# Discussion Questions

<p class="subtitle">The paper separates fleet coverage, first entry, and generator components before interpreting hierarchy.</p>

<div class="close-line">
  <p>Is the three-estimand architecture convincing? Are the Firth entry design and engineering identity explained clearly enough? Which missing project-level evidence should come next?</p>
</div>

<!--
Script cue: Ask for targeted feedback, then stop.
-->
