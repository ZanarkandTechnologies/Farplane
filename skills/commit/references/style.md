# Commit Message Style

## Default Shape

`type(scope): summary`

Examples from repo style:

- `feat(cli): persist convex site url during setup`
- `refactor(skills): split skills panel content`
- `docs(team): replace proposal spec wording`

## Compression Rules

- lead with the main delta
- keep scope short: `cli`, `team`, `skills`, `docs`, `qa`
- use sharp verbs: `add`, `split`, `align`, `persist`, `retire`, `flatten`, `record`
- avoid filler: `update`, `misc`, `various`, `stuff`, `cleanup` unless it is truly cleanup

## Type Hints

- `feat` = new behavior / capability
- `fix` = bug fix
- `refactor` = structural change, same behavior intent
- `docs` = docs, rules, copy
- `chore` = maintenance / housekeeping
- `test` = test-only change
- `perf` = measurable performance change
- `build` = build/toolchain/package wiring
- `ci` = pipeline / automation
- `init` = first-time scaffold or bootstrap

## Output Preference

Default to one best subject.

Only add alternates when:

- type is ambiguous between `feat` / `refactor`
- scope could reasonably be 2 different things
- diff has one user-visible change and one structural change of similar weight
