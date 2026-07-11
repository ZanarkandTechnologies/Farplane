---
date: 2026-07-04
change: sync upstream Remotion rules and add Remocn reference
upstream_commit: 5b7a8066b4eed645dae5e26dc6c8ac44650e9109
status: complete
---

# Sync Upstream Remotion Rules And Remocn Reference

## Change

Synced the official Remotion skill `rules/` tree recursively from
`remotion-dev/remotion/packages/skills/skills/remotion`, including nested
`rules/assets`.

Kept Farplane-owned routing in `SKILL.md` and added `references/remocn.md` as
the local branch for Remocn copy-paste component guidance.

## Notable Deltas

- Added upstream `rules/video-layout.md`.
- Added upstream `rules/effects.md`.
- Replaced stale `rules/mapbox.md` with upstream `rules/maplibre.md`.
- Preserved upstream `rules/assets/*.tsx`.
- Added Remocn guidance as a reference, not as a renderer or replacement for
  Remotion composition proof.

## Proof

- `python3 skills/skill-maintenance/scripts/check_skills.py --write`
- `python3 bin/validators/check_doc_refs.py`
