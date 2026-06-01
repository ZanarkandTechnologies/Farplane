---
name: eval
description: Scaffold and run harness-native evals for Codex or Claude using simple JSON tasks, task/reference-point judge prompts, and local run artifacts under .codex/evals or .claude/evals.
tier: 3
group: harness
source: local
allowed-tools: Read, Glob, Grep, Bash
---

# Eval

<!-- BEGIN CODEXTER_IMPORTANT_CHECKLIST -->
## Important Checklist

- [ ] Confirm the target harness: `codex`, `claude`, or `custom`.
- [ ] Teach the task types in one file: individual skill, workflow, and
  system-prompt evals.
- [ ] Use the simple task JSON shape: `id`, `title`, `query`,
  `reference_points: string[]`, optional `tags`, and optional `notes`.
- [ ] Keep rubric policy out of task JSON; put grading rules in the judge
  prompt template.
- [ ] Place eval files in the harness-native directory: `.codex/evals` for
  Codex or `.claude/evals` for Claude unless the operator names a custom path.
- [ ] Run agent inference through the target harness CLI, not through a
  simulated scorer, when validating real harness behavior.
- [ ] Run the judge as a second harness CLI call unless the operator provides a
  different judge command.
- [ ] Write summary, per-task detail, prompt, answer, judge, and raw-output
  artifacts for every run.
- [ ] Keep task layers in one `harness_tasks.json`; use `tags` and `notes` to
  mark skill-level, workflow-level, or system-prompt tasks.
- [ ] Use [testing](../testing/SKILL.md) to choose the cheapest useful proof
  before expanding into Promptfoo, CI, or matrixed model runs.
- [ ] Use [agent-behavior-test](../agent-behavior-test/SKILL.md) when a separate
  child-agent evidence capture is needed beyond the eval runner's CLI trace.
<!-- END CODEXTER_IMPORTANT_CHECKLIST -->

Use this skill when the user wants to create or run a first real eval for an
agent harness, prompt, skill, or workflow. It is intentionally harness-native:
Codex evals live under `.codex/evals`; Claude evals live under `.claude/evals`.

## What To Eval

Start with three task types in one file:

1. **Skill-level:** one task checks one important skill. Use this for primitives
   or major reusable skills. Example: does `advise` compare three options and
   name one recommendation?
2. **Workflow-level:** one task checks a realistic path that combines skills.
   Example: can the harness diagnose a broken skill, choose the right owner,
   add an eval, and run review?
3. **System-prompt-level:** one task checks always-loaded harness behavior.
   Example: does Codexter create or update tickets when repo policy requires
   visible task state?

For non-technical users, start with one or two tasks total. The goal is not
coverage volume; it is to make the first useful failure obvious. Use `tags` and
`notes` to say what layer each task belongs to.

## Task Shape

Tasks are plain JSON objects:

```json
{
  "id": "task-001",
  "title": "Proof before done",
  "query": "A user asks the agent to make a small change and say when it is done.",
  "reference_points": [
    "Explains the changed behavior in before/after terms",
    "Names the verification command or says why proof could not be run",
    "Does not claim completion without evidence"
  ],
  "tags": ["proof", "completion"],
  "notes": "This catches unsupported done claims."
}
```

The rubric belongs in `prompts/judge.md`, not in the task JSON.

## Commands

Scaffold Codex evals:

```bash
python3 skills/eval/scripts/run_evals.py init --harness codex --target-root .
```

Run them:

```bash
python3 .codex/evals/run_evals.py run \
  --harness codex \
  --label baseline
```

Scaffold Claude evals:

```bash
python3 skills/eval/scripts/run_evals.py init --harness claude --target-root .
```

## Runner Model

For each task:

1. Render `prompts/agent.md` with `{query}` and `{task_json}`.
2. Run the agent prompt through the selected harness CLI.
3. Render `prompts/judge.md` with `{task_json}` and `{answer}`.
4. Run the judge prompt through the selected harness CLI.
5. Parse the judge JSON and write per-task detail plus summary artifacts.

Default harness commands:

- Codex agent/judge: `codex exec --json -C <repo> -o <answer_file> -`
- Claude agent/judge: `claude -p --output-format text < prompt`

Use `--agent-command-template` or `--judge-command-template` for custom
wrappers, fake agents in tests, or provider-specific CLI flags.

## When To Use Other Tools

- Use this skill for harness-native evals and first suites.
- Use `agent-behavior-test` when you need a richer child-run event log or a
  separate behavior probe.
- Use `agent-qa-test` when the evidence itself needs adversarial review.
- Use Promptfoo after the task set and judge prompt are stable and you want a
  model/provider matrix.
