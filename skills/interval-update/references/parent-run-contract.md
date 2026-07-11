---
title: "Interval Parent Run Contract"
status: active
owner: interval-update
kind: reference
---

# Interval Parent Run Contract

```text
interval_parent_run(config, context_refs)
  -> evidence_bundle
   -> dated_bau_report
   -> bounded_prior_evidenced_maintenance_deltas
```

Parent responsibilities:

- resolve the bounded Daily or Weekly window and optional completed upstream
  report refs;
- distinguish prior finalized evidence from discoveries first written during
  this run;
- synthesize a compact report and Markdown Problems ledger;
- write and finalize the dated report before any maintenance ticket delta;
- apply only maintenance deltas that pass the admission gates and cap;
- return source gaps and a no-execution receipt.

The parent must not spawn planning, provider, Dogfood, reward-checkin, or
implementation workflows. Read-only evidence-review lanes are optional for a
large Weekly window, but they return findings only; the parent owns the report
and admission decision.
