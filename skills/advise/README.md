# Advise

## Purpose

Guide agents to act like a reliable consultant when the user has not already chosen a direction.

## Public API / Entrypoints

- `SKILL.md`: main decision-framing contract
- `AGENTS.md`: maintenance rules
- `SKILL.md` Todo List: Tier 1 decision checklist

## Minimal Example

1. State the decision.
2. Name the first-principles basis: objective, need, root cause, constraints,
   assumptions, proof, tradeoffs, and non-goals.
3. Compare 3 viable options with pros and cons.
4. Recommend one option and the accepted tradeoff.
5. State the next step directly.

## How to Test

- Confirm the output contains 3 options.
- Confirm the options are grounded in first-principles basis rather than only
  surface preference.
- Confirm one option is explicitly recommended.
- Confirm fact-dependent recommendations are grounded through
  `reference-grounding` or `research:*`.
- Confirm the answer does not end with "if you want I can ...".
