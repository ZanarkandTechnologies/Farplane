---
title: Edit Direction
owner: storyboard
status: active
kind: reference
updated_at: 2026-10-12
---

# Edit Direction

Load this in the `edit` mode. It decides which reusable editing patterns fit,
how they work together, where they land on the timing master, and what
HyperFrames must implement and prove. It never renders or generates media.

```text
edit_direction(brief, storyboard?, timing_master?, brand_kit?, editing_elements?, project_id?, methods?, constraints?)
  -> editing_direction_packet + pattern_search_receipt + ordered_edit_recipe
   + hyperframes_handoff | blocked_report
```

## Methods

Pick only the methods the request needs.

| Method | Owns | Required evidence |
| --- | --- | --- |
| `structure` | assembly order, scene boundaries, compression, state handoffs | storyboard or source sequence and the intended viewer-state change |
| `pacing` | beat duration, holds, cut rhythm, reveal density | one measured timing master or explicit `none` |
| `motion` | frame-addressed transforms, springs, parallax, tactile cadence | target layer, purpose, parameters, restraint or reduced-motion rule |
| `transitions` | continuity or contrast across scene changes | state before/after and why the transition serves that change |
| `captions` | phrase timing, hierarchy, safe zones, readability | transcript/cues, platform frame, audio coordination |
| `compositing` | layer order, masks, blends, overlays, prepared-media treatment | accepted asset refs or blockers plus a final-frame proof plan |

A transition describes change between states; motion happens inside one
state. Do not call every animation a transition, and do not prescribe vague
"dynamic pacing": name durations, holds, cut or reveal logic, and the timing
evidence.

## Sources and precedence

1. Explicit caller constraints and approved Brand Kit policy govern the run.
2. Resource Bank CreativeElements with `kind: editing` are the canonical
   cross-project pattern corpus. Their `goldenRecipe` values condition the
   edit; they are not agent workflow programs.
3. A Brand Kit editing element is an approved project snapshot; it may approve,
   constrain, or pin a Resource Bank pattern but does not replace the corpus.
4. A complete caller-supplied editing element is valid for this run.
5. Skill findings are harness-improvement proposals, never production recipes.

Deduplicate by stable element ID, else normalized title plus provenance;
preserve conflicts instead of merging them. Do not copy a learned pattern into
this skill; ingest it as a Resource Bank `editing` element and retrieve it.

## Resource Bank retrieval

The Resource Bank lives in the bunker checkout (Farplane-UI-v2), module
`convex/modules/resourceBank/`. Direct retrieval when the brief names an
editing need:

```bash
corepack pnpm exec convex run modules/resourceBank/creativeElements:listCreativeElements \
  '{"query":"exact state handoff tactile pacing captions","kind":"editing","projectId":"<project-id>","limit":8}'
```

Broader cross-kind discovery with the editing filter kept explicit:

```bash
corepack pnpm exec convex run modules/resourceBank/retrieval:createTastyPack \
  '{"idea":"35-second evidence-led explainer with tactile editorial motion","kinds":["editing"],"projectId":"<project-id>","limit":8}'
```

Load an approved Brand Kit through `brandKits:getBrandKitForProduction`;
inspect its local signature first because identifiers are runtime state.

Every request for reusable patterns returns exactly one search receipt:
`selected_fit` (explicit decisions), `searched_no_fit` (corpus checked and why
nothing improves the edit), or `adapter_blocked` (unavailable runtime and the
recovery route). `retrieval_attempted: true` only after an observable adapter
or command call; otherwise `false` with the missing runtime. Never invent a
remembered recipe or reconstruct one from a title.

## Decision records

```text
EditingPatternDecision {
  element_id?, title, source_kind: resource_bank | brand_kit | explicit,
  provenance, description, whyItWorks, goldenExample, goldenRecipe, anchor?,
  tags[], decision: use | adapt | reject | block, planned_use_or_nonuse,
  compatibility_note, acceptance_check
}
BrandPolicyDecision {
  policy, source_ref, effect_on_edit, affected_patterns[], acceptance_check
}
OriginalEditDirection {
  direction, provenance: advisor_authored_from_brief, brief_or_policy_basis,
  planned_use, restraint_rule, acceptance_check
}
OrderedEditStep {
  order, time_or_frames, scene_or_state, method, operation, parameters,
  dependencies[], pattern_ref?, renderer_owner: hyperframes, acceptance_check
}
AssetDependency {
  need, expected_output_path, accepted_file_ref: null until inspected,
  asset_owner: storyboard assets, possible_child: ai-image | ai-video | audio | avatar
}
```

- Prose Brand Kit policy ("calm captions", "restrained registration accent")
  is a `BrandPolicyDecision`, never an `EditingPatternDecision`. A Brand Kit
  item enters the pattern table only as a complete CreativeElement.
- The pattern table holds only retrieved, caller-supplied, or
  named-but-incomplete CreativeElements. Advisor-authored or brief-inferred
  moves go in `OriginalEditDirection` with provenance
  `advisor_authored_from_brief`; never attribute them to the user or to a
  stored pattern.
- A selected pattern without both a resolved golden example and golden recipe
  is `block`. Brand policy wins conflicts.
- Test each candidate for brand fit, story function, timing fit, asset and
  renderer feasibility, accessibility, and compatibility with the other picks.
  One coherent edit grammar beats a pile of effects.

## Timing basis

Use one timing basis in every recipe row. When a voiceover or measured voice
cue sheet exists or is required, it is the timing master. Without exact
timestamps, declare one provisional basis (`scene_local_normalized`,
`cue:<spoken phrase>`, or a labelled fps assumption), emit relative
entry/hold/exit ranges, and name the measurement that replaces them. Do not mix
seconds, frames, normalized ranges, and verbal cues as peer coordinates; put
conversions in labelled `derived_display` metadata. A provisional basis blocks
final readiness, not recipe compilation; it cannot replace the voice-led remap
once the voice file exists.

## Provisional and repair responses

Compile the strongest honest packet before isolating blockers; never answer
an executable request with only a missing-input list or an empty schema.

- Missing files: keep file-dependent steps blocked but emit their positions,
  owner routes, `expected_output_path` (or `blocked_artifact_owner`), and
  checks. Every unprepared media dependency, including sound and model-native
  clips, returns to the `assets` mode, which picks any `ai-image` or `ai-video`
  child. The edit lane never selects a generator.
- A simple motion the user describes directly gets concrete bounded parameters
  (target layer, transform/opacity/easing or spring, duration, restraint)
  without pretending they came from a stored pattern.
- Every recipe row repeats `renderer_owner: hyperframes`; a global note is not
  a substitute.

## Proof handoff

HyperFrames owns implementation and rendered proof. Require representative
stills plus the relevant rendered ranges: captions add safe-zone and
readability checks, transitions add before/during/after checks, motion adds
target-layer and reduced-motion checks, and compositing adds alpha, edge, and
layer-order checks. A recipe alone is not rendered proof.

## Example

```text
Editing thesis: keep exact state continuity; give evidence beats a restrained
tactile cadence.
- use `exact-state handoffs` (resource_bank): scene 03 starts from scene 02's
  accepted end frame; reject a decorative wipe, no viewer-state change needs it.
- adapt `8 FPS tactile page cadence`: paper layers only, 3-frame holds;
  captions and camera stay full-rate for readability.
- step 12, frames 184-207, page layer: posterize held transforms to 8 FPS;
  renderer_owner: hyperframes; check frames 184, 195, 207 and the range.
```
