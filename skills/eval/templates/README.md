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

All task types live in one file. Use `tags` and `notes` to mark the layer.
Start with one or two tasks total. Add more only after the first run shows a
useful failure.

## Edit These First

- `tasks/harness_tasks.json`: skill, workflow, and system-prompt tasks.
- `prompts/judge.md`: the rubric. Keep rubric rules here, not in task JSON.

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

## Run

Run one task:

```bash
python3 .codex/evals/run_evals.py run --harness codex --label baseline --limit 1
```

Claude users should run the same commands from `.claude/evals` with
`--harness claude`.

## Read Results

Each run writes:

- `runs/<job_id>/summary.json`
- `runs/<job_id>/tasks/<task_id>.json`
- `runs/index.json`

Open `summary.json` first. Then inspect a task detail when something fails.
