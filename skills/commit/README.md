# Commit

Create one verified local commit for the change the operator requested.

## Public Entrypoints

- `SKILL.md`: boundary discovery, isolated staging, commit, and verification
- `scripts/commit_staged.py`: deterministic commit of the isolated index
- `references/style.md`: compact subject conventions

## Boundary

The skill may stage explicit paths or cached hunks owned by the requested
change. It preserves unrelated work and never pushes, amends, rebases, or
rewrites history.
