# Visual QA Module

## Purpose

Own the visual-judgment contract for UI verification and visual debugging.

## Invariants

- `visual-qa` stays ticket-first and judgment-first; it does not become a browser-orchestration prompt.
- The skill must fail underspecified QA instead of improvising a vague happy-path check.
- Every judged screen must carry the required output shape: Expected UI Spec, Observed Snapshot Report, Diff Report + Verdict, and Fix Plan.
- Geometry/layout assertions are required in every serious pass.
- Evidence capture belongs in references and supporting tools, not bloated into the top-level contract.

## Notes

- Keep `SKILL.md` focused on judgment boundaries and report shape.
- Keep the `SKILL.md` Important Checklist as anti-forgetting scaffolding only; prefer plain natural-language checklist text with Markdown links over a custom mini-language or browser runbook. See `MEM-0028`.
- If this module grows more helper surfaces, keep `README.md` current in the same change.
