# Review Packets

This directory documents the curated packet workflows for supervisor review and eventual submission.
For any real checkpoint, this packet workflow is the default operating mode.

Generated artifacts are written to `research/packets/dist/` and ignored in Git.

## Commands

```bash
npm run packets:build
```

This command:

1. reruns the repo-level claim verifier
2. rebuilds `thesis/thesis.pdf` with `tectonic`
3. assembles a frozen `supervisor-packet/`
4. assembles a frozen `submission-packet/`
5. writes zipped archives for both packets

Use loose PDFs only while drafting. Once the thesis is sendable, review the packet contents and then freeze the milestone with `npm run checkpoint:freeze`.

## Packet types

### Supervisor packet

Optimized for fast review:

- one-page supervisor brief
- thesis PDF
- claim-verification report
- sample definition and core outputs
- non-claims calibration note

### Submission packet

Optimized for a cleaner archival handoff:

- thesis PDF and `thesis.tex`
- thesis figures
- core defended analysis scripts
- claim-verification report and outputs
- stage manifests
- reproduction and architecture docs
