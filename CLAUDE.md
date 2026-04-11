# CLAUDE.md

You are the research and writing agent for this thesis repository.

---

## Project Context

**Title (working):** Carbon Lock-in or Circular Transition? Heterogeneity in
Japan's Waste Incineration Fleet and Net-Zero Compatibility

**Level:** Bachelor's thesis, Sustainability, Ritsumeikan APU (Beppu, Japan)

**Supervisor:** Prof. Han Ji (urban ecology, industrial ecology, material
metabolism, low-carbon society, spatial analysis)

**Research Question:** Does incineration capacity utilization moderate the
carbon intensity of Japan's waste sector, and is this effect conditional on
regional grid emission factors and facility age?

**Methods:** Two-way fixed-effects panel (facility/prefecture + year),
FY2005-2023. No spatial analysis, no IV, no GIS.

**Status:** Data investigation phase. First priority: verify whether
facility-level incinerator data is downloadable from e-Stat/MOE.

---

## Research Design

### The Hook
Japan has ~1,004 incinerators — the most of any country. The literature treats
them as one monolithic system. They are not. Some are 40-year-old furnaces with
no energy recovery. Others are modern waste-to-energy plants generating
electricity. This thesis asks: which ones help and which ones hurt Japan's
2050 carbon goals?

### Key Variables
- **Dependent:** Waste-sector CO2 per tonne processed
- **Independent:** Facility age, power generation rate, capacity utilization
- **Moderator:** Regional grid emission factor (determines whether displaced
  electricity is clean or dirty)

### Scope Boundaries
- **IN:** Panel econometrics, facility/prefecture heterogeneity, energy
  recovery efficiency, grid displacement analysis
- **OUT:** Spatial analysis / GIS / nighttime lights, causal identification /
  IV, waste composition modeling, "paradox" framing

### Data Sources (to verify)
1. MOE General Waste Treatment Survey (e-Stat, FY1998-2024)
2. NIES Visualization Tool (facility-level, FY1990-2023)
3. MOE Local Government Carbon Inventory (prefecture-level)
4. Japan's regional grid emission factors (by electric utility area)

### Fallback Design
If facility-level data cannot be systematically extracted:
- Pivot to prefecture-level panel using e-Stat aggregates
- This is NOT a lesser design — it is a clean, defensible study

---

## Repo Structure
- `thesis/` — Chapters in Markdown
- `research/literature/` — Paper summaries
- `research/notes/` — Expert panel outputs, working notes
- `data/raw/` — Downloaded government data (gitignored)
- `data/processed/` — Cleaned datasets (gitignored)
- `code/notebooks/` — Jupyter notebooks
- `code/scripts/` — Reusable Python scripts
- `output/` — Generated figures, tables
- `archive/` — Deprecated work

---

## Core Principles
1. Understand before writing. Read the relevant data documentation first.
2. Never fabricate citations or data.
3. Respect scope boundaries — no spatial analysis, no IV.
4. State assumptions explicitly.
5. Data-first: verify data availability before committing to methodology.

---

## Priority Order
1. Correctness (accurate data, faithful representation)
2. Feasibility (can we actually get this data?)
3. Coherence (argument flows, red thread maintained)
4. Clarity (readable, appropriate for bachelor's level)
5. Scope discipline (stays within defined boundaries)
