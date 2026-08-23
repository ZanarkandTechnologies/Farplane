# Commit

Create one verified local commit from changes the operator already staged.

## Public Entrypoints

- `SKILL.md`: staged-boundary contract
- `scripts/commit_staged.py`: deterministic local commit helper
- `references/style.md`: compact subject conventions

## Boundary

The skill never stages files or pushes. An empty index produces
`no_staged_changes` and leaves the repository untouched.
