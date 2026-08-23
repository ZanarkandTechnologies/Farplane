---
title: Invoice Chaser campaign planner example
owner: ad-impl-plan
status: active
kind: example
---

# Invoice Chaser Campaign Planner Example

Use this only to calibrate the shape of a campaign ticket. Do not copy its
offer, metric, budget, or approval facts into another campaign.

```md
## Summary

Test the offer “Get your money faster by chasing your invoices” with a small
three-variation static Meta lead campaign. No creative generation, Meta setup,
launch, spend, or message is authorized by this draft.

## Scope

In: campaign lock, three controlled copy/creative variations, visual review,
and a later read-only learning loop. Out: automatic delivery optimization.

## Delta

<!-- Campaign ticket only. -->

## Change Plan

### Paid Ad Campaign

- Platform / account binding: Meta / private alias resolved
- Objective / conversion event: qualified inbound lead / accepted lead event
- Offer / landing page: Invoice Chaser / accepted landing-page review
- Ad Advisor receipt / campaign thesis reference: accepted campaign lock;
  it owns the hypothesis, falsifier, test matrix, guard metrics, and policy review
- Budget cap / schedule: operator-approved cap / operator-approved test window
- Measurement / guard metrics: qualified-lead cost; form completion and
  disqualification rate
- Brand Kit decision: accepted
- Tasty Pack decision: absent

| Order | Owner | Accepted inputs | Primary output | Gate or blocker | Approval gate | Evidence writeback |
| ---: | --- | --- | --- | --- | --- | --- |
| 1 | Ad Advisor | offer, audience, event, cap | accepted campaign lock and small controlled test matrix | block on policy or measurement review | campaign-lock acceptance | ticket campaign-lock reference |
| 2 | Operator | ticket and campaign-lock reference | plan acceptance | rows 1 and bindings complete | plan acceptance only | approval record |
| 3 | Social Content | accepted lock and Brand Kit | three copy/creative variation briefs | do not make claims beyond proof | creative-planning approval | creative packet brief |
| 4 | Creative production owner | approved briefs | three visual variants plus one approval sheet image | no generation without its own cost approval | creative-generation approval | `artifacts/creative-review/approval-sheet.png` |
| 5 | Worker Artifact Review Request | approval sheet and compact three-variation summary | one Telegram photo request: `approve`, `revise`, or `reject` | visual packet must be phone-reviewable | review request only | Telegram delivery receipt |
| 6 | Goal Advisor | accepted ticket only | `program.md` and `progress.md` | block until explicit Goal approval | Goal Packet approval | linked packet files |
| 7 | Meta setup operator | approved final creative, account, and event | draft/paused setup receipt | no setup authority or payment permission | draft/paused-setup approval | setup evidence |
| 8 | Operator | setup receipt and launch checklist | launch record | requires explicit launch authority | launch approval | launch audit |
| 9 | Meta Ads | bound account and reporting window | factual read-only performance report | no read access blocks observation only | none | dated report artifact |
| 10 | Ad Advisor | report and observed entities | hold, pause, scale, or replan recommendation | no write-capable route | new operation-specific approval | decision receipt |

## Done

- The campaign lock and plan acceptance are recorded.
- The three creative variants have a phone-reviewable image packet and one
  Telegram review receipt; that receipt is not final-creative or launch approval.
- The first live-spend review, read-only reporting window, factual no-op rule,
  and new-operation approval policy are visible.

## QA Strategy

Check Brand Kit/policy adherence, claim support, creative-review image and
Telegram photo delivery, account/event bindings, budget cap, and every approval
record. If an observation is missing or a recommendation is unapproved, write
the report/request only; do not change delivery.

## State

`draft | awaiting campaign lock and bindings`

## Links

- `creative review:` `artifacts/creative-review/approval-sheet.png`
- `telegram receipt:` `artifacts/creative-review/telegram-receipt.json`
- `program:` `none — Goal Advisor creates after explicit approval`
```

The three variants are intentionally produced by the copy and creative owners,
not invented by the parent ticket. A performance report is evidence, never
authorization to change delivery.
