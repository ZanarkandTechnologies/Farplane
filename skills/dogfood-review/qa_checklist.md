---
title: Dogfood Review QA Checklist
owner: dogfood-review
status: active
kind: qa-checklist
updated_at: 2026-07-16
---

# Dogfood Review QA Checklist

```text
dogfood_check(report, cutoff, admission_receipts, live_packets, prior_report?)
  -> pass | revise | fail + evidence
```

- [ ] `complete_cutoff_reconstruction`: `farplane tickets history --area
      self_improvement --all --json` returned `query.limit: all` and
      `receipt.exhausted: true`; cutoff-bounded exact-area receipts and all
      still-live earlier packets were read; ambiguity is a gap.
- [ ] `ticket_truth_preserved`: Reward/check-in/progress/artifact state is cited
      without rescoring, rewriting, or converting missing evidence to zero.
- [ ] `outcome_attribution_honest`: only external ultimate-metric evidence is
      counted as revenue, reach, or subscription movement; enabler/guard results
      stay leading/protective.
- [ ] `state_ownership_lean`: report owns interval joins and stable portfolio
      pattern refs only; target rules remain in reviewed target memory.
- [ ] `planner_boundary`: report exposes bounded `planner_context_ref`; it
      creates no skill calls, allocation, target quota, or planner API.
- [ ] `authority_receipts`: no execution, materialization, dispatch, check-in,
      Reward decision, direct ticket write, promotion, rollback, or mutation.
- [ ] `golden_and_leanness`: result applies golden invariants without copying
      fixture facts and adds no duplicate state/workflow/forecast fields.

Material changes require an independent reviewer to reapply this checklist.
