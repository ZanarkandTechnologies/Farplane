---
title: Campaign plan and approval inventory
owner: ads
status: active
kind: reference
---

# Campaign Plan and Approval Inventory

Load this in `plan` mode (N2-N4) when the campaign needs the full thesis, test
matrix columns, issue block, or approval inventory. SKILL.md holds the rules;
this file holds the shapes.

## Campaign thesis

Write it before any setting:

- audience pain or demand signal, and the observable business context that
  shows it (never a personal attribute);
- offer promise and the proof that supports it;
- channel reason (why paid, why this platform);
- conversion event and its source of truth; for a book-a-call funnel the
  optimisation event is the post-qualifier event (lead passed the fit
  questions) sent back to Meta, and raw form submits stay a monitoring metric;
- when a lead funnel "doesn't convert", the stage counts (click, page
  conversion, qualified, booked, showed, closed, revenue) and the first stage
  that leaks; the test aims there, and with no show or close counts the plan is
  blocked on measurement. Show-stage fixes (fast confirm call, proof sent
  before the call) go to the operator as non-ad work;
- creative angle families, market awareness and sophistication, category entry
  point, distinctive brand asset;
- one primary hypothesis and what would make the campaign obviously wrong.

## Test matrix columns

One row per variant. Every row in the first test changes the same one variable
(audience, creative, offer, or landing page); everything else is matched.

| Column | Holds |
| --- | --- |
| Variant | A, B, C |
| Isolated variable | audience slice, angle or creative asset, offer promise, or landing page |
| Matched setup | what stays identical across rows |
| Metric / guard metric | primary success metric; the guard that catches a bad win |
| Read window / spend | days or spend before reading; learning-phase or platform-stability risk |
| Kill rule | stop condition, written before launch |
| Scale rule | what result earns more budget, still behind a new approval |
| Next iteration | the one variable the next test changes |

Success, guard, and anti-metrics come from the
[metric card](../../goal-advisor/references/metrics.md).

## Measurement method

| Question | Method |
| --- | --- |
| Is it delivering, what does it cost | platform attribution (monitoring only) |
| Which variant is better | A/B or split test with matched setup |
| Did ads cause the sales | holdout or conversion-lift test |
| No real measurement source | blocked until one exists |

Platform attribution never answers a causal question; say so when the operator
asks one.

## Policy risks

Label every risk before the plan is returned:

- targeting that implies personal hardship, health, finances, or another
  personal attribute; reframe to observable business context;
- special ad categories (employment, housing, credit, social issues) and the
  targeting limits they impose;
- health, finance, or income claims, and before/after claims without proof;
- copy that tells the viewer they personally have a problem ("teams with manual
  handoffs", not "your team is failing").

## Config review block

```text
Ad goal:
Platform / account binding: <alias only>
Offer / landing page:
Audience / exclusions:
Objective / conversion event:
Primary hypothesis / falsifier:
Isolated variable:
Creative variants:
Budget cap / schedule:
Policy risks:
Measurement method / source of truth:
Success / guard / anti-metric:
Dry-run or paused setup route:
Launch gate:
Kill / scale rule:
Learning or stability risk:
Next owner:
```

## Issue block

The plan lives on the business's private-repo GitHub issue: the block below
under the issue body's `## Change Plan`, approvals and receipts as top-level
comments. Never put budgets, prices, client names, or account IDs on a public
repository's issue. With no issue, write the block to
`.farplane/ads/<YYYY-MM-DD>-<slug>/plan.md`.

```md
### Paid Ad Campaign

- Platform / account binding:
- Objective / conversion event:
- Offer / landing page:
- Campaign thesis / hypothesis / falsifier:
- Budget cap / schedule:
- Measurement method / guard metrics:
- Brand Kit decision: absent | accepted | blocked
- Reference pack decision: absent | choose | augment | reject | blocked

| Order | Owner | Accepted inputs | Primary output | Gate or blocker | Approval gate | Evidence writeback |
| ---: | --- | --- | --- | --- | --- | --- |
```

Row rules:

- One owner per row; a child skill's output stays in its own artifact.
- An unknown fact (event, binding, budget, measurement) is a blocked row with
  its next owner, never a guess and never a dropped row.
- Row order: plan acceptance first, then the Goal row (conditional), creative
  rows, review notification, paused setup, launch, read-only report, and the
  next decision.

## Approval inventory

Each of these is its own approval, and none implies another:

1. plan acceptance (accepts the plan and thesis only);
2. creative-generation spend (per `ai-image` or `ai-video` quote);
3. final creative;
4. paused/draft setup;
5. launch, naming account, budget, creative, landing page, launch window;
6. every later pause, budget change, scale, or creative replacement.

Read-only reporting needs no approval. A scheduled check-in may read and
recommend; it never pauses, scales, or changes budget on its own.

## Creative routes

Add a creative row only when its condition holds:

| Condition | Route |
| --- | --- |
| New ad copy, hooks, headlines | [copywriting](../../copywriting/SKILL.md), final pass in [final pass](../../copywriting/references/final-pass.md) |
| Static concepts or a social-native set | [social-content](../../social-content/SKILL.md) |
| New images | [ai-image](../../ai-image/SKILL.md) |
| Video ads or reference-led production | [storyboard](../../storyboard/SKILL.md), then [ai-video](../../ai-video/SKILL.md) |
| Offer or landing page is the blocker | [landing-page](../../landing-page/SKILL.md) |
| Creative already approved | no creative row; reuse it |

An approved Brand Kit is identity and policy truth. A reference pack is
optional inspiration, never a licence to copy its source.

When a reviewable creative or campaign packet exists, an internal
`notify` row can send one phone-readable approve / revise / reject
request with a PNG or JPEG review image. The notification is not approval of
production, setup, launch, or spend.

## Operating loop

A campaign that runs for days gets a conditional
[goal-advisor](../../goal-advisor/SKILL.md) row right after plan acceptance. It
compiles the loop only after its own approval. The loop reads with `report`
mode, appends evidence as issue comments, and selects `report_now`,
`request_feedback`, or `stop`. A proposed delivery change returns to `plan`
mode for a fresh review and then waits for a new explicit approval.
