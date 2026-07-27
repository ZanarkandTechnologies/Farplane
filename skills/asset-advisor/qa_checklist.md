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
  queries, candidate links or IDs, rights/fit decisions, and a selected file or
  evidenced `searched_no_fit`; generation never happens merely because it is
  faster than searching. For layered documentary/editorial reels, every overlay has concrete
  media or a blocker plus provenance, rights, dimensions, alpha/background
  suitability, cleanup for levels/edges/loops, expected blend behavior, and an
  acceptance check. Asset Advisor owns this preparation; Remotion owns
  deterministic treatment and compositing.
- [ ] Each asset has a source, decision, owner route, and acceptance check.
  Custom-created SVG animation assets and SVG/JSX/programmatic vector
  substitutes for scene content are rejected. Existing user-supplied,
  brand-owned, licensed, or discovered SVG files are allowed only as
  provenance-bearing static source media.
- [ ] Rights, likeness, brand, platform, duration, and aspect-ratio risks are
  named when relevant.
- [ ] Remotion handoff includes files or missing-file blockers, scene roles,
  timing, captions/overlays, proof expectations, and no generic CSS/text-only
  pass for inspiration-led video unless explicitly downgraded.
- [ ] The output separates stills, model-native clips, avatar, audio, and
  composition work instead of routing everything to one skill.
