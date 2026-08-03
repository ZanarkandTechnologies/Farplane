---
name: editing-advisor
description: "Turn a brief, storyboard, timing master, and reusable editing patterns into a compatible timed edit direction and renderer-ready handoff."
tier: 3
group: content-video
source: local
template_uses:
  skill-template: "0.3.9"
  skill-qa-checklist: "0.1.1"
  skill-eval-task: "0.2.0"
  skill-surface-budget: "0.1.0"
eval: evals/evals.json
qa_checklist: qa_checklist.md
methods:
  - editing-advisor:structure
  - editing-advisor:pacing
  - editing-advisor:motion
  - editing-advisor:transitions
  - editing-advisor:captions
  - editing-advisor:compositing
common_chains:
  after: ["content-impl-plan", "video-production", "storyboard", "asset-advisor", "remotion", "review"]
allowed-tools: Read, Grep, Glob, Bash
---

# Editing Advisor

## Context

Use this skill when a video or motion deliverable needs editorial judgment:
which reusable editing patterns fit, how they work together, where they land
on the timing master, and what a renderer must implement and prove. It covers
structure, pacing, motion, transitions, captions, and compositing; choose only
the methods needed for the request.

Resource Bank `editing` CreativeElements are the canonical reusable creative
pattern corpus. Their `goldenRecipe` values are conditioning recipes, not agent
workflow programs. A Brand Kit may carry an approved project or brand snapshot,
and an explicit caller packet may supply patterns for one run. This skill reads
those sources but does not become a second pattern store, mutate the Resource
Bank, or treat skill findings as production recipes. Asset Advisor prepares
source media and selects any image, video, avatar, or audio realization child.
Remotion or another named renderer implements and proves the edit.

Keep Brand Kit policy and creative-pattern records visibly separate. A prose policy
such as “calm captions” or “restrained orange registration” is a constraint in
`BrandPolicyDecision`, not an `EditingPatternDecision`. Put a Brand Kit item
in the pattern table only when it is a complete CreativeElement with its own
provenance, description, why, golden example, and golden recipe.

The creative-pattern decision table contains only actual retrieved, caller-supplied,
or named-but-incomplete CreativeElement candidates. Never promote an
advisor-authored operation, an inference from the brief, or a policy-derived
operation into that table, and never attribute it to the user. Put those moves
in `OriginalEditDirection` and the ordered recipe with provenance
`advisor_authored_from_brief`; they may be executable without pretending to be
stored reusable patterns.

## Skill Signature

```text
editing_advisor(brief, storyboard?, timing_master?, brand_kit?, editing_elements?, project_id?, renderer?, methods?, constraints?, artifact_owner?)
  -> editing_direction_packet + selected_patterns
   + ordered_edit_recipe + renderer_handoff | blocked_report

state:
  reads(user brief, storyboard/scene map, timing-master media or cue sheet,
        Resource Bank editing elements, optional Brand Kit editing snapshot,
        explicit creative-pattern packets, qa_checklist.md)
  writes(ticket-scoped editing direction packet only when durable execution is requested)

gates:
  source_provenance_visible; complete_selected_patterns;
  compatibility_decisions_explicit; one_timing_basis;
  ordered_recipe_complete; asset_child_selection_owner_explicit;
  renderer_handoff_observable

routes:
  content-impl-plan | video-production | storyboard | asset-advisor |
  remotion | review | qa

fails:
  vibes_only_editing; title_only_pattern_handoff; brand_kit_as_corpus;
  skill_findings_as_production_recipes; incompatible_pattern_pile;
  transition_spam; random_motion; multiple_timing_masters;
  editing_lane_selects_asset_realization_child;
  renderer_handoff_without_observable_proof
```

Resolve missing creative-pattern context from the Resource Bank when its adapter is
available. Otherwise use complete caller-supplied elements or return an exact
retrieval blocker; never invent a remembered recipe. Load
[Resource Bank retrieval](references/resource-bank-retrieval.md) when discovery,
provenance, or source precedence matters.

## Provisional and Repair Responses

Do not answer an executable editing request with only a missing-input list,
policy recap, or empty packet schema. Compile the strongest honest packet before
isolating blockers:

- If exact timestamps are missing, choose one declared provisional basis such
  as `scene_local_normalized`, `cue:<spoken phrase>`, or a clearly labeled FPS
  assumption. Emit relative entry/hold/exit ranges and the exact measurement
  that will replace them. Provisional timing blocks final readiness, not useful
  recipe compilation.
- Use that one basis in every recipe row. Do not mix seconds, frames,
  normalized scene ranges, and verbal cues as peer timing coordinates. If a
  conversion is useful, put it in labeled `derived_display` metadata and name
  the FPS/source; the canonical `time_or_frames` field remains single-basis.
- If a creative-pattern packet is incomplete, inspect the available Resource Bank
  adapter. Record `retrieval_attempted`, the exact adapter/runtime result, and
  a `block` decision containing planned use, compatibility criteria, and the
  missing fields. Never merely say to search later.
- `retrieval_attempted: true` is permitted only after an observable adapter or
  command call. If no adapter exists in the run, record
  `retrieval_attempted: false`, the unavailable adapter/runtime, and the exact
  recovery route. Never call a conceptual search an attempt.
- Every request for reusable patterns returns one search receipt:
  `selected_fit` with explicit pattern decisions, `searched_no_fit` with the
  checked corpus and reason no pattern improves the edit, or `adapter_blocked`
  with the unavailable runtime and recovery route. An empty decision table
  without this receipt is not a completed search.
- When a voiceover or measured voice cue sheet is part of the brief, it is the
  canonical timing master. A scene-local normalized basis is only provisional
  while that voice asset is missing and cannot replace the required voice-led
  remap before renderer readiness.
- If the user describes a simple motion or transition directly, distinguish
  its state function and emit concrete bounded parameters—target layer,
  transform/opacity/easing or spring behavior, duration/normalized range, and
  restraint—without pretending those parameters came from a missing reusable
  stored pattern.
- If accepted files are missing, keep file-dependent operations blocked but
  still emit their dependency-aware positions in the recipe, owner routes, and
  proof checks. Give every dependency an `expected_output_path` and keep
  `accepted_file_ref: null` until inspected. If no artifact owner can determine
  the path, mark `expected_output_path: blocked_artifact_owner` explicitly.
  Do not let missing assets erase the edit plan.
- Always say the named renderer owns implementation and rendered proof. Require
  representative still frames plus the relevant rendered ranges; captions add
  safe-zone/readability checks, transitions add before/during/after checks,
  motion adds target-layer and reduced-motion checks, and compositing adds
  alpha/edge/layer-order checks.

Every recipe row must repeat `renderer_owner`; a global renderer note is not a
substitute. When deterministic timeline assembly is requested and the caller
does not name a renderer, select `remotion` as the provisional implementation
owner and expose that assumption. Use `renderer_unresolved` only when Remotion
is unavailable or the requested operation requires a different provider.

## Method Contract

| Method | Owns | Required evidence |
| --- | --- | --- |
| `editing-advisor:structure` | assembly order, scene boundaries, narrative compression, state handoffs | storyboard or source sequence and intended viewer-state change |
| `editing-advisor:pacing` | beat duration, holds, cut rhythm, reveal density | one measured timing master or explicit `none` |
| `editing-advisor:motion` | frame-addressed transforms, springs, parallax, tactile cadence | target layer, purpose, parameters, and reduced-motion or restraint rule |
| `editing-advisor:transitions` | continuity or contrast across scene changes | state before/after and reason the transition serves that change |
| `editing-advisor:captions` | phrase timing, hierarchy, safe zones, readability | transcript/cues, platform frame, and audio coordination |
| `editing-advisor:compositing` | layer order, masks, blends, overlays, prepared-media treatment | accepted asset refs or explicit blockers plus final-frame proof plan |

Methods are executable advisory procedures, not storage buckets. One creative
pattern may inform several methods, but it remains one provenance-bearing
Creative Element record.

## Creative Pattern and Edit Recipe Contract

Preserve each candidate as a complete realization packet:

```text
EditingPatternDecision {
  element_id?
  title
  source_kind             # resource_bank | brand_kit | explicit
  provenance
  description
  whyItWorks
  goldenExample
  goldenRecipe
  anchor?
  tags[]
  decision                # use | adapt | reject | block
  planned_use_or_nonuse
  compatibility_note
  acceptance_check
}

BrandPolicyDecision {
  policy
  source_ref
  effect_on_edit
  affected_patterns[]
  acceptance_check
}

OriginalEditDirection {
  direction
  provenance             # advisor_authored_from_brief
  brief_or_policy_basis
  planned_use
  restraint_rule
  acceptance_check
}

OrderedEditStep {
  order
  time_or_frames
  scene_or_state
  method
  operation
  parameters
  dependencies[]
  pattern_ref?
  renderer_owner
  acceptance_check
}

AssetDependency {
  need
  expected_output_path
  accepted_file_ref
  asset_lane_owner          # asset-advisor
  child_selection_owner     # asset-advisor
  possible_child            # ai-image | ai-video | avatar | audio
}
```

A selected pattern without both a resolved golden example and golden recipe
is `block`, not a license to improvise. Brand policy wins conflicts. A Brand Kit
snapshot can approve or constrain a pattern, but Resource Bank remains the
cross-project source of reusable creative-pattern truth.

## Phase Boundary

Plan inline by default. Route missing source-media preparation to
`asset-advisor`, including sound or model-native clip dependencies; Asset
Advisor selects any generation child. Route deterministic assembly to
`remotion`, and material or close-reference direction to independent `review`.
Do not render or generate provider media inside this skill.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the brief, storyboard or source sequence, renderer, constraints,
  platform/frame, and one timing master.
  - [ ] Read `qa_checklist.md` as preflight guardrails.
- [ ] 2. Retrieve editing patterns from the Resource Bank or bind complete
  caller-supplied/Brand Kit packets.
  - [ ] Preserve provenance, description, why, golden example, golden recipe,
    anchor, and tags; block incomplete selected packets.
  - [ ] Return exactly one pattern search receipt: `selected_fit`,
    `searched_no_fit`, or `adapter_blocked`.
- [ ] 3. Select only the necessary methods and diagnose the edit.
  - [ ] Name the viewer-state changes, pacing problem, continuity needs,
    caption constraints, motion purpose, and compositing dependencies that
    actually apply.
- [ ] 4. Decide every candidate as `use`, `adapt`, `reject`, or `block`.
  - [ ] Test brand fit, story function, timing fit, asset feasibility,
    renderer feasibility, accessibility, and compatibility with other selected
    patterns. Prefer one coherent edit grammar over a pile of effects.
  - [ ] Keep prose Brand Kit policies in a separate policy table; promote only
    complete Brand Kit CreativeElements into the pattern decision table.
  - [ ] Keep advisor-authored and brief-inferred operations in
    `OriginalEditDirection`, never in the reusable-pattern table.
- [ ] 5. Compile the `editing_direction_packet`.
  - [ ] State the editing thesis, timing basis, method choices, pattern
    decisions, restraint rules, and falsifiable quality checks.
- [ ] 6. Emit one frame- or time-addressed ordered edit recipe.
  - [ ] Every step names scene/state, method, operation, usable parameters,
    dependencies, pattern ref, renderer owner, and acceptance check.
  - [ ] When exact timing or files are unresolved, emit a provisional recipe
    with relative cue/scene anchors and dependency blockers instead of stopping
    at a request for inputs.
- [ ] 7. Resolve cross-owner dependencies.
  - [ ] Return every unprepared media dependency—including sound and
    model-native clips—to the Asset Advisor lane. Do not select generation
    children from the editing lane; state explicitly that Asset Advisor owns
    any Audio Advisor or AI Video Advisor child selection.
  - [ ] Emit `asset_lane_owner: asset-advisor` and
    `child_selection_owner: asset-advisor` on every unresolved media
    dependency instead of drawing direct Editing Advisor-to-generator arrows.
- [ ] 8. Hand off to the renderer with observable proof.
  - [ ] Include accepted files or blockers, composition/layer order, timing,
    captions, transitions, motion parameters, output spec, and frame/range or
    render checks. A recipe alone is not rendered proof.
- [ ] 9. Apply `qa_checklist.md` again and route material direction to
  independent review before claiming readiness.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Example

```text
Editing thesis: Preserve exact state continuity while giving evidence beats a
restrained tactile cadence.

- use `exact-state handoffs`: scene 03 begins from scene 02's accepted end
  frame; reject a decorative wipe because no viewer-state change supports it.
- adapt `8 FPS tactile page cadence`: apply only to paper layers at 3-frame
  holds while captions and camera motion remain full-rate for readability.
- renderer step 12: frames 184-207, page layer, posterize held transforms to
  8 FPS; keep caption layer continuous; inspect frames 184, 195, and 207 and
  the rendered transition range.
```

## Gotchas

- Do not copy conditioning recipes into this skill whenever a new Vox creative
  pattern is learned; ingest the selected pattern as a Resource Bank `editing`
  element and retrieve it. Promote only reusable branching/tool/proof behavior
  into a skill method.
- Do not call every animated visual a transition. Transitions describe change
  between states; motion may happen inside one state.
- Do not prescribe vague “dynamic pacing.” Name durations, holds, cut/reveal
  logic, and the timing evidence that makes them executable.

## Reference Map

- `references/resource-bank-retrieval.md` - load for creative-pattern discovery,
  source precedence, current adapter commands, or retrieval blockers.
- `qa_checklist.md` - read at start and finish for runtime guardrails.
- `../content-impl-plan/SKILL.md` - parent production-plan route and complete
  element realization packets.
- `../asset-advisor/SKILL.md` - source-media discovery, preparation, and
  acceptance.
- `../audio-advisor/SKILL.md` - child audio realization contract selected by
  Asset Advisor when the edit declares an audio dependency.
- `../ai-video-advisor/SKILL.md` - child model-native video contract selected
  by Asset Advisor when the edit declares a clip dependency.
- `../remotion/SKILL.md` - deterministic implementation and render proof.

## Output

Return a concise editing direction packet, complete creative-pattern decision table,
ordered edit recipe, cross-owner blockers, and renderer handoff. When durable
execution is requested, write it under the active ticket or caller-supplied
artifact owner; do not create a parallel global creative-pattern library.
