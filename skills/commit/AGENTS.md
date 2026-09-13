# Commit Maintenance

## Scope

- `SKILL.md`
- `scripts/commit_staged.py`
- `scripts/test_commit_staged.py`
- `references/style.md`

## Boundaries

- Resolve and stage only the change the operator asked to commit.
- Use explicit paths for wholly owned files and cached patches for mixed files.
- Preserve unrelated staged and unstaged work.
- Commit locally; never push, amend, rebase, or rewrite history.

## Checks

- `python3 scripts/test_commit_staged.py`
- Confirm the final staged diff contains only the requested boundary.
- Confirm unrelated work remains after the commit.
