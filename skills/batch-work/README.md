# Batch Work Skill Support

## Purpose

`batch-work` executes an explicit operator-supplied ticket range or list in one
unattended pass. It is useful for solo-local work where many small known
tickets would otherwise repeat setup, planning, and review overhead.

It stays separate from `$ralph`: `batch-work` runs a named range/list, while
`$ralph` reads a board and decides what work unit to select next.

## Public API / Entrypoints

- `SKILL.md`: operator-facing batch workflow
- `SKILL.md` Important Checklist: anti-forgetting checklist for batch ledger, blockers, and review

## Minimal Example

```text
batch-work TASK-0201 TASK-0202 TASK-0203
```

## How to Test

```bash
python3 skills/skill-maintenance/scripts/check_skills.py --write
```

