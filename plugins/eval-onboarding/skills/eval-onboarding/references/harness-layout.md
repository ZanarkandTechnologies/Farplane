# Minimal Harness Layout

Use this shape when a repo has no eval harness yet:

```text
evals/
├── tasks.json
├── rubric.json
├── run-report.example.json
├── fixtures/
│   ├── todo-cli/
│   ├── notes-api/
│   └── widget-dashboard/
└── artifacts/
    └── .gitkeep
```

## Smoke Command

The first runner can be a tiny script or manual check. It only needs to prove
that tasks load and that a run report can be produced.

```bash
node evals/run.js --tasks evals/tasks.json --rubric evals/rubric.json --out evals/artifacts/latest-report.json
```

If no runner exists yet, use this manual smoke checklist:

```text
1. JSON parses without errors.
2. Every task has id, prompt, success_criteria, required_evidence, and runner.
3. Every required rubric dimension has anchors.
4. The run report contains one result per executed task.
5. The final verdict is pass, fail, or blocked.
```

## Starter Expansion

After the first smoke pass, add only the next bottleneck:

- Add a loader script when people keep hand-validating JSON.
- Add command execution when task proof depends on tests or lint.
- Add agent run capture when the target is prompt or skill behavior.
- Add adversarial evidence review when a pass claim is easy to overstate.
