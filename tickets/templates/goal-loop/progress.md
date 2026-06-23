---
kind: goal-progress
ticket_id: TASK-XXXX
status: active
created_at: 2026-06-12
template_id: goal-loop-progress
template_version: "0.1.0"
---

# TASK-XXXX Goal Progress

Append one entry per Goal turn, heartbeat, feedback resume, or drift checkpoint.
Keep entries compact. Use this file for after-turn reflection, compact
decision entries, drift notes, evidence links, and completion notes. Link
artifacts instead of pasting raw transcripts.

Create a sibling `decisions.md` only when material branching decisions, council
notes, or reusable architecture/API/data-model rationale would make this
chronological log hard to scan. Do not create an empty `decisions.md` by
default.

## Entry Template

```markdown
## 2026-06-12 HH:MM +0800 - turn N

- `trigger:` native_goal | scheduled_heartbeat | human_feedback_received | manual_resume
- `intent:`
- `actions:`
- `decision:` none | compact decision and rationale
- `files_changed:`
- `artifacts:`
- `metric_sample:`
- `feedback_sample:`
- `drift_verdict:` aligned | drifting | blocked | complete_candidate | not_run
- `drift_evidence:`
- `next_action:`
- `blocker:`
```

## Completion Entry Template

```markdown
## 2026-06-12 HH:MM +0800 - completion

- `completed_goal:`
- `proof:`
- `review_or_drift:`
- `portfolio_update:`
- `next_trigger:` start_child_goal | parent_heartbeat | manual_replan | complete
- `next_action:`
```
