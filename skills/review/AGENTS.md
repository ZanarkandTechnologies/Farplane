# Review Module

## Purpose

Own the live rubric-driven review contract for Codexter.

## Invariants

- Review scores use a `1.0` to `5.0` anchored scale, not percentages. See `MEM-0006`.
- `1` means clearly failing or unproven, `3` means acceptable but ordinary or caveated, and `5` means exemplary and hard to improve materially without changing scope.
- `evidence-quality` and `integration-readiness` are hard gates: if either required family scores below threshold, the overall verdict cannot be `pass`.
- Review output must contain concrete findings and next actions, not just questions or vibes.
- The canonical live references are this module's `SKILL.md` and `references/*`, not `skills/code-review/`.

## Notes

- Keep the selection map compact in `references/review-rubric-index.md`.
- Keep one reference file per review family in `references/`.
- If the review contract changes, update `docs/specs/review-gates.md` and the ticket `Review Packet` template in the same change.
