# Deep System Design

## Purpose

`deep-system-design` turns a vague architecture ask into a reusable `System
Design Brief` before `impl-plan`, `spec-to-ticket`, or implementation.

## Public Entrypoints

- `SKILL.md` - live interview contract and handoff rules
- `AGENTS.md` - maintenance rules and boundaries

## Minimal Example

```text
$deep-system-design --data-first "design the ingestion and indexing system for the new search feature"
```

## How To Test

- Re-read `skills/deep-system-design/SKILL.md` once and confirm the boundary
  with `deep-interview`, `functional-ui`, and `deep-ui-design` is obvious.
- Confirm the skill requires explicit entities, signatures, storage ownership,
  and execution boundaries before handoff.
- Confirm the output contract produces a reusable `System Design Brief` instead
  of implementation steps.
