# Review

Rubric-driven verification for plans, code, UI, evidence, demos, and integration readiness, with a repo-grounded anti-slop search playbook for substantive review.

## Purpose

Turn review into a repeatable scoring pass with an explicit `1.0`-to-`5.0`
contract, skeptic questions, and hard thresholds instead of generic questions
or optimistic prose. The reviewer starts from the active ticket's `Proof
Contract` when present, then loads the named rubric families and checks metric
traceability against linked evidence.

## Public API or Entrypoints

- [`SKILL.md`](/Users/kenjipcx/coding-harness/Codexter/skills/review/SKILL.md): main review workflow
- [`todos.md`](/Users/kenjipcx/coding-harness/Codexter/skills/review/todos.md): example natural-language todo template for review
- [`references/review-rubric-index.md`](/Users/kenjipcx/coding-harness/Codexter/skills/review/references/review-rubric-index.md): family selection map, shared score contract, and threshold policy
- [`references/desloppify.md`](/Users/kenjipcx/coding-harness/Codexter/skills/review/references/desloppify.md): cross-cutting anti-slop search playbook for neighboring-surface consistency checks
- [`references/spec-contract.md`](/Users/kenjipcx/coding-harness/Codexter/skills/review/references/spec-contract.md)
- [`references/implementation-plan.md`](/Users/kenjipcx/coding-harness/Codexter/skills/review/references/implementation-plan.md)
- [`references/code-quality.md`](/Users/kenjipcx/coding-harness/Codexter/skills/review/references/code-quality.md)
- [`references/ui-quality.md`](/Users/kenjipcx/coding-harness/Codexter/skills/review/references/ui-quality.md)
- [`references/user-intent-satisfaction.md`](/Users/kenjipcx/coding-harness/Codexter/skills/review/references/user-intent-satisfaction.md)
- [`references/evidence-quality.md`](/Users/kenjipcx/coding-harness/Codexter/skills/review/references/evidence-quality.md)
- [`references/demo-quality.md`](/Users/kenjipcx/coding-harness/Codexter/skills/review/references/demo-quality.md)
- [`references/video-quality.md`](/Users/kenjipcx/coding-harness/Codexter/skills/review/references/video-quality.md)
- [`references/integration-readiness.md`](/Users/kenjipcx/coding-harness/Codexter/skills/review/references/integration-readiness.md)
- [`references/debloatability.md`](/Users/kenjipcx/coding-harness/Codexter/skills/review/references/debloatability.md)
- [`/Users/kenjipcx/coding-harness/Codexter/agents/code-reviewer.toml`]: specialist review agent prompt

## Minimal Example

```text
Use `review` on the active ticket.
Read `todos.md` if using skill todos.
Read the ticket Proof Contract for declared metrics, rubric gates, hard gates, and required evidence.
Select `code-quality`, `integration-readiness`, and `evidence-quality`.
Load `references/desloppify.md` because consistency and integration trust are in scope.
Search the changed files plus the smallest neighboring constants/docs/interfaces needed to test drift.
Use the family skeptic questions and score each family on the anchored 1.0-5.0 scale.
Add `user-intent-satisfaction` when the ticket is clearly user-facing and the review needs to judge whether the delivered result actually satisfies the ask.
Return severity-ranked findings with concrete file refs.
Explain why the result is not a lower or higher adjacent band.
Return a linked review artifact and clear `pass|revise|block` verdict grounded in the ticket `Evidence` artifacts.
```

## How to Test

- `git diff --check`
- `sed -n '1,80p' skills/review/todos.md`
  and expect a plain `# Todos` checklist with natural-language review steps
- `rg -n "desloppify|search_scope|finding_log|severity|confidence|user-intent-satisfaction" skills/review/SKILL.md skills/review/README.md skills/review/references agents/code-reviewer.toml docs/specs/review-gates.md tickets/templates/ticket.md`
  and expect live matches in the updated review surfaces
- `rg -n "interpolation points|interpolation-style|2\\.0 and 4\\.0 are interpolation|2 and 4 are interpolation" skills/review/SKILL.md skills/review/AGENTS.md skills/review/references agents/code-reviewer.toml docs/specs/review-gates.md tickets/templates/ticket.md`
  and expect no live matches
- Manually verify that examples and thresholds in `SKILL.md`,
  `references/review-rubric-index.md`, `references/desloppify.md`, and
  `docs/specs/review-gates.md` all use the same explicit `1.0`-to-`5.0`
  contract and search/output expectations
