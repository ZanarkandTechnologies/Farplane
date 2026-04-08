---
ticket_id: TASK-0026
title: bind worker identity to ticket handoffs
phase: planning
status: review
owner: codex
priority: high
depends_on: []
blocked_by: []
ready: true
approval_required: false
created_at: 2026-04-08T00:00:00Z
updated_at: 2026-04-08T00:00:00Z
next_action: define how impl/orchestrator assigns worker identity, ticket id, and session metadata so stop-hook and orchestrator can reliably tie context back to the right worker
last_verification: none
linked_docs: []
---

# TASK-0026: bind worker identity to ticket handoffs

## Summary
Make orchestrated multi-agent handoffs legible by assigning each spawned worker a stable identity plus explicit ticket/session context so the Stop hook and orchestrator can tell which worker owns which ticket.

## Scope
- In:
  - worker naming rules
  - ticket-to-worker binding
  - session metadata updates
  - orchestrator and stop-hook consumption of that mapping
- Out:
  - broad queue scheduler redesign
  - full cloud/distributed worker orchestration

## Plan

### Pitch
- `Req:` give the orchestrator and Stop hook a reliable way to know which worker is working on which ticket during multi-agent handoffs
- `Bet:` a small worker identity contract plus runtime-state/session metadata is enough for v1
- `Win:` handoffs become inspectable and continuation decisions become less ambiguous

### B -> A
- `Before:` worker ownership is inferred from ticket state, tmux/session metadata, and current run state, but there is no explicit worker identity contract
- `After:` each spawned worker gets a stable name plus bound ticket id/session context that the orchestrator and Stop hook can read directly
- `Outcome:` continuation, review, and next-ticket routing can be tied back to the correct worker lane

### Delta
- `Touch:` impl/orchestrator worker launch contract, runtime state fields, tmux/session helper metadata, and stop-hook/orchestrator lookup logic
- `Keep:` single-ticket execution ownership and ticket-first workflow
- `Change:` add explicit worker identity metadata instead of relying on loose inference
- `Delete/Avoid:` avoid heavy worker registries or hidden daemon state

### Core Flow
```pseudo
orchestrator selects ticket
orchestrator assigns worker_name + ticket_id + session metadata
launch worker with bound identity
persist worker->ticket mapping in runtime state
stop hook reads worker identity and ticket binding
orchestrator uses that mapping for followup or next-step decisions
```

### Proof
- `P1:` each active worker can be traced back to exactly one ticket
- `P2:` stop-hook and orchestrator no longer need to guess which worker owns the active ticket
- `Risk:` identity fields could drift if worker launch and state persistence are not updated atomically
- `Rollback:` keep binding additive at first and fall back to current ticket/session inference if fields are missing

### Plan Review
- `Refs:` impl skill, tmux helper, stop-hook routing, current run-state schema, and orchestrator references
- `Scope:` bounded to worker identity and ticket/session binding
- `Proof:` success is observable through runtime state and follow-up routing
- `Guardrails:` no hidden daemon registry, no broad runtime expansion
- `Fixes:` none

### Delegation
- `Need:` `Not needed`
- `Why:` this is a centralized runtime contract slice
- `Artifact:` none

### Ask
- `Ready: yes`
- `Next:` plan the exact worker identity fields and handoff/readback points

### Ticket Move
- `Now:` `tickets/`
- `On approval:` move to active planning/building work
- `Follow-ups:` none yet
- `Blocked in building?:` `no`

## Acceptance Criteria
- [ ] AC-1: orchestrator assigns a stable worker identity when spawning a worker
- [ ] AC-2: runtime state records worker identity, ticket id, and session metadata together
- [ ] AC-3: stop-hook can use the worker binding to identify the correct ticket/worker context
- [ ] AC-4: orchestrator can use the same binding to route followup or next-ticket actions without guessing

## Working Notes
- The goal is not a heavy worker registry; it is explicit ownership metadata.
- This should work for tmux-backed lanes and other future session surfaces.

## Implementation Notes
- Touched areas:
- Reused patterns:
- Guardrails:

## Evidence
- [ ] Tests
- [ ] Typecheck
- [ ] Lint
- [ ] QA / manual verification

## Review Packet
- `reviewed_at:`
- `rubrics_used:`
- `overall_score:`
- `overall_verdict:`
- `rerun_required:`
- `blocking_findings:`
- `next_action:`

## Blockers
- none

## Handoff
- Current state: idea captured as a ticket; not yet planned in detail
- Resume from: this ticket, impl worker launch surfaces, and stop-hook/orchestrator runtime state usage

## Writeback
- Update this ticket as work progresses.
- If the ticket changes queue state, update `status` and `phase` in frontmatter. Do not move the file.
- When implementation and verification pass, move `phase` to `documenting`, write durable docs, then move the ticket into `tickets/archive/` or set `status: done` briefly if you intentionally keep a short-lived visible completion state first.
