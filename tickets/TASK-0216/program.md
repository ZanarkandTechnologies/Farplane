---
ticket_id: TASK-0216
title: "Goal Program: Shared GraphIR and Configurable Projections"
status: draft
owner: codex
created_at: 2026-06-24T11:00:33+0800
updated_at: 2026-06-24T11:00:33+0800
refs:
  - ticket.md
  - generated-goal-prompt.md
---

# Goal Program

```text
goal_loop(
  ticket = tickets/TASK-0216/ticket.md,
  trigger = operator-approved implementation,
  budget = focused single-pass implementation with review,
  metric = compatibility-preserving graph generator refactor
) -> compatible graph artifacts + docs + evidence
```

## Execution Policy

- Treat the existing generated artifacts as compatibility contracts unless a
  documented count/schema delta is necessary.
- Keep generated files in `skills/skill-maintenance/graph/`.
- Keep current generator commands working as public wrappers.
- Do not add a hidden daemon, watcher, database, or runtime service.
- Prefer shared helpers over broad rewrites of generator-specific extraction
  logic.

## Turn Routine

1. Re-read `ticket.md`, current generator files, graph README, and graph
   contract.
2. Capture current generated counts for skill, harness, and lifecycle graphs.
3. Add shared GraphIR/projection modules.
4. Port lifecycle generator first because it already has projection-like
   core/full behavior.
5. Port skill and harness generators while preserving their emitted schemas.
6. Regenerate artifacts and run the proof checklist.
7. Request reviewer lane for TAS-A code-quality/integration/docs review.
8. Address review findings, update `progress.md`, and summarize evidence.

## Drift Policy

Stop and update the ticket before continuing if implementation reveals:

- a current graph consumer requires a schema-breaking change;
- output compatibility would require duplicating most of the old code anyway;
- projection config needs a user-editable external file to satisfy the ticket;
- the refactor touches unrelated UI/runtime behavior.

## Stop Conditions

- All `done_when` bullets in `ticket.md` are satisfied.
- Proof commands pass or a concrete blocker is recorded.
- Review evidence exists under `artifacts/`.
- `progress.md` contains the final counts, verification summary, and next
  action.
