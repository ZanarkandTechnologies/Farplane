# Commit Maintenance

## Scope

- `SKILL.md`
- `evals/evals.json`
- `references/style.md`
- `references/push-main.md`
- `references/single-worktree-pr.md`

## Boundaries

- Stage every change in the shared checkout; label other threads' work in the
  commit body instead of excluding it.
- Commit locally first. When asked to push, push `main` straight to
  `origin/main` (merge, never rebase or force). Open a PR only on request. Never
  switch local branches, amend, or rewrite pushed history.
- The pre-push secret and private-data scan always blocks on a public repo.

## Checks

- After a commit, the index matches `HEAD` and the body names other threads'
  included work.
- After a push, confirm `origin/main` equals `HEAD`.
