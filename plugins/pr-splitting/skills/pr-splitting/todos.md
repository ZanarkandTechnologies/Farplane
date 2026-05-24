# Todos

- [ ] Confirm the branch already works end to end before trying to split it.
- [ ] Pick the real merge target as the base branch.
- [ ] Try feature-first grouping before reaching for frontend/backend/infra buckets.
- [ ] Check whether each candidate PR can merge cleanly against base without depending on another PR.
- [ ] If feature-first is too entangled, switch to layer-based grouping instead of faking independence with hunks.
- [ ] Keep contract changes with their required consumers when backward compatibility is not real.
- [ ] Keep generated files, lockfiles, tests, and docs with the bucket that honestly owns them.
- [ ] Return exact file lists, size notes, blockers, and a refusal reason if a clean non-stacked split is not honest.
