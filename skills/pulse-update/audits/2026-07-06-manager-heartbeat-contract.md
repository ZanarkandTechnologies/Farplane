---
skill: pulse-update
date: 2026-07-06
change_type: structure
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: skills/pulse-update/SKILL.md at 572 lines before TASK-0302 edits
after_ref: skills/pulse-update/SKILL.md at 478 lines after TASK-0302 edits
reasoning_basis: first_principles
proof_artifacts:
  - tickets/TASK-0302/ticket.md
  - tickets/TASK-0302/program.md
  - tickets/TASK-0302/progress.md
eval_required: yes
---

# Pulse Update Manager Heartbeat Contract Audit

## Change

- Before: `pulse-update` repeated detailed doctrine for ticket quality,
  product-lane artifacts, worker review notifications, and execution handoff
  behavior that already belonged to owner skills.
- After: `pulse-update` keeps the manager heartbeat contract and routes detailed
  ticket spec quality to `plan-next-wave`, artifact workflow
  contracts to product skills, execution compilation to `goal-advisor`, and
  Telegram artifact-review details to `worker-artifact-review-request`.
- Why: Pulse had become harder to maintain because the caller surface carried
  too much downstream workflow detail. The leaner contract should preserve
  autonomy gates while making owner boundaries obvious.
- Tradeoff accepted: Pulse now depends more explicitly on owner-skill contracts;
  evals and reviewer checks are the backstop against hiding required gates.

## First-Principles Reasoning

- Objective: Keep autonomous Pulse throughput high while reducing first-load
  burden and duplicated ownership.
- Placement logic: Keep manager decisions, gates, modes, state writeback, and
  handoff receipts in `pulse-update`; keep detailed ticket and review contracts
  in owner skills.
- Expected behavior delta: Future agents should read Pulse as a manager loop
  rather than as the full doctrine for products, tickets, execution, and
  Telegram review.
- Proof needed: skill-system validation, JSON parse checks, ticket metadata
  check, line-count audit, owner-boundary grep, and reviewer gate before final
  completion.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Pulse still has signature, modes, gates, todos, routes, output contract, and writeback requirements. |
| `reference_load_precision` | pass | Pulse links `plan-next-wave` and `worker-artifact-review-request` at the owner handoff points. |
| `missing_context_rate` | pass | TASK-0294 hard gates remain represented in Pulse, generator, review-request, and evals. |
| `noisy_context_rate` | pass | Pulse first-load reduced from 572 to 478 lines by removing repeated downstream detail. |
| `duplicated_instruction_count` | pass | Detailed ticket spec fields now point to the generator owner; Telegram message detail points to review-request owner. |
| `prompt_size_tokens` | pass | Line count dropped by 94 lines while preserving hard gates. |
| `task_success_rate` | unknown | No live Pulse automation run was performed in this ticket. |
| `review_tas_rate` | unknown | Reviewer receipt pending. |
| `maintenance_locality` | pass | Future ticket-spec quality edits belong to generator; worker review message edits belong to worker-review skill. |
| `composition_clarity` | pass | Manager flow, generator flow, worker-review flow, and Goal execution flow are explicit in ticket/program/docs. |

## Proof Artifacts

- Skill-local evals, when needed: `skills/pulse-update/eval_task.json` now
  includes `pulse_stays_manager_while_owner_skills_hold_detail`.
- Structure evals, when needed: `python3 skills/skill-maintenance/scripts/check_skills.py --write`.
- Reviewer receipt: pending `tickets/TASK-0302/artifacts/review/<timestamp>-planning-review.json`.
- Validator:
  - `python3 -m json.tool skills/pulse-update/eval_task.json`
  - `python3 -m json.tool skills/plan-next-wave/eval_task.json`
  - `python3 -m json.tool skills/worker-artifact-review-request/eval_task.json`
  - `python3 tickets/scripts/check_ticket_metadata.py tickets/TASK-0302/ticket.md`
- Eval required: yes.
- Evidence gaps: no live Pulse run; reviewer gate pending.

## Before Behavior

- Pulse first-load repeated concrete generator fields such as big claim,
  audience tension, surprise factor, dedupe status, artifact level, and review
  surface.
- Pulse handoff prose repeated Telegram-first review details that
  `worker-artifact-review-request` already owns.
- Maintainers could reasonably think Pulse owned ticket planning, product
  workflow contracts, and review-message wording.

## After Behavior

- Pulse remains responsible for board/worker reconciliation, proceedable ticket
  admission, mode choice, safe next-wave routing, worker handoff creation or
  recording, and decision/reward/report writeback.
- `plan-next-wave` is explicitly the detailed owner for
  executable ticket spec quality.
- `worker-artifact-review-request` is explicitly the detailed owner for
  Telegram-first worker artifact review.
- The framework doc includes the lean owner graph.

## Followups

- Run reviewer gate before closing TASK-0302.
- Only restore duplicated Pulse detail if evals or reviewer findings show an
  owner-pointer version is too weak to prevent a known regression.
