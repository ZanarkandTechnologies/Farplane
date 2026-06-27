---
skill: qa
date: 2026-06-27
change_type: behavior
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/qa/SKILL.md; skills/qa/README.md
after_ref: skills/qa/SKILL.md; skills/qa/README.md
reasoning_basis: first_principles
proof_artifacts: []
eval_required: no
---

# QA Goal Completion Proof Audit

## Change

- Before: `qa` described its structured result as hook-coupled gating and ended
  with `EXECUTION_RESULT`.
- After: `qa` describes its output as ticket/Goal completion proof and ends
  with `QA_RESULT`, while preserving `result.json`, report, artifacts, and
  ticket writeback.
- Why: QA should be a durable evidence producer, not a coupling point to hook
  orchestration.
- Tradeoff accepted: Consumers that expected `EXECUTION_RESULT` must update to
  read `result.json` and ticket links directly.

## First-Principles Reasoning

- Objective: Keep QA proof usable after live Stop orchestration is removed.
- Placement logic: The `qa` skill owns the artifact/result contract.
- Expected behavior delta: Agents call QA for evidence and writeback, then
  reviewers judge completion from those artifacts.
- Proof needed: Skill validator and JSON/Markdown consistency checks.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Signature and checklist still describe artifacts and gates. |
| `reference_load_precision` | pass | No extra references required. |
| `missing_context_rate` | pass | Ticket/proof read remains the first obligation. |
| `noisy_context_rate` | pass | Removed Stop-hook coupling instead of adding ceremony. |
| `duplicated_instruction_count` | pass | `result.json` remains the shared artifact. |
| `prompt_size_tokens` | pass | Net wording stays compact. |
| `task_success_rate` | unknown | Needs future QA run sample. |
| `review_tas_rate` | unknown | Needs future completion review sample. |
| `maintenance_locality` | pass | Change stays in QA docs. |
| `composition_clarity` | pass | Goal/ticket completion owns the final review. |

## Proof Artifacts

- Skill-local evals, when needed: none
- Structure evals, when needed: pending validator run
- Reviewer receipt: none
- Validator: pending
- Eval required: no
- Evidence gaps: no live Goal sample yet

## Before Behavior

- QA completion language pointed agents back to the Stop-hook runtime.

## After Behavior

- QA completion language points agents to durable ticket/Goal proof artifacts.

## Followups

- Update any archived Stop-hook tests only if they are reactivated as a
  non-continuing guard.
