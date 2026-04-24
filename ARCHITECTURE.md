# Paper Repo Architecture

## Purpose

This repository is a **paper-focused derivative workspace** cloned from the defended incineration-thesis repo.

Its purpose is to preserve the original empirical pipeline while shifting the
active writing target from a bachelor's thesis to a journal-style paper.

## Design Principle

Keep one stable evidence core and let the paper layer narrow, reorganize, and
reframe that evidence for article publication.

In practical terms:

- `code/`, `data/`, and `output/` remain the empirical core
- `paper/` is the active article workspace
- `thesis/` and `research/` remain as reference history from the original thesis repo

## Active vs Reference Layers

### Active

- `paper/manuscript/paper.md`
- `paper/notes/`
- `paper/journals/`
- `paper/supplement/`
- `paper/evidence/current/`

### Canonical empirical base

- `code/scripts/`
- `data/raw/`
- `data/processed/`
- `output/`

### Reference-only thesis layer

- `thesis/`
- `research/`

## Artifact Flow

```text
data/raw
  -> code/scripts
  -> data/processed
  -> output/*
  -> paper/evidence/current/*
  -> paper/notes/claim-stack.md
  -> paper/manuscript/paper.md
  -> paper/supplement/*
  -> paper/journals/target-journals.md
```

The important distinction is that `paper/manuscript/paper.md` should not become
a second uncontrolled source of empirical truth. It should remain downstream of
the canonical outputs.

## Current Evidence Snapshot

- Full panel: (23,599 observations, 2,948 unique facilities, FY2005–FY2024)
- Adoption risk set: (13,770 facility-years, 2,035 facilities, 141 observed first-adoption events)
- Main adoption model: 11,717 facility-years across 1,915 facilities and 140 events
- Adoption age pattern: facilities older than 10 years are 1.1–1.8 percentage points less likely to transition into generation.
- Adoption capacity pattern: prior-year capacity raises transition probability by about 0.50 percentage points per 100 t/day.
- Pathway audit: 82 observed transitions as reset/rebuild-like, 38 as continuity/in-place-upgrade-like, 20 as forward-dated or placeholder entries, and 1 as unresolved.

| Evidence block | Current finding | Check |
|:--|:--|:--|
| Adoption hazard, prior-year age bands | Facilities older than 10 years are 1.1–1.8 pp less likely than 0–10-year facilities to record transition in the next observed year | p < 0.05 in every reported age-band coefficient |
| Adoption hazard, prior-year capacity | +0.50 pp per 100 t/day | p < 0.05 |
| Facility age effect | −0.019 to −0.035 in the four main specifications | p < 0.001 in every reported main specification |
| Design capacity effect | +0.041 to +0.103 in the four main specifications | Positive in every main specification |
| Capacity utilization effect | +0.541 to +0.779 in the four main specifications | Positive in every main specification |

## Directory Map

```text
incineration-paper/
|
|-- paper/
|   |-- manuscript/                    # active paper draft
|   |-- notes/                         # claim stack, conversion map, rewrite logic
|   |-- journals/                      # target-journal fit and strategy
|   |-- supplement/                    # supplement planning
|   |-- evidence/                      # synced paper-facing output snapshots
|   |-- figures/
|   +-- tables/
|
|-- code/                              # empirical pipeline retained from thesis repo
|-- data/                              # raw and processed data
|-- output/                            # canonical generated artifacts
|-- thesis/                            # defended thesis baseline
|-- research/                          # legacy supervision and defense machinery
|-- docs/figures/                      # README-facing diagrams
```

## Operational Rules

1. The paper draft lives in `paper/manuscript/paper.md`.
2. The current defended thesis remains in `thesis/thesis.tex`.
3. Current result values come from `output/*`, not from the paper draft.
4. After material result changes, refresh the paper-facing evidence snapshot with `npm run paper:sync`.
5. Do not treat `research/` as the active paper workspace; it is legacy thesis support.

## Immediate Goal

The near-term goal is one strong article built around:

- selective modernization on the adoption margin
- bounded responsiveness on the efficiency margin

That means the architecture should optimize for:

- one dominant claim
- narrow article scope
- light manuscript body
- strong supplement plan
- traceability back to the defended thesis evidence base
