---
title: "Farplane Hooks and Runtime"
status: active
owner: farplane-framework
created_at: 2026-06-23
updated_at: 2026-08-03
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

Farplane has one installed hook surface. Root `hooks.json` contains small Codex
lifecycle telemetry commands. Ticket completion and mining are explicit CLI
operations; hooks do not infer durable state transitions from arbitrary writes.

```text
codex_hook(event, transcript/runtime_state)
  -> telemetry | mechanical_gate

ticket_close(project_root, ticket_id)
  -> terminal metadata + archive + completion event -> mining route
```

## Codex Lifecycle Hooks

Root `hooks.json` currently defines:

| Event | Commands | Purpose |
| --- | --- | --- |
| `UserPromptSubmit` | `shared_checkout_guard.py`, `capture_user_turn.py`, `farplane_console_ping.py` | claim the primary Git checkout for one active session, classify the current user turn, append lightweight conversation windows, resolve native/ticket display metadata locally, and send sanitized `turn_start` hook telemetry |
| `Stop` | `final_response_gate.py`, `shared_checkout_guard.py`, `farplane_console_ping.py` | compress over-limit user-facing responses before releasing primary-checkout ownership, then send sanitized `turn_end` hook telemetry |
| `SubagentStart` | `farplane_console_ping.py` | send sanitized subagent-start lifecycle telemetry |
| `SubagentStop` | `farplane_console_ping.py` | send sanitized subagent-stop lifecycle telemetry |

These are graphable as `hook:*` nodes that `triggers` command nodes.

## Explicit Ticket Completion And Mining

`farplane/bindings.yaml#event_routes` maps an event to a versioned immutable
Core program. Core owns deterministic event/run IDs, the durable event record
and outbox, frozen replay, current-source rerun, small machine receipts, and
verdict records.

```text
event_id = sha256(source, project_id, ticket_id, content_hash)
run_id   = sha256(event_id, route_id, program_digest)
```

`farplane ticket finalize TASK-XXXX` owns the successful terminal transition. It
sets `status: done`, clears `claimed_by`, advances `updated_at`, archives the
ticket, writes `farplane.ticket.completed` to the local event store, applies the
matching route, and returns a closure/mining receipt. Failed mining leaves the
event retryable through `farplane mining drain`. There is no file watcher,
daemon, shell-tail workflow engine, or extra heartbeat.

Ticket completion has one active mining route. Its normal entry point is
`farplane ticket finalize TASK-XXXX`; `farplane mining ticket TASK-XXXX` remains
an explicit repair/backfill command. The program freezes the ticket,
optional program/progress/artifacts, and any bounded operator-turn window named
by immutable event provenance, then runs a structured read-only Codex review in
the detached drain process. A missing conversation window does not block mining
because the completed ticket packet is the required source. The executor
ignores user config and rules; Core validates output schema, evidence refs,
sensitive patterns, and raw-source overlap before accepting findings.

Each finding contains an evidenced issue, the inefficiency it caused, a proposed
improvement, owner, confidence, and stable semantic dedupe key. Core projects at
most the strongest high/medium-confidence finding into one ordinary deduped
`todo` ticket. It does not compute a ticket score, require a project KPI, emit a
human lean report, or choose an eval. Generated mining tickets cannot project
another ticket. The command resolves active or archived ticket evidence and the
latest task association from the ID alone. Missing
sources or executor failures remain replayable machine receipts. Cloud telemetry
receives status/count metadata only, never finding prose or evidence.

## Runtime State Boundaries

Runtime state lives under `.farplane/` when it is generated, mutable, local, or
too noisy for tracked config.

```text
.farplane/reports/pulse/<timestamp>.md
.farplane/reports/interval/<interval_id>/<timestamp>.md
.farplane/reports/dogfood-review/<timestamp>.md
.farplane/automation/decisions.jsonl
.farplane/automation/rewards.jsonl
.farplane/evals/runs/
.farplane/events/
.farplane/mine/
.farplane/logs/
.farplane/state/message-windows/
.farplane/state/ticket-thread-locks/
.farplane/state/ticket-thread-associations.jsonl
```

`UserPromptSubmit` does not write singleton current-run or execution-ownership
files. When a root prompt names exactly one active `TASK-XXXX`, it may atomically
write that ticket's previously empty `thread_id` frontmatter field. A ticket owns
at most one durable Codex task thread; a later root thread cannot replace it and
helpers never inherit it. Prompt text never enters ticket frontmatter or hook
telemetry.

`ticket-thread-locks/` contains short-lived atomic lock directories shared by
the hook and ticket UI writer. They protect a ticket's full read/modify/write
cycle so an ordinary ticket edit cannot replace a freshly hook-bound
`thread_id` with stale frontmatter.

`ticket-thread-associations.jsonl` remains an optional, completion-only metrics
observation surface for historical sources. It is not the ticket-to-task-thread
source of truth; lifecycle, completion mining, and UI joins resolve the ticket's
own `thread_id` first.

`shared_checkout_guard.py` is narrower than ticket execution ownership. It
stores a local lease under the primary checkout's Git directory for the active
turn and blocks a different Codex session from starting there until `Stop`
releases it. Linked Git worktrees bypass the lease because their filesystem
writes are already isolated. A stale lease expires after 24 hours; set
`FARPLANE_SHARED_CHECKOUT_GUARD=0` only for deliberate single-writer recovery.

The lifecycle publisher also reads the latest exact-id `thread_name` from the
append-only Codex `session_index.jsonl`. Telemetry sends only sanitized native
and ticket title metadata. Native names outrank ticket display titles; a native
rename is observed on the next lifecycle hook without requiring the Codex app
server or a background watcher. Subagent and eval hooks do not create or inherit
ticket thread ownership.

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
2. non-secret local settings from `~/.farplane/config.toml`
3. rendered adapter fallback `~/.codex/config.toml`

This keeps Farplane compatible with Doppler-style secret injection:
`doppler run -- farplane install`, `doppler run -- codex`, or any equivalent
runtime env source can supply API keys without making Doppler a required
Farplane dependency. `~/.farplane/config.toml` may hold local bootstrap or
UI-managed settings, but Core does not read rotatable secrets from it. See
[secret management](../fundamentals/secret-management.md).

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
Codex install path owns symlinking `hooks.json`, the lifecycle telemetry hook,
and required Core Python command targets into `~/.codex`. `farplane hooks list`
inventories every managed command and `farplane hooks doctor --json` validates
each target and interpreter.

## Hook Rules

Global Codex installation is primary-checkout-only. `farplane install`,
`farplane hooks install`, and direct `install.sh` execution reject linked Git
worktrees so `~/.codex` cannot be repointed at an ephemeral task checkout.

- Detect or capture cheaply.
- Keep live Stop behavior telemetry-only except for small deterministic gates
  with explicit evidence. The final-response gate may continue a turn only to
  compress an over-limit user-facing message; it may not judge completion,
  rewrite artifacts, start new work, or treat budget-exempt presentation as
  permission to introduce more topics.
- Write only small, bounded runtime records unless a ticket or skill owns the
  durable write.
- Route judgment-heavy work to skills, tickets, reviewers, or drains.
- Never auto-rewrite durable memory/context files from a hook.
- Do not use Stop hooks for completion review. Put QA evidence review and
  reviewer-lane completion review in the ticket `Done / Proof` block or Goal
  program final checkpoint.

Durable memory and skill cleanup need source preservation, responsibility-based
structure, proposal evidence, and review. `knowledge-tidier`, `update-memory`,
or `skill-maintenance` own that work; raw file length does not trigger it.

## Graph Tags

Hook and runtime nodes should use these tags:

- `hook`: Codex hook event from `hooks.json`
- `command`: hook command target
- `runtime`: ignored local state under `.farplane/`
- `automation`: Codex automation prompt/thread surface
- `pm-ui`: UI grouping through `farplane/pm.json`
- `mechanical-gate`: deterministic validation surface; the final-response prose
  word ceiling is hard, while the normal prose-line ceiling requests one
  semantic compression pass. Closed Mermaid, exact image/video embed lines,
  and trailing link-only references are classified separately by
  `bin/core/farplane_response.py`; malformed or mixed forms count as prose. The
  gate receives `last_assistant_message` directly, so agents do not need a
  response draft file; `farplane response check PATH|--stdin` is only an
  inspectable preflight. The gate never truncates or owns task completion.

These tags let the lifecycle graph show hook boundaries without implying that
hooks are a central orchestrator.
