# Legacy Thesis Archive

This directory preserves the defended thesis and its historical supervision,
defense, checkpoint, and packet-building workflow. It is retained for
traceability, not as the active paper workspace.

## Contents

| Path | Role |
|:--|:--|
| `thesis/` | Defended thesis source and figures. |
| `research/` | Historical defense notes, slides, checkpoints, and packet documentation. |
| `scripts/` | Automation used by the historical thesis workflow. |

## Rules

- Active paper writing belongs in `paper/`.
- Current empirical logic belongs in `code/analysis/`.
- Current generated evidence belongs in `output/`.
- Do not use archived thesis wording as evidence for the paper without checking the current outputs.
- Edit this directory only when a task explicitly concerns the defended thesis or its historical handoff workflow.

The legacy npm commands remain available under the `legacy:*` namespace in
`package.json`; their implementation lives in `legacy/scripts/`.
