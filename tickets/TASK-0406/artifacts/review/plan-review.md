---
kind: review
review_focus: planning
context_ref: tickets/TASK-0406/ticket.md
created_at: 2026-07-24T00:00:00+08:00
reviewer: native-reviewer
verdict: pass
overall_tas: TAS-A
---

# TASK-0406 Plan Review

## Review Summary

- `work_type`: material implementation plan
- `search_scope`:
  - `tickets/TASK-0406/ticket.md`
  - `tickets/TASK-0406/diagrams.md`
  - previous receipt: `tickets/TASK-0406/artifacts/review/plan-review.md`
  - overlap context: `tickets/TASK-0405/ticket.md`, `tickets/TASK-0405/progress.md`
  - review contract: `skills/review/SKILL.md`, `docs/review/rubrics/review-rubric-index.md`, `docs/review/rubrics/implementation-plan.md`, `docs/review/rubrics/spec-contract.md`, `docs/review/rubrics/integration-readiness.md`, `docs/review/rubrics/evidence-quality.md`, `docs/review/rubrics/debloatability.md`, `docs/review/rubrics/desloppify.md`
  - neighboring surfaces checked for the repaired gates: `bin/core/farplane_ticket_reward.py`, `skills/plan-next-wave/references/skill-call-contract.md`, `skills/plan-next-wave/scripts/validate_wave_response.py`, `skills/pulse-update/scripts/materialize_skill_call.py`, `skills/pulse-update/scripts/list_pulse_board.py`, `skills/interval-update/SKILL.md`, `skills/interval-update/templates/interval-report.md`, `skills/interval-update/qa_checklist.md`, `skills/interval-update/scripts/highlight_ledger.py`, `skills/interval-update/scripts/test_highlight_ledger.py`, `bin/core/farplane_project_snapshot.py`, `bin/tests/test_farplane_project_snapshot.py`
- `rubrics_used`: `spec-contract`, `implementation-plan`, `integration-readiness`, `evidence-quality`, `debloatability`; `desloppify` used as the cross-cutting search playbook.
- `overall_tas`: `TAS-A`
- `verdict`: `pass`
- `rerun_required`: no for planning approval; yes after implementation for QA/evidence/completion gates named by the ticket.
- `hard_gate_failures`: none.
- `finding_log`: no blocking findings.
- `blocking_findings`: none.
- `next_action`: approve the implementation plan for Goal execution; implementation must preserve the ticket's named proof route and final TAS-A review gates.

## Repaired Gate Check

- `planner due_at validation/materialization`: pass. The revised plan now explicitly routes optional `lifecycle.due_at` through `skills/plan-next-wave/scripts/validate_wave_response.py`, tests absent/valid/date-only/timezone-naive/malformed cases, reuses `bin/core/farplane_ticket_reward.py:is_timezone_bearing_iso_datetime`, and materializes accepted values through `skills/pulse-update/scripts/materialize_skill_call.py` while omitting absent values.
- `TASK-0405 overlap`: pass. Change 2 now names `tickets/TASK-0405/ticket.md`, `tickets/TASK-0405/progress.md`, `skills/interval-update/scripts/highlight_ledger.py`, and its tests as read/proof surfaces, preserves report-finalized highlight append before ticket deltas, and adds highlight regression proof to Done/QA/evidence.
- `final review routing`: pass. The QA Strategy now uses registered rubric families: `code-quality`, `skill-contract`, `integration-readiness`, `evidence-quality`, and `documentation-quality`.
- `direct admission and refill fallback proof`: pass. Done/QA still require one integrated proof for same-run known intervention without Plan Next Wave and a second proof where ungrounded evidence produces no ticket and later low-watermark refill can call Plan Next Wave.

## Adversarial Rejection Attempts

- Tried to reject the plan as too broad for one ticket. Rejected: the plan defends one coherent migration and explains why splitting movement, Interval admission, strategy-state removal, and deadlines would leave temporary competing owners.
- Tried to reject `due_at` as a second scheduler state. Rejected: the plan keeps `priority` first, `due_at` optional and delivery-only, and `Reward.check_in_at` outcome-evaluation-only.
- Tried to reject Interval versus Plan Next Wave ownership as ambiguous. Rejected: Interval owns observed-problem conversion; Plan Next Wave remains side-effect-free low-supply refill.
- Tried to reject removal boundaries as unsafe. Rejected: the ticket explicitly preserves native Goal Advisor, ticket Goal Packets, user goals, non-goals, metric targets, and historical/migration evidence while retiring only project-level strategy surfaces.
- Tried to reject TASK-0405 overlap as under-specified. Rejected after revision: the plan now names the exact highlight read, order, and regression tests.

## Rubric Sections

### Spec Contract

- `tas`: `TAS-A`
- `required_tas`: `TAS-A`
- `pass`: true
- `checks`: coherent single problem, explicit in/out boundaries, preserved native Goal execution, clear Interval/refill split, testable done conditions.
- `failed_checks`: none.
- `findings`: none.
- `next_action`: execute the whole ticket as the planned migration unit unless implementation discovers a real blocker.

### Implementation Plan

- `tas`: `TAS-A`
- `required_tas`: `TAS-A`
- `pass`: true
- `checks`: readable before/after structure, local owner mapping, sequencing, proof route, docs strategy, visual companion, overlap handling, and valid review routing.
- `failed_checks`: none.
- `findings`: none.
- `next_action`: proceed to implementation with the listed ordered sanity checks.

### Integration Readiness

- `tas`: `TAS-A`
- `required_tas`: `TAS-A`
- `pass`: true
- `checks`: shared parser route for date validation, explicit materialization path, TASK-0405 overlap preservation, removal boundary, dirty-worktree caution, and no-compatibility migration stance.
- `failed_checks`: none.
- `findings`: none.
- `next_action`: implementation should reconcile current uncommitted edits before changing overlapping files and rerun both TASK-0406 and TASK-0405 focused checks.

### Evidence Quality

- `tas`: `TAS-A`
- `required_tas`: `TAS-A`
- `pass`: true
- `checks`: critical path, ordered sanity checks, concrete QA commands, delegated QA/agent-QA/reviewer lanes, due_at edge proof, removal-term search, TASK-0405 regression artifact, direct-admission proof, refill-fallback proof.
- `failed_checks`: none.
- `findings`: none.
- `next_action`: collect the named artifacts under `tickets/TASK-0406/artifacts/qa/` and `tickets/TASK-0406/artifacts/review/` during implementation.

### Debloatability

- `tas`: `TAS-A`
- `required_tas`: `TAS-A`
- `pass`: true
- `checks`: removes duplicated mutable strategy state, deletes uncalled `update-strategy`, rejects compatibility aliases, avoids war-room/state sprawl, preserves only stable intent and ticket strategy.
- `failed_checks`: none.
- `findings`: none.
- `next_action`: keep the implementation to the no-compatibility cleanup boundary and regenerate inventories from source.

## Residual Risk

- The worktree remains dirty and overlapping. This is accepted for plan approval because the ticket now requires reconciliation, TASK-0405 highlight preservation, and focused reruns before completion.
- The live Plan Next Wave response contract does not yet include `due_at`; this is expected pre-implementation and is now explicitly part of the approved write/test plan.

## Next Action

Proceed with implementation. Before completion, require the ticket's planned QA evidence, TASK-0405 regression artifact, evidence review, and completion review to reach TAS-A.
