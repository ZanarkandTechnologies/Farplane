---
ticket_id: TASK-0046
status: active
---

# Worker release claim fixture

## Summary

Verify that awaiting-review tickets release workers.

## Scope

- In: ticket transition and worker lifecycle state.

## Delta

Worker leases should be released after transition to awaiting-review.

## Change Plan

Capture the transition and worker state before and after it.

## Done

- A ticket transition to awaiting-review releases its assigned worker.

## QA Strategy

Require representative lifecycle evidence for the transition and release.

## Docs Strategy

No docs change.

## Links

- `artifacts/markdown-formatting.log`
