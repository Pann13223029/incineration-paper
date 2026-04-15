# Defense Slides

This directory contains the editable oral-defense deck for the thesis.

## Files

- `defense-deck.md`: primary slide deck in Markdown, structured for `5-7` core slides plus short appendix slides
- `themes/defense-apu.css`: custom Marp theme for the polished defense deck
- `figures/`: local SVG assets used by the deck

## Why Markdown

The repo keeps the deck in Markdown so it is:

- easy to diff and revise in Git
- easy for assistants to update without layout drift
- portable into Marp, PowerPoint, Google Slides, Figma Slides, or PDF workflows later

## Suggested use

1. Revise `defense-deck.md` as the thesis changes.
2. Rehearse using `research/notes/defense-question-order.md`.
3. Use `research/notes/defense-rapid-answers.md` for fast-answer rehearsal.
4. Use `research/notes/defense-q-and-a.md` for hostile follow-up preparation.
5. Use `research/notes/defense-run-sheet.md` for timed delivery.
6. Keep slide claims aligned with `output/claim_verification.md`.

## Export options

- Read directly as speaker notes and copy into a conventional slide tool.
- Use a Markdown slide tool such as Marp with `themes/defense-apu.css` if you want local export automation.
- Copy the deck into a conventional slide tool later only if you need institution-specific branding or presenter view features.
