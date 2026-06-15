---
kind: skill-audit
skill: skill-maintenance
status: complete
created_at: 2026-06-15
---

# Harden And Refine Modes

## Decision

`skill-maintenance` now owns two weekly skill-upkeep modes:

- `harden_skill`: immediately turns fresh lessons/troubles into evals,
  gotchas, checklist guardrails, or improvement tickets.
- `refine_skill`: later consolidates accumulated evals/gotchas and shortens
  skill surfaces without weakening guardrails.

`learning-drain` remains as a compatibility wrapper for legacy
`docs/TROUBLES.md` / `docs/LESSONS.md` intake, and `self-improve` remains
separate for measured variant/search loops.

## Proof Targets

- `skill-maintenance/SKILL.md` names both modes, routes to `eval` and
  `self-improve` only when warranted, and keeps final skill writeback here.
- `learning-drain/SKILL.md` points new weekly upkeep to
  `skill-maintenance(mode: harden_skill)`.
- Skill-system validators pass.
