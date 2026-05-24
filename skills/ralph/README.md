# Ralph Skill Support

## Purpose

This package contains the public `$ralph` dispatcher contract and a small
read-only selector helper for filesystem ticket boards. The selector now uses
the canonical `FileTicketAdapter` and `ComputeSelector` contracts so Ralph's
serial queue choice matches Codexter invocation policy.

`$ralph` selects one eligible ticket or a safe related tiny-ticket batch and
hands the resulting work unit to `$work`. `$work` then decides whether to call
`impl-plan`, `$impl`, `close-ticket`, direct local work, reslicing, or another
owning surface. Ralph does not replace those skills and does not own parallel
execution in v0.

## Public API / Entrypoints

- `SKILL.md`: operator-facing serial dispatcher workflow
- `todos.md`: short anti-forgetting checklist for a Ralph run
- `references/parallel-ralph.md`: design-only future N-agent Ralph contract
  covering leases, worktrees, merge policy, stale recovery, and batch QA
- `scripts/select_next_ticket.py`: deterministic read-only selector and smoke
  helper; it emits selected/skipped rows with compute details and setup hints
  but does not mutate tickets or launch runners

## Minimal Example

```bash
python3 skills/ralph/scripts/select_next_ticket.py --root . --json
```

Then run the recommended skill on the selected ticket path.

In normal operator usage, pair Ralph with a native Goal when the board should
keep draining:

```text
/goal Drain the active ticket board until no eligible unblocked tickets remain.
After each selected work unit, reread the board. Stop only when all remaining
tickets are complete, archived, or blocked with evidence.

$ralph tickets/
```

If a ticket requests `local_worktree`, `symphony`, or `codex_cloud` before the
needed runtime or adapter exists, the selector stops with explicit blocker
codes instead of falling back to shared local compute.

## How to Test

- `python3 -m py_compile skills/ralph/scripts/select_next_ticket.py`
- `python3 skills/ralph/scripts/test_select_next_ticket.py`
- `python3 skills/ralph/scripts/select_next_ticket.py --root . --json`
