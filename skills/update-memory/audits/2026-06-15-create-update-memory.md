---
kind: skill-audit
skill: update-memory
status: complete
created_at: 2026-06-15
---

# Create Update Memory

## Decision

Created `update-memory` as the generic project memory refresh primitive for PM
heartbeats.

It consolidates README, relevant docs, MEMORY, HISTORY, LESSONS, TROUBLES, and
recent progress into context/doc deltas, while routing eval/gotcha/skill-package
work to `skill-maintenance(mode: harden_skill)`.

## Proof Targets

- Frontmatter and checklist follow the Farplane skill template.
- Skill keeps strategy planning and skill hardening out of memory upkeep.
- Skill-system validators pass.
