---
ticket_id: TASK-0001
title: Draft initial PRD
phase: planning
status: review
owner: human
claimed_by:
priority: high
depends_on: []
blocked_by: []
ready: false
approval_required: true
requires_qa: false
requires_demo: false
created_at: TODO
updated_at: TODO
next_action: run deep-interview for the project idea, then use prd to draft docs/prd.md
last_verification: scaffolded by init-advisor
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

## State
- `next_action:` run `deep-interview`, then call `prd`.
- `blocked:` false
- `latest_verification:` scaffolded
- `result:` pending

## Links
- `program:` none
- `progress:` none
- `artifacts:`
- `review:`
- `refs:` `docs/prd.md`
