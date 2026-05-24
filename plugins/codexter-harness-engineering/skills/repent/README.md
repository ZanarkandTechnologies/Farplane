# Repent Skill

## Purpose

Provide an operator-visible recovery mode for when the assistant likely missed
an obvious requirement and needs to switch into audit-then-fix behavior.

## Entrypoint

- [SKILL.md](/Users/kenjipcx/coding-harness/Codexter/skills/repent/SKILL.md)

## Minimal Example

- User: `repent, you forgot to update the docs`
- Expected behavior: verify the miss, update the docs if the complaint is real,
  and keep the first response action-oriented.

## How To Test

- review the fixtures in [fixtures.md](/Users/kenjipcx/coding-harness/Codexter/skills/repent/references/fixtures.md)
- run the skill validator against `skills/repent/`
