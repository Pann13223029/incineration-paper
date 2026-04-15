---
marp: true
paginate: true
theme: defense-apu
size: 16:9
---

<!-- _class: hero -->

# Selective Modernization, Bounded Responsiveness

## Japan's Waste Incineration Fleet and Net-Zero Compatibility

<div class="pill-row">
  <span class="pill">23,599 facility-years</span>
  <span class="pill">2-part empirical design</span>
  <span class="pill">Verified claim spine</span>
</div>

<div class="meta-block">
  <strong>Pann Phetra</strong><br/>
  Bachelor's Thesis Defense<br/>
  Ritsumeikan Asia Pacific University, 2026
</div>

<!--
Open with the architecture, not with the policy debate.
Fast opening: This thesis asks two different questions with two different frames:
who actually transitions into generation, and conditional on generation, what predicts performance?
-->

---

<!-- _class: split -->

# 1. Thesis in One Sentence

<div class="two-col">
  <div>
    <div class="statement-card">
      <p class="eyebrow">Core claim</p>
      <p class="big-statement">Japan's incineration transition is empirically two-part: observed entry into generation is selective on the extensive margin, while conditional generator performance is shaped by age, scale, and bounded within-facility responsiveness on the intensive margin.</p>
    </div>
    <div class="note-card">
      <p class="eyebrow">Why the redesign matters</p>
      <ul>
        <li>A generator-only sample cannot carry the whole fleet-transition story.</li>
        <li>The revised thesis separates modernization entry from generator efficiency.</li>
        <li>That makes the scope narrower, cleaner, and harder to attack.</li>
      </ul>
    </div>
  </div>
  <div class="figure-card">
    <img src="../../docs/figures/readme_fleet_split.svg" alt="Fleet split overview" />
  </div>
</div>

<!--
Fast answer if pressed early: the earlier version over-asked a selected generator frame to explain the whole fleet.
The redesign fixes that by splitting extensive and intensive margins.
-->

---

<!-- _class: split -->

# 2. One Dataset, Two Analytical Frames

<div class="kpi-grid">
  <div class="kpi-card">
    <p class="eyebrow">Administrative panel</p>
    <p class="kpi">23,599</p>
    <p class="kpi-sub">facility-year observations</p>
    <p class="kpi-note">2,948 facilities, FY2005-FY2024</p>
  </div>
  <div class="kpi-card">
    <p class="eyebrow">Extensive margin</p>
    <p class="kpi">13,770</p>
    <p class="kpi-sub">risk-set rows</p>
    <p class="kpi-note">2,035 facilities, 141 observed first-adoption events</p>
  </div>
  <div class="kpi-card">
    <p class="eyebrow">Lagged hazard frame</p>
    <p class="kpi">11,717</p>
    <p class="kpi-sub">model rows</p>
    <p class="kpi-note">1,915 facilities, 140 retained events</p>
  </div>
  <div class="kpi-card">
    <p class="eyebrow">Intensive margin</p>
    <p class="kpi">5,683</p>
    <p class="kpi-sub">generator rows</p>
    <p class="kpi-note">1,016 facilities in the canonical efficiency frame</p>
  </div>
</div>

<div class="statement-card compact">
  <p class="eyebrow">Design logic</p>
  <p class="big-statement">The extensive margin asks who gets into generation. The intensive margin asks what drives performance once they are already there.</p>
</div>

<!--
If you need a 15-second version: same dataset, two different estimands, two different frames.
-->

---

<!-- _class: split -->

# 3. Observed Transition Into Generation Is Selective

<div class="two-col">
  <div class="figure-card">
    <img src="./figures/defense_adoption_hazard.svg" alt="Adoption hazard summary" />
  </div>
  <div>
    <div class="note-card">
      <p class="eyebrow">Main hazard result</p>
      <ul>
        <li><strong>Age penalty:</strong> facilities older than 10 years are about <strong>1.1-1.8 pp less likely</strong> to record observed transition.</li>
        <li><strong>Scale premium:</strong> each additional <strong>100 t/day</strong> raises annual transition probability by about <strong>0.5 pp</strong>.</li>
      </ul>
    </div>
    <div class="note-card">
      <p class="eyebrow">What that means</p>
      <ul>
        <li>Observed transition is concentrated among facilities already younger and larger before the event year.</li>
        <li>No broad late-life conversion wave appears in the coded panel.</li>
      </ul>
    </div>
  </div>
</div>

<!--
Fast oral version:
The extensive-margin result is simple: observed first transition into generation is selective, not diffuse.
The older-than-10 age penalty is negative, capacity is positive, and the sign pattern survives lagged cloglog and lagged LPM robustness.
-->

---

<!-- _class: split -->

# 4. The Pathway Audit Sharpens the Mechanism Claim

<div class="two-col">
  <div class="figure-card">
    <img src="./figures/defense_pathway_audit.svg" alt="Pathway audit summary" />
  </div>
  <div>
    <div class="note-card">
      <p class="eyebrow">Rule basis</p>
      <ul>
        <li><strong>Reset / rebuild-like</strong>: observed <code>year_started</code> reset or mature-to-new age reset.</li>
        <li><strong>Continuity / upgrade-like</strong>: no such reset on the event row.</li>
        <li><strong>Placeholder / forward-dated</strong>: left unresolved rather than forced into a stronger story.</li>
      </ul>
    </div>
    <div class="statement-card compact">
      <p class="eyebrow">Calibrated interpretation</p>
      <p class="big-statement">Reset/rebuild-like events are the largest observed bucket in this panel, but replacement is not uniquely identified and retrofit still remains in the story.</p>
    </div>
  </div>
</div>

<!--
Fast oral version:
The audit does not prove one mechanism.
It prevents the policy section from outrunning the data by showing that reset/rebuild-like transitions are the largest observed bucket, while continuity-type upgrades still exist.
-->

---

<!-- _class: split -->

# 5. Conditional Efficiency Looks Structured, Not Easily Reversed

<div class="two-col">
  <div class="figure-card">
    <img src="./figures/defense_efficiency_structure.svg" alt="Generator efficiency structure summary" />
  </div>
  <div>
    <div class="note-card">
      <p class="eyebrow">Main relationships</p>
      <ul>
        <li><strong>Age:</strong> older facilities are less efficient.</li>
        <li><strong>Capacity:</strong> larger facilities are more efficient.</li>
        <li><strong>Utilization:</strong> better-loaded facilities perform better.</li>
      </ul>
    </div>
    <div class="note-card">
      <p class="eyebrow">Deepest finding</p>
      <ul>
        <li>Within/total variance ratio is only <strong>0.1499</strong>.</li>
        <li>It falls further to <strong>0.0956</strong> post-Fukushima.</li>
        <li>Operations matter, but cross-facility gaps remain much larger than within-facility movement.</li>
      </ul>
    </div>
  </div>
</div>

<!--
Fast oral version:
The intensive-margin story is not that operations are irrelevant.
It is that the biggest differences remain across facilities, not within the same facility over time.
-->

---

<!-- _class: split -->

# 6. Why This Design, and Why Not Two-Way FE?

<div class="kpi-grid">
  <div class="note-card">
    <p class="eyebrow">Substantive fit</p>
    <p>The question is about structured heterogeneity, not removing all between-facility information by design.</p>
  </div>
  <div class="note-card">
    <p class="eyebrow">Age-year problem</p>
    <p>Facility age rises mechanically with year, so the main regressor is poorly identified in two-way FE.</p>
  </div>
  <div class="note-card">
    <p class="eyebrow">Variance structure</p>
    <p>With a within/total ratio of only <strong>0.1499</strong>, FE would lean on the smaller part of the signal.</p>
  </div>
  <div class="statement-card compact">
    <p class="eyebrow">Position</p>
    <p class="big-statement">Estimator choice follows the question, not a ritual preference for FE.</p>
  </div>
</div>

<!--
Use this slide to answer the hardest methods question in under 30 seconds:
age-year collinearity, low within variation, and estimator choice matched to the substantive question.
-->

---

<!-- _class: split -->

# 7. What the Thesis Claims, and Does Not Claim

<div class="two-col">
  <div class="claim-box do">
    <p class="eyebrow">Does claim</p>
    <ul>
      <li>The fleet transition is empirically two-part.</li>
      <li>Observed entry into generation is selective.</li>
      <li>Generator performance is shaped by age, scale, and bounded responsiveness.</li>
      <li>Capital-side modernization likely matters more than operations alone for the weakest segment.</li>
    </ul>
  </div>
  <div class="claim-box dont">
    <p class="eyebrow">Does not claim</p>
    <ul>
      <li>strict causal proof</li>
      <li>replacement as the only modernization pathway</li>
      <li>full net climate accounting</li>
      <li>heat-recovery or district-heating evaluation</li>
    </ul>
  </div>
</div>

<div class="statement-card compact">
  <p class="eyebrow">Defense posture</p>
  <p class="big-statement">The revised thesis is stronger because its scope now matches its evidence.</p>
</div>

<!--
This is the overclaim shield.
If pressed hard, say: the thesis is narrow on purpose because precision is a strength, not a weakness.
-->

---

<!-- _class: hero close -->

# 8. Bottom Line

<div class="closing-grid">
  <div class="closing-card">
    <p class="eyebrow">Extensive margin</p>
    <p class="closing-text">Old and small facilities rarely record observed transition into generation.</p>
  </div>
  <div class="closing-card">
    <p class="eyebrow">Intensive margin</p>
    <p class="closing-text">Among generators, vintage and scale gaps remain large even when utilization improves.</p>
  </div>
  <div class="closing-card">
    <p class="eyebrow">Implication</p>
    <p class="closing-text">Operations matter, but capital-side modernization and regional consolidation appear more consequential for the weakest segment.</p>
  </div>
</div>

<div class="statement-card compact close-line">
  <p class="big-statement">Japan's incineration transition is happening, but it is selective and slower than a net-zero-compatible fleet transition would require.</p>
</div>

<!--
Clean close:
The contribution is not that I prove one causal mechanism.
It is that I show, with a reproducible two-part design, where transition is actually occurring and where bounded responsiveness still constrains performance.
-->

---

<!-- _class: appendix -->

# Appendix A. Fast Answer: Why Not Two-Way FE?

<div class="statement-card">
  <p class="big-statement">Because age is mechanically linked to year, the main regressor is poorly identified in two-way FE, and the within signal is only 14.99% of the total.</p>
</div>

<div class="note-card">
  <ul>
    <li>FE would lean on the smaller part of the variance.</li>
    <li>The thesis question is about structured heterogeneity, not purging all between-facility information.</li>
  </ul>
</div>

---

<!-- _class: appendix -->

# Appendix B. Fast Answer: Did You Prove Replacement?

<div class="statement-card">
  <p class="big-statement">No. The pathway audit shows reset/rebuild-like events are the largest observed bucket in this panel, but it does not cleanly distinguish replacement, new build, and major refurbishment within that bucket.</p>
</div>

<div class="note-card">
  <ul>
    <li>Reset/rebuild-like: `82`</li>
    <li>Continuity/in-place upgrade: `38`</li>
    <li>Forward-dated/placeholder: `20`</li>
  </ul>
</div>

---

<!-- _class: appendix -->

# Appendix C. Fast Answer: Did You Prove Lock-In?

<div class="statement-card">
  <p class="big-statement">Not causally. The thesis shows that low within-facility movement, stable age/scale relationships, and bounded Fukushima response are strongly consistent with bounded infrastructural responsiveness.</p>
</div>

<div class="note-card">
  <ul>
    <li>Within/total ratio: `0.1499`</li>
    <li>Pre-Fukushima: `0.1795`</li>
    <li>Post-Fukushima: `0.0956`</li>
  </ul>
</div>
