---
skill: problem-framing
date: 2026-07-06
change_type: eval
owner: proof-advisor
status: pass
review_route: self_check
before_ref: skills/problem-framing/eval_task.json
after_ref: skills/problem-framing/eval_task.json
reasoning_basis: first_principles
proof_artifacts:
  - skills/problem-framing/eval_task.json
eval_required: yes
---

# Skill Audit

## Change

- Before: Starter evals covered obvious happy paths and lightly leading
  requests.
- After: Eval rows cover requested-artifact trap, sparse complaint, first-
  principles reset, platform-overbuild negative control, and already-framed
  handoff boundary.
- Why: The skill's critical behavior is resisting wrong problem/product
  selection, not simply producing a tidy frame.
- Tradeoff accepted: Five higher-signal eval rows instead of three broad smoke
  rows.

## Proof-Advisor QA

| Check | Verdict | Evidence |
| --- | --- | --- |
| `behavior_named` | pass | Each row targets one failure risk. |
| `source_traceable` | pass | Notes identify real thread failure, Jensen source, boundary, or synthetic gap. |
| `dimension_coverage` | pass | Ordinary trap, sparse input, reset, anti-overbuild, and handoff boundary covered. |
| `proof_surface_fit` | pass | Skill behavior is variable; eval rows use explicit reference criteria. |
| `oracle_visible` | pass | Reference points expose success criteria and failure owner. |
| `query_not_spoiled` | pass | Queries avoid naming the skill or checklist and sound like operator requests. |
| `fixture_safe` | pass | No secrets, live systems, deploys, or private paths. |
| `diagnostic_value` | pass | Failures route to skill contract gates. |
| `batch_size_disciplined` | pass | Five distinct cases. |
| `maintenance_loop` | pass | Future failures should replace or extend rows by distinct failure mode. |

## Eval Query Review

- changed_files: `skills/problem-framing/eval_task.json`
- reviewed_rows: 5
- reviewer: self
- query_spoiler_verdict: pass
- fixes_applied: removed skill-name-leading language and added anti-cheat and
  boundary cases
- deferrals: no independent reviewer lane
- remaining_risk: rows have not yet been run through the eval harness
