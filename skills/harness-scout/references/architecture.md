# Architecture

`harness-scout` is a composition skill, not a new data-acquisition or execution
runtime.

## Owned Surfaces

- `skills/harness-scout/`: workflow contract and scoring references
- `docs/sources/registry.jsonl`: structured source provenance and duplicate
  source identity
- `docs/systems/*.md`: structured system source of record
- feature pages in `docs/features/`: structured feature source of record
- `docs/systems/registry.jsonl`: generated public system registry output
- `docs/features/registry.jsonl`: generated feature registry output
- `.farplane/harness-scout/runs/`: local source-run outputs and scorecards

## Upstream Inputs

- [summarize](../../summarize/SKILL.md): extracts source content
- `docs/sources/registry.jsonl`: source identity, provenance, and dedupe
- system/feature metadata and generated registries: dedupe and local
  baseline
- `docs/features/README.md`: human-readable current inventory
- [codebase-analysis](../../codebase-analysis/SKILL.md): checks local behavior
  when registry/docs search is inconclusive
- [external-patterns](../../external-patterns/SKILL.md): checks source repos or
  real implementation patterns
- [doc-advisor](../../doc-advisor/SKILL.md): checks official docs for
  platform, API, or standard claims
- [brainstorm](../../brainstorm/SKILL.md): explores alternate scout workflows
  when the operator asks for options
- [reference-grounding](../../reference-grounding/SKILL.md): compact evidence
  checks before scoring source claims
- [research:parity](../../research/SKILL.md#researchparity): external
  convergence checks
- [research:gap](../../research/SKILL.md#researchgap): repo-specific
  missing-scope checks
- [best-of-worlds](../../best-of-worlds/SKILL.md): multi-source synthesis
- [advise](../../advise/SKILL.md): judgement calls when evidence leaves a real
  decision

## Downstream Outputs

- decision matrix
- manual scorecard
- optional [metric-advisor](../../metric-advisor/SKILL.md) metric card
- optional [self-improve](../../self-improve/SKILL.md) skill-eval follow-up
- optional [impl-plan](../../impl-plan/SKILL.md) ticket handoff
- optional [review](../../review/SKILL.md) quality gate
- optional feature doc update plus generated registry refresh
- optional source registry update

## Boundaries

- no cron/feed polling
- no background Codex launchers
- no semantic memory or vector database
- no raw transcript promotion into durable docs
- no source registry records that duplicate `FEAT-*` technique ownership
