---
name: review-model
description: "Review a current business model against ten offer-sequence and monetization criteria, then recommend one evidence-backed next improvement with a Before/After target."
tier: 3
source: local
group: sales
template_uses:
  skill-template: "0.6.2"
allowed-tools: Read, Glob, Grep
---

# Review Model

## Context

Use this skill when deciding how to improve an existing business's offer,
conversion path, cash collection, expansion, downsells, or continuity. It is a
diagnostic rubric, not a mandate to copy Greg Faxon's business or Alex
Hormozi's examples. Preserve the business's actual customer, economics,
capacity, trust constraints, and evidence.

## Skill Signature

```text
review_model(current_model, business_context?, performance_evidence?, objective?)
  -> criterion_review + before_after_map + ranked_bottleneck + next_experiment
reads: supplied or local business evidence, current offer and payment paths, relevant results
does: evaluates ten money-model criteria and selects the smallest decision-changing improvement
writes: review artifact only when requested or when a durable project owner exists
returns: evidence-tagged review, one priority, alternatives, experiment, and source gaps
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] **N1 — Reconstruct the current money path.**
  `business evidence -> customer-to-cash sequence | evidence_gap`

  Rule: Map what customers can actually buy, in what order, at what price and
  payment timing; do not infer an offer ladder from marketing copy alone.

  Assert:
  - The map names attraction, core, expansion, downsell, payment, and continuity states when they exist.
  - Unknown conversion, margin, churn, capacity, or payment facts remain `unknown`, never estimated as fact.

- [ ] **N2 — Gate optimization on viable customer value.**
  `customer-to-cash sequence + outcome evidence -> proceed | offer/product repair | evidence first`

  Rule: If outcomes are materially broken, complaints/refunds show harm, or
  the promise is unsupported, stop commercial sequencing work and name the
  offer/product repair. If viability is unknown, gather evidence before
  optimizing cash extraction.

  Assert:
  - `proceed` requires credible value delivery or a bounded early-stage hypothesis with no contrary harm evidence.
  - A broken core product never routes to more upsells, payment tactics, or continuity.

- [ ] **N3 — Grade all ten criteria from observable evidence.**
  `customer-to-cash sequence + results -> criterion cards`

  Rule: Load [references/rubric.md](references/rubric.md) and grade each
  criterion `0 unknown | 1 absent/fragile | 2 partial | 3 effective`; cite the
  evidence and confidence separately from the grade. Compare the current model
  with the matching Before → Move → After/Result trajectory in that rubric.

  Example: `one $30K annual offer -> first yes is high-risk -> grade 1; a paid diagnostic may be a candidate, not an automatic prescription`.

  Assert:
  - Every criterion has Current/Before, evidence, grade, confidence, and Better/After condition.
  - Every criterion records the closest source trajectory and why it should be adapted, rejected, or investigated.
  - Failed attempts, reported results, and hypotheses in the source remain distinct from universal rules.

- [ ] **N4 — Identify the binding money-model constraint.**
  `criterion cards + objective -> ranked intervention frontier`

  Rule: Do not sum scores into a generic maturity grade. Rank gaps by their
  causal proximity to the objective, evidence strength, expected customer
  value, cash impact, operational cost, and downside.

  Assert:
  - One primary constraint and up to two credible alternatives are named.
  - A low score is not prioritized when another constraint blocks its benefit.

- [ ] **N5 — Design the Before → After change.**
  `primary constraint -> target state + candidate mechanism`

  Rule: Define the customer-visible and business-visible state change before
  choosing tactics; adapt or reject the source example based on fit.

  Assert:
  - Before and After are observable, specific, and preserve customer value.
  - The proposed mechanism names assumptions, risks, and what must remain unchanged.

- [ ] **N6 — Select one bounded next experiment.**
  `target state + evidence gaps -> next experiment | research first | stop`

  Rule: Prefer the smallest test that can change the next decision. Do not
  redesign the entire ladder, change multiple commercial variables at once,
  or claim revenue lift without a baseline.

  Example: `test a paid diagnostic with five qualified prospects; compare acceptance, delivery load, and core-offer progression against the present path`.

  Assert:
  - The experiment names cohort, duration/volume, success signal, guardrail, and positive/negative next branch.
  - Pricing changes, customer contact, spend, or publication remain proposals unless separately authorized.

- [ ] **N7 — Return a decision-ready review.**
  `criterion cards + selected experiment -> Money Model Review`

  Rule: Lead with the recommended next improvement and its reason, then show
  the rubric trace that supports it.

  Assert:
  - The output includes recommendation, Before/After, adapted example, proof plan, alternatives, and evidence gaps.
  - The reader can see why this move comes before the other nine criteria.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Output

Return the shared [business review contract](../../docs/contracts/business-strategy-review.md), specialized as follows:

- **Decision:** proceed with one money-model improvement, repair the core offer/product, or gather viability evidence.
- **Criterion cards:** all ten money-model criteria when the viability gate permits review.
- **Alternatives:** no more than two deferred moves.

## Gotchas

- Do not prescribe a cheaper front-end offer when the real constraint is weak demand, poor outcomes, or delivery capacity.
- Do not label deferred revenue, fee savings, and collected cash as identical forms of revenue.
- Do not turn ten criteria into ten simultaneous projects; the review exists to choose what comes next.
