---
name: storyboard
description: "Turn a content implementation plan, idea, ICP, proof, or offer into script, beats, and storyboard scenes for production handoff."
tier: 3
group: content-video
source: local
template_uses:
  skill-template: "0.3.7"
  skill-qa-checklist: "0.1.1"
  skill-eval-task: "0.1.0"
  skill-surface-budget: "0.1.0"
eval: eval_task.json
qa_checklist: qa_checklist.md
common_chains:
  after: ["asset-advisor", "audio-advisor", "avatar-advisor", "remotion", "social-content"]
allowed-tools: Read, Grep, Glob, Bash
---

# Storyboard

## Context

Use this skill when a content implementation plan, creative idea, proof point,
offer, or campaign goal needs script, beats, and storyboard scenes before
production. It is a child primitive of `content-impl-plan`: it turns the chosen
idea and reference pattern into narrative signatures, beat structure, scene
requirements, and production-facing shot notes.

This skill owns narrative and scene design. It does not own the parent content
implementation ticket, asset decomposition, media generation, Remotion code,
publishing, or final creative QA. Route parent planning to `content-impl-plan`
and production-specific work to the relevant advisor or Remotion skill.

## Skill Signature

```text
storyboard(idea_or_brief, icp?, proof?, platform?, duration?, style?, cta?, reference_pattern?, artifact_owner?)
  -> script_storyboard + scene_handoff | blocked_report

state:
  reads(user brief, supplied proof/examples/swipes, active ticket?,
        qa_checklist.md, examples/remotion-proof-video/example.md when useful)
  writes(storyboard artifact or content-ticket section when durable output is requested)

gates:
  viewer_promise_bound; proof_or_reason_to_believe_named;
  narrative_signatures_present; beat_sheet_and_script_aligned;
  storyboard_executable; asset_needs_named; scene_handoff_observable

routes:
  content-impl-plan | asset-advisor | audio-advisor | avatar-advisor |
  remotion | ai-video-advisor | social-content | review

fails:
  vague_video_idea_as_plan; script_without_shots; shots_without_viewer_promise;
  generic_brand_filler; parent_action_list_hidden_in_storyboard;
  production_handoff_without_assets_or_proof;
  publishing_or_rendering_as_default
```

## Phase Boundary

Plan inline by default. Use `content-impl-plan` when the user needs the parent
ticket, advisor action list, and execution order. Use `research` only when current platform norms, peer
examples, official specs, or source material materially affect the script. Use
`review` when a material creative plan needs independent judgment before
production. Hand off to production skills only after this skill has named the
scene handoff, asset needs, proof, and blocker conditions.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the creative ticket inputs.
  - [ ] Resolve or state assumptions for ICP, viewer promise, core idea, proof
    or reason to believe, platform, duration, style, CTA, constraints, and
    artifact owner.
  - [ ] Read `qa_checklist.md` as preflight guardrails.
- [ ] 2. Choose the artifact home.
  - [ ] Use `tickets/TASK-XXXX/artifacts/storyboard.md` when an active
    ticket owns the work.
  - [ ] Use `.farplane/content/<date>-<slug>/storyboard.md` for a fast
    proof run without an owning ticket.
  - [ ] Keep chat-only output only for tiny sketches where no production or
    review handoff is expected.
- [ ] 3. Draft the narrative spine.
  - [ ] Include `Narrative Signatures`: hook, tension, turn, proof moment,
    payoff, and final action.
  - [ ] If the user needs a full ticket/action list, route back to
    `content-impl-plan` instead of expanding this skill's scope.
- [ ] 4. Write the script and storyboard as one connected plan.
  - [ ] Produce beat sheet, voiceover or on-screen copy, scene-by-scene
    storyboard panels, shot list, motion notes, audio notes, captions or
    supers, and asset requirements.
  - [ ] Ensure each beat has a viewer job and each shot has a production job.
- [ ] 5. Select the production route.
  - [ ] Route parent ticket/action-list planning to `content-impl-plan`.
  - [ ] Route asset decomposition and recreation planning to `asset-advisor`.
  - [ ] Route persistent presenter or character direction to `avatar-advisor`.
  - [ ] Route voice, music, SFX, Foley, and mix notes to `audio-advisor`.
  - [ ] Route deterministic motion graphics, captions, overlays, and editing to
    `remotion`.
  - [ ] Route model-native footage or generated clips to
    `ai-video-advisor`.
  - [ ] Route broader video planning or ad deliverables to `video-production`.
  - [ ] Route captions, launch copy, thread, carousel, or platform copy to
    `social-content`.
- [ ] 6. Make proof and review observable.
  - [ ] Name render, still-frame, storyboard-review, script-review, or
    production-handoff evidence.
  - [ ] Apply `qa_checklist.md` again before calling the plan production-ready.
  - [ ] Use `review` for material campaign claims, high-visibility output, or
    taste-sensitive plans that will guide real production.
- [ ] 7. Output the handoff without doing production by default.
  - [ ] Return the artifact path or inline creative ticket, the selected
    production route, required assets, proof contract, blockers, and next owner.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

Storyboard core:

```text
Narrative Signatures:
- Hook:
- Tension:
- Turn:
- Proof moment:
- Payoff:
- Final action:

Beat Sheet:
1.

Script:
- Scene 1:

Storyboard:
| Scene | Time | Visual | Copy/VO | Motion | Assets | Proof |
| --- | ---: | --- | --- | --- | --- | --- |

## Notes
- Rejected angles:
- Taste notes:
- Blockers:
```

Short positive example: load
`examples/remotion-proof-video/example.md` when the task needs a concrete model
of a Remotion-ready creative ticket.

## Gotchas

- Do not output only a premise, angle, or theme when the user needs production.
  The plan must include beats, script, storyboard panels, asset needs, and
  proof.
- Do not separate script quality from shot feasibility. If the copy implies a
  visual, name the shot or asset; if the shot carries the point, name the copy
  or viewer job.
- Do not claim platform-native quality without current platform evidence,
  supplied examples, or an explicit local-only assumption.
- Do not render, publish, post, upload, or spend external compute unless the
  user explicitly asks for that next action.

## Reference Map

- `qa_checklist.md` - read at start and finish for storyboard QA.
- `examples/remotion-proof-video/example.md` - load when a Remotion-ready
  example would improve the creative ticket or proof handoff.
- `../video-production/SKILL.md` - route broader video planning, ad specs, or
  production method selection after the storyboard is ready.
- `../remotion/SKILL.md` - route deterministic composition authoring after the
  storyboard names dimensions, duration, assets, scenes, and proof.
- `../social-content/SKILL.md` - route captions, launch copy, threads,
  carousels, or platform distribution drafts after production planning.

## Output

- `script_storyboard`: narrative signatures, beats, script, scenes, shots, and
  visual/audio notes.
- `scene_handoff`: selected route, required assets, scene map, proof
  contract, and next owner.
- `blocked_report`: missing ICP, proof, platform, asset permission, production
  route, or review/proof condition.
