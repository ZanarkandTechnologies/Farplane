Ticket / Proof Policy: `tickets/TASK-0323/ticket.md` / `tests + CLI integration + reviewer`
Verdict: pass

# TASK-0323 authoritative-evidence QA

## Scope

Re-tested completion evidence authority after hardening result selection and
reviewer frontmatter parsing. Prior boundary, diagrams, deterministic receipt,
and allowlist checks remain covered by the focused suites.

## Evidence

- `python3 -m unittest bin.tests.test_ticket_validation bin.validators.test_farplane_checks`
  passed all 13 tests.
- QA/demo evidence now uses the lexically latest `result.json` beneath the
  owning artifact directory as the sole authoritative result.
- An older passing QA result followed by a newer failing result fails
  completion evidence validation.
- A malformed latest result fails closed even when an older passing result
  exists.
- Reviewer completion parsing reads YAML-style frontmatter fields rather than
  searching free-form prose.
- `verdict: pass` with `overall_tas: TAS-B` fails.
- `verdict: revise` with `overall_tas: TAS-A` fails.
- Only the correlated pair `verdict: pass` and `overall_tas: TAS-A` passes.
- A real bounded TASK-0323 completion still exits 1 because its current
  authoritative `completion-review.md` is `revise / TAS-B`. Metadata and visual
  companion pass; `ticket.completion-evidence` correctly blocks.
- Absolute, parent-traversal, nested-traversal, and empty explicit paths all
  continue to exit 1.
- `python3 bin/validators/check_doc_refs.py` passed: 1,893 references checked.
- Registry resolution remains allowlist-only and canonical receipts remain
  duration-free.

## Critical-path reconciliation

- Planning: mandatory separate diagram validation remains enforced.
- Completion provenance: explicit paths fail closed on escape/empty input.
- Completion evidence: latest evidence is authoritative; malformed or failing
  latest results cannot be bypassed by older passes.
- Reviewer gate: both pass verdict and TAS-A are required from frontmatter.
- Current ticket completion: correctly remains blocked until an independent
  reviewer replaces the existing revise/TAS-B receipt with pass/TAS-A.

## Residual risk

Lexical directory naming is now part of the artifact-authority contract; QA and
demo run directories must continue using sortable names. This lane validates
the implementation but does not replace the required independent reviewer
rerun.

## Best evidence

`tickets/TASK-0323/artifacts/qa/20260711T132041Z-ticket-validation-authority-final/report.md`
