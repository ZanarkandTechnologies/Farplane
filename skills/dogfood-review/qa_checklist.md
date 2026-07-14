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
dogfood_check(report, active_packets, recent_archive, prior_report?, history_receipts,
              candidates, admitted_specs, pulse_materialization_receipt)
  -> pass | violation | source_gap
```

## Checklist

- [ ] Portfolio inputs are complete enough to judge: active packets, recent
      archived packets, prior Dogfood report when available, current
      reports/metrics, new completed ticket-completion learning reports, Reward
      rows, programs, progress tails, and cited proof were read before
      candidates were generated; omissions are source gaps.
- [ ] The Core ticket-history CLI was queried globally before progressive
      `self_improvement` filters. Its receipt preserves expected/actual Reward,
      decisions, evidence, origin, and exact-versus-KPI-fallback area derivation.
- [ ] Harness-health evidence includes current metric observations plus
      skill/template rollout, eval/QA coverage, heat or composition importance
      when available, and recurring correction evidence. UI-only scores remain
      diagnostic rather than canonical Reward.
- [ ] The cutoff is applied as a snapshot, not a forced terminal decision. The
      outcome ledger separates settled, pending, monitoring,
      due-check-in-pending, inconclusive, accepted, killed, and iterating state
      without Dogfood deciding or mutating a Reward row.
- [ ] The report carries an active/pending view, due-check-in-pending gaps, transfer
      candidates, rejected patterns, attribution/proof findings, and prior
      report cursor state, while canonical ticket evidence wins on conflict.
- [ ] Allocation evidence proves a target of five new weekly specs. Active WIP
      remains visible and constrains same-surface conflicts, delayed-live load,
      dedupe, and review burden, but does not subtract from unrelated weekly
      slots. Any shortfall names the exact hard guard, conflict, duplicate,
      source gap, delayed cap, or incomplete-spec rejection.
- [ ] The dated report exists before candidate ranking.
      Ranking covers surface attribution, objective impact, proofability,
      compounding value, cost, risk, review load, interference, and rejection.
      Candidate generation covers Reward history, harness health, leverage of
      accepted capabilities, and failure/loss-term harness placement.
- [ ] Admitted specs number `0..5` and use `reserved_area:self_improvement`.
      Every candidate names area, attributable surface, hypothesis, baseline,
      Reward, proof, horizon, cost/risk, budget, stop, and rollout/rollback;
      selected surfaces are independent and unoccupied.
- [ ] Immediate candidates name an immediately available signal. Delayed
      candidates name the future signal and check-in procedure outline needed
      to materialize an executable Goal Packet after planner admission.
      Human-feedback candidates route through `optimize-with-human` and name
      the feedback artifact, wait state, and later decision procedure.
- [ ] Every admitted spec passes the full `plan-next-wave` executable ticket
      contract. The report predates selection, and Pulse alone writes ticket,
      program, progress, and admission receipt files.
- [ ] Any known-fix recovery occupies one of the five slots, is deduped and
      KPI/guard-linked, names a preventive mechanism and next-run proof, and is
      not created as an extra ticket outside the reserved wave.
- [ ] Completion-learning reports include a created/existing/no-ticket receipt;
      their projected direct-fix or prove-or-reject ticket is counted once and
      Dogfood does not recreate it or execute it.
- [ ] The run invoked only Pulse's bounded materialization route after the
      report and planner decision. It did not execute/compile Goals, dispatch
      workers, mature a check-in, decide Reward, promote, roll back, or perform
      external actions.
