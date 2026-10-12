---
ticket_id: TASK-0003
title: Collect the first revenue
status: todo
priority: high
depends_on: [TASK-0002]
foundation_step: collect_revenue
foundation_sequence: 3
created_at: TODO
updated_at: TODO
---

# TASK-0003: Collect the first revenue

## Summary

Turn the delivered value into the project's first real revenue. Agree on a
clear price and approved payment path, then preserve evidence of the completed
commercial exchange without storing secrets in the ticket.

## Scope

- In: shape the smallest fair offer, prepare the invoice or payment request,
  obtain approval, send it through an authorized channel, and record the result.
- Out: fake receipts, simulated payments, unapproved pricing or outreach,
  storing payment credentials, broad billing infrastructure, or recurring
  commitments not required for the first transaction.

## Done / Proof

```text
done_when:
  - the customer, offer, price, and payment terms are recorded
  - the operator approves the offer and payment request before it is sent
  - non-secret evidence confirms the first revenue was actually received
  - the amount, date, and source reference are recorded without payment secrets
proof:
  - approved offer or invoice reference
  - redacted provider, bank, or ledger evidence of received revenue
  - recorded amount and receipt date
```

## Program

Use the accepted value evidence from `TASK-0002`. Prepare the smallest honest
commercial offer, stop for operator approval before sending it, and close only
after traceable non-secret evidence shows that revenue was received.
