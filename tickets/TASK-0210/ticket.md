---
ticket_id: TASK-0210
title: Normalize eval scope selection
phase: verifying
status: review
owner: codex
priority: medium
ready: true
approval_required: false
requires_qa: true
requires_demo: false
next_action: review and merge scope-selection migration
last_verification: 2026-06-23 unit tests, query lint, skill checks, and no-suite active-surface grep passed
---

# TASK-0210: Normalize Eval Scope Selection

## Summary
The eval runner currently mixes harness/system-prompt examples and exposes
`--suite skills` as the way to reach skill-local evals. Normalize selection
around eval families: harness evals, AGENTS.md evals, and skill evals. Keep
task JSON simple and make file location plus CLI flags define scope.

## Scope
- In:
  - Add `--harness-evals`, `--agents-md`, `--skills`, and `--skill`.
  - Make no-scope `run` execute all known eval families.
  - Add `.farplane/evals/tasks/agents_md_tasks.json` through the eval template.
  - Update docs and tests.
- Out:
  - No new task JSON metadata fields.
  - No eval budget system.
  - No batching/subagent orchestration.
  - No change to judge prompt schema.

## Delta
- `Before:` default run only used `harness_tasks.json`; AGENTS.md evals were
  mixed into harness/example files; selected skill evals still carried old
  `--suite skills` terminology in docs.
- `After:` no-scope run covers all known eval families; scope flags narrow the
  run; `--skill qa` is enough for selected skill evals; AGENTS.md evals live in
  their own task file.
- `Why now:` the eval API should match the actual mental model before more eval
  rows are added.
- `First-principles basis:`
  - `objective:` make eval execution obvious and hard to misuse.
  - `need:` avoid duplicating eval type metadata in every task row.
  - `assumptions:` file path is the canonical family signal.
  - `root_cause:` runner exposes internal suite naming instead of user-facing scope.
  - `constraints:` keep existing task schema and generated artifacts stable.
  - `first_viable_slice:` runner flags, AGENTS.md task file, docs, tests.
  - `proof_or_falsification:` tests prove default all-scope, selected scopes,
    and selected skill.
  - `tradeoff:` remove the old `--suite` interface instead of preserving a
    hidden compatibility path.
  - `non_goals:` no budget model, no new eval orchestration runtime.

## Program
```text
signature:
  normalize_eval_scopes(runner_args, eval_files) -> task_paths + run_summary + docs_delta

program:
  inventory_current_tasks()
    -> harness_tasks + system_prompt_candidates + skill_eval_files

  add_scope_resolution()
    -> all_scope_default + explicit_scope_flags + selected_skill_filter

  migrate_agents_md_tasks()
    -> .farplane/evals/tasks/agents_md_tasks.json

  update_docs_and_templates()
    -> examples use --skills / --skill / --agents-md / --harness-evals

  verify()
    -> unit_tests + query_lint + skill_checks
```

## Map
- `Touch:`
  - `skills/eval/scripts/run_evals.py`
  - `skills/eval/tests/test_run_evals.py`
  - `skills/eval/templates/agents_md_tasks.json`
  - eval docs/templates that mention `--suite skills`
- `Inspect:`
  - `.farplane/evals/tasks/harness_tasks.json`
  - `skills/eval/examples/farplane-global-harness/tasks.json`
- `Signature delta:`
  - `resolve_task_paths(eval_dir, tasks, scopes, target_root): list[Path]`
  - `selected_scopes(args): set[str]`
  - `command_run(args): summary["scopes"] + task_files`
- `Type Sketch:`
  - `Scope = "harness" | "agents-md" | "skills"`
  - `task JSON = existing fields only`
- `Typed flow example:`
  - `run --skill qa` -> scopes `{skills}` -> `skills/qa/eval_task.json`
  - `run` -> scopes `{harness, agents-md, skills}` -> all available task files

## Done / Proof
```text
done_when:
  - no-scope run selects harness, agents-md, and skills task files when present
  - --harness-evals selects only harness_tasks.json
  - --agents-md selects only agents_md_tasks.json
  - --skills selects all skill-local eval_task.json files
  - --skill qa selects only skills/qa/eval_task.json
  - task JSON schema remains unchanged

proof:
  checks:
    - python3 -m unittest skills/eval/tests/test_run_evals.py
    - python3 skills/eval/scripts/check_eval_queries.py --root .
    - python3 skills/skill-maintenance/scripts/check_skills.py --write
  manual:
    - grep docs for stale "--suite skills --skill" examples
    - inspect run summary fields for scopes/task_files clarity
  review:
    - rubric: eval-quality
      required_tas: TAS-B or better
  evidence:
    - unit test output
    - relevant doc diff
```

## State
- `next_action:` review and merge scope-selection migration
- `blocked:` no
- `latest_verification:` `python3 -m unittest skills/eval/tests/test_run_evals.py`; `python3 skills/eval/scripts/check_eval_queries.py --root .`; `python3 skills/skill-maintenance/scripts/check_skills.py --write`; active eval-surface grep for `--suite`/summary suite references
- `result:` runner scope flags, AGENTS.md task file, docs, tests, viewer summary display, and local eval sidecar sync implemented with no compatibility bridge
