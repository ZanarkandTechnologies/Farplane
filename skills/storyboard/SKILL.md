---
name: storyboard
description: "Use for \"storyboard this video\", \"plan this reel\", \"write the script\" or \"what assets do we need\": hook, script, scenes, asset plan and edit direction ready to render in HyperFrames."
source: local
department: marketing
template_uses:
  skill-template: "0.6.5"
  skill-eval-task: "0.2.0"
methods:
  - id: storyboard:plan
    class: internal
    output: production-action-graph
  - id: storyboard:script
    class: artifact
    output: hook-script-scenes
  - id: storyboard:assets
    class: artifact
    output: asset-plan
  - id: storyboard:edit
    class: artifact
    output: edit-direction
allowed-tools: Read, Glob, Grep, Bash
---

# Storyboard

## Context

Use this when a reel, explainer, launch clip, or news short needs an approved
production package: work order, hook, script, scenes, per-scene assets, and
timed edit direction, recorded on the active GitHub issue and ready for
HyperFrames (`/hyperframes`) to render. Default runs `plan -> script -> assets
-> edit`; a single requested mode reads earlier accepted outputs, never re-authors them.

It does not render, publish, or spend. Generation belongs to
[ai-image](../ai-image/SKILL.md) and [ai-video](../ai-video/SKILL.md) (audio
and avatar modes too); post captions and platform copy to
[social-content](../social-content/SKILL.md); close-reference or
high-visibility judgment to [review](../review/SKILL.md).

## Skill Signature

```text
storyboard(brief | idea | issue, mode?: plan | script | assets | edit, icp?, proof?, platform?,
           duration?, source_title?, brand_kit?, tasty_pack?, timing_master?, supplied_media?)
  -> storyboard_package { action graph, hook decision?, script, scene map, asset plan, edit recipe,
                          hyperframes handoff } | blocked_report
reads: the active GitHub issue, brief, proof, Brand Kit/Tasty Pack, Resource Bank, supplied media
does: plan orders work; script writes hook/beats/scenes; assets searches and decides; edit times it
writes: the issue (Change Plan + checkpoint in body, receipts as comments), else .farplane/storyboard/<date>-<slug>/
returns: the approved package or exact blockers, and the next owner
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] **N1 — Bind the brief and the durable home.**
  `request -> modes + ICP, promise, proof, platform, duration, style, CTA + home | one narrow question`

  Rule: Pick the modes from the request ("write the script" is `script`, "what
  assets do we need" is `assets`, "storyboard this video" runs all four).
  Record ICP, viewer promise, proof or reason to believe, platform, duration,
  style, CTA, and constraints; infer low-risk fields as `assumption`. The home
  is the active GitHub issue, else `.farplane/storyboard/<date>-<slug>/`.
  Creative sources are only the Brand Kit and an optional Tasty Pack; Brand
  Kit policy wins conflicts. In a public repo the issue carries no client names.

  Assert:
  - An accepted upstream input (approved storyboard, accepted file, approved
    recipe) is consumed as fixed and never turns back into a blocker.
  - Every assumption is labelled; only fields that block production block.
- [ ] **N2 — plan: write the production action graph on the issue.**
  `brief -> Content Production rows in Change Plan + Done / Proof receipts | blocked_report`

  Rule: Load [production contract](references/production-contract.md). Emit
  one row per applicable action with `owner`, `accepted_inputs`,
  `primary_output`, `acceptance_or_blocker`, `next_handoff`: `script` ->
  `assets` -> realization children (`ai-image`, `ai-video`) -> `edit` ->
  HyperFrames -> `review`/`qa`. Receipts go in `Done / Proof`, progress in
  comments. Compile what the brief allows, then isolate exact blockers.

  Assert:
  - No grouped "production" row; each row has one owner and one output.
  - HyperFrames is ordered only after accepted scenes, files, and edit recipe.
- [ ] **N3 — script: run the hook lab before the script.**
  `idea + proof + audience + source_title? -> candidates[10+] + finalists[3+] + winner + first_3_seconds`

  Rule: For short-form, latest-news, title-led, or retention-sensitive work,
  load the [hook lab](references/plain-language-hook-lab.md). Write at least
  ten candidates across at least six lenses, no more than two per lens, then
  at least three finalists compared with the source title on meaning,
  curiosity, accuracy, one breath, and drawable first frame. The display hook
  is at most 8 words: one recognizable actor, one concrete verb, one
  consequence. Block "fund", "funding", "secure", "backing", "back",
  "finance", "guarantee", "support", "unlock", and "get money" in the display
  hook unless the ordinary word is the story; blocked drafts appear only as
  rejected lines with reasons. Bind the winner to the first 3 seconds:
  on-screen copy, VO, visual action, evidence qualifier.

  Example: `"California legislature weighs conditional small-engine phaseout"
  -> "California may stop gas mower sales" + qualifier "proposal, not law"`

  Assert:
  - The winner beats the source title or the source title is kept.
  - Uncertainty survives: a proposal never becomes a signed law.
- [ ] **N4 — script: write narrative, beats, script and scenes as one plan.**
  `hook + ICP + evidence -> narrative signatures + two-column script + scene map + topology`

  Rule: Write hook, tension, turn, proof moment, payoff, final action. Use a
  two-column script (narration | visual) where each beat changes viewer state;
  load [storytelling](references/storytelling-asset-persona.md) for narrative
  or persuasive work and [documentary reel](references/documentary-reel.md)
  for voice-led editorial reels. Every visual scene lists its background,
  main-topic, and foreground assets ([scene bundles](references/scene-asset-bundles.md)).
  Pick `continuous_chain` (start/end frame pairs), `deliberate_scene_breaks`
  (load [scene grids](references/scene-grid-production.md)), or `montage`.

  Assert:
  - Every scene names a concrete, searchable subject per layer; no "B-roll".
  - A chart or supplied PNG is the main topic, never the whole scene.
- [ ] **N5 — assets: search before generating, then decide each asset.**
  `scene map + references -> discovery receipt + decisions + accepted files | blockers`

  Rule: Load [asset plan](references/asset-plan.md). Run the searches now:
  `reuse -> source -> inspired_generation -> original_generation`. Record
  `usage_role` and `rights_status` as separate axes. For inspired generation,
  get the moodboard traits accepted before any prompt is written. Resolve
  timestamped Tasty Pack anchors (`frame_08_28.58s`, `contact_sheet`) to real
  media or a regeneration packet. Route stills to `ai-image`, clips, audio,
  and presenters to `ai-video`.

  Assert:
  - No SVG, JSX, or programmatic-vector stand-in for a scene illustration.
  - Expected outputs are concrete file paths; a prompt or provider job is
    never an accepted file.
- [ ] **N6 — edit: compile the timed edit direction.**
  `scenes + accepted files + timing master + editing elements -> pattern receipt + ordered recipe`

  Rule: Load [edit direction](references/edit-direction.md). Retrieve
  Resource Bank `editing` CreativeElements (golden example plus golden recipe)
  and return one receipt: `selected_fit`, `searched_no_fit`, or
  `adapter_blocked`. Keep `BrandPolicyDecision` separate from
  `EditingPatternDecision`; label own moves `advisor_authored_from_brief`.
  The voiceover or measured cue sheet is the timing master; use one timing
  basis in every row, provisional when needed.

  Assert:
  - A pattern missing its golden example or recipe is `block`, not improvised.
  - Every row names operation, parameters, dependencies, and an acceptance check.
- [ ] **N7 — Hand off to HyperFrames and get approval.**
  `package -> approval packet + hyperframes handoff + next owner | blocked_report`

  Rule: Show the operator the hook decision, scene map (with grids and the
  character card when used), asset plan, and recipe; generation and rendering
  start only after approval. Hand HyperFrames dimensions, fps, duration,
  timing master, accepted file paths, the recipe, and proof frames.

  Assert:
  - This skill never renders, publishes, or spends.
  - The issue holds the package checkpoint and a receipt comment.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Gotchas

- An accurate sentence or shortened headline is not a hook; run the lab.
- Copy that implies a visual names the shot, and vice versa.
- "Original" or "rights-safe" never licenses skipping discovery or drawing
  SVG/JSX; existing licensed SVG files with provenance stay usable.
- ShotDeck, FilmGrab, Pinterest: references, not licensed media.
- Brand Kit prose ("calm captions") is a policy, never a pattern-table row.
- After approval, reuse the exact grids and character references; a provider
  fallback that changes identity voids approval for the affected scenes only.

## Reference Map

- [hook lab](references/plain-language-hook-lab.md) - N3 short-form hooks.
- [production contract](references/production-contract.md) - N2 leverage map, readiness, creative lock.
- [storytelling](references/storytelling-asset-persona.md) - N4 ICP, causal beats, evidence ladder, persona review.
- [scene asset bundles](references/scene-asset-bundles.md) - N4/N5 three-layer manifest and readiness.
- [scene grids](references/scene-grid-production.md) - deliberate breaks, approval, reuse lock.
- [documentary reel](references/documentary-reel.md) and [newsprint](references/newsprint-treatment.md) - those looks.
- [asset plan](references/asset-plan.md) - N5 receipt, ladder, moodboard gate, source roles.
- [edit direction](references/edit-direction.md) - N6 methods, pattern contract, Resource Bank, timing.
- [package template](templates/storyboard.md); examples: [proof video](examples/proof-video/example.md),
  [editorial explainer](examples/editorial-explainer/example.md), [constrained variance](examples/constrained-variance-editorial/example.md).

## Output

```yaml
home: <issue URL> | .farplane/storyboard/<date>-<slug>/storyboard.md  # modes run listed here
action_graph: <rows: owner, accepted_inputs, primary_output, acceptance_or_blocker, next_handoff>
hook_decision: <candidates, finalists, source-title contest, winner, first_3_seconds> | not_applicable
script: <narrative signatures + two-column beats>
scene_map: <scene: time, background, main_topic, foreground, copy/VO, motion, audio, proof>
asset_plan: <discovery receipt, decisions, moodboard state, expected paths, accepted files>
edit_direction: <pattern receipt, policy table, ordered recipe on one timing basis>
hyperframes_handoff: <dims, fps, duration, timing master, files, recipe, proof frames> | blocked
blockers: <exact missing input and owner>
next_owner: hyperframes | ai-image | ai-video | social-content | review | operator_approval
```
