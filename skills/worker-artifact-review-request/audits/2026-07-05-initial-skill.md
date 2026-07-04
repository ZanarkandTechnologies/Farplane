---
skill: worker-artifact-review-request
date: 2026-07-05
change_type: structure
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: no dedicated skill
after_ref: skills/worker-artifact-review-request/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - skills/worker-artifact-review-request/eval_task.json
  - skills/worker-artifact-review-request/qa_checklist.md
  - python3 skills/skill-maintenance/scripts/check_skills.py --write
eval_required: yes
---

# Skill Audit

## Change

- Before: Workers had to remember ad hoc Telegram review behavior from prompts
  or nearby workflow examples.
- After: A dedicated wrapper turns completed worker artifacts into
  phone-readable Telegram review requests with archive-safe refs and sent or
  fallback receipts.
- Why: Completed worker artifacts need a consistent Kenji review ping without
  creating a second approval queue or implying final-action permission.
- Tradeoff accepted: The skill is a thin wrapper over `telegram-message` rather
  than a new notification runtime.

## First-Principles Reasoning

- Objective: Make human review visible, replyable, and auditable when worker
  artifacts are ready.
- Placement logic: Telegram credential/routing remains owned by
  `telegram-message`; worker artifact packaging gets a small Tier 2 wrapper.
- Expected behavior delta: Artifact completion requires a review request or
  explicit fallback receipt.
- Proof needed: JSON eval syntax, skill registry validation, and reviewer
  judgment against TASK-0294.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Signature, gates, todos, templates, and output are in `SKILL.md`. |
| `reference_load_precision` | pass | Reference Map names when to load Telegram skill/checklist. |
| `missing_context_rate` | pass | Phone readability, reply route, side-effect boundary, and receipt gates are first-load. |
| `noisy_context_rate` | pass | `SKILL.md` is 155 lines. |
| `duplicated_instruction_count` | pass | Telegram details are linked, not copied wholesale. |
| `prompt_size_tokens` | pass | Under the rough 250-line guideline. |
| `task_success_rate` | unknown | Behavioral evals added but not run by an automated judge in this pass. |
| `review_tas_rate` | unknown | Pending completion review. |
| `maintenance_locality` | pass | Wrapper-specific behavior lives in one new skill package. |
| `composition_clarity` | pass | Inputs, outputs, state, routes, and fails are explicit. |

## Proof Artifacts

- Skill-local evals, when needed: `skills/worker-artifact-review-request/eval_task.json`.
- Structure evals, when needed: `python3 skills/skill-maintenance/scripts/check_skills.py --write`.
- Reviewer receipt: pending.
- Validator: `python3 skills/skill-maintenance/scripts/check_skills.py --write` passed.
- Eval required: yes; initial cases cover local-path-only, receipt, and content review behavior.
- Evidence gaps: This pass does not send a real Telegram message.

## Before Behavior

- A finished worker could leave only a local artifact path and no review ping.

## After Behavior

- A finished worker must send or record a phone-readable review request with
  message id/fallback receipt and side-effect boundary.

## Followups

- Add a live behavior test after a worker thread completes a real artifact.
