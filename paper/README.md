# Paper Workspace

This directory is the active article layer.

Current repo state:

- private remote: `https://github.com/Pann13223029/incineration-paper`
- frozen milestone tag: `wm-near-submission-20260418-9af5603`

Start here:

1. [`manuscript/paper.md`](manuscript/paper.md)
2. [`submission/current-status.md`](submission/current-status.md)
3. [`notes/claim-stack.md`](notes/claim-stack.md)
4. [`notes/thesis-to-paper-map.md`](notes/thesis-to-paper-map.md)
5. [`notes/paper-claim-evidence-map.md`](notes/paper-claim-evidence-map.md)
6. [`notes/paper-budget.md`](notes/paper-budget.md)
7. [`notes/reviewer-rubric.md`](notes/reviewer-rubric.md)
8. [`notes/paper-structure-checklist.md`](notes/paper-structure-checklist.md)
9. [`notes/abstract-introduction-checklist.md`](notes/abstract-introduction-checklist.md)
10. [`journals/target-journals.md`](journals/target-journals.md)
11. [`references/selected-references.md`](references/selected-references.md)
12. [`references/citation-plan.md`](references/citation-plan.md)
13. [`supplement/supplement.md`](supplement/supplement.md)
14. [`submission/title-page.md`](submission/title-page.md)
15. [`submission/highlights.md`](submission/highlights.md)
16. [`submission/cover-letter.md`](submission/cover-letter.md)
17. [`submission/submission-checklist.md`](submission/submission-checklist.md)
18. [`evidence/`](evidence/)

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
