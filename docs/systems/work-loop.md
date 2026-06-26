---
title: "Work Loop"
status: active
owner: farplane-framework
created_at: 2026-06-26
updated_at: 2026-06-26
tags:
  - farplane
  - systems
  - work-loop
refs:
  - tickets/README.md
  - docs/specs/spec-first-execution-loop.md
  - docs/specs/spec-authoring-contract.md
  - docs/specs/first-principles-planning.md
system_record_json: |
  {
    "id": "SYS-0002",
    "name": "Work Loop",
    "status": "implemented",
    "summary": "The durable loop that turns intent into plans, tickets, skills, implementation, and reviewable proof for one bounded unit of work.",
    "owner_spec": "docs/systems/work-loop.md",
    "primary_feature_ref": "FEAT-0007",
    "feature_refs": [
      "FEAT-0007"
    ],
    "refs": [
      "tickets/README.md",
      "docs/specs/spec-first-execution-loop.md",
      "docs/specs/spec-authoring-contract.md",
      "docs/specs/first-principles-planning.md"
    ],
    "last_verified": "2026-06-26"
  }
---

# Work Loop

The durable loop that turns intent into plans, tickets, skills, implementation, and reviewable proof for one bounded unit of work.

## Role

Work Loop is the one-ticket execution product: it turns a fuzzy request into durable task memory, scoped action, evidence, and reviewable closure.

## What Belongs Here

Tickets, planning contracts, task decomposition, implementation handoff, and proof-oriented closeout for bounded work.

## What Belongs Elsewhere

Long-horizon scheduling belongs to Horizon Loop; reusable expertise belongs to Skill System; final judgment belongs to Proof and Review.

## Feature Docs

- [FEAT-0007 Ticket as durable task memory](../features/FEAT-0007-ticket-as-durable-task-memory.md)

## Maintenance

This system page owns only the system-level contract. Feature registry rows are authored as feature pages in `docs/features/` and generated into `docs/features/registry.jsonl`.
