# Single-Worktree PR Publication

Use this route only when project policy keeps one shared checkout on local
`main` and the operator explicitly requests a pull request.

## Preconditions

- The checkout is on `main`; do not create or switch a local branch.
- One writer owns Git state. Other tasks are read-only until publication and
  merge synchronization finish.
- The requested change is already an isolated verified commit.
- `origin/main..HEAD` contains only the commit range intended for this PR. If a
  prior PR is still present in that range, stop instead of stacking work.
- The temporary remote branch does not already own unrelated history.

## Publish

```bash
git fetch origin main
git rev-list --left-right --count origin/main...HEAD
git push origin HEAD:refs/heads/codex/<task-name>
gh pr create --base main --head codex/<task-name> --title "<title>" --body-file <body-file>
```

The push creates or updates only the remote PR branch. It does not change the
local branch, worktree, or index. Verify the PR head SHA and file list after
creation.

## Merge And Synchronize

Use a merge commit so the local commit remains in remote `main` history:

```bash
gh pr merge <number> --merge
git fetch origin main
git merge --ff-only origin/main
```

Delete the remote temporary branch after merge when desired. Do not squash or
rebase this workflow's PR, push directly to `main`, switch branches, or begin
the next writing task before local `main` is synchronized.
