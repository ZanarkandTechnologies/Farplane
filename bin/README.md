# Bin

Executable helpers for the Codex harness.

## Purpose

This folder contains small scripts used by the live Codex config and prototype orchestration flows.

## Entrypoints

- `notify.py` - local notification helper
- `check_ticket_metadata.py` - validates the canonical ticket contract
- `stop_hook.py` - optional assisted stop-hook classifier
- `ralph_worker.sh` - thin phase worker launcher for the Ralph prototype
- `ralph_judge.py` - conservative judge for Ralph phase results
- `ralph_orchestrate.py` - minimal orchestrator entrypoint for one ticket/phase

## Minimal Example

```bash
python3 bin/ralph_orchestrate.py \
  --ticket tickets/building/TASK-0010-ralph-thin-prototype.md \
  --phase planning \
  --dry-run
```

## How To Test

- `bash -n bin/ralph_worker.sh`
- `python3 -m py_compile bin/ralph_judge.py`
- `python3 -m py_compile bin/ralph_orchestrate.py`
- `python3 bin/ralph_orchestrate.py --ticket <ticket> --phase planning --dry-run`
