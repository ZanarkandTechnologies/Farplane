---
title: "Ticket as durable task memory"
status: implemented
owner: feature-registry
created_at: 2026-06-26
updated_at: 2026-06-26
tags:
  - farplane
  - feature
  - sys-0002
refs:
  - tickets/README.md
  - tickets/templates/ticket.md
  - skills/impl-plan
  - skills/spec-to-ticket
  - docs/specs/context-and-handoff-policy.md
  - docs/specs/harness-techniques.md
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
      "docs/specs/context-and-handoff-policy.md"
    ],
    "source_refs": [
      "docs/specs/harness-techniques.md",
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

## Owned Behavior

This feature owns the behavior implemented, specified, or enforced by its owner surfaces. Keep the details in those surfaces; keep this page focused on the stable feature contract and registry metadata.

## Owner Surfaces

- `tickets/README.md`
- `tickets/templates/ticket.md`
- `skills/impl-plan`
- `skills/spec-to-ticket`
- `docs/specs/context-and-handoff-policy.md`

## Source Context

- `docs/specs/harness-techniques.md`
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
