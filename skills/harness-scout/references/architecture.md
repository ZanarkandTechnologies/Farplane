# Architecture

`harness-scout` is a composition skill, not a new data-acquisition or execution
runtime.

## Owned Surfaces

- `skills/harness-scout/`: workflow contract and scoring references
- `docs/features/registry.jsonl`: structured feature system of record
- `experiments/harness-scout/runs/`: source-run outputs and scorecards

## Upstream Inputs

- [summarize](../../summarize/SKILL.md): extracts source content
- `docs/features/registry.jsonl`: dedupe and local baseline
- `docs/specs/harness-techniques.md`: human-readable current inventory
- [parity-research](../../parity-research/SKILL.md): external convergence
  checks
- [gap-analysis](../../gap-analysis/SKILL.md): repo-specific missing-scope
  checks
- [best-of-worlds](../../best-of-worlds/SKILL.md): multi-source synthesis

## Downstream Outputs

- decision matrix
- manual scorecard
- optional [impl-plan](../../impl-plan/SKILL.md) ticket handoff
- optional feature registry update

## Boundaries

- no cron/feed polling
- no background Codex launchers
- no semantic memory or vector database
- no raw transcript promotion into durable docs
