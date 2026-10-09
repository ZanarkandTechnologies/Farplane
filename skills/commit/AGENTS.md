# Commit Maintenance

## Scope

- `SKILL.md`
- `scripts/commit_staged.py`
- `scripts/test_commit_staged.py`
- `references/style.md`
- `references/push-main.md`
- `references/single-worktree-pr.md`

## Boundaries

- Resolve and stage only the change the operator asked to commit.
- Use explicit paths for wholly owned files and cached patches for mixed files.
- Preserve unrelated staged and unstaged work.
- Commit locally first. When asked to push, push `main` straight to
  `origin/main` (merge, never rebase or force). Open a PR only on request. Never
  switch local branches, amend, or rewrite pushed history.

## Checks

- `python3 scripts/test_commit_staged.py`
- Confirm the final staged diff contains only the requested boundary.
- Confirm unrelated work remains after the commit.
- After a push, confirm `origin/main` equals `HEAD` and unrelated work is
  unchanged.
