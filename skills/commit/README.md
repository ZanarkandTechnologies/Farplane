# Commit

Create one verified local commit for the change the operator requested.

## Public Entrypoints

- `SKILL.md`: boundary discovery, isolated staging, commit, and verification
- `scripts/commit_staged.py`: deterministic commit of the isolated index
- `references/style.md`: compact subject conventions
- `references/push-main.md`: the default publish route, straight to `main`
- `references/single-worktree-pr.md`: publish `HEAD` to a remote PR branch
  when the operator asks for a PR

## Boundary

The skill may stage explicit paths or cached hunks owned by the requested
change. It preserves unrelated work. When asked to push, it pushes `main`
straight to `origin/main` with a merge commit if needed; it opens a PR only on
request and never amends, rebases, force-pushes, or rewrites pushed history.
