---
name: script-storyboard
description: "Turn a content idea, ICP, proof, or offer into a ticket-shaped script and storyboard plan when production needs an executable creative handoff."
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
  after: ["video-production", "remotion", "social-content"]
allowed-tools: Read, Grep, Glob, Bash
---

# Script Storyboard

## Context

Use this skill when a creative idea, proof point, offer, or campaign goal needs
to become an executable script and storyboard before production. It is the
content-production analogue of `impl-plan`: it turns fuzzy intent into a
ticket-shaped creative plan with narrative signatures, beat structure, shot
requirements, asset needs, and a proof contract.

This skill owns planning and production handoff. It does not render video,
generate model-native footage, publish social posts, run accounts, or claim
final creative quality after production. Route production to `remotion`,
`video-production`, `video-generation`, `remotion-render`, or `social-content`
after the handoff is concrete enough to execute.

## Skill Signature

```text
script_storyboard(idea_or_brief, icp?, proof?, platform?, duration?, style?, cta?, artifact_owner?)
  -> creative_ticket + production_handoff | blocked_report

state:
  reads(user brief, supplied proof/examples/swipes, active ticket?,
        qa_checklist.md, examples/remotion-proof-video/example.md when useful)
  writes(ticket artifact or experiment content artifact when durable output is requested)

gates:
  viewer_promise_bound; proof_or_reason_to_believe_named;
  narrative_signatures_present; beat_sheet_and_script_aligned;
  storyboard_executable; asset_plan_named; production_route_selected;
  proof_contract_observable

routes:
  research | video-production | remotion | video-generation |
  remotion-render | social-content | review

fails:
  vague_video_idea_as_plan; script_without_shots; shots_without_viewer_promise;
  generic_brand_filler; production_handoff_without_assets_or_proof;
  publishing_or_rendering_as_default
```

## Phase Boundary

Plan inline by default. Use `research` only when current platform norms, peer
examples, official specs, or source material materially affect the script. Use
`review` when a material creative plan needs independent judgment before
production. Hand off to production skills only after this skill has named the
route, assets, proof, and blocker conditions.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the creative ticket inputs.
  - [ ] Resolve or state assumptions for ICP, viewer promise, core idea, proof
    or reason to believe, platform, duration, style, CTA, constraints, and
    artifact owner.
  - [ ] Read `qa_checklist.md` as preflight guardrails.
- [ ] 2. Choose the artifact home.
  - [ ] Use `tickets/TASK-XXXX/artifacts/script-storyboard.md` when an active
    ticket owns the work.
  - [ ] Use `experiments/content/<date>-<slug>/script-storyboard.md` for a fast
    proof run without an owning ticket.
  - [ ] Keep chat-only output only for tiny sketches where no production or
    review handoff is expected.
- [ ] 3. Draft the ticket-shaped creative plan.
  - [ ] Use `Summary`, `Scope`, `Delta`, `Program`, `Map`, `Done / Proof`,
    `State`, `Links`, and `Notes`.
  - [ ] In `Delta`, make the before/after explicit: fuzzy idea to executable
    production plan.
  - [ ] Include `Narrative Signatures`: hook, tension, turn, proof moment,
    payoff, and final action.
- [ ] 4. Write the script and storyboard as one connected plan.
  - [ ] Produce beat sheet, voiceover or on-screen copy, scene-by-scene
    storyboard panels, shot list, motion notes, audio notes, captions or
    supers, and asset requirements.
  - [ ] Ensure each beat has a viewer job and each shot has a production job.
- [ ] 5. Select the production route.
  - [ ] Route deterministic motion graphics, captions, overlays, and editing to
    `remotion`.
  - [ ] Route model-native footage, avatars, or generated clips to
    `video-generation`.
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

Creative ticket core:

```text
## Summary
What will be produced, for whom, and why this artifact should exist now.

## Scope
- In:
- Out:
- Platform:
- Duration:
- Style:
- CTA:

## Delta
- Before:
- After:
- Why now:

## Program
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

## Map
- Production route:
- Asset route:
- Distribution route:

## Done / Proof
- done_when:
- evidence:
- residual_risk:

## State
draft | review | approved | in_production | blocked

## Links
- source proof:
- examples:
- production:
- outputs:

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

- `qa_checklist.md` - read at start and finish for script-storyboard QA.
- `examples/remotion-proof-video/example.md` - load when a Remotion-ready
  example would improve the creative ticket or proof handoff.
- `../video-production/SKILL.md` - route broader video planning, ad specs, or
  production method selection after the script-storyboard is ready.
- `../remotion/SKILL.md` - route deterministic composition authoring after the
  storyboard names dimensions, duration, assets, scenes, and proof.
- `../social-content/SKILL.md` - route captions, launch copy, threads,
  carousels, or platform distribution drafts after production planning.

## Output

- `creative_ticket`: ticket-shaped script-storyboard artifact or inline packet.
- `production_handoff`: selected route, required assets, scene map, proof
  contract, and next owner.
- `blocked_report`: missing ICP, proof, platform, asset permission, production
  route, or review/proof condition.
