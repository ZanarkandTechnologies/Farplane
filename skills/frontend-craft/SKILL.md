---
name: frontend-craft
version: 1.1.0
description: "Route frontend build or improvement work through UX, visual design, implementation, assets, standards review, and QA."
tier: 3
group: frontend
source: local
template_uses:
  skill-template: "0.2.0"
  skill-qa-checklist: "0.1.0"
qa_checklist: qa_checklist.md
methods:
  - frontend-craft:composed-scroll-animation
common_chains:
  after: ["visual-qa"]
allowed-tools: Read, Grep, Glob, Bash

---

# Frontend Craft

## Context

`frontend-craft` is the general frontend entrypoint and router. Use it when a
frontend request needs more than one lane, such as workflow shape, visual taste,
component implementation, assets, standards review, browser proof, or visual QA.

This skill should stay small enough to load before work starts. It decides which
frontend lanes to run, what evidence must exist, and which reference to open
after a branch is chosen. Detailed design doctrine, asset recipes, animation
playbooks, and QA checklists belong in downstream skills, references, or
`qa_checklist.md`.

## Skill Signature

```text
frontend_craft(request, target_surface?, repo_context?, proof_need?)
  -> lane_plan + implementation_or_handoff + frontend_proof_summary

state:
  reads(user request, existing UI/source, package/theme facts, relevant refs,
        screenshots/browser evidence when available)
  writes(code/assets when implementing, ticket or final proof notes, QA links)

routes:
  research:user-grounding | functional-ui | visual-design | best-of-worlds |
  frontend-design | landing-page | ai-image-advisor | ai-video-advisor |
  remotion | remotion-render | web-design-guidelines | visual-qa |
  Codex Browser

fails:
  implements before audience/workflow is known; treats a router as a design
  system doc; skips stack facts before adding libraries; claims UI completion
  without rendered proof when the surface is user-visible
```

Program projection: the `## Todo List` below is the executable `steps[]` for
this skill. Do not duplicate it in a separate workflow section; put branch
detail in references only after the branch is chosen.

## Phase Boundary

`frontend-craft` owns routing, composition, and proof expectations for frontend
work. It does not own every niche frontend rule:

- `functional-ui` owns workflow, IA, user stories, and UI states.
- `visual-design` owns visual direction, taste, density, type, color, and
  motion feel.
- `frontend-design` owns settled shadcn, AI Elements, registry, theming, and
  component implementation patterns.
- `landing-page` owns one-page marketing, launch, and hero narrative planning.
- Media skills own generated images, video, Remotion, and rendered assets.
- `web-design-guidelines`, `qa_checklist.md`, `visual-qa`, and ticket QA own
  standards, copy/help checks, rendered evidence, and final UI judgment.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Classify the frontend surface: app screen, workflow component, dashboard,
  AI interface, landing page, portfolio, game/tool, media-heavy page, or
  experimental rendering surface.
- [ ] 2. Use [research:user-grounding](../research/SKILL.md#researchuser-grounding)
  when the user, operator, audience, or job-to-be-done is not already clear.
- [ ] 3. Use [functional-ui](../functional-ui/SKILL.md) when workflow, IA, states,
  or behavior are unclear or broken.
- [ ] 4. Use [landing-page](../landing-page/SKILL.md) before visual design for
  one-page marketing, launch, hero-heavy, cinematic, portfolio, or scrolltelling
  surfaces.
- [ ] 5. Use [visual-design](../visual-design/SKILL.md) when look, taste, visual
  system, density, or motion direction is open.
- [ ] 6. For substantial redesigns or taste-open surfaces, inspect the user's
  references plus 2-4 comparable products or strong examples, then use
  [best-of-worlds](../best-of-worlds/SKILL.md) to decide what to adopt, adapt,
  reject, or defer before implementing.
- [ ] 7. Use the native planning phase to choose lanes, scope cuts, proof surfaces,
  and accepted tradeoffs before implementation.
- [ ] 8. Capture stack facts before importing UI libraries or writing
  framework-specific code: `package.json`, Tailwind/CSS major-version shape,
  component aliases, app/router structure, and existing design-system patterns.
- [ ] 9. Use [frontend-design](../frontend-design/SKILL.md) for shadcn, AI
  Elements, registry, theme, component-state, and app UI implementation
  references. Keep broad app pages server-rendered where the framework expects
  it, and isolate interactive or motion-heavy behavior in client leaf
  components.
- [ ] 10. Route special assets through the owning Tier 3 media skill:
  [ai-image-advisor](../ai-image-advisor/SKILL.md),
  [ai-video-advisor](../ai-video-advisor/SKILL.md),
  [remotion](../remotion/SKILL.md), or
  [remotion-render](../remotion-render/SKILL.md). Capability-gate external
  model CLIs and prefer built-in `imagegen` first for ordinary still assets.
- [ ] 11. For layered generated-media scroll/timed scenes, use
  [composed-scroll-animation](./references/composed-scroll-animation.md) to
  define layers, asset routes, timeline phases, debug hooks, fallback behavior,
  and proof. Use Three.js/WebGL or experimental rendering only with
  accessibility, mobile performance, reduced-motion, and nonblank-frame proof.
- [ ] 12. Use [web-design-guidelines](../web-design-guidelines/SKILL.md) for
  source-fresh UI fundamentals and [visual-qa](../visual-qa/SKILL.md) for
  user-visible visual proof.
- [ ] 13. Use ticket QA with the Codex in-app Browser to collect screenshots,
  snapshots, console/page errors, and route proof.
- [ ] 14. Before completion, apply [qa_checklist.md](./qa_checklist.md) when the
  change includes UI copy, help text, settings/status panels, onboarding,
  tooltips, or developer/operator-facing surfaces.
- [ ] 15. Use the native execution phase for final proof, writeback, and
  handoff before claiming the frontend work is complete.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Use When

- The user says to build or implement a frontend, page, component, app surface, dashboard, or tool UI.
- The request includes both function and look, such as "make this UI good and implement it."
- The target may need shadcn, AI Elements, animation, generated image/video assets, web-interface audit, visual QA, or one-page marketing treatment.

## Do Not Use When

- The user only wants UX/workflow redesign: use `functional-ui`.
- The user only wants look/taste/theming: use `visual-design`.
- The user only wants one-page/landing-page narrative planning: use `landing-page`.
- The user only wants review findings on an existing finished UI: use `web-design-guidelines`, `visual-qa`, or `review` as appropriate.

## Decision Branches

| Request shape | Required route |
| --- | --- |
| "this UI sucks", "redesign this component", broken flow | `functional-ui` first, then `visual-design`, then implementation |
| App, dashboard, AI workflow UI | `functional-ui` if unsettled, `visual-design`, `frontend-design` references |
| Landing page, homepage, launch page, portfolio hero | `landing-page`, JSON recipe/taste/effect records when useful, then `visual-design`, then motion/assets references |
| Visual polish only | `visual-design`, then implementation |
| Complex scroll animation | `landing-page` if narrative; otherwise `motion-routing.md`; use official GreenSock skills or docs for GSAP truth |
| Layered generated-media scroll/timed scene | `composed-scroll-animation.md` when the section needs 6-12 layers, generated/cutout assets, HTML overlays, named phases, debug hooks, and source-frame/checkpoint proof |
| Generated hero/image/texture/reference asset | `asset-generation.md` and `imagegen` |
| Inference.sh image model, background removal, upscaling, or model comparison | `asset-generation.md` and `ai-image-advisor` |
| Generated video, image-to-video, avatar/lipsync, foley, or video edit | `asset-generation.md` and `ai-video-advisor` |
| Deterministic React/Remotion animation or video component | `asset-generation.md`, `remotion` for code, and `remotion-render` for inference.sh MP4 render |
| Three.js, React Three Fiber, WebGL, shader, or 3D scene | `three-js.md`, progressive enhancement, and explicit fallback |
| Canvas/WebGPU/futuristic rendering outside Three.js | `experimental-rendering.md`, progressive enhancement, explicit fallback, and browser-support proof |

## Reference Map

- `references/routing.md` - entrypoint and lane selection.
- `references/architecture.md` - why this is a wrapper-plus-granular topology.
- `references/workflows.md` - common frontend orchestration paths.
- `references/gotchas.md` - load when a frontend review or implementation
  still feels generic, overbuilt, cinematic in the wrong surface, or visually
  padded after the main routing steps are chosen.
- `references/motion-routing.md` - CSS, Motion, GSAP, View Transitions, WebGL/WebGPU.
- `references/asset-generation.md` - native `imagegen`, `ai-image-advisor`, `ai-video-advisor`, `remotion`, `remotion-render`, project-bound assets, external-tool gates.
- `references/media-pipelines.md` - multi-asset website/campaign workflows spanning image, model-native video, Remotion, and frontend QA.
- `references/composed-scroll-animation.md` - method contract for layered
  generated-media scenes with scroll or timed transitions.
- `references/three-js.md` - Three.js/WebGL/R3F routing with links to architecture, planning, workflows, gotchas, and testing refs.
- `references/experimental-rendering.md` - HTML-in-Canvas, Pretext, WebGL/WebGPU, progressive enhancement.
- `references/qa.md` - browser/visual proof expectations.
- `qa_checklist.md` - final frontend checks for audience-facing copy, help
  affordances, tooltip placement, and developer-explainer leakage.
- `references/upstream-sources.md` - pinned upstream repos and what to borrow from each.

## Outcome Contract

When this skill drives implementation, the final output must include:

- The lanes used or skipped, with one-line reasons.
- The stack facts captured before implementation.
- The implementation files changed.
- The validation commands and results.
- The `web-design-guidelines` result or a concrete reason it was skipped.
- The `qa_checklist.md` result or a concrete reason it was skipped when UI
  copy, help text, onboarding, settings/status, or tooltips changed.
- Any generated asset paths and prompts when assets were created.
- A clear handoff to `visual-qa` or ticket QA when UI changed.
