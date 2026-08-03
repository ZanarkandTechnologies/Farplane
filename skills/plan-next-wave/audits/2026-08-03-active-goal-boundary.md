---
skill: plan-next-wave
date: 2026-08-03
change_type: harden_skill
owner: plan-next-wave
status: accepted
review_route: reviewer
reasoning_basis: fragmented portfolio-versus-leaf ownership
eval_required: yes
proof_artifacts: [tickets/TASK-0428/ticket.md]
---

# Active Goal boundary

> **Before:** Portfolio selection was conceptually separate but insufficiently
> explicit about active Goal exclusion.
> **After:** Plan Next Wave runs only for empty-board refill and never joins a
> leaf Goal's `choose_next` loop.

Configured-skill selection, validation, and no-materialization behavior remain
unchanged. Contract validation and completion review are TAS-A; see
`tickets/TASK-0428/artifacts/`.
