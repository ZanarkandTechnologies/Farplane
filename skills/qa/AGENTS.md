# `skills/qa/AGENTS.md`

Rules for the `qa` skill module.

## Purpose

`skills/qa/` owns proof for issue-scoped work: functional evidence capture,
visual judgment, adversarial claim testing, the canonical receipt, and the
post-pass closeout demo.

## Invariants

- Builder ≠ tester ≠ judge. In Goal-backed loops the coordinating lane routes
  browser driving to `qa-tester` instead of self-certifying operated proof
  (`MEM-0069`); visual mode judges captures as a separate pass; the
  adversarial tester lane cannot self-approve.
- Visual mode stays judgment-first and fails underspecified QA instead of
  improvising a happy-path check. Every judged screen carries the four parts
  (Expected UI Spec, Observed Snapshot Report, Diff Report + Verdict, Fix Plan)
  and geometry assertions from DOM facts.
- The closeout demo runs only after a QA pass, cites evidence for every claim,
  and never uses generated visuals as product proof.
- Per-run artifacts live under `.farplane/qa/<issue>/<run>/`; verdicts go on
  the GitHub issue. Reusable browser-entry guidance lives in the project's
  `AGENTS.md` Agent QA section or `docs/qa/<flow>.md`.
- Experiment design and eval rows belong to `skills/eval`; this module only
  links to it.

## Notes

- Keep `SKILL.md` at or under 200 lines; branch detail goes to `references/`.
- Keep the README short and aligned with the modes.
