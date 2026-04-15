# Review Packets

This directory documents the curated packet workflows for supervisor review and eventual submission.
For any real checkpoint, this packet workflow is the default operating mode.

Generated artifacts are written to `research/packets/dist/` and ignored in Git.

## Commands

```bash
npm run packets:build
npm run supervisor:ready
```

`npm run packets:build`:

1. reruns the repo-level claim verifier
2. rebuilds `thesis/thesis.pdf` with `tectonic`, or reuses an already-current local `thesis/thesis.pdf` if `tectonic` is unavailable
3. assembles a frozen `supervisor-packet/`
4. assembles a frozen `submission-packet/`
5. writes zipped archives for both packets

`npm run supervisor:ready`:

1. reruns the full packet build
2. creates a flattened supervisor-only handoff at `research/packets/dist/supervisor-handoff/`
3. writes `research/packets/dist/supervisor-handoff.zip`
4. refreshes the stable local alias `research/packets/latest-supervisor-handoff`

The packet and handoff commands work from the current thesis source plus the generated manifests and output artifacts already in the repo. They are packaging and verification commands, not full analysis rebuild commands. If `tectonic` is missing, they can still proceed when `thesis/thesis.pdf` already exists and is current relative to `thesis.tex` and the figure files.

Use loose PDFs only while drafting. Once the thesis is sendable, review the packet contents and then freeze the milestone with `npm run checkpoint:freeze`.

## Packet types

### Supervisor packet

Optimized for fast review:

- one-page supervisor brief
- change summary since the last frozen checkpoint
- examiner risk register
- thesis PDF
- claim-verification report
- claim-to-evidence map
- sample definition and core outputs
- non-claims calibration note

### Supervisor handoff

Optimized for sending to a supervisor who should not need GitHub or repo context:

- `00_START_HERE.txt`
- thesis PDF with a plain filename
- one-page summary
- change summary since the last send
- main risks and mitigations
- key claims and evidence map
- non-claims note
- claim-verification report

Use the stable alias `research/packets/latest-supervisor-handoff` when you only want the newest sendable supervisor bundle.

### Submission packet

Optimized for a cleaner archival handoff:

- thesis PDF and `thesis.tex`
- change summary since the last frozen checkpoint
- examiner risk register
- thesis figures
- core defended analysis scripts
- claim-verification report and outputs
- claim-to-evidence map
- stage manifests
- reproduction and architecture docs
