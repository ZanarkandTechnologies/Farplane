---
name: eval
description: Check, initialize, and run harness-native evals for Codex or Claude using simple JSON tasks, boolean/tier judge prompts, and local run artifacts under .codex/evals or .claude/evals.
tier: 3
group: harness
source: local
allowed-tools: Read, Glob, Grep, Bash
---

# Eval

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Important Checklist

- [ ] 1. Check whether evals are set up with `run_evals.py status` or equivalent
  bash; if missing, load [onboarding](references/onboarding.md) and guide or
  initialize setup before running.
- [ ] 2a. If adding evals, load
  [eval best practices](references/eval-best-practices.md) and edit the task or
  judge files.
- [ ] 2b. If running evals, use the installed `run_evals.py run` script.
- [ ] 3. Summarize findings from `summary.json` and task detail artifacts: verdict
  counts, important failures, likely cause, and the next concrete fix.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

Use this skill when the user wants to run, create, or repair a first real eval
for an agent harness, prompt, skill, or workflow. It is intentionally
harness-native: Codex evals live under `.codex/evals`; Claude evals live under
`.claude/evals`.

## Commands

Check setup:

```bash
python3 skills/eval/scripts/run_evals.py status --harness codex --target-root .
```

Initialize only when setup is missing:

```bash
python3 skills/eval/scripts/run_evals.py init --harness codex --target-root .
```

Run installed evals:

```bash
python3 .codex/evals/run_evals.py run --harness codex --label baseline --limit 1
```

For Claude, use `--harness claude` and `.claude/evals/run_evals.py`. For custom
harnesses, pass `--eval-dir` plus command templates.

## Runner Model

The runner writes the proof surfaces this skill should summarize:

- `runs/<job_id>/summary.json`: task count, verdict counts, pass rate, and rows.
- `runs/<job_id>/tasks/<task_id>.json`: task, prompt, answer, judge, and raw
  command detail.
- `runs/index.json`: newest-first run index.
