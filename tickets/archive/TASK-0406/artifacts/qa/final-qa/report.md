Ticket / Proof Policy: `tickets/TASK-0406/ticket.md` / Done + QA Strategy + deterministic artifact proof; independent review gates handled after this QA receipt.
Verdict: pass

# TASK-0406 final QA report

## Runtime target and setup

Runtime target: local CLI plus isolated child-agent behavior traces. This is
proof over repo-owned project files, validators, tests, generated registries,
replayable integration fixtures, and Eval `behavior_trace` outputs. No
browser/API runtime is required.

## Critical path checked

1. Metric observations produce direction-normalized movement.
2. Interval consumes movement/evidence and finalizes a report.
3. A grounded known intervention becomes a concrete ticket delta with priority
   and optional `due_at`, without Plan Next Wave.
4. Pulse orders executable tickets by priority, then `due_at`, then ticket ID.
5. Insufficient evidence produces no direct ticket; later low ready supply can
   invoke Plan Next Wave as a side-effect-free refill planner.

## Commands and evidence

- Ordered test matrix: `tickets/TASK-0406/artifacts/qa/test-results.txt`
- Known-intervention fixture: `tickets/TASK-0406/artifacts/qa/control-loop-known-intervention.json`
- Refill-fallback fixture: `tickets/TASK-0406/artifacts/qa/control-loop-refill-fallback.json`
- TASK-0405 highlight regression: `tickets/TASK-0406/artifacts/qa/task-0405-highlight-regression.txt`
- Adversarial Interval QA: `tickets/TASK-0406/artifacts/qa/interval-agent-qa.md`
- Replay command:
  `python3 tickets/TASK-0406/artifacts/qa/run_control_loop_fixtures.py`
- Executed replay outputs:
  `tickets/TASK-0406/artifacts/qa/fixture-output/`
- Child-agent prompts, answers, logs, events, and judge receipts:
  `tickets/TASK-0406/artifacts/qa/agent-traces/`

## Obligation reconciliation

| Obligation | Verdict | Evidence |
| --- | --- | --- |
| Metric definitions declare direction and Core derives honest movement | PASS | `bin/tests/test_farplane_project_snapshot.py`; `bin/validators/test_check_farplane_project_files.py`; `test-results.txt` |
| Daily/Weekly Interval share one review/admission contract | PASS | `skills/interval-update/SKILL.md`; `skills/interval-update/references/interval-update.md`; interval eval fixtures |
| Known intervention admitted same run; uncertain intervention only with decision-changing output | PASS | `control-loop-known-intervention.json`; `control-loop-refill-fallback.json`; interval QA artifact |
| Ticket admission rejects weak, duplicate, unsafe, planning-only work and has no arbitrary count cap | PASS | `skills/interval-update/qa_checklist.md`; interval QA artifact |
| `due_at` validates/projects/orders correctly | PASS | `bin.tests.test_ticket_metadata`; `bin.tests.test_farplane_boards`; `skills/pulse-update/scripts/test_list_pulse_board.py`; `test-results.txt` |
| Retired strategy fields and `update-strategy` removed from active surfaces | PASS | `check_farplane_project_files.py`; active removed-term scan; docs/skill registry validation |
| Plan Next Wave remains refill-only and side-effect-free | PASS | `skills/plan-next-wave/scripts/test_validate_wave_response.py`; `skills/pulse-update/scripts/test_plan_wave_guard.py`; refill fixture |
| Native Goal Advisor / Goal Packet docs preserved | PASS | doc refs/parity validation; ticket/program Goal Packet links |
| TASK-0405 highlight behavior preserved | PASS | `task-0405-highlight-regression.txt`; `test_highlight_ledger.py` result |

## Failure/falsifier checked

- Zero-time, invalid-date, stale/missing metric movement do not create fake
  favorable momentum.
- A lower-priority dated ticket does not outrank higher-priority undated work.
- Unknown or timezone-naive `due_at` fails validation.
- Ungrounded Interval evidence does not become a planning-only ticket.
- Low-watermark refill remains available only when grounded work is absent.

## Judgment handoffs

This QA receipt does not self-approve completion. Required follow-on judgment
receipts are:

- `tickets/TASK-0406/artifacts/review/evidence-review.md`
- `tickets/TASK-0406/artifacts/review/completion-review.md`

## Verdict, blockers, residual risk

Verdict: PASS.

Blockers: none for QA artifact proof.

Residual risk: no live scheduled Daily/Weekly automation or external board
provider was run. Local code paths are replayed, and prompt behavior is captured
through independently judged child-agent traces; external-provider authority is
proved fail-closed.

## Learning

Learning outcome: `ticket_only`. The proof artifacts are specific to TASK-0406
and do not establish a reusable cookbook path.
