---
ticket_id: TASK-0002
title: Deliver the first value
status: todo
priority: high
depends_on: [TASK-0001]
foundation_step: deliver_value
foundation_sequence: 2
created_at: TODO
updated_at: TODO
---

# TASK-0002: Deliver the first value

## Summary

Deliver one small, concrete outcome for the first customer. The result should
solve part of the evidenced problem well enough for the customer to inspect,
use, or respond to it.

## Scope

- In: agree on a narrow outcome, produce it, verify it against the customer's
  problem, and capture the customer's response.
- Out: speculative platform work, a broad roadmap, unrelated polish, fabricated
  acceptance, deploys, credentials, or commitments outside the approved slice.

## Done / Proof

```text
done_when:
  - one customer-specific outcome is delivered or made ready for approved delivery
  - before/after evidence shows how it addresses the customer's problem
  - the customer response or an explicit operator-reviewed acceptance gap is recorded
  - the operator approves delivery and the proof before the ticket closes
proof:
  - delivered artifact or result reference
  - verification evidence tied to the agreed outcome
  - customer response or documented acceptance gap
```

## Program

Use the customer and problem evidence from `TASK-0001`. Choose the smallest
honest result that can demonstrate value, produce and verify it, then request
approval before any external delivery or commitment.
