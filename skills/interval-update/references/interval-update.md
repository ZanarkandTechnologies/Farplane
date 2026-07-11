---
title: "BAU Interval Reporting Contract"
status: active
owner: interval-update
kind: reference
---

# BAU Interval Reporting Contract

Daily and Weekly are profiles over the same report primitive:

```text
report_bau_window(interval_id, review_window, evidence)
  -> dated_report + problems + source_gaps
```

## Daily Profile

Summarize recent BAU execution:

- completed, blocked, abandoned, and review-waiting tickets;
- repeated execution failures, ticket/attention drift, and feedback obligations;
- objective or metric movement backed by current artifacts;
- signals from the latest completed provider report passed as context;
- maintenance/documentation problems observed during BAU work.

Daily does not call the provider whose report it reads and does not turn
provider suggestions into Interval-owned direction.

## Weekly Profile

Compress Daily reports and the wider ticket window into:

- completed and abandoned work;
- repeated or unresolved BAU problems;
- review/intervention load and proof obligations;
- resource consumption and policy-defined budget state;
- maintenance problems worth resurfacing.

Weekly may report planning-frontier suggestions as observations, but it cannot
create new-direction tickets. It does not run the weekly self-improvement job.

## Problems Ledger

Use ordinary Markdown, not a finding schema:

```markdown
## Problems

- [ ] Repeated render failure. Evidence: `reports/...`. Ticket: none
- [x] Stale review request. Evidence: `tickets/TASK-0100/...`. Ticket: `TASK-0110`
```

The current report may update the ledger while it is a draft. After
finalization it is immutable history. A later report carries unresolved rows
forward with the prior report link.

## Maintenance Admission

```text
resurface_problem(problem, prior_finalized_evidence, active_tickets, limit)
  -> 0..limit maintenance_ticket_deltas
```

A candidate passes only when all are true:

1. A finalized artifact from before this report already records the problem.
2. The problem remains unresolved and is material enough to act on.
3. The scope is corrective maintenance, not a new direction or experiment.
4. No active ticket already owns substantially the same problem.
5. The ticket can name executable scope, proof, and a stop condition.
6. Local ticket creation is authorized and the run cap remains available.

Same-run discoveries stay ledger-only even when urgent. The operator may create
an explicit ticket immediately; Interval itself waits for prior evidence.

## Ownership Boundaries

| Decision | Owner |
| --- | --- |
| New BAU direction | `ticket-opportunity-generator.plan_next_wave` |
| Feed/provider discovery and source-backed ticket | provider skill |
| Harness experiment selection | weekly `dogfood-review` automation |
| Ticket execution and matured reward check-in | Work Pulse |
| BAU evidence compression and known maintenance resurfacing | Interval |

Missing sources never cause Interval to invoke another job. Record the gap and
finish the report with the evidence available.
