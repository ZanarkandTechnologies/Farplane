---
kind: native-goal-prompt
ticket_id: TASK-0406
compiled_from_ticket_updated_at: 2026-07-25T23:04:13+08:00
approval: approved
---

# TASK-0406 Native Goal Prompt

```text
/goal Run the following files as one Goal Packet.
Files:
- tickets/TASK-0406/ticket.md
- tickets/TASK-0406/program.md
- tickets/TASK-0406/progress.md
- tickets/TASK-0406/diagrams.md
- tickets/archive/TASK-0405/ticket.md
- tickets/archive/TASK-0405/progress.md
- farplane/harness.yaml
- farplane/metrics.yaml
- docs/features/FEAT-0007-ticket-as-durable-task-memory.md
- docs/features/FEAT-0063-metric-advisor-cards.md
- docs/features/FEAT-0067-daily-interval-review-reports.md
- docs/features/FEAT-0071-project-work-pulse.md
- docs/systems/horizon-loop.md

First read tickets/TASK-0406/program.md; it is the executable loop policy.
Then read the ticket as the scope, acceptance, and proof contract. Use
progress.md as append-only state. Reconcile existing dirty changes and preserve
the archived TASK-0405 highlight behavior.

Task: Complete every TASK-0406 Scope: In and Done condition as one
no-compatibility migration. Follow the ticket's six changes and ordered sanity
checks. Scope: Out wins on conflict.

Logging: Before ending each turn, append actions, files, verification, drift,
blockers, and next action to progress.md.

Metric: All Done conditions, ordered checks, integrated fixtures, delegated
agent QA, docs validation, and TAS-A evidence/completion reviews must pass.
Self-certification is forbidden for delegated proof.

Grounding: This is an explicitly local-only Farplane ownership/schema
consolidation; final evidence must name the local code, tests, ticket, and
canonical docs checked.

After each turn: compare ticket, program, progress, and current diffs; request
goal-drift-reviewer at program checkpoints; continue while useful or stop
blocked with the exact unresolved condition.

Final checkpoint: validate the active ticket with an explicit changed-path
boundary; run the QA evidence review and completion review; write the strongest
receipts to ticket Links, progress, and artifacts. Only after both reviews
reach TAS-A, run `farplane ticket close TASK-0406`. Final response must include
Ticket, Verification, Artifacts, Grounding, and Residual risk.

Approval: approved by the operator on 2026-07-25 for full-ticket execution.
```
