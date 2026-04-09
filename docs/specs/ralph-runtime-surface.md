# Ralph Runtime Surface

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
- worker lanes such as `ralph` where a persistent build loop is useful
- `stop_hook.py` for continuation/completion decisions

The primary control plane is not:

- `ralph_orchestrate.py`
- `ralph_worker.sh`
- direct binary-first orchestration docs

Those are prototype or transitional surfaces.

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
- `capture_user_turn.py`, `skills/impl/scripts/tmux_helper.py`, and `stop_hook.py` may be documented as operator/runtime shims.
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
