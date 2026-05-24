# goal-crafter

## Purpose

`goal-crafter` turns fuzzy operator intent into a paste-ready native Codex
`/goal` command with an outcome, proof surface, constraints, boundaries,
iteration policy, and blocked-stop condition.

It can draft Goal contracts for `$work`, `$ralph`, `batch-work`, metric loops,
and figure-it-out unblock runs.

## Public API

- `SKILL.md`: the loaded skill contract.
- `todos.md`: the checklist used while drafting a goal.

## Minimal Example

Ask for a goal when the desired outcome is clear enough to pursue, but the
stopping rule is still soft:

```text
Use goal-crafter to turn "make this demo work even if I am away" into a
paste-ready /goal.
```

## How to Test

```bash
python3 skills/skill-maintenance/scripts/check_skills.py --write
python3 skills/skill-maintenance/scripts/generate_skill_graph.py
```
