# Review

TAS rubric verification for plans, implementations, skills, prompts, evals,
docs, UI evidence, demos, and integration readiness, with a repo-grounded
anti-slop search playbook for substantive review.

## Purpose

Turn review into a repeatable TAS pass with explicit family verdicts, skeptic
questions, and hard gates instead of generic questions, fake-precise scores, or
optimistic prose. The caller owns rubric routing through a reviewer handoff or
ticket `Proof Contract`; the actor using this contract starts from that routing,
validates it against the changed surface, then loads the named rubric families
and checks metric traceability against linked evidence.

## Public API or Entrypoints

- [`SKILL.md`](/Users/kenjipcx/coding-harness/Farplane/skills/review/SKILL.md): main review workflow
- `SKILL.md` Important Checklist: example natural-language todo template for review
- [`references/review-rubric-index.md`](/Users/kenjipcx/coding-harness/Farplane/skills/review/references/review-rubric-index.md): family selection map, shared TAS contract, and hard-gate policy
- [`references/reviewer-handoff.md`](/Users/kenjipcx/coding-harness/Farplane/skills/review/references/reviewer-handoff.md): reusable caller-to-reviewer handoff template
- [`references/desloppify.md`](/Users/kenjipcx/coding-harness/Farplane/skills/review/references/desloppify.md): cross-cutting anti-slop search playbook for neighboring-surface consistency checks
- [`references/spec-contract.md`](/Users/kenjipcx/coding-harness/Farplane/skills/review/references/spec-contract.md)
- [`references/implementation-plan.md`](/Users/kenjipcx/coding-harness/Farplane/skills/review/references/implementation-plan.md)
- [`references/code-quality.md`](/Users/kenjipcx/coding-harness/Farplane/skills/review/references/code-quality.md)
- [`references/ui-quality.md`](/Users/kenjipcx/coding-harness/Farplane/skills/review/references/ui-quality.md)
- [`references/user-intent-satisfaction.md`](/Users/kenjipcx/coding-harness/Farplane/skills/review/references/user-intent-satisfaction.md)
- [`references/evidence-quality.md`](/Users/kenjipcx/coding-harness/Farplane/skills/review/references/evidence-quality.md)
- [`references/demo-quality.md`](/Users/kenjipcx/coding-harness/Farplane/skills/review/references/demo-quality.md)
- [`references/video-quality.md`](/Users/kenjipcx/coding-harness/Farplane/skills/review/references/video-quality.md)
- [`references/integration-readiness.md`](/Users/kenjipcx/coding-harness/Farplane/skills/review/references/integration-readiness.md)
- [`references/skill-contract.md`](/Users/kenjipcx/coding-harness/Farplane/skills/review/references/skill-contract.md)
- [`references/prompt-quality.md`](/Users/kenjipcx/coding-harness/Farplane/skills/review/references/prompt-quality.md)
- [`references/eval-quality.md`](/Users/kenjipcx/coding-harness/Farplane/skills/review/references/eval-quality.md)
- [`references/debloatability.md`](/Users/kenjipcx/coding-harness/Farplane/skills/review/references/debloatability.md)
- [`/Users/kenjipcx/coding-harness/Farplane/agents/reviewer.toml`]: independent reviewer agent prompt

## Minimal Example

```text
Use the `SKILL.md` Important Checklist when invoking the skill.
Provide task context, changed files, evidence artifacts, and any declared
metrics, rubric families, required TAS gates, or hard gates.
Start from caller-declared families such as `code-quality`, `integration-readiness`, and `evidence-quality`.
Load `references/desloppify.md` because consistency and integration trust are in scope.
Search the changed files plus the smallest neighboring constants/docs/interfaces needed to test drift.
Use the family skeptic questions and assign TAS for each selected family.
Add `user-intent-satisfaction` when the ticket is clearly user-facing and the review needs to judge whether the delivered result actually satisfies the ask.
Return severity-ranked findings with concrete file refs.
Explain why the result is `TAS-A`, `TAS-B`, `TAS-C`, or `TAS-D`.
Return a clear `pass|revise|block|invalid` verdict grounded in the provided evidence artifacts.
```

## How to Test

- `git diff --check`
- `sed -n '1,120p' skills/review/SKILL.md`
  and expect a marker-delimited `## Important Checklist` with natural-language
  review steps
- `rg -n "reviewer-handoff|rubric_families|desloppify|search_scope|finding_log|severity|confidence|user-intent-satisfaction" skills/review/SKILL.md skills/review/README.md skills/review/references agents/reviewer.toml docs/specs/review-gates.md tickets/templates/ticket.md`
  and expect live matches in the updated review surfaces
- Run a stale numeric-review-contract scan over `skills/review`,
  `agents/reviewer.toml`, and `docs/specs/review-gates.md`; expect no live
  review-contract matches outside historical notes or unrelated schema versions.
- Manually verify that examples and TAS gates in `SKILL.md`,
  `references/review-rubric-index.md`, `references/desloppify.md`, and
  `docs/specs/review-gates.md` all use the same explicit TAS contract and
  search/output expectations
