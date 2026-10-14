---
name: review-business
description: "Use for \"review my offer\", \"review my business model\" or \"review my lead gen\": grades the lens's criteria from evidence and returns one next improvement with a Before/After test."
source: local
department: leadership
template_uses:
  skill-template: "0.6.5"
  skill-eval-task: "0.2.0"
allowed-tools: Read, Glob, Grep
---

# Review Business

## Context

Use this when deciding what to improve next in one part of a running business:
the offer (`lens: offer`), the money model from first sale to continuity
(`lens: model`), or lead generation and referrals (`lens: leads`). Each lens is
an evidence-graded rubric adapted from Greg Faxon's summaries of Alex Hormozi's
books, not a recipe to copy. Preserve the business's real buyer, economics,
capacity, ethics, and proof. It returns advice and one test; it does not
publish, contact customers, change prices, or spend.

## Skill Signature

```text
review_business(current_state, lens: offer | model | leads, context?, evidence?, objective?)
  -> criterion cards + binding constraint + Before/After + next experiment
reads: the offer, payment path or acquisition system, buyer and outcome evidence, results
does: grades every lens criterion and picks the smallest decision-changing improvement
writes: a review artifact only when asked or when a durable project owner exists
returns: the shared business review contract with one priority and evidence gaps
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] **N1 — Pick the lens and reconstruct the real system.**
  `request + evidence -> lens + buyer/cash/acquisition map | evidence_gap`

  Rule: `offer` maps buyer, promised outcome, mechanism, deliverables, price,
  terms, proof, capacity, and risk reversal. `model` maps what customers can
  actually buy, in what order, at what price and payment timing (attraction,
  core, expansion, downsell, continuity). `leads` maps actual lead sources,
  conversion steps, volume, cost, quality, and referrals, separating warm
  outreach, content, cold outreach, paid ads, and referrals. Build the map from
  delivered behaviour, never from sales-page or marketing copy.

  Assert:
  - Missing market, conversion, outcome, margin, churn, capacity, or payment
    facts stay `unknown`, never estimated as fact.
  - Repeated performance is separated from one-off wins.

- [ ] **N2 — Gate on viable customer value before optimizing.**
  `map + outcome evidence -> proceed | offer/product repair | evidence first`

  Rule: When outcomes are materially broken, complaints or refunds show harm,
  or the promise is unsupported, stop and name the offer or product repair. No
  upsells, payment tactics, continuity, scarcity, bonuses, or new channels on
  a broken core. When viability is unknown, gather evidence first.

  Assert:
  - `proceed` needs credible value delivery or a bounded early-stage hypothesis
    with no contrary harm evidence.

- [ ] **N3 — Grade every lens criterion from observable evidence.**
  `map + results -> criterion cards`

  Rule: Load the lens rubric ([offer](references/offer.md),
  [model](references/model.md), or [leads](references/leads.md)) and grade each
  criterion `0 unknown | 1 absent/fragile | 2 partial | 3 effective`, with
  confidence kept separate. Compare against the rubric's matching Before →
  Move → After/Result trajectory and record adapt, reject, or investigate. For
  `leads`, label each Core Four channel `required now | assessable | candidate
  later | not currently required` and grade only applicable ones: an unused
  channel is not a weak one.

  Example: `weekly coaching calls described by format -> offer
  category-of-one grade 1; an outcome-led package is a candidate, not proof`.

  Assert:
  - Every card has Before, evidence, grade, confidence, and After condition.
  - Creator tactics, book illustrations, and numeric heuristics stay labelled
    examples, never pass requirements.

- [ ] **N4 — Choose the one binding constraint.**
  `criterion cards + objective -> primary constraint + up to two alternatives`

  Rule: Never sum grades into a score. Rank gaps by causal proximity to the
  objective, evidence strength, buyer value, cash effect, cost, and downside.
  Never polish copy, positioning, or bonuses when market, outcome, proof, or
  delivery is the blocker. For `leads`, use More → Better → New inside the
  current method: open a new method only after adequate volume and an improved
  constraint, or proven channel mismatch; paid ads only after economics,
  message, and capacity are proven.

  Assert:
  - A low grade is not prioritized when another constraint blocks its benefit.
  - The review separates volume, quality, conversion, economics, and capacity.

- [ ] **N5 — Define the Before → After change and one bounded test.**
  `primary constraint -> target state + next experiment | research first | stop`

  Rule: Define the observable buyer, customer, or funnel change before picking
  a tactic, then test one primary variable on a representative sample with
  decision branches declared first. Claim no lift without a baseline.

  Example: `show five qualified prospects the present and revised outcome
  framing; capture comprehension, fit objections, and next-step intent`.

  Assert:
  - The test names cohort, volume or timebox, success signal, guardrail, and
    positive and negative branches.
  - Price changes, customer contact, spend, and publication stay proposals.

- [ ] **N6 — Return a decision-ready review.**
  `criterion cards + experiment -> Offer | Money Model | Lead Engine Review`

  Rule: Lead with the one recommended improvement and why it comes before the
  other criteria, then show the rubric trace in the shared contract.

  Assert:
  - Output has recommendation, Before/After, adapted example, proof plan,
    alternatives, and evidence gaps.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Gotchas

- Deferred revenue, fee savings, and collected cash are different money; do not
  report them as one revenue figure.
- False scarcity, inflated anchors, clutter bonuses, or guarantees the business
  cannot honour make a weak offer worse, not better.
- A cheaper front-end offer does not fix weak demand, poor outcomes, or
  delivery capacity.
- Follower count, impressions, or raw lead volume are not outcomes without
  quality and conversion evidence.
- Ten criteria are not ten projects; the review exists to pick what is next.

## Reference Map

- [offer](references/offer.md) - ten offer criteria and trajectories.
- [model](references/model.md) - ten money-model criteria and the viability gate.
- [leads](references/leads.md) - five lead lessons and the Core Four subrubric.

## Output

Return the shared
[business review contract](references/business-strategy-review.md):

- **Decision:** the one next improvement for the lens, the core repair, or
  gather viability evidence.
- **Criterion cards:** every lens criterion (ten offer, ten model, five leads
  plus applicable Core Four subgrades) when the viability gate permits review.
- **Alternatives:** no more than two deferred moves.
