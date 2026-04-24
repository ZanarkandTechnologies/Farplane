# Gap Analysis

## Purpose

Ground one missing or partial feature in current repo reality plus production
expectation before `impl-plan` scopes the ticket.

## Public API / Entrypoints

- `SKILL.md`: main workflow contract
- `README.md`: module summary and test checklist
- `AGENTS.md`: maintenance notes

## Minimal Example

1. State the feature, user, and top job-to-be-done.
2. Read the local ticket, specs, and code to capture current state.
3. Inspect a few grounded comparables only after the repo limit is clear.
4. Write `Current state`, `Production expectation`, `Missing gaps`,
   `Comparable implementations`, and `Recommendation`.
5. Hand the result to `impl-plan`.

## How to Test

- Confirm `SKILL.md` says current repo state comes before external research.
- Confirm the output includes the five required sections.
- Confirm the boundary with `parity-research` and `runtime-debugging` is
  explicit.
