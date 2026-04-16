# Defense Slides

This directory contains the editable oral-defense deck for the thesis.

## Files

- `defense-deck.md`: primary slide deck in Markdown, structured for `5-7` core slides plus short appendix slides
- `themes/defense-apu.css`: custom Marp theme for the polished defense deck
- `figures/`: local SVG assets used by the deck
- `dist/`: generated local presentation artifacts, produced by the export script and ignored in Git

## Why Markdown

The repo keeps the deck in Markdown so it is:

- easy to diff and revise in Git
- easy for assistants to update without layout drift
- portable into Marp, PowerPoint, Google Slides, Figma Slides, or PDF workflows later

## Suggested use

1. Revise `defense-deck.md` as the thesis changes.
2. Start with `research/notes/final-viva-cheat-sheet.md` for the one-file viva spine.
3. Rehearse using `research/notes/defense-question-order.md`.
4. Use `research/notes/defense-rapid-answers.md` for fast-answer rehearsal.
5. Use `research/notes/defense-q-and-a.md` for hostile follow-up preparation.
6. Use `research/notes/defense-run-sheet.md` for timed delivery.
7. Keep slide claims aligned with `output/claim_verification.md`.

## Export options

### Reproducible local export

```bash
npm install
npm run slides:export
```

This writes:

- `research/slides/dist/defense-deck.html`

Optional PDF export:

```bash
npm run slides:export:pdf
```

This also writes:

- `research/slides/dist/defense-deck.pdf` when a local Chrome/Edge browser can launch headlessly

If PDF export fails with a `TargetCloseError`, rerun the same command in a normal local shell. Sandboxed terminals can block headless Chrome even when the browser works normally on the machine.

### Frozen defense bundle

```bash
npm run slides:bundle
```

This writes:

- `research/slides/dist/defense-bundle/`
- `research/slides/dist/defense-bundle.zip`

The bundle includes the HTML deck, slide source, local assets, the final viva cheat sheet, rehearsal notes, supervisor brief, and the current claim-verification snapshot.

### Other options

- Read directly as speaker notes and copy into a conventional slide tool.
- Use the generated HTML deck directly in a browser if you want a lightweight presentation mode.
- Copy the deck into a conventional slide tool later only if you need institution-specific branding or presenter view features.
