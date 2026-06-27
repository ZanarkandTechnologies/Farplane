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

This feature makes a Farplane ticket the durable memory object for one bounded
unit of work. Instead of asking an agent to remember scope, decisions, blockers,
proof, and next steps from chat, Farplane writes that state into a compact
ticket file and ticket-local artifacts that another agent can resume.

```text
ticket_memory(intent, repo_state?) -> ticket_contract + proof_scoreboard + resume_state
```

## At A Glance

- Feature ID: `FEAT-0007`
- System: [Work Loop](../systems/work-loop.md)
- Status: `implemented`
- Category: `memory`
- Primary user: coding agent and operator
- Job: turn a request into a visible work contract that survives handoff,
  interruption, review, and closeout.

## Problem

Farplane agents do long, context-heavy work. If the plan only lives in chat, the
next agent cannot reliably tell what was promised, what changed, what proof is
required, or whether the task is blocked. That creates repeat explanations,
false completion claims, and brittle handoffs.

The ticket is the fix: it is the task-local source of truth. Chat can steer the
work, but the ticket owns the durable contract.

## What It Does

- Creates or updates a `ticket.md` for each material unit of work.
- Keeps scope, delta, program, file map, `Done / Proof`, state, links, and notes
  in predictable sections.
- Moves bulky proof into `tickets/TASK-*/artifacts/` and links it from the
  ticket instead of stuffing it into chat.
- Lets `impl-plan`, `spec-to-ticket`, Goal Packets, QA, review, and closeout all
  read the same task contract.
- Preserves resume state through `program.md`, `progress.md`, and artifact
  links when a work loop needs more than one turn.

## User Stories

- As an operator, I can open one ticket and see what the agent is trying to do,
  what is in scope, what proof is required, and what is blocked.
- As a coding agent, I can resume a ticket without relying on hidden transcript
  memory.
- As a reviewer, I can judge completion against the ticket's `Done / Proof`
  block and linked artifacts.

## Operating Contract

A durable ticket is not a generic task note. It is a small program for the next
agent:

```text
work_loop(request, evidence?) -> ticket.md + optional program.md + optional progress.md + artifacts/
```

Required ticket behavior:

- `Summary` says the job in one compact paragraph.
- `Scope` states what is in and out.
- `Delta` describes the intended behavior change.
- `Program` gives the execution shape or pseudocode.
- `Map` points to the files, docs, skills, or tests that matter.
- `Done / Proof` is the completion scoreboard.
- `State` carries current status, blocker, verification, and result.
- `Links` points to evidence, artifacts, related specs, and handoffs.

For longer loops, `program.md` owns continuation settings and `progress.md`
owns append-only turn logs. The ticket remains the stable front door.

## Surfaces

- Owner surfaces:
  - `tickets/README.md`
  - `tickets/templates/ticket.md`
- Producer surfaces:
  - `skills/impl-plan`
  - `skills/spec-to-ticket`
- Consumer surfaces:
  - Goal Packets
  - QA and review lanes
  - closeout and memory update flows
- Generated or linked surfaces:
  - `tickets/TASK-*/program.md`
  - `tickets/TASK-*/progress.md`
  - `tickets/TASK-*/artifacts/`

## Proof And Quality

- Evidence:
  - `docs/HISTORY.md`
  - `docs/MEMORY.md#MEM-0058`
  - `docs/MEMORY.md#MEM-0148`
- Required checks:
  - `python3 bin/validators/check_doc_refs.py`
  - ticket-specific tests, QA, or review gates named in `Done / Proof`
- Acceptance signals:
  - A fresh agent can reconstruct the task from filesystem artifacts alone.
  - The ticket says how to verify the work and where proof belongs.
  - Review can pass or fail the work without relying on chat-only promises.

## Rollout And Maintenance

- Update path: change `tickets/README.md` and `tickets/templates/ticket.md`
  first, then update producer skills such as `impl-plan` and `spec-to-ticket`.
- Rollback path: revert the template/policy change and keep existing tickets as
  historical artifacts.
- Compatibility notes: avoid adding mandatory sections unless producers,
  reviewers, and closeout flows are updated in the same pass.
- Maintenance owner: Work Loop / ticket system.

## Limits And Non-Goals

- This feature is not a project-management app.
- This feature does not make ticket existence an invocation trigger.
- This feature does not replace feature specs, system specs, review rubrics, or
  bulky proof artifacts.
- Known weak spot: it only works when agents keep ticket state current instead
  of hiding decisions in chat.
- Delete or merge this feature only if Farplane stops using filesystem tickets
  as execution memory.

## Alternatives Considered

- Chat-only task memory.
  Decision: reject.
  Reason: fails handoff, review, and long-running resume.
- Central task database.
  Decision: defer.
  Reason: useful later, but the filesystem ticket is inspectable, git-friendly,
  and sufficient for the current harness.
- One spec file per task.
  Decision: reject.
  Reason: specs own durable capability behavior; tickets own bounded execution.

## Change History

- 2026-06-12: Ticket-as-program memory pattern stabilized in project memory.
- 2026-06-27: Migrated from old specs into the feature/system registry model.
- 2026-06-27: Rewritten as the readable feature-spec exemplar.
