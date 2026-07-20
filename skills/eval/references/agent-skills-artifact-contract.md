# Agent Skills Artifact Contract

Farplane keeps `skills/<skill>/evals/evals.json` as the durable test suite and
emits Agent Skills-shaped evidence under `.farplane/evals`.

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

- `eval`: cases, clean runs, grading, timing, benchmark, comparison, artifacts.
- Owning ticket `program.md`: instantiated harden/refine policy, metrics,
  budgets, and stop conditions.
- Owning ticket `progress.md`: append-only hypotheses, results, and run links.
- `skill-creator`: initial draft and canonical case seeding, then eval handoff.
- `skill-maintenance`: accepted writeback, then matched regression rerun.
- Farplane UI Eval OS: history, health, comparison, drilldown, and visualization.
