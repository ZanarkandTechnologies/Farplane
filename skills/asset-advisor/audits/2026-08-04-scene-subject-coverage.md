---
skill: asset-advisor
date: 2026-08-04
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: skills/asset-advisor/qa_checklist.md
after_ref: skills/asset-advisor/qa_checklist.md
reasoning_basis: first_principles
proof_artifacts:
  - ../Gagazet/tickets/TASK-0019/artifacts/production/production-handoff-v4.json
eval_required: no
---

# Scene-subject coverage hardening

## Change

- Before: Asset readiness could pass at inventory level while a scene used UI,
  typography, or procedural drawing as its actual subject.
- After: every material editorial scene must point to accepted background,
  subject, evidence, and acceptance receipts; generic interface substitutes
  fail QA.
- Why: TASK-0019 v3 had a nominal asset plan but still rendered as CSS-first
  infographic motion.
- Tradeoff accepted: editorial reels need a slightly larger scene manifest.

## Proof

- Runtime guardrail: `skills/asset-advisor/qa_checklist.md`.
- Negative regression: TASK-0019 v4 passes handoff completeness but fails
  operator visual fidelity; it is not a positive brand exemplar.
- Deterministic adversarial cases: Gagazet production-handoff validator tests.
- Remaining risk: visual quality still requires isolated positive references,
  independent golden-frame judgment, and explicit artifact-bound approval;
  file presence alone does not prove taste.
