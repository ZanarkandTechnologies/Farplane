---
skill: solution-shaping
date: 2026-07-07
change_type: behavior
owner: eval
status: pass
review_route: self_check
before_ref: .farplane/evals/runs/20260706-160629-problem-mvp-proof-advisor-check/summary.json
after_ref: skills/solution-shaping/SKILL.md
reasoning_basis: eval
proof_artifacts:
  - .farplane/evals/runs/20260706-160629-problem-mvp-proof-advisor-check/summary.json
eval_required: yes
---

# Skill Audit

## Change

- Before: Eval run found two `B` gaps for `solution-shaping`: missing explicit
  risks/assumptions heading in accepted-MVP handoff, and weak
  permissions/decision-rights plus system-design routing in hospital bed
  allocation.
- After: `SKILL.md` now gates on explicit risks/assumptions, and requires
  decision rights, permissions, records/entities, workflow risks, and
  `deep-system-design` handoff for system-heavy MVPs.
- Why: The MVP brief must stay reviewable and must not let regulated or
  coordination-heavy systems skip system design.
- Tradeoff accepted: Slightly stricter first-load gates for the product-level
  skill.

## Proof Artifacts

- Initial run: `.farplane/evals/runs/20260706-160629-problem-mvp-proof-advisor-check/summary.json`
- Follow-up required: rerun failed cases after the skill contract patch.

## Eval Query Review

- No eval rows changed in this patch.
- The fix targets skill behavior rather than teaching the answer in queries.
