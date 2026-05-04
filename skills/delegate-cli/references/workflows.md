# Delegate CLI Workflows

## Dry-Run First

1. Run `doctor`.
2. Run `setup`.
3. Run `run --dry-run`.
4. Inspect the rendered prompt and command.
5. Run live only after human gates for credentials, spend, and filesystem
   writes are satisfied.

Dry-run mode records the intended checkout path but does not create a Git
worktree. A live run with `--checkout worktree` creates a detached worktree
under the run directory before invoking the external CLI.

Live mode fails before invoking the external CLI when required provider
environment variables such as `OPENROUTER_API_KEY` are missing. Treat a
`doctor` result with `ok: true` and `live_ready: false` as dry-run-ready only.

## Ticket Evidence

When `--ticket` is supplied, copy durable artifacts under:

```text
tickets/TASK-XXXX/artifacts/external-cli/<run-id>/
```

Runtime-only bundles stay under:

```text
.harness/external-cli/runs/<run-id>/
```
