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
- `research:code-patterns`: maintained-repo implementation examples
- `research:source-synthesis`: compact source normalization before
  `best-of-worlds`
- `todos.md`: method and dependency checklist
- `AGENTS.md`: maintenance rules

## Minimal Example

1. Choose `research:gap`.
2. Capture the local baseline.
3. Inspect grounded comparables.
4. Return current state, production expectation, missing gaps, recommendation,
   and next route.

## How To Test

- Confirm every method has an anchor in `SKILL.md`.
- Confirm `todos.md` links Tier 1 primitives and method anchors.
- Confirm old live `parity-research` and `gap-analysis` packages are absent.
