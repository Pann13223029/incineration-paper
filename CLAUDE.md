# CLAUDE.md

Compatibility wrapper for tools that automatically read `CLAUDE.md`.

## Canonical Repo Guidance

Read and follow [AGENTS.md](AGENTS.md). It is the assistant-agnostic source of
truth for:

- source-of-truth rules
- workflow and sync expectations
- build and verification guidance
- panel-workflow usage
- durable repo quality standards

If `CLAUDE.md` and `AGENTS.md` ever disagree, `AGENTS.md` wins.

## Claude-Specific Adapter

- No additional Claude-only repo rules are required beyond `AGENTS.md`.
- Do not store volatile project facts, sample sizes, readiness claims, or
  workflow state in this file.
- Keep this file thin; project policy should live in `AGENTS.md`.
