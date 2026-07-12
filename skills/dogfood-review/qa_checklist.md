---
title: Dogfood Review QA Checklist
owner: dogfood-review
status: active
kind: qa-checklist
applies_to:
  - dogfood-review
  - weekly-self-improvement
  - experiment-candidate-supply
---

# Dogfood Review QA Checklist

Use before evidence collection and again before returning the portfolio report.
Record each violation, its fix, or an explicit source gap.

```text
dogfood_check(report, active_packets, recent_archive, prior_report?, candidates, recovery_tickets)
  -> pass | violation | source_gap
```

## Checklist

- [ ] Portfolio inputs are complete enough to judge: active packets, recent
      archived packets, prior Dogfood report when available, current
      reports/metrics, new completed ticket-completion learning reports, Reward
      rows, programs, progress tails, and cited proof were read before
      candidates were generated; omissions are source gaps.
- [ ] The cutoff is applied as a snapshot, not a forced terminal decision. The
      outcome ledger separates settled, pending, monitoring,
      due-check-in-pending, inconclusive, accepted, killed, and iterating state
      without Dogfood deciding or mutating a Reward row.
- [ ] The report carries an active/pending view, due-check-in-pending gaps, transfer
      candidates, rejected patterns, attribution/proof findings, and prior
      report cursor state, while canonical ticket evidence wins on conflict.
- [ ] Capacity evidence proves
      `available_slots = min(wave_size, max(0, wip_limit - active_wip))`, total
      WIP 3, delayed-live WIP 1, one active experiment per attributable
      surface, dedupe, and review capacity. It also computes remaining delayed
      slots independently; monitoring delayed work does not block unrelated
      immediate proof when total capacity remains.
- [ ] The dated report exists before candidate ranking.
      Ranking covers surface attribution, objective impact, proofability,
      compounding value, cost, risk, review load, interference, and rejection;
      a weak or full-capacity week returns no packet.
- [ ] Candidates number `0..available_slots` and never exceed wave size 2.
      Every candidate names area, attributable surface, hypothesis, baseline,
      Reward, proof, horizon, cost/risk, budget, stop, and rollout/rollback;
      selected surfaces are independent and unoccupied.
- [ ] Immediate candidates name an immediately available signal. Delayed
      candidates name the future signal and check-in procedure outline needed
      to materialize an executable Goal Packet after planner admission.
- [ ] The report links every experiment candidate to evidence and records no
      experiment-ticket creation. The adaptive project planner owns experiment admission.
- [ ] Every created recovery ticket is capped, deduped, KPI/guard-linked, and
      directly justified by a settled attributable failure; it requires no
      uncertain hypothesis or new experiment.
- [ ] Completion-learning reports include a created/existing/no-ticket receipt;
      their projected direct-fix or prove-or-reject ticket is counted once and
      Dogfood does not recreate it or execute it.
- [ ] The run did not invoke implementation, Goal compilation/execution, Pulse,
      workers, a matured check-in, promotion, rollback, or external actions.
