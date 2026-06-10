# Minimal Harness Layout

Use this shape when a repo has no eval harness yet:

```text
.farplane/evals/
├── README.md
├── run_evals.py
├── config.json
├── contexts/
│   └── agi-toy-shop.md
├── prompts/
│   ├── agent.md
│   └── judge.md
├── tasks/
│   └── harness_tasks.json
└── runs/
```

Skill-specific evals can live outside the sidecar beside the owning skill:

```text
skills/<skill-name>/eval_task.json
```

## Smoke Command

The first runner should use the real harness path and only one task.

```bash
python3 skills/eval/scripts/run_evals.py init --harness codex --target-root .
python3 .farplane/evals/run_evals.py run --harness codex --label baseline --limit 1
python3 .farplane/evals/run_evals.py run --harness codex --suite skills --label skill-baseline
```

If no runner exists yet, use this manual smoke checklist:

```text
1. JSON parses without errors.
2. Suite-wide context lives in config.json plus contexts/*. Every task has id,
   title, query, reference_points, optional context override, and optional
   tags/notes.
3. Rubric rules live in the judge prompt, not in task JSON.
4. The run report contains one result per executed task.
5. The final verdict is pass, fail, or blocked.
```

## Starter Expansion

After the first smoke pass, add only the next bottleneck:

- Add a loader script when people keep hand-validating JSON.
- Add command execution when task proof depends on tests or lint.
- Add agent run capture when the target is prompt or skill behavior.
- Add adversarial evidence review when a pass claim is easy to overstate.

## Setup Commands

Codex:

```bash
python3 skills/eval/scripts/run_evals.py status --harness codex --target-root .
python3 skills/eval/scripts/run_evals.py init --harness codex --target-root .
python3 .farplane/evals/run_evals.py run --harness codex --label baseline --limit 1
```

Claude:

```bash
python3 skills/eval/scripts/run_evals.py status --harness claude --target-root .
python3 skills/eval/scripts/run_evals.py init --harness claude --target-root .
python3 .farplane/evals/run_evals.py run --harness claude --label baseline --limit 1
```

Run `init` only when `status` reports missing eval files.

## Promptfoo Graduation Rule

Use the local runner for first harness-native behavior checks, especially when
the proof depends on Codex/Claude CLI artifacts, files, or local task reports.
Graduate to Promptfoo when the suite is stable enough to compare models,
providers, prompts, or variants in a matrix.
