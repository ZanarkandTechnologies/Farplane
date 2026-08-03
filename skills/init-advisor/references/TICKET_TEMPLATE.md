---
template_id: ticket-template
template_version: "0.2.5"
feature_refs:
  - FEAT-0007
  - FEAT-0008
ticket_id: TASK-XXXX
title: title
status: todo
created_at: YYYY-MM-DDTHH:MM:SSZ
updated_at: YYYY-MM-DDTHH:MM:SSZ
depends_on: []
---

# TASK-XXXX: title

<!-- Keep ticket.md + program.md + the latest 80 progress lines within the
300-line target and 400-line hard limit. Bulky evidence belongs in artifacts/.
`claimed_by` is present only while status=active. Never store session_id here.
Full authoring rules: tickets/README.md. -->

## Summary

One paragraph: valuable outcome, beneficiary, and why this ticket matters now.

## Scope

- In:
- Out:
- Constraints:

## Delta

> **Before:** Current observable behavior.
>
> **After:** Intended observable behavior.
>
> **Example:** One representative workflow or result.

<!-- Add Planned Skill Call, Objective Contribution, or Reward only when their
named consumer exists; use tickets/README.md for those optional shapes. -->

## Change Plan

### Change 1: coherent unit

```yaml
files:
  read: []
  edit: []
operation: concrete change
proof: command, eval, QA, or review artifact
failure: blocker or rollback condition
```

<!-- Repeat Change N only for independently reviewable units. -->

## Map

```text
input -> owner/change -> output + evidence
```

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

## Links

- `program:` `none`
- `progress:` `none`
- `artifacts:` `none`
- `related:` `none`

## Notes

<!-- Sparse durable decisions only; execution logs belong in progress.md. -->
