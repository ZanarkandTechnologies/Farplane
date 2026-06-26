---
template_id: ticket-template
template_version: "0.1.1"
feature_refs:
  - FEAT-0064
ticket_id: TASK-0236
title: Taste Loop landing page worker pilot
phase: building
status: building
owner: codex
claimed_by: taste-loop-worker
priority: high
depends_on: []
blocked_by: []
ready: true
approval_required: false
requires_qa: true
requires_demo: false
created_at: 2026-06-26T21:34:52+08:00
updated_at: 2026-06-26T21:42:00+08:00
next_action: worker thread created; wait for worker artifact/Telegram feedback request or steer if it blocks
last_verification: worker thread created and accepted direct follow-up; title/search visibility lagged
---

# TASK-0236: Taste Loop Landing Page Worker Pilot

## Summary

Run the first threaded Taste Loop artifact job. The worker thread should create
or revise a Farplane landing-page artifact, ask Kenji for a short Telegram
decision through `$optimize-with-human`, and continue revisions from replies in
that same thread.

## Scope

- In:
  - Pilot the `trust_distribution / landing_page_offer` workflow from
    `farplane/products.md`.
  - Use `$landing-page` to produce a reviewable artifact.
  - Use `$optimize-with-human` inside the worker thread for Telegram feedback.
  - Keep durable state in this ticket, `program.md`, `progress.md`, and
    `artifacts/`.
  - Provide phone-friendly evidence: a public/mobile-viewable URL, screenshot,
    or Farplane UI-ready preview fallback.
- Out:
  - No external publishing beyond a private review preview or screenshot.
  - No skill source edits unless explicitly spun into a separate ticket.
  - No parent heartbeat feedback request; replies should route to the worker
    thread.

## Delta

- `Before:` Taste Loop could create a local artifact and message Kenji from the
  parent heartbeat, which lost the reply-routing property needed for Telegram.
- `After:` Taste Loop creates a dedicated worker packet/thread first; the
  worker uses `$optimize-with-human` after producing the artifact.
- `Why now:` Kenji's Telegram replies are wired to thread conversations, so the
  artifact job needs its own persistent thread to revise from feedback.

## Program

See `tickets/TASK-0236/program.md`.

## Map

- `Touch:`
  - `tickets/TASK-0236/ticket.md`
  - `tickets/TASK-0236/program.md`
  - `tickets/TASK-0236/progress.md`
  - `tickets/TASK-0236/artifacts/`
- `Inspect:`
  - `farplane/products.md`
  - `skills/taste-loop/SKILL.md`
  - `skills/landing-page/SKILL.md`
  - `skills/optimize-with-human/SKILL.md`

## Done / Proof

```text
done_when:
  - dedicated worker thread is created and titled
  - worker prompt lists this ticket, program.md, and progress.md
  - worker is instructed to use $landing-page and $optimize-with-human
  - Kenji receives a Telegram feedback request that points at the worker thread
  - progress.md records the thread id and pilot state

proof:
  checks:
    - source Taste Loop and optimize-with-human changes installed
    - focused validators pass or unrelated validator blockers are named
  manual:
    - Telegram message sent to Kenji
    - worker thread created in Codex app
  review:
    - rubric: none
      required_tas: none
  evidence:
    - tickets/TASK-0236/progress.md
```

## Run Hints

- `Likely size:` normal
- `Goal recommendation:` required
- `Budget hint:` one worker thread; 3 artifact attempts; no spend; no public
  publish
- `Compute hint:` local_shared
- `Planning hint:` light
- `Proof weight:` smoke
- `Proof route:` none for pilot; later worker output may need visual QA
- `Final evidence:` worker thread id, Telegram send status, artifact or blocker
- `Human inputs/assets:` Kenji feedback via Telegram replies to worker thread
- `Credentials / external access:` Telegram notification only; no deployment
  unless worker can use an already configured private preview path
- `Human gates:` publish/deploy/spend require explicit approval

## Goal Packet

- `Goal packet:` active
- `Program:` `tickets/TASK-0236/program.md`
- `Progress:` `tickets/TASK-0236/progress.md`
- `Files:`
  - `tickets/TASK-0236/ticket.md`
  - `tickets/TASK-0236/program.md`
  - `tickets/TASK-0236/progress.md`
- `Metric provider:` human_feedback
- `Feedback preset:` optimize-with-human
- `Drift reviewer:` inline
- `Heartbeat:` manual resume through Telegram reply / worker thread
- `Stop condition:` keep/approve, convergence, budget exhausted, or blocker
- `Final report:` include artifact refs and best viewable evidence

## State

- `next_action:` wait for worker artifact/Telegram feedback request or steer if
  it blocks.
- `blocked:` false
- `latest_verification:` worker thread created and accepted direct follow-up
- `result:` in progress

## Links

- `program:` `tickets/TASK-0236/program.md`
- `progress:` `tickets/TASK-0236/progress.md`
- `artifacts:` `tickets/TASK-0236/artifacts/`
- `worker_thread:` `019f0424-a832-7712-b952-85b50222a716`
- `refs:`
  - `farplane/products.md`
  - `skills/taste-loop/SKILL.md`
  - `skills/optimize-with-human/SKILL.md`
