---
title: Taste Loop progress hypothesis ledger
owner: taste-loop
status: accepted
date: 2026-06-29
related:
  - skills/taste-loop/SKILL.md
  - skills/optimize-with-human/SKILL.md
  - tickets/TASK-0240/program.md
  - tickets/TASK-0240/progress.md
---

# Taste Loop Progress Hypothesis Ledger

## Trigger

Kenji clarified that the loop should not keep creating fresh `TL-EXP` units as
the main work identity. The intended pattern is autoresearch-like:
`progress.md` stores the current hypothesis, the attempted artifact, the human
signal, the learning, and the next hypothesis. The ticket remains the workflow
container until the loop is approved, converged, blocked, budget-exhausted, or
closed.

## Delta

- Replaced the Taste Loop `Experiment Log Contract` with a `Progress Log
  Contract`.
- Updated `optimize-with-human` to log `hypothesis_cycle` rows instead of
  requiring named experiment proposals.
- Removed the requirement that worker thread titles include a transient
  `TL-EXP-###` suffix.
- Updated TASK-0240 `program.md` with `progress_unit = hypothesis_cycle`.

## Proof

- `skills/taste-loop/eval_task.json` now checks for timestamped hypothesis
  cycles in `progress.md`.
- `tickets/TASK-0240/progress.md` records the correction and the future
  progress shape.
