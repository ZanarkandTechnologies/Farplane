# Ticket Metadata

## Goal
- Prove active tickets remain machine-readable enough for Pulse, interval
  planning, Goal Advisor, and review lanes.

## Fast Entry
- Route or deep link: n/a.
- Shortcut or debug control: n/a.
- Panel or mode to open directly: terminal at repo root.

## Setup
- Auth / fixture / seed: none.
- Reset path: do not rewrite ticket history; patch only malformed active
  ticket metadata.
- Commands:
  - `python3 bin/validators/check_harness_invariants.py`

## Stable Selectors
- `data-testid`: n/a.
- Roles / labels: n/a.
- Assertion targets: ticket front matter, status, proof block, and archive
  shape accepted by validators.

## agent-browser Path
1. Not applicable unless validating ticket rendering in Farplane UI.

## Playwright Path
1. Not applicable unless validating ticket rendering in Farplane UI.

## Observability
- `tickets/TASK-*/ticket.md`
- `tickets/README.md`
- ticket-scoped `program.md`, `progress.md`, and `artifacts/` when present.

## Known Gaps
- Add a dedicated ticket metadata validator if `check_harness_invariants.py`
  becomes too broad for routine ticket QA.
