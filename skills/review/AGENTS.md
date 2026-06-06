# Review Module

## Purpose

Own the live rubric-driven review contract for Farplane.

## Invariants

- Review uses TAS verdicts, not numeric scores: `TAS-A` pass, `TAS-B`
  revise, `TAS-C` block, and `TAS-D` invalid review.
- Review family references use modular binary checklist groups and return one
  TAS verdict per family; do not assign TAS per dimension or average checklist
  results. See `MEM-0131`.
- `evidence-quality` and `integration-readiness` are hard gates: if either
  required family is below `TAS-A`, the overall verdict cannot be `pass`.
- Caller skills or ticket `Proof Contract` own rubric routing. The review
  module owns TAS meanings, family definitions, hard gates, and output shape.
  See `MEM-0129`.
- For code, cleanup, integration, or evidence-heavy review, the live review surface must use the anti-slop search playbook, return a compact `search_scope`, and express substantive findings with severity/confidence and concrete file refs. See `MEM-0020`.
- Review output must contain concrete findings and next actions, not just questions or vibes.
- The canonical live references are this module's `SKILL.md` and `references/*`, not `skills/code-review/`.
- Keep the `SKILL.md` Todo List as plain natural-language todo-list text with Markdown links rather than a custom mini-language. See `MEM-0028` and `MEM-0124`.

## Notes

- Keep the family catalog compact in `references/review-rubric-index.md`, but
  keep caller-owned routing and TAS contract explicit.
- Keep the reusable reviewer handoff template in `references/reviewer-handoff.md`.
- Keep one reference file per review family in `references/`.
- Keep `references/desloppify.md` cross-cutting rather than turning it into a second public review skill.
- Each family file should stay skimmable while still including required checks,
  blocker checks, evidence checks, and finding cues.
- If the review contract changes, update `docs/specs/review-gates.md` and the ticket/evidence artifact contract in the same change.
