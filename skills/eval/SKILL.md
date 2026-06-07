---
name: eval
description: Check, initialize, and run harness-native evals for Codex or Claude using simple JSON tasks, boolean/tier judge prompts, and local run artifacts under .codex/evals or .claude/evals.
tier: 3
group: harness
source: local
methods:
  - eval:onboarding
allowed-tools: Read, Glob, Grep, Bash
---

# Eval

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Check whether evals are set up with `run_evals.py status` or equivalent
  bash; if missing, load [onboarding](references/onboarding.md) and guide or
  initialize setup before running.
- [ ] 2a. If adding evals, load
  [eval best practices](references/eval-best-practices.md) and edit the task or
  judge files.
- [ ] 2b. If designing a first eval or clean-room starter, use
  [onboarding](references/onboarding.md) plus the templates under
  [references/onboarding](references/onboarding/).
- [ ] 2c. If running evals, use the installed `run_evals.py run` script.
- [ ] 3. Summarize findings from `summary.json` and task detail artifacts: verdict
  counts, important failures, likely cause, and the next concrete fix.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

Use this skill when the user wants to run, create, or repair a first real eval
for an agent harness, prompt, skill, or workflow. It is intentionally
harness-native: Codex evals live under `.codex/evals`; Claude evals live under
`.claude/evals`.

Use method address `eval:onboarding` when the user needs a clean-room first
eval shape, starter JSON tasks, judge prompt guidance, or a minimal smoke
workflow before a full eval suite exists.

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

## Reference Map

- [references/onboarding.md](references/onboarding.md) - first eval setup,
  clean-room constraints, and starter workflow.
- [references/onboarding/harness-layout.md](references/onboarding/harness-layout.md) -
  minimal harness layout and smoke checklist.
- [references/onboarding/task-template.json](references/onboarding/task-template.json) -
  starter task JSON examples.
- [references/onboarding/judge-prompt-template.md](references/onboarding/judge-prompt-template.md) -
  tier/boolean judge prompt template.
- [references/onboarding/run-report-template.json](references/onboarding/run-report-template.json) -
  report shape example.
- [examples/first-harness-eval/tasks.json](examples/first-harness-eval/tasks.json) -
  clean-room starter task set.
