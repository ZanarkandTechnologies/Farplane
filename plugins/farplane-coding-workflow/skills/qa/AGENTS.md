# `skills/qa/AGENTS.md`

Rules for the `qa` skill module.

## Purpose

`skills/qa/` owns the QA-phase contract for ticket-scoped evidence gathering.

## Invariants

- In live `$impl` loops, `$qa` is a delegated execution surface. The coordinating lane should route browser/tool-driving work to `qa-tester` instead of using `agent-browser` directly. See `MEM-0069`.
- QA owns artifact capture and ticket reconciliation; `visual-qa` owns the separate UI judgment pass.
- Keep reusable browser-entry guidance in repo-owned `qa/` docs and cookbook pages, not in transient chat or ticket-local prose.

## Notes

- Keep the top-level skill contract focused on proof shape and role boundaries.
- Keep the README short and aligned with the current delegation contract.
