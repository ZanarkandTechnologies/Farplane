---
skill: impl-plan
date: 2026-06-23
change_type: behavior
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/impl-plan/SKILL.md@plan-only-approval
after_ref: skills/impl-plan/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - skills/impl-plan/SKILL.md
  - skills/impl-plan/references/template.md
  - skills/impl-plan/prompts/plan.md
  - skills/impl-plan/qa_checklist.md
  - skills/goal-advisor/SKILL.md
  - skills/goal-advisor/references/prompt-templates.md
  - skills/goal-advisor/qa_checklist.md
eval_required: no
---

# Skill Audit

## Change

- Before: `impl-plan` approved the ticket plan and handed off to
  `goal-advisor`, leaving the compiled Goal Packet as a later review surface.
- After: Goal-backed `impl-plan` output includes a `goal-advisor`-compiled Goal
  Packet preview so the human can approve the ticket plan and execution packet
  together.
- Why: hidden post-approval `program.md`, `progress.md`, and native `/goal`
  prompts are another source of mistakes.
- Tradeoff accepted: one extra compile step during planning, but no extra
  orchestration step after approval.

## First-Principles Reasoning

- Objective: let the operator approve the complete execution contract once.
- Placement logic: `impl-plan` owns the approval artifact; `goal-advisor` owns
  compiling the packet; native Goal owns execution after approval.
- Expected behavior delta: if the plan changes, `goal-advisor` regenerates the
  packet before execution instead of running a stale packet.
- Proof needed: source diff, checklist updates, validator, and installed-copy
  inspection.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `impl-plan/SKILL.md` gates now include missing-input resolution, Goal Packet preview, and approval before Goal run. |
| `reference_load_precision` | pass | `template.md` owns detailed Goal Packet preview shape; `qa_checklist.md` owns acceptance checks. |
| `missing_context_rate` | pass | Clarifying-question policy, packet preview, and regeneration after plan change are first-load visible. |
| `noisy_context_rate` | pass | The detailed packet structure lives in `references/template.md`, not expanded into the Todo List. |
| `duplicated_instruction_count` | pass | `impl-plan` defines the approval need; `goal-advisor` defines packet compilation and pause-before-run. |
| `prompt_size_tokens` | pass | The new behavior adds compact gates without returning to the old bloated first-load shape. |
| `task_success_rate` | unknown | No live plan-to-goal run artifact yet. |
| `review_tas_rate` | unknown | No reviewer receipt requested for this targeted workflow contract edit. |
| `maintenance_locality` | pass | Future changes split cleanly between `impl-plan` approval shape and `goal-advisor` packet compilation. |
| `composition_clarity` | pass | Inputs, gates, routes, output, and next owner are explicit. |

## Proof Artifacts

- Skill-local evals, when needed: not changed.
- Structure evals, when needed: checklist self-review.
- Reviewer receipt: skipped; targeted behavior contract change.
- Validator: `python3 scripts/check_skills.py --write` from
  `skills/skill-maintenance`.
- Eval required: no.
- Evidence gaps: no live transcript proves the new one-shot approval path yet.

## Before Behavior

- Human approval could happen before seeing the actual Goal Packet.

## After Behavior

- Human approval covers both the ticket plan and Goal Packet preview; changed
  plans force `goal-advisor` regeneration before run.

## Followups

- Add an eval case if future agents still run Goal Packets without showing the
  packet preview first.
