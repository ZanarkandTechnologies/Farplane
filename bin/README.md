# Bin

Executable helpers for the Codex harness.

## Purpose

This folder contains small scripts used by the live Codex config plus a few
transitional runtime helpers from the earlier Ralph prototype.

Primary control plane:

- `impl-plan`
- `$impl`
- persistent builder lanes
- `stop_hook.py`

Stop-hook role instructions are canonical TOML configs under `agents/`.
`stop_hook.py` reads those TOML files directly and injects their exact
`developer_instructions` into `codex exec`.

The `bin/` directory is now mostly shim/utility territory, not the main
orchestration story.

## Entrypoints

- `check_doc_parity.py` - narrow canonical-doc parity validator for README/spec/ticket surfaces
- `capture_user_turn.py` - turn-start user-intent writer for the hook surface
- `notify.py` - local notification helper
- `stop_hook.py` - thin stop-hook/runtime shim

## Runtime Decisions

- `stop_hook.py`: keep
- `capture_user_turn.py`: keep

Runtime state stays lightweight and machine-facing. The grouped `claim` object
tracks the active ticket/run/session ownership for hook consumers, while
`last_user_turn` carries the saved current-turn user ask.

Delegated worker metadata is additive:

- `worker_name` identifies the lane role for the current live path
- `main_artifact_path` points at the worker's canonical work object
- `grounding_summary` captures the worker's explicit artifact-grounding line when available
- `worker_started_at`, `last_checkpoint_at`, and `checkpoint_summary` support stale-wait backpressure reads

The live `status` surface now derives a first advisory backpressure signal:

- `backpressure_state`: `within_budget`, `over_budget`, `inactive`, or `unknown`
- `stale_for_secs`: elapsed seconds since the latest checkpoint when available
- `recommended_action`: present for over-budget waits

Runtime routing is session-first for parallel Codex usage:

- explicit run-state selector when a managed lane exports one
- hook `session_id` for lane-scoped session state
- `.harness/state/current-run.json` as the compatibility pointer / last-active selector, with `.ralph/state/current-run.json` kept only as legacy fallback during migration

See [the runtime-surface spec](/Users/kenjipcx/coding-harness/Codexter/docs/specs/ralph-runtime-surface.md) for the canonical decision table.

## Minimal Example

```bash
python3 skills/impl/scripts/tmux_helper.py launch \
  --ticket tickets/TASK-0014-tmux-visibility-and-followup.md \
  --phase building \
  --dry-run

python3 skills/impl/scripts/tmux_helper.py followup \
  --ticket tickets/TASK-0014-tmux-visibility-and-followup.md \
  --phase documenting \
  --reason "hook-driven follow-up"

python3 skills/impl/scripts/tmux_helper.py status

```

In the live interactive path, `$impl` is the orchestrator contract and
`skills/impl/scripts/tmux_helper.py` is only a visibility/recovery helper.
Same-lane continuations come from the normal Stop-hook block/continue flow.
`followup` is the fallback path when a lane must be recreated or resumed from
stored session metadata. `status` centralizes the active lane plus the latest
hook verdict, falling back to the Stop-hook log when the live run state has
already advanced.

## How To Test

- `python3 bin/check_doc_parity.py`
- `python3 -m unittest bin/test_doc_parity.py`
- `python3 -m py_compile bin/stop_hook.py`
- `python3 -m py_compile bin/capture_user_turn.py bin/user_turn.py`
- `python3 -m py_compile bin/check_doc_parity.py bin/test_doc_parity.py`
- `python3 -m py_compile skills/impl/scripts/tmux_helper.py`
- `python3 -m unittest discover -s bin -p 'test_*.py'`
- `python3 skills/impl/scripts/tmux_helper.py launch --ticket <ticket> --phase building --tmux-session <session> --dry-run`
- `python3 skills/impl/scripts/tmux_helper.py followup --ticket <ticket> --phase documenting --run-state <run-state> --dry-run`
- `python3 skills/impl/scripts/tmux_helper.py status`
