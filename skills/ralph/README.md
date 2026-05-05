# Ralph Skill Support

## Purpose

This package contains the public `$ralph` dispatcher contract and a small
read-only selector helper for filesystem ticket boards.

`$ralph` selects one eligible ticket at a time and hands it to `impl-plan`,
`$impl`, or `close-ticket`. It does not replace those phase skills and does not
own parallel execution in v0.

## Public API / Entrypoints

- `SKILL.md`: operator-facing serial dispatcher workflow
- `todos.md`: short anti-forgetting checklist for a Ralph run
- `references/parallel-ralph.md`: design-only future N-agent Ralph contract
  covering leases, worktrees, merge policy, stale recovery, and batch QA
- `scripts/select_next_ticket.py`: deterministic read-only selector and smoke
  helper

## Minimal Example

```bash
python3 skills/ralph/scripts/select_next_ticket.py --root . --json
```

Then run the recommended skill on the selected ticket path.

## How to Test

- `python3 -m py_compile skills/ralph/scripts/select_next_ticket.py`
- `python3 skills/ralph/scripts/test_select_next_ticket.py`
- `python3 skills/ralph/scripts/select_next_ticket.py --root . --json`
