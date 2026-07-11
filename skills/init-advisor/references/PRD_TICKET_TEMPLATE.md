---
ticket_id: TASK-0001
title: Draft initial PRD
status: awaiting_review
priority: high
created_at: TODO
updated_at: TODO
---

# TASK-0001: Draft initial PRD

## Summary
Turn the project idea into a clear first PRD after the repository scaffold is in
place. This is intentionally separate from initialization because PRD discovery
can take time and should preserve human feedback.

## Scope
- In: run `deep-interview` for the project idea, draft `docs/prd.md`, and
  identify the first small lovable complete slice.
- Out: implementation, full backlog conversion, deploys, credentials, billing,
  and broad architecture rewrites.

## Done / Proof

```text
done_when:
  - docs/prd.md contains the problem, audience, first slice, goals, non-goals,
    constraints, risks, and backpressure.
  - next ticket or spec handoff is identified.

proof:
  checks:
    - docs/prd.md exists and is reviewable
  manual:
    - human reviews the PRD before implementation tickets are created
  review:
    - rubric: none
      required_tas: none
  evidence:
    - docs/prd.md
```

## Program

After approval, set `status: todo`; run `deep-interview`, then call `prd`.
Record current action, blockers, and verification in `progress.md` when the
ticket becomes a Goal Packet.

## Links
- `program:` none
- `progress:` none
- `artifacts:`
- `review:`
- `refs:` `docs/prd.md`
