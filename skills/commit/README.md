# Commit

Create one local commit of this thread's named files in the shared checkout,
and push it to `main` when asked.

## Public Entrypoints

- `SKILL.md`: sort changes by owner, stage this thread's paths, commit, push on request
- `references/style.md`: compact subject conventions
- `references/push-main.md`: the default publish route, straight to `main`
- `references/single-worktree-pr.md`: publish `HEAD` to a remote PR branch
  when the operator asks for a PR

## Boundary

The skill stages only this thread's files and leaves other threads' changes
unstaged for their owners; a file both threads edited is committed whole with
the other thread's edit labelled. It never runs `git add -A`. When asked to
push, it pushes `main` straight to `origin/main` with a merge if needed; it opens
a PR only on request and never amends, rebases, force-pushes, or rewrites pushed
history.
