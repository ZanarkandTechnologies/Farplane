---
skill: pulse-update
date: 2026-07-15
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: skills/pulse-update/SKILL.md@HEAD-505-lines-plus-concurrent-dirty-base
after_ref: skills/pulse-update/SKILL.md@521-lines
reasoning_basis: reviewer
proof_artifacts:
  - tickets/TASK-0380/artifacts/agent-qa/plan.md
  - skills/pulse-update/evals/evals.json#pulse_transports_terminal_preference_without_rejection_outage
eval_required: yes
---

# Terminal Preference Transport Audit

## Change

- Before: Pulse did not explicitly normalize terminal Reward decisions into a
  bounded planner preference snapshot, and rejected idea count could be a hard
  planning guard.
- After: Pulse transports terminal `accept|kill` evidence only, omits pending
  and monitor rows, requires Idea QA receipts before materialization, and leaves
  rejection count diagnostic-only.
- Why: negative feedback should teach ranking without freezing unrelated work.
- Tradeoff accepted: one additional planner input/receipt with no new runtime
  controller or script-owned taste policy.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Signature, history normalization, planner call, and receipt are explicit. |
| `reference_load_precision` | pass | No new reference is required for the normal Pulse path. |
| `missing_context_rate` | pass | Missing terminal fields produce no invented preference. |
| `noisy_context_rate` | pass | Prompt/transport delta is narrow; no planner logic was copied into Pulse. |
| `duplicated_instruction_count` | pass | Pulse owns normalization/transport; planner owns admission judgment. |
| `prompt_size_tokens` | fail | Aggregate line count is 505 -> 521 and the pre-existing skill exceeds the normal budget. |
| `task_success_rate` | pass | Focused Pulse guard tests pass and the selected rejection metric is absent from hard guards. |
| `review_tas_rate` | unknown | Completion review pending. |
| `maintenance_locality` | pass | No hook, new agent, or taste-bearing script was added. |
| `composition_clarity` | pass | Terminal Reward -> preference snapshot -> pure planner -> Pulse materialization is explicit. |

## Proof Artifacts

- Eval row: `pulse_transports_terminal_preference_without_rejection_outage`.
- Mechanical proof: focused Pulse guard tests and harness/metrics inspection.
- Evidence gap: a live model invocation is blocked by account usage capacity.

## Before Behavior

- Rejection was observable but not a bounded preference input and could also
  participate in the planning outage guard set.

## After Behavior

- Terminal feedback changes planner context without becoming authority or a
  hard outage; unrelated planning remains governed by actual configured guards.

## Followups

- Preserve `monitor` as nonterminal and revisit preference aging only through a
  separately evidenced ticket.
