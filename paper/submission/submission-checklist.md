# Submission Checklist

This checklist converts the current paper repo into a practical
`Waste Management` submission packet.

Official source used for this checklist:
- Elsevier `Waste Management` guide for authors:
  https://www.sciencedirect.com/journal/waste-management/publish/guide-for-authors

## Current Status

- manuscript draft exists:
  - [paper.md](../manuscript/paper.md)
- title page exists:
  - [title-page.md](title-page.md)
- highlights file exists:
  - [highlights.md](highlights.md)
- cover letter draft exists:
  - [cover-letter.md](cover-letter.md)
- supplement draft exists:
  - [supplement.md](../supplement/supplement.md)
- working references layer exists:
  - [selected-references.md](../references/selected-references.md)
  - [citation-plan.md](../references/citation-plan.md)
- manuscript export command exists:
  - `npm run paper:export`
- LaTeX reading-PDF command exists:
  - `npm run paper:build:latex`
- clean manuscript PDF export exists:
  - `paper/submission/waste-management-manuscript.pdf`
- clean LaTeX reading PDF export exists when built:
  - `paper/submission/waste-management-manuscript-latex.pdf`

## Journal-Fit Checks

- abstract at or below 250 words:
  - current draft is about 235 words
- keywords present:
  - current manuscript has 6 keywords
- numbered main sections present:
  - yes
- figures and tables embedded in manuscript:
  - yes
- combined main-text figure/table count within 8:
  - current count is 6
- full-length article word count within 6,500 words:
  - current main text is about 4,870 words before references

## Still Required Before Real Submission

- rerun the reference-style check if the manuscript citations change
- confirm conflict-of-interest and funding statements in the submission system
- decide whether to keep or revise the AI disclosure statement and whether the
  journal requires it as a separate upload
- rerun `npm run paper:export` after any manuscript change
- rerun `npm run paper:build:latex` after any figure or layout change
- confirm author metadata exactly as it should appear in submission

## Nice-To-Have Before Submission

- `Waste Management`-specific editorial pass completed on current draft;
  repeat only after substantive manuscript changes
- a cleaner caption/figure numbering pass after conversion
- one or two appendix tables copied directly into the supplement if reviewers
  are likely to ask for them early
