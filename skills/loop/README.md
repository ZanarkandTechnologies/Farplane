# Loop

## Purpose

Provide the operator-facing contract for the lightweight `$loop` control
surface.

## Public API / Entrypoints

- `SKILL.md`: main `$loop` invocation and guardrail contract
- `README.md`: module summary and test checklist
- `AGENTS.md`: maintenance notes

## Minimal Example

1. Start the prompt with `$loop`.
2. Add either `done_when=[...]` or `completion_marker=...`.
3. Add `retry_message=...` so the same session knows what to keep doing.
4. Stop with `stop loop`, `cancel loop`, `exit loop`, or `$loop stop`.

## How to Test

- Confirm `SKILL.md` distinguishes `$loop` from `impl-plan` and `$impl`.
- Confirm the examples only use the shipped local predicates.
- Confirm the stop contract names explicit same-session stop intent, not Escape.
