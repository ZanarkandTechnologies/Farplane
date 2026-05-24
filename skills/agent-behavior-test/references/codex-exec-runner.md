# Codex Exec Runner

Use `codex exec --json` as the default runner when you need stable logs for an
isolated agent behavior test.

## What It Captures

The JSONL stream can include:

- `thread.started` with the child thread id
- `turn.started`
- `item.started` and `item.completed` for command executions
- `agent_message` items for visible intermediary messages
- `turn.completed` with token usage

It does not expose hidden chain-of-thought. Tests should require visible
checkpoint messages and final structured reports instead.

## Minimum Artifact Set

```text
run-dir/
  prompt.md
  events.jsonl
  stderr.log
  last-message.txt
  score.json
```

Add screenshots, console logs, app server logs, or `final-report.json` when the
target behavior needs them.

## Prompt Contract

Ask the child agent to emit a visible behavior report:

```json
{
  "target": "skill-or-feature-name",
  "persona": "new user | qa tester | skill caller | reviewer",
  "checkpoints": [
    {
      "name": "loaded_required_context",
      "status": "done | skipped | blocked",
      "evidence": "file path, command, log line, or artifact"
    }
  ],
  "artifacts": ["relative/path"],
  "deviations": [
    {
      "expected": "what should have happened",
      "observed": "what happened instead",
      "owner": "skill | feature | prompt | instrumentation | unknown"
    }
  ],
  "verdict": "pass | fail | blocked"
}
```

## Recommended Command

```bash
python3 skills/agent-behavior-test/scripts/run_codex_exec_behavior_test.py \
  --cwd . \
  --prompt-file prompt.md \
  --out experiments/agent-behavior-test/demo
```

Use `--schema-file` when the final answer must match a JSON schema. Use
`--persist-session` only when the child thread must be resumable; otherwise keep
the default ephemeral run and trust the saved artifacts.

## Scoring Heuristic

Start at `pass`, then mark `fail` when any required checkpoint is missing,
required artifacts are absent, the final output is unparseable, or the child
agent took a forbidden shortcut.

Use `blocked` when the product or skill cannot be tested because access,
environment, seed data, runner permissions, or instrumentation is missing.
