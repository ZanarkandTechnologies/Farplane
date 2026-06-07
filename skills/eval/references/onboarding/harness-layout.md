# Minimal Harness Layout

Use this shape when a repo has no eval harness yet:

```text
.codex/evals/
├── README.md
├── run_evals.py
├── prompts/
│   ├── agent.md
│   └── judge.md
├── tasks/
│   └── harness_tasks.json
└── runs/
```

## Smoke Command

The first runner should use the real harness path and only one task.

```bash
python3 skills/eval/scripts/run_evals.py init --harness codex --target-root .
python3 .codex/evals/run_evals.py run --harness codex --label baseline --limit 1
```

If no runner exists yet, use this manual smoke checklist:

```text
1. JSON parses without errors.
2. Every task has id, title, query, reference_points, and optional tags/notes.
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
