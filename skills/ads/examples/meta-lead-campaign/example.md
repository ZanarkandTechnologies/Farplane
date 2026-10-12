---
title: Meta lead campaign example
owner: ads
status: active
kind: example
---

# Meta Lead Campaign Example

Calibrates the shape of a `plan` mode result and its issue block. Do not copy
its offer, metric, budget, or approval facts into another campaign.

## Config review

```text
Ad goal: test whether owner-operators book a review call for an onboarding
  workflow diagnostic
Platform / account binding: Meta / farplane/bindings.yaml#ads.meta.primary
  (alias only; blocked until configured)
Offer / landing page: 20-minute review of onboarding handoffs / accepted page
Audience / exclusions: founders and operators of B2B service and software
  companies / existing customers, internal test accounts
Objective / conversion event: leads / booked call (pixel event confirmed in
  report mode before setup)
Primary hypothesis / falsifier: an operational-pain angle books more qualified
  calls than a proof angle / no angle books a qualified call before the cap
Isolated variable: creative angle only; audience, offer, page, budget matched
Creative variants: A operational pain hook; B before/after workflow proof;
  C founder diagnostic offer
Budget cap / schedule: operator-named cap / operator-named 7-day window
Policy risks: say "teams with manual onboarding handoffs", never "your team is
  failing onboarding"
Measurement method / source of truth: A/B split test on the booked-call event;
  platform attribution for daily monitoring only
Success / guard / anti-metric: qualified booked calls / cost per qualified
  call, page conversion rate / cheap unqualified leads
Dry-run or paused setup route: verified write route dry run, then paused
  campaign, ad sets and ads
Launch gate: explicit approval naming account, budget cap, creative bundle,
  landing page, and launch window
Kill / scale rule: stop at the cap with no qualified call, or when the first
  review batch shows wrong-fit leads; a winner earns a new plan, not auto-scale
Learning or stability risk: small budget may not exit the learning phase;
  read after the full window, not daily swings
Next owner: copywriting for the three angles
```

## Issue block (business's private repo)

```md
### Paid Ad Campaign

- Platform / account binding: Meta / private alias resolved
- Objective / conversion event: leads / booked call
- Offer / landing page: onboarding diagnostic / accepted page
- Campaign thesis / hypothesis / falsifier: see config review comment
- Budget cap / schedule: operator-approved cap / 7-day window
- Measurement method / guard metrics: A/B split / cost per qualified call
- Brand Kit decision: accepted
- Reference pack decision: absent

| Order | Owner | Accepted inputs | Primary output | Gate or blocker | Approval gate | Evidence writeback |
| ---: | --- | --- | --- | --- | --- | --- |
| 1 | Operator | issue plan and thesis | plan acceptance | bindings complete | plan acceptance only | approval comment |
| 2 | goal-advisor | accepted plan | loop policy in the issue body | conditional: multi-day run | Goal approval | issue body `## Goal program` |
| 3 | copywriting | thesis, Brand Kit | three angle drafts after final pass | no claim beyond proof | creative-planning approval | linked copy file |
| 4 | ai-image | approved copy | three statics plus one review sheet | no generation before its quote | generation-spend approval | asset folder link |
| 5 | telegram-message | review sheet | one approve / revise / reject photo request | packet phone-readable | review request only | delivery receipt |
| 6 | ads launch | final creative, account, event | redacted dry run, then paused objects | no write route or `ads_management` | paused-setup approval | setup receipt comment |
| 7 | Operator | setup receipt | launch record | needs named launch approval | launch approval | launch comment |
| 8 | ads report | bound account, window | factual read-only report | no `ads_read` blocks the read only | none | dated report comment |
| 9 | ads plan | report | hold, pause, scale, or replan recommendation | no auto-change | new operation-specific approval | decision comment |
```

The three variants come from the copy and image owners, not from the plan. A
performance report is evidence, never authorization to change delivery.
