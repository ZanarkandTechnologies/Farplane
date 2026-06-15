---
name: board-drain
description: "Turn idle project time and local/Notion task boards into a selected Goal Advisor handoff, clarification request, or strategy-planning fallback."
tier: 3
group: harness
source: local
skill_template_version: "0.2.0"
common_chains:
  after:
    - goal-advisor
    - weekly-strategy-analysis
allowed-tools: Read, Grep, Glob, Bash
---

# Board Drain

## Context

Use this skill when an operator wants an autonomous idle worker to check whether
a project has been active recently, select useful proceedable work from local
and Notion boards, and hand the selected work to Goal Advisor without creating
a hidden scheduler.

This skill is a selector and handoff contract. It does not replace
`goal-advisor` as the execution compiler, `impl` as the coding-ticket executor,
or `weekly-strategy-analysis` as the no-ticket planning fallback. Live hourly
scheduling must be provided by an explicit automation surface; until then, this
skill emits a ready-to-run heartbeat packet or no-op report.

## Skill Signature

```text
board_drain(project_root?, activity_window?, board_sources?, budget?)
  -> activity_status
   + candidate_set
   + selection_decision
   + goal_advisor_handoff | clarification_request | weekly_strategy_handoff | no_op

state:
  reads(Farplane Console activity provider, tickets/TASK-*/ticket.md,
        tickets/README.md, Notion task views through notion-context when available,
        docs/specs/goal-loop-contract.md, active project docs)
  writes(ticket/progress/artifact updates only when explicitly running a selected ticket)

gates:
  activity_window_checked; local_board_checked; notion_status_labeled;
  proceedable_filter_applied; compounding_filter_applied;
  human_gates_respected; goal_advisor_handoff_ready

routes:
  notion-context | goal-advisor | impl-plan | impl |
  weekly-strategy-analysis | telegram-message | review

fails:
  hidden daemon; skipping activity check; mutating Notion;
  selecting blocked/claimed/human-gated work; starting implementation without
  a ticket or Goal Packet; treating weekly planning as a replacement for tickets
```

```text
BoardDrainBudget = {
  activity_window_minutes?: 60,
  selection_width?: 3,
  implementation_budget?: "tiny" | "normal" | "large",
  notify?: "telegram" | "local_artifact" | "none"
}
```

## Phase Contract

```text
phase_contract(idle_heartbeat, bound_inputs, state)
  -> grounded_activity
   + normalized_candidates
   + advised_selection
   + goal_advisor_or_strategy_handoff
   + no_op_or_notification_evidence
```

Keep planning and execution separate: this skill chooses the next useful
milestone, then `goal-advisor` compiles the native Goal, heartbeat, or direct
route for the selected ticket.

## Phase Boundary

This skill performs board normalization and selection inline. Call
`weekly-strategy-analysis` only when no proceedable candidate exists, and call
`review` only for a material changed artifact or completion claim.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the heartbeat inputs.
  - [ ] `project_root :=` current repo unless a project path is supplied.
  - [ ] `activity_window :=` default 60 minutes unless the caller supplies a cadence.
  - [ ] `board_sources :=` local tickets first, then Notion through `notion-context` when available.
  - [ ] `budget :=` operator-provided time/compute/notification limits, or a normal bounded ticket budget.
- [ ] 2. Check recent activity before selecting work.
  - [ ] Run `python3 bin/farplane_recent_activity.py --project-root <project_root> --window-minutes <activity_window> --json` to query the Farplane Console activity endpoint.
  - [ ] If recent activity exists, emit `no_op(activity_present)` unless the caller explicitly asks to drain anyway.
  - [ ] If the endpoint or key is missing, stop with `activity_provider_unavailable` unless the caller explicitly permits `--allow-local-fallback` for diagnostics.
- [ ] 3. Load and normalize candidate boards.
  - [ ] Read local `tickets/TASK-*/ticket.md` plus `tickets/README.md` selection rules.
  - [ ] Use `notion-context` for Notion task/project rows when the connector is available; if it is unavailable, label `notion_status := unavailable` and continue with local tickets.
  - [ ] Normalize each candidate as `source, id, title, status, phase, ready, approval_required, claimed_by, blocked_by, depends_on, project, next_action, proof, confidence, compounding_reason`.
- [ ] 4. Filter for safe autonomous work.
  - [ ] Keep only tickets that are ready, unblocked, unclaimed, dependency-satisfied, computer-actionable, and not gated by approval, spend, deploy, private credentials, or missing external access.
  - [ ] Skip Notion tasks in `Review` unless the operator explicitly asks for review work.
  - [ ] Prefer tasks with clear `Done / Proof`, explicit files, and narrow blast radius.
- [ ] 5. Rank the top milestone.
  - [ ] Build a top-three shortlist using compounding value: improves harness loops, ticket quality, telemetry, review/proof, skill reliability, feedback collection, or downstream unblock.
  - [ ] Use `advise` when the shortlist has real tradeoffs, and record the accepted tradeoff in the handoff.
  - [ ] Prefer well-defined tickets over speculative high-leverage ideas when both can compound.
- [ ] 6. Route the result.
  - [ ] If a ticket is selected, emit a `goal-advisor` handoff that lists the ticket, program/progress files if present, budget, proof target, and recommended path such as `impl-plan -> impl`.
  - [ ] If a promising ticket is unclear, emit a clarification request or `telegram-message` draft with the exact missing human input.
  - [ ] If no proceedable tickets exist, emit a `weekly-strategy-analysis` handoff to create or refresh tickets.
- [ ] 7. Finish with an operator-readable report.
  - [ ] Include `activity_status`, board source status, rejected blockers by category, selected ticket or fallback, next Goal prompt location, and notification/evidence paths.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

Selection report:

```text
activity_status:
  active: true|false
  window_minutes:
  latest_event:
board_status:
  local: checked|unavailable
  notion: checked|unavailable|blocked
shortlist:
  - id:
    source:
    title:
    compounding_reason:
    confidence:
decision:
  route: no_op|goal_advisor|clarification|weekly_strategy
  selected:
  accepted_tradeoff:
handoff:
  files:
  prompt_or_next_action:
  notification:
```

Goal Advisor handoff:

```text
Use goal-advisor for a board-drain heartbeat selection.

Files:
- <selected ticket.md>
- <program.md if present>
- <progress.md if present>

Trigger mode: heartbeat-selected ticket
Budget: <bounded time/compute/review limits>
Metric: ticket Done / Proof plus review or mechanical checks
Recommended path: impl-plan -> impl -> QA/review as required
No-op policy: if the ticket is no longer proceedable, re-run board-drain selection
```

## Gotchas

- Do not start a hidden background worker from this skill. A scheduler may call
  the skill, but the schedule itself must be an explicit automation artifact.
- Do not mutate Notion during selection. Treat Notion as a read source unless a
  separate task explicitly authorizes a write.
- Do not pick the highest-upside ticket if it is vague, blocked, human-gated,
  or missing proof; pick the most compounding proceedable ticket instead.
- Do not let an empty board end the loop silently. Route to
  `weekly-strategy-analysis` and create or refresh ticket candidates.

## Reference Map

- [../goal-advisor/SKILL.md](../goal-advisor/SKILL.md) - compile selected work into native Goal, heartbeat, rollout, or direct-route prompt.
- [../weekly-strategy-analysis/SKILL.md](../weekly-strategy-analysis/SKILL.md) - fallback when no proceedable tickets exist.
- `notion-context` installed skill - Notion project/task context rules when the connector is available.
- [../../tickets/README.md](../../tickets/README.md) - local ticket board and proceedable-work rules.
- [../../docs/specs/goal-loop-contract.md](../../docs/specs/goal-loop-contract.md) - Goal Packet, heartbeat, and progress contracts.
- [../../bin/farplane_recent_activity.py](../../bin/farplane_recent_activity.py) - Farplane Console recent-activity helper.

## Output

- A compact board-drain report in chat or a ticket-scoped artifact.
- A `goal-advisor` handoff for a selected ticket, or a clarification request,
  no-op report, or `weekly-strategy-analysis` handoff.
