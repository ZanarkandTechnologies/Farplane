---
skill: content-impl-plan
date: 2026-08-07
change_type: structure
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: tickets/TASK-9019/ticket.md
after_ref: skills/content-impl-plan/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - skills/content-impl-plan/scripts/test_validate_production_program.py
  - docs/skills/composition.md
eval_required: no
---

# Skill Audit: Composable Plan Contract

## Change

- Before: Content Impl Plan's 8-node todo and QA restated final storyboard,
  asset, realization, editing, rendering, and review detail.
- After: It produces one `CONTENT_PRODUCTION_PLAN` with five domain nodes and
  delegates each child output to its sole owner.
- Why: The parent must compile the full artifact-birth route without becoming a
  second implementation lane.
- Tradeoff accepted: Detailed production rules remain in conditional references
  and child contracts rather than always loading with the planner.

## First-Principles Reasoning

- Objective: preserve the complete production plan while making ownership and
  handoff inspectable.
- Placement logic: shared grammar belongs in `docs/skills/`; the planner's
  child graph belongs in its own package; deterministic graph shape belongs in
  its existing validator.
- Expected behavior delta: a content request now returns one named plan and
  action graph, not an ambiguous bundle of child artifacts.
- Proof needed: schema tests, registry/template validation, and independent
  review of ownership boundaries.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | five-node Todo List plus conditional references |
| `reference_load_precision` | pass | selected content-type references remain named |
| `duplicated_instruction_count` | pass | child-artifact detail removed from planner todo/QA |
| `maintenance_locality` | pass | contract/system/template own shared behavior |
| `composition_clarity` | pass | `CONTENT_PRODUCTION_PLAN` and `AdvisorAction` schema |
| `proof_surface_fit` | pass | deterministic validator tests; reviewer for ownership |

## Proof Artifacts

- Validator: `python3 -m unittest skills/content-impl-plan/scripts/test_validate_production_program.py skills/content-impl-plan/scripts/test_verify_scene_direction.py` (12 passing tests)
- Structure: `python3 skills/skill-maintenance/scripts/check_skills.py --write`
- Eval required: no; the change is contract/schema normalization and existing
  routed cases already cover the sibling sequence and missing media boundary.
- Ticket validation: `farplane validate ticket tickets/TASK-9019/ticket.md --phase complete --path ...` passed all 7 selected checks.
- Reviewer receipt: `tickets/TASK-9019/artifacts/review.md` (`TAS-A`); its
  non-blocking terminology finding was repaired before closeout.
