---
title: Skill template intelligence artifact audit
date: 2026-06-14
owner: skill-maintenance
ticket: TASK-0202
---

# Skill Template Intelligence Artifact Audit

## Behavior Delta

- Before: skill template rollout could be inspected through
  `skill_template_version` and `check_skills.py`, but template history, feature
  rows, archive snapshots, and common eval signals were not generated together.
- After: `generate_template_intelligence.py` produces
  `skills/skill-maintenance/graph/skill-template-intelligence.json` with
  template epochs, archived snapshot paths, skill feature rows, rollout matrix,
  and representative template eval signals.

## Evidence

- `python3 skills/skill-maintenance/scripts/test_generate_template_intelligence.py`
  passed.
- `python3 docs/features/validate_features.py` passed with 58 records.
- `python3 skills/skill-maintenance/scripts/check_skills.py --write` passed.
- Generated artifact summary: 19 epochs, 87 rollout rows, 95 eval results.

## Caveats

- Template evals are heuristic research signals, not universal quality scores.
- Git mining recovers useful historical snapshots, but future template changes
  should refresh the archive deliberately at change time.
- Farplane UI renders the generated artifact; Farplane remains the source of
  truth for skill template governance.
