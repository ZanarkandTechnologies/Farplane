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
   -> reporting_phase {dated_report, weekly_draft_delta, ticket_deltas}
   -> Daily {candidate_upserts, zero_promotions, receipt}
    | Weekly {dispositions, promoted_records, receipt, next_draft}
```

Parent responsibilities:

- resolve the bounded Daily or Weekly window and optional completed upstream
  report refs;
- distinguish prior finalized evidence from discoveries first written during
  this run;
- synthesize a compact report and Markdown Problems ledger;
- classify independent candidate lanes and upsert stable fingerprints into the
  current weekly working draft;
- write and finalize the dated report before board or canonical-owner mutation;
- on Daily, apply only explicit mutable task progress and promote no knowledge;
- on Weekly, disposition every candidate, apply independently qualified ticket
  deltas, route authorized promotions through Skill Maintenance, Doc Advisor,
  or Manage Wiki, write the receipt, and open the next draft;
- return source gaps and a no-ticket-execution receipt.

The parent must not spawn planning, provider, Dogfood, reward-checkin, Goal,
Pulse, worker, or ticket-execution workflows. Its three knowledge routes are
Weekly-only promotion owners, not new scheduled jobs or ticket executors.
