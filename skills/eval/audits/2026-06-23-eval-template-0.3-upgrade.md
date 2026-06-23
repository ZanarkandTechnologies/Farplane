---
skill: eval
date: 2026-06-23
change_type: structure
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/eval/SKILL.md
after_ref: skills/eval/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - skills/eval/SKILL.md
  - skills/eval/qa_checklist.md
  - docs/skills/registry.jsonl
eval_required: no
---

# Eval Template 0.3 Upgrade

## Change

- Before: `eval` used `skill_template_version: "0.2.0"`, carried long inline
  examples and command inventories in first load, and lacked explicit
  `0.3.0` phase contract and phase boundary sections.
- After: `eval` declares `skill_template_version: "0.3.0"`, advertises
  `qa_checklist.md`, exposes an eval budget, adds phase contract/boundary
  sections, and moves long task/profile/runner detail behind references.
- Why: `eval` is a core meta skill; it should be current with the latest
  template and stay compact enough to load before task context degrades.
- Tradeoff accepted: The first-load file now points to references for detailed
  examples and commands, so agents must follow branch load conditions for
  deeper authoring help.

## First-Principles Reasoning

- Objective: Keep the normal eval workflow executable from first load while
  reducing prompt weight and aligning with the latest skill template.
- Placement logic: Always-needed routing, gates, phase boundary, and finish
  rules stay in `SKILL.md`; detailed examples, setup commands, and surface maps
  stay in references.
- Expected behavior delta: An agent can bind eval inputs, select a proof
  surface, run or write the eval, inspect artifacts, route QA/review, and
  report next fixes without hidden chat context.
- Proof needed: line budget review, registry sync, eval runner tests,
  query-spoiler smoke lint, and skill-system validation.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` keeps context, signature, budget, phase contract, phase boundary, todos, gotchas, reference map, and output. |
| `reference_load_precision` | pass | Todo and Reference Map name when to load onboarding, best practices, surface ownership, QA checklist, consolidation, and self-improve refs. |
| `missing_context_rate` | pass | Required gates now include `query_not_spoiled` and `evidence_inspected_before_claim`; output contract remains in first load. |
| `noisy_context_rate` | pass | Long JSON examples, profile details, and command inventories moved out of first load. |
| `duplicated_instruction_count` | pass | First load points to `eval-best-practices.md` and `eval-surface-ownership.md` instead of duplicating their bodies. |
| `prompt_size_tokens` | pass | Observed `SKILL.md` length changed from 386 lines before this pass to 250 lines after. |
| `task_success_rate` | unknown | No full live Codex eval benchmark was run for this structure-only upgrade. |
| `review_tas_rate` | unknown | No independent reviewer receipt was available in this turn. |
| `maintenance_locality` | pass | Runtime QA lives in `skills/eval/qa_checklist.md`; template structure lives in `skills/eval/SKILL.md`; generated registry rows were regenerated. |
| `composition_clarity` | pass | Signature, `EvalBudget`, phase contract, and phase boundary clarify inputs, state, gates, routes, and handoffs. |

## Proof Artifacts

- Skill-local evals, when needed: not required for the structure-only template
  upgrade.
- Structure evals, when needed: not required beyond local unit and skill-system
  checks.
- Reviewer receipt: not available; self-check used because no reviewer tool was
  exposed in this turn.
- Validator:
  - `python3 -m unittest skills/eval/tests/test_run_evals.py skills/eval/tests/test_fetch_evals_edited_since_last_run.py`
  - `python3 skills/eval/scripts/check_eval_queries.py --root .`
  - `python3 skills/skill-maintenance/scripts/check_skills.py --write`
- Eval required: no.
- Evidence gaps: global `--template-version 0.3.0` report still fails on
  unrelated `budget-advisor` structure errors in the current dirty worktree.

## Before Behavior

- `eval` had useful behavior, but its first-load file carried detailed examples
  and command inventories that belonged in references.
- The skill had no explicit latest-template phase contract or phase boundary.
- The latest skill-system registry did not mark `eval` as `0.3.0`.

## After Behavior

- `eval` is discoverable as a `0.3.0` skill with `qa_checklist.md`.
- The first-load contract is shorter and more compositional.
- Detailed task writing, profile-backed runs, fixture placement, and runner
  ownership live behind explicit references.

## Remaining Opportunities

- Run one native profile-backed Codex skill eval for `eval` itself once the
  local Codex profile is finalized, so the new phase/profile guidance has live
  behavior evidence.
- Add or update a reviewer receipt for the structure change when the native
  reviewer lane is available.
- Decide whether `references/onboarding.md` and `README.md` duplicate enough
  setup material to consolidate later.
- Address unrelated `budget-advisor` template errors before using global
  `--require-template-version 0.3.0` as a clean rollout gate.
