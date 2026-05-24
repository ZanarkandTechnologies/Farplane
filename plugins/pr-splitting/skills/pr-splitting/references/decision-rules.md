# PR Splitting Decision Rules

Use these rules after the main skill workflow is loaded.

## Decision Order

1. `Mergeability`
   - Can this PR merge against the base branch by itself?
   - If not, it is not an honest non-stacked PR bucket.
2. `Reviewer story`
   - Does the PR tell one coherent story that a reviewer can evaluate without
     reading another pending PR first?
3. `Ownership clarity`
   - If feature-first fails, does a layer-based split create clear ownership?
4. `Size pressure`
   - Keep PRs under the soft target when possible, but never by sacrificing the
     first three rules.
5. `Shared-file minimization`
   - If two valid options remain, choose the one with fewer shared files.

## Feature-First vs Layer-Fallback

- Prefer feature-first when the bucket can hold the full end-to-end story:
  backend, frontend, tests, docs, and config together if needed.
- Fall back to technical seams like `frontend`, `backend`, `schema`, `infra`,
  `tooling`, or `docs` when feature slicing would create too much cross-bucket
  coupling.
- Do not move to layer buckets just because they are easier to describe; they
  need to improve honesty or reviewer clarity.

## Coupling Rules

- Keep contract changes together with non-backward-compatible consumers.
- Shared routes, schemas, types, and configs belong with the bucket that owns
  the public contract, unless that still leaves another bucket dishonest.
- If the same file is materially needed by multiple candidate PRs, either give
  it one clear owner or treat it as a blocker.

## File-Ownership Rules

- Generated files follow the human-authored source of truth.
- Lockfile or config churn follows the dependency or tooling change that caused
  it.
- Colocated tests follow the behavior they validate.
- Broad integration tests follow the first bucket that introduces the meaningful
  cross-surface behavior.
- Docs usually travel with the code change they describe unless they are
  independently reviewable.

## Refactor Rules

- Isolate a mechanical prep PR only when the refactor is truly mechanical and
  independently reviewable.
- If the refactor is necessary to understand the behavior change, keep it with
  that behavior bucket.
- Do not create a vague cleanup PR to hide uncertainty.

## Refusal Conditions

Refuse or recommend fewer PRs when:

- every plausible split creates hidden dependencies
- the branch depends on hunk surgery across the same files
- contract changes and consumers cannot stay compatible with base
- the resulting PRs would be smaller but less honest
