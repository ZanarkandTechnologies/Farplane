---
title: "Farplane Hooks and Runtime"
status: active
owner: farplane-framework
created_at: 2026-06-23
updated_at: 2026-06-27
framework_template_version: "0.2.0"
tags:
  - farplane
  - hooks
  - runtime
  - lifecycle
refs:
  - hooks.json
  - docs/farplane-framework/lifecycle.md
  - docs/farplane-framework/project-files.md
  - docs/features/FEAT-0060-registry-backed-documentation-os.md
  - docs/features/FEAT-0065-pulse-and-interval-automation.md
---

# Farplane Hooks and Runtime

Farplane hooks are small Codex boundary actions. They capture intent and send
heartbeats. They do not own project strategy, documentation judgment, skill
optimization, memory rewriting, or native Goal continuation.

```text
hook(event, transcript/runtime_state)
  -> capture | heartbeat | mechanical_gate | handoff_ref
```

## Active Hook Events

`hooks.json` currently defines:

| Event | Commands | Purpose |
| --- | --- | --- |
| `UserPromptSubmit` | `capture_user_turn.py`, `farplane_console_ping.py` | capture current-turn user intent and send `turn_start` hook telemetry |
| `Stop` | `farplane_console_ping.py` | send `turn_end` hook telemetry |

These are graphable as `hook:*` nodes that `triggers` command nodes.

## Runtime State Boundaries

Runtime state lives under `.farplane/` when it is generated, mutable, local, or
too noisy for tracked config.

```text
.farplane/reports/pulse/<timestamp>.md
.farplane/reports/interval/<interval_id>/<timestamp>.md
.farplane/automation/decisions.jsonl
.farplane/automation/rewards.jsonl
.farplane/automation/action-outcomes.jsonl
.farplane/automation/spawned-threads.jsonl
.farplane/evals/runs/
.farplane/logs/
```

Tracked framework config stays under `farplane/`. The important separation is:

- `farplane/automations.toml` stores human-owned Codex prompt text.
- Codex automation records store cadence and runtime automation IDs.
- `farplane/pm.json` groups PM-visible thread IDs for UI display.
- automation runtime IDs live in the Codex app automation store, not in
  `farplane/pm.json`.

## Telemetry Config

Codex lifecycle telemetry is defined by the installed Codex hook config.
`hooks.json` calls `hooks/farplane_console_ping.py` on `UserPromptSubmit` and
`Stop`.

`farplane_console_ping.py` loads config through Farplane Core runtime config in
this order:

1. process env
2. UI-managed `~/.farplane/config.toml`
3. rendered `~/.codex/config.toml`

Endpoint selection:

1. `FARPLANE_TELEMETRY_HOOKS_URL` when explicitly set
2. `FARPLANE_CONVEX_SITE_URL` plus `/telemetry/hooks`

The Farplane UI or its setup flow may own the `~/.farplane/*` values; the
Codex install path owns symlinking `hooks.json` and
`hooks/farplane_console_ping.py` into `~/.codex`.

## Hook Rules

- Detect or capture cheaply.
- Keep live Stop behavior telemetry-only unless a future ticket introduces a
  non-continuing guard with explicit evidence and no native Goal reentry.
- Write only small, bounded runtime records unless a ticket or skill owns the
  durable write.
- Route judgment-heavy work to skills, tickets, reviewers, or drains.
- Never auto-rewrite durable memory/context files from a hook.
- Do not use Stop hooks for completion review. Put QA evidence review and
  reviewer-lane completion review in the ticket `Done / Proof` block or Goal
  program final checkpoint.

This rule exists because durable memory cleanup needs source preservation,
retention scoring, proposal evidence, and review. A hook can notice growth or
missing capture, but `knowledge-tidier`, `update-memory`, or
`skill-maintenance` should own the applied change.

## Graph Tags

Hook and runtime nodes should use these tags:

- `hook`: Codex hook event from `hooks.json`
- `command`: hook command target
- `runtime`: ignored local state under `.farplane/`
- `automation`: Codex automation prompt/thread surface
- `pm-ui`: UI grouping through `farplane/pm.json`
- `mechanical-gate`: deterministic validation surface; no live Stop gate is
  configured by default

These tags let the lifecycle graph show hook boundaries without implying that
hooks are a central orchestrator.
