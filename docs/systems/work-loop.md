---
title: "Work Loop"
status: active
owner: farplane-framework
created_at: 2026-06-26
updated_at: 2026-06-27
tags:
  - farplane
  - systems
  - work-loop
refs:
  - tickets/README.md
  - docs/features/FEAT-0007-ticket-as-durable-task-memory.md
  - docs/features/FEAT-0042-lean-global-agent-operating-kernel.md
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
      "docs/features/FEAT-0007-ticket-as-durable-task-memory.md",
      "docs/features/FEAT-0042-lean-global-agent-operating-kernel.md"
    ],
    "last_verified": "2026-06-26"
  }
---
# Work Loop

The durable loop that turns intent into plans, tickets, skills, implementation, and
reviewable proof for one bounded unit of work. This page is the product-layer owner for
that subsystem: it explains what belongs here, which feature specs make up the stack,
and where adjacent responsibilities should move.

```text
work_loop(change, repo_state?) -> owned_feature_set + boundary_decision + maintenance_signal
```

## At A Glance

- System ID: `SYS-0002`
- Status: `implemented`
- Primary feature: `FEAT-0007`
- Owner spec: `docs/systems/work-loop.md`
- Feature count: `1`

## Role

Work Loop owns the short-horizon execution loop: translate intent into a bounded task
contract, use skills to do the work, keep state in tickets, and prove completion through
visible artifacts.

## Feature Docs

- [FEAT-0007 Ticket as durable task memory](../features/FEAT-0007-ticket-as-durable-task-memory.md)

## What Belongs Here

Ticket-as-memory behavior, task contracts, implementation planning, scoped execution,
closeout, and the handoff state needed for one bounded work unit.

## What Belongs Elsewhere

Long-horizon cadence belongs in Horizon Loop; proof judgment belongs in Proof And
Review; reusable workflow definitions belong in Skill System.

## Operating Contract

- Material work gets a visible ticket or equivalent owner.
- The ticket `Done / Proof` block defines completion.
- Bulky evidence lives in artifacts and is linked back to the task.
- Handoffs must be reconstructable from filesystem state.
- Feature-level behavior belongs in `docs/features/FEAT-*.md`; this page owns the system boundary and feature grouping.
- Registry data is generated from system and feature docs, not edited by hand.
- When a capability no longer deserves a feature page, fold its current truth into the best owner and remove active refs.

## Surfaces

- `tickets/README.md`
- `docs/features/FEAT-0007-ticket-as-durable-task-memory.md`
- `docs/features/FEAT-0042-lean-global-agent-operating-kernel.md`

## Proof And Maintenance

- Registry proof: `python3 docs/features/validate_features.py`.
- Link proof: `python3 bin/validators/check_doc_refs.py`.
- Update this system page when product-layer boundaries or feature membership changes.
- Update feature pages when capability behavior changes.
- Regenerate registries and commit generated outputs with the source docs.

## Change History

- 2026-06-27: Migrated into the reader-first system-spec shape.
