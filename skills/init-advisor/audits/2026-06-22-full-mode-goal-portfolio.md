---
kind: skill-maintenance-audit
skill: init-advisor
created_at: 2026-06-22
change: full-mode-project-goals-readiness
status: complete
---

# Full-Mode Project Goals Readiness Audit

## Behavior Delta

`init-advisor` now distinguishes substrate setup from full project
initialization. Full mode must run a project-goals readiness pass, ask the
first missing operator-owned goal question, and avoid claiming
`project_initialized` while goals, success criteria, non-goals, or decision
boundaries are missing.

## Files Changed

- `skills/init-advisor/SKILL.md`
- `skills/init-advisor/references/BOOTSTRAP_BRIEF_TEMPLATE.md`
- `skills/init-advisor/references/GOALS_TEMPLATE.md`
- `skills/init-advisor/eval_task.json`

## Evidence

- Added eval case `init_advisor_full_mode_goal_intake_01`.
- Required focused checks:
  - `python3 -m json.tool skills/init-advisor/eval_task.json`
  - `python3 skills/skill-maintenance/scripts/check_skills.py --write`

## Remaining Risk

This change updates the skill contract and templates. It does not implement a
shell wizard in `scripts/bootstrap.sh`; the interactive/questioning behavior is
owned by the agent skill invocation.
