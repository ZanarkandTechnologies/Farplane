# Commit Maintenance

## Scope

- `SKILL.md`
- `scripts/commit_staged.py`
- `scripts/test_commit_staged.py`
- `references/style.md`

## Boundaries

- Commit exactly the staged boundary; never stage, push, amend, or rebase.
- Keep subject selection compact and repository-aware.
- Return `no_staged_changes` without mutation when the index is empty.

## Checks

- `python3 scripts/test_commit_staged.py`
- Confirm the helper contains no stage or push Git command.
