# Architecture

`harness-scout` is a composition skill, not a new data-acquisition or execution
runtime.

## Owned Surfaces

- `skills/harness-scout/`: workflow contract and scoring references
- `docs/features/registry.jsonl`: structured feature system of record
- `experiments/harness-scout/runs/`: source-run outputs and scorecards

## Upstream Inputs

- `summarize`: extracts source content
- `docs/features/registry.jsonl`: dedupe and local baseline
- `docs/specs/harness-techniques.md`: human-readable current inventory
- `skills/parity-research`: external convergence checks
- `skills/gap-analysis`: repo-specific missing-scope checks
- `skills/best-of-worlds`: multi-source synthesis

## Downstream Outputs

- decision matrix
- manual scorecard
- optional `impl-plan` ticket handoff
- optional feature registry update

## Boundaries

- no cron/feed polling
- no background Codex launchers
- no semantic memory or vector database
- no raw transcript promotion into durable docs
