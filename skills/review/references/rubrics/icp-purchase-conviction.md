# ICP Purchase Conviction

Use when reviewing whether one explicit ideal customer profile would buy,
approve, or adopt a finished product or credible offer now.

Required TAS: `TAS-A` when purchase conviction is a declared completion gate.

This family is a structured simulated-buyer judgment. It does not prove actual
demand, willingness to pay, product-market fit, or future conversion.

```text
icp_purchase_review(product, icp, offer, alternatives, evidence)
  -> TAS + buyer_verdict + decisive_reason + blocking_objection
```

## Buyer Verdict Contract

- `TAS-A` -> `buy`: I would purchase, approve, or adopt now.
- `TAS-B` -> `trial`: I would enter a trial, pilot, demo, or focused evaluation,
  but one repairable objection prevents commitment now.
- `TAS-C` -> `no-buy`: I would not commit because the product or offer is
  materially misaligned, unconvincing, dominated, or too costly.
- `TAS-D` -> `invalid`: the supplied buyer or decision context is insufficient
  to judge honestly.

Return exactly one TAS for the family. Do not average checks or treat `trial` as
a passing purchase verdict.

## Family TAS Guide

- `TAS-A`: one explicit buyer has an important job now, sees a material and
  credible advantage over the current alternative, can accept the price and
  adoption costs, and has no unresolved deal-breaker.
- `TAS-B`: the buyer sees enough value to evaluate the product, but a specific,
  repairable proof, trust, workflow, approval, or economic objection prevents
  purchase now.
- `TAS-C`: the product does not earn commitment because the problem lacks
  priority, the outcome is weak, the alternative is better, the evidence is
  not credible, or a material buying constraint defeats the offer.
- `TAS-D`: the review lacks one coherent ICP, a credible product or offer,
  current alternative, price or equivalent commitment, or enough evidence to
  inhabit the decision without inventing context.

## Checklist Modules

### Required Checks

- [ ] `single-icp`: The review inhabits one explicit buyer or approver profile,
  not a blend of users, buyers, sponsors, legal reviewers, or market segments.
- [ ] `buyer-job-grounded`: The buyer's important job, pain, desired gain, and
  decision trigger come from supplied evidence rather than invented persona
  detail.
- [ ] `problem-priority-now`: The problem is important and timely enough for
  this buyer to spend money, time, attention, or organizational credibility.
- [ ] `outcome-value-material`: The product creates an outcome the buyer values
  materially, expressed in the buyer's terms rather than as a feature list.
- [ ] `alternative-advantage`: The offer is compared with the buyer's real
  current alternative or status quo and wins on a decision-relevant dimension.
- [ ] `trust-and-proof`: Product evidence is credible enough for the buyer's
  risk level, environment, and claimed outcome.
- [ ] `commitment-fit`: Price or equivalent commitment, switching cost,
  onboarding, approval, security, and workflow disruption do not outweigh the
  expected value.
- [ ] `decisive-buyer-verdict`: The review states `buy`, `trial`, `no-buy`, or
  `invalid`, plus the decisive reason and strongest remaining objection.

### Blocker Checks

- [ ] `invented-buyer-context`: The verdict depends on demographics,
  priorities, authority, budget, workflow, or risk tolerance not present in the
  supplied ICP evidence.
- [ ] `blended-persona-verdict`: Multiple roles or segments with different
  jobs and objections are collapsed into one fictional buyer.
- [ ] `commitment-free-buy`: The review returns `buy` without price or an
  equivalent commitment and adoption-cost context.
- [ ] `demo-equals-demand`: A polished demo, feature list, or reviewer
  enthusiasm is presented as observed demand, willingness to pay, or
  product-market fit.
- [ ] `status-quo-dominates`: The current alternative is cheaper, safer,
  easier, or better on the buyer's decisive criterion and the offer does not
  overcome that disadvantage.
- [ ] `unresolved-deal-breaker`: A material trust, legal, security,
  integration, budget, or workflow objection remains while the review returns
  `buy`.

### Evidence Checks

- [ ] `icp-source-visible`: The buyer profile, job, pains, gains, authority, and
  evidence gaps are traceable to supplied sources.
- [ ] `product-evidence-visible`: The reviewer inspected a finished product,
  representative workflow, credible demo, or equivalent product evidence.
- [ ] `alternative-evidence-visible`: The current alternative or status quo and
  its meaningful strengths are explicit.
- [ ] `offer-economics-visible`: Price or equivalent commitment and the main
  switching or adoption costs are explicit.
- [ ] `claim-boundary-visible`: The result distinguishes reviewer judgment from
  observed customer behavior and names any missing market evidence.

## Multi-Persona Rule

For a buying group, run this family separately for each decision-relevant role.
A buyer, daily user, legal reviewer, and executive sponsor may receive different
TAS verdicts. Caller-owned synthesis may identify the weakest required role,
but this family never manufactures one blended persona.

## Evidence and Finding Cues

- Weak evidence sounds like "the ICP would love this" without a named buyer,
  alternative, commitment, or objection.
- Ordinary evidence supports a demo or trial decision but leaves one material
  proof, trust, workflow, or economic question open.
- Strong evidence makes the buyer's job, advantage, proof, tradeoffs, and
  commitment decision easy to defend.
- Findings should use the buyer's first-person decision logic and name the
  exact objection: "I would trial this, but I would not buy until..."
- A real purchase, signed pilot, paid conversion, or observed rejection can
  strengthen evidence, but this rubric must label that behavior separately
  from its own simulated verdict.

## Example Judgments

- `TAS-A` / `buy`:
  As the named RevOps director, I would approve this now because the inspected
  workflow removes a measured weekly research burden, fits the current stack,
  clears the stated legal requirements, and costs less than the documented
  status quo.
- `TAS-B` / `trial`:
  I would run a focused pilot because the workflow appears valuable, but I
  would not purchase until source traceability and manager review-time
  reduction are proven.
- `TAS-C` / `no-buy`:
  I would keep the current process because this product adds administration,
  costs more, and has not shown a compensating outcome on my decisive metric.
- `TAS-D` / `invalid`:
  The supplied audience blends founders, enterprise operators, users, and
  approvers and provides no price or current alternative, so an honest purchase
  verdict is not possible.

## Review Artifact Attachment

Attach this rubric in the linked review artifact when used:

- `tas`
- `required_tas`
- `pass`
- `buyer_verdict`
- `decisive_reason`
- `blocking_objection`
- `checks`
- `failed_checks`
- `findings`
- `next_action`
