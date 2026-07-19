# Modeled-Event External Verification Handoff

Status: packet ready; external verification has not been completed. This is a
research protocol, not evidence that any reported entry is a physical project.

## Purpose

The primary entry model contains 35 first reported installed-capacity events.
The administrative workbooks identify the reporting transition but do not state
whether it represents initial installation, commissioning, replacement,
redevelopment, or correction of an earlier record. This review seeks external
official evidence for that physical interpretation without changing the model
outcome after seeing a preferred result.

## Build And Copy The Packet

Generate the blank packet with:

```bash
npm run review:build:event-verification
```

The command writes
`paper/notes/review/model-event-external-verification-packet.csv`. It must contain
exactly 35 unique facility-year rows. Before entering evidence, make a dated
copy named `model-event-verification-REVIEWERID-YYYY-MM-DD.csv`. Never type into
the generated blank packet.

## Source Priority

Use the strongest available source in this order:

1. Municipal procurement, council, environmental, facility, or budget records.
2. Ministry or prefectural administrative records.
3. Official operator, engineering contractor, or project documentation.
4. Archived versions of official pages or reports.
5. Reputable secondary reporting only as a search lead or clearly labelled
   supporting source.

Search the visible facility and municipality names for the event fiscal year
and at least two years on either side. Look separately for generation
installation, commissioning, redevelopment, replacement, retrofit, reporting,
and facility-name changes. Absence of a search result is not evidence that no
physical project occurred.

## Allowed Verification Statuses

Enter exactly one value in `verification_status`:

- `verified new generation installation or commissioning`
- `verified redevelopment or replacement with generation`
- `existing generation predates reported entry`
- `administrative or reporting transition without verified physical project`
- `conflicting external evidence`
- `unresolved from available evidence`

Use `verified` only when an official or comparably authoritative source names
the facility, the relevant generation equipment or project, and a date that can
be reconciled with the administrative event. A general municipal statement
about waste-to-energy is insufficient.

## Evidence Fields

- `reviewer_id`: one stable identifier for the researcher.
- `verified_event_year`: physical project or commissioning year stated by the
  source; leave blank if unresolved.
- `source_title`: exact document or page title.
- `source_publisher`: municipality, Ministry, operator, or other publisher.
- `source_url`: direct URL to the evidence, not a search-results page.
- `source_access_date`: ISO date in `YYYY-MM-DD` form.
- `archived_url`: stable archive URL when available.
- `evidence_locator`: page, table, section, or short locator; do not copy long
  passages.
- `review_notes`: explain how the source supports or contradicts the event.

Use additional rows in a separate source log when one event requires multiple
documents. Do not concatenate unrelated URLs into one cell.

## Locking And Adjudication

After all 35 events have a status:

1. Save and close the dated review file.
2. Record its SHA-256 hash with
   `shasum -a 256 model-event-verification-REVIEWERID-YYYY-MM-DD.csv`.
3. Preserve the locked file; put adjudication in a separate dated document.
4. Have the author and, where possible, a second reviewer examine conflicting
   and unresolved cases.
5. Retain the administrative model outcome unless a documented rule approved
   before adjudication requires reclassification.

## Thesis Decision Rules

- External evidence can refine the description of individual events, but it
  does not automatically create a causal treatment variable.
- A verified project date outside the reported event year demonstrates timing
  mismatch and must be disclosed rather than forced to match the workbook.
- If an event is reclassified or removed, rerun the complete analysis, claim
  verification, evidence synchronization, thesis build, and PDF audit.
- If verification is incomplete, keep the current term `first reported entry`
  and the existing limitation language.
- Do not report a verification percentage until every numerator, denominator,
  source rule, and unresolved category is documented.

The thesis remains valid as an administrative-transition study while this work
is open. Completing the packet would strengthen physical interpretation; it is
not a license to replace the observational design with causal project claims.
