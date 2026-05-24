# PR Splitting Output Template

Use this shape when handing the result back to the user or ticket.

```md
## PR Split Plan

- Base branch: `main`
- Split strategy: `feature-first` | `layer-fallback` | `refuse`
- Why this strategy won:

### PR 1: short name
- Reviewer story:
- Why independent:
- Exact files:
  - `path/to/file`
  - `path/to/dir/*`
- Approx size:
- Risk notes:

### PR 2: short name
- Reviewer story:
- Why independent:
- Exact files:
  - `path/to/file`
- Approx size:
- Risk notes:

## Blockers
- none

## Branch Steps
1. branch from `main`
2. move only the listed files for PR 1
3. open PR 1
4. repeat for the remaining buckets
```

## Notes

- Replace `Split strategy` with `refuse` when a clean non-stacked split would be
  dishonest.
- `Exact files` is required; do not substitute a vague folder summary alone.
- `Why independent` should name mergeability against base, not just thematic
  similarity.
