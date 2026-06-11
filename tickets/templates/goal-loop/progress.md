---
kind: goal-progress
ticket_id: TASK-XXXX
status: active
created_at: 2026-06-12
---

# TASK-XXXX Goal Progress

Append one entry per Goal turn, heartbeat, feedback resume, or drift checkpoint.
Keep entries compact. Link artifacts instead of pasting raw transcripts.

## Entry Template

```markdown
## 2026-06-12 HH:MM +0800 - turn N

- `trigger:` native_goal | scheduled_heartbeat | human_feedback_received | manual_resume
- `intent:`
- `actions:`
- `files_changed:`
- `artifacts:`
- `metric_sample:`
- `feedback_sample:`
- `drift_verdict:` aligned | drifting | blocked | complete_candidate | not_run
- `drift_evidence:`
- `next_action:`
- `blocker:`
```
