---
template_uses:
  skill-qa-checklist: "0.1.1"
---

# Content Impl Plan QA Checklist

- [ ] `composition-boundary`: The plan accepts `brand_kit?` and `tasty_pack?`
  as its reusable creative inputs. It does not accept, alias, or merge
  `style_profile` in this path; direct standalone `video-production` profile
  behavior stays intact. Brand Kit identity/constraints win conflicts, and
  each Brand/Tasty element considered is marked chosen, augmented, rejected,
  conflicting, or unused with provenance and rationale.
- [ ] `complete-leverage-map`: Every selected element preserves `description`,
  `whyItWorks`, one `goldenExample { assetId, description? }`, and one
  `goldenRecipe`. The `element_leverage_map` ties it to a beat, artifact,
  advisor action, audio/motion cue, copy move, or production rule; incompatible
  Tasty elements are never silently blended.
- [ ] `review-and-realization`: Before provider spend, the plan exposes a
  creative hypothesis, why the combination should work, conflict/reject
  decisions, exact leverage map, low-fi demo, and actual visual storyboard
  image paths plus notes tied to element IDs. Every child generation handoff
  receives provenance, description, why, resolved golden example, golden
  recipe, planned use, and acceptance check; text-only storyboards or
  title/description-only handoffs block `creative_lock`.
- [ ] `timing-and-ownership`: The plan selects `voiceover`, `music`,
  `source_video`, or `none` as timing master before final visual generation and
  orders measurement, cue/storyboard revision, visual generation, and Remotion
  accordingly. Storyboard, asset, avatar, audio, image, video, Remotion,
  review, and QA remain separate owner actions with inputs, outputs, acceptance
  checks, blockers, and topology obligations; spend waits for operator
  storyboard approval.
- [ ] `terminal-proof`: Rights, likeness, music, source, brand, and platform
  risks are named. The terminal path supplies actual timing-master media,
  observed duration/alignment/cues, element realization receipts,
  captions/subtitles, transitions, mix, Remotion render proof, and review/QA
  evidence; isolated narrative clip batches remain blocked unless the locked
  topology is montage.
