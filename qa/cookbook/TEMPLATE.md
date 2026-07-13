---
title: <workflow name>
status: planned | verified | retired
owner: <module or team>
source_ticket: TASK-XXXX
updated_at: YYYY-MM-DD
last_verified_at:
last_verified_receipt:
environment: local | test | staging | production-safe
---

# <workflow name>

## Goal

- What behavior this workflow proves.

## Fast Entry

- Route or deep link:
- Panel or mode:
- Runtime handoff:

## Shortcut Contract

```yaml
shortcut:
  trigger:
  environment_guard:
  prerequisites: []
  expected_visible_state:
  expected_internal_state:
  reset_or_cleanup:
  verification:
  evidence_to_capture: []
  source_ticket: TASK-XXXX
  last_verified_receipt:
```

Use `none` with a reason when no shortcut is needed. Never document a
development/test bypass as production-safe without evidence.

## Setup

- Auth / fixture / seed:
- Reset path:
- Commands:

## Stable Selectors and Assertions

- `data-testid`:
- Roles / labels:
- Output or state probes:
- Expected observations:

## Capture Path

1. Bind the documented runtime or command target.
2. Use the fast entry and shortcut when applicable.
3. Exercise the declared workflow.
4. Capture proof appropriate to the proof type.
5. Record failures and unresolved instrumentation gaps.

For browser/UI runs, capture snapshot, screenshots, console, and page errors.
For CLI/API/artifact runs, capture commands, outputs, responses, logs, or files.

## Playwright Path

- Status: not graduated | graduated
- Regression reason:
- Stable selectors and assertions:

## Observability

- Debug HUD or panel:
- DOM/state mirrors:
- Event logs or traces:
- Pause / step / inspect helpers:

## Known Gaps

- Missing shortcut:
- Missing deterministic helper:
- Missing selector, state probe, or assertion surface:

## Learning History

- YYYY-MM-DD — `ticket_only | cookbook_update | instrumentation_ticket` — receipt or follow-up ref
