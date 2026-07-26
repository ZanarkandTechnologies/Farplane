---
ticket_id: TASK-0413
kind: validation-receipt
status: pass
created_at: 2026-07-26T21:32:00+08:00
---

# Validation Receipt

## Deterministic Checks

- `python3 skills/skill-maintenance/scripts/check_skills.py --write` — pass:
  123 skill rows, surface budgets, template usage, configs, eval lint, method
  references, and 1,995 documentation refs.
- `python3 -m unittest test_check_skills.py
  test_validate_skill_configs.py test_install_selected_skills.py` from the
  owning scripts directory — 28/28 pass.
- `python3 -m unittest bin.tests.test_runtime_state
  bin.tests.test_farplane_invocation` — 35/35 pass.
- `python3 bin/farplane.py validate ticket tickets/TASK-0413/ticket.md --phase
  planning` — pass.
- `python3 skills/impl-plan/scripts/validate_visual_companion.py
  tickets/TASK-0413/ticket.md` — pass.
- Focused compiler assertions — pass for template version, QA/demo/review
  ordering, no ticket flag, direct-route exclusion, MP4-only output, and
  validator-compatible `result.json`.
- Installed source copies of `demo` and `goal-advisor` refreshed under the
  Codex home using `install_selected_skills.py`.

## Behavior Evals

- Demo happy path and failed-QA blocker:
  `.farplane/evals/runs/20260726-132928-task-0413-demo-recap-final-v2/`
  — both TAS-A.
- Demo PPTX/generated-visual rejection and unauthorized-spend blocker:
  `.farplane/evals/runs/20260726-133122-task-0413-demo-recap-final-two/`
  — both TAS-A.
- Goal compiler final checkpoint:
  `.farplane/evals/runs/20260726-132937-task-0413-goal-demo-compiler-v3/`
  — TAS-A.

Final candidate coverage is 4/4 TAS-A for `demo` and 1/1 TAS-A for the Goal
compiler checkpoint.

## Baseline Note

The paired native-discovery run at
`.farplane/evals/runs/20260726-131949-task-0413-demo-recap-candidate/` was
inconclusive because the candidate was not yet installed and only one task
triggered. Later paired runs still showed inconsistent trigger telemetry, so no
candidate-over-baseline rate is claimed. The accepted behavior claim rests on
owner-skill-injected candidate evals plus deterministic validation and
independent review.
