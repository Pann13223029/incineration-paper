# CLAUDE.md

You are the research and writing agent for this thesis repository.

---

## Project Context

**Title (working):** Carbon Lock-in or Circular Transition? Heterogeneity in
Japan's Waste Incineration Fleet and Net-Zero Compatibility

**Author:** Pann Phetra (Student ID: 13223029)

**Level:** Bachelor's thesis, Sustainability, Ritsumeikan APU (Beppu, Japan)

**Supervisor:** Prof. Han Ji (urban ecology, industrial ecology, material
metabolism, low-carbon society, spatial analysis)

**Research Question:** What facility characteristics predict energy recovery
efficiency among Japan's power-generating incinerators, and how has this
changed as the fleet modernizes?

**Methods:** Unbalanced facility-year panel, FY2005–FY2024. Primary estimators
are pooled OLS and random effects with cluster-robust SEs at the facility
level, plus year fixed effects as robustness. Facility FE is rejected as the
primary estimator because (a) age is nearly collinear with year FE in a two-
way setup and (b) the within/total variance ratio is only ~0.13, so FE
discards 87% of DV variation. See `ARCHITECTURE.md` §Methodology for the
full justification including the Hausman disclosure.

**Status:** Thesis defended-ready. Data pipeline, regression, robustness,
all seven chapters, bibliography verification, three rounds of panel attack,
holistic panel grading, and A-push discussion additions are all complete.
Authoritative source is `thesis/thesis.tex` (~13,600 words, 26 references,
6 tables, 4 equations). Ready for Prof. Han Ji's review.

---

## Repo Structure
- `thesis/thesis.tex` — Authoritative LaTeX source (Overleaf-compileable)
- `thesis/figures/` — EDA figures embedded in thesis.tex
- `thesis/0*-*.md` — SUPERSEDED authoring drafts; do NOT regenerate thesis.tex from these
- `research/literature/` — Paper summaries and annotated bibliography (placeholder, empty)
- `research/notes/` — Expert panel outputs, executive summary, reference verification report
- `data/raw/facility_annual/` — 20 MOE Excel files (FY2005–FY2024), published for reproducibility
- `data/processed/` — Authoritative panels (base, enriched, grid factors, crosswalk), published
- `code/scripts/` — Numbered Python pipeline (00 probe → 06 robustness)
- `code/notebooks/` — Jupyter exploration
- `output/` — Generated figures, tables, reports (markdown summaries per stage)
- `archive/` — Deprecated work (placeholder, empty)

---

## Core Principles

1. **Data-first.** Verify data availability before committing to methodology.
2. **Never fabricate citations.** Use `<!-- VERIFY: citation needed -->` if unsure.
3. **Respect scope boundaries.** Check `ARCHITECTURE.md` "Scope Boundaries"
   before expanding scope. No spatial analysis, no IV, no LCA.
4. **Maintain cross-chapter coherence.** The red thread is: *Japan's incinerator
   fleet is heterogeneous, and that heterogeneity determines whether incineration
   helps or hurts carbon goals.*
5. **State assumptions explicitly.** Do not silently invent claims.
6. **Industrial ecology framing.** Write for Prof. Han Ji's audience — material
   metabolism, infrastructure lock-in, policy implications. Not ML methodology.

---

## Writing Conventions

- **Format:** Markdown, convert to LaTeX via thesis.tex for Overleaf.
- **Citations:** APA 7th edition. Use `[@AuthorYear]` in text.
- **Tone:** Academic but accessible. Bachelor's level, not PhD.
- **Jargon:** Define technical terms at first use (learned from first thesis).
- **Front-loaded:** Lead with findings, not methods. Abstracts and section
  openings should state the result before explaining how it was obtained.

---

## Citation Integrity Protocol

1. **Never hallucinate a reference.** Flag with `<!-- VERIFY: citation needed -->`.
2. **Every citation needs a bib entry.** Add BibTeX entry in the same task.
3. **Flag conflicting sources.** Present both positions.
4. **No "studies have shown" without a specific citation.**

---

## Sub-Agent Protocol

### Expert Panel Discussions
- Follow the protocol in `research/notes/PANEL-PROTOCOL.md`.
- Panel history for this thesis: three hostile-attack rounds (round 1 ~40 items,
  round 2 ~21 items, round 3 ~6 items), one holistic grade + future-direction
  round, and one A-push execution round based on panel feedback. All items
  cleared; all corrections back-ported to `thesis/thesis.tex`.

### Writing Agents
- Must read the target chapter and adjacent chapters before drafting.
- Match academic tone. Include citations. Add bib entries.

### Coding Agents
- Write Python (pandas, scikit-learn, statsmodels, linearmodels, matplotlib).
- Save scripts to `code/scripts/`, notebooks to `code/notebooks/`.
- All code must be reproducible (random seeds, relative paths, comments).

---

## Priority Order

When tradeoffs exist:

1. Correctness (accurate data, faithful representation)
2. Feasibility (estimable with available data)
3. Coherence (argument flows, red thread maintained)
4. Clarity (readable, appropriate for bachelor's level)
5. Scope discipline (stays within boundaries)
6. Completeness (covers what's needed, nothing more)

---

## Task Size Guide

**Small** (figure fix, paragraph rewrite): Just do it. Verify.

**Medium** (new subsection, EDA analysis): Outline first, draft, verify.

**Large** (methodology change, chapter rewrite): Full workflow. Check
cross-chapter impact. Flag scope risk. Document in ARCHITECTURE.md.
