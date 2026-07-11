---
title: "Farplane Hooks and Runtime"
status: active
owner: farplane-framework
created_at: 2026-06-23
updated_at: 2026-07-12
framework_template_version: "0.3.0"
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

Farplane has two explicit hook surfaces. Root `hooks.json` contains installed
Codex lifecycle commands. Project `farplane/hooks.json` selects typed file
events for portable Core mining. Neither owns project strategy, skill
optimization, memory rewriting, or native Goal continuation.

```text
codex_hook(event, transcript/runtime_state)
  -> telemetry | mechanical_gate

file_change(project_root, path)
  -> drain_pending -> durable FileEvent -> snapshot -> routes -> drain_pending
```

## Codex Lifecycle Hooks

Root `hooks.json` currently defines:

| Event | Commands | Purpose |
| --- | --- | --- |
| `UserPromptSubmit` | `capture_user_turn.py`, `farplane_console_ping.py` | classify the current user turn, append lightweight conversation windows, and send `turn_start` hook telemetry |
| `Stop` | `farplane_console_ping.py` | send `turn_end` hook telemetry |

These are graphable as `hook:*` nodes that `triggers` command nodes.

## Project File Events And Mining

Project `farplane/hooks.json` declares allowed file patterns and event names.
`farplane/bindings.yaml#event_routes` maps an event to a versioned immutable
Core program. Core owns deterministic event/run IDs, privacy-safe snapshots,
the durable outbox, frozen replay, current-source rerun, lean reports, and
verdict records.

```text
event_id = sha256(project_id, event_name, entity_ref, previous_hash, content_hash)
run_id   = sha256(event_id, route_id, program_digest, input_digest)
```

Session and task IDs are provenance only. Failed routes remain retryable; each
later hook call drains pending work before and after capture, and operators or
UI can call `farplane mining drain`. There is no daemon or extra heartbeat.

The default completion report contains `source`, `program`, `coverage`,
`observations`, `material_findings`, `source_gaps`, and `escalation`. It does
not emit a false-precision scalar quality score.

## Runtime State Boundaries

Runtime state lives under `.farplane/` when it is generated, mutable, local, or
too noisy for tracked config.

```text
.farplane/reports/pulse/<timestamp>.md
.farplane/reports/interval/<interval_id>/<timestamp>.md
.farplane/reports/dogfood-review/<timestamp>.md
.farplane/automation/decisions.jsonl
.farplane/automation/rewards.jsonl
.farplane/automation/action-outcomes.jsonl
.farplane/automation/spawned-threads.jsonl
.farplane/evals/runs/
.farplane/events/
.farplane/file-events/
.farplane/mine/
.farplane/logs/
.farplane/state/message-windows/
.farplane/state/ticket-thread-associations.jsonl
```

`UserPromptSubmit` does not write singleton current-run or per-session
ownership files. Hook telemetry, conversation windows, explicit run-state files
owned by managed lanes, tickets, and ticket/thread association logs are the live
surfaces.

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
2. private local fallback/cache `~/.farplane/config.toml`
3. rendered adapter fallback `~/.codex/config.toml`

This keeps Farplane compatible with Doppler-style secret injection:
`doppler run -- farplane install`, `doppler run -- codex`, or any equivalent
runtime env source can supply API keys without making Doppler a required
Farplane dependency. `~/.farplane/config.toml` may still hold local bootstrap
or UI-managed fallback values, but it is not the preferred canonical source for
rotatable secrets when an injector is available.

In this Farplane checkout, use `farplane run -- <command>` as the standard
project wrapper for credentialed scripts. It checks the current project's
Doppler setup and runs `doppler run -- <command>` so skill scripts can live
under `skills/` while resolving secrets from the project scope.

Readiness and repair stay on the existing verbs: `farplane doctor` reports
Core, hook, UI, local-config, and Doppler readiness; `farplane install` performs
safe mechanical render/link/repair work and wraps its installer subprocess with
Doppler when this checkout declares Doppler and the shell is not already
Doppler-injected. Do not add a separate setup/sync command for this lifecycle.

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
- Persist file events before advancing snapshots; retry route failure from the
  outbox rather than dropping or duplicating work.
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
