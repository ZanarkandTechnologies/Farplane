# Eval

Purpose: scaffold and run harness-native evals for Codex and Claude.

## Layout

```text
.codex/evals/
├── run_evals.py
├── viewer.html
├── viewer-react/
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
python3 skills/eval/scripts/run_evals.py status --harness codex --target-root .
python3 skills/eval/scripts/run_evals.py init --harness codex --target-root .
python3 .codex/evals/run_evals.py run --harness codex --label baseline --limit 1
```

Then open `.codex/evals/viewer.html`, or run the shadcn React viewer:

```bash
cd .codex/evals/viewer-react
pnpm install
pnpm dev --host 127.0.0.1
```

If you want the quick loader to fetch `./runs/index.json`, serve the folder:

```bash
cd .codex/evals
python3 -m http.server
```

## Test

```bash
python3 skills/eval/tests/test_run_evals.py
```
