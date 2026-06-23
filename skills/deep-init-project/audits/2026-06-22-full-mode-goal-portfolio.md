---
kind: skill-maintenance-audit
skill: deep-init-project
created_at: 2026-06-22
change: full-mode-project-goals-readiness
status: complete
---

# Full-Mode Project Goals Readiness Audit

## Behavior Delta

`deep-init-project` now distinguishes substrate setup from full project
initialization. Full mode must run a project-goals readiness pass, ask the
first missing operator-owned goal question, and avoid claiming
`project_initialized` while goals, success criteria, non-goals, or decision
boundaries are missing.

## Files Changed

- `skills/deep-init-project/SKILL.md`
- `skills/deep-init-project/references/BOOTSTRAP_BRIEF_TEMPLATE.md`
- `skills/deep-init-project/references/GOALS_TEMPLATE.md`
- `skills/deep-init-project/eval_task.json`

## Evidence

- Added eval case `deep_init_project_full_mode_goal_intake_01`.
- Required focused checks:
  - `python3 -m json.tool skills/deep-init-project/eval_task.json`
  - `python3 skills/skill-maintenance/scripts/check_skills.py --write`

## Remaining Risk

This change updates the skill contract and templates. It does not implement a
shell wizard in `scripts/bootstrap.sh`; the interactive/questioning behavior is
owned by the agent skill invocation.
