# Review Module

## Purpose

Own the live rubric-driven review contract for Codexter.

## Invariants

- Review scores use a `1.0` to `5.0` anchored scale, not percentages. See `MEM-0006`.
- The live contract defines all five bands explicitly: `1` failing, `2`
  weak/untrusted, `3` acceptable but caveated, `4` strong/pass-worthy, `5`
  exemplary.
- `evidence-quality` and `integration-readiness` are hard gates: if either required family scores below threshold, the overall verdict cannot be `pass`. See `MEM-0006`.
- For code, cleanup, integration, or evidence-heavy review, the live review surface must use the anti-slop search playbook, return a compact `search_scope`, and express substantive findings with severity/confidence and concrete file refs. See `MEM-0020`.
- Review output must contain concrete findings and next actions, not just questions or vibes.
- The canonical live references are this module's `SKILL.md` and `references/*`, not `skills/code-review/`.
- If `todos.md` exists here, keep it as plain natural-language checklist text with Markdown links rather than a custom mini-language. See `MEM-0028`.

## Notes

- Keep the selection map compact in `references/review-rubric-index.md`, but keep the score-band contract explicit.
- Keep one reference file per review family in `references/`.
- Keep `references/desloppify.md` cross-cutting rather than turning it into a second public review skill.
- Each family file should stay skimmable while still including skeptic questions plus evidence/finding cues.
- If the review contract changes, update `docs/specs/review-gates.md` and the ticket `Review Packet` template in the same change.
