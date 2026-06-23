---
kind: skill-audit
skill: harness-creator
status: pass
created_at: 2026-06-15
owner: harness-creator
refs:
  - ../SKILL.md
  - ../references/harness-il.md
  - ../../horizon-advisor/references/project-goals.md
  - ../../../farplane/goals.md
---

# Feedback-Sized Project Rule Audit

## Change

Harness Creator now mirrors Goal Advisor's portfolio boundary rule: a project is
the default durable unit, and child tickets appear only when a real boundary
needs durable state.

## Checks

- `SKILL.md` first-load context names the rule before harness generation.
- `references/harness-il.md` defines `feedback_sized_project(...)`.
- The Farplane dogfood portfolio uses project-level nodes with `starting_tasks`
  hints instead of nested task trees.

## Risk

This is a planning-language change only. It does not schedule automations or
create child tickets.
