---
skill: pulse-update
date: 2026-07-05
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: skills/pulse-update/SKILL.md before TASK-0294 implementation
after_ref: skills/pulse-update/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - skills/pulse-update/eval_task.json
  - python3 skills/skill-maintenance/scripts/check_skills.py --write
eval_required: yes
---

# Skill Audit

## Change

- Before: Pulse could treat human review as a reason to idle/request planning,
  and worker handoffs did not consistently require Telegram artifact review
  receipts.
- After: Pulse first scans safe local prep work, uses the ticket opportunity
  generator for bold product-backed ticket waves, and requires review
  notification instructions plus sent/fallback receipts for completed artifacts.
- Why: Autonomy should keep useful throughput high while irreversible actions
  stay gated.
- Tradeoff accepted: The first-load skill remains long because Pulse is the
  manager contract for board admission, next-wave creation, and worker state.

## First-Principles Reasoning

- Objective: Make Pulse behave like a manager with workers, not a parent thread
  that no-ops behind approvals or implements tickets inline.
- Placement logic: Pulse owns worker portfolio, queue refill, handoffs, and
  idle behavior; the generator owns idea quality.
- Expected behavior delta: Waiting review workers stay open, review reminders
  are routed through a worker wrapper, and safe product-backed work continues.
- Proof needed: JSON eval syntax, skill registry validation, and reviewer
  judgment against TASK-0294.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Context, signature, modes, and todos include idle/review/handoff rules. |
| `reference_load_precision` | pass | New route links directly to the wrapper skill and Telegram primitive. |
| `missing_context_rate` | pass | Safe-local-prep scan and review receipt gates are first-load. |
| `noisy_context_rate` | unknown | File is 561 lines; reviewer should judge bloat separately. |
| `duplicated_instruction_count` | pass | Repeated rules appear in context, gates, todo, and mode output intentionally. |
| `prompt_size_tokens` | unknown | Long before this change and longer after; accepted for now due manager role. |
| `task_success_rate` | unknown | Behavioral evals added but not run by an automated judge in this pass. |
| `review_tas_rate` | unknown | Pending completion review. |
| `maintenance_locality` | pass | Pulse-specific behavior lives in Pulse skill/eval and framework doc. |
| `composition_clarity` | pass | Routes and outputs name worker-artifact-review-request and Telegram receipts. |

## Proof Artifacts

- Skill-local evals, when needed: `skills/pulse-update/eval_task.json`.
- Structure evals, when needed: `python3 skills/skill-maintenance/scripts/check_skills.py --write`.
- Reviewer receipt: pending.
- Validator: `python3 skills/skill-maintenance/scripts/check_skills.py --write` passed.
- Eval required: yes; cases added for final-action gate idle and review notification receipt.
- Evidence gaps: No live heartbeat run is part of this ticket.

## Before Behavior

- Human-gated final action could cause `request_planning` or no-op despite safe
  local work being available.

## After Behavior

- Pulse leaves the waiting worker open, sends/records a review request when
  appropriate, and continues with safe local prep or product-backed ticket waves.

## Followups

- Consider a separate compaction pass for Pulse first-load length after the
  behavior is stable.
