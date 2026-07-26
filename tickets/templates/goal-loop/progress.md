---
kind: goal-progress
ticket_id: TASK-XXXX
status: active
created_at: 2026-06-12
template_id: goal-loop-progress
template_version: "0.1.1"
feature_refs:
  - FEAT-0029
  - FEAT-0032
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

## Review

Add this block only while the ticket is `status: awaiting_review`. It is the
mutable reminder and reply-routing ledger; frontmatter remains lifecycle-only.

```yaml
artifact_refs: []
thread_ref:
requested_at:
next_reminder_at:
reminder_count: 0
escalation_used: false
decision:
```

Remove the next reminder or fill `decision` when feedback arrives. The replying
thread updates this block and the ticket status without occupying a worker while
waiting.

## Entry Template

```markdown
## 2026-06-12 HH:MM +0800 - turn N

- `trigger:` native_goal | scheduled_heartbeat | human_feedback_received | manual_resume
- `intent:`
- `action:`
- `observation:`
- `evidence:`
- `decision:` none | compact decision and rationale
- `learning:`
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
