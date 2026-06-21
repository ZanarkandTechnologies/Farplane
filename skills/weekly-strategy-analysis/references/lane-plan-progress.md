---
title: Plan Progress Lane
owner: weekly-strategy-analysis
kind: lane-reference
---

# Plan Progress Lane

```text
plan_progress_lane(context_bundle, lane_output)
  -> goal_movement + task_drag + plan_realism + priority_delta
```

Question: did the planned week actually advance the active goals, and what
should change next?

Track:

- planned commitments vs done tasks vs not-done tasks.
- goal/project coverage: meaningful progress, maintenance only, or no progress.
- task conversion and drag: done count, not-done count, stale count, blocked
  count, overdue count, and work that should carry forward, delegate, or die.
- plan realism: bad estimates, weak priority calls, blocked dependencies,
  justified plan changes from meetings, or new evidence.
- strategic delta: strengthened/weakened assumptions, priority changes,
  depriorities, due dates, and proof-of-progress checks.

Output:

- `goal_movement`: goal/project, evidence, impact label.
- `drag_table`: task/cluster, reason, carry/delegate/kill decision.
- `plan_calibration`: what to plan differently next week.
- `priority_delta`: priority, depriority, due date, proof check.
- source gaps and rejected claims.
