# Research

## Purpose

Provide one Tier 2 evidence workflow with explicit method addresses instead of
separate same-level research wrapper skills.

## Public API / Entrypoints

- `research:parity`: peer norms, standards, and reference implementations
- `research:gap`: local missing or partial feature scope versus production
  expectation
- `research:competitor`: named product or workflow comparison
- `research:official-docs`: official API, platform, protocol, or standard
  behavior
- `research:code-patterns`: literal-code discovery plus maintained-repository
  deep dives, file maps, tests/failures, comparison, and local adaptation; its
  conditional workflow lives in `references/code-patterns.md`
- `research:source-synthesis`: compact source normalization before
  `best-of-worlds`
- `SKILL.md` Todo List: method and dependency checklist
- `AGENTS.md`: maintenance rules

## Minimal Example

1. Choose `research:gap`.
2. Capture the local baseline.
3. Inspect grounded comparables.
4. Return current state, production expectation, missing gaps, recommendation,
   and next route.

## How To Test

- Confirm every method has an anchor in `SKILL.md`.
- Confirm the `SKILL.md` Todo List links Tier 1 primitives and method anchors.
- Confirm retired public wrappers, including `external-patterns`, are absent.
- Validate `evals/evals.json` and run the focused research eval comparison.
