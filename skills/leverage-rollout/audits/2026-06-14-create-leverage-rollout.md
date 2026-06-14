---
title: Create leverage-rollout skill
status: complete
owner: skill-creator
created_at: 2026-06-14
target:
  - skills/leverage-rollout/SKILL.md
---

# Create Leverage Rollout Skill

## Summary

Created a Tier 3 harness workflow for proving a selected leverage play through
one to three exemplar cases before scaling through Goal Advisor rollout mode.

## Checks

- First-load contract includes trigger boundary, signature, phase contract,
  todo path, program, gotchas, references, and output shape.
- Reuse is explicit: `leverage-rollout` calls `leverage-advisor` for play
  selection and `goal-advisor` for Goal-backed rollout after sample proof.
- The default path blocks broad rollout until exemplar proof and target set
  exist.

## Proof

Run:

```bash
python3 skills/skill-maintenance/scripts/check_skills.py --write
```
