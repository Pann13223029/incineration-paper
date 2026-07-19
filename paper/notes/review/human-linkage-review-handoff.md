# Independent Human Linkage Review Handoff

Status: ready for an independent second reviewer. Human review has not yet been
completed, and this document does not change that status.

## Purpose

The thesis reconstructs administrative facility histories because official
facility codes are missing in FY2010-FY2012 and are completely recoded between
FY2019 and FY2020. This handoff tests whether a person who has not seen the
algorithmic decision can reach a defensible judgment from the visible record
pairs.

The review validates administrative-history linkage only. It cannot verify
unchanged ownership, physical equipment, commissioning, retrofit, closure, or
construction history.

## Files To Give The Reviewer

- `output/linkage_validation_packet.csv`
- this handoff document

Do not give the reviewer `output/linkage_validation_key.csv`, facility identity
crosswalks, match scores, simulation decisions, or algorithmic lineage labels.
The answer key is intentionally ignored by Git and remains separate from the
tracked packet.

## Required Review Standard

The strongest thesis standard is to review all 558 packet pairs. This removes
post-hoc sampling discretion and ensures that every modeled-event, uncertain,
fuzzy, gap, and FY2019-FY2020 bridge pair receives a human judgment.

If a supervisor authorizes a smaller review because of time constraints, the
sampling rule must be written and frozen before any decisions or answer-key
fields are examined. At minimum, it must include every modeled-event link,
every identity-uncertain link, and a prespecified blinded sample of the
remainder. Do not reduce the sample after difficult cases are encountered.

## Before Reviewing

1. Make a dated copy of `output/linkage_validation_packet.csv`. Never type into
   the generated packet.
2. Name the copy `linkage-review-REVIEWERID-YYYY-MM-DD.csv`.
3. Enter one stable reviewer identifier in `reviewer_id` for every reviewed row.
4. Hide the five selection columns while judging pairs:
   `modeled_event_link`, `identity_match_uncertain`, `fuzzy_link`, `gap_link`,
   and `fy2019_2020_bridge`.
5. Do not open the answer key, identity crosswalk, or simulation files.
6. Review the packet in its provided order or a random order chosen before
   seeing any pair. Do not prioritize apparently easy cases.

## Allowed Decisions

Enter exactly one of these values in `review_decision`:

- `same administrative facility history`
- `different facility history`
- `indeterminate from available evidence`
- `same lineage but probable asset/configuration reset`

Use `same administrative facility history` when the visible fields support one
continuing administrative history without a material reset signal.

Use `different facility history` when the names, municipality, timing, scale,
or configuration provide positive evidence for different histories. A minor
spelling or punctuation change alone is not sufficient.

Use `indeterminate from available evidence` when the visible fields do not
support a defensible same/different judgment. Do not guess to reduce the number
of unresolved cases.

Use `same lineage but probable asset/configuration reset` when the record still
appears to represent one administrative history but the reported start year,
capacity, furnace configuration, or naming pattern suggests a material reset.
This remains an administrative classification, not proof of physical
replacement.

## Other Reviewer Fields

- `review_confidence`: enter `high`, `medium`, or `low`.
- `same_lineage_but_asset_reset`: enter `TRUE` only for the probable-reset
  decision and `FALSE` for the other three decisions.
- `evidence_url`: leave blank unless an external municipal or Ministry source
  was actually consulted.
- `review_notes`: briefly record the decisive agreement, contradiction, or
  reason the pair is indeterminate. Do not reproduce algorithmic reasoning.

Missing values in source fields are absence of visible evidence, not evidence
that two histories are different.

## Locking The Independent Decisions

After the reviewer finishes:

1. Confirm that every reviewed row has `reviewer_id`, `review_decision`,
   `review_confidence`, and a valid reset flag.
2. Save and close the dated review copy.
3. Calculate and record its SHA-256 hash before opening the answer key. On macOS
   or Linux, run:

   ```bash
   shasum -a 256 linkage-review-REVIEWERID-YYYY-MM-DD.csv
   ```

4. Record the hash, reviewer identifier, completion date, and reviewed-row count
   in a signed or emailed review note.
5. Do not alter the locked review copy during adjudication.

## Adjudication

Only after the independent file is locked may the author or adjudicator compare
decisions with the separate answer key.

- Preserve the original reviewer decision verbatim.
- Put adjudication outcomes in a separate dated file.
- Resolve disagreements using visible administrative evidence first.
- For a modeled-event or identity-uncertain disagreement, seek an archived
  municipal or Ministry source and record its URL or archive reference.
- Retain `unresolved: external evidence required` when no adequate source exists.
- Never relabel an unresolved physical question as a confirmed retrofit,
  replacement, commissioning, opening, or closure.

## Completion Report

The final review report should state:

- reviewer identifier and review date
- SHA-256 hash of the locked decision file
- number and percentage of packet pairs reviewed
- exact four-category agreement with the algorithmic classification
- agreement after collapsing both same-history categories
- agreement by modeled-event, uncertain, fuzzy, gap, and bridge strata
- counts of same history, different history, probable reset, indeterminate, and
  unresolved adjudications
- every modeled-event disagreement and its resolution
- whether any adjudicated result changes a lineage, event definition, sample,
  coefficient, or thesis conclusion

Any changed lineage or modeled event requires rerunning the complete analysis,
claim verification, evidence synchronization, thesis build, and PDF audit.

## Prohibited Substitutes

- The synthetic reviewer simulation is not independent human validation.
- A generated blank packet is not completed validation.
- Author review alone is not independent validation.
- Agreement on aggregate counts cannot replace pair-level decisions.
- Opening the answer key before decisions are locked invalidates blinding.

The thesis acceptance gate remains open until the independent decisions are
locked, disagreements are adjudicated, and any resulting empirical changes are
recomputed.
