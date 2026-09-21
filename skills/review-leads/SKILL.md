---
name: review-leads
description: "Review a current lead strategy against five acquisition criteria, then recommend one evidence-backed next improvement with a Before/After target."
tier: 3
source: local
group: marketing
template_uses:
  skill-template: "0.6.2"
allowed-tools: Read, Glob, Grep
---

# Review Leads

## Context

Use this skill when deciding what to improve next in lead generation,
distribution, referrals, or acquisition capability. It evaluates the business
against five lessons without assuming every business needs every channel now.
The present bottleneck, customer economics, available time/money, and evidence
determine the recommendation.

## Skill Signature

```text
review_leads(current_lead_strategy, business_context?, acquisition_evidence?, objective?, constraints?)
  -> criterion_review + before_after_map + ranked_bottleneck + next_experiment
reads: supplied or local audience, channel, funnel, customer, referral, and economics evidence
does: evaluates five lead-engine criteria and selects the smallest decision-changing improvement
writes: review artifact only when requested or when a durable project owner exists
returns: evidence-tagged review, one priority, alternatives, experiment, and source gaps
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] **N1 — Reconstruct the working acquisition system.**
  `business evidence -> audience-to-customer map | evidence_gap`

  Rule: Map actual lead sources, conversion steps, volume, cost, time, quality,
  and referral behavior; distinguish repeated performance from one-off wins.

  Assert:
  - The map separates warm outreach, content, cold outreach, paid acquisition, and referrals when present.
  - Missing rates, attribution, margin, capacity, or churn remain `unknown`.

- [ ] **N2 — Grade the five lessons and Core Four subchannels.**
  `acquisition map + results -> criterion cards`

  Rule: Load [references/rubric.md](references/rubric.md) and grade each lesson
  `0 unknown | 1 absent/fragile | 2 partial | 3 effective`; grade each Core
  Four channel separately only when applicable or materially assessable.
  Otherwise label it `candidate later` or `not currently required` and do not
  grade it. Compare the current strategy with each relevant Before → Move →
  After/Result trajectory in that rubric.

  Example: `consistent warm referrals but no repeatable ask -> referral lesson grade 2; improve the referral moment before opening a new ad channel`.

  Assert:
  - Every lesson has Current/Before, evidence, grade, confidence, and Better/After condition.
  - Each Core Four channel has an applicability label; unused does not automatically mean weak.
  - Every lesson records the closest source trajectory and why it should be adapted, rejected, or investigated.
  - Creator applications, book illustrations, and numeric heuristics remain clearly labeled examples.

- [ ] **N3 — Locate the binding acquisition constraint.**
  `criterion cards + objective + constraints -> ranked intervention frontier`

  Rule: Use the sequence `More → Better → New` inside the currently suitable
  method. Choose a new method only after the current one has adequate volume
  and its main constraint has been improved, or when evidence shows structural
  channel mismatch.

  Assert:
  - One primary constraint and up to two alternatives are named.
  - The review distinguishes insufficient volume, poor conversion, weak economics, capacity limits, and channel mismatch.

- [ ] **N4 — Define the Before → After acquisition change.**
  `primary constraint -> target state + adapted mechanism`

  Rule: Specify the observable audience or funnel behavior that should change
  before choosing a tactic. Match channel choice to relationship, reach,
  economics, operational capacity, and the business's time-versus-money profile.

  Assert:
  - Before and After are measurable without pretending attribution proves causality.
  - The proposed mechanism names assumptions, exclusions, and customer-trust risks.

- [ ] **N5 — Select one bounded lead experiment.**
  `target state + evidence gaps -> next experiment | research first | stop`

  Rule: Change one primary variable, use a representative sample, and declare
  the decision branches before execution. Do not authorize outreach, ads,
  spend, or publishing through this review.

  Example: `ask ten high-outcome customers for an immediate three-way introduction; measure asks, introductions, qualified conversations, and customer discomfort`.

  Assert:
  - The experiment names cohort, volume/timebox, success signal, guardrail, and positive/negative next branch.
  - It does not recommend scale beyond delivery capacity or known unit economics.

- [ ] **N6 — Return a decision-ready review.**
  `criterion cards + selected experiment -> Lead Engine Review`

  Rule: Lead with the recommended next improvement and why it precedes more
  channels, then expose the rubric trace.

  Assert:
  - The output includes recommendation, Before/After, adapted example, proof plan, alternatives, and evidence gaps.
  - The reader can distinguish lead volume, lead quality, conversion, economics, and referral health.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Output

Return the shared [business review contract](../../docs/contracts/business-strategy-review.md), specialized as follows:

- **Decision:** the one next lead-engine improvement and why now.
- **Criterion cards:** all five lessons plus applicable Core Four channel subgrades.
- **Alternatives:** no more than two deferred moves.

## Gotchas

- Do not recommend paid ads merely because other channels are absent; prove economics, message, and capacity first.
- Do not confuse more activity with better acquisition when the funnel constraint is conversion or product value.
- Do not treat follower count, impressions, or raw lead volume as business outcomes without quality and conversion evidence.
