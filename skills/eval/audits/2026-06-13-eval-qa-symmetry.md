---
skill: eval
date: 2026-06-13
change_type: behavior
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/eval/SKILL.md
after_ref: skills/eval/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - docs/fundamentals/harness-algebra.md
  - skills/eval/SKILL.md
  - skills/skill-maintenance/SKILL.md
eval_required: no
---

# Eval QA Symmetry Audit

## Change

- Before: `eval` owned skill-local `eval_task.json` files and reference points,
  but did not name what to do when reference points became reusable runtime
  guardrails.
- After: `eval` routes that writeback through `skill-maintenance` to update the
  owning skill's checklist reference, final QA checklist, or validator/hook
  candidate.
- Why: eval cases and todo checklists converge only after the behavior contract
  is known; the writeback owner should be the skill maintenance surface, not the
  eval runner.
- Tradeoff accepted: this adds one todo item to `eval` instead of automatic
  checklist generation.

## First-Principles Reasoning

- Objective: preserve eval reference points as reusable execution guardrails
  when they become stable.
- Placement logic: `eval` owns expected behavior cases; `skill-maintenance`
  owns skill-local checklist and reference updates.
- Expected behavior delta: after changing a skill eval, agents check whether any
  reference point should be promoted into runtime QA or checklist language.
- Proof needed: structure validation and review of the changed skill todo.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | The sync instruction is in the first-load todo list. |
| `reference_load_precision` | pass | Detailed theory lives in `docs/fundamentals/harness-algebra.md`. |
| `missing_context_rate` | pass | The todo names the owner skill and target artifacts. |
| `noisy_context_rate` | pass | One line adds only the writeback condition. |
| `duplicated_instruction_count` | pass | `eval` routes writeback; `skill-maintenance` owns details. |
| `prompt_size_tokens` | pass | No long examples or rubric bodies were added to `SKILL.md`. |
| `task_success_rate` | unknown | No eval run was needed for this policy-only change. |
| `review_tas_rate` | unknown | No reviewer lane was required for this narrow self-check. |
| `maintenance_locality` | pass | The behavior change is in the owning `eval` skill package. |
| `composition_clarity` | pass | The handoff chain is explicit: eval to skill-maintenance to QA/reviewer. |

## Proof Artifacts

- Skill-local evals, when needed: not required; no task behavior changed.
- Structure evals, when needed: not required.
- Reviewer receipt: not required for this narrow sync rule.
- Validator: pending command result in final work summary.
- Eval required: no.
- Evidence gaps: no live run proved whether agents will remember the handoff.

## Before Behavior

- Eval reference points could harden into standards without a named durable
  checklist writeback step.

## After Behavior

- Stable, reusable eval reference points are candidates for skill-local QA
  checklist or validator promotion through `skill-maintenance`.

## Followups

- Consider a future eval case that checks whether agents perform this writeback
  after materially changing a skill's `eval_task.json`.
