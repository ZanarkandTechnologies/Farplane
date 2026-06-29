---
template_id: ticket-template
template_version: "0.1.1"
ticket_id: TASK-0240
title: Taste Loop social thread proposal worker
phase: building
status: building
owner: codex
claimed_by: codex-taste-loop-controller
priority: medium
depends_on:
  - TASK-0237
blocked_by: []
ready: true
approval_required: false
requires_qa: true
requires_demo: false
created_at: 2026-06-27T22:50:30+08:00
updated_at: 2026-06-29T22:35:00+08:00
next_action: wait for Kenji's current planning-hypothesis feedback; if he selects A/B/C then draft only after approval, otherwise append feedback, learning, and the next hypothesis to progress.md until explicit stop, blocker, convergence, or budget exhaustion
last_verification: current planning-hypothesis reminder sent via Telegram message 2283 from the reused visible worker thread with artifact-first framing; program now treats progress.md as the hypothesis ledger rather than creating fresh TL experiment labels
---

# TASK-0240: Taste Loop social thread proposal worker

## Summary

Run one Goal-backed Taste Loop worker for the `trust_distribution/social_thread`
workflow. The worker should start with detailed TasteProposal planning for the
AGI Toy Shop scenario and ask Kenji for idea feedback before spending effort on
execution.

## Scope

- In:
  - Use `farplane/products.md` workflow `social_thread`.
  - Use owner route `social-content:twitter-thread`.
  - Use `tickets/TASK-0237/artifacts/agi-toy-shop-scenario.md` unless a better
    live context is explicitly supplied.
  - Create one to three TasteProposal entries as the planning artifact.
  - Use `optimize-with-human` with `phases=planning,execution`.
  - Log planning and execution hypothesis cycles in `progress.md`.
  - Route Telegram or fallback feedback from the dedicated worker thread, not
    the parent controller thread.
- Out:
  - No public posting, publishing, spend, or external account mutation.
  - No target-skill hardening from a first rejection.
  - No execution artifact until a concept passes, unless a tiny artifact is
    explicitly serving as the planning test.

## Delta

- `Before:` Taste Loop has one valid open execution feedback item for
  `landing_page_offer` and legacy broad-skill cards that no longer count
  against budget.
- `After:` Taste Loop has a dedicated worker path for the next eligible
  product-lane workflow, `social_thread`, with ticket/program/progress state.
- `Why now:` Manual operator invocation requested one real bounded beat and
  explicitly bypassed the time-of-day gate.

## Program

```text
workflow:
  product_lane: trust_distribution
  workflow_id: social_thread
  owner: social-content:twitter-thread
  planning_artifact: TasteProposal batch
  execution_artifact: draft thread
  feedback_question: pick A/B/C, revise, or reject the proposal

worker:
  create_or_reuse_goal_packet(ticket.md, program.md, progress.md)
  load fixed scenario tickets/TASK-0237/artifacts/agi-toy-shop-scenario.md
  append planning hypothesis cycle in progress.md
  create one to three TasteProposal entries
  use optimize-with-human(phases=planning,execution, channel=telegram)
  wait for idea feedback before execution
```

## Map

- `ticket:` `tickets/TASK-0240/ticket.md`
- `program:` `tickets/TASK-0240/program.md`
- `progress:` `tickets/TASK-0240/progress.md`
- `scenario:` `tickets/TASK-0237/artifacts/agi-toy-shop-scenario.md`
- `worker_thread:` `019f0e45-a5c1-7381-80b8-df88a2a3e2ee`
- `worker_title:` Taste Loop Worker: TASK-0240 social_thread
- `diagnostic_thread:` `019f0990-49a5-72f1-8720-dde9054fede1`
- `unverified_replacement_worker_thread:` `019f09c4-ecda-7423-a80c-7ab5a8e53788`

## Done / Proof

- [x] Worker thread created or existing worker reused.
- [x] `progress.md` contains a planning hypothesis cycle before feedback.
- [x] One to three TasteProposal entries are visible.
- [x] Feedback request is sent from an app-visible worker thread or a
  blocker/fallback is recorded there.
- [x] Execution waits for idea approval.
- [x] Controller memory records active worker state.
- [ ] Critical-path proof before completion: inspect the path from controller
  selection -> worker thread -> TasteProposal batch -> feedback request ->
  approved idea or blocker, with evidence linked from the worker/progress
  artifacts.

## State

- `selected_by:` manual Taste Loop beat
- `selected_at:` 2026-06-27T22:50:30+08:00
- `valid_open_feedback_count:` 1
- `legacy_invalid_feedback_count:` 4
- `status:` waiting_for_current_planning_hypothesis_feedback
- `last_reminder_at:` 2026-06-29T22:02:35+08:00
- `last_request_at:` 2026-06-29T18:51:25+08:00
- `reminder_count:` 1
- `max_reminders_per_feedback:` 2
- `telegram_message_id:` 2282
- `telegram_reminder_message_id:` 2283
- `telegram_parse_mode:` Markdown
- `last_feedback_at:` 2026-06-29T03:31:22+08:00
- `feedback_verdict:` revise
- `framing_requirement:` artifact-first header with review artifact, skill/workflow, product, stage, and not-judging fields
- `active_feedback_artifact:` `tickets/TASK-0240/artifacts/feedback-TL-EXP-004.json`
- `progress_unit:` hypothesis_cycle
- `idea_pass_rate:` 0/4 planning attempts approved
- `execution_pass_rate:` 0/0 execution attempts approved

## Links

- `parent_controller_thread:` 019f0774-76d7-77d3-b7e5-0e9bb48e232f
- `source_thread:` 019f076a-3365-7800-a243-095a7ab68e08
- `active_worker_thread:` `019f0e45-a5c1-7381-80b8-df88a2a3e2ee`
- `diagnostic_thread:` `019f0990-49a5-72f1-8720-dde9054fede1`
- `replacement_worker_thread:` `019f09c4-ecda-7423-a80c-7ab5a8e53788` (unverified; not app-visible)
- `telegram_reminder_TL_EXP_003:` `tickets/TASK-0240/artifacts/telegram-reminder-TL-EXP-003-final-20260629T020723.txt`
- `feedback_TL_EXP_003:` `tickets/TASK-0240/artifacts/feedback-TL-EXP-003.json`
- `taste_proposal_TL_EXP_004:` `tickets/TASK-0240/artifacts/taste-proposal-TL-EXP-004.md`
- `telegram_message_TL_EXP_004:` `tickets/TASK-0240/artifacts/telegram-message-TL-EXP-004.md`
- `telegram_reminder_TL_EXP_004:` `tickets/TASK-0240/artifacts/telegram-reminder-TL-EXP-004-markdown-20260629T220235.md`
- `feedback_request_TL_EXP_004:` `tickets/TASK-0240/artifacts/feedback-request-TL-EXP-004.md`
- `feedback_TL_EXP_004:` `tickets/TASK-0240/artifacts/feedback-TL-EXP-004.json`
