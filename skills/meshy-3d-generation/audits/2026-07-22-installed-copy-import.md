---
skill: meshy-3d-generation
date: 2026-07-22
change_type: maintenance
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: /Users/kenjipcx/.codex/skills/meshy-3d-generation
after_ref: skills/meshy-3d-generation
reasoning_basis: first_principles
proof_artifacts: []
eval_required: no
---

# Installed-Copy Import

## Change

- Before: the installed Meshy skill existed only under `.codex`.
- After: Farplane contains the full external package plus normalized discovery
  metadata; reinstall can now derive the live copy from repo source.
- Why: repo source must stay ahead of installed harness state.
- Tradeoff accepted: imported external instructions remain vendor-owned and
  are not rewritten as Farplane policy in this drift-recovery pass.

## First-Principles Reasoning

- Objective: remove installed-only reusable harness state.
- Placement logic: keep the package under `skills/` with `source: external` and
  an explicit upstream URL.
- Expected behavior delta: none; source ownership and reinstallability change.
- Proof needed: registry validation, reinstall, and byte comparison.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Imported package preserves the installed first-load body. |
| `reference_load_precision` | pass | Endpoint detail remains in the imported `reference.md`. |
| `missing_context_rate` | unknown | No behavior eval was run for a mechanical import. |
| `noisy_context_rate` | unknown | Vendor body is intentionally preserved. |
| `duplicated_instruction_count` | pass | One canonical repo package now owns reinstall state. |
| `prompt_size_tokens` | unknown | Vendor package is intentionally unchanged. |
| `task_success_rate` | unknown | `eval_skip_reason`: no behavior delta. |
| `review_tas_rate` | pass | TASK-0401 final review returned TAS-A. |
| `maintenance_locality` | pass | Only the missing package and metadata were imported. |
| `composition_clarity` | pass | Package remains an external Tier-3 domain skill. |

## Proof Artifacts

- Skill-local evals: skipped; mechanical import only.
- Structure evals: `check_skills.py --write` passed with 124 skill rows.
- Reviewer receipt: `tickets/TASK-0401/artifacts/review/final-review.md`.
- Validator: registry, installed-copy diff, installer tests, and doctor passed.
- Eval required: no.
- Evidence gaps: vendor behavior was not re-evaluated because the import was mechanical.

## Before Behavior

- `.codex` contained an installed-only reusable skill.

## After Behavior

- Farplane is the reinstallable owner while preserving external provenance.

## Followups

- Review or adapt vendor behavior only under a separate behavior-change ticket.
