---
template_uses:
  skill-qa-checklist: "0.1.1"
---

# Asset Advisor QA Checklist

- [ ] The plan decomposes the reference/storyboard into concrete asset units and
  maps relevant Inspiration Pack `captures[].elements` to asset rows,
  generation routes, source handles, or explicit missing-input blockers,
  prioritizing pinned elements when present. For
  narrative video, it includes continuity assets: character bible or
  no-character rationale, recurring prop/object bible, location/lighting
  anchors, and start/end frame files or blockers for AI-video handoffs.
  Anchored Tasty Pack elements such as contact sheets, frame timestamps, frame
  ranges, thumbnails, clips, audio, or transcripts are resolved into media refs
  or regeneration packets with owner skill, prompt/direction, and acceptance
  checks. Missing visuals have a discovery receipt covering supplied/local and
  Resource Bank/reference media plus suitable external source classes, exact
  queries, candidate links or IDs, rights/fit decisions, and exactly one
  result: `selected_source`, `inspiration_for_generation`, or
  `searched_no_reference`. Inspired generation carries rights-safe reference
  links, independent `usage_role` and `rights_status` values for every
  reference, transferable visual traits, explicit must-not-copy constraints,
  and a `moodboard_traits_accepted_at` receipt that precedes prompt
  compilation. Without an approval source, the Moodboard Decision is
  `pending`, the complete Generation Packets section is
  `blocked_until_moodboard_accepted`, and no generation prompt or prompt-like
  direction is emitted. The discovery receipt itself preserves candidate
  URLs/IDs, owner, expected output path, and acceptance check. After acceptance, the generation
  packet carries prompt/owner/output and an acceptance check. Original generation follows an
  evidenced no-reference result or an explicit generation brief; generation
  never happens merely because it is faster than searching. For layered
  documentary/editorial reels, every overlay has concrete
  media or a blocker plus provenance, rights, dimensions, alpha/background
  suitability, cleanup for levels/edges/loops, expected blend behavior, and an
  acceptance check. Asset Advisor owns this preparation; Remotion owns
  deterministic treatment and compositing.
- [ ] Each asset has a source, decision, owner route, and acceptance check.
  Decisions use `reuse`, `source`, `inspired_generation`,
  `original_generation`, `capture`, or `compose`; generation packets preserve
  prompt, model/owner, inspiration provenance when used, output path,
  rights/likeness notes, and acceptance checks.
  Custom-created SVG animation assets and SVG/JSX/programmatic vector
  substitutes for scene content are rejected. Existing user-supplied,
  brand-owned, licensed, or discovered SVG files are allowed only as
  provenance-bearing static source media.
- [ ] Rights, likeness, brand, platform, duration, and aspect-ratio risks are
  named when relevant. Rights status is never inferred from the source's
  usefulness: cinematic frames and taste galleries remain reference-only or
  per-item/unknown until a production license is verified.
- [ ] Downstream asset handoff includes files or missing-file blockers, scene
  roles, timing-relevant media metadata, and no generic CSS/text-only asset
  substitute for inspiration-led video unless explicitly downgraded. Every generation
  packet remains `blocked_pending_accepted_file` until its expected raster/video
  path exists and the output passes inspection; a prompt or provider result
  alone never unlocks downstream Editing Advisor or Remotion work.
- [ ] The output separates stills, model-native clips, avatar, audio, and
  accepted asset receipts instead of routing everything to one generation skill.
