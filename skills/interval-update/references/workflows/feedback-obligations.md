---
title: "Feedback Obligations Workflow"
status: active
owner: interval-update
kind: workflow-reference
template_uses:
  skill-template: "0.3.2"
---

# Feedback Obligations Workflow

## Context

Use this workflow when an interval update needs to extract commitments,
blockers, follow-ups, or plan changes from configured human or external
feedback sources. This workflow is intentionally source-gated: if the caller
does not pass feedback refs, do not search private inboxes, chats, Notion,
CRM, or meeting systems by convention.

## Workflow Signature

```text
feedback_obligations(context_bundle, review_window, planning_window,
                     feedback_refs?, status_refs?)
  -> commitments + blockers + followups + plan_changes + source_gaps

state: reads(context_bundle, feedback_refs?, status_refs?);
       writes(parent_interval_update_report_section)
gates: feedback_refs_present_or_not_applicable; privacy_preserved;
       commitments_cited; no_external_mutation
fails: scraping private systems without refs; exposing private contact details;
       inventing due dates; treating suggestions as commitments
```

## Source Contract

Required for `when_sources_exist`:

- `context_refs.workflow_refs.feedback_refs`: meeting notes, operator feedback,
  customer feedback, support reports, review comments, user interviews, or
  stakeholder messages.

Optional supporting refs:

- `context_refs.workflow_refs.status_refs`: task, CRM, or status records linked
  to feedback.

Do not include private contact details in reports. Use role/org labels when the
identity is not necessary for the plan.

## Phase Boundary

Run inline for a small feedback packet. Use a read-only subagent when feedback
refs contain many meeting notes, reviews, or stakeholder rows.

## Todo List

- [ ] 1. Bind inputs.
  - [ ] If no feedback refs exist and mode is `when_sources_exist`, return
        `not_applicable`.
  - [ ] Confirm source date/window coverage.
- [ ] 2. Normalize feedback.
  - [ ] Extract source, date, safe actor/org label, decision, commitment,
        blocker, follow-up, related goal/ticket, and evidence.
- [ ] 3. Separate obligations.
  - [ ] Identify commitments made by the project.
  - [ ] Identify commitments owed by others.
  - [ ] Separate asks, ideas, and feedback from true commitments.
- [ ] 4. Identify planning impact.
  - [ ] Name blockers or plan changes caused by feedback.
  - [ ] Mark due dates as explicit or inferred.
- [ ] 5. Return follow-up agenda.
  - [ ] Distinguish proposed writebacks from permitted mutations.
  - [ ] Do not mutate external systems.

## Templates

Read-only subagent handoff:

```text
Read <context_bundle>. Run feedback_obligations for <review_window> and
<planning_window>. Use only configured feedback refs. Return commitments,
blockers, followups, plan_changes, and source_gaps. Do not mutate external
systems or expose private contact details.
```

## Gotchas

- Feedback can change priority without creating a commitment.
- A vague “we should” is not a due obligation unless the source provides owner
  and intent.
- If a person’s identity is not operationally needed, summarize at the role or
  organization level.

## Reference Map

- Parent interval update loads this file only when
  `report_workflows.feedback_obligations` is enabled.

## Output

```text
commitments:
  - owner:
    commitment:
    due_or_inferred:
    evidence:
blockers:
  - blocker:
    owner:
    evidence:
followups:
  - item:
    owner:
    due_or_inferred:
    evidence:
plan_changes:
  - change:
    reason:
    evidence:
source_gaps:
```
