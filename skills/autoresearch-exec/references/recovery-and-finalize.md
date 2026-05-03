# Recovery and Finalize

## Session Recovery

If a previous agent stopped mid-run:

- dirty editable files with no experiment commit: discard only those in-scope
  experiment edits after confirming they are not user work
- last commit is `experiment(...)` and has no JSONL run entry: verify it or
  revert it before continuing
- clean tree and latest commit has a JSONL entry: resume normally

When unsure whether dirty changes are user work, stop and ask.

## Updating `autoresearch.md`

Update the session program after:

- a new best metric
- three or more repeated failures in one area
- a strategy shift
- a discovered constraint that future agents must know

Keep updates short. Do not paste raw logs.

## Finalizing a Run

When the user asks to finalize:

1. Read kept runs from `autoresearch.jsonl`.
2. Group kept commits by logical theme and changed files.
3. Preserve application order.
4. Do not split groups that touch the same files or depend on one another.
5. Produce a concise branch/PR plan from the merge-base.

Do not implement a Pi-style branch splitter in v1. Treat finalize as a
documented handoff until a dedicated helper is added.

