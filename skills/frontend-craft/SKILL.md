---
name: frontend-craft
version: 1.0.0
description: "Turn a frontend build or improvement request into UX planning, visual design, implementation, assets, standards review, and QA."
tier: 3
group: frontend
source: local
methods:
  - frontend-craft:composed-scroll-animation
common_chains:
  after: ["visual-qa"]
allowed-tools: Read, Grep, Glob, Bash
---

# Frontend Craft

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] Classify the frontend surface: app screen, workflow component, dashboard,
  AI interface, landing page, portfolio, game/tool, media-heavy page, or
  experimental rendering surface.
- [ ] Use [research:user-grounding](../research/SKILL.md#researchuser-grounding)
  when the user, operator, audience, or job-to-be-done is not already clear.
- [ ] Use [functional-ui](../functional-ui/SKILL.md) when workflow, IA, states,
  or behavior are unclear or broken.
- [ ] Use [visual-design](../visual-design/SKILL.md) when look, taste, visual
  system, density, or motion direction is open.
- [ ] For substantial redesigns or taste-open surfaces, inspect the user's
  references plus 2-4 comparable products or strong examples, then use
  [best-of-worlds](../best-of-worlds/SKILL.md) to decide what to adopt, adapt,
  reject, or defer before implementing.
- [ ] Use [plan](../plan/SKILL.md) to choose lanes, scope cuts, proof surfaces,
  and accepted tradeoffs before implementation.
- [ ] Capture stack facts before importing UI libraries or writing
  framework-specific code.
- [ ] Use [frontend-design](../frontend-design/SKILL.md) for shadcn, AI
  Elements, registry, theme, component-state, and app UI implementation
  references.
- [ ] Route special assets through the owning Tier 3 media skill:
  [image-generation](../image-generation/SKILL.md),
  [video-generation](../video-generation/SKILL.md),
  [remotion](../remotion/SKILL.md), or
  [remotion-render](../remotion-render/SKILL.md).
- [ ] For layered generated-media scroll/timed scenes, use
  [composed-scroll-animation](./references/composed-scroll-animation.md) to
  define layers, asset routes, timeline phases, debug hooks, and proof.
- [ ] Use [web-design-guidelines](../web-design-guidelines/SKILL.md) for
  source-fresh UI fundamentals and [visual-qa](../visual-qa/SKILL.md) for
  user-visible visual proof.
- [ ] Use [agent-browser](../agent-browser/SKILL.md) or ticket QA to collect
  screenshots, snapshots, console/page errors, and route proof.
- [ ] Use [execute](../execute/SKILL.md) for final proof, writeback, and
  handoff before claiming the frontend work is complete.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

Build production frontends by routing the work through the right frontend brain instead of mixing UX, visual taste, landing-page storytelling, assets, animation, and QA into one blob.

## Use When

- The user says to build or implement a frontend, page, component, app surface, dashboard, or tool UI.
- The request includes both function and look, such as "make this UI good and implement it."
- The target may need shadcn, AI Elements, animation, generated image/video assets, web-interface audit, visual QA, or one-page marketing treatment.

## Do Not Use When

- The user only wants UX/workflow redesign: use `functional-ui`.
- The user only wants look/taste/theming: use `visual-design`.
- The user only wants one-page/landing-page narrative planning: use `landing-page`.
- The user only wants review findings on an existing finished UI: use `web-design-guidelines`, `visual-qa`, or `review` as appropriate.

## Core Workflow

1. **Classify the surface.** Product app, workflow component, dashboard, AI interface, landing/marketing page, portfolio, game/tool, or experimental canvas/rendering surface.
2. **Run functional shape when needed.** Use `functional-ui` when the workflow, IA, user story, states, or component behavior is unclear or broken. Skip only when a recent UX brief already settles those answers.
3. **Ground and synthesize visual direction.** For substantial redesigns or
   taste-open surfaces, inspect the user's references plus 2-4 comparable
   products or strong examples, then use `best-of-worlds` to decide what to
   adopt, adapt, reject, or defer before implementing.
4. **Route special surfaces.** Use `landing-page` for one-page, marketing, launch, cinematic, scrolltelling, or hero-heavy surfaces before visual-design so the page recipe, taste profile, and effect stack can guide the look.
5. **Run visual design.** Use `visual-design` to set register, scene sentence, typography, color strategy, layout rhythm, density, motion taste, and anti-slop constraints. For landing pages, refine this with the selected taste profile.
6. **Capture stack facts.** Before importing UI libraries or writing framework-specific code, inspect `package.json`, Tailwind config/CSS, `components.json`, app router structure, and existing component paths. Record framework/router, Tailwind major version, installed icon/motion/form/chart/AI packages, shadcn aliases, and theme/preset status.
7. **Choose implementation references.** Use `frontend-design` references for shadcn, AI Elements, registries, and app UI construction. Use `motion-routing.md` for CSS vs Motion vs GSAP vs WebGL decisions.
8. **Plan assets and experiments.** Use `asset-generation.md` with `imagegen` for ordinary Codex-native still bitmap assets, `image-generation` for inference.sh image model routing, `video-generation` for model-native video, `remotion` for authoring Remotion code, and `remotion-render` for deterministic React/Remotion MP4s. Use `three-js.md` when the surface earns 3D/WebGL/R3F, and `experimental-rendering.md` only when the effect clearly earns HTML-in-Canvas, Pretext, WebGPU, or canvas text layout complexity.
9. **Audit source fundamentals.** Run `web-design-guidelines` on changed UI files for source-fresh accessibility, focus, forms, navigation, animation, and interface checks.
10. **Implement and verify.** Build with repo patterns, run type/lint/tests, and route UI proof through `visual-qa` or the ticket's QA contract when the surface is user-visible.
11. **Write the handoff.** Summarize the UX/visual decisions, changed files, proof commands, guideline audit result, and any skipped lanes with reasons.

## Decision Branches

| Request shape | Required route |
| --- | --- |
| "this UI sucks", "redesign this component", broken flow | `functional-ui` first, then `visual-design`, then implementation |
| App, dashboard, AI workflow UI | `functional-ui` if unsettled, `visual-design`, `frontend-design` references |
| Landing page, homepage, launch page, portfolio hero | `landing-page`, JSON recipe/taste/effect records when useful, then `visual-design`, then motion/assets references |
| Visual polish only | `visual-design`, then implementation |
| Complex scroll animation | `landing-page` if narrative; otherwise `motion-routing.md` and official GreenSock skills or docs |
| Layered generated-media scroll/timed scene | `composed-scroll-animation.md` when the section needs 6-12 layers, generated/cutout assets, HTML overlays, named phases, debug hooks, and source-frame/checkpoint proof |
| Generated hero/image/texture/reference asset | `asset-generation.md` and `imagegen` |
| Inference.sh image model, background removal, upscaling, or model comparison | `asset-generation.md` and `image-generation` |
| Generated video, image-to-video, avatar/lipsync, foley, or video edit | `asset-generation.md` and `video-generation` |
| Deterministic React/Remotion animation or video component | `asset-generation.md`, `remotion` for code, and `remotion-render` for inference.sh MP4 render |
| Three.js, React Three Fiber, WebGL, shader, or 3D scene | `three-js.md`, progressive enhancement, and explicit fallback |
| Canvas/WebGPU/futuristic rendering outside Three.js | `experimental-rendering.md`, progressive enhancement, and explicit fallback |

## Top Gotchas

- Do not skip `functional-ui` when the UI problem is behavioral, not just visual. Broken IA with prettier cards is still broken.
- Do not start substantial redesign from an internal palette or one-shot
  layout. Use the user's references, comparable products, and `best-of-worlds`
  synthesis before committing to a look.
- Do not let `landing-page` rules leak into dense product tools. A settings page wants clarity and state feedback, not cinematic scrolltelling.
- Do not maintain local GSAP API truth. Use official `greensock/gsap-skills`; this skill only routes when GSAP is appropriate.
- Do not assume inference.sh, Nano Banana, video tooling, or external model CLIs are installed. Capability-gate and use built-in `imagegen` first.
- Do not use experimental rendering APIs without fallback, accessibility, and browser-support checks.
- Do not import icon, motion, chart, form, AI, or registry packages before checking `package.json`.
- Do not use Tailwind v4 syntax in a v3 project, or v3 config assumptions in a v4 project.
- Do not turn an entire Next.js App Router page into a client component just to support one animated widget; isolate interactive/motion-heavy pieces in client leaf components.
- Do not implement sequential product workflows as arbitrary two-column layouts.
  Stack the steps unless the columns are the actual interaction model, such as
  file tree + file viewer, inspector + canvas, editor + preview, or dashboard
  comparison.
- Before adding nested bordered wrappers, ask what each container does. If the
  inner wrapper is not a repeated card, selectable option, modal, tool pane, or
  true sub-surface, remove the extra border and use spacing, a heading, a
  divider, or a band.
- Do not assume inference.sh, Nano Banana, video tooling, or external model CLIs are installed. Capability-gate through the owning asset skill before live external runs, and use built-in `imagegen` first for still images.
- Do not use Three.js/WebGL or experimental rendering APIs without fallback, accessibility, mobile performance, and browser-support checks.

## Reference Map

- `references/routing.md` - entrypoint and lane selection.
- `references/architecture.md` - why this is a wrapper-plus-granular topology.
- `references/workflows.md` - common frontend orchestration paths.
- `references/gotchas.md` - high-risk routing and proof failures.
- `references/motion-routing.md` - CSS, Motion, GSAP, View Transitions, WebGL/WebGPU.
- `references/asset-generation.md` - native `imagegen`, `image-generation`, `video-generation`, `remotion`, `remotion-render`, project-bound assets, external-tool gates.
- `references/media-pipelines.md` - multi-asset website/campaign workflows spanning image, model-native video, Remotion, and frontend QA.
- `references/composed-scroll-animation.md` - method contract for layered
  generated-media scenes with scroll or timed transitions.
- `references/three-js.md` - Three.js/WebGL/R3F routing with links to architecture, planning, workflows, gotchas, and testing refs.
- `references/experimental-rendering.md` - HTML-in-Canvas, Pretext, WebGL/WebGPU, progressive enhancement.
- `references/qa.md` - browser/visual proof expectations.
- `references/upstream-sources.md` - pinned upstream repos and what to borrow from each.

## Outcome Contract

When this skill drives implementation, the final output must include:

- The lanes used or skipped, with one-line reasons.
- The stack facts captured before implementation.
- The implementation files changed.
- The validation commands and results.
- The `web-design-guidelines` result or a concrete reason it was skipped.
- Any generated asset paths and prompts when assets were created.
- A clear handoff to `visual-qa` or ticket QA when UI changed.
