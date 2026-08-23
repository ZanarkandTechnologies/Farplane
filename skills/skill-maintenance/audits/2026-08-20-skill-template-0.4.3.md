---
title: "Skill template 0.4.3: simple callable contracts"
status: pass
owner: skill-maintenance
created_at: 2026-08-20
ticket: TASK-0442
---

# Skill template 0.4.3 audit

## Behavior delta

- Kept `Skill Signature` as the default type-linting contract.
- Reduced the signature to required files/data, caller parameters, work,
  writes, and returned outputs.
- Removed template-level `Phase Boundary`, `Phase Contract`, and `SkillBudget`
  guidance; Tier 0 and `budget-advisor` remain the canonical owners.
- Kept exact output-format guidance and made `unslop` the golden first-load
  writing pattern, with short examples beside the rule they clarify.

## Structure review

- `SKILL_TEMPLATE.md`: 98 lines and 527 words.
- Kept in first load: Context, Signature, domain Todo List, Gotchas, Output.
- Moved: no new files; shared budget behavior already lives in
  `budget-advisor`.
- Deleted: scaffolded phase and budget modules plus generic todo language.
- Rollout: no bulk rewrite of the 56 existing `Phase Boundary` sections;
  migrate them on contact after checking for unique domain behavior.

## Proof

- Template-intelligence unit tests: 6 passed.
- Template `0.4.3` heuristic checks: 5/5 passed.
- Skill checks, registry generation, feature validation, document references,
  JSON parsing, and `git diff --check`: passed.
- `skill_maintenance_plain_core_01`: initial TAS-B exposed missing explicit
  validation; repaired and rerun at TAS-A.
- `unslop` suite: three TAS-A and one recurring unsupported-summary miss;
  smallest failed case repaired and rerun at TAS-A.

## Verdict

Pass pending independent completion review. The change reduces first-load
ceremony without losing the callable contract, output shape, centralized
budget behavior, or inherited phase policy.
