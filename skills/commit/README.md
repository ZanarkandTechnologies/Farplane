# Commit

Create one verified local commit for the change the operator requested.

## Public Entrypoints

- `SKILL.md`: boundary discovery, isolated staging, commit, and verification
- `scripts/commit_staged.py`: deterministic commit of the isolated index
- `references/style.md`: compact subject conventions
- `references/single-worktree-pr.md`: publish `HEAD` to a remote PR branch
  without changing the shared local checkout

## Boundary

The skill may stage explicit paths or cached hunks owned by the requested
change. It preserves unrelated work. It pushes only when the operator requests
a PR and project policy permits the serial single-worktree route; it never
pushes directly to `main`, amends, rebases, or rewrites history.
