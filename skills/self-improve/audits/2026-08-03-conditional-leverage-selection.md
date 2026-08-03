---
skill: self-improve
date: 2026-08-03
change_type: harden_skill
owner: self-improve
status: accepted
review_route: reviewer
reasoning_basis: repeated coordination-cost evidence
eval_required: yes
proof_artifacts: [tickets/TASK-0428/ticket.md]
---

# Conditional leverage selection

> **Before:** Leverage Advisor was mandatory before every experiment.
> **After:** The active Goal owns `choose_next`; Leverage Advisor is called only
> for a real multi-option judgment and must beat outside options.

Structure checks: first-load sufficient; no state owner moved; tree-first
writeback and frozen-eval proof preserved. Focused behavior is A and completion
review is TAS-A; see `tickets/TASK-0428/artifacts/`.
