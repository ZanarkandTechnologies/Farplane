# Eval Onboarding

Use this when evals are not installed yet, or when the user is new to evals and
needs guided setup before running a suite.

## Onboarding Checklist

1. Name the harness under test: `codex`, `claude`, or a custom command.
2. Name the behavior claim the eval should protect.
3. Pick one task first; avoid broad suites on day one.
4. Write `reference_points` as plain strings that describe the expected visible
   answer or artifact.
5. Keep judge policy in `prompts/judge.md`; use A-D tiers and booleans instead
   of 0-100 scores.
6. Keep `prompts/agent.md` realistic. For harness evals, use `{query}` unless
   the user explicitly wants an extra wrapper prompt.
7. Run one task with `--limit 1`.
8. Open `runs/<job_id>/summary.json`, then inspect the task detail file when
   the verdict surprises you.
9. Revise the task or judge before adding more tasks.

## Setup Commands

Codex:

```bash
python3 skills/eval/scripts/run_evals.py status --harness codex --target-root .
python3 skills/eval/scripts/run_evals.py init --harness codex --target-root .
python3 .codex/evals/run_evals.py run --harness codex --label baseline --limit 1
```

Claude:

```bash
python3 skills/eval/scripts/run_evals.py status --harness claude --target-root .
python3 skills/eval/scripts/run_evals.py init --harness claude --target-root .
python3 .claude/evals/run_evals.py run --harness claude --label baseline --limit 1
```

Run `init` only when `status` reports missing eval files.
