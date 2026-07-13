---
ticket_id: TASK-0045
status: active
---

# Planned web QA fixture

## Summary

Plan proof for the web-app QA route without inventing completed capture.

## Scope

- In: bound `/qa` route, browser capture, receipt, and reusable learning.

## Delta

The web app exposes a candidate deterministic QA route.

## Change Plan

Use the candidate cookbook entry, delegate capture, then reconcile evidence.

## Done

- The `/qa` route is exercised at the bound runtime.
- UI evidence and a canonical receipt are captured.
- The rendered ready state receives an independent visual judgment.

## QA Strategy

Runtime: `http://127.0.0.1:4173/qa`. Delegate browser operation to
`qa-tester`; the rendered-state obligation requires a separate `visual-qa`
judgment after capture.

## Agent Contract

The `/qa` route is a candidate reusable fast entry, not pre-existing proof.

## Docs Strategy

Update the cookbook only after the run verifies the route is reusable.

## Links

- `../qa/cookbook/web-app-qa-route.md`
