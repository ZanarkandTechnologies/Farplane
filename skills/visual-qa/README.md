# Visual QA

Ticket-first visual verification and visual debugging for UI work.

## Purpose

Help agents judge captured UI evidence against ticket intent and `docs/TASTE.md` without collapsing into vague "looks fine" QA.

## Public API / Entrypoints

- `SKILL.md`: main visual judgment contract
- `SKILL.md` Todo List: example natural-language todo template for visual QA
- `references/workflows.md`: extended evidence-capture and workflow variants
- `references/review.md`: final review questions before handoff
- `AGENTS.md`: maintenance rules for this module

## Minimal Example

1. Read the active ticket and its declared screens/states.
2. Read `docs/TASTE.md` when taste or layout quality is in scope.
3. Use the `SKILL.md` Todo List when invoking the skill.
4. Judge one declared screen at a time and produce the required four-section diff report.
5. Return `FAIL` when the ticket is too underspecified to judge honestly.

## How to Test

- Confirm `SKILL.md` still requires ticket-first context and all four report sections.
- Confirm the `SKILL.md` Todo List reinforces judgment behaviors as plain natural-language todo-list text without becoming a browser-automation script.
- Confirm geometry/layout assertions remain explicit in `SKILL.md`.
- Confirm the references linked from `SKILL.md` exist.
