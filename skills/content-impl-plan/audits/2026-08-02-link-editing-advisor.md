---
skill: content-impl-plan
date: 2026-08-02
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: skills/content-impl-plan/SKILL.md
after_ref: skills/content-impl-plan/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - skills/content-impl-plan/qa_checklist.md
  - skills/editing-advisor/evals/evals.json
eval_required: no
---

# Skill Audit

## Change

- Before: Selected editing elements could be mapped from Content Impl Plan
  directly to Remotion as editing/subtitle or motion moves.
- After: Complete editing element packets route through `editing-advisor` for
  compatibility decisions and an ordered timed recipe before renderer work.
- Why: The parent planner should preserve creative intent, while a focused
  advisor owns editorial composition and a renderer owns pixels.
- Tradeoff accepted: One additional handoff is required when editing elements
  are selected; non-editing plans do not incur it.

## First-Principles Reasoning

- Objective: Make accumulated editing techniques reliably reusable from the
  original production-planning path.
- Placement logic: Content Impl Plan maps elements; Editing Advisor composes
  editing decisions; Remotion implements and proves them.
- Expected behavior delta: Direct editing-element-to-renderer handoffs block.
- Proof needed: Advisor behavior evals, parent-route static check, skill checker,
  and reviewer receipt. The parent suite is not expanded because it already
  exceeds its enrolled surface budget.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | route, failure, todo, proof gate, and reference are first-load visible |
| `reference_load_precision` | pass | direct Reference Map route |
| `missing_context_rate` | pass | advisor provisional behavior covers incomplete downstream inputs |
| `noisy_context_rate` | pass | parent delta is route-local and reviewer accepted it |
| `duplicated_instruction_count` | pass | technique details remain in Resource Bank |
| `prompt_size_tokens` | pass | no new top-level todo or QA item; parent stays at baseline 19/19 debt |
| `task_success_rate` | pass | latest verdict for each advisor integration behavior is A |
| `review_tas_rate` | pass | independent reviewer TAS-A |
| `maintenance_locality` | pass | parent route plus focused QA/eval |
| `composition_clarity` | pass | planner -> advisor -> renderer chain is explicit |

## Proof Artifacts

- Skill-local evals, when needed: covered by
  `skills/editing-advisor/evals/evals.json`; parent suite intentionally unchanged
- Structure evals, when needed: canonical skill checker
- Reviewer receipt: independent scoped rereview, TAS-A, no hard-gate failures
- Validator: route/registry/query/JSON checks pass; Content Impl Plan's enrolled
  19-item QA and 19-eval surface debt is unchanged from HEAD
- Eval required: no new parent row; advisor behavior evals cover the handoff
- Evidence gaps: None for this scoped integration.

## Before Behavior

- Editing elements were present in the leverage map but had no required
  specialist composition step before Remotion.

## After Behavior

- The original Content Impl Plan chain visibly names and gates the Editing
  Advisor handoff before rendering.

## Followups

- None unless observed production plans reveal a missing editing method.
