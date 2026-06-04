# Repent Skill

## Purpose

Provide an operator-visible recovery and lesson-capture mode for when the
assistant likely missed an obvious requirement, then optionally preserve the
fixed episode as a hardcase for future eval or training-data review.

## Entrypoint

- [SKILL.md](/Users/kenjipcx/coding-harness/Farplane/skills/repent/SKILL.md)

## Minimal Example

- User: `repent, you forgot to update the docs`
- Expected behavior: verify the miss, update the docs if the complaint is real,
  keep the first response action-oriented, then write a concise lesson when the
  fix is known.
- User: `repent hardcase, this is a good sample`
- Expected behavior: after the fix is known, create a sanitized artifact under
  `experiments/hardcases/`.

## How To Test

- review the fixtures in [fixtures.md](/Users/kenjipcx/coding-harness/Farplane/skills/repent/references/fixtures.md)
- run `python3 skills/skill-maintenance/scripts/check_skills.py --write`
- run `python3 bin/check_skill_todo_tiers.py --allow-peer-tier3`
