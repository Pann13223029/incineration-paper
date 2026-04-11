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

**Methods:** Two-way fixed-effects panel (facility FE + year FE), FY2005-2024.
See `ARCHITECTURE.md` for the full blueprint.

**Status:** Data pipeline complete (23,599 obs, 20 years). Next: EDA + grid
emission factors + regression.

---

## Repo Structure
- `thesis/` — Chapters in Markdown (to be drafted)
- `research/literature/` — Paper summaries and annotated bibliography
- `research/notes/` — Expert panel outputs, working notes
- `data/raw/` — Downloaded MOE Excel files (gitignored)
- `data/processed/` — Cleaned panel dataset (gitignored)
- `code/scripts/` — Numbered Python scripts
- `code/notebooks/` — Jupyter notebooks
- `output/` — Generated figures, tables, reports
- `archive/` — Deprecated work

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
- Follow the protocol in the first thesis's panel protocol (3-round structure).
- All panel outputs saved to `research/notes/expert-panel/`.

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
