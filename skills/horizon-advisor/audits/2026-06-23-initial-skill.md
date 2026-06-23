---
kind: skill-audit
skill: horizon-advisor
status: pass
created_at: 2026-06-23
review_route: deliberative_advice
reasoning_basis:
  - user-requested skill creation
  - local goal-advisor boundary review
  - harness-algebra objective function review
proof_artifacts:
  - python3 skills/skill-maintenance/scripts/check_skills.py --write
---

# Horizon Advisor Initial Skill Audit

## Change

Created `horizon-advisor` as the strategy and KPI authoring owner for
long-horizon Farplane goals, and moved the long project-goals reference out of
`goal-advisor`.

## Checklist

- [x] Stable trigger: ambiguous long-horizon strategy, KPI tree, goals.md, and
  portfolio authoring.
- [x] Separate from neighbors: `goal-advisor` compiles selected frontiers into
  Goal Packets; `horizon-advisor` decides what frontier should exist.
- [x] First-load sufficiency: `SKILL.md` includes trigger, signature, todo path,
  value-function model, gotchas, output, and execution handoff boundary.
- [x] Reference routing: long portfolio detail is in
  `references/project-goals.md` and loaded only for material project-goals edits.
- [x] Proof named: skill registry validation is the mechanical proof for the
  package shape.
- [x] Dissent preserved: the main risk is duplicating existing
  `goal-advisor` portfolio logic; mitigated by moving the reference and leaving
  a compatibility pointer.

## Follow-Up

Add a focused `eval_task.json` after the first two real uses reveal the common
failure modes for strategy authoring.
