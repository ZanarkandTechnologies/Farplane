---
skill: solution-shaping
date: 2026-07-06
change_type: eval
owner: proof-advisor
status: pass
review_route: self_check
before_ref: skills/solution-shaping/eval_task.json
after_ref: skills/solution-shaping/eval_task.json
reasoning_basis: first_principles
proof_artifacts:
  - skills/solution-shaping/eval_task.json
eval_required: yes
---

# Skill Audit

## Change

- Before: Starter evals covered basic MVP brief, outreach uncertainty, and
  system-heavy routing.
- After: Eval rows cover quote-workflow V1, outreach inference guard,
  system-heavy handoff, AI-solution-bias negative control, and accepted-MVP
  execution gate.
- Why: The product-level skill must prove realistic MVP selection, assumption
  handling, and downstream handoff discipline.
- Tradeoff accepted: Five higher-signal eval rows instead of three broad smoke
  rows.

## Proof-Advisor QA

| Check | Verdict | Evidence |
| --- | --- | --- |
| `behavior_named` | pass | Each row targets one MVP workflow failure risk. |
| `source_traceable` | pass | Notes identify real thread failure, agency outreach use, user-provided workflow class, or synthetic anti-cheat gap. |
| `dimension_coverage` | pass | Ordinary path, outreach uncertainty, system-heavy handoff, AI-bias negative, and execution gate covered. |
| `proof_surface_fit` | pass | Skill behavior is variable; eval rows use explicit reference criteria. |
| `oracle_visible` | pass | Reference points define observable pass/fail criteria. |
| `query_not_spoiled` | pass | Queries do not name the skill, checklist, or eval internals. |
| `fixture_safe` | pass | No secrets, live systems, deploys, or private paths. |
| `diagnostic_value` | pass | Failures route to framing, MVP boundary, proof model, or handoff gates. |
| `batch_size_disciplined` | pass | Five distinct cases. |
| `maintenance_loop` | pass | Future real outreach/client failures should replace or extend rows by distinct failure mode. |

## Eval Query Review

- changed_files: `skills/solution-shaping/eval_task.json`
- reviewed_rows: 5
- reviewer: self
- query_spoiler_verdict: pass
- fixes_applied: added anti-cheat and execution-gate rows; sharpened failure
  owner notes and query naturalness
- deferrals: no independent reviewer lane
- remaining_risk: rows have not yet been run through the eval harness
