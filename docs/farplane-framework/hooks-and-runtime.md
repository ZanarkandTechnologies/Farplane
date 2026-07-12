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
  -> durable FileEvent/outbox -> fixed local drain subprocess -> routes
```

## Codex Lifecycle Hooks

Root `hooks.json` currently defines:

| Event | Commands | Purpose |
| --- | --- | --- |
| `UserPromptSubmit` | `capture_user_turn.py`, `farplane_console_ping.py` | classify the current user turn, append lightweight conversation windows, and send `turn_start` hook telemetry |
| `Stop` | `farplane_console_ping.py` | send `turn_end` hook telemetry |
| `PostToolUse` read/thread matchers | `farplane_local_event.py` | record small sanitized local skill/thread observations without Farplane UI |
| `PostToolUse` write matchers | `farplane_file_change.py` | capture typed file events into the local outbox and launch the Core local drain process |

These are graphable as `hook:*` nodes that `triggers` command nodes.

## Project File Events And Mining

Project `farplane/hooks.json` declares allowed file patterns and event names.
`farplane/bindings.yaml#event_routes` maps an event to a versioned immutable
Core program. Core owns deterministic event/run IDs, privacy-safe snapshots,
the durable outbox, frozen replay, current-source rerun, lean reports, and
verdict records.

```text
event_id = sha256(project_id, event_name, entity_ref, previous_hash, content_hash)
run_id   = sha256(event_id, route_id, program_digest)
```

Session and task IDs are provenance only. The hook process does not run mining
itself and does not call a cloud dispatcher. It writes the typed event and
outbox row first, then launches the fixed Core local drain entrypoint in a
separate process. That child reads the local outbox, applies every matching
`event_routes` row, and writes immutable local runs/reports. Failed launches
write `.farplane/hooks/drain-launches/*.json` receipts and leave outbox rows
retryable; operators or UI can still call `farplane mining drain`. There is no
daemon, shell-tail workflow engine, or extra heartbeat.

Ticket completion fans out to two immutable Core programs. The lean report
contains `source`, `program`, `coverage`, `observations`, `material_findings`,
`source_gaps`, and `escalation` without a false-precision quality score. The
completion-learning program freezes the ticket packet with only the bounded
operator-turn window named by immutable event thread/session provenance, then
runs a structured read-only Codex review in the detached drain process.
Assistant responses are intentionally excluded: ticket/program/progress are
the authoritative completion record. The executor ignores user config and
rules; Core validates the output schema, evidence refs, sensitive patterns, and
raw-source overlap before accepting a report. It emits compact
problem/solution/owner/evidence findings, then deterministically projects at
most the strongest high/medium-confidence finding into one deduped local
`todo` ticket with a source-ticket or self-improvement KPI Reward. When no
declared project KPI exists, Core still writes the ticket as `awaiting_review`
instead of admitting metricless work. Known corrections become direct-fix
tickets; uncertain improvements become prove-or-reject tickets. A validated
semantic `dedupe_key` collapses paraphrased equivalents across active/archive
tickets, and completion-learning-generated tickets are report-only on their
own completion so projection cannot recurse. The semantic executor still never
edits docs, skills, tickets, or external systems. Missing association or executor failures become visible
replayable source gaps; there is no turn-count trigger or daily scan. Cloud
telemetry receives status/count metadata only, never finding prose or evidence.

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
Codex install path owns symlinking `hooks.json`, `hooks/*.py`, and required
Core Python command targets into `~/.codex`. `farplane hooks list` inventories
every managed command, `farplane hooks doctor --json` validates each target and
interpreter, and `farplane hooks test --project-root <fixture> --json` runs the
deterministic Core hook runtime smoke from
`qa/cookbook/core-hooks-runtime.md`.

## Hook Rules

- Detect or capture cheaply.
- Keep live Stop behavior telemetry-only unless a future ticket introduces a
  non-continuing guard with explicit evidence and no native Goal reentry.
- Write only small, bounded runtime records unless a ticket or skill owns the
  durable write.
- Route judgment-heavy work to skills, tickets, reviewers, or drains.
- Persist file events before advancing snapshots; retry route failure from the
  outbox rather than dropping or duplicating work.
- Keep file-change mining out of the hook process. Launch only the fixed
  Core-owned local drain entrypoint, and keep launch failures inspectable while
  leaving pending events retryable.
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
