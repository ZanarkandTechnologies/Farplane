# Eval Onboarding

Use method address `eval:onboarding` when evals are not installed yet, or when
the user needs a first clean-room eval shape before running a suite.

This reference is intentionally clean-room. If the operator mentions a private,
restricted, interview, client, or proprietary eval example, use it only through
sanitized pattern notes. Convert abstract traits such as task JSON, rubric
prompt, runner, report shape, or quality bar into new invented examples. Do not
copy private task text, file names, prompts, schemas, fixtures, or repo
structure unless the source is explicitly shareable.

## First Eval Workflow

1. Name the eval target: skill behavior, coding task, prompt conformance,
   workflow adherence, app behavior, or regression.
2. Write one claim under test:
   `Claim: <behavior this eval proves when it passes>`.
3. Pick the smallest harness shape:
   - **Static JSON review** when the eval only checks artifact contents.
   - **Command runner** when tasks require scripts, tests, or repo commands.
   - **Agent run capture** when the subject is an agent following a prompt or
     skill.
   - **Adversarial QA loop** when readiness depends on skeptical evidence
     review.
4. Start with one task; grow to `3-5` synthetic tasks only after the smoke pass.
5. Cover happy path, ambiguity path, failure/refusal path, and regression canary
   when the suite grows beyond one task.
6. Write `reference_points` as plain strings that describe the expected visible
   answer or artifact.
7. Keep judge policy in `prompts/judge.md`; use A-D tiers and booleans instead
   of 0-100 scores.
8. Define judge inputs before running: changed files, command output, child
   agent event logs, screenshots, JSON reports, or reviewer notes.
9. Keep `prompts/agent.md` realistic. For harness evals, use `{query}` unless
   the user explicitly wants an extra wrapper prompt.
10. Run one task with `--limit 1`, inspect `summary.json`, then inspect task
    detail when the verdict surprises you.
11. Revise the task or judge before adding more tasks.

## Templates

- [onboarding/task-template.json](onboarding/task-template.json)
- [onboarding/judge-prompt-template.md](onboarding/judge-prompt-template.md)
- [onboarding/run-report-template.json](onboarding/run-report-template.json)
- [onboarding/harness-layout.md](onboarding/harness-layout.md)
- [../examples/first-harness-eval/tasks.json](../examples/first-harness-eval/tasks.json)

## Decision Branches

- **New skill eval:** task prompts must require the child agent to load the
  skill, show checklist progress, create the expected artifact, and report what
  it skipped.
- **Coding harness eval:** each task should name repo setup, allowed files,
  command budget, expected evidence, and disallowed shortcuts.
- **Prompt eval:** each task should include the prompt input, expected visible
  checkpoints, and failure signals such as asking for unnecessary permission or
  skipping proof.
- **Regression eval:** keep task IDs stable and compare new run reports against
  the previous accepted report.

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

## Promptfoo Graduation Rule

Use the local runner for first harness-native behavior checks, especially when
the proof depends on Codex/Claude CLI artifacts, files, or local task reports.
Graduate to Promptfoo when the suite is stable enough to compare models,
providers, prompts, or variants in a matrix.
