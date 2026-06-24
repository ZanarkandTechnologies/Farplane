---
name: eval
description: "Turn agent, prompt, or skill behavior into local eval tasks, boolean or tier judges, run artifacts, and verdicts."
tier: 3
group: harness
source: local
workflow: true
template_uses:
  skill-template: "0.3.0"
  skill-eval-task: "0.1.0"
  skill-qa-checklist: "0.1.0"
eval: eval_task.json
qa_checklist: qa_checklist.md
skill_ui: skills/eval/templates/viewer-react
methods:
  - eval:onboarding
  - eval:consolidate
allowed-tools: Read, Glob, Grep, Bash

---

# Eval

## Context

Use this skill when the user wants to run, create, repair, or consolidate a
real eval for an agent harness, prompt, skill, or workflow. It is intentionally
harness-native: project working evals live under `.farplane/evals` for Codex or
Claude runs. Repo-owned reusable task suites live under `skills/eval/examples/`.
Skill-specific evals live next to their owning skill as
`skills/<skill-name>/eval_task.json`.

AGI Toy Shop is the default clean-room fixture for generic harness evals. Extend
that fixture for new toy-company needs instead of inventing new fictional
companies unless a real repo fixture is required.

## Skill Signature

```text
eval(task_intent, harness?, target_root?, mode?, budget?) -> eval_case? + run_summary? + consolidation_report? + next_fix
state: reads(existing evals, skill eval_task.json files, qa_checklist?, fixtures, task context, expected behavior, eval-drain processed state); writes(eval tasks, hardcase metadata, run artifacts, consolidation reports, processed state)
gates: expected_behavior:testable; baseline_before_mutation; query_not_spoiled; hardcase:sanitized_and_reusable; evidence_inspected_before_claim
routes: optimize-harness | self-improve | skill-maintenance | deliberative-advice | agent-behavior-test | agent-qa-test | review
fails: wording-only eval; query_teaches_answer; stores raw private transcript; delays obvious regression coverage; marks hardcase without benchmark value
```

```text
EvalBudget = {
  grounding?: "skim" | "targeted" | "deep",
  harness_realism?: "static" | "custom-command" | "native-codex-profile",
  suite_scope?: "one-task" | "selected-skills" | "full-suite",
  finish_gate?: "self-check" | "checklist" | "eval-run" | "review"
}
```

When required inputs are missing, resolve them from local eval setup, skill
files, task artifacts, or one narrow blocking question. Do not invent the
behavior under test or silently choose live side effects.

Common modes:

- `proof`: create or run the smallest repeatable proof for expected behavior.
- `regression`: preserve a known failure so it cannot silently recur.
- `hardcase`: mark an eval case as unusually difficult, reusable,
  benchmark-worthy, or saleable after sanitization. A hardcase is still a
  runnable eval case, not a separate capture backlog.
- `consolidate`: run the eval drain. Fetch skill eval files edited since the
  last drain, spawn one bounded `consolidate_eval` lane per changed file, and
  apply only changes that make evals less noisy without losing distinct
  coverage.

Use [eval surface ownership](references/eval-surface-ownership.md) when the
question is where to put fixture state, profile config, task rows, judge rules,
runner behavior, validators, or harness-advisor placement.

## Phase Contract

```text
eval_phase_contract(task, bound_inputs, state)
  -> grounded_eval_target
   + proof_surface_choice
   + eval_or_revision
   + run_or_static_check
   + artifact_inspection
   + qa_or_review_when_material
   + summary_and_next_fix
```

Use Codex native planning and execution phases inline by default. Externalize a
phase only when it produces a smaller artifact, independent judgment, or proof
surface.

## Phase Boundary

Call `review` when eval design, prompt changes, meta-skill changes, or
completion claims need independent judgment. Call `skill-maintenance` when
eval reference points should become reusable runtime guardrails in
`qa_checklist.md`. Call `agent-behavior-test` or `agent-qa-test` when the
behavior of another agent, prompt, skill, or workflow is the subject under
test.

Do not call `eval` recursively for the same eval-design task. Split the child
scope to a narrower target such as one task row, one judge prompt, or one
changed skill file.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Check whether evals are set up with `run_evals.py status` or equivalent
  bash; if missing, load [onboarding](references/onboarding.md) and guide or
  initialize setup before running.
- [ ] 2. Choose the eval job.
  - [ ] 1. If writing or revising tasks, load
    [eval best practices](references/eval-best-practices.md) and
    [task-template.json](references/onboarding/task-template.json), use
    [eval writing rubric](references/eval-writing-rubric.md) for quality
    review, then edit task JSON and judge prompts.
  - [ ] 2. If designing a first eval or clean-room starter, load
    [onboarding](references/onboarding.md) and
    [eval surface ownership](references/eval-surface-ownership.md); use AGI Toy
    Shop as the default context unless real repo files are the behavior under
    test.
  - [ ] 3. If capturing a hardcase, create the normal eval task first, then add
    hardcase metadata such as `hardcase: true`, difficulty, tags,
    sanitization notes, and benchmark value.
  - [ ] 4. If running evals, use the installed `.farplane/evals/run_evals.py run`
    script and inspect the generated task detail artifacts before judging.
  - [ ] 5. If writing evals for skill-structure quality, load
    [eval skill structure cases](references/eval-skill-structure-cases.md) and
    route Tier 1, meta, `eval`, cross-skill, or precedent-setting structure
    changes through `deliberative-advice` before final review.
  - [ ] 6. If improving how the `eval` skill writes evals across iterations,
    load [self-improve program](self-improve/program.md) and log ideas, tests,
    Kenji feedback, and accepted lessons there.
  - [ ] 7. If consolidating evals, load
    [eval consolidation](references/eval-consolidation.md), run
    `fetch_evals_edited_since_last_run`, and hand each changed eval file to a
    bounded `consolidate_eval` subagent or equivalent isolated review lane.
- [ ] 3. Write eval tasks with the core shape: realistic `query`, shared fixture
  in `config.json` plus `contexts/*`, visible `reference_points`, narrow tags,
  and no live side effects unless the runner owns a sandbox fixture.
  - [ ] Do not put the target skill's expected answer, routing policy, or
    business logic into the user `query`. For skill-local evals, keep the query
    natural and rely on the runner-provided owner `SKILL.md` context plus
    reference points to judge behavior.
  - [ ] Run query-spoiler QA after editing skill-local evals.
    - [ ] Use `python3 skills/eval/scripts/check_eval_queries.py --root .` as
      a fast smoke check for obvious leaks.
    - [ ] For new, material, high-risk, or proof-acceptance eval rows, run the
      skill-local [eval QA checklist](qa_checklist.md) with a reviewer, QA
      lane, or separate LLM judgment turn.
    - [ ] Treat checklist failures as eval-design failures: rewrite the query
      or harden the skill/fixture/reference points instead of teaching the
      answer in the query.
  - [ ] For Codex harness runs that need realistic agent defaults, use a Codex
    config profile with `--agent-profile` and, when useful, `--judge-profile`.
    Profile-backed Codex runs use native skill discovery instead of injected
    `SKILL.md` context.
  - [ ] Keep AGI Toy Shop as the shared fixture for generic harness examples;
    add new AGI Toy Shop tickets, roles, workflows, or product facts rather
    than creating new fictional companies.
- [ ] 4. For skill-specific behavior, prefer the modular owner file
  `skills/<skill-name>/eval_task.json`; use `.farplane/evals/tasks/*` for
  active working suites and `skills/eval/examples/*` for reusable cross-skill
  examples.
- [ ] 5. When skill eval `reference_points` become reusable runtime guardrails,
  route writeback through `skill-maintenance` to update the owning skill's
  checklist reference, final QA checklist, or validator/hook candidate.
- [ ] 6. For eval drain work, keep immediate lesson/trouble-derived evals in
  `eval_task.json`; the drain may merge, rewrite, or archive already-landed rows
  only when the consolidation report preserves every distinct failure mode.
- [ ] 7. Summarize findings from `summary.json`, task detail artifacts, or eval
  drain reports: verdict counts or changed files, important failures or coverage
  risks, likely cause, and the next concrete fix.
- [ ] 8. Review before completion.
  - [ ] If the eval task changes a Tier 1, meta, `eval`, cross-skill, or
    precedent-setting behavior, record the `deliberative-advice` recommendation
    or the explicit reason it was not needed.
  - [ ] For skill or workflow evals, check first-load sufficiency, reference-load
    precision, missing/noisy context risk, duplicated instructions, prompt-size
    cost, maintenance locality, and composition clarity.
  - [ ] Do not claim `task_success_rate` or `review_tas_rate` improved unless run
    artifacts or reviewer receipts prove it.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

Use `eval:onboarding` for clean-room first eval setup, starter tasks, judge
prompt guidance, or a minimal smoke workflow.

Use `eval:consolidate` for the weekly eval drain: fetch changed eval files,
dispatch one `consolidate_eval` lane per file, and reduce noise without
delaying fresh regression coverage.

## Templates

- Use [references/eval-best-practices.md](references/eval-best-practices.md)
  for good task shape, bad task rejection, judge design, and harness realism.
- Use [references/eval-surface-ownership.md](references/eval-surface-ownership.md)
  for profile-backed skill evals, fixture placement, runner ownership, and
  task-surface decisions.
- Use `eval_task.json` at the skill package root for focused behavioral evals.
- Use `qa_checklist.md` for settled reusable eval-row QA guardrails.
- Use `audits/YYYY-MM-DD-<short-change>.md` for material eval-skill changes.

## Reference Map

- [references/onboarding.md](references/onboarding.md) - first eval setup,
  clean-room constraints, and starter workflow.
- [references/eval-skill-structure-cases.md](references/eval-skill-structure-cases.md) -
  load when writing evals for skill-structure quality or reviewing the
  compounding impact of Tier 1, meta, `eval`, or cross-skill skill changes.
- [references/eval-writing-rubric.md](references/eval-writing-rubric.md) -
  load when judging eval-task quality, batch ROI, owner locality, breadth/depth,
  and skill-local versus workflow-level placement.
- [references/eval-surface-ownership.md](references/eval-surface-ownership.md) -
  load when deciding whether to change a Codex profile, AGI Toy Shop fixture,
  eval task, judge prompt, runner, validator, or harness-advisor route.
- [qa_checklist.md](qa_checklist.md) - load when reviewing whether
  skill-local eval queries leak skill invocation, policy, expected answer, or
  reference-point logic.
- [references/eval-consolidation.md](references/eval-consolidation.md) - load
  when running the weekly eval drain, writing the automation prompt, or
  dispatching per-file `consolidate_eval` lanes.
- [references/automation-prompt.md](references/automation-prompt.md) - use when
  installing or updating a weekly automation that invokes eval consolidation.
- [self-improve/program.md](self-improve/program.md) - Goal-backed
  human-feedback memory for improving eval-writing patterns.

## Gotchas

- Do not keep hardcase samples outside the eval system when the expected
  behavior is testable now.
- Do not treat `check_eval_queries.py` as a complete anti-cheat oracle. It is a
  cheap smoke check for obvious phrases; use the skill-local eval QA checklist
  with a separate reviewer, QA lane, or LLM judgment turn for material eval
  changes.
- Do not "fix" a failing skill eval by adding the answer to the query. If the
  generic query fails with the owning `SKILL.md` in context, harden the skill,
  checklist, fixture, reference points, or runner context instead.
- Do not mark a case as `hardcase` just because it was annoying. It needs
  difficulty, reuse, benchmark, or saleable-data value.
- Do not store raw private transcripts, secrets, local handles, or unsanitized
  user context inside a hardcase eval.
- Do not delay obvious regression coverage into a future drain process.
- Do not consolidate evals by count alone. Preserve hardcases and distinct
  failure modes unless a stronger replacement explicitly covers them.

## Output

- `eval_case` or `task_rows`
- `mode`
- `hardcase_metadata` when applicable
- `run_artifacts`
- `consolidation_report` and `processed_state_delta` when applicable
- `summary`
- `next_fix`
