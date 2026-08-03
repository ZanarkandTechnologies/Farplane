---
title: Mine-To-Margin Reference Standard
kind: quality-reference
updated_at: 2026-07-13
---

# Mine-To-Margin Reference Standard

Mine-To-Margin is the reference pattern for shaping customer-facing operational
decision systems. Copy its proof architecture, not its mining vocabulary or UI.

## Why It Works

- It resolves many signals into one valuable decision: allocate material lots
  to routes, customers, and time windows under physical and commercial limits.
- It sits beside systems of record instead of pretending to replace ERP, mine
  planning, laboratory, contract, or logistics systems.
- It assigns deterministic economics and feasibility to OR-Tools while the
  agent gathers evidence, invokes tools, and explains verified results.
- It exposes representative inputs, source provenance, solver status, solution
  gap, bottlenecks, downside, baseline comparison, and rebalance triggers.
- It proves responsiveness with an ordinary plan, a resource shortage, a price
  or premium shift, edited inputs, and an infeasible commitment.
- It closes the buyer loop with inspectable output, follow-up challenge,
  rerun/fork behavior, and a concrete shadow-mode production pilot.

## Rubric

Judge a new solution on five equally important questions:

1. Is there one precise and valuable recurring decision?
2. Does a credible domain mechanism produce the important result?
3. Do realistic records and constraints interact strongly enough to change it?
4. Can a skeptical buyer inspect the evidence and challenge the answer?
5. Is the boundary from reference demo to governed production use explicit?

Hard failure: invented tool results, hidden infeasibility, unlabeled provenance,
or a polished interface with no decision-changing mechanism.

## Operational Example

```text
Reported signals: choose 60% versus 65% Fe processing, rank prospectivity, and
judge mineability despite uncertain overburden.
Shared decision: allocate material lots to processing routes, buyers, and time
windows under grade, resource, logistics, price, and mineability constraints.
System boundary: decision layer beside ERP, GIS, mine-planning, laboratory, and
accounting systems.
Mechanism: retrieve source evidence, generate feasible options, run a
constraint optimizer, and return allocations, bottlenecks, downside, and
rebalance triggers.
Proof: ordinary campaign, labor shortage, premium spike, edited input, and
infeasible commitment.
Feedback: reconcile actual grade, yield, duration, cost, and price into the next
planning cycle.
```
