---
name: review-offer
description: "Review a current offer against ten value, market, pricing, delivery, and risk-reversal criteria, then recommend one evidence-backed improvement with a Before/After target."
tier: 3
source: local
group: sales
template_uses:
  skill-template: "0.6.2"
allowed-tools: Read, Glob, Grep
---

# Review Offer

## Context

Use this skill when deciding how to improve a specific offer: its buyer,
outcome, positioning, price/value, delivery, urgency, components, or guarantee.
This is an evidence-based rubric, not a recipe for copying Greg Faxon's or Alex
Hormozi's examples. Preserve actual buyer needs, delivery economics, ethics,
capacity, and proof.

## Skill Signature

```text
review_offer(current_offer, business_context?, performance_evidence?, objective?)
  -> criterion_review + before_after_map + ranked_bottleneck + next_experiment
reads: current offer, buyer/market evidence, delivery model, economics, and performance results
does: evaluates ten offer criteria and selects the smallest decision-changing improvement
writes: review artifact only when requested or when a durable project owner exists
returns: evidence-tagged review, one priority, alternatives, experiment, and source gaps
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] **N1 — Reconstruct what the buyer is actually being offered.**
  `offer evidence -> buyer-value-delivery map | evidence_gap`

  Rule: Separate promised outcome, ideal buyer, mechanism, deliverables, price,
  terms, proof, capacity, and risk reversal; do not mistake a sales-page claim
  for delivered capability.

  Assert:
  - The map names the offer's buyer, job, outcome, path, friction, economics, and proof where known.
  - Missing market, conversion, outcome, margin, or fulfillment evidence remains `unknown`.

- [ ] **N2 — Grade all ten offer criteria from observable evidence.**
  `buyer-value-delivery map + results -> criterion cards`

  Rule: Load [references/rubric.md](references/rubric.md) and grade each
  criterion `0 unknown | 1 absent/fragile | 2 partial | 3 effective`; keep
  confidence separate from grade. Also load the required
  [application trajectories](references/application-trajectories.md) and compare
  the current offer with the matching Before → Move → After/Result trace.

  Example: `weekly coaching calls described by format -> category-of-one grade 1; an outcome-led package is a candidate, not proof of improvement`.

  Assert:
  - Every criterion has Current/Before, evidence, grade, confidence, and Better/After condition.
  - Every criterion records the closest source trajectory and why it should be adapted, rejected, or investigated.
  - Every creator/book tactic is labeled `example`; creator applications and book illustrations remain distinct.

- [ ] **N3 — Identify the binding offer constraint.**
  `criterion cards + objective -> ranked intervention frontier`

  Rule: Do not add the grades into a pseudo-precise offer score. Rank gaps by
  causal proximity to the objective, evidence strength, buyer value, economic
  effect, feasibility, trust risk, and dependencies.

  Assert:
  - One primary constraint and up to two credible alternatives are named.
  - A copy or bonus problem is not prioritized when market, outcome, proof, or delivery is the blocker.

- [ ] **N4 — Define the Before → After offer change.**
  `primary constraint -> observable target state + adapted mechanism`

  Rule: Define how buyer understanding, behavior, or delivered value should
  change before choosing new copy, price, bonuses, urgency, or guarantees.

  Assert:
  - Before and After are specific, observable, and consistent with delivery reality.
  - The mechanism names assumptions, tradeoffs, and what must remain unchanged.

- [ ] **N5 — Select one bounded offer experiment.**
  `target state + evidence gaps -> next experiment | research first | stop`

  Rule: Test one primary variable on a representative sample and declare the
  decision branches first. Do not publish, contact customers, change live
  prices, promise guarantees, or incur spend through this review.

  Example: `show five qualified prospects the present and revised outcome framing; capture comprehension, fit objections, and next-step intent without changing price`.

  Assert:
  - The test names cohort, volume/timebox, success signal, guardrail, and positive/negative next branch.
  - It measures buyer or delivery behavior, not aesthetic preference alone.

- [ ] **N6 — Return a decision-ready offer review.**
  `criterion cards + selected experiment -> Offer Review`

  Rule: Lead with the one recommended improvement and why it precedes the
  other criteria, then expose the rubric trace.

  Assert:
  - The output includes recommendation, Before/After, adapted example, proof plan, alternatives, and evidence gaps.
  - The reader can distinguish actual value, perceived value, market fit, and conversion tactics.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Output

Return the shared [business review contract](../../docs/contracts/business-strategy-review.md), specialized as follows:

- **Decision:** the one next offer improvement and why now.
- **Criterion cards:** all ten offer criteria.
- **Alternatives:** no more than two deferred moves.

## Gotchas

- Do not polish positioning when the market lacks urgent need or purchasing power.
- Do not create false scarcity, inflated anchors, clutter bonuses, or guarantees the business cannot honor.
- Do not make the offer bigger by default; reduce customer delay and effort with the cheapest reliable delivery shape.
