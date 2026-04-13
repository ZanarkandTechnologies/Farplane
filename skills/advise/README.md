# Advise

## Purpose

Guide agents to act like a reliable consultant when the user has not already chosen a direction.

## Public API / Entrypoints

- `SKILL.md`: main decision-framing contract
- `AGENTS.md`: maintenance rules

## Minimal Example

1. State the decision.
2. Compare 3 viable options with pros and cons.
3. Recommend one option and the accepted tradeoff.
4. State the next step directly.

## How to Test

- Confirm the output contains 3 options.
- Confirm one option is explicitly recommended.
- Confirm the answer does not end with "if you want I can ...".
