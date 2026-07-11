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
```

No-scope `run` executes every known available family. Use `--harness-evals`,
`--agents-md`, `--skills`, or `--skill <name>` to narrow scope. `--harness`
continues to choose the runner backend only.

Claude users should run the same `.farplane/evals/run_evals.py` commands with
`--harness claude`.

## Viewer

Use the packaged shadcn React viewer:

```bash
cd .farplane/evals/viewer-react
pnpm install
pnpm dev --host 127.0.0.1
```

Open the local URL and click `Load latest`.

For a no-install fallback, open `viewer.html` in the eval folder and pick:

- one `runs/<job_id>/summary.json`
- optional `runs/<job_id>/tasks/*.json`

That path works directly from the filesystem with file pickers.

If you want the quick loader to pull the newest run from `./runs`, serve the
folder locally first:

```bash
cd .farplane/evals
python3 -m http.server
```

## Read Results

Each run writes:

- `runs/<job_id>/summary.json`
- `runs/<job_id>/tasks/<task_id>.json`
- `runs/index.json`

Open `summary.json` first. Then inspect a task detail when something fails.
