# Review Module

## Purpose

Own the thin callable review wrapper for Farplane's docs-owned rubric contract.

## Invariants

- Review uses TAS verdicts, not numeric scores: `TAS-A` pass, `TAS-B`
  revise, `TAS-C` block, and `TAS-D` invalid review.
- Review rubric docs use modular binary checklist groups and return one
  TAS verdict per family; do not assign TAS per dimension or average checklist
  results. See `MEM-0131`.
- `evidence-quality` and `integration-readiness` are hard gates: if either
  required family is below `TAS-A`, the overall verdict cannot be `pass`.
- Caller skills or ticket `Proof Contract` own rubric routing.
  `docs/review/rubrics/*` owns TAS meanings, family definitions, hard gates,
  and rubric bodies. This module owns the callable wrapper and output shape.
  See `MEM-0129`.
- For code, cleanup, integration, or evidence-heavy review, the live review surface must use the anti-slop search playbook, return a compact `search_scope`, and express substantive findings with severity/confidence and concrete file refs. See `MEM-0020`.
- Review output must contain concrete findings and next actions, not just questions or vibes.
- The canonical live rubric references are `docs/review/rubrics/*`, not the
  legacy review-skill reference directory or `skills/code-review/`.
- Keep the `SKILL.md` Todo List as plain natural-language todo-list text with Markdown links rather than a custom mini-language. See `MEM-0028` and `MEM-0124`.

## Notes

- Keep the family catalog compact in `docs/review/rubrics/review-rubric-index.md`, but
  keep caller-owned routing and TAS contract explicit.
- Keep the reusable reviewer handoff template in `docs/review/rubrics/reviewer-handoff.md`.
- Keep one reference file per review family in `docs/review/rubrics/`.
- Keep `docs/review/rubrics/desloppify.md` cross-cutting rather than turning it into a second public review skill.
- Each family file should stay skimmable while still including required checks,
  blocker checks, evidence checks, and finding cues.
- If the review contract changes, update `docs/specs/review-gates.md` and the ticket/evidence artifact contract in the same change.
