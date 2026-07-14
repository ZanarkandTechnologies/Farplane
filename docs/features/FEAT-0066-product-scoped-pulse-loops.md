---
title: Product-scoped Pulse loops
status: retired
owner: feature-registry
created_at: 2026-07-07
updated_at: 2026-07-11
tags:
  - farplane
  - feature
  - sys-0003
refs:
  - docs/prd.md
  - docs/features/FEAT-0071-project-work-pulse.md
  - tickets/archive/TASK-0318/ticket.md
feature_id: FEAT-0066
system_id: SYS-0003
category: planning
public: true
surfaces:
  - docs/features/FEAT-0066-product-scoped-pulse-loops.md
  - docs/features/FEAT-0071-project-work-pulse.md
source_refs:
  - docs/prd.md
  - tickets/archive/TASK-0318/ticket.md
external_refs: []
evidence_refs:
  - tickets/archive/TASK-0318/artifacts/review/plan-review.md
known_limits: "Retired historical design only; TASK-0321 removed its project files and active readers."
metrics:
  - product_loop_ticket_relevance
  - review_capacity_fit
last_verified: 2026-07-10
experimental: false
superseded_by: FEAT-0071
track: false
---

# Product-scoped Pulse loops

Product-scoped Pulse loops are retired. They split project work across five
controllers with separate product strategy, progress, worker budget, review
capacity, and heartbeat records before those concerns proved they needed
independent runtime ownership.

The active successor is [Project Work Pulse](FEAT-0071-project-work-pulse.md):

```text
one project board + one Work Pulse + one pure planner + one worker pool
```

## Historical Behavior

The retired feature:

- routed empty-board planning through product `product.md` and `progress.md`;
- required product-backed rewards and learning writeback for admission;
- assigned worker/review capacity per product loop;
- ran five product-scoped heartbeat automations.

## Retirement Boundary

- Active `pulse-update` and `plan-next-wave` no longer require or
  invoke product controllers.
- The five product Pulse automations are removed in TASK-0318.
- TASK-0321 removed the retained product files, registry, and active readers.
- Historical product-loop details remain only in archived evidence and this
  retired feature record.

## Evidence

- Current standard: `docs/prd.md`
- Migration rationale: `tickets/archive/TASK-0318/ticket.md`
- Implementation ticket: `tickets/archive/TASK-0318/ticket.md`
- Successor: `docs/features/FEAT-0071-project-work-pulse.md`

## Change History

- 2026-07-07: Added as an experimental product-scoped controller design.
- 2026-07-10: Retired in favor of one project Work Pulse.
- 2026-07-11: Recorded the completed TASK-0321 file-and-reader removal.
