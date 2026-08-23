# Harness Evals

This folder is the local eval lab for this harness.

## Task Types

1. **Skill-level tasks** test one skill at a time.
   Example: does `advise` compare three options and name one recommendation?

2. **Workflow-level tasks** test a realistic path that combines skills.
   Example: can the harness diagnose a broken skill, choose the right owner,
   add an eval, and report proof?

3. **System-prompt tasks** test always-loaded behavior.
   Example: does the harness create or update tickets when repo policy requires
   visible task state?

Harness and workflow tasks live in `tasks/harness_tasks.json`. AGENTS.md and
system-prompt tasks live in `tasks/agents_md_tasks.json`. Use `tags` and
`notes` to mark the layer. Start with one or two tasks total. Add more only
after the first run shows a useful failure.

Skill-specific tasks may instead live in the owning skill package as
`skills/<skill-name>/evals/evals.json`. Use that modular file when a task proves
one skill's behavior rather than the whole harness.

## Edit These First

- `tasks/harness_tasks.json`: harness and cross-skill workflow tasks.
- `tasks/agents_md_tasks.json`: AGENTS.md and system-prompt behavior tasks.
- `config.json` and `contexts/*`: shared fixture setup such as AGI Toy Shop.
- `prompts/judge.md`: the rubric. Keep rubric rules here, not in task JSON,
  and use A-D tiers plus booleans instead of 0-100 scores.
- `schemas/behavior-report.schema.json`: standard final report for instrumented
  behavior traces.

Task JSON should stay simple:

```json
{
  "id": "skill_example_01",
  "title": "Skill does the main thing",
  "query": "Ask the harness to use one skill.",
  "reference_points": [
    "The answer includes required behavior A",
    "The answer avoids failure mode B"
  ],
  "tags": ["skill"],
  "notes": "Why this task matters."
}
```

Use `config.json` and `contexts/*` for stable fixture setup, company
background, role assumptions, and safety boundaries. Keep `query` as the
realistic user request the harness should answer. Add task `context` only for a
specific override, and use `"context": ""` when a task should not inherit the
default context.

AGI Toy Shop is the default fictional fixture for generic harness evals. Extend
that context for new toy tickets, product facts, UI flows, policies, or failure
cases instead of creating unrelated toy companies.

## Run

Check whether evals are installed:

```bash
python3 .farplane/evals/run_evals.py status --harness codex
```

Run one task:

```bash
python3 .farplane/evals/run_evals.py run --harness codex --label baseline --limit 1
python3 .farplane/evals/run_evals.py run --harness codex --harness-evals --label harness-only
python3 .farplane/evals/run_evals.py run --harness codex --agents-md --label agents-md
python3 .farplane/evals/run_evals.py run --harness codex --skills --label skill-baseline
python3 .farplane/evals/run_evals.py run --harness codex --skill qa --label qa-skill
python3 .farplane/evals/run_evals.py run --harness codex --skill qa --behavior-trace --behavior-output-schema .farplane/evals/schemas/behavior-report.schema.json --max-parallel-tasks 1 --label qa-trace
python3 skills/eval/scripts/run_evals.py reliability path/to/run-1/summary.json path/to/run-2/summary.json --eval-file skills/qa/evals/evals.json --output path/to/reliability.json
```

No-scope `run` executes every known available family. Use `--harness-evals`,
`--agents-md`, `--skills`, or `--skill <name>` to narrow scope. `--harness`
continues to choose the runner backend only.

Claude users should run the same `.farplane/evals/run_evals.py` commands with
`--harness claude`.

Native Codex agent, judge, and baseline invocations are always launched with
`--ephemeral --disable hooks -c notify=[]`. This isolation is enforced by the
runner after profile and user arguments; profiles remain responsible for
model, sandbox, MCP, and skill behavior, not session or telemetry safety.
Custom command templates are operator-owned and do not receive this automatic
Codex isolation tail.

`--behavior-trace` preserves the exact prompt, Codex JSONL stream, stdout and
stderr, final output, command/usage summary, checkpoint score, produced-file
inventory, and optional schema validation in each task receipt. It composes
with baseline comparison and requires `--max-parallel-tasks 1` so file deltas
remain attributable. Use Agent QA for native-subagent-only capture.

Before a material stochastic promotion, pass two or more comparable summaries
to `reliability`. `stable_pass` requires every strict grade and behavior trace
to pass across every repetition; `unstable` exposes strict-grade variance and
`fail` identifies a behavior regression. New summaries record comparison
metadata; legacy summaries retain an explicit metadata-gap warning.

## Viewer

Farplane UI `Eval OS` is the only product viewer. These templates define Core
runner inputs and artifacts only; do not add a skill-local HTML or React viewer.

## Read Results

Each run writes:

- `runs/<job_id>/summary.json`
- `runs/<job_id>/tasks/<task_id>.json`
- `runs/index.json`

Open `summary.json` first. Then inspect a task detail when something fails.
