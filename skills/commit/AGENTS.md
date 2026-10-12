# Commit Maintenance

## Scope

- `SKILL.md`
- `evals/evals.json`
- `references/style.md`
- `references/push-main.md`
- `references/single-worktree-pr.md`

## Boundaries

- Stage this thread's named paths only, never `git add -A`; leave other
  threads' changes unstaged and label another thread's edit inside a shared file.
- Commit locally first. When asked to push, push `main` straight to
  `origin/main` (merge, never rebase or force). Open a PR only on request. Never
  switch local branches, amend, or rewrite pushed history.
- The pre-push secret and private-data scan always blocks on a public repo.

## Checks

- Before a commit, `git diff --cached --name-only` equals this thread's paths.
- After a commit, other threads' changes are still unstaged.
- After a push, confirm `origin/main` equals `HEAD`.
