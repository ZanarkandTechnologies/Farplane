# Skill Validation

## Goal
- Prove skill metadata, todo-list shape, and generated skill registry outputs
  are coherent after skill edits.

## Fast Entry
- Route or deep link: n/a.
- Shortcut or debug control: n/a.
- Panel or mode to open directly: terminal at repo root.

## Setup
- Auth / fixture / seed: none.
- Reset path: do not reset; preserve unrelated dirty skill work.
- Commands:
  - `python3 skills/skill-maintenance/scripts/check_skills.py --write`
  - `python3 -m unittest skills.skill-maintenance.scripts.test_check_skills`

## Stable Selectors
- `data-testid`: n/a.
- Roles / labels: n/a.
- Assertion targets: command exit status and generated registry diff.

## Browser Path
1. Not applicable for skill file validation.

## Playwright Path
1. Not applicable unless validating a skill-owned UI.

## Observability
- `docs/skills/registry.jsonl`
- `.farplane/generated/graphs/*.json`
- Target `SKILL.md`, `qa_checklist.md`, and eval task files.

## Known Gaps
- Local project skills under `.agents/skills/` are intentionally not promoted
  to the root reusable skill registry unless a human-reviewed promotion happens.
