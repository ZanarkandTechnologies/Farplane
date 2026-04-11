# Spec-to-Ticket

Turn one bounded spec slice into raw executable tickets.

## Purpose

Help agents convert product/spec intent into dependency-ordered ticket truth while front-loading testability, QA shape, and evidence expectations.

## Public API / Entrypoints

- `SKILL.md`: main planning contract
- `todos.md`: example natural-language todo template for slice decomposition
- `references/spec-template.md`: canonical spec structure
- `references/ticket-template.md`: ticket-writing reference
- `references/review.md`: planning review checklist
- `AGENTS.md`: maintenance rules for this module

## Minimal Example

1. Read the chosen SLC slice.
2. Read `todos.md` if using skill todos.
3. Split the slice into dependency-ordered tickets.
4. Add UI testability and evidence requirements up front when relevant.
5. Write the raw tickets into `tickets/` and stop before implementation.

## How to Test

- Confirm `SKILL.md` still says one slice per planning pass.
- Confirm `todos.md` reinforces planning/testability behaviors as plain natural-language checklist text without becoming a second ticket template.
- Confirm UI-bearing ticket requirements remain explicit.
- Confirm the linked references exist and match the live ticket contract.
