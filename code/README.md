# Code Workspace

The code layer is split by responsibility. Analysis code creates evidence;
publishing code turns existing sources and evidence into review artifacts.

## Directory Roles

| Path | Responsibility | Main entry point |
|:--|:--|:--|
| `analysis/` | Parse data, construct samples, estimate models, run robustness checks, and verify claims | `07_rebuild_analysis.py` |
| `publishing/` | Synchronize evidence, export submission files, build the LaTeX PDF, and export paper slides | npm commands in `package.json` |

## Analysis Order

The numbered analysis stages run in this order:

```text
02 parse panel
  -> 03 add grid factors
  -> 04 audit the estimation frame
  -> 05a estimate entry and transition models
  -> 05 estimate generator-performance models
  -> 06 run robustness checks
  -> 06a/06b run data-quality and identifier audits
  -> 08 verify paper-facing claims
```

`analysis/panel_utils.py` owns shared sample definitions, technology mappings,
manifest normalization, and regression-frame construction. Change it carefully:
multiple downstream stages depend on its contracts.

## Commands

```bash
npm run repo:check
npm run analysis:rebuild
npm run claims:verify
npm run paper:sync
npm run paper:check
npm run paper:export:nopdf
npm run paper:build:latex
```

`repo:check` validates ownership boundaries and tracked Markdown links. Run it
after moving files or changing navigation documentation.

Do not hand-edit `output/` to compensate for a code change. Regenerate the
evidence, synchronize `paper/evidence/current/`, and let claim verification
identify any paper-facing drift.
