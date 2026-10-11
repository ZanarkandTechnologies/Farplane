# Commit

Create one local commit of everything changed in the shared checkout, labelled
by owner, and push it to `main` when asked.

## Public Entrypoints

- `SKILL.md`: sort changes by owner, stage everything, commit, push on request
- `references/style.md`: compact subject conventions
- `references/push-main.md`: the default publish route, straight to `main`
- `references/single-worktree-pr.md`: publish `HEAD` to a remote PR branch
  when the operator asks for a PR

## Boundary

The skill stages every change, including other threads' unfinished work, and
labels that work in the commit body instead of excluding it. When asked to
push, it pushes `main` straight to `origin/main` with a merge if needed; it opens
a PR only on request and never amends, rebases, force-pushes, or rewrites pushed
history.
