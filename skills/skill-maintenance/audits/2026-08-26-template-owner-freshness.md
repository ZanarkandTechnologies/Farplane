---
skill: skill-maintenance
date: 2026-08-26
change_type: behavior
owner: skill-maintenance
status: reviewed
review_route: reviewer
before_ref: skills/skill-maintenance/scripts/check_skills.py
after_ref: skills/skill-maintenance/scripts/check_skills.py
reasoning_basis: observed_failure
proof_artifacts:
  - docs/skills/templates/SKILL_TEMPLATE.md
  - skills/skill-maintenance/SKILL.md
  - skills/skill-maintenance/scripts/check_skills.py
  - skills/skill-maintenance/scripts/test_check_skills.py
eval_required: no
---

# Skill Audit

## Change

- Before: `skill-maintenance` declared `skill-template: "0.5.0"`; its normal
  validation path checked lint and registry consistency but did not reject that
  stale declaration. Golden Node shape checking was also limited to exactly
  template `0.5.0` when invoked manually.
- After: `skill-maintenance` declares `0.6.2`; every standard
  `check_skills.py` run compares it to the canonical template and fails on a
  mismatch. Golden Node structure checking applies to `0.5.0` and newer.
- Why: the runtime-debugging maintenance pass used a stale maintenance package,
  so current-template behavior could not be assumed.
- Scope: the gate protects the maintenance owner only; it intentionally does
  not force an unproven all-skill template rollout.

## Decision

```text
canonical template version != skill-maintenance version
  -> standard validation fails
  -> upgrade skill-maintenance in the same change
```

## Proof

- `cd skills/skill-maintenance/scripts && python3 test_check_skills.py` —
  passed, 13 tests including current and stale owner-version cases.
- `python3 skills/skill-maintenance/scripts/check_skills.py --write
  --template-version 0.6.2` — passed: 12 skill-system checks, standard
  template-owner gate, and `0.6.2` Golden Node structure validation.
- Focused current-owner and Golden Node assertions, `py_compile`, and
  `git diff --check` — passed.
- Native reviewer — TAS-A pass; no blocking findings.

## Followup

- Add more template-owner skills only when each has been structurally migrated;
  do not turn this narrow recurrence guard into a broad rollout gate.
