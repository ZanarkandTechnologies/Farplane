# Warehouse handover task packet

## Ticket

- ID: `EXAMPLE-001`
- State: `awaiting_review`
- Goal: preserve `acknowledgement_id` when a dispatcher reopens a handover and
  return it in the detail response.
- Out of scope: rewriting historical shifts or changing the dispatcher UI.
- Before: reopen replaced the payload and dropped the acknowledgement ID.
- After: reopen retains the ID and the detail response returns it.
- Example: a Friday-night acknowledgement remains attached after the
  Saturday-morning shift is reopened.
- Done: implementation and targeted unit coverage.
- Missing proof: an operated dispatch-to-handover receipt.

## Progress

- 2026-08-08 09:10 +0800 — Customer asked whether the Monday shift can be told
  that reopened handovers no longer lose acknowledgements.
- 2026-08-08 09:35 +0800 — The data-loss path was reproduced.
- 2026-08-08 10:05 +0800 — A manual-copy runbook reminder was rejected because
  it does not prevent data loss.
- 2026-08-08 11:20 +0800 — The merge and detail response were updated; targeted
  unit coverage passed.
- 2026-08-08 15:40 +0800 — The staffed check stopped before dispatcher reopen.
  No customer-workflow receipt exists.

## Evidence

- Unit merge check: pass.
- Detail-response fixture: pass.
- Staffed dispatch-to-handover: incomplete; no receipt.
- Freshness: captured 2026-08-08. No later runtime or customer confirmation.

## Historical worktree capture

Captured 2026-08-08 15:45 +0800; this is not live state.

- Task-owned: `apps/handover/reopen.ts`, `apps/handover/reopen.test.ts`
- Excluded noise: `docs/brand-voice.md`
