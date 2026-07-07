---
skill: dogfood-review
date: 2026-07-07
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: skills/dogfood-review/SKILL.md
after_ref: skills/dogfood-review/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - tickets/TASK-0313/ticket.md
  - tickets/TASK-0313/artifacts/sample-dogfood-improvement-ticket-output.md
  - tickets/TASK-0313/artifacts/reviewer-receipt.md
  - skills/dogfood-review/eval_task.json
  - skills/dogfood-review/qa_checklist.md
  - skills/dogfood-review/templates/dogfood-report.md
eval_required: yes
---

# Skill Audit

## Change

- Before: `dogfood-review` produced a dated report and interval summary, but
  actionable repair work stayed report-only.
- After: material tracked-feature reports must include exactly one consolidated
  improvement ticket path or complete candidate, with a no-autostart receipt.
- Why: dogfood findings should close into visible board work without creating
  one ticket per feature or starting implementation implicitly.
- Tradeoff accepted: the report template is slightly longer so the ticket
  writeback contract stays inspectable without turning Daily into the owner of
  dogfood logic.

## First-Principles Reasoning

- Objective: turn reviewer-backed dogfood findings into durable improvement
  work while preserving explicit invocation boundaries.
- Placement logic: `dogfood-review` owns converting its own findings into one
  ticket path or candidate; `interval-update` only surfaces that output.
- Expected behavior delta: material tracked-feature reports now expose the
  follow-up ticket artifact and record that no execution was triggered.
- Proof needed: skill validator, JSON eval validation, feature registry
  validation, ticket metadata validation, sample output, and reviewer lane.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` signature, gates, todos, fails, and output name the one-ticket/no-autostart contract. |
| `reference_load_precision` | pass | Detailed report shape stays in `templates/dogfood-report.md`; interval details stay in interval references. |
| `missing_context_rate` | pass | Ticket path/candidate, reviewer TAS, track checklist, evidence refs, and skipped refs are required. |
| `noisy_context_rate` | pass | Ticket detail is grouped in one report section and one candidate instead of per-feature ticket spam. |
| `duplicated_instruction_count` | pass | Interval only surfaces the dogfood output and does not duplicate ticket construction logic. |
| `prompt_size_tokens` | pass | First-load text grew for a new output contract; bulky field shape remains in the template. |
| `task_success_rate` | unknown | Needs future live dogfood run after install/sync. |
| `review_tas_rate` | pass | Reviewer rereview passed the blocking integration finding at TAS-A; see `tickets/TASK-0313/artifacts/reviewer-receipt.md`. |
| `maintenance_locality` | pass | Changes are local to dogfood-review and interval-update caller surface. |
| `composition_clarity` | pass | Signature exposes `write_policy`, optional ticket writeback, and no-autostart receipt. |

## Proof Artifacts

- Skill-local evals, when needed: `skills/dogfood-review/eval_task.json`.
- Structure evals, when needed: `python3 skills/skill-maintenance/scripts/check_skills.py --write`.
- Reviewer receipt: `tickets/TASK-0313/artifacts/reviewer-receipt.md`.
- Validator:
  - `python3 docs/features/validate_features.py`
  - `python3 -m json.tool skills/dogfood-review/eval_task.json`
  - `python3 -m json.tool skills/interval-update/eval_task.json`
  - `python3 skills/skill-maintenance/scripts/check_skills.py --write`
  - `python3 tickets/scripts/check_ticket_metadata.py tickets/TASK-0313/ticket.md`
- Eval required: yes; future eval execution should exercise candidate and
  explicit ticket-writeback modes.
- Evidence gaps: live installed automation was not synced in this task.

## Before Behavior

- A dogfood report could recommend repair work but had no required board
  writeback artifact.
- Interval could link the report without surfacing a concrete improvement
  ticket path or candidate.

## After Behavior

- A material tracked-feature dogfood report includes one improvement ticket path
  or complete candidate, grouped by feature and cross-cutting repairs.
- The report and interval summary carry a no-autostart receipt so ticket
  creation remains distinct from implementation.

## Followups

- Run a live dogfood review after the next source install/sync and verify Daily
  links the created ticket path or candidate.
