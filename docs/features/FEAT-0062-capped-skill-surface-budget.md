---
title: Capped skill surface budget
status: implemented
owner: feature-registry
created_at: 2026-06-28
updated_at: 2026-06-28
tags:
  - farplane
  - feature
  - sys-0006
refs:
  - docs/features/FEAT-0062-capped-skill-surface-budget.md
  - docs/skills/system.md
  - docs/skills/templates/SKILL_TEMPLATE.md
  - docs/skills/templates/QA_CHECKLIST_TEMPLATE.md
  - bin/validators/check_skill_surface_budget.py
  - skills/skill-maintenance/scripts/minimize_skill_surface.py
  - skills/skill-maintenance/scripts/check_skills.py
feature_id: FEAT-0062
system_id: SYS-0006
category: skills
public: true
surfaces:
  - docs/features/FEAT-0062-capped-skill-surface-budget.md
  - docs/skills/system.md
  - docs/skills/templates/SKILL_TEMPLATE.md
  - docs/skills/templates/QA_CHECKLIST_TEMPLATE.md
  - bin/validators/check_skill_surface_budget.py
  - skills/skill-maintenance/scripts/minimize_skill_surface.py
  - skills/skill-maintenance/scripts/check_skills.py
source_refs:
  - tickets/archive/TASK-0221/ticket.md
  - skills/consolidate/SKILL.md
  - skills/skill-maintenance/SKILL.md
external_refs: []
evidence_refs:
  - bin/validators/test_check_skill_surface_budget.py
  - tickets/archive/TASK-0221/ticket.md
known_limits: Opt-in scanner only. Existing skills are not globally capped, and over-budget skill consolidation remains a skill-maintenance refinement decision rather than an automatic rewrite.
metrics:
  - skill_surface_budget_pass
  - capped_skill_subscription_count
last_verified: 2026-06-28
---
# Capped skill surface budget

Capped skill surface budget gives maintainers a mechanical way to keep
high-leverage skill todos, skill-local QA checklists, and skill-local eval rows
small enough for agents to actually use. It belongs to
[Skill System](../systems/skill-system.md) and keeps `FEAT-0062` as the feature
handle for opt-in budget enforcement.

```text
skill_surface_budget(skill, template_uses, limits)
  -> pass | violation(minimizer_command) | skipped
```

## At A Glance

- Feature ID: `FEAT-0062`
- System: [Skill System](../systems/skill-system.md)
- Status: `implemented`
- Category: `skills`
- Primary user: skill maintainer
- Job: cap subscribed skill surfaces at `10` top-level todos, `5` QA checklist
  items, and `5` eval tasks.

## Problem

Skill checklists and eval rows grow because adding a new item is easier than
choosing what matters most. Long lists cost context and do not guarantee that
agents apply every item.

## What It Does

- Treats `template_uses.skill-surface-budget: "0.1.0"` as the opt-in
  subscription.
- Checks subscribed skills against `10 / 5 / 5` budgets for top-level
  `SKILL.md` todos, `qa_checklist.md` items, and `eval_task.json` rows.
- Skips unsubscribed skills without warnings so rollout can happen gradually.
- Reports exact minimizer commands for over-budget subscribed skills.
- Uses `skill-maintenance.refine_skill` and `consolidate(..., structure =
  skill)` for value-preserving compaction before enrolling over-budget skills.

## User Stories

- As a maintainer, I can enroll only the skills ready for capped-surface
  enforcement.
- As an operator, I can see when a skill exceeds the useful checklist budget
  without being flooded by warnings from every legacy skill.

## Operating Contract

Subscribed skills declare the feature through `template_uses`:

```yaml
template_uses:
  skill-surface-budget: "0.1.0"
```

The validator is deterministic. It counts only top-level numbered skill todos,
top-level Markdown checkbox items in `qa_checklist.md`, and skill-local eval
rows. It does not judge item quality or rewrite files.

When a subscribed skill is over budget, the maintainer runs the minimizer
worksheet and then applies `skill-maintenance.refine_skill` before keeping the
subscription.

## Surfaces

Owner surfaces:

- `bin/validators/check_skill_surface_budget.py`
- `skills/skill-maintenance/scripts/minimize_skill_surface.py`
- `skills/skill-maintenance/scripts/check_skills.py`

Supporting surfaces:

- `docs/skills/system.md`
- `docs/skills/templates/SKILL_TEMPLATE.md`
- `docs/skills/templates/QA_CHECKLIST_TEMPLATE.md`
- `tickets/archive/TASK-0221/ticket.md`

## Proof And Quality

Required checks:

- `python3 -m unittest bin/validators/test_check_skill_surface_budget.py`
- `python3 bin/validators/check_skill_surface_budget.py`
- `python3 skills/skill-maintenance/scripts/check_skills.py --write`

Acceptance signals:

- Subscribed Seed A and Seed B skills pass the budget scanner.
- Unsubscribed skills are skipped without warnings.
- Over-budget fixtures fail with a minimizer command.

## Rollout And Maintenance

- Update path: add `template_uses.skill-surface-budget: "0.1.0"` only after the
  skill fits `10 / 5 / 5`.
- Rollback path: remove the `skill-surface-budget` template use or remove the
  scanner call from `check_skills.py`.
- Compatibility notes: raw `feature_refs` are not skill frontmatter; use
  `template_uses` for this structural adoption marker.
- Maintenance owner: `skill-maintenance`.

## Limits And Non-Goals

- This feature does not auto-rewrite skills.
- This feature does not globally enforce all existing skills.
- This feature does not prove the selected top items are semantically best;
  that judgment stays with `skill-maintenance.refine_skill`, `consolidate`, and
  review.

## Alternatives Considered

- Option: Add raw `feature_refs` to skills.
  Decision: reject.
  Reason: current skill registry validation rejects direct skill
  `feature_refs`; structural adoption belongs in template metadata.

- Option: Enforce all skills immediately.
  Decision: reject.
  Reason: the existing skill tree has useful legacy bloat and should not start
  failing unrelated work.

## Change History

- 2026-06-28: Created and implemented with opt-in scanner, minimizer, and Seed
  A/B rollout.
