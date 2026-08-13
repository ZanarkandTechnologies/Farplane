---
ticket_id: EXAMPLE-001
title: Preserve critical handover acknowledgements
status: awaiting_review
---

# Preserve critical handover acknowledgements

## Summary

Warehouse shift leads lose the acknowledgement attached to a critical handover
when a dispatcher reopens the shift. The customer needs a reliable history
before the next Monday changeover.

## Scope

- In: preserve acknowledgement identity through a dispatcher reopen and expose
  it in the handover detail response.
- Out: rewriting historical shifts or changing the dispatcher UI.

## Delta

> **Before:** reopening a shift replaced the handover payload and dropped the
> acknowledgement identifier.
>
> **After:** a reopen retains the acknowledgement identifier and returns it in
> the detail response.
>
> **Example:** a Friday-night incident acknowledgement remains attached after a
> dispatcher reopens the Saturday-morning shift.

## Done / Proof

- [x] The acknowledgement identifier is retained through the reopen path.
- [x] Unit coverage passes for a retained identifier.
- [ ] An operated dispatch-to-handover receipt proves the customer workflow.

## State

- Current: implementation and unit coverage are present; customer workflow
  evidence is not yet complete.
- Next: run the staffed dispatch-to-handover receipt and answer the customer
  with its result.
- Blockers: only a staffed dispatcher and shift-lead test window.

## Links

- `progress:` `progress.md`
- `evidence:` `evidence.md`
