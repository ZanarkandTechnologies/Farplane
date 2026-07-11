---
title: Tasty Pack Media Readiness Hardening
status: applied
created_at: 2026-07-07
skills:
  - content-impl-plan
  - asset-advisor
  - remotion
---

# Tasty Pack Media Readiness Hardening

## Behavior Delta

Expected behavior: when a content agent produces an inspiration-led video from a
Tasty Pack, it must carry over the pack's pinned visual/audio/editing atoms as
resolved media refs or regenerated assets before claiming production reuse.

Observed behavior: the agent built a stronger storyboard from pinned elements
but used only semantic descriptions, dropping actual frame/contact-sheet/audio
anchors and producing generic Remotion visuals.

## Changes

- `content-impl-plan` now classifies `reference_readiness` as `media_ready`,
  `regen_ready`, `semantic_only`, or `blocked`.
- `content-impl-plan` creative lock now requires a media-or-regeneration plan
  for pinned visual/audio/editing elements.
- `asset-advisor` now requires `assetId + anchor` resolution or regeneration
  packets for anchored Tasty Pack elements.
- `remotion` now refuses production claims when only semantic Tasty Pack
  descriptions were handed off.

## Proof

- Passed: `python3 skills/skill-maintenance/scripts/check_skills.py --write`
- Passed: focused grep for the new readiness terms across
  `skills/content-impl-plan`, `skills/asset-advisor`, and `skills/remotion`.
- Live skills synced to `/Users/kenjipcx/.codex/skills` for
  `content-impl-plan`, `asset-advisor`, and `remotion`.
