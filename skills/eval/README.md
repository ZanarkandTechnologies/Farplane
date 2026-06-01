# Eval

Purpose: scaffold and run harness-native evals for Codex and Claude.

## Layout

```text
.codex/evals/
├── run_evals.py
├── prompts/
│   ├── agent.md
│   └── judge.md
├── tasks/
│   └── harness_tasks.json
└── runs/
```

Claude uses the same shape under `.claude/evals/`.

## Example

```bash
python3 skills/eval/scripts/run_evals.py init --harness codex --target-root .
python3 .codex/evals/run_evals.py run --harness codex --label baseline --limit 1
```

## Test

```bash
python3 skills/eval/tests/test_run_evals.py
```
