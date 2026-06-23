---
title: "Steer Daily Report Workflow"
status: active
owner: steer-update
created_at: 2026-06-23
updated_at: 2026-06-23
---

# Steer Daily Report Workflow

```text
daily_report(tickets, pulse_reports, worker_threads, outcomes)
  -> interval_summary + blocker_labels + pulse_guidance
```

Read tickets, Pulse reports, worker-thread outcomes, and reports created since
the previous daily interval. Summarize what changed, label blockers and source
gaps, and write lightweight guidance that Pulse can use for board selection.

Do not run strategy replanning from this workflow unless the weekly steering
job is also due. Do not execute leaf tickets from this workflow.
