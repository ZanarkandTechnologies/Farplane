---
template_id: golden-example
template_version: "0.1.0"
status: active
---

# Call notes to a concise priced proposal

## Input and context

- Request: Turn customer call notes into a short proposal with a recommended price.
- Source context: Three coordinators each spend ten hours per week correcting
  order errors at a loaded cost of $40 per hour. The discussed outcome is an
  order-validation workflow that routes only exceptions to a coordinator.
- Branch: A complete people-and-time value anchor exists.

## Accepted output

# Proposal: Reduce manual order correction

## The problem

Three coordinators currently spend a combined 30 hours each week correcting
orders before scheduling. That delays work and keeps the team focused on
preventable exceptions.

## What it costs today

`3 coordinators × 10 hours × $40 × 52 weeks = $62,400 per year`

## Proposed outcome

The workflow validates each order against the agreed rules and sends only
incomplete or exceptional cases to a coordinator. People keep final control;
routine checking no longer consumes the team's week.

## Recommended engagement

- **Deliverable:** Working order-validation workflow with exception routing.
- **Scope:** Agreed validation rules, exception queue, representative tests,
  operating notes, and handoff.
- **Timeline:** Four weeks.
- **Price:** **$9,500**.
- **Client return:** approximately **6.6×** the investment in the first year.

## Milestones and payment

1. **Signing:** 40% to confirm scope and begin.
2. **Working proof:** 30% when representative orders route correctly.
3. **Handoff:** 30% when the agreed workflow and operating notes are delivered.

## Assumptions and exclusions

- The existing order data is available in the reviewed format.
- New systems or materially different validation rules require a scope change.

## Next step

Approve the engagement and schedule the scope-confirmation session.

## Why it passes QA

- The source numbers produce one visible, correct value calculation.
- The result recommends one engagement and omits pricing theory.
- The proposal remains short while keeping price, milestones, exclusions, and
  the next decision visible.

## Tempting negative

Produce an internal pricing memo, a confidence-adjusted value ledger, three
packages, a maintenance plan, a long discovery appendix, and a proposal.

Why it fails: the customer needs one clear commercial decision, not the
provider's entire pricing workflow.

## Transferable invariants

- Use the customer's language and one conservative value anchor.
- Make the calculation and price obvious without explaining the pricing method.
- Prefer one complete recommendation over decorative choice architecture.

## Non-copyable facts and wording

- The coordinator count, hours, rate, workflow, timeline, price, and prose are
  fixture-specific.
- Generate fresh wording from the current transcript.

## Proof receipt

```yaml
golden_case: proposal-pricing/call-to-proposal
source_refs:
  - operator-approved pricing-method reconstruction
qa_refs:
  - skills/proposal-pricing/qa_checklist.md
accepted_because:
  - correct arithmetic
  - one concise recommendation
  - human-readable commercial decision
heldout_required: true
review_input: candidate + transferable_invariants + qa + heldout_context
review_excludes: planner_scratch_reasoning
```
