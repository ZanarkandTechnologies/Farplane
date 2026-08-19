---
skill: feed-scout
date: 2026-08-19
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: skills/feed-scout/SKILL.md@pre-TASK-0441
after_ref: skills/feed-scout/SKILL.md
reasoning_basis: reviewer
proof_artifacts:
  - skills/feed-scout/scripts/test_validate_scout_brief.py
  - skills/plan-next-wave/scripts/test_eval_fixtures.py
  - bin/tests/test_farplane_project_snapshot.py
eval_required: no
---

# Scout Brief Migration Audit

## Change

- Before: Feed Scout exposed a separate World Memory product name, config key,
  artifact kind, path, validator, receipt, and planner payload.
- After: Scout Brief owns that bounded sidecar end to end through
  `scout_brief`, `feed-scout-brief`, `source_facts`, and the renamed files.
- Why: Wiki must remain the sole knowledge-system term while Feed Scout keeps
  its compact, non-authoritative planning context.
- Tradeoff accepted: Existing projects must rename the old config and ignored
  sidecar directly; there is no runtime alias or fallback.

## First-Principles Reasoning

- Objective: Remove competing knowledge vocabulary without collapsing source
  planning context into canonical Wiki articles.
- Placement logic: Rename the existing owner and consumers; add no new state or
  service.
- Expected behavior delta: Feed Scout writes one Scout Brief, Pulse loads it
  once, and tickets copy selected `source_facts` rather than sidecar pointers.
- Proof needed: Renamed validator, fixture, planner/Pulse transport, snapshot,
  config rejection, live-file validation, and active terminology sweep.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Feed Scout names the new path, validator, receipt, and handoff. |
| `reference_load_precision` | pass | Workflow and data-model references route only conditional detail. |
| `missing_context_rate` | pass | Planner, Pulse, automation, and project snapshot consumers were migrated. |
| `noisy_context_rate` | pass | The migration adds no new workflow prose. |
| `duplicated_instruction_count` | pass | Scout Brief remains one Feed Scout-owned sidecar. |
| `prompt_size_tokens` | pass | Mechanical terminology delta only. |
| `task_success_rate` | pass | Focused suites and live validator pass. |
| `review_tas_rate` | unknown | Parent completion review pending. |
| `maintenance_locality` | pass | Validator/template/tests remain inside `skills/feed-scout/`. |
| `composition_clarity` | pass | `scout_brief_ref -> scout_brief_update_receipt` is explicit. |

## Proof Artifacts

- Skill-local evals: mechanical rename; existing cases were renamed in place.
- Structure evals: not required.
- Reviewer receipt: pending TASK-0441 completion review.
- Validator: 70 focused unittest cases, live Scout Brief validation, structured
  config parses, binding rejection cases, Python compilation, and diff checks.
- Eval required: no; the sidecar behavior is unchanged and deterministic tests
  cover the renamed contract.
- Evidence gaps: generated registries await the parent-owned regeneration pass.

## Before Behavior

- The same sidecar leaked a second operator-facing knowledge product name.

## After Behavior

- Wiki is canonical knowledge; Scout Brief is explicitly bounded source context.

## Followups

- Parent regenerates feature/system/skill registries and runs the ticket-level
  terminology sweep and independent completion review.
