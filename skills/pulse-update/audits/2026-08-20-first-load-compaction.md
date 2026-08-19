---
skill: pulse-update
date: 2026-08-20
change_type: refinement
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: skills/pulse-update/SKILL.md@532-lines
after_ref: skills/pulse-update/SKILL.md@144-lines
reasoning_basis: first-principles low-value prose scan
proof_artifacts:
  - tickets/TASK-0441/artifacts/review/completion-review.md
  - skills/pulse-update/references/work-pulse-runbook.md
  - skills/pulse-update/evals/evals.json
  - skills/pulse-update/scripts/test_plan_wave_guard.py
eval_required: no
---

# Pulse Update First-Load Compaction

## Change

Conditional guard, reward, review, dispatch, refill, and receipt mechanics moved
to one always-routed runbook. The first load keeps the five-phase invariant,
signature, capacity and authority gates, eight-step wake path, clean-worker
boundary, finish artifact, and no-inline-execution rule.

## Low-Value Prose Decisions

- `move`: branch mechanics, command recipes, phase examples, and full receipt
  schema moved to the precise runbook loaded before every operated wake.
- `rewrite`: duplicate phase prose became concise executable todos.
- `delete`: repeated outcomes and explanatory prose already encoded in gates.
- `keep`: guard freshness, delayed reward ownership, review policy, clean task
  lineage, planner validation/materialization, caps, and bare JSON receipt.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| First-load sufficiency | pass | Default wake path and hard gates remain in `SKILL.md`. |
| Reference precision | pass | One mandatory runbook owns conditional mechanics. |
| Behavior preservation | pass | Focused tests passed; independent review returned TAS-A. |
| Surface budget | pass | 144 physical lines, below the 200-line hard cap. |
| Maintenance locality | pass | Changes stay in the Pulse package. |

No eval rerun is required for the behavior-preserving prose split; existing
TASK-0441 eval evidence and focused deterministic Pulse tests remain applicable.
