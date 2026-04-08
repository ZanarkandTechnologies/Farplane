# Review

Rubric-driven verification for plans, code, UI, evidence, demos, and integration readiness.

## Purpose

Turn review into a repeatable scoring pass with explicit 1-to-5 anchors and hard thresholds instead of generic questions or optimistic prose.

## Public API or Entrypoints

- [`SKILL.md`](/Users/kenjipcx/coding-harness/Codexter/skills/review/SKILL.md): main review workflow
- [`references/review-rubric-index.md`](/Users/kenjipcx/coding-harness/Codexter/skills/review/references/review-rubric-index.md): family selection map and threshold policy
- [`references/spec-contract.md`](/Users/kenjipcx/coding-harness/Codexter/skills/review/references/spec-contract.md)
- [`references/implementation-plan.md`](/Users/kenjipcx/coding-harness/Codexter/skills/review/references/implementation-plan.md)
- [`references/code-quality.md`](/Users/kenjipcx/coding-harness/Codexter/skills/review/references/code-quality.md)
- [`references/ui-quality.md`](/Users/kenjipcx/coding-harness/Codexter/skills/review/references/ui-quality.md)
- [`references/evidence-quality.md`](/Users/kenjipcx/coding-harness/Codexter/skills/review/references/evidence-quality.md)
- [`references/demo-quality.md`](/Users/kenjipcx/coding-harness/Codexter/skills/review/references/demo-quality.md)
- [`references/video-quality.md`](/Users/kenjipcx/coding-harness/Codexter/skills/review/references/video-quality.md)
- [`references/integration-readiness.md`](/Users/kenjipcx/coding-harness/Codexter/skills/review/references/integration-readiness.md)
- [`references/debloatability.md`](/Users/kenjipcx/coding-harness/Codexter/skills/review/references/debloatability.md)
- [`/Users/kenjipcx/coding-harness/Codexter/agents/code-reviewer.toml`]: specialist review agent prompt

## Minimal Example

```text
Use `review` on the active ticket.
Select `code-quality`, `integration-readiness`, and `evidence-quality`.
Score each family on the anchored 1.0-5.0 scale.
Return a `Review Packet` with a clear `pass|revise|block` verdict.
```

## How to Test

- `git diff --check`
- `rg -n "skills/code-review|../code-review|rubric-anchors" skills/review agents/code-reviewer.toml docs/specs/review-gates.md tickets/templates/ticket.md`
  and expect no live matches beyond intentional historical wording in the review module docs
- Manually verify that examples and thresholds in `SKILL.md`, `references/review-rubric-index.md`, and `docs/specs/review-gates.md` all use the same `1.0`-to-`5.0` contract
