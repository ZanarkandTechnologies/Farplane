# Commit Message

## Purpose

Guide agents to write compact high-signal commit subjects in the repo's preferred style.

## Public API / Entrypoints

- `SKILL.md`: main contract
- `references/style.md`: type/scope/style hints
- `AGENTS.md`: maintenance rules

## Minimal Example

1. Read staged diff or recent changes.
2. Choose the main delta.
3. Output `type(scope): summary`.

## How to Test

- Confirm output defaults to one best subject.
- Confirm subject is lowercase and imperative.
- Confirm scope is used when obvious.
