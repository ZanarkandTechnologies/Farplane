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
- worker lanes and runtime helpers behind the canonical `$impl` surface
- `stop_hook.py` for continuation/completion decisions

The primary control plane is not:

- `ralph_orchestrate.py`
- `ralph_worker.sh`
- direct binary-first orchestration docs

There is no separate public legacy execution surface anymore.
Same-ticket repeats re-enter `$impl`.

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

## Binary Decisions

| Binary | Decision | Reason |
| --- | --- | --- |
| `capture_user_turn.py` | `keep` | lightweight input-hook writer that stores bounded current-turn intent for later relevance checks |
| `notify.py` | `keep` | local utility with no orchestration overlap |
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
- Public docs should describe `current-run.json` as control-session-owned state, not a generic sink for every prompt-bearing session.
- Public docs should describe same-ticket `$impl` continuation as requiring both the session-scoped loop gate and the matching runtime claim.
- Public docs should describe `$loop` as session-owned state with explicit local predicates, not as a ticket/run-state or tmux-worker surface.
- Public docs should describe tmux `auto_continue` as lane-follow-up plumbing, not as the source of truth for whether the `$impl` loop is active.
- Public docs should describe explicit same-session stop intent, not Escape/cancel, as the supported v1 loop-stop control.
- internal Stop-hook role instructions should live under `agents/`, not as giant string literals in Python helpers.
- Any removed prototype binaries should remain only as historical references in
  archived tickets or older specs, not as live runtime files.
- Do not present `ralph_orchestrate.py` as the preferred future entrypoint.

## Immediate Cleanup Scope

This cleanup does:

- relabel the primary runtime story
- document keep/remove/rewrite decisions
- remove the dead prototype wrappers that are no longer load-bearing
- keep skill behavior in tracked skills, not tracked prompt files

Follow-on cleanup can further simplify the remaining shims without reopening the
control-plane decision.
