---
title: Browser-Operated Comparable Research Audit
owner: functional-ui
status: complete
kind: skill-audit
created_at: 2026-08-02
updated_at: 2026-08-02
mode: behavior_hardening
ticket: TASK-9004
---

# Browser-Operated Comparable Research Audit

## Behavior Delta

```text
before: functional-ui requested 2-4 comparable apps but did not say how to
  inspect them, preserve evidence, handle access limits, or skip the work.
after: material/unsettled/current workflows operate 2-4 comparables through
  agent-browser and record URL, user job/query, observed sequence/states,
  evidence refs, access limits, and adopt/adapt/reject decisions. Tiny settled
  fixes and pure visual polish skip the pass. Pinterest and galleries remain
  taste sources rather than functional proof.
owner_surface: functional-ui decides the workflow and evidence threshold;
  agent-browser operates sources; visual-design and ingest-content own taste.
```

## Source Role Review

- Direct products: current behavior and defaults.
- Mobbin: screen, element, state, category, and flow reconnaissance.
- Page Flows: recorded end-to-end journeys and sequence evidence.
- Pinterest/Savee/galleries: visual taste only, never the sole functional proof.
- Login walls: record the limit; do not bypass or invent inaccessible states.

## Proof Notes

- Baseline comparable task verdict: `C`; the answer used documentation and
  generalized claims instead of operated evidence.
- Baseline tiny-fix task verdict: `A`; the settled-pattern skip route was
  already correct and remained A in the owner candidate.
- Final comparable synthesis candidate:
  `tickets/TASK-9004/artifacts/eval-runs/20260801-182439-task-9004-owner-candidate-v8/summary.json` (A).
- Independent live operation proof:
  `tickets/TASK-9004/artifacts/browser-operation-qa.md` (pass), with Mobbin
  access-limit and public Page Flows/HeyGen sequence evidence.
- Comparison receipt: `tickets/TASK-9004/artifacts/eval-comparison.md`.
- Query-spoiler lint: pass.
- Skill Maintenance aggregate validation: generated registries and functional
  todo/link checks passed; unrelated `content-impl-plan` surface-budget debt
  remains outside this ticket.
