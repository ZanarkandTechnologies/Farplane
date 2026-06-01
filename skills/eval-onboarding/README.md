# Eval Onboarding

Purpose: help someone write a first clean-room eval for an agent, prompt, skill,
or harness workflow.

## Public Entrypoints

- `SKILL.md`: the workflow an agent should follow when asked to set up a first
  eval.
- `../eval/scripts/run_evals.py`: the harness-native runner used for real Codex
  or Claude evals.
- `examples/first-harness-eval/tasks.json`: starter tasks for testing a coding
  harness without using private fixtures.

## Minimal Example

```bash
python3 skills/eval/scripts/run_evals.py init --harness codex --target-root .
python3 .codex/evals/run_evals.py run \
  --harness codex \
  --label baseline
```

The command writes a job under `.codex/evals/runs/` with:

- `summary.json`
- `tasks/<task_id>.json`
- `index.json`

## How To Test

```bash
python3 skills/eval/tests/test_run_evals.py
```

Use this runner for first-eval teaching and quick local smoke checks. Use
`agent-behavior-test` when the eval should launch Codex or another child agent,
and Promptfoo when the stable suite needs model/provider matrix runs.
