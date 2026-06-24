---
skill: advise
date: 2026-06-24
change_type: maintenance
owner: skill-maintenance
status: pass
review_route: operator_correction
before_ref: skills/advise/SKILL.md
after_ref: skills/advise/SKILL.md
reasoning_basis: operator_feedback
proof_artifacts:
  - skills/advise/SKILL.md
  - skills/budget-advisor/references/advise-example.md
eval_required: no
---

# Skill Audit

## Change

- Before: `advise` briefly carried `budget?`, `AdviseBudget`, budget personas,
  and `budget-advisor` routing inside its first-load contract.
- After: `advise` is restored as the simple Tier 1 primitive: state the
  decision, compare three viable options, recommend one, name the tradeoff, and
  state the next step.
- Why: Budget transformation belongs to `budget-advisor`, not to the base
  `advise` skill. `budget-advisor/references/advise-example.md` is the correct
  place to show how budget parameters wrap the base advice program.
- Tradeoff accepted: `advise` keeps its older template marker until there is a
  separate structure-only upgrade that does not change its behavior.

## Proof Artifacts

- Validator: pass, `python3 scripts/check_skills.py --write`.
- Live install: pass, selected install of `advise`.
