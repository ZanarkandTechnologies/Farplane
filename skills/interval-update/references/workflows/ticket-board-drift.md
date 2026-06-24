---
title: "Ticket Board Drift Workflow"
status: active
owner: interval-update
kind: workflow-reference
template_uses:
  skill-template: "0.3.2"
---

# Ticket Board Drift Workflow

## Context

Use this workflow when an interval update needs to know whether the ticket board
still represents reality after the review window. The workflow proposes board
hygiene deltas; the parent interval update or a later ticket workflow decides
what to mutate.

Do not edit tickets, external boards, or project status systems from this
workflow.

## Workflow Signature

```text
ticket_board_drift(context_bundle, review_window, planning_window,
                   ticket_refs, status_refs?)
  -> stale_work + orphaned_work + board_hygiene_deltas + source_gaps

state: reads(context_bundle, ticket_refs, status_refs?);
       writes(parent_interval_update_report_section)
gates: ticket_refs_resolved; evidence_cited; proposed_deltas_only;
       no_ticket_mutation
fails: silently closing tickets; treating absent proof as completion;
       using external boards without configured refs
```

## Source Contract

Default sources:

- `ticket_refs`: local `tickets/` board, ticket metadata, ticket progress.
- Pulse reports and spawned-thread rows for selected work.
- interval reports for reported completions, blockers, or plan deltas.

Optional sources:

- `context_refs.workflow_refs.status_refs`: Notion tasks, external boards, PM
  dashboards, or customer-facing task trackers.

## Phase Boundary

Run inline for small ticket sets. Use a read-only subagent when many tickets,
worker reports, or external status rows need reconciliation.

## Todo List

- [ ] 1. Bind inputs.
  - [ ] Resolve local ticket refs and review-window evidence.
  - [ ] Resolve configured status refs, if any.
- [ ] 2. Compare board to reality.
  - [ ] Find completed work not reflected in tickets.
  - [ ] Find tickets that were claimed, stale, blocked, oversized,
        underspecified, or repeatedly skipped by Pulse.
- [ ] 3. Check ticket metadata.
  - [ ] Compare `ready`, `blocked_by`, `approval_required`, `claimed_by`,
        phase, and proof state against evidence.
- [ ] 4. Classify hygiene deltas.
  - [ ] Label each issue as `writeback`, `split`, `park`, `kill`,
        `goal_advisor_candidate`, `needs_human`, or `source_gap`.
- [ ] 5. Return proposed deltas.
  - [ ] Include evidence refs and the smallest next mutation surface.
  - [ ] Do not perform the mutation.

## Templates

Read-only subagent handoff:

```text
Read <context_bundle>. Run ticket_board_drift for <review_window>.
Return stale_work, orphaned_work, board_hygiene_deltas, and source_gaps.
Do not edit tickets or external boards.
```

## Gotchas

- A skipped ticket might be intentionally blocked or low-leverage; check Pulse
  reports before calling it stale.
- A completed implementation without proof is not a closed ticket.
- External status refs can disagree with local tickets; report the conflict
  rather than choosing a winner silently.

## Reference Map

- Parent interval update loads this file only when
  `report_workflows.ticket_board_drift` is enabled.

## Output

```text
stale_work:
  - ticket:
    issue:
    evidence:
orphaned_work:
  - work:
    suggested_ticket_delta:
    evidence:
board_hygiene_deltas:
  - ticket_or_candidate:
    action: writeback | split | park | kill | goal_advisor_candidate | needs_human
    evidence:
source_gaps:
```
