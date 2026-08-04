---
skill: editing-advisor
date: 2026-08-04
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: skills/editing-advisor/qa_checklist.md
after_ref: skills/editing-advisor/qa_checklist.md
reasoning_basis: first_principles
proof_artifacts:
  - ../Gagazet/tickets/TASK-0019/artifacts/production/v4-editing-direction.md
eval_required: no
---

# Visual grammar and cadence hardening

## Change

- Before: the renderer handoff required timing and observable proof but did not
  explicitly prevent interface widgets from becoming the scene grammar.
- After: material scenes must bind accepted-media subjects, environments,
  evidence hierarchy, viewer-state changes, declared hold/motion limits, and
  golden-frame/range comparison.
- Why: timing compliance did not prevent TASK-0019 v3 from looking like a
  dashboard rather than an editorial explainer.
- Tradeoff accepted: readiness now needs representative rendered evidence.

## Proof

- Runtime guardrail: `skills/editing-advisor/qa_checklist.md`.
- Negative regression: TASK-0019 v4 satisfies the timed direction packet but
  fails operator visual fidelity; it is not a positive editing exemplar.
- Remaining risk: brand-specific cadence thresholds remain with the caller;
  this reusable skill enforces declared constraints without inventing them.
  Positive visual similarity still needs explicit human judgment.
