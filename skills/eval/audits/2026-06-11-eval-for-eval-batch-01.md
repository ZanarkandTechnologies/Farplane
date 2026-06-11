---
title: Eval For Eval Batch 01 Review
owner: skills/eval
status: human-feedback-review
updated: 2026-06-11
review_route: internal
proof_artifacts:
  - skills/eval/self-improve/program.md
  - skills/eval/eval_task.json
  - .farplane/evals/runs/20260611-052148-eval-skill-smoke/summary.json
eval_required: true
---

# Eval For Eval Batch 01 Review

## Goal

Create the first representative eval batch for the `eval` skill so future
changes to eval authoring can be tested against concrete clean-room behavior.
The ongoing idea/test/feedback loop is tracked in
[`../self-improve/program.md`](../self-improve/program.md).

```text
eval_for_eval_batch(eval_skill, agi_toy_shop_fixture, review_metrics)
  -> skill_local_eval_task_json + review_note + human_feedback_request
```

## Candidate Tasks

| Task | Behavior Under Test | Review |
| --- | --- | --- |
| `eval_skill_modular_task_authoring_01` | Skill-specific evals go in the owning skill's `eval_task.json`. | Keep. This is the baseline modularity case. |
| `eval_skill_bad_task_rejection_01` | Vague eval prompts are rejected or rewritten into visible behavior. | Keep. This catches the most likely quality failure. |
| `eval_skill_best_practices_branching_01` | Run-only eval work does not load authoring best practices unnecessarily. | Keep, but verify with a real run later because reference loading is partly behavioral. |
| `eval_skill_structure_metric_01` | Skill structure uses first-load and prompt-size tradeoffs instead of one absolute rule. | Keep as the first structure-quality case. |

## Structure Review

| Metric | Result | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | The eval skill already states the owner-local eval path and default AGI Toy Shop fixture in `SKILL.md`. |
| `reference_load_precision` | pass | One task specifically checks run-only work avoids loading authoring-only best practices. |
| `missing_context_rate` | pass | The task queries avoid repeating AGI Toy Shop background and rely on `config.json` plus `contexts/agi-toy-shop.md`. |
| `noisy_context_rate` | pass | Each task tests one behavior rather than bundling every eval standard into one mega-case. |
| `duplicated_instruction_count` | pass | The task file points at behaviors; detailed rubric policy stays in references and judge prompt. |
| `prompt_size_tokens` | pass | The batch adds four compact tasks, not long embedded examples or full standards. |
| `task_success_rate` | unknown | Needs real harness runs before making success claims. |
| `review_tas_rate` | unknown | Needs reviewer or human judgment after this checkpoint. |
| `maintenance_locality` | pass | The tasks live in `skills/eval/eval_task.json`, beside the skill they test. |
| `composition_clarity` | pass | The batch separates authoring, running, bad-task rejection, and structure placement behaviors. |

## Before Behavior

- The eval skill had one modular-authoring eval task but did not yet cover
  vague task rejection, best-practice load precision, or SKILL.md/reference
  placement tradeoffs.

## After Behavior

- `skills/eval/eval_task.json` now has a four-task batch that can be run as
  part of the `skills` suite and reviewed by Kenji before rollout.

## Validation

- `python3 -m json.tool skills/eval/eval_task.json`
- `python3 skills/eval/scripts/run_evals.py status --harness codex --target-root .`
- `python3 skills/skill-maintenance/scripts/check_skills.py --write`
- `python3 .farplane/evals/run_evals.py run --harness custom --judge-harness custom --eval-dir .farplane/evals --target-root . --suite skills --label eval-skill-smoke --limit 4 ...`

Smoke result:

- Summary:
  `.farplane/evals/runs/20260611-052148-eval-skill-smoke/summary.json`
- Task count: `4`
- Verdict counts: `{"A": 4}`
- Note: this proves task loading, fixture plumbing, artifact writing, and judge
  JSON parsing only. It does not prove real agent task success.

## Human Feedback Question

Should this become the standard seed pattern for eval-skill evals?

Review specifically:

- Are these task queries realistic enough?
- Are the reference points visible enough to judge?
- Is four tasks the right first batch, or should batch 01 be smaller?
- Should the structure-placement case live in `skills/eval/eval_task.json`, or
  should it move to a cross-skill suite later?

## Next Iteration

After feedback, either tighten these four tasks or split the next batch into:

- one eval for judge-prompt quality;
- one eval for AGI Toy Shop context override behavior;
- one eval for deciding when a deterministic validator is better than an eval.
