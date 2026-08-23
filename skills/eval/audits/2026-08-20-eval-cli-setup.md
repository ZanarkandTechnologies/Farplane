---
title: Farplane Eval CLI setup
owner: skills/eval
status: complete
kind: change-receipt
created_at: 2026-08-20
feature_ref: FEAT-0039
---

# Farplane Eval CLI Setup

## Objective

Make the existing Promptfoo skill-comparison adapter discoverable and runnable
as a stable `farplane` command without creating a second runner or authored
eval format.

## Delta

- `farplane eval init` writes the non-secret local provider profile at
  `.farplane/evals/promptfoo-profile.json`; it never writes credentials.
- `farplane eval promptfoo --skill <name> --label <label>` resolves the owning
  Agent Skills manifest and delegates unchanged to `run_promptfoo.py`.
- The wrapper defaults receipts to `.farplane/evals/runs`, the artifact root
  consumed by Farplane Office. An explicit manifest, variant skills, selected
  eval IDs, alternate profile, and package versions remain available.

## Boundaries

- Promptfoo continues to execute, detect skill use, and grade.
- `run_promptfoo.py` continues to isolate workspaces and normalize Office
  artifacts.
- This command does not run a model during `init` or `--dry-run`, install a
  dependency, store credentials, mutate a skill, or replace project/trace evals.

## Proof

- `farplane eval init` wrote the project-local profile.
- `farplane eval promptfoo --skill eval --eval-id
  eval_skill_modular_task_authoring_01 --label promptfoo-cli-smoke --dry-run`
  wrote `.farplane/evals/runs/20260819T221113Z-promptfoo-cli-smoke/summary.json`.
- `python3 -m unittest bin.tests.test_farplane_eval_cli
  bin.tests.test_farplane_cli_parser skills.eval.tests.test_run_promptfoo`
  passed: 18 tests.
- `python3 bin/validators/check_doc_refs.py` passed.

## Independent Review

Passed. The reviewer confirmed the command delegates to the owner-local
adapter, keeps credentials out of the generated profile, resolves project-local
paths, preserves child exit codes, and targets the Office-readable runs root.

## Review Contract

- Review focus: delegation preserves adapter ownership, profile has no secret
  field, project-relative paths resolve correctly, and child exit codes reach
  the caller unchanged.
- Rubrics: `code-quality`, `integration-readiness`.
- Hard gates: no duplicate runner, no source mutation in dry run, no provider
  credential persistence, and Office-readable artifact path.
