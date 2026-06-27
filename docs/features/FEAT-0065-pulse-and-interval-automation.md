---
title: Pulse and interval automation
status: implemented
owner: feature-registry
created_at: 2026-06-27
updated_at: 2026-06-27
tags:
  - farplane
  - feature
  - sys-0003
refs:
  - farplane/automations.md
  - skills/pulse-update/SKILL.md
  - skills/interval-update/SKILL.md
  - skills/automation-advisor/SKILL.md
feature_id: FEAT-0065
system_id: SYS-0003
category: planning
public: true
surfaces:
  - farplane/automations.md
  - skills/pulse-update/SKILL.md
  - skills/interval-update/SKILL.md
  - skills/automation-advisor/SKILL.md
source_refs:
  - docs/features/FEAT-0029-goal-packet-architecture-for-native-codex-goals.md
external_refs: []
evidence_refs:
  - skills/pulse-update/eval_task.json
  - skills/interval-update/eval_task.json
  - skills/automation-advisor/audits/2026-06-24-automation-prompt-qa.md
known_limits: Automation prompts and previewable loops exist, but Farplane still avoids hidden daemons and requires visible tickets, reports, or automations as state surfaces.
metrics:
  - pulse_action_relevance
  - interval_report_usefulness
  - ticket_supply_learning
last_verified: 2026-06-27
---
# Pulse and interval automation

Pulse and interval automation is a first-class Farplane feature in [Horizon Loop](../systems/horizon-loop.md). It owns the recurring loops that keep long-running work moving without turning Farplane into a hidden scheduler.

```text
automation_loop(window, horizon_state, tickets, feedback?) -> action | report | calibration_delta
```

## System

- System: [Horizon Loop](../systems/horizon-loop.md)
- Feature ID: `FEAT-0065`
- Status: `implemented`
- Category: `planning`

## Feature Spec

This feature folds the former minimal-autonomy-loop, pulse/interval automation, and adaptive-backoff specs into one horizon-loop feature.

Core model:

- The base loop is still ticket-backed execution: plan, act, prove, review, and update durable state.
- Longer horizon autonomy uses Pulse, Interval, Rhythm, Horizon, and Goal Packet surfaces to select the next bounded action or report.
- Ticket memory is the spine; sidecar systems and earned organs are shortcuts that reduce repeated work only after the loop proves they are useful.
- Marketing/content shortcut organs are allowed early when they reduce common business work, but they should remain decoupled systems with proof gates rather than hidden magic inside the main agent.
- Ticket supply learning notices repeated unmet needs, reward closure, stale queues, and missing skills, then feeds maintenance or feature work.
- Reward closure connects actions to proof, feedback, shipped artifacts, or learning signals.

Automation cadence:

- Pulse: a fast bounded action decision. It may execute a ready ticket slice, produce a short update, or no-op when no high-value action is safe.
- Daily/interval update: reviews the recent window, reconciles ticket/report outcomes, and plans the next window.
- Weekly/horizon update: recalibrates goals, product bets, ticket supply, and skill hardening priorities.
- Adaptive backoff: repeated checks and waits widen over time, reset on progress, and honor provider/service retry hints.

Human authority:

- Humans own ambiguous business direction, destructive changes, spend, deploys, and hard-to-reverse architecture choices.
- Automations may propose and execute bounded safe work only through visible state surfaces.

Non-goals:

- No invisible background queue.
- No daemon that mutates project state without a visible automation/ticket/report owner.
- No claim that every business function needs a bespoke sidecar before the basic ticket loop works.

Proof gates:

- Each automation has a visible prompt or config owner.
- Outputs land in tickets, reports, docs, or another durable owner.
- Backoff and polling do not create untracked background work.
- Learning signals create ticket supply, skill maintenance, feature specs, or explicit no-op decisions.

## Owner Surfaces

- `farplane/automations.md`
- `skills/pulse-update/SKILL.md`
- `skills/interval-update/SKILL.md`
- `skills/automation-advisor/SKILL.md`

## Source Context

- `docs/features/FEAT-0029-goal-packet-architecture-for-native-codex-goals.md`

## Evidence

- `skills/pulse-update/eval_task.json`
- `skills/interval-update/eval_task.json`
- `skills/automation-advisor/audits/2026-06-24-automation-prompt-qa.md`

## Known Limits

Automation prompts and previewable loops exist, but Farplane still avoids hidden daemons and requires visible tickets, reports, or automations as state surfaces.

## Metrics

- `pulse_action_relevance`
- `interval_report_usefulness`
- `ticket_supply_learning`

## Maintenance

Update this feature doc before regenerating `docs/features/registry.jsonl`. If the feature stops deserving its own doc, delete this file and remove all active template, source, ticket, and system refs to `FEAT-0065`.
