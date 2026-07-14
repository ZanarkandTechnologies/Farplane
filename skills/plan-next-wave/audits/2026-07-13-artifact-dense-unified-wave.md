---
skill: plan-next-wave
date: 2026-07-13
change_type: behavior-and-identity
owner: skill-maintenance
status: implemented
before_ref: skills/ticket-opportunity-generator/SKILL.md
after_ref: skills/plan-next-wave/SKILL.md
review_route: reviewer
reasoning_basis: operator correction + TASK-0345 + focused evals + reviewer receipt
eval_required: yes - setup bundling, configured-area ranking, and artifact classification are durable planner behaviors
---

# Artifact-Dense Unified Wave Audit

## Before Behavior

- The callable was `plan_next_wave(...)`, but the package retained the
  historical `ticket-opportunity-generator` identity.
- Areas fed one global ranking, but the contract did not require an explicit
  candidate/no-candidate receipt for every objective-relevant area.
- Positive-output strings and proof receipts could pass the mechanical ticket
  validator even when the proposed ticket only created setup.

## After Behavior

- `plan-next-wave` is the canonical source and installed package; the retired
  rendered package name is pruned with backup and no compatibility alias.
- One planner considers each relevant area, then globally ranks all candidates;
  no content Pulse, area Pulse, planner fanout, quota, or controller exists.
- Avoidable setup is consolidated into at most one first-exemplar ticket.
- Ordinary specs carry structured `direct_value` artifacts with supported
  kinds, concrete refs, independent value, and direct use paths. Setup and
  proof/test receipts are classified separately and cannot pass alone.

## Proof Artifacts

- `tickets/archive/TASK-0345/artifacts/implementation-evidence.md`
- `.farplane/evals/runs/20260713-100000-task-0345-artifact-dense/summary.json`
- `.farplane/evals/runs/20260713-104254-task-0345-artifact-dense-rerun9/summary.json`
- `.farplane/evals/runs/20260713-104532-task-0345-proof-receipts-final/summary.json`
- `.farplane/evals/runs/20260713-105046-task-0345-guard-restoration-final/summary.json`
- `tickets/archive/TASK-0345/artifacts/eval-validation.md`
- `tickets/archive/TASK-0345/artifacts/review/completion-review.md`
- `tickets/archive/TASK-0345/artifacts/review/completion-review-accepted.md`
- `skills/plan-next-wave/scripts/test_validate_ticket_specs.py`
- `skills/skill-maintenance/scripts/test_install_selected_skills.py`

## Binary Structure Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Trigger, exact response schema, area/global ranking, setup bundling, direct-value artifact contract, authority, and proof gates remain first-load requirements. |
| `reference_load_precision` | pass | Conditional detail remains in QA, reviewer handoff, scripts, and audits; the first-load file links each owner. |
| `missing_context_rate` | pass | The rerun fixture supplies exact configured Farplane areas, objective metrics, guard, and operator availability instead of inheriting AGI Toy Shop assumptions. |
| `noisy_context_rate` | pass with tradeoff | The first-load contract is long because every admission decision needs the ordered response, hard gates, ticket schema, and wave-shape constraints; rare historical rationale remains in audits/docs. |
| `duplicated_instruction_count` | pass | SKILL owns runtime behavior, QA restates review gates, validator enforces structured fields, and evals pressure failure cases; these are distinct execution surfaces. |
| `prompt_size_tokens` | unknown mechanical | File length is tracked during review; no token counter is treated as a quality score. |
| `task_success_rate` | pass | Final grounded flagship rerun is TAS-A and its six admitted specs pass the real mechanical materialization validator. |
| `review_tas_rate` | pass | Final independent completion review returned TAS-A after ordinary artifact and exclusive guard-restoration repairs. |
| `maintenance_locality` | pass | Primary behavior stays in one skill package; project objective and Pulse docs are secondary sync points only. |
| `composition_clarity` | pass | `plan-next-wave` is pure; Pulse alone materializes/dispatches; capability skills own domain production. |

## Verification Commands

```text
python3 -m unittest bin.tests.test_farplane_ticket_history skills/plan-next-wave/scripts/test_validate_ticket_specs.py
python3 skills/eval/scripts/check_eval_queries.py --root .
python3 skills/skill-maintenance/scripts/check_skills.py --write
python3 bin/validators/check_farplane_project_files.py --root .
python3 bin/validators/check_doc_refs.py
```

## Follow-Ups

- Inspect the next real scheduled low-watermark refill for area receipts,
  setup-bearing count, direct-value artifact records, and no controller drift.
- Keep publishing human-gated while allowing unattended production of local
  reviewable artifacts.
