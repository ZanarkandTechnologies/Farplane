---
name: eval-onboarding
description: Guide newcomers through setting up a minimal, clean-room eval harness for coding agents, prompts, skills, or workflow changes. Use when the user asks for basic eval JSON tasks, synthetic fixtures, judge shape, harness setup, or an example evaluation workflow without copying private or third-party systems.
tier: 3
group: harness
source: local
common_chains:
  after: ["testing", "agent-qa-test"]
allowed-tools: Read, Glob, Grep, Bash
---

# Eval Onboarding

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Important Checklist

- [ ] Confirm the eval target, user-visible behavior, and smallest useful
  pass/fail claim.
- [ ] Keep the fixture set clean-room: use invented tasks, synthetic repos, and
  generic file names; do not inspect or copy private example systems.
- [ ] If the operator wants inspiration from a private example, capture only
  sanitized, high-level pattern notes and convert them into new clean-room
  tasks.
- [ ] Use [testing](../testing/SKILL.md) to choose the cheapest meaningful
  proof level before adding harness machinery.
- [ ] Define the JSON task schema, tier/boolean judge fields, expected artifacts, and
  runner contract.
- [ ] Create or adapt 3-5 starter tasks that cover happy path, edge path,
  failure path, and regression/canary path.
- [ ] Decide whether the eval needs `agent-behavior-test` run capture or
  `agent-qa-test` adversarial evidence review.
- [ ] Run or document one smoke command that proves the harness can load tasks
  and emit a run report.
- [ ] Use [execute](../execute/SKILL.md) for final proof/writeback when eval
  files are added to a repo.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

Use this skill when a newcomer needs a small evaluation harness for a coding
agent, prompt, skill, or workflow and the immediate goal is a clear starter
shape rather than a full benchmark platform.

This skill is intentionally clean-room. If the operator mentions a private,
restricted, interview, client, or proprietary eval example, use it only through
sanitized pattern notes. The operator may describe non-confidential traits such
as "it had task JSON, expected files, a rubric, and run reports"; convert those
traits into new invented examples. Do not read, copy, quote, or structurally
recreate the private source unless the operator explicitly confirms that source
is shareable.

## Job

Create a minimal eval setup that answers:

1. What behavior are we testing?
2. Which synthetic JSON tasks exercise it?
3. How does a runner execute each task?
4. What evidence does the judge inspect?
5. What run report proves pass, fail, or blocked?

## First-Load Workflow

1. Name the eval target: skill behavior, coding task, prompt conformance,
   workflow adherence, app behavior, or regression.
2. Write one claim under test:
   `Claim: <behavior this eval proves when it passes>`.
3. If inspiration comes from a private example, write a short clean-room
   inspiration note using only abstract traits:
   - artifact types, such as tasks, rubric, report, fixtures, or logs
   - evaluator flow, such as load task, run agent, judge evidence, write report
   - quality bar, such as proof required, forbidden shortcuts, or blocker shape
   Avoid names, prompts, code, exact schema, judge text, and fixture details.
4. Pick the smallest harness shape:
   - **Static JSON review** when the eval only checks artifact contents.
   - **Command runner** when tasks require scripts, tests, or repo commands.
   - **Agent run capture** when the subject is an agent following a prompt or
     skill.
   - **Adversarial QA loop** when readiness depends on skeptical evidence
     review.
5. Copy and adapt the reference templates:
   - [task-template.json](references/task-template.json)
   - [judge-prompt-template.md](references/judge-prompt-template.md)
   - [run-report-template.json](references/run-report-template.json)
   - [harness-layout.md](references/harness-layout.md)
   Or start from the runnable harness-native starter in [eval](../eval/SKILL.md):
   - [first-harness-eval/tasks.json](examples/first-harness-eval/tasks.json)
   - [eval run_evals.py](../eval/scripts/run_evals.py)
6. Start with 3-5 synthetic tasks:
   - one obvious success path
   - one realistic ambiguity path
   - one failure or refusal path
   - one regression canary for a known bug or invariant
7. Define judge inputs before running: changed files, command output, child
   agent event logs, screenshots, JSON reports, or reviewer notes.
8. Run a smoke pass that loads the task JSON and writes a report, even if the
   first judge is manual.
9. Record the result in the durable surface the repo uses: ticket evidence,
   `experiments/`, CI artifact, or the eval harness directory.

## Starter Runner

Use the `eval` skill runner when the first goal is to test the real harness
path:

```bash
python3 skills/eval/scripts/run_evals.py init --harness codex --target-root .
python3 .codex/evals/run_evals.py run \
  --harness codex \
  --label baseline
```

Supported flags:

- `--tasks`: path to a JSON list of task objects.
- `--label`: short label used in the generated job ID.
- `--limit`: optional cap on how many tasks to run.
- `--max-parallel-tasks`: optional concurrency cap for API/key friendliness.
- `--agent-command-template` and `--judge-command-template`: optional custom
  command wrappers for non-Codex/non-Claude harnesses or tests.

Each run writes:

- `<harness>/evals/runs/<job_id>/summary.json`: aggregate metrics and task rows.
- `<harness>/evals/runs/<job_id>/tasks/<task_id>.json`: task, prompt, answer,
  judge, and raw command detail.
- `<harness>/evals/runs/index.json`: newest-first job index.

Use `agent-behavior-test` only when the runner's CLI artifacts are not enough
and a separate child-agent behavior capture is needed. Graduate to Promptfoo
when the suite is stable enough to compare models, providers, prompts, or
variants in a matrix.

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

## Gotchas

- Do not copy private task text, file names, judge logic, fixtures, or repo
  structure from restricted examples. Invent replacement values.
- Do not treat "inspired by" as permission to inspect protected files. Use
  sanitized pattern notes, then make new JSON values.
- Do not call prose confidence a pass. A pass needs artifacts, command output,
  logs, screenshots, or structured reviewer evidence.
- Do not overbuild the first harness. A JSON task file plus a report schema is
  enough until repeated runs expose the next bottleneck.
- Do not mix target behavior with judge policy. Tasks say what to attempt;
  rubrics say what counts.

## Judgment Questions

Use `advise` when these choices are material:

- manual review vs automated judge
- JSON-only fixture vs executable repo fixture
- local script vs CI job
- single-agent run capture vs adversarial QA loop
- boolean verdicts vs coarse tiers

## Outcome Contract

A completed onboarding pass leaves:

- an eval target and claim under test
- a task JSON file with synthetic tasks
- a judge prompt or equivalent evaluator contract
- a run report template or produced smoke report
- a smoke command, artifact path, or explicit next proof step

Keep generated examples generic unless the user provides shareable domain
details. Synthetic names like `todo-cli`, `notes-api`, and `widget-dashboard`
are preferred over references to real private systems.
