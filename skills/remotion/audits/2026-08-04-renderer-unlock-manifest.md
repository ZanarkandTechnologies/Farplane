---
skill: remotion
date: 2026-08-04
change_type: reference
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: skills/remotion/references/documentary-reel.md
after_ref: skills/remotion/references/documentary-reel.md
reasoning_basis: first_principles
proof_artifacts:
  - ../Gagazet/tickets/TASK-0019/artifacts/production/production-handoff-v4.json
eval_required: no
---

# Documentary renderer-unlock hardening

## Change

- Before: Remotion had to consume accepted media but could trust an incomplete
  renderer-ready label.
- After: the documentary route requires one scene-level unlock manifest tying
  Brand Kit, asset, edit, cadence, rights, and acceptance receipts together.
- Why: renderer success is not proof that upstream production planning was
  actually applied.
- Tradeoff accepted: final authoring blocks sooner on incomplete handoffs.

## Proof

- Runtime contract: `skills/remotion/references/documentary-reel.md`.
- Negative regression and adversarial failures: Gagazet v4 proves a manifest
  can pass while visual fidelity fails; five deterministic cases still prove
  the intended shortcut rejection.
- Remaining risk: the generic Remotion skill does not own project-specific
  brand thresholds or approval transport.
