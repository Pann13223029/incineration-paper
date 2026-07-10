# Waste Management Submission Checklist

Official source: [Waste Management guide for authors](https://www.sciencedirect.com/journal/waste-management/publish/guide-for-authors), checked 10 July 2026.

## Format Gates

- [ ] Full-length article main text is no more than 6,500 words. The journal excludes the abstract, references, nomenclature, acknowledgements, and appendices from this count.
- [ ] Abstract is no more than 250 words, stands alone, and defines any necessary abbreviation at first use.
- [ ] Main manuscript contains no more than eight figures and tables combined, unless the cover letter justifies an exception.
- [ ] Title is concise and avoids unnecessary abbreviations or formulae.
- [ ] One to seven English keywords are present.
- [ ] A separate highlights file contains three to five bullets, each no more than 85 characters including spaces.
- [ ] Equations are editable text, numbered consecutively, and cited in the prose.
- [ ] Tables are editable, numbered, captioned, cited, and avoid vertical rules or duplicated results.
- [ ] Figures are supplied as separate reproducible files and remain legible at publication size.
- [ ] Editable `.tex` and/or `.docx` source accompanies the reading PDF; PDF alone is not an acceptable source.

## Integrity Gates

- [ ] The title page contains the author name, full affiliation, current corresponding email, and complete postal address.
- [ ] Funding and sponsor roles are stated, including an explicit no-specific-funding statement if applicable.
- [ ] Competing interests are declared consistently in the manuscript and submission system.
- [ ] The CRediT contribution statement reflects the human author's actual work.
- [ ] Data and code availability distinguish public source workbooks, derived data, redistribution limits, and versioned code.
- [ ] The manuscript discloses overlap with the thesis or related outputs if required by the venue.
- [ ] OpenAI Codex and Anthropic Claude use is named in a declaration immediately before the references; purpose, human review, and author responsibility are stated.
- [ ] AI tools are not listed as authors and no citation, result, or interpretation is accepted without human verification.
- [ ] All citations have been checked against publisher or official records; see `paper/references/verification-notes.md`.

## Repository Gates

Run in this order after substantive analysis or manuscript changes:

```bash
npm run analysis:rebuild
npm run paper:sync
npm run paper:check
npm run claims:verify
npm run paper:export:nopdf
npm run paper:build:latex
npm run repo:check
git diff --check
```

Then inspect the generated PDF page by page, confirm no overfull LaTeX boxes, verify the final word/item counts, and compare the tracked share PDF with the manuscript commit being submitted.

## Current Evidence Boundary

The paper may report reconstructed stable administrative lineages, first reported installed-generation-capacity events, gross output, generator design intensity, electrical capacity factor, and waste-loading measures. It must not infer verified physical closure, a uniquely identified retrofit, net electricity export, useful heat, R1 performance, lifecycle benefit, or causal effects of age and equipment sizing from the available administrative panel.
