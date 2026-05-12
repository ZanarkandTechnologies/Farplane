# Architecture

`harness-scout` is a composition skill, not a new data-acquisition or execution
runtime.

## Owned Surfaces

- `skills/harness-scout/`: workflow contract and scoring references
- `docs/sources/registry.jsonl`: structured source provenance and duplicate
  source identity
- `docs/features/registry.jsonl`: structured feature system of record
- `experiments/harness-scout/runs/`: source-run outputs and scorecards

## Upstream Inputs

- [summarize](../../summarize/SKILL.md): extracts source content
- `docs/sources/registry.jsonl`: source identity, provenance, and dedupe
- `docs/features/registry.jsonl`: dedupe and local baseline
- `docs/specs/harness-techniques.md`: human-readable current inventory
- [codebase-analysis](../../codebase-analysis/SKILL.md): checks local behavior
  when registry/docs search is inconclusive
- [external-patterns](../../external-patterns/SKILL.md): checks source repos or
  real implementation patterns
- [documentation](../../documentation/SKILL.md): checks official docs for
  platform, API, or standard claims
- [brainstorm](../../brainstorm/SKILL.md): explores alternate scout workflows
  when the operator asks for options
- [parity-research](../../parity-research/SKILL.md): external convergence
  checks
- [gap-analysis](../../gap-analysis/SKILL.md): repo-specific missing-scope
  checks
- [best-of-worlds](../../best-of-worlds/SKILL.md): multi-source synthesis
- [advise](../../advise/SKILL.md): judgement calls when evidence leaves a real
  decision

## Downstream Outputs

- decision matrix
- manual scorecard
- optional [autoresearch-plan](../../autoresearch-plan/SKILL.md) benchmark plan
- optional [self-improve](../../self-improve/SKILL.md) skill-eval follow-up
- optional [impl-plan](../../impl-plan/SKILL.md) ticket handoff
- optional [review](../../review/SKILL.md) quality gate
- optional feature registry update
- optional source registry update

## Boundaries

- no cron/feed polling
- no background Codex launchers
- no semantic memory or vector database
- no raw transcript promotion into durable docs
- no source registry records that duplicate `FEAT-*` technique ownership
