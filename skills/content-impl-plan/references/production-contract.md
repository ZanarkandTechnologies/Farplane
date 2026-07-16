---
title: Content Implementation Production Contract
status: active
owner: content-impl-plan
kind: reference
created_at: 2026-07-16
updated_at: 2026-07-16
---

# Content Implementation Production Contract

Load this reference after binding the implementation brief and before compiling
the production ticket. It owns Resource Bank interpretation, visual-direction
composition, creative lock detail, and the full ticket template.

## Production Graph

```text
idea + content_kind + method + style_profile? + inspiration_pack?
  -> video-production: method and reusable visual direction
  -> storyboard: narrative, script, beats, scene map and scene packets
  -> asset/avatar/audio/image/video advisors: production-ready inputs
  -> audio-generation: approved voice, music, or SFX assets
  -> remotion: stitching, transitions, captions, audio placement, render proof
  -> review/qa: plan, asset, render, and output evidence
```

Style profiles and Inspiration Packs are separate inputs. A profile supplies
creator-neutral aesthetic and motion grammar; Inspiration supplies task facts,
approved source assets, and task-specific motifs. Invocation constraints win.
Incompatible hard constraints return a blocked report rather than a silent
blend.

## Resource Bank And Readiness

```text
{
  request: { idea?, timeframe, startAtMs?, endAtMs?, filters },
  captures: [{ captureId, source, analysis, elements }],
  meta: { captureCount: number, timeframe: string }
}
```

Consume `captures[].source`, `captures[].analysis`, and
`captures[].elements`; tags/facets live on `capture.source`. Build the
`reference_leverage_map` from creative elements, prioritize pinned elements,
and use `analysis.operatorNote` to understand taste. If warnings say an
operator note exists but nothing from it was pinned, state the gap. Extract
structure without copying protected assets, likenesses, music, or exact
expression.

```text
reference_readiness(pack)
  -> media_ready | regen_ready | semantic_only | blocked

media_ready: pinned visual/audio/editing elements have resolved media refs.
regen_ready: pinned elements have enough anchors for concrete advisor packets.
semantic_only: taste descriptions exist but no reusable media or generation
               packet; usable for planning, not final-production claims.
blocked: required evidence, rights, or usable inputs are missing.
```

Do not require separate evidence objects, lane taxonomy, serialized production
patterns, or frame records unless direct reuse or audit proof needs them.

## Creative Lock

```text
creative_lock(idea, visual_direction, inspiration_pack?, storyboard, asset_plan, audio_plan)
  -> locked_brief | blocked_report
```

Requires:

- resolved `method_default`, `profile_only`, `inspiration_only`, or
  `composed_direction`, with supplied-profile compatibility checked;
- a reference leverage map and reference classification when Inspiration is
  supplied;
- hook → tension → turn → proof → payoff, exact copy/VO beats, and viewer job;
- recurring character or explicit no-character rationale, useful recurring
  motif/object, cause/effect, and viewer question → answer;
- asset manifest and a media/regeneration/nonuse decision for each used pinned
  element;
- frame/time-coded cue sheet and required motion bindings;
- `continuous_chain`, `deliberate_scene_breaks`, or `montage` topology;
- start/end frame pairs for chained clips, or one approved scene-grid packet per
  deliberate-break clip using
  `../../video-production/references/scene-grid-production.md`;
- an overview plus actual grids and notes for human review before generation;
- complete scene packets with existing, dimension-verified clean-grid and
  annotated-grid image files rather than placeholder filenames, text-only
  panels, or a statement that grids will be created later; text specifications
  may reach `storyboard_draft_ready` but cannot unlock human review or spend;
- user-intent, video-quality, source-honesty, narrative, asset, and audio-motion
  QA gates, plus Inspiration-use checks when Inspiration exists.

Blocks when the method/profile conflict, Inspiration and profile hard
constraints conflict, an inspiration-led plan has only generic cards, audio has
no edit/motion obligations, a narrative clip batch has neither continuous
handoffs nor deliberate scene packets nor montage rationale, pinned elements
have no media/regeneration route, or proof checks only renderability.

When named Inspiration elements appear in the brief but their capture payload
is unavailable, build a provisional element-level leverage map from those
named elements and mark the missing capture IDs/pins/rights as blockers. Do not
substitute category-only placeholders for the map.

## Ticket Template

```text
## Summary
What will be produced, for whom, and what proof or marketing job it must do.

## Scope
- In / Out:
- Platform / target artifact:
- Content kind / method / visual direction / style profile:
- Reference / Inspiration Pack / CTA:

## Delta
- Before / After / Why now:

## Program
Reference Pattern:
- Visual direction / style profile:
- Hook stack / timeline / story format:
- Visual / audio / motion-edit patterns:
- Proof mechanism / must change:

Reference Leverage Map:
| Capture / Element | Anchor | Reused As | Planned Output | Acceptance Check |
| --- | --- | --- | --- | --- |

Scene Grid Review Packet:
| Scene | Target seconds | Clean grid | Annotated grid | Notes | Provider strategy | Transition / audio | Approval |
| --- | ---: | --- | --- | --- | --- | --- | --- |

Advisor Action List:
| Order | Owner | Input | Output | Acceptance Check | Blocker |
| ---: | --- | --- | --- | --- | --- |

## Map
- Storyboard / Assets / Avatar / Audio:
- Image generation / Video generation / Remotion / Review-QA:

## Done / Proof
- plan_ready_when / production_ready_when:
- render_proof / review / residual_risk:

## State
draft | review | approved | in_production | blocked

## Links
- source proof / reference / child artifacts / outputs:

## Notes
- Rejected angles / rights / taste notes:
```
