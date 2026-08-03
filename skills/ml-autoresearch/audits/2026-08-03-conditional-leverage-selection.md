---
skill: ml-autoresearch
date: 2026-08-03
change_type: harden_skill
owner: ml-autoresearch
status: accepted
review_route: reviewer
reasoning_basis: repeated coordination-cost evidence
eval_required: yes
proof_artifacts: [tickets/TASK-0428/ticket.md]
---

# Conditional leverage selection

> **Before:** Every experiment traversed Leverage Advisor regardless of choice.
> **After:** The Goal executes an implied move directly and calls Leverage
> Advisor only when several credible experiments require comparison.

Evaluator freezing, causal-diagnosis gates, tree ownership, append-only
receipts, and budget checks remain unchanged. Focused behavior is A and
completion review is TAS-A; see `tickets/TASK-0428/artifacts/`.
