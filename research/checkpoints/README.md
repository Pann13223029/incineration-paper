# Checkpoints

This directory documents how to freeze a sendable thesis milestone once the repo
has already passed the normal rebuild, verification, and packet workflow.

Generated artifacts are written to `research/checkpoints/dist/` and ignored in
Git. A stable local alias is also maintained at
`research/checkpoints/latest-sendable`, so you do not need to remember the
dated directory name during normal use.

## Command

```bash
npm run checkpoint:freeze
```

This command:

1. rebuilds the supervisor and submission packets from the current verified repo state
2. copies the packet ZIPs into a dated checkpoint directory
3. writes checkpoint metadata with the exact git SHA and packet hashes
4. refreshes `research/checkpoints/latest-sendable` to point at the newest frozen checkpoint
5. prints a suggested git tag for that sendable state

Optional local tag creation:

```bash
python3 code/scripts/12_freeze_checkpoint.py --create-tag
```

## Recommended use

- Use this only after a checkpoint is genuinely review-ready.
- Treat the checkpoint directory plus the git SHA as the auditable baseline you could send immediately.
- Use `research/checkpoints/latest-sendable` as the convenience path when you only want the newest frozen sendable state.
- Keep one clean `sendable-now` checkpoint alive even while you continue drafting on later commits.
