# Spec-to-Ticket Module

## Purpose

Own the planning-only slice-to-ticket conversion contract for Farplane.

## Invariants

- `spec-to-ticket` remains planning-only; it does not implement features.
- Ticket files stay the primary output surface, not `docs/progress.md` or hidden run state.
- Capability-first packaging is the default: start from one self-contained feature-sized ticket and split only on real boundary triggers. See `MEM-0041`.
- Ambition-aware sizing refines that default: keep CRUD and other narrow workflows whole, and for complex systems split by proof/foundation boundaries or real reuse/runtime seams instead of by each internal stage. See `MEM-0044`.
- UI-bearing tickets must front-load testability and QA shape instead of leaving QA to improvise later.
- When an `Agent Testability Brief` exists, preserve it in ticket proof/testability fields instead of re-deriving that doctrine ad hoc. See `MEM-0043`.
- When `docs/bootstrap-brief.md` carries `Agent Experience / Testability`
  defaults, use them as the fallback seed for the first UI-bearing or
  agentically hard ticket instead of making the operator restate the same
  shortcuts, probes, and proof surfaces from memory.
- When a split is needed, dependency order remains explicit and conservative.
- `SKILL.md` Todo List here is anti-forgetting scaffolding, preferably plain natural-language todo-list text with Markdown links, not a second ticket template. See `MEM-0028`.

## Notes

- Keep the top-level skill concise and execution-ready.
- Keep the `SKILL.md` Todo List aligned with the live workflow and gotchas in `SKILL.md`.
- If ticket-output shape changes, check the ticket template and related review guidance in the same pass.
