# Agent Skills Artifact Contract

Farplane keeps `skills/<skill>/evals/evals.json` as the durable test suite and
emits Agent Skills-shaped evidence into the artifact root read by Farplane
Office. The Promptfoo adapter honors `FARPLANE_EVALS_ROOT`, otherwise reuses an
existing `~/.farplane/evals/runs/index.json`, and falls back to the current
project's `.farplane/evals` directory.

For Promptfoo comparisons, each task directory additionally preserves the
generated `promptfooconfig.json`, raw `promptfoo-results.json`, command and log
evidence, `normalized.json`, and copied candidate/baseline workspaces. Generated
Promptfoo config is run evidence, never a second authored suite.

```text
.farplane/evals/
  runs/<job-id>/
    summary.json
    benchmark.json
    tasks/<task-id>.json
    tasks/<task-id>/
      candidate/
        outputs/agent_answer.txt
        timing.json
        grading.json
      baseline/                 # comparison runs only
        outputs/agent_answer.txt
        timing.json
        grading.json
      comparison.json           # comparison runs only
```

`schema_version: 2` identifies this contract. Existing Farplane task details
and behavior traces remain in the same job so harness-specific proof is not
lost. Farplane UI Eval OS is the only browser renderer.

## Ownership

- Agent Skills manifest: the only authored skill behavior cases.
- Promptfoo: target execution, inferred skill use, rubric grading, timing,
  token data, and raw comparison export.
- `eval` adapter: source validation, clean workspaces, profile projection,
  source immutability, file deltas, and normalized schema-v2 receipt.
- Existing Eval runner: project suites and isolated behavior traces during the
  migration window.
- Owning ticket `program.md`: instantiated harden/refine policy, metrics,
  budgets, and stop conditions.
- Owning ticket `progress.md`: append-only hypotheses, results, and run links.
- `skill-creator`: initial draft and canonical case seeding, then eval handoff.
- `skill-maintenance`: accepted writeback, then matched regression rerun.
- Farplane UI Eval OS: history, health, comparison, drilldown, and visualization.
