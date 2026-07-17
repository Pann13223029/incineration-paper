# Professor-Facing Thesis Profile

This directory preserves the comprehensive professor-review content frozen from
commit `4ac9afe` before the public journal draft was revised. Its LaTeX wrapper
now presents that content as an APU-style graduation thesis: 12-point type on
A4 paper, 1.5 line spacing, a formal cover, contents, lists of figures and
tables, and front/main-matter page numbering. It shares the canonical analysis,
evidence, tables, figures, and supplement with the public profile; it is not an
independent empirical pipeline.

Build the professor-facing PDF with:

```bash
npm run paper:build:professor
```

The canonical tracked reading copy is
`paper/share/professor-review-thesis.pdf`. The former
`paper/share/professor-review-manuscript-latex.pdf` path is refreshed as a
compatibility alias.

`npm run repo:check` conservatively excludes tables, captions, equations, and
headings when enforcing the APU minimum of 6,500 English main-text words.

## Immutable Baseline Hashes

These hashes identify artifacts exactly as stored at tag
`professor-review-v1`. The source files in this directory use adjusted relative
figure paths and a thesis-format LaTeX wrapper, and the professor reading PDF is
a fresh compilation, so their working-tree byte hashes are not expected to
match the tagged files.

| Artifact at `professor-review-v1` | SHA-256 |
|:--|:--|
| `paper/manuscript/paper.md` | `d971a92f05961cc82288044298cf282c6359f50ee83c11f4a7fe0bd3ffe85209` |
| `paper/manuscript/paper.tex` | `418cba59463244c88368e7a0a156671ab096ad070286fe2848fdb64e92e5c39c` |
| `paper/share/waste-management-manuscript-latex.pdf` | `00b5ab260f097d5552f472a4fdff4dbb6b3b143cb853a0d3f733af5780dbbf99` |
| `paper/supplement/supplement.md` | `601d92c19804323c11a334c6fd0b20f4e511554fc25867f5d06a59504a72327e` |

The Git tag, rather than the mutable convenience PDF, is the authoritative
complete-repository baseline.
