---
date: 2026-06-12
change: phase-recursion-boundary
skill: plan
---

# Phase Recursion Boundary Audit

## Reason

`plan` had gained a review budget, which made ownership between planning and
review easy to confuse. The intended model is that every skill can perform Tier
0 phases inline, while callable phase skills are used only when a phase deserves
its own artifact, budget, handoff, independent judgment, or proof surface.

## Before

`plan` exposed `ReviewBudget`, which could imply that the plan skill owns review
judgment or recursive plan/review loops.

## After

`plan` exposes `PlanReviewRequest` and a `max_phase_depth` cap. `plan` owns the
decision to request review of a plan artifact; `review` owns the verdict. Any
externalized phase call must shrink or specialize the parent scope.

## Example

Allowed:

```text
plan(epic) -> epic_plan + review_request
review(epic_plan) -> findings
plan(revision_scope) -> smaller revised_todos
```

Invalid:

```text
plan(epic) -> review(epic_plan) -> plan(epic_review) -> review(...)
```

The invalid loop keeps the same parent scope and turns phase discipline into
ceremony.

## Proof

- `docs/skills/system.md` now owns the formal phase ownership and recursion
  invariant.
- `docs/fundamentals/harness-algebra.md` now models phase calls as inline or
  externalized functions with a scope-shrink condition.
- `skills/plan/SKILL.md` now returns `review_request?` instead of implying plan
  owns review.
- `skills/review/SKILL.md` now documents inline review planning and forbids
  same-scope recursive planning.
