---
skill: plan-next-wave
date: 2026-07-17
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: skills/plan-next-wave/SKILL.md@208-lines-free-form-proposal-planner
after_ref: skills/plan-next-wave/SKILL.md@119-lines-configured-skill-selector
reasoning_basis: operator_feedback_plus_local_eval
proof_artifacts:
  - tickets/TASK-0385/ticket.md
  - tickets/TASK-0385/artifacts/review/completion-review.md
eval_required: yes
---

# Configured Skill Calls Audit

## Change

- Before: Plan Next Wave invented lanes, proposal types, idea-card scoring,
  workflows, and full ticket specs.
- After: it may select only `harness.planning.skill_refs`, bind each selected
  skill's `planner_contract`, and return compact calls for Pulse to materialize.
- Deleted: the ticket-spec validator, Idea QA reference, proposal-type schema,
  and area-owned planner instructions.
- Preserved: objective attribution, evidence, proof, authority, dedupe,
  lifecycle safety, ranking, wave limits, and honest empty waves.

## First-Principles Placement

The failure was not insufficient scoring. The planner had authority to invent
the unit of work even though project skills already owned those workflows.
Selection now belongs to Plan Next Wave, workflow to the selected skill,
materialization to Pulse, and lifecycle/proof to the generic ticket.

Areas remain useful audience and metric context, but no longer generate work.
Historical `admitted_specs` are read-only evidence; new decisions write compact
`admitted_skill_calls` receipts.

## Lean Review

| Check | Result |
| --- | --- |
| First-load skill size | 208 -> 119 lines |
| Active planner schemas | one call contract plus one response envelope |
| Work-type registries | none added |
| Specialized ticket templates | none added |
| Duplicated workflow prose | removed from planner output |
| Human-interest claim | intentionally unproven until simulated/live review |

## Proof Plan

- Deterministic valid, invalid, duplicate, legacy-shape, empty-wave, and
  materialization-boundary tests.
- Pulse guard, board, and ticket-history receipt tests.
- Project-file validation proving the configured allowlist resolves.
- Skill maintenance checks and independent reviewer verdict.
- Delayed human simulation remains owned by `TASK-0384`; validator success
  must not be reported as improved taste.
