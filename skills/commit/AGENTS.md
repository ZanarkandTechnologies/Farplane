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
- Commit locally first. Push only for an explicit PR through the serial
  single-worktree route; never push directly to `main`, switch local branches,
  amend, rebase, or rewrite history.

## Checks

- `python3 scripts/test_commit_staged.py`
- Confirm the final staged diff contains only the requested boundary.
- Confirm unrelated work remains after the commit.
- For requested PR publication, confirm local `main` and the index remain
  unchanged while `HEAD` is pushed to the temporary remote branch.
