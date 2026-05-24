# Close Ticket

## Purpose

Provide the operator-facing contract for the canonical closeout control surface:
`$close-ticket`. This is a Tier 3 Codexter coding-pipeline closeout skill that
uses the generic
[`execute`](/Users/kenjipcx/coding-harness/Codexter/skills/execute/SKILL.md)
interface's proof and writeback shape.

## Public API / Entrypoints

- `SKILL.md`: main close-ticket workflow and guardrails
- `todos.md`: ordered parent-skill checklist
- `README.md`: module summary and test checklist
- `AGENTS.md`: maintenance notes

## Minimal Example

1. Start the prompt with `$close-ticket TASK-00XX`.
2. Update the ticket writeback and durable docs for the final state.
3. Run the repo-local closeout checks for the touched surfaces.
4. Use `commit-message` to write the commit subject.
5. Commit the closeout slice.
6. Push only if the user or workflow explicitly calls for publishing.

## How to Test

- Confirm `SKILL.md` positions `close-ticket` as the canonical name and
  `docs-closeout` as alias-only.
- Confirm `todos.md` stays a plain ordered checklist with Markdown links to
  related skills.
- Confirm the workflow covers docs writeback, checks, commit prep, and optional
  push in that order.
