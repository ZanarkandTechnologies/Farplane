---
template_id: ticket-template
template_version: "0.1.4"
feature_refs:
  - FEAT-0007
  - FEAT-0008
  - FEAT-0029
ticket_id: TASK-0249
title: Farplane KPI snapshot pipeline
phase: building
status: review
owner: codex
claimed_by:
priority: high
depends_on:
  - TASK-0248
blocked_by: []
ready: true
approval_required: false
requires_qa: true
requires_demo: false
created_at: 2026-06-30T05:22:00Z
updated_at: 2026-06-30T05:39:00Z
next_action: Kenji Review should inspect the generated KPI snapshot, tracked KPI metadata, bindings, and focused test proof
last_verification: focused metric tests, real snapshot generation, ticket metadata validation, CLI help, and diff whitespace check passed on 2026-06-30
---

# TASK-0249: Farplane KPI snapshot pipeline

## Summary
Implement the minimal KPI pipeline selected by `TASK-0248`: keep KPI
definitions in `goals.md`, source bindings in `bindings.md`, write source
snapshots under `.farplane/metrics/source-snapshots/`, and generate
`.farplane/metrics/ui/latest.json` for the KPI cockpit. The first slice is
local-only and deterministic; social metrics remain manual/source-gap until X
and Instagram bindings exist.

## Scope
- In:
  - Extend `farplane/goals.md` with tracked KPI metadata.
  - Extend `farplane/bindings.md` with metric source bindings.
  - Add a small local generator for source snapshots and UI chart snapshots.
  - Add focused tests for point, daily, cumulative, source-gap, and target-hit
    behavior.
  - Generate one current `.farplane/metrics/ui/latest.json`.
- Out:
  - No external API calls, secrets, social account mutations, posting,
    publishing, deploys, or dashboards.
  - No new KPI DSL beyond `aggregation: point | daily` and
    `cumulative: true | false`.
  - No fake values for X, Instagram, agent-hours, intervention minutes,
    incidents, or market attention.

## Delta
```text
overall_before:
  - Goals name KPI axes, but the UI has no stable project-local KPI read model.
  - Intervals can discuss metric source gaps, but chart data is not generated.
overall_after:
  - Tracked KPI metadata lives in goals.md.
  - Metric source bindings live in bindings.md.
  - A deterministic local command writes source snapshots and ui/latest.json.
why_now:
  - TASK-0248 selected the minimal point/daily observation contract and the KPI
    cockpit needs daily bars, point lines, cumulative lines, and target markers.
first_principles_basis:
  objective: make real Farplane products chartable without fake metrics.
  need: one generated UI read model shared by interval reports and the cockpit.
  constraints: local-only, no external API calls, no custom KPI DSL.
  first_viable_slice: local ledgers and ticket/eval files plus source gaps for
    unbound social and effort metrics.
```

## Reward
```text
moves: validated_self_improvement, quality_and_proof, project_control, distribution_from_evidence
win_signal: `.farplane/metrics/ui/latest.json` exists, contains point and daily KPI series with target-hit/source-gap metadata, and focused tests pass
guard: no fake social/effort/incident values, no external account calls, no UI scraping of interval prose
```

## Change Plan
```text
architecture_signatures:
  module_level:
    - bin/core/farplane_metrics.py / generate_metric_snapshots(project_root, date): SnapshotResult
  data_flow:
    - goals.md tracked KPI table + bindings.md source bindings -> source snapshots -> ui/latest.json

change_1:
  read:
    - farplane/goals.md
    - farplane/bindings.md
    - tickets/TASK-0248/artifacts/kpi-snapshot-decision.md
  write:
    - farplane/goals.md
    - farplane/bindings.md
  operation:
    - add a compact tracked KPI table and metric source binding block
  routes:
    docs: inline_project_config
    qa: tests
    review: inline

change_2:
  read:
    - .farplane/automation/rewards.jsonl
    - .farplane/automation/decisions.jsonl
    - tickets/TASK-*/ticket.md
    - .farplane/evals/runs/**/summary.json
  write:
    - bin/core/farplane_metrics.py
    - bin/farplane.py
    - bin/tests/test_farplane_metrics.py
    - .farplane/metrics/source-snapshots/
    - .farplane/metrics/ui/latest.json
  operation:
    - generate local source snapshots and UI-ready chart series
  routes:
    docs: no_docs
    qa: tests
    review: inline
```

## Done
```text
done_when:
  - [done] `farplane/goals.md` lists tracked KPI metadata
  - [done] `farplane/bindings.md` lists metric source bindings
  - [done] `python3 bin/farplane.py metrics snapshot --project-root . --date 2026-06-30 --json` writes source snapshots and UI latest JSON
  - [done] focused tests pass
  - [done] ticket metadata validates
```

## QA Strategy
```text
qa_strategy:
  proof_weight: tests
  checks:
    - python3 -m unittest bin.tests.test_farplane_metrics
    - python3 bin/farplane.py metrics snapshot --project-root . --date 2026-06-30 --json
    - python3 tickets/scripts/check_ticket_metadata.py
  manual:
    - inspect `.farplane/metrics/ui/latest.json` for point/daily/cumulative/source_gap fields
  delegated_lanes:
    - none
  review:
    - rubric: inline
      required_tas: none
  evidence:
    - .farplane/metrics/ui/latest.json
    - tickets/TASK-0249/progress.md
  goal_advisor_inputs:
    proof_route: focused local tests and generated snapshot inspection
    final_evidence: command outputs and latest JSON path
    final_checkpoint: update ticket/progress with validation evidence before completion
  residual_risk:
    - social metrics require manual or API bindings in a follow-up before real X/Instagram charts show values
```

## Docs Strategy
```text
docs_strategy:
  outcome: update_docs
  doc_targets:
    - farplane/goals.md
    - farplane/bindings.md
  no_docs_reason:
  validation:
    - focused tests and ticket metadata validation
```

## State
```text
state: review
completed_at: 2026-06-30T05:39:00Z
outputs:
  - farplane/goals.md Tracked KPIs table
  - farplane/bindings.md Metric Source Bindings table
  - bin/core/farplane_metrics.py
  - bin/tests/test_farplane_metrics.py
  - bin/farplane.py metrics snapshot command
  - .farplane/metrics/ui/latest.json
proof_summary:
  - `python3 -m unittest bin.tests.test_farplane_metrics` passed
  - `python3 bin/farplane.py metrics snapshot --project-root . --date 2026-06-30 --json` wrote 15 metrics with 7 explicit source gaps
  - `python3 tickets/scripts/check_ticket_metadata.py` passed for 43 ticket files
  - `python3 bin/farplane.py metrics --help` and `python3 bin/farplane.py metrics snapshot --help` passed
  - `git diff --check` passed for touched KPI pipeline files
residual_risk:
  - X/Instagram and effort/incident metrics are still source gaps until manual exports or API bindings are configured.
  - Lower-is-better target semantics are deferred; this slice leaves those targets blank instead of adding a direction field.
```
