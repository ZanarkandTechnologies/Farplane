---
template_id: ticket-template
template_version: "0.3.0"
feature_refs:
  - FEAT-0007
  - FEAT-0008
ticket_id: TASK-XXXX
title: title
status: todo
created_at: YYYY-MM-DDTHH:MM:SSZ
updated_at: YYYY-MM-DDTHH:MM:SSZ
depends_on: []
# Required only when UI, layout, interaction, visual state, or taste is in scope.
# ui_scope: true
---

# TASK-XXXX: title

<!-- Keep ticket.md + program.md + the latest 80 progress lines within the
300-line target and 400-line hard limit. Bulky evidence belongs in artifacts/.
Start with the sections rendered below. Add Map, Docs Strategy, Links, or Notes
only when omitting them would lose a current execution, review, proof, or resume
decision. Never retain an empty optional section or placeholder `none` row.
`claimed_by` is present only while status=active. The hook may set one immutable
`thread_id` for this ticket's persistent Codex task; never store session_id here.
Full authoring rules: tickets/README.md. -->

## Summary

One paragraph: valuable outcome, beneficiary, and why this ticket matters now.

## Scope

- In:
- Out:
- Constraints:

## Delta

> **Before:** Quote or cite the observed current behavior and exact gap; if
> evidence is missing, state the current assumption and evidence gap.
>
> **After:** State the smallest intended change and how it closes that gap.
>
> **Example:** One representative current workflow or result -> intended
> outcome.

## Contract Diagram

<!-- Required. Draw the smallest ASCII model that lets an unfamiliar agent
simulate the intended work before implementation. Adapt it to the ticket: UI
states/actions; backend boundaries/data flow; docs/config transformation; or
research evidence/decision flow. Give referenced states and seams stable IDs. -->

```text
[S1 input/current state] -> [S2 decision/change] -> [S3 intended state]
                               |
                               +-> [F1 failure/recovery]
[S3] -> [P1 observable proof]
```

<!-- Add Planned Skill Call, Objective Contribution, or Reward only when their
named consumer exists; use tickets/README.md for those optional shapes. -->

## Change Plan

### Change 1: coherent unit

```yaml
diagram_nodes: [S2, S3]
files:
  read: []
  edit: []
operation: concrete change
signature_delta: before -> after
assertions:
  - observable postcondition linked to the diagram
proof: command, eval, QA, or review artifact
failure: blocker or rollback condition
```

<!-- Repeat Change N only for independently reviewable units. Each unit owns
its files, operation, local proof, and failure boundary; do not repeat the
global Delta, QA Strategy, Docs Strategy, or routing policy in every unit. -->

## Done

- [ ] User-visible or system outcome is satisfied.
- [ ] Required checks pass with evidence links.
- [ ] No declared guard regresses.

## QA Strategy

```yaml
proof_weight: mechanical | eval | qa | visual_qa | agent_qa | review | hybrid
checks: []
delegated_lanes: []
evidence_paths: []
final_checkpoint: inline | reviewer | none
residual_risk: none
```

<!-- Add Gap Analysis, Docs Strategy, Agent Contract, or Run Hints only when the
branch needs them; use tickets/README.md for their compact contracts. -->

## State

- Current:
- Next:
- Blockers: none
