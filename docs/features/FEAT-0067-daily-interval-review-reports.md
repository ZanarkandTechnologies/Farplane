---
title: Daily and weekly BAU problem reports
status: implemented
owner: feature-registry
created_at: 2026-07-07
updated_at: 2026-07-11
tags:
  - farplane
  - feature
  - sys-0003
refs:
  - skills/interval-update/SKILL.md
  - skills/interval-update/references/interval-update.md
  - docs/farplane-framework/pulse-and-interval-loop.md
feature_id: FEAT-0067
system_id: SYS-0003
category: planning
public: true
surfaces:
  - skills/interval-update/SKILL.md
  - skills/interval-update/references/interval-update.md
  - skills/interval-update/templates/interval-report.md
  - farplane/automations.toml
source_refs:
  - docs/features/FEAT-0065-pulse-and-interval-automation.md
  - docs/farplane-framework/pulse-and-interval-loop.md
  - docs/prd.md
external_refs: []
evidence_refs:
  - skills/interval-update/eval_task.json
  - tickets/archive/TASK-0319/ticket.md
  - tickets/archive/TASK-0319/artifacts/qa/integrated-qa.md
known_limits: "Reports may resurface only prior-evidenced BAU maintenance; same-run discoveries remain ledger-only, and the first proof uses representative ticket-local fixtures rather than wall-clock cron runs."
metrics:
  - interval_report_usefulness
  - maintenance_ticket_precision
last_verified: 2026-07-11
experimental: true
superseded_by: false
track: >-
  Review Daily and Weekly BAU reports for the current window. Read the dated
  report, its Problems ledger, source refs, and maintenance tickets it created
  or updated. Judge compression, source-gap honesty, prior-evidence enforcement,
  dedupe, ticket proof/stop quality, and whether the run avoided new strategy,
  Feed Scout execution, Dogfood review, reward check-ins, and ticket execution.
  Return continue, adjust, cap, pause, graduate, or source_gap.
---

# Daily and weekly BAU problem reports

Daily and Weekly Interval compress bounded project evidence into reports and
resurface already-known business-as-usual problems as executable maintenance
tickets. They do not plan new direction or execute ticket work.

```text
interval_update(project_root, interval_id, review_window, context_refs?,
                maintenance_ticket_limit?)
  -> dated_report + problems
   + maintenance_ticket_deltas[0..limit] + source_gaps
```

## At A Glance

- Feature ID: `FEAT-0067`
- System: [Horizon Loop](../systems/horizon-loop.md)
- Status: `implemented`
- Experimental: `true`
- Category: `planning`
- Primary user: operator and Work Pulse planner
- Job: preserve a compact BAU problem history and create only already-justified
  corrective work.

## Problem

The previous Interval matrix mixed reflection, Feed Scout, Dogfood Review,
reward mutation, maintenance, leverage synthesis, and next-window planning.
That made a reporting cadence compete with Pulse and self-improvement for
ticket supply.

## What It Does

- Daily summarizes the last operational window: work outcomes, obligations,
  anomalies, current signals, metrics, and open BAU problems.
- Weekly synthesizes repeated BAU problems, goal/metric drift, review load, and
  unresolved maintenance across Daily reports.
- Each report contains a minimal Markdown `## Problems` checkbox ledger.
- A report may create or update a bounded maintenance ticket only when a prior
  finalized report, ticket, review, or run artifact already proves the problem.
- A problem first discovered in the current run remains ledger-only until a
  later interval or explicit operator action.

## Operating Contract

```text
new BAU direction       -> plan_next_wave
known BAU problem       -> Interval report + optional maintenance ticket
experiment improvement  -> Dogfood self-improvement automation
ticket execution/checkin -> Work Pulse
```

Interval writes its report before any ticket delta. Maintenance tickets must be
actionable, material, deduped against active/recent work, authority-safe, and
able to name proof plus a stop condition. Interval does not run Feed Scout,
Dogfood Review, reward check-ins, priority planning, Goal execution, or workers.

## Feature Flow

```mermaid
flowchart LR
  classDef keep fill:#f3f4f6,stroke:#6b7280,color:#111827
  classDef changed fill:#fef3c7,stroke:#b45309,color:#111827
  classDef added fill:#dcfce7,stroke:#15803d,color:#111827
  classDef retired fill:#fee2e2,stroke:#b91c1c,color:#7f1d1d,stroke-dasharray: 5 3

  evidence["tickets + Pulse outcomes<br/>latest provider reports"]:::keep
  interval["Daily / Weekly Interval<br/>bounded BAU synthesis"]:::changed
  report["dated report<br/>Problems ledger"]:::added
  prior["prior finalized evidence?"]:::keep
  maintenance["0..limit maintenance tickets"]:::added
  pulse["Work Pulse<br/>execution"]:::keep
  planning["priority / Dogfood / check-ins"]:::retired

  evidence --> interval --> report
  report --> prior
  prior -->|"yes + gates pass"| maintenance --> pulse
  prior -->|"no"| report
  planning -. removed .-> interval
```

## Proof And Quality

Required proof:

- current-run discoveries remain ledger-only;
- prior-evidenced problems can create no more than the configured ticket cap;
- duplicates, vague fixes, authority gaps, and new direction are rejected;
- Daily and Weekly reports remain useful without priority planning;
- `python3 docs/features/validate_features.py` and
  `python3 bin/validators/check_doc_refs.py` pass.

## Rollout And Maintenance

- Update path: refine the two report profiles, Problems ledger, and maintenance
  admission checks.
- Rollback path: set maintenance ticket limit to zero while retaining reports.
- Maintenance owner: Horizon Loop.

## Limits And Non-Goals

- Interval does not decide product or harness strategy.
- Interval does not execute tickets or update delayed reward results.
- Interval reports link ticket-owned QA and review evidence instead of copying
  it into a findings registry.
- Feed Scout and Dogfood remain separate scheduled jobs with separate reports.

## Change History

- 2026-07-07: Created as an experimental Daily report feature.
- 2026-07-11: Reframed Daily and Weekly as BAU problem reports with bounded
  prior-evidence maintenance ticket supply.
