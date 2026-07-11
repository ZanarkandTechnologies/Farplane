---
title: Dogfood Review QA Checklist
owner: dogfood-review
status: active
kind: qa-checklist
applies_to:
  - dogfood-review
  - weekly-self-improvement
  - experiment-goal-packets
---

# Dogfood Review QA Checklist

Use before evidence collection and again before returning the portfolio report.
Record each violation, its fix, or an explicit source gap.

```text
dogfood_check(report, active_packets, recent_archive, prior_report?, created_packets)
  -> pass | violation | source_gap
```

## Checklist

- [ ] Portfolio inputs are complete enough to judge: active packets, recent
      archived packets, prior Dogfood report when available, current
      reports/metrics, Reward rows, programs, progress tails, and cited proof
      were read before candidates were generated; omissions are source gaps.
- [ ] The cutoff is applied as a snapshot, not a forced terminal decision. The
      outcome ledger separates settled, pending, monitoring,
      due-but-unscored, inconclusive, accepted, killed, and iterating state
      without Dogfood scoring or mutating a Reward row.
- [ ] The report carries an active/pending view, due-but-unscored gaps, transfer
      candidates, rejected patterns, attribution/proof findings, and prior
      report cursor state, while canonical ticket evidence wins on conflict.
- [ ] Capacity evidence proves
      `available_slots = min(wave_size, max(0, wip_limit - active_wip))`, total
      WIP 3, delayed-live WIP 1, one active experiment per attributable
      surface, dedupe, and review capacity. It also computes remaining delayed
      slots independently; monitoring delayed work does not block unrelated
      immediate proof when total capacity remains.
- [ ] The dated report exists before candidate ranking or packet creation.
      Ranking covers surface attribution, objective impact, proofability,
      compounding value, cost, risk, review load, interference, and rejection;
      a weak or full-capacity week returns no packet.
- [ ] Created folders number `0..available_slots` and never exceed wave size 2.
      Every folder contains canonical `ticket.md`, `program.md`, and
      `progress.md` with Reward, proof, budget, stop, and rollout/rollback
      policy; each selected surface is independent and unoccupied.
- [ ] Immediate toy/replay/eval packets use an immediately available signal and
      have no future check-in debt. Every delayed packet sets a Reward
      `check_in_at` or event wake and completely fills the canonical Check-In
      Program `inputs`, ordered `procedure`, matured-row-only `writeback`,
      `decisions`, `idempotency`, and `source_gap`, backed by the packet's
      Metric Provider, Heartbeat Policy, Stop Conditions, and Rollout Policy.
- [ ] Admission defaults to `status: awaiting_review` unless explicit local write policy
      clears all human/external gates. The report links every created packet
      and records initialization only.
- [ ] The run did not invoke implementation, Goal compilation/execution, Pulse,
      workers, a matured check-in, promotion, rollback, or external actions.
