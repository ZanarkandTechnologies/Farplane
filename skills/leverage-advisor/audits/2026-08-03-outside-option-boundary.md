---
skill: leverage-advisor
date: 2026-08-03
change_type: harden_skill
owner: leverage-advisor
status: accepted
review_route: reviewer
reasoning_basis: fragmented next-decision ownership
eval_required: yes
proof_artifacts: [tickets/TASK-0428/ticket.md]
---

# Outside-option boundary

> **Before:** The skill ranked candidate moves without a mandatory comparison
> to reporting, feedback, or stopping.
> **After:** Invocation requires a real multi-option judgment and the winning
> move must beat `report_now`, `request_feedback`, and `stop`.

Execution and state ownership remain with the caller. Focused behavior is A and
completion review is TAS-A; see `tickets/TASK-0428/artifacts/`.
