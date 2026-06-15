---
kind: skill-audit
skill: learning-drain
status: complete
created_at: 2026-06-15
---

# Compatibility Wrapper

## Decision

`learning-drain` is now documented as a compatibility wrapper for legacy
automations that still call it directly.

The canonical weekly skill-upkeep operation is
`skill-maintenance(mode: harden_skill)`. `learning-drain` keeps the
TROUBLES/LESSONS intake, dedupe, cap, pairing, and processed-state behavior,
then emits hardening handoffs.

## Proof Targets

- `learning-drain/SKILL.md` points new weekly upkeep to
  `skill-maintenance(mode: harden_skill)`.
- Legacy automation prompt and eval reference points reflect the wrapper role.
- Skill-system validators pass.
