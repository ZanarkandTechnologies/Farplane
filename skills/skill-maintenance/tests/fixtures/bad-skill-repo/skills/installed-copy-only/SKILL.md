---
name: installed-copy-only
description: "Fixture skill where the desired behavior is assumed to exist only in an installed copy, not the repo source."
tier: 2
source: local
---

# Installed Copy Only

## Context

This fixture simulates the case where an operator points at an installed skill
copy and asks `skill-maintenance` to patch it directly.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Treat this fixture as repo source in a temp sandbox only.
- [ ] 2. Require a dry-run import or explicit source-owner decision before
  replacing repo-owned files from an installed copy.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

None.

## Gotchas

- Do not edit live `~/.codex/skills/*` as the durable source of truth.

## Reference Map

None.

## Output

Source-owner decision and validation plan.
