---
title: Ticket as durable task memory
status: implemented
owner: feature-registry
created_at: 2026-06-26
updated_at: 2026-06-27
tags:
  - farplane
  - feature
  - sys-0002
refs:
  - tickets/README.md
  - tickets/templates/ticket.md
  - skills/impl-plan
  - skills/spec-to-ticket
  - docs/features/FEAT-0007-ticket-as-durable-task-memory.md
  - docs/features/README.md
  - "docs/MEMORY.md#MEM-0058"
  - "docs/MEMORY.md#MEM-0148"
  - docs/HISTORY.md
feature_id: FEAT-0007
system_id: SYS-0002
category: memory
public: true
surfaces:
  - tickets/README.md
  - tickets/templates/ticket.md
  - skills/impl-plan
  - skills/spec-to-ticket
  - docs/features/FEAT-0007-ticket-as-durable-task-memory.md
source_refs:
  - docs/features/README.md
  - "docs/MEMORY.md#MEM-0058"
  - "docs/MEMORY.md#MEM-0148"
external_refs: []
evidence_refs:
  - docs/HISTORY.md
known_limits: Only works when agents keep the compact ticket-as-program body, ticket State/Links, progress logs, and artifact pointers current instead of hiding state in chat.
metrics: []
last_verified: 2026-06-12
---
# Ticket as durable task memory

Ticket as durable task memory exists to turn a request into a visible work contract that
survives handoff, interruption, review, and closeout. It belongs to [Work
Loop](../systems/work-loop.md) and keeps `FEAT-0007` as a stable capability handle
because the behavior has an owner, proof path, and maintenance boundary.

```text
ticket_memory(intent, repo_state?) -> ticket_contract + proof_scoreboard + resume_state
```

## At A Glance

- Feature ID: `FEAT-0007`
- System: [Work Loop](../systems/work-loop.md)
- Status: `implemented`
- Category: `memory`
- Primary user: coding agent and operator
- Job: turn a request into a visible work contract that survives handoff, interruption, review, and closeout.

## Problem

Farplane agents do long, context-heavy work. If the plan only lives in chat, the next
agent cannot reliably tell what was promised, what changed, what proof is required, or
whether the task is blocked.

A ticket fixes that by making one bounded unit of work readable from the filesystem.
Chat can steer the work, but the ticket owns the durable contract.

## What It Does

- Creates or updates a `ticket.md` for each material unit of work.
- Keeps scope, delta, program, file map, `Done / Proof`, state, links, and notes in predictable sections.
- Moves bulky proof into `tickets/TASK-*/artifacts/` and links it from the ticket.
- Lets `impl-plan`, `spec-to-ticket`, Goal Packets, QA, review, and closeout all read the same task contract.
- Preserves resume state through `program.md`, `progress.md`, and artifact links when a work loop needs more than one turn.

## User Stories

- As an operator, I can open one ticket and see what the agent is trying to do, what is in scope, what proof is required, and what is blocked.
- As a coding agent, I can resume a ticket without relying on hidden transcript memory.
- As a reviewer, I can judge completion against the ticket's `Done / Proof` block and linked artifacts.

## Operating Contract

A durable ticket is a small program for the next agent, not a generic task note.

- `Summary` says the job in one compact paragraph.
- `Scope` states what is in and out.
- `Delta` describes the intended behavior change.
- `Program` gives the execution shape or pseudocode.
- `Map` points to the files, docs, skills, or tests that matter.
- `Done / Proof` is the completion scoreboard.
- For material features, the same `Done / Proof` body carries critical-path
  proof notes in ordinary prose or bullets rather than a new required schema.
- `State` carries current status, blocker, verification, and result.
- `Links` points to evidence, artifacts, related specs, and handoffs.

## Surfaces

Owner surfaces:

- `tickets/README.md`
- `tickets/templates/ticket.md`
- `skills/impl-plan`
- `skills/spec-to-ticket`
- `docs/features/FEAT-0007-ticket-as-durable-task-memory.md`

Source context:

- `docs/features/README.md`
- `docs/MEMORY.md#MEM-0058`
- `docs/MEMORY.md#MEM-0148`

Evidence:

- `docs/HISTORY.md`

## Proof And Quality

Required checks:

- `python3 docs/features/validate_features.py`
- `python3 bin/validators/check_doc_refs.py`

Acceptance signals:

- The feature remains listed under exactly one owning system.
- The owner surfaces still exist and agree with this contract.
- Evidence refs support the current status.

## Rollout And Maintenance

- Update this feature page first when the capability contract changes.
- Then update owner surfaces and regenerate feature/system registries when metadata changes.
- Preserve the feature ID while active templates, skills, tickets, or docs still reference it.
- Maintenance owner: Work Loop.

## Limits And Non-Goals

- This feature is not a project-management app.
- This feature does not make ticket existence an invocation trigger.
- This feature does not replace feature specs, system specs, review rubrics, or bulky proof artifacts.
- Known limit: Only works when agents keep the compact ticket-as-program body, ticket State/Links, progress logs, and artifact pointers current instead of hiding state in chat.
- Delete or merge this feature only when its current truth has moved into a clearer owner and all active refs are removed.

## Metrics

- no dedicated metric yet

## Alternatives Considered

- Keep this only as a registry row.
  Decision: reject.
  Reason: Farplane features must be readable specs, not opaque metadata entries.
- Fold this entirely into the owning system page.
  Decision: defer.
  Reason: keep the `FEAT-*` page while templates, skills, tickets, or proof surfaces need a stable capability handle.

## Change History

- 2026-06-26: Feature spec created.
- 2026-06-27: Migrated into the reader-first feature-spec shape.
