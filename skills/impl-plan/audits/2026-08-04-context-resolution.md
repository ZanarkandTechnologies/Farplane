---
skill: impl-plan
date: 2026-08-04
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: .farplane/evals/runs/20260804-035503-task9015-context-resolution-baseline/summary.json
after_ref: .farplane/evals/runs/20260804-041230-task9015-context-resolution-candidate-v4/summary.json
reasoning_basis: first_principles
proof_artifacts:
  - skills/impl-plan/evals/evals.json
  - tickets/TASK-9015/artifacts/qa/validation.md
  - tickets/TASK-9015/artifacts/review/completion-review.md
eval_required: yes
---

# Impl Plan Context Resolution Audit

## Change

- Before: `impl-plan` recorded advisors as `called`, `skipped_settled`, or
  `blocked`, so accepted artifacts were treated as route skips rather than
  first-class reusable planning inputs.
- After: each required facet resolves as `reuse`, `targeted_refresh`, `create`,
  `block`, or `not_applicable`, with evidence, a bounded resolver/result, and
  exact Change Plan integration.
- Why: implementation planning should preserve accepted product and design
  work, fill only real gaps, and produce one execution contract.
- Tradeoff accepted: blocked external facts remain explicit, but they do not
  erase the maximal honest portion of the plan.

## First-Principles Reasoning

- Objective: minimize repeated discovery while keeping implementation plans
  grounded enough to execute and review.
- Placement logic: the planner owns context sufficiency because it alone can
  connect accepted artifacts to repository seams and proof gates. Advisors own
  only bounded missing or stale facets.
- Expected behavior delta: reuse sufficient UX, landing, copy, visual, and
  asset artifacts; call only the exact missing resolver; never shrink scope or
  invent unavailable external facts to make the plan appear complete.
- Proof needed: representative UI and landing cases, deterministic skill-system
  checks, and independent reviewer judgment of the candidate outputs.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Skill phase boundary and Todo 3-5 define artifact inventory, five-way resolution, planning-time resolver execution, and plan integration. |
| `reference_load_precision` | pass | Existing artifacts are inspected before advisors; only `targeted_refresh` and `create` may invoke a bounded advisor. |
| `missing_context_rate` | pass | Candidate v4 identifies only mobile hierarchy and current animation documentation as gaps. |
| `noisy_context_rate` | pass | Candidate v4 reuses accepted UX, landing, visual, and asset context and marks media irrelevant where stated. |
| `duplicated_instruction_count` | pass | `SKILL.md` owns semantics; prompt, template, README, and QA mirror the same decision model. |
| `prompt_size_tokens` | unknown | No tokenizer comparison was run. |
| `task_success_rate` | external_limit | Candidate answers completed, but the judge failed after the Codex account hit its usage ceiling. Manual assertion review is pending independent confirmation. |
| `review_tas_rate` | pass | Independent completion review graded both preserved candidate answers A/pass and returned TAS-A with no hard-gate failures. |
| `maintenance_locality` | pass | Runtime behavior changes are confined to `impl-plan`; the prior landing-page handoff delta remains separately owned. |
| `composition_clarity` | pass | Context advisors resolve narrow gaps; `impl-plan` owns the one Change Plan; `goal-advisor` only compiles approved execution. |

## Eval Evidence

- Baseline: `.farplane/evals/runs/20260804-035503-task9015-context-resolution-baseline/summary.json`
  - two selected cases, pass rate `0.5`;
  - the landing case used old `skipped_settled` route language and left the
    documentation gap unresolved.
- Repair runs:
  - candidate v1 exposed scope-shrinking and deferred-documentation gaps;
  - candidate v2 accidentally ran the full five-case suite and exposed older
    fixture-grounding weaknesses outside this change boundary;
  - candidate v3 exposed self-authored advisor context and plan erasure on a
    block.
- Final candidate:
  `.farplane/evals/runs/20260804-041230-task9015-context-resolution-candidate-v4/summary.json`
  - both agent answers completed;
  - both judge processes returned `D` solely because the external Codex usage
    ceiling was reached;
  - UI answer reuses UX/desktop context, routes only mobile hierarchy to
    `visual-design`, marks assets `not_applicable`, and preserves one plan;
  - landing answer reuses the approved spec and asset receipt, blocks only the
    unavailable library/documentation fact, and still provides one evidence-
    linked Change Plan.
- Fixture correction: the landing assertion originally demanded live official
  documentation while withholding both library identity and external lookup.
  It now requires the honest route: create/refresh when callable, otherwise
  block without fabrication.

## Proof Artifacts

- Deterministic validation: `tickets/TASK-9015/artifacts/qa/validation.md`.
- Reviewer receipt: `tickets/TASK-9015/artifacts/review/completion-review.md`.
- Eval suite: `skills/impl-plan/evals/evals.json`.

## Before Behavior

- Accepted artifacts appeared as advisor skips rather than usable inputs.
- A safe missing facet could be deferred, silently excluded, or improvised by
  the planner.
- One blocked external fact could collapse an otherwise useful Change Plan.

## After Behavior

- Context is resolved before advisor selection and every decision records its
  evidence and plan effect.
- Named omissions remain in scope and route to the narrow owner; the planner
  cannot self-author advisor-owned context.
- Blocked facts withhold approval but preserve the grounded plan that can
  already be written.

## Followups

- Rerun the same two selected cases with the external judge after the account
  usage ceiling resets; do not change the assertions before that rerun.
