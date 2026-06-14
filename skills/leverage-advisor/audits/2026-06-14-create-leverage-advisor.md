---
title: Create leverage-advisor skill
status: complete
owner: skill-creator
created_at: 2026-06-14
target:
  - skills/leverage-advisor/SKILL.md
---

# Create Leverage Advisor Skill

## Summary

Created a Tier 2 advice workflow for turning an existing feature or capability
into ranked leverage plays, a recommendation, and an executable first proof
step.

## Checks

- First-load contract includes trigger boundary, signature, todo path, program,
  gotchas, references, and output shape.
- Reuse is explicit through `reference-grounding`, `advise`, `prototyping`,
  `goal-advisor`, `harness-advisor`, and `leverage-rollout`.
- The default path is advisory and does not execute rollout work.

## Proof

Run:

```bash
python3 skills/skill-maintenance/scripts/check_skills.py --write
```
