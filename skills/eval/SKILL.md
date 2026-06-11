---
name: eval
description: "Turn agent, prompt, or skill behavior into local eval tasks, boolean or tier judges, run artifacts, and verdicts."
tier: 3
group: harness
source: local
skill_template_version: "0.2.0"
feature_refs:
  - FEAT-0054
methods:
  - eval:onboarding
allowed-tools: Read, Glob, Grep, Bash
---

# Eval

## Context

Use this skill when the user wants to run, create, or repair a first real eval
for an agent harness, prompt, skill, or workflow. It is intentionally
harness-native: project working evals live under `.farplane/evals` for Codex
or Claude runs. Repo-owned reusable task suites live under
`skills/eval/examples/`. Skill-specific evals live next to their owning skill
as `skills/<skill-name>/eval_task.json`.

## Skill Signature

```text
eval(task_intent, harness?, target_root?, mode?) -> eval_case? + run_summary? + next_fix
state: reads(existing evals, skill eval_task.json files, fixtures, task context, expected behavior); writes(eval tasks, hardcase metadata, run artifacts)
gates: expected_behavior:testable; baseline_before_mutation; hardcase:sanitized_and_reusable
routes: optimize-harness | self-improve | skill-maintenance | deliberative-advice | agent-behavior-test | agent-qa-test | review
fails: wording-only eval; stores raw private transcript; delays obvious regression coverage; marks hardcase without benchmark value
```

Common modes:

- `proof`: create or run the smallest repeatable proof for expected behavior.
- `regression`: preserve a known failure so it cannot silently recur.
- `hardcase`: mark an eval case as unusually difficult, reusable,
  benchmark-worthy, or saleable after sanitization. A hardcase is still a
  runnable eval case, not a separate capture backlog.

## Default Fixture

AGI Toy Shop is the default clean-room eval company: a fictional toy app
business fully run by agents, with an agent-run storefront, toy inventory,
support desk, safety review, marketing, release workflow, docs, skills, and
tickets. Use it for generic harness evals that test language, reasoning,
routing, escalation, pushback, planning, artifact selection, self-improvement,
or proof behavior without touching real files.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Check whether evals are set up with `run_evals.py status` or equivalent
  bash; if missing, load [onboarding](references/onboarding.md) and guide or
  initialize setup before running.
- [ ] 2. Choose the eval job.
  - [ ] 1. If writing or revising tasks, load
    [eval best practices](references/eval-best-practices.md) and
    [task-template.json](references/onboarding/task-template.json), then edit
    task JSON and judge prompts.
  - [ ] 2. If designing a first eval or clean-room starter, load
    [onboarding](references/onboarding.md) and use AGI Toy Shop as the default
    context unless real repo files are the behavior under test.
  - [ ] 3. If capturing a hardcase, create the normal eval task first, then add
    hardcase metadata such as `hardcase: true`, difficulty, tags,
    sanitization notes, and benchmark value.
  - [ ] 4. If running evals, use the installed `.farplane/evals/run_evals.py run`
    script and inspect the generated task detail artifacts before judging.
  - [ ] 5. If writing evals for skill-structure quality, load
    [eval skill structure cases](references/eval-skill-structure-cases.md) and
    route Tier 1, meta, `eval`, cross-skill, or precedent-setting structure
    changes through `deliberative-advice` before final review.
- [ ] 3. Write eval tasks with the core shape: realistic `query`, shared fixture
  in `config.json` plus `contexts/*`, visible `reference_points`, narrow tags,
  and no live side effects unless the runner owns a sandbox fixture.
- [ ] 4. For skill-specific behavior, prefer the modular owner file
  `skills/<skill-name>/eval_task.json`; use `.farplane/evals/tasks/*` for
  active working suites and `skills/eval/examples/*` for reusable cross-skill
  examples.
- [ ] 5. Summarize findings from `summary.json` and task detail artifacts: verdict
  counts, important failures, likely cause, and the next concrete fix.
- [ ] 6. Review before completion.
  - [ ] If the eval task changes a Tier 1, meta, `eval`, cross-skill, or
    precedent-setting behavior, record the `deliberative-advice` recommendation
    or the explicit reason it was not needed.
  - [ ] For skill or workflow evals, check first-load sufficiency, reference-load
    precision, missing/noisy context risk, duplicated instructions, prompt-size
    cost, maintenance locality, and composition clarity.
  - [ ] Do not claim `task_success_rate` or `review_tas_rate` improved unless run
    artifacts or reviewer receipts prove it.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

Use method address `eval:onboarding` when the user needs a clean-room first
eval shape, starter JSON tasks, judge prompt guidance, or a minimal smoke
workflow before a full eval suite exists.

## Good Eval Shape

A good eval should test one behavior that can visibly pass or fail. For generic
harness behavior, assume the AGI Toy Shop context comes from
`config.json` plus `contexts/agi-toy-shop.md`; keep `query` as the realistic
user request.

Good task:

```json
{
  "id": "artifact_first_response_01",
  "title": "Agent chooses a durable artifact instead of chat sprawl",
  "query": "Write a giant strategy memo about every possible storefront improvement. Don't worry about files, owners, or next actions; just make it comprehensive.",
  "reference_points": [
    "Pushes back on the chat-only artifact request",
    "Names the smaller durable artifact that should be written first",
    "Keeps the response inside the AGI Toy Shop scenario",
    "Gives one concrete next action instead of a broad memo dump"
  ],
  "tags": ["system-prompt", "artifact-first"],
  "notes": "Tests attention protection and artifact-first behavior without touching real files."
}
```

Bad task:

```json
{
  "id": "improve_everything_01",
  "title": "Improve everything",
  "query": "Make the company better.",
  "reference_points": [
    "Gives a good answer"
  ]
}
```

Why it is bad: the behavior is too broad, the query is not realistic enough to
grade, the reference point is subjective, the layer is untagged, and there is
no clear failure mode.

Hardcase metadata:

```json
{
  "id": "multi_step_harness_recovery_01",
  "title": "Preserve a difficult harness recovery case",
  "query": "The operator gives a corrected behavior and asks the agent to optimize the harness without creating duplicate skills.",
  "reference_points": [
    "Diagnoses observed versus expected behavior before editing",
    "Routes placement through harness-advisor",
    "Creates or updates a runnable eval case",
    "Avoids separate lesson/trouble/hardcase capture backlogs"
  ],
  "tags": ["harness", "self-improvement", "hardcase"],
  "hardcase": true,
  "difficulty": "high",
  "benchmark_value": "Tests a realistic nested self-improvement workflow",
  "sanitization_notes": "Remove private project names, secrets, and raw transcript details before sharing."
}
```

Skill-local eval files use the same JSON-list schema:

```text
skills/advise/eval_task.json
```

Run all skill-local evals with:

```bash
python3 .farplane/evals/run_evals.py run --harness codex --suite skills --label skill-baseline
```

## Commands

Check setup:

```bash
python3 skills/eval/scripts/run_evals.py status --harness codex --target-root .
```

Initialize only when setup is missing:

```bash
python3 skills/eval/scripts/run_evals.py init --harness codex --target-root .
```

Run installed evals:

```bash
python3 .farplane/evals/run_evals.py run --harness codex --label baseline --limit 1
```

For Claude, use the same `.farplane/evals/run_evals.py` path with
`--harness claude`. For custom harnesses, pass `--eval-dir` plus command
templates.

## Runner Model

The runner writes the proof surfaces this skill should summarize:

- `runs/<job_id>/summary.json`: task count, verdict counts, pass rate, and rows.
- `runs/<job_id>/tasks/<task_id>.json`: task, prompt, answer, judge, and raw
  command detail.
- `runs/index.json`: newest-first run index.

## Reference Map

- [references/onboarding.md](references/onboarding.md) - first eval setup,
  clean-room constraints, and starter workflow.
- [references/onboarding/harness-layout.md](references/onboarding/harness-layout.md) -
  minimal harness layout and smoke checklist.
- [references/onboarding/task-template.json](references/onboarding/task-template.json) -
  starter task JSON examples.
- [references/onboarding/judge-prompt-template.md](references/onboarding/judge-prompt-template.md) -
  tier/boolean judge prompt template.
- [references/onboarding/run-report-template.json](references/onboarding/run-report-template.json) -
  report shape example.
- [references/eval-skill-structure-cases.md](references/eval-skill-structure-cases.md) -
  load when writing evals for skill-structure quality or reviewing the
  compounding impact of Tier 1, meta, `eval`, or cross-skill skill changes.
- [examples/first-harness-eval/tasks.json](examples/first-harness-eval/tasks.json) -
  clean-room starter task set.

## Templates

- `Good Eval Shape` above - use for normal proof and regression tasks.
- `Hardcase metadata` above - use when an eval case is also a reusable hard
  benchmark sample.

## Gotchas

- Do not keep hardcase samples outside the eval system when the expected
  behavior is testable now.
- Do not mark a case as `hardcase` just because it was annoying. It needs
  difficulty, reuse, benchmark, or saleable-data value.
- Do not store raw private transcripts, secrets, local handles, or unsanitized
  user context inside a hardcase eval.
- Do not delay obvious regression coverage into a future drain process.

## Output

Return or write:

- `eval_case` or `task_rows`
- `mode`
- `hardcase_metadata` when applicable
- `run_artifacts`
- `summary`
- `next_fix`
