# Eval

Purpose: scaffold and run harness-native evals for Codex and Claude.

## Layout

```text
.farplane/evals/
├── run_evals.py
├── config.json
├── contexts/
│   └── agi-toy-shop.md
├── viewer.html
├── viewer-react/
├── prompts/
│   ├── agent.md
│   └── judge.md
├── tasks/
│   └── harness_tasks.json
└── runs/
```

Codex and Claude runs use this same project-local sidecar; select the runner
with `--harness codex` or `--harness claude`.

Skill-specific eval tasks can also live beside the owning skill:

```text
skills/<skill-name>/eval_task.json
```

## Example

```bash
python3 skills/eval/scripts/run_evals.py status --harness codex --target-root .
python3 skills/eval/scripts/run_evals.py init --harness codex --target-root .
python3 .farplane/evals/run_evals.py run --harness codex --label baseline --limit 1
python3 .farplane/evals/run_evals.py run --harness codex --suite skills --label skill-baseline
```

Then open `.farplane/evals/viewer.html`, or run the shadcn React viewer:

```bash
cd .farplane/evals/viewer-react
pnpm install
pnpm dev --host 127.0.0.1
```

If you want the quick loader to fetch `./runs/index.json`, serve the folder:

```bash
cd .farplane/evals
python3 -m http.server
```

## Test

```bash
python3 skills/eval/tests/test_run_evals.py
```
