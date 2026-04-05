# Prompts

Tracked `skill` prompts for `ralph` handoff sessions.

## What These Are

These files are designed to be piped directly into `codex exec`.

Example:

```bash
RALPH_TICKET="tickets/building/TASK-0042-example.md" \
RALPH_RUN_STATE=".ralph/runs/run-20260405-001.json" \
codex exec --skip-git-repo-check -C "$ROOT" - < prompts/ralph.md
```

## Runtime Inputs

Primary runtime source:

- `.ralph/state/current-run.json`

Expected fields there:

- `ticket_path`
- `phase`
- `run_id`
- optional `next_phase`
- optional `executor_target`

Optional environment overrides:

- `RALPH_TICKET`
  Override canonical ticket path for the current skill worker
- `RALPH_RUN_STATE`
  Optional run-state path for volatile execution metadata
- `RALPH_EXECUTOR_TARGET`
  Optional scheduler hint for remote/local execution lanes

## Result Line Contract

Every prompt requires exactly one final line:

```text
RALPH_RESULT: status=<enum> next=<enum> reason=<optional>
```

The orchestrator or judge reads that line and decides what to do next.

## Prompt Inventory

- `ralphplan.md`
- `ralph.md`
