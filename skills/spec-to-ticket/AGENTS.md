# Spec-to-Ticket Module

## Purpose

Own the planning-only slice-to-ticket conversion contract for Codexter.

## Invariants

- `spec-to-ticket` remains planning-only; it does not implement features.
- Ticket files stay the primary output surface, not `docs/progress.md` or hidden run state.
- Capability-first packaging is the default: start from one self-contained feature-sized ticket and split only on real boundary triggers. See `MEM-0041`.
- UI-bearing tickets must front-load testability and QA shape instead of leaving QA to improvise later.
- When a split is needed, dependency order remains explicit and conservative.
- `todos.md` here is anti-forgetting scaffolding, preferably plain natural-language checklist text with Markdown links, not a second ticket template. See `MEM-0028`.

## Notes

- Keep the top-level skill concise and execution-ready.
- Keep `todos.md` aligned with the live workflow and gotchas in `SKILL.md`.
- If ticket-output shape changes, check the ticket template and related review guidance in the same pass.
