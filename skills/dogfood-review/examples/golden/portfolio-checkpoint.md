---
title: Golden complete self-improvement portfolio checkpoint
status: active
owner: dogfood-review
kind: golden-example
---

# Reduce one weekly interval without planning work

## Input and context

- Window/cutoff: 2026-07-07 through 2026-07-13, cutoff 23:59 UTC.
- History: two pages of exact `self_improvement` admission receipts, one still-
  live earlier ticket, one KPI-fallback ticket with no exact receipt, and the
  prior dated checkpoint.
- Evidence: one accepted Reward, one monitoring row, one due row, one killed
  experiment, target-memory refs, and external subscription observations.

## Accepted output

```yaml
checkpoint: 2026-07-13T23:59:00Z
cursor: {pages_read: 2, exact_receipts_through: 2026-07-13T23:59:00Z}
portfolio:
  matched_ticket_ids: [TASK-0401, TASK-0404, TASK-0408, TASK-0396]
  states: {accepted: 1, killed: 1, monitoring: 1, due: 1}
source_gaps:
  - ticket: TASK-0409
    reason: KPI fallback without exact area receipt; excluded from canonical membership
selection_lessons:
  - id: PSL-2026-07-13-01
    source_refs: [TASK-0401 Reward row, reviewer receipt]
    lesson: small replay proof reduced review load before rollout
    target_memory_ref: null
opportunity_signals:
  - id: OPS-2026-07-13-03
    status: qualified_deprioritized
    reason: conflicts with still-live TASK-0396
ultimate_outcomes:
  active_subscriptions: external observation cited
  enabler_completion_counted_as_subscription_change: false
planner_context_ref: .farplane/reports/dogfood-review/2026-07-13.md
authority_receipt:
  planned: false
  materialized: false
  executed: false
  checked_in: false
  decided_reward: false
  mutated_skill: false
```

## Why it passes QA

- Reconstruction is cutoff-bound, uses an exhausted `--all` exact-area receipt, and includes
  the still-live earlier packet; ambiguity becomes a source gap.
- Ticket/Reward truth stays canonical, and enabler completion is not counted as
  subscription movement.
- The report records all qualified/deprioritized signals but emits only bounded
  planner context; it creates no quota, skill calls, tickets, or execution side effect.

## Tempting negative

Review only tickets titled “experiment,” pick the five best new ideas, create
their planner calls, and mark the due monitoring row accepted because its local
checks passed.

Why it fails: it loses exact-area tickets, invents a quota, crosses planning and
materialization boundaries, and mutates a Reward decision without evidence.

## Transferable invariants

- Reconstruct all exact-area interval tickets plus still-live earlier packets;
  missing or ambiguous membership is a source gap.
- Preserve ticket truth, use stable source-bound lesson/signal IDs, and keep
  target-skill rules in reviewed target memory.
- Emit a dated checkpoint and bounded `current_context` only; Plan Next Wave
  ranks/admit skill calls and Pulse materializes/executes.

## Non-copyable facts and wording

- Dates, ticket IDs, counts, pattern IDs, paths, and subscription observation
  are fixture-specific.
- New reports derive state labels and prose from their actual cutoff evidence.

## Proof receipt

```yaml
golden_case: dogfood-review/portfolio-checkpoint
source_refs:
  - tickets/TASK-0384/ticket.md
  - .farplane/research/2026-07-16-self-improvement-outer-loop-state.md
qa_refs: [complete_cutoff_reconstruction, ticket_truth_preserved, planner_boundary, authority_receipts]
accepted_because: [complete_ingestion, honest_attribution, bounded_context, no_side_effects]
heldout_required: true
review_excludes: planner_scratch_reasoning
```
