---
template_id: ticket-template
template_version: "0.1.1"
ticket_id: TASK-0240
title: Taste Loop social thread concept worker
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
updated_at: 2026-06-27T22:52:05+08:00
next_action: wait for Kenji planning feedback before drafting the social thread
last_verification: manual operator Taste Loop beat selected social_thread; valid open feedback budget permits one new worker; worker thread created; Telegram feedback request sent
---

# TASK-0240: Taste Loop social thread concept worker

## Summary

Run one Goal-backed Taste Loop worker for the `trust_distribution/social_thread`
workflow. The worker should start with planning concept cards for the AGI Toy
Shop scenario and ask Kenji for compact idea feedback before spending effort on
execution.

## Scope

- In:
  - Use `farplane/products.md` workflow `social_thread`.
  - Use owner route `social-content:twitter-thread`.
  - Use `tickets/TASK-0237/artifacts/agi-toy-shop-scenario.md` unless a better
    live context is explicitly supplied.
  - Create one to three concept cards as the planning artifact.
  - Use `optimize-with-human` with `phases=planning,execution`.
  - Log planning and execution experiment proposals/results in `progress.md`.
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
  planning_artifact: hook and argument concept card
  execution_artifact: draft thread
  feedback_question: keep / revise / reject the hook and argument

worker:
  create_or_reuse_goal_packet(ticket.md, program.md, progress.md)
  load fixed scenario tickets/TASK-0237/artifacts/agi-toy-shop-scenario.md
  log planning experiment proposal in progress.md
  create one to three ConceptCard entries
  use optimize-with-human(phases=planning,execution, channel=telegram)
  wait for idea feedback before execution
```

## Map

- `ticket:` `tickets/TASK-0240/ticket.md`
- `program:` `tickets/TASK-0240/program.md`
- `progress:` `tickets/TASK-0240/progress.md`
- `scenario:` `tickets/TASK-0237/artifacts/agi-toy-shop-scenario.md`
- `worker_thread:` `019f0990-49a5-72f1-8720-dde9054fede1`

## Done / Proof

- [x] Worker thread created or existing worker reused.
- [x] `progress.md` contains a planning experiment proposal before feedback.
- [x] One to three concept cards are visible.
- [x] Feedback request is sent from the worker thread or a blocker/fallback is
  recorded there.
- [x] Execution waits for idea approval.
- [x] Controller memory records active worker state.
- [ ] Critical-path proof before completion: inspect the path from controller
  selection -> worker thread -> concept cards -> feedback request -> approved
  idea or blocker, with evidence linked from the worker/progress artifacts.

## State

- `selected_by:` manual Taste Loop beat
- `selected_at:` 2026-06-27T22:50:30+08:00
- `valid_open_feedback_count:` 1
- `legacy_invalid_feedback_count:` 4
- `status:` waiting_for_planning_feedback

## Links

- `parent_controller_thread:` 019f0774-76d7-77d3-b7e5-0e9bb48e232f
- `source_thread:` 019f076a-3365-7800-a243-095a7ab68e08
- `worker_thread:` `019f0990-49a5-72f1-8720-dde9054fede1`
