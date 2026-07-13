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

## Evidence Provider Binding

Resolve evidence before reading either board:

```text
resolve_interval_evidence(project_root, farplane/bindings.yaml?)
  -> provider + sanitized_coordinates + filesystem_ticket_policy + source_gaps
```

When bindings exist, `integrations.kanban` is authoritative:

```yaml
integrations:
  kanban:
    provider: filesystem_tickets | notion
    filesystem_ticket_policy: include | exclude
    tickets_dir: tickets                 # filesystem_tickets only
    archive_dir: tickets/archive         # filesystem_tickets only
    task_source_handle: notion.tasks.source  # notion only; named handle, not ID
```

`filesystem_tickets` preserves the existing project-relative ticket read and
dedupe behavior only when its filesystem policy is `include`; `exclude`
produces a source gap without exposing or inspecting ticket paths. `notion`
resolves `task_source_handle` through private Notion
context and queries through the existing `ntn` boundary. Normalize provider
rows before synthesis; tracked artifacts may retain human-readable task labels
and opaque evidence labels but never raw Notion IDs, URLs, tokens, or payloads.

The default `filesystem_ticket_policy` is `include` for `filesystem_tickets`
and `exclude` for `notion`. An explicit `exclude` is a hard gate across work
review, dedupe, and recovery admission. Missing Notion context, handle, CLI,
credential, or query access produces a `source_gap` with no filesystem fallback.
Resolver readiness for Notion means only that the named handle and `ntn` route
can be attempted; access remains unverified until the bounded compact query
succeeds. Query or credential failure becomes the run's source gap.
When the bindings file itself is absent, the pre-bindings filesystem behavior
remains the documented legacy default.

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
resurface_problem(problem, current_or_prior_evidence, active_tickets, limit)
  -> 0..limit maintenance_ticket_deltas
```

A candidate passes only when all are true:

1. Current or prior evidence from the configured provider proves an existing problem.
2. The problem remains unresolved and is material enough to act on.
3. The scope is corrective maintenance, not a new direction or experiment.
4. No active work item from the configured provider already owns substantially
   the same problem; excluded filesystem tickets are not a hidden dedupe source.
5. The ticket can name executable scope, proof, and a stop condition.
6. Local ticket creation is authorized and the run cap remains available.

Same-run findings may create recovery only when the direct correction and all
proof, KPI/guard, authority, dedupe, and stop gates are already settled. An
uncertain diagnosis stays in the report for planner comparison or experiment
design.

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
