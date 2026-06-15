---
kind: skill-audit
skill: update-strategy
status: complete
created_at: 2026-06-15
---

# Create Update Strategy

## Decision

Created `update-strategy` as the generic project strategy refresh primitive
for PM heartbeats.

It separates the reusable interface from specialized wrappers such as
`weekly-strategy-analysis`, which can prefill Kenji-specific Notion, meeting,
people-signal, Codex-thread, and opportunity-scan sources.

## Proof Targets

- Frontmatter and checklist follow the Farplane skill template.
- Skill routes strategy deltas into tickets, experiments, Goal Advisor
  handoffs, or review rather than hidden execution.
- Skill-system validators pass.
