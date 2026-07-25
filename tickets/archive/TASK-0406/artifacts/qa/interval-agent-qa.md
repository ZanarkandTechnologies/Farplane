---
kind: qa-artifact
ticket_id: TASK-0406
artifact: interval-agent-qa
verdict: pass
created_at: 2026-07-25
---

# Interval adversarial QA

Verdict: PASS

## Claim

The consolidated Interval contract resists the ticket-quality regressions called
out by TASK-0406: ticket flooding, planning residue, fake momentum, missing
evidence, duplicate ownership, and accidental execution.

## Method And Executed Traces

The QA route used Eval `behavior_trace` to capture exact child-agent prompts,
answers, JSONL events, logs, and independent Codex judge results. The initial
run exposed incomplete decision receipts; the contract and one underspecified
eval input were repaired, and only failed cases were rerun. These are the final
TAS-A receipts:

Invocation pattern:

```text
farplane run -- python3 skills/eval/scripts/run_evals.py run \
  --harness codex --judge-harness codex --target-root . \
  --skill interval-update --behavior-trace --max-parallel-tasks 1 \
  --runs-dir tickets/TASK-0406/artifacts/qa/agent-traces \
  --label <run-label> --task-id <case-id>
```

| Behavior | Judge | Receipt |
| --- | --- | --- |
| Duplicate active owner | A | `agent-traces/20260725-152851-task0406-agentqa/tasks/interval_duplicate_active_owner_rejected.json` |
| Provider fail-closed / authority | A | `agent-traces/20260725-152851-task0406-agentqa/tasks/interval_notion_binding_fails_closed.json` |
| Planning residue / weak work | A | `agent-traces/20260725-153310-task0406-agentqa-rerun1/tasks/interval_vague_low_materiality_and_ungrounded_rejected.json` |
| Sparse nonplanning highlights | A | `agent-traces/20260725-153310-task0406-agentqa-rerun1/tasks/interval_highlights_remain_sparse_and_nonplanning.json` |
| No cap, volume-as-momentum, or fragmentation | A | `agent-traces/20260725-153527-task0406-agentqa-rerun2/tasks/interval_multiple_independent_qualified_interventions.json` |
| Same-run known correction; no accidental execution | A | `agent-traces/20260725-153723-task0406-agentqa-rerun3/tasks/interval_known_intervention_same_run_ticket.json` |
| Missing evidence admits only concrete feedback unblock | A | `agent-traces/20260725-154045-task0406-agentqa-rerun6/tasks/interval_missing_feedback_admits_only_concrete_unblock.json` |

Superseded B/C receipts remain in earlier run directories as the visible
repair trail. No scheduled external-provider run was performed; provider
authority is tested fail-closed, and local integration is replayable through
`run_control_loop_fixtures.py` plus `fixture-output/`.

## Adversarial cases

| Case | Expected behavior | Evidence |
| --- | --- | --- |
| Ticket flooding | No numeric cap, but each admitted ticket must independently pass materiality, executability, concrete proof, dedupe, authority, and coherence gates. | `skills/interval-update/SKILL.md`; `skills/interval-update/references/interval-update.md`; interval eval fixtures in `skills/interval-update/evals/evals.json`. |
| Planning residue | Vague “plan strategy” work and artifact-free tickets are rejected. | `skills/interval-update/qa_checklist.md`; behavior eval fixtures; `tickets/TASK-0406/artifacts/qa/control-loop-refill-fallback.json`. |
| Fake momentum | Core derives movement from raw adjacent observations and direction; missing, stale, invalid-date, and zero-time inputs yield unknown instead of favorable momentum. | `bin/core/farplane_project_snapshot.py`; `bin/tests/test_farplane_project_snapshot.py`; ordered test receipt. |
| Missing evidence | Interval records the source gap/candidate and creates no direct ticket unless the investigation output is decision-changing. | `skills/interval-update/templates/interval-report.md`; `control-loop-refill-fallback.json`. |
| Duplicate ownership | Active duplicate work is rejected/updated rather than creating another competing ticket. | `skills/interval-update/references/interval-update.md`; interval eval fixtures. |
| Accidental execution | Interval may create/update/reject todo tickets but does not execute ticket work, mutate terminal evidence, or bypass the configured board provider. | `skills/interval-update/SKILL.md`; `farplane/automations.toml`. |

## Result

PASS / TAS-A. The adversarial risks are covered by final A-rated child-agent
traces, the updated Interval contract/checklist/evals, Core movement tests, and
replayable integration fixtures. This tester receipt does not self-approve the
evidence bundle or completion.
