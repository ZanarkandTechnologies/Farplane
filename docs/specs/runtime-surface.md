# Runtime Surface

Date: 2026-04-07

## Goal

Define the current target runtime surface now that `$impl` is the public
build-phase orchestrator.

This spec answers two questions:

1. which existing `bin/` helpers still matter
2. which ones should stop being documented as the future primary control plane

## Control Plane

The primary control plane is now:

- `impl-plan` for ticket planning
- `$impl` for build-phase orchestration
- `$loop` for bounded same-session persistence without ticket orchestration
- `$ralph` for serial board draining over prepared filesystem tickets
- worker lanes and runtime helpers behind the canonical `$impl` surface
- `stop_hook.py` for continuation/completion decisions

The primary control plane is not:

- `ralph_orchestrate.py`
- `ralph_worker.sh`
- direct binary-first orchestration docs

There is no separate public legacy execution surface anymore.
Same-ticket repeats re-enter `$impl`.
Serial board drains enter through `$ralph`, which selects one eligible active
ticket and then hands that ticket to `impl-plan`, `$impl`, or `close-ticket`.
It does not revive legacy binary-first orchestration.

For same-ticket build looping, the runtime contract is:

- ticket `phase/status` says the work is still in a loopable build state
- ticket frontmatter may declare durable execution requirements such as `requires_qa` and `requires_demo`
- runtime `claim` says which session/lane currently owns that work
- session ownership is explicit: only control sessions that entered through a public skill invocation may own canonical current-turn intent
- explicit `$impl` control-session invocations must seed selected-ticket runtime ownership when ticket resolution is explicit or unambiguous; a session-only control stub is not sufficient
- `impl_loop_active` says this session is currently allowed to auto-continue the `$impl` loop
- runtime `execution_phase` plus `phase_requirements` define whether the active build loop is in `impl`, `qa`, or `demo`
- tmux `auto_continue` only says whether a visible follow-up lane may be spawned or reused; it is not the global activation gate

For bounded same-session `$loop`, the runtime contract is:

- `$loop` is session-owned, not ticket-owned
- `bin/user_turn.py` seeds `skill_name: "loop"`, `loop_active`, and `loop_contract` into `.harness/state/current-run.json` plus the matching session state
- `bin/stop_hook.py` branches early on active loop state before ticket resolution
- v1 loop predicates are local and deterministic only: `completion_marker_seen`, `path_exists`, and `file_contains`
- explicit same-session stop intent clears `loop_active`; Escape/cancel is not the canonical loop-stop contract
- `skills/impl/scripts/tmux_helper.py` remains `$impl`-only in v1 and is not part of loop ownership

For serial `$ralph`, the runtime contract is:

- ticket frontmatter and body remain the queue source of truth
- selector helpers are read-only and may not create claims, mutate tickets, or
  launch agents
- each selected ticket is handed to the existing phase skill
- `$ralph` stops on no ready ticket, human gate, blocker, failed handoff, or
  loop limit
- parallel dispatch stays out of scope until worktrees, leases, merge policy,
  stale-worker handling, and batch QA are specified

For ticket-scoped isolated checkout and local QA targeting, runtime may also
persist ticket runtime records under:

- `.harness/state/tickets/TASK-XXXX.runtime.json`

Those records are runtime-only and may carry:

- branch
- checkout mode
- checkout path
- runtime mode
- declared frontend/backend targets
- reserved ports
- declared frontend/backend/compose commands
- launched process or compose metadata
- owner session alias

## Binary Decisions

| Binary | Decision | Reason |
| --- | --- | --- |
| `capture_user_turn.py` | `keep` | lightweight input-hook writer that stores bounded current-turn intent for later relevance checks |
| `notify.py` | `keep` | local utility with no orchestration overlap |
| `ticket_runtime.py` | `keep` | narrow local helper for ticket runtime records, optional isolated checkout creation, local runtime launch/stop, port reservation, and QA target publication |
| `tickets/scripts/check_ticket_metadata.py` | `keep` | canonical validator for the ticket surface and lives with the ticket system it validates |
| `stop_hook.py` | `keep` | thin runtime shim that evaluates stop events, judges worker results, and handles re-entry decisions |
| `skills/impl/scripts/tmux_helper.py` | `keep` | skill-local operator visibility and lane recovery helper, not the control plane; it also writes the active runtime claim used by stop-hook consumers |
| `ralph_orchestrate.py` | `retired` | superseded by `$impl`; removed from `bin/` once no live surfaces depended on it |
| `ralph_worker.sh` | `retired` | old phase-launch wrapper removed in favor of direct prompt/`codex exec` worker lanes |
| `export_omx_team_input.py` | `retired` | removed with the OMX bridge path because it is not part of the current skill-first runtime |

## Documentation Rules

- Public docs should describe `$impl` as the build-phase orchestrator.
- Public docs should describe `.harness/` as the canonical live runtime root.
- `capture_user_turn.py`, `skills/impl/scripts/tmux_helper.py`, and `stop_hook.py` may be documented as operator/runtime shims.
- `ticket_runtime.py` may be documented as the narrow ticket-runtime shim for
  isolated checkout, declared runtime launch/stop, and live QA target setup.
- Public docs should describe `current-run.json` as control-session-owned state, not a generic sink for every prompt-bearing session.
- Public docs should describe `.harness/state/tickets/*.runtime.json` as
  runtime-only metadata, not as a durable replacement for ticket truth.
- Public docs should describe same-ticket `$impl` continuation as requiring both the session-scoped loop gate and the matching runtime claim.
- Public docs should describe `$loop` as session-owned state with explicit local predicates, not as a ticket/run-state or tmux-worker surface.
- Public docs should describe `$ralph` as a serial filesystem-ticket
  dispatcher over existing phase skills, not as a second executor or hidden
  runtime plane.
- Public docs should describe tmux `auto_continue` as lane-follow-up plumbing, not as the source of truth for whether the `$impl` loop is active.
- Public docs should describe explicit same-session stop intent, not Escape/cancel, as the supported v1 loop-stop control.
- internal Stop-hook role instructions should live under `agents/`, not as giant string literals in Python helpers.
- Any removed prototype binaries should remain only as historical references in
  archived tickets or older specs, not as live runtime files.
- Do not present `ralph_orchestrate.py` as the preferred future entrypoint.
- Do not present the legacy Ralph runtime directory or `docs/progress.md` as
  live queue state.

## Immediate Cleanup Scope

This cleanup does:

- relabel the primary runtime story
- document keep/remove/rewrite decisions
- remove the dead prototype wrappers that are no longer load-bearing
- keep skill behavior in tracked skills, not tracked prompt files

Follow-on cleanup can further simplify the remaining shims without reopening the
control-plane decision.
