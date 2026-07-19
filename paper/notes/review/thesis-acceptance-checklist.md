# Professor-Facing Thesis Acceptance Checklist

## Purpose

This checklist defines convergence criteria for the professor-facing graduation
thesis. It prevents each review pass from changing the standard after earlier
issues have been fixed. A later review should classify a finding as one of:

- **Regression:** a previously satisfied criterion now fails.
- **New evidence:** new data, supervisor guidance, or an external requirement
  changes what the thesis must do.
- **Optional improvement:** useful polish that does not block professor review.

The journal manuscript and supplement are outside this checklist.

## Acceptance gates

| Gate | Acceptance criterion | Status |
|:--|:--|:--|
| Thesis scope | Title, abstract, research questions, results, and conclusion consistently describe coverage, reported entry, and generator sizing. | **Pass** |
| University format | English main text exceeds 6,500 words and the PDF uses a graduation-thesis title page, contents page, numbered sections, references, and appendices. | **Pass: 10,797 reader-count words** |
| Primary model hierarchy | The broad exact-year five-parameter Firth model is the only primary entry model; prior-operation, same-episode, identity-certain, and other fits are sensitivities. | **Pass** |
| Model-decision provenance | The internal model freeze, implementation, and later diagnostic additions are distinguished by a version-control chronology and are not described as external preregistration. | **Pass** |
| Literature positioning | The comparator search is documented as retrospective and non-systematic, with explicit screening boundaries and no exhaustive novelty claim. | **Pass** |
| Event-history notation | The first-entry equation conditions on explicit at-risk status, not only the immediately previous outcome. | **Pass** |
| RQ3 claim boundary | “Largest component” is qualified as the largest absolute point-estimate accounting component; no joint ranking uncertainty or causal mediation is claimed. | **Pass** |
| Model transparency | Exact variable scaling, risk-set rule, reference groups, uncertainty type, and all focal model coefficients are reported in the methods or Appendix B. | **Pass** |
| Exploratory separation | The post-entry pathway comparison is in Appendix A and is not presented as an answer to RQ3. | **Pass** |
| Terminology | Fiscal year, research question, MWh/t, MWh, kW, t/day, MJ/kg, confidence interval, variance inflation factor, feed-in tariff, and artificial intelligence are explained at first substantive use. | **Pass** |
| Claim-evidence consistency | All numerical claims match machine-readable outputs and automated claim verification passes. | **Pass** |
| Source integrity | Journal manuscript and supplement hashes remain unchanged during this thesis-only pass. | **Pass** |
| PDF build | The professor-facing LaTeX source builds without errors. | **Pass: 45-page A4 PDF** |
| Visual quality | No cropped headers, clipped tables, overlapping text, blank spill pages, or illegible figures are found in a rendered-page audit. | **Pass** |
| Human linkage validation | A second person completes and adjudicates the blinded 558-pair clerical linkage packet. | **Open human-only gate** |
| Modeled-event verification | Official commissioning, procurement, equipment, or operator records verify the physical meaning of the 35 modeled administrative events. | **Open; supervisor decides whether pre-submission or post-thesis** |

## Supervisor decisions that are not coding defects

- Confirm whether the university or supervisor requires a particular wording or
  placement for the generative-AI disclosure.
- Confirm whether the public repository URL should remain in the submitted
  thesis or be replaced by a dated archival release.
- Decide whether Appendix A should remain in the final submitted thesis after
  professor feedback; it is intentionally excluded from the core RQs.
- Decide whether official-source verification of all 35 modeled events is
  required before submission or retained as a post-thesis evidence programme;
  the current outcome remains first reported administrative entry.

## Convergence rule

The thesis is professor-review ready when every automated and manuscript gate is
marked **Pass**. The independent clerical linkage review remains visibly open
until a human reviewer completes it. That open gate should not be rediscovered
and relabelled as a new manuscript defect in every review pass.
