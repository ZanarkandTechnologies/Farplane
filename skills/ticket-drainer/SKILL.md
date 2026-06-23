---
name: ticket-drainer
description: "Turn a lane-invoked ticket-drainer action into one selected local ticket, named child-thread handoff, report, and ledger update."
tier: 3
group: harness
source: local
template_uses:
  skill-template: "0.2.0"
  skill-eval-task: "0.1.0"
eval: eval_task.json
allowed-tools: Read, Glob, Grep, Bash

---

# Ticket Drainer

## Context

Use this skill when a pulse or rhythm lane policy selects ticket execution. It
selects one proceedable ticket and offloads leaf work to a named Codex child
thread. It is not the executor. It should preserve lane context by writing
reports and lineage, then letting the child thread handle implementation or
closeout.

This skill differs from `board-drain`: `board-drain` is the idle selector that
may produce a Goal Advisor handoff; `ticket-drainer` is the lane-invoked
project selector that owns report/ledger writeback and child-thread spawning.

Keep this skill separate from `pulse-update`, `rhythm-update`, and
`horizon-update`. Those skills decide lane planning and action policy; this
skill owns ticket-selection execution handoff when a lane chooses the
`ticket_execution` action.

## Automation Presets

`ticket-drainer.daily @none -> reports.ticket_update`

The automation manifest supplies lane policy, target thread, ticket sources,
side-effect gates, report handles, and local overrides. This skill owns
candidate filtering, ranking, child-thread prompt shape, lineage writeback,
fallback blocker reporting, and the ticket-update output contract.

## Skill Signature

```text
ticket_drainer_daily(project_root, ticket_sources, gates, report_paths, ledger)
  -> selected_ticket?
   + child_thread_handoff?
   + ticket_update_report
   + ledger_delta

state:
  reads(farplane/automations.json, farplane/goals.md, latest lane reports,
        .farplane/state/run-ledger.json, tickets/TASK-*/ticket.md,
        tickets/README.md, optional Notion read source)
  writes(.farplane/reports/ticket-update/latest.md,
         .farplane/reports/ticket-update/runs/<timestamp>.md,
         .farplane/state/run-ledger.json,
         selected ticket Links/Notes only when safe)

gates:
  local_tickets_checked; notion_disabled_or_labeled; proceedable_filter_applied;
  one_ticket_selected_or_no_op; child_thread_named_by_parent;
  lineage_recorded; no_leaf_context_pollution; side_effect_gates_respected

routes:
  impl-plan | goal-advisor | board-drain | review | close-ticket

fails:
  executing broad leaf work in the parent lane; asking the child to rename
  itself; selecting blocked/human-gated tickets; skipping ledger/report
  writeback; mutating Notion when disabled
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind project inputs from the automation manifest.
  - [ ] Read `farplane/automations.json`, especially ticket sources, gates,
        reports, lane policy, and `job_catalog.ticket_update`.
  - [ ] Read shared memory refs requested by the lane: goals, latest horizon or
        rhythm report, latest ticket update report, run ledger, and local tickets.
- [ ] 2. Normalize candidate tickets.
  - [ ] Load active `tickets/TASK-*/ticket.md`; exclude archive and templates.
  - [ ] If no local ticket is proceedable and Notion is enabled, read Notion
        through the configured binding; otherwise label Notion as skipped.
  - [ ] Normalize `id`, `title`, `status`, `phase`, `ready`,
        `approval_required`, `claimed_by`, `blocked_by`, `depends_on`,
        `priority`, `next_action`, `requires_qa`, and proof state.
- [ ] 3. Filter for safe daily-drainer work.
  - [ ] Keep only ready, unblocked, dependency-satisfied, approval-free,
        computer-actionable tickets.
  - [ ] Prefer bounded closeout or clear implementation work over vague,
        strategy-heavy, external-side-effect, or human-gated work.
  - [ ] Skip tickets in `review` unless the next action is explicit closeout,
        review prep, or evidence repair.
- [ ] 4. Rank and select at most one ticket.
  - [ ] Rank by priority, compounding ROI, project value, autonomy, and
        likelihood of reaching Done or Review.
  - [ ] Record the accepted tradeoff when bypassing higher-upside but riskier
        tickets.
- [ ] 5. Spawn or prepare the child handoff.
  - [ ] Name the child thread from the parent using
        `[Project] <ticket-id> <ticket name>` or the project override.
  - [ ] Include project root, parent cadence id, ticket path, context refs,
        expected outputs, gates, and lineage writeback path in the child prompt.
  - [ ] If thread creation is unavailable, write a handoff-ready prompt and
        blocker instead of executing broad leaf work in the parent cadence.
- [ ] 6. Write report and ledger.
  - [ ] Write latest and timestamped ticket-update reports.
  - [ ] Update the run ledger with status, selected ticket, child thread id or
        blocker, report paths, and freshness.
  - [ ] Update ticket Links/Notes only when doing so is safe and scoped.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Output

- `selected_ticket` or no-op reason.
- `child_thread_id` or handoff blocker.
- ranking reason and accepted tradeoff.
- report paths.
- ledger update.
- next daily/weekly follow-up recommendation.
