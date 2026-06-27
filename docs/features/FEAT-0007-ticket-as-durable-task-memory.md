---
title: "Ticket as durable task memory"
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
  - docs/MEMORY.md#MEM-0058
  - docs/MEMORY.md#MEM-0148
  - docs/HISTORY.md
feature_record_json: |
  {
    "id": "FEAT-0007",
    "name": "Ticket as durable task memory",
    "status": "implemented",
    "system_id": "SYS-0002",
    "category": "memory",
    "public": true,
    "surfaces": [
      "tickets/README.md",
      "tickets/templates/ticket.md",
      "skills/impl-plan",
      "skills/spec-to-ticket",
      "docs/features/FEAT-0007-ticket-as-durable-task-memory.md"
    ],
    "source_refs": [
      "docs/features/README.md",
      "docs/MEMORY.md#MEM-0058",
      "docs/MEMORY.md#MEM-0148"
    ],
    "external_refs": [],
    "evidence_refs": [
      "docs/HISTORY.md"
    ],
    "known_limits": "Only works when agents keep the compact ticket-as-program body, ticket State/Links, progress logs, and artifact pointers current instead of hiding state in chat.",
    "metrics": [],
    "last_verified": "2026-06-12"
  }
---

# Ticket as durable task memory

Ticket as durable task memory is a first-class Farplane feature in [Work Loop](../systems/work-loop.md). It survives as a `FEAT-*` handle because it has owner surfaces, evidence, limits, and a maintenance path.

```text
feature(FEAT-0007, repo_state?) -> behavior + evidence + maintenance_signal
```

## System

- System: [Work Loop](../systems/work-loop.md)
- Feature ID: `FEAT-0007`
- Status: `implemented`
- Category: `memory`

## Feature Spec

This feature owns the spec-to-ticket work loop. A durable ticket is the smallest reusable execution memory for a bounded unit of work. It carries scope, program, map, Done / Proof, state, links, and sparse notes so an agent can resume without relying on chat transcript memory.

```text
work_loop(intent, evidence?) -> ticket_contract + execution_program + proof_obligations
```

The contract folded the former spec-first execution, handoff, context, and spec-authoring rules into one feature:

- Discovery produces the smallest useful feature/spec owner, then a ticket slice with explicit proof gates.
- Agent-testability planning identifies controls, probes, coordination views, and evidence before build work begins.
- Work packaging keeps `ticket.md` compact and moves bulky proof to ticket artifacts.
- Build proceeds through focused implementation, QA, review, and closeout against the ticket `Done / Proof` scoreboard.
- Handoffs name the current state, next step, blockers, exact files, and evidence instead of relying on transcript memory.
- Reset/resume decisions prefer visible ticket state, `program.md`, `progress.md`, and artifact links over hidden process state.

Non-goal: this feature is not a general project-management app. It is the durable execution substrate for Farplane-controlled work.

Proof gates:

- A new work item can be reconstructed from filesystem artifacts alone.
- The ticket says what is in scope, how to verify it, and where evidence belongs.
- Stale plans, broad specs, or chat-only decisions are folded into the owning feature/system/ticket or deleted.

## Owner Surfaces

- `tickets/README.md`
- `tickets/templates/ticket.md`
- `skills/impl-plan`
- `skills/spec-to-ticket`
- `docs/features/FEAT-0007-ticket-as-durable-task-memory.md`

## Source Context

- `docs/features/README.md`
- `docs/MEMORY.md#MEM-0058`
- `docs/MEMORY.md#MEM-0148`

## Evidence

- `docs/HISTORY.md`

## Known Limits

Only works when agents keep the compact ticket-as-program body, ticket State/Links, progress logs, and artifact pointers current instead of hiding state in chat.

## Metrics

- no dedicated metric yet

## Maintenance

Update this feature doc before regenerating `docs/features/registry.jsonl`. If the feature stops deserving its own doc, delete this file and remove all active template, source, ticket, and system refs to `FEAT-0007`.
