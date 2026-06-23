---
kind: skill-audit
skill: goal-advisor
status: pass
created_at: 2026-06-15
owner: goal-advisor
refs:
  - ../../horizon-advisor/references/project-goals.md
  - ../../../farplane/goals.md
  - ../../../docs/specs/program-notation.md
  - ../../../farplane/goals.md
---

# Feedback-Sized Project Rule Audit

## Change

Goal portfolios now default to feedback-sized projects instead of decomposing
goals into tasks by habit.

```text
goal -> project[]
project(...) -> milestone + starting_tasks? + evidence + child_ticket[]?
```

Child tickets are reserved for real execution, unblock, approval, review,
dependency, or proof boundaries.

## Checks

- Old frontier language was replaced with milestone language in the
  Goal Advisor portfolio reference and portfolio template.
- The shared Program Notation spec now defines `feedback_sized_project(...)`.
- The Farplane framework goals file dogfoods the rule with project-level nodes and
  `starting_tasks` hints instead of nested task trees.

## Risk

This is a grammar and template change only. Existing historical tickets and
archives are not rewritten.
