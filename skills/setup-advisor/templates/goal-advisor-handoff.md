---
kind: goal-advisor-handoff
status: draft
created_at: TODO
---

# Goal Advisor Handoff

## Files

- `ticket.md:`
- `program.md:`
- `progress.md:`
- `project_goals_or_harness_packet:`
- `other_source_files:`

## Task

```text
TODO
```

## Trigger

- `mode:` active_goal / heartbeat / feedback_loop / rollout / batch_goal / direct
- `why_this_mode:`

## Budget

- `time:`
- `token/model:`
- `compute:`
- `subagent:`
- `review:`
- `QA:`
- `feedback:`
- `spend:`

## Metric / Feedback Provider

- `provider:` mechanical / review / agent_qa / human_feedback / market / learning / hybrid
- `signal:`
- `minimum:`

## Drift Policy

- `drift_check:` inline / goal-drift-reviewer / reviewer / none
- `checkpoints:`
- `block_on_drift:`

## Side-Effect Gates

- `requires_approval:`
- `forbidden_until_approved:`

## Stop Conditions

- `complete_when:`
- `blocked_when:`
- `pause_when:`
- `escalate_when:`

## Native Goal Prompt Draft

```text
/goal Run the following files as one Goal Packet.
Files:
- TODO

Task: TODO
Logging: TODO
Metric: TODO
After each turn: TODO
```
