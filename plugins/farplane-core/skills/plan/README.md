# Plan

## Purpose

Define the Tier 2 planning interface that domain-specific skills implement.

## Public API / Entrypoints

- `SKILL.md`: generic planning interface
- `SKILL.md` Important Checklist: planning checklist
- `AGENTS.md`: maintenance rules

## Minimal Example

1. Clarify intent and artifact.
2. Ground expectations.
3. Choose one path.
4. Write executable steps and proof.
5. Hand off to the domain execution skill.

## How To Test

- Confirm the skill stays domain-neutral.
- Confirm coding-specific planning still belongs to `spec-to-ticket` or
  `impl-plan`.
- Confirm the plan defines proof before execution starts.
