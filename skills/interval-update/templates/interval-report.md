---
kind: interval-report
ref: reports/interval/<interval_id>/<timestamp>
project: <project>
automation_id: <automation_id>
interval_id: <daily|weekly>
status: draft
created_at: <timestamp>
review_window: <start>..<end>
ui_summary: "<one concise control-loop summary under 100 words>"
source_gaps: []
---

# <Daily|Weekly> BAU Review

## Summary

- `window_result:`
- `what_changed_and_why:`
- `feedback_loop_status:` working | proxy_only | human_review_only | missing_instrumentation
- `dominant_bottleneck:`
- `material_decision:`
- `operator_attention:`

## Work And Outcomes Reviewed

| State / outcome | Work items / reports | Sanitized evidence | Observation |
| --- | --- | --- | --- |

## Metric Movement

| Objective / metric | Direction | Prior -> current | Progress delta / velocity | Momentum | Evidence / confidence |
| --- | --- | --- | --- | --- | --- |

Use `unavailable`, `stale`, or `incomparable` plus a source gap when movement
cannot be derived honestly. Never invent a flat or favorable value.

## Bottleneck And Root Cause

- `objective_or_need:`
- `feedback_loop_status:`
- `missing_feedback_or_instrumentation:`
- `blocked_systems:`
- `observed_symptoms:`
- `dominant_bottleneck:`
- `root_cause_claim:`
- `root_cause_confidence:` high | medium | low | unknown
- `alternatives_ruled_out:`
- `simplest_correct_path:`

Ground every problem and system-gap statement in ticket, progress, metric,
feedback, or completed-report evidence. Do not optimize from vibes.

## Problems

- [ ] <carried|new>: <problem>. Evidence: `<prior or same-run ref>`. Ticket: none
- [x] <resolved|ticketed>: <problem>. Evidence: `<ref>`. Ticket: `TASK-XXXX`

Use ordinary Markdown only. Do not add finding IDs, finding frontmatter, or a
registry. Carry unresolved finalized rows by report link; never rewrite them.

## Intervention Comparison

| Root problem | Candidate intervention | Compounding effect / recurrence prevention | Time to evidence / reversibility | Dependencies / risk | Coherence | Decision |
| --- | --- | --- | --- | --- | --- | --- |

Prefer the largest coherent intervention for each root problem. `Decision` is
one of `solution_ticket`, `investigation_ticket`, `update_todo`,
`reject_todo`, `duplicate`, `planner_candidate`, `low_materiality`,
`planning_residue`, `source_gap`, `blocked_by_authority`, or `not_ticketable`.

## Ticket Delta Decisions

| Problem | Existing owner / dedupe evidence | Executable intervention | Concrete output and proof | Authority / protected-state check | Intended delta | Reason |
| --- | --- | --- | --- | --- | --- | --- |

An investigation output must include reproduced cause, ruled-out alternatives,
selected correction, and proof artifact. Record every qualified independent
delta; there is no numeric cap or target. Never rewrite active, review,
waiting-signal, blocked-execution, or terminal work.

Every actionable finding must map to an intended delta or explicit no-action
reason. A feedback-loop unblock must name the signal, capture artifact, decision
it unlocks, and stop condition. Preserve approval gates for spend, publishing,
customer contact, account changes, and private-data use.

## Source Gaps

| Missing or stale source | Effect on review/admission | Safe fallback |
| --- | --- | --- |

For an unavailable configured provider with filesystem policy `exclude`, use
`none` as the fallback. Never include resolved private IDs, URLs, tokens, or raw
provider payloads.

## Receipts

- `shared_review_algorithm:` yes | no
- `cadence_difference:` evidence_window_only | violation
- `report_finalized_before_highlight_append:` yes | no
- `highlight_selection_after_report_complete:` yes | no
- `team_slug:`
- `win_highlight:` appended | already_exists | no_eligible_win
- `failure_highlight:` appended | already_exists | no_eligible_failure
- `highlight_memory_or_correction_action:` none
- `ticket_deltas_applied_after_highlights:` yes | no
- `solution_tickets_created:`
- `investigation_tickets_created:`
- `todo_tickets_updated_or_rejected:`
- `candidate_interventions_not_admitted:`
- `arbitrary_ticket_cap_applied:` no
- `protected_ticket_rewrites:` 0
- `planning_only_tickets_created:` 0
- `side_effect_gates_bypassed:` 0
- `provider_or_dogfood_run:` no
- `kanban_provider:` filesystem_tickets | notion | source_gap
- `filesystem_ticket_fallback_used:` no | yes_legacy_default
- `reward_or_checkin_mutated:` no
- `goal_pulse_worker_or_execution_started:` no
- `next_goal_or_heartbeat_owner:`
