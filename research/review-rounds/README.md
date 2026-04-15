# Review Rounds

This directory documents the intake workflow for supervisor or reviewer feedback after a packet has been sent.

Generated round workspaces are written to `research/review-rounds/dist/` and ignored in Git.

## Command

```bash
npm run review:round:start
```

This command:

1. reuses the current `supervisor-packet.zip` baseline, or rebuilds it only if missing
2. creates a dated local review-round directory
3. copies the exact `supervisor-packet.zip` used as the baseline
4. writes templates for comment intake, revision decisions, and a reply draft

## Recommended use

- Start a new round only after a real packet has been sent or is about to be discussed.
- Treat the copied `supervisor-packet.zip` as the exact baseline being reviewed.
- Record feedback in `feedback-intake.md` before changing the repo.
- Convert accepted or narrowed comments into concrete actions in `revision-decision-log.md`.
- Keep the round local and auditable even if the repo evolves afterward.
