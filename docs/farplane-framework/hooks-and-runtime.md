---
title: "Farplane Hooks and Runtime"
status: active
owner: farplane-framework
created_at: 2026-06-23
updated_at: 2026-06-23
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
  - docs/specs/filesystem-lifecycle.md
  - docs/specs/steer-pulse-automation.md
---

# Farplane Hooks and Runtime

Farplane hooks are small Codex boundary actions. They capture intent, send
heartbeats, and run mechanical gates. They do not own project strategy,
documentation judgment, skill optimization, or memory rewriting.

```text
hook(event, transcript/runtime_state)
  -> capture | heartbeat | mechanical_gate | handoff_ref
```

## Active Hook Events

`hooks.json` currently defines:

| Event | Commands | Purpose |
| --- | --- | --- |
| `UserPromptSubmit` | `capture_user_turn.py`, `farplane_console_ping.py` | capture current-turn user intent and send a start heartbeat |
| `Stop` | `stop_hook.py`, `farplane_console_ping.py` | evaluate mechanical stop gates and send a stop heartbeat |

These are graphable as `hook:*` nodes that `triggers` command nodes.

## Runtime State Boundaries

Runtime state lives under `.farplane/` when it is generated, mutable, local, or
too noisy for tracked config.

```text
.farplane/state/steer-scheduler.json
.farplane/reports/pulse/<timestamp>.md
.farplane/reports/steer/<job>/<timestamp>.md
.farplane/automation/decisions.jsonl
.farplane/automation/rewards.jsonl
.farplane/automation/action-outcomes.jsonl
.farplane/automation/spawned-threads.jsonl
.farplane/evals/runs/
.farplane/logs/
```

Tracked framework config stays under `farplane/`. The important separation is:

- `farplane/steer.config.toml` stores human-owned cadence and prompt intent.
- `.farplane/state/steer-scheduler.json` stores mutable due times and last
  report pointers.
- `farplane/pm.json` groups PM-visible thread IDs for UI display.
- automation runtime IDs live in the Codex app automation store, not in
  `farplane/pm.json`.

## Hook Rules

- Detect or capture cheaply.
- Gate mechanically when the required evidence is already explicit.
- Write only small, bounded runtime records unless a ticket or skill owns the
  durable write.
- Route judgment-heavy work to skills, tickets, reviewers, or drains.
- Never auto-rewrite durable memory/context files from a hook.

This rule exists because durable memory cleanup needs source preservation,
retention scoring, proposal evidence, and review. A hook can notice growth or
missing capture, but `knowledge-tidier`, `update-memory`, `learning-drain`, or
`skill-maintenance` should own the applied change.

## Graph Tags

Hook and runtime nodes should use these tags:

- `hook`: Codex hook event from `hooks.json`
- `command`: hook command target
- `runtime`: ignored local state under `.farplane/`
- `automation`: Codex automation prompt/thread surface
- `pm-ui`: UI grouping through `farplane/pm.json`
- `mechanical-gate`: deterministic stop or validation surface

These tags let the lifecycle graph show hook boundaries without implying that
hooks are a central orchestrator.

