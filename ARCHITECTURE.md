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
