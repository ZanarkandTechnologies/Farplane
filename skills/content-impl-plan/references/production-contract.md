---
title: Content Implementation Production Contract
status: active
owner: content-impl-plan
kind: reference
created_at: 2026-07-16
updated_at: 2026-07-22
---

# Content Implementation Production Contract

Load this reference after binding the implementation brief and before compiling
the production ticket. It owns Resource Bank interpretation, visual-direction
composition, creative lock detail, and the full ticket template.

## Production Graph

```text
idea + icp + evidence + brand_kit? + tasty_pack? + invocation_policy
  -> compile_story: causal beats + viewer-state turns + persona lenses
  -> compose_elements: creative hypothesis + chosen/rejected leverage map
  -> choose_assets: jobs + evidence levels + provenance + rights
  -> discover_assets: candidates + rights/fit
     + selected_source | inspiration_for_generation | searched_no_reference
  -> gather_scene_assets: background + main topic + foreground per scene
  -> storyboard: low-fi visual approval packet tied to element ids
  -> select_timing_master: voiceover | music | source_video | none
  -> asset/avatar/audio/image/video advisors: element-conditioned outputs
  -> remotion: timing-master assembly + element leverage receipts
  -> review/qa: plan, asset, render, and output evidence
```

The Brand Kit supplies approved identity, production policy, and prompt truth.
The optional Tasty Pack supplies ad-hoc current inspiration. Invocation policy
still binds the deliverable, but Brand Kit policy wins creative-source conflicts. Compatible
Tasty elements augment the kit by role; incompatible elements are explicitly
rejected or block the plan. `style_profile` is not an input or fallback in this
composition contract. Standalone `video-production` callers retain their
separately owned profile behavior.

```text
compose_elements(brand_kit?, tasty_pack?, idea)
  -> creative_hypothesis + chosen_elements + rejected_elements + leverage_map

ElementRealizationPacket {
  elementId
  provenance: brand_kit | tasty_pack
  kind: format | storyboard | visual | character | audio | editing
  description
  whyItWorks
  goldenExample { assetId, description? }
  goldenRecipe
  plannedUse
  acceptanceCheck
}
```

Every selected element must map to a beat, planned artifact, advisor action, or
production rule. Any child generation handoff must carry the resolved golden
example and golden recipe; title/description-only conditioning cannot pass the
creative lock.

For a repair request, retrieve the selected element by its authoritative ID and
show the repaired packet with its actual stored values. A type signature or
instruction to retrieve later is not a repaired handoff.

When a Tasty Pack exists, make the decision surface visible:

| Element / provenance | Pinned | Decision | Rationale | Planned use or nonuse | Owner / output | Acceptance |
| --- | --- | --- | --- | --- | --- | --- |

List pinned elements first, then every remaining captured element. `unused`
requires a reason; do not hide nonuse in prose.

Use `is_element(value) = independently selectable && independently
conditionable from an example && owned by a recognizable production step`.
Hook folds into the storyboard opening beat; semantic copy folds into
storyboard; subtitle rendering/timing folds into editing; constraints are
production policy or Brand Kit prompt content, not CreativeElement rows.

## Resource Bank And Readiness

```text
{
  request: { idea?, timeframe, startAtMs?, endAtMs?, filters },
  captures: [{ captureId, source, analysis, elements }],
  meta: { captureCount: number, timeframe: string }
}
```

Consume `captures[].source`, `captures[].analysis`, and complete
`captures[].elements`; tags/facets live on `capture.source`. Build the
`element_leverage_map` from Brand Kit snapshots and Tasty Pack creative
elements, prioritize pinned Tasty elements,
and use `analysis.operatorNote` to understand taste. If warnings say an
operator note exists but nothing from it was pinned, state the gap. Extract
structure without copying protected assets, likenesses, music, or exact
expression.

```text
reference_readiness(pack)
  -> media_ready | regen_ready | semantic_only | blocked

media_ready: selected elements have resolved golden-example media refs or
             accepted discovered source files.
regen_ready: selected visual elements have complete example + recipe advisor
             packets plus an Asset Advisor discovery receipt ending in
             inspiration_for_generation or searched_no_reference, or the
             brief explicitly requires generation.
             This state permits the named raster/video generation owner; it
             does not unlock Remotion until generated files are accepted.
semantic_only: taste descriptions exist but no reusable media or generation
               packet; usable for planning, not final-production claims.
blocked: required evidence, rights, or usable inputs are missing.
```

Do not require separate evidence objects, lane taxonomy, serialized production
patterns, or frame records unless direct reuse or audit proof needs them.

## Creative Lock

```text
creative_lock(idea, creative_hypothesis, element_leverage_map, storyboard, timing_master, advisor_receipts)
  -> locked_brief | blocked_report
```

Requires:

- a resolved ICP contract plus decision-relevant persona lenses;
- one point of view plus stakes, a causal spine, and beat-level viewer-state
  changes in a two-column narration/visual script;
- evidence/explanation/soul beat functions and a paid-off opening promise;
- asset decisions with jobs, evidence levels, material identity, motion purpose,
  provenance, rights, and acceptance; wallpaper rejected or quarantined;
- Asset Advisor candidate-discovery receipts for every missing visual, with
  queries, candidate links or asset IDs, rights/fit decisions, and a selected
  file, `inspiration_for_generation`, `searched_no_reference`, or explicit
  generation requirement;
- no custom-created SVG animation assets, SVG/JSX scene illustrations, or
  programmatic vector asset substitutes; provenance-bearing existing SVG media
  remains allowed as static source material;
- one `SceneAssetBundle` per production scene under
  `scene-asset-bundles.md`: genuine shared background, dominant main-topic
  asset, and separate foreground asset, with complete packets and accepted
  files before lock;
- a representative layered frame proving one background world, one dominant
  topic, and one foreground depth/attention layer without a card-grid
  composition;
- thumbnail alternatives for the opening, mechanism, and payoff, plus timed
  animatic silent/mute tests;
- an independent pre-production `PersonaContentReview` passing the thresholds
  in `storytelling-asset-persona.md`;
- Brand Kit policy precedence and explicit choose/augment/reject/block decisions for
  every selected or conflicting Tasty element;
- a creative hypothesis plus exact element leverage map with provenance;
- a low-fidelity demo and visual storyboard image paths/notes tied to element
  IDs, approved before provider spend;
- complete realization packets and output receipts for selected elements,
  including resolved golden example and golden recipe where generation occurs;
- storyboard opening beat -> tension -> turn -> proof -> payoff, exact
  semantic copy/VO beats, and viewer job;
- recurring character or explicit no-character rationale, useful recurring
  motif/object, cause/effect, and viewer question → answer;
- asset manifest and a media/regeneration/nonuse decision for each used pinned
  element;
- selected timing master plus actual media duration/alignment/cue evidence;
- frame/time-coded cue sheet and required motion bindings derived from that
  timing master;
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
  QA gates, plus Brand/Tasty element-use checks when either exists.

Blocks when ICP resolution is generic, a beat does not change viewer state,
metaphor is used as factual proof, wallpaper fills the asset plan, a required
persona concern remains unresolved, any scene lacks a genuine background,
main-topic, or foreground asset, a chart or supplied PNG is treated as a whole
scene, planned paths are treated as accepted files, Tasty elements silently override Brand Kit policy, a selected
element reaches a child without its example and recipe, a reference-led plan has
only generic cards, the timing-master media/cues are missing, final visuals are
generated before a required voice/music/source timing master is measured, a
narrative clip batch has neither continuous handoffs nor deliberate scene
packets nor montage rationale, selected elements have no media/regeneration
route, a visual regeneration route lacks Asset Advisor discovery evidence,
custom SVG/JSX drawings substitute for missing scene assets, or proof checks
only renderability.

When named Tasty Pack elements appear in the brief but their capture payload
is unavailable, build a provisional element-level leverage map from those
named elements and mark the missing capture IDs/pins/rights as blockers. Do not
substitute category-only placeholders for the map.

When a brief names enough elements or roles to compile a provisional plan,
compile them first and isolate missing payload, rights, approval, or media as
specific blockers. Do not return only a generic blocked report.

## Ticket Template

```text
## Summary
What will be produced, for whom, and what proof or marketing job it must do.

## Scope
- In / Out:
- Platform / target artifact:
- Content kind / method / Brand Kit / Tasty Pack:
- Invocation policy / CTA:

## Delta
- Before / After / Why now:

## Program
ICP Contract:
- role/job / context / starting belief / friction / knowledge:
- emotional stake / objection / must-believe-after / desired action:

Story Contract:
- point of view + stakes / backbone / promise-payoff:
- two-column beats with viewer-state before/after:
- evidence / explanation / soul:

Asset Decisions:
| Asset | Beat | Job | Claim | Evidence Level | Material | Motion Purpose | Provenance / Rights | Decision / Acceptance |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

Scene Asset Manifest:
| Scene | Beat | Shared Background | Main Topic | Foreground | Layer / Reveal Order | Source or Generation Packet | Owner | Rights Note | Expected Output | Accepted File | Acceptance Check | Readiness |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

Persona Content Review:
- lenses / acceptance checks / objections / must-see proof:
- comprehension / relevance / trust / action clarity:
- blockers / conflicts / receipt / independent reviewer / verdict:

Creative Hypothesis:
- Why this Brand Kit + selected Tasty Pack combination should work:
- Falsifier / risk:

Element Decisions:
- Chosen / augmented / rejected / conflicting:

Reference Pattern:
- Compiled creative direction:
- Storyboard opening beat / timeline / story format:
- Visual / audio / motion-edit patterns:
- Proof mechanism / must change:

Element Leverage Map:
| Provenance / Element | Why It Works | Golden Example | Golden Recipe | Planned Use | Owner / Output | Acceptance Check |
| --- | --- | --- | --- | --- | --- | --- |

Low-Fidelity Review Packet:
- Demo path:
- Visual storyboard image paths / notes / element IDs:
- Operator approval:

Timing Master:
- kind: voiceover | music | source_video | none
- asset / observed duration / alignment / cue receipt:

SFX Candidate Shortlist:
| Cue | Search Phrase | SoundButtonsWorld Item | Why It Fits | Rights Risk | Status / Fallback |
| --- | --- | --- | --- | --- | --- |

Use `awaiting_operator_download_and_approval` for candidates and
`searched_no_fit` when generation remains the fallback. The agent never
downloads from SoundButtonsWorld.

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
- element realization receipts / timing proof / render proof / review / residual_risk:

## State
draft | review | approved | in_production | blocked

## Links
- source proof / reference / child artifacts / outputs:

## Notes
- Rejected angles / rights / taste notes:
```
