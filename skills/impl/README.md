# Impl Skill Support

Support files for the `impl` skill live here.

## Purpose

This area contains orchestration helpers used by `$impl`, especially the
tmux-backed lane launcher and follow-up utilities.

## Public Entrypoints

- `SKILL.md` - build-phase orchestration contract
- `scripts/tmux_helper.py` - launch, follow up, and inspect visible tmux lanes

The first live delegated-worker contract is carried in runtime state:

- `worker_name`
- `main_artifact_path`
- `grounding_summary`
- `worker_started_at`
- `last_checkpoint_at`
- `checkpoint_summary`

## Minimal Example

```bash
python3 skills/impl/scripts/tmux_helper.py launch \
  --ticket tickets/TASK-0026-enforce-delegated-worker-contract.md \
  --phase building \
  --worker-name builder \
  --dry-run
```

## How To Test

- `python3 -m py_compile skills/impl/scripts/tmux_helper.py`
- `python3 -m unittest bin/test_tmux_helper.py`
- `python3 skills/impl/scripts/tmux_helper.py launch --ticket <ticket> --phase building --tmux-session <session> --dry-run`
- `python3 skills/impl/scripts/tmux_helper.py followup --ticket <ticket> --phase documenting --run-state <run-state> --dry-run`
- `python3 skills/impl/scripts/tmux_helper.py status --run-state <run-state>`
