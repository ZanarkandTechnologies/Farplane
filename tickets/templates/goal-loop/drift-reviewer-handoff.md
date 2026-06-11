---
kind: goal-drift-reviewer-handoff
ticket_id: TASK-XXXX
status: draft
created_at: 2026-06-12
---

# TASK-XXXX Drift Reviewer Handoff

## Inputs

- `ticket:` `tickets/TASK-XXXX/ticket.md`
- `program:` `tickets/TASK-XXXX/program.md`
- `progress:` `tickets/TASK-XXXX/progress.md`
- `progress_tail:` latest 1-3 entries
- `current_claim:` what the main agent believes it should do next

## Task

Compare the current claim and latest progress against the ticket contract and
Goal program. Do not edit files. Do not plan implementation. Return an
alignment verdict with evidence and the smallest recovery constraint.

## Output

```json
{
  "verdict": "aligned | drifting | blocked | complete_candidate",
  "reason": "",
  "objective_delta": [],
  "scope_delta": [],
  "evidence_gap": [],
  "contract_refs": [],
  "recovery_action": "",
  "next_action_constraint": ""
}
```
