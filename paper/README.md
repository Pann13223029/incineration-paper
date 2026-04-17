# Paper Workspace

This directory is the active article layer.

Current repo state:

- private remote: `https://github.com/Pann13223029/incineration-paper`
- frozen milestone tag: `wm-near-submission-20260418-9af5603`

Start here:

1. [`manuscript/paper.md`](manuscript/paper.md)
2. [`manuscript/paper.tex`](manuscript/paper.tex)
3. [`submission/current-status.md`](submission/current-status.md)
4. [`notes/claim-stack.md`](notes/claim-stack.md)
5. [`notes/thesis-to-paper-map.md`](notes/thesis-to-paper-map.md)
6. [`notes/paper-claim-evidence-map.md`](notes/paper-claim-evidence-map.md)
7. [`notes/paper-budget.md`](notes/paper-budget.md)
8. [`notes/reviewer-rubric.md`](notes/reviewer-rubric.md)
9. [`notes/paper-structure-checklist.md`](notes/paper-structure-checklist.md)
10. [`notes/abstract-introduction-checklist.md`](notes/abstract-introduction-checklist.md)
11. [`journals/target-journals.md`](journals/target-journals.md)
12. [`references/selected-references.md`](references/selected-references.md)
13. [`references/citation-plan.md`](references/citation-plan.md)
14. [`supplement/supplement.md`](supplement/supplement.md)
15. [`submission/title-page.md`](submission/title-page.md)
16. [`submission/highlights.md`](submission/highlights.md)
17. [`submission/cover-letter.md`](submission/cover-letter.md)
18. [`submission/submission-checklist.md`](submission/submission-checklist.md)
19. [`evidence/`](evidence/)

## Rule

The paper should narrow and reorganize the thesis evidence. It should not become
a second source of empirical truth.

Refresh paper-facing evidence copies with:

```bash
npm run paper:sync
```

Export submission-facing manuscript artifacts with:

```bash
npm run paper:export
```

This writes local-only generated files under `paper/submission/`:

- `waste-management-manuscript.md`
- `waste-management-manuscript.html`
- `waste-management-manuscript.docx`
- `waste-management-manuscript.pdf`

Build a cleaner LaTeX reading PDF with:

```bash
npm run paper:build:latex
```

This writes a local-only manuscript PDF at:

- `paper/submission/waste-management-manuscript-latex.pdf`

For opening the current paper from another machine without rebuilding it, use
the tracked share copy:

- `paper/share/waste-management-manuscript-latex.pdf`
