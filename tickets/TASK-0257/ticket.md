---
template_id: ticket-template
template_version: "0.1.5"
feature_refs:
  - FEAT-0007
  - FEAT-0008
ticket_id: TASK-0257
title: Budget runway review loop
phase: complete
status: done
owner: codex
claimed_by: codex-local
priority: high
depends_on:
  - TASK-0253
blocked_by: []
ready: true
approval_required: false
requires_qa: true
requires_demo: false
created_at: 2026-07-01T12:30:00+08:00
updated_at: 2026-07-01T12:48:00+08:00
next_action: complete; inspect the next real weekly interval report for Budget / Runway Review quality
last_verification: 2026-07-01 project validators, ticket metadata, metric tests/snapshot, skill checks, and diff check passed
---

# TASK-0257: Budget Runway Review Loop

## Summary
Add the missing budget/runway constraint to Farplane without creating a new
accounting system. The durable rule belongs in `farplane/harness.md`; weekly
review belongs in `interval-update`; active allocation belongs in
`farplane/ops-memory.md`; tickets continue to use the existing `Reward` block.

This keeps quarterly bets as protected runway while letting weekly intervals
decide whether active projects should continue, narrow, pause, instrument, or
stop.

## Scope
- In:
  - Add a static runway allocation guardrail to `farplane/harness.md`.
  - Add a compact budget-accountability SMART loop to `farplane/goals.md`.
  - Add current runway fields to `farplane/ops-memory.md`.
  - Add Budget / Runway Review guidance to the interval report template and
    interval workflow docs.
  - Update framework docs so ticket `Reward` is the budget justification
    primitive.
- Out:
  - No new cost-accounting database, schema, UI, daemon, or scheduler.
  - No new ticket field duplicating `Reward`.
  - No deterministic parser for ops-memory project sections.
  - No live spend limits, billing integration, or provider-cost ingestion.

## Delta
```text
overall_before:
  - Quarterly SMART goals exist, but runway and spend justification are mostly
    implicit.
  - Tickets already have Reward(moves, win_signal, guard), but interval reports
    do not explicitly summarize those rewards into continue/pause decisions.
overall_after:
  - Harness states that active work must justify burn through contribution.
  - Goals include a lean weekly budget-accountability loop.
  - Ops-memory records contribution modes and weekly runway decisions for
    active projects.
  - Weekly Interval has a Budget / Runway Review section that turns ticket
    rewards and observed evidence into continue/narrow/pause/instrument/stop.
why_now:
  - KPI tracking now exposes actual feedback loops; Farplane needs budget
    pressure before AI-worker speed turns into unconstrained busywork.
first_principles_basis:
  objective: preserve strategic runway while forcing weekly budget-conscious
    learning.
  need: active projects should earn more attention through evidence, not merely
    through being listed in ops-memory.
  assumptions: rough weekly spend/contribution notes are enough for the first
    viable slice; exact accounting can follow only if the review changes
    decisions.
  root_cause: subsidy hides burn, so strategy can drift without an explicit
    contribution constraint.
  constraints: use existing Reward fields; keep project files declarative; avoid
    new accounting machinery.
  first_viable_slice: docs and templates make weekly runway decisions explicit.
  proof_or_falsification: a weekly interval can write a runway decision for each
    active project using ticket rewards, metrics, reports, and source gaps.
  tradeoff: rough budget evidence before precise cost accounting.
  non_goals: real billing ledger, monetization plan, or revenue enforcement.
```

## Reward
```text
moves:
  - Adds budget pressure to the weekly operating loop without bloating tickets.
  - Keeps quarterly strategy useful as protected runway rather than slow feedback.
  - Makes active projects justify continued agent attention through evidence.
win_signal:
  - A future weekly interval can produce a Budget / Runway Review that cites
    ticket Reward blocks and chooses continue, narrow, pause, instrument, stop,
    or escalate_to_revenue for each active project.
guard:
  - Do not create a new ticket schema, deterministic ops-memory parser, spend
    database, or UI surface in this ticket.
```

## Change Plan
### Change 1: Static runway guardrail
```text
fixes:
  - Budget/runway is not named as a static allocation law.
read:
  - farplane/harness.md
write:
  - farplane/harness.md
operation:
  - Add one allocation guardrail and agent-authority note.
qa:
  - Project file validator.
```

### Change 2: Weekly budget loop surfaces
```text
fixes:
  - Weekly Interval has no explicit section for converting ticket rewards into
    active-project runway decisions.
read:
  - skills/interval-update/templates/interval-report.md
  - skills/interval-update/references/interval-update.md
  - docs/farplane-framework/pulse-and-interval-loop.md
write:
  - skills/interval-update/templates/interval-report.md
  - skills/interval-update/references/interval-update.md
  - docs/farplane-framework/pulse-and-interval-loop.md
operation:
  - Add Budget / Runway Review shape and rules.
qa:
  - Skill checks and doc refs.
```

### Change 3: Goals and ops-memory contract
```text
fixes:
  - Active projects have no standard contribution-mode or runway decision
    language.
read:
  - farplane/goals.md
  - farplane/ops-memory.md
write:
  - farplane/goals.md
  - farplane/ops-memory.md
operation:
  - Add one lean SMART goal and active-project runway fields.
qa:
  - Metric snapshot still parses goals.
```

## Done
```text
done_when:
  - Harness has a runway allocation guardrail.
  - Goals include a budget-accountability loop without requiring a new registry.
  - Ops-memory active projects include contribution and runway decision fields.
  - Interval report template includes Budget / Runway Review.
  - Framework docs state that ticket Reward is the spend-justification primitive.
  - Validators and focused tests pass.
```

## QA Strategy
```text
qa_strategy:
  proof_weight: tests
  checks:
    - python3 bin/validators/check_farplane_project_files.py --root .
    - python3 -m unittest bin.tests.test_farplane_metrics
    - python3 bin/farplane.py metrics snapshot --project-root . --date 2026-07-01 --json
    - python3 skills/skill-maintenance/scripts/check_skills.py --write
    - git diff --check
  manual:
    - Inspect that no new ticket field duplicates Reward.
  delegated_lanes:
    - none
  review:
    - rubric: inline
      required_tas: none
  evidence:
    - command output in final/progress
  residual_risk:
    - The first real weekly interval still needs inspection to verify the new
      section changes planning decisions.
```

## Docs Strategy
```text
docs_strategy:
  outcome: update_docs
  doc_targets:
    - docs/farplane-framework/pulse-and-interval-loop.md
    - docs/farplane-framework/project-files.md
  validation:
    - project file validator
    - skill/doc reference checks
```

## Links
- `farplane/harness.md`
- `farplane/goals.md`
- `farplane/ops-memory.md`
- `skills/interval-update/templates/interval-report.md`
- `skills/interval-update/references/interval-update.md`
- `docs/farplane-framework/pulse-and-interval-loop.md`

## State
- 2026-07-01: Implemented lean runway loop across harness, goals, bindings,
  ops-memory, interval report template, interval workflow reference, framework
  docs, and KPI snapshot source reader.
- Verification:
  - `python3 bin/validators/check_farplane_project_files.py --root .`
  - `python3 bin/validators/check_template_version_metadata.py --all`
  - `python3 tickets/scripts/check_ticket_metadata.py`
  - `python3 -m unittest bin.tests.test_farplane_metrics`
  - `python3 bin/farplane.py metrics snapshot --project-root . --date 2026-07-01 --json`
  - `python3 skills/skill-maintenance/scripts/check_skills.py --write`
