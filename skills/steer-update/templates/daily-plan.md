---
title: "Steer Daily Plan Workflow"
status: active
owner: steer-update
created_at: 2026-06-23
updated_at: 2026-06-23
---

# Steer Daily Plan Workflow

Compatibility alias for the active daily report workflow. Prefer
[daily-report.md](daily-report.md) for new Steer configs.

New Steer configs should use `daily_report`, not `daily_plan`.

```text
daily_plan_compat(tickets, pulse_reports, worker_threads, outcomes)
  -> interval_summary + blocker_labels + pulse_guidance
```

Read recent Pulse outcomes, worker-thread outcomes, and open tickets. Summarize
what changed, label blockers and source gaps, and write guidance that Pulse can
use for board selection.

Do not run drift review or strategy replanning from this compatibility workflow.
Do not execute leaf tickets from this workflow.
