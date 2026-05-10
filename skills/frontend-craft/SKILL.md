---
name: frontend-craft
version: 1.0.0
description: Main frontend implementation orchestrator. Use when the user asks to build, implement, improve, or ship a frontend surface and may need UX planning, visual design, landing-page treatment, motion, assets, or QA routing. Routes through functional-ui, visual-design, landing-page, frontend-design references, imagegen, and visual-qa as needed.
allowed-tools: Read, Grep, Glob, Bash
---

# Frontend Craft

Build production frontends by routing the work through the right frontend brain instead of mixing UX, visual taste, landing-page storytelling, assets, animation, and QA into one blob.

## Use When

- The user says to build or implement a frontend, page, component, app surface, dashboard, or tool UI.
- The request includes both function and look, such as "make this UI good and implement it."
- The target may need shadcn, AI Elements, animation, generated assets, visual QA, or one-page marketing treatment.

## Do Not Use When

- The user only wants UX/workflow redesign: use `functional-ui`.
- The user only wants look/taste/theming: use `visual-design`.
- The user only wants one-page/landing-page narrative planning: use `landing-page`.
- The user only wants review findings on an existing finished UI: use `web-design-guidelines`, `visual-qa`, or `review` as appropriate.

## Core Workflow

1. **Classify the surface.** Product app, workflow component, dashboard, AI interface, landing/marketing page, portfolio, game/tool, or experimental canvas/rendering surface.
2. **Run functional shape when needed.** Use `functional-ui` when the workflow, IA, user story, states, or component behavior is unclear or broken. Skip only when a recent UX brief already settles those answers.
3. **Run visual design.** Use `visual-design` to set register, scene sentence, typography, color strategy, layout rhythm, density, motion taste, and anti-slop constraints.
4. **Route special surfaces.** Use `landing-page` for one-page, marketing, launch, cinematic, scrolltelling, or hero-heavy surfaces.
5. **Capture stack facts.** Before importing UI libraries or writing framework-specific code, inspect `package.json`, Tailwind config/CSS, `components.json`, app router structure, and existing component paths. Record framework/router, Tailwind major version, installed icon/motion/form/chart/AI packages, shadcn aliases, and theme/preset status.
6. **Choose implementation references.** Use `frontend-design` references for shadcn, AI Elements, registries, theme/preset application, component-state matrices, and app UI construction. Use `motion-routing.md` for CSS vs Motion vs GSAP vs WebGL decisions.
7. **Plan assets and experiments.** Use `asset-generation.md` with the `imagegen` skill for generated bitmap assets. Use `experimental-rendering.md` only when the effect clearly earns HTML-in-Canvas, Pretext, WebGL, WebGPU, or canvas text layout complexity.
8. **Implement and verify.** Build with repo patterns, run type/lint/tests, and route UI proof through `visual-qa` or the ticket's QA contract when the surface is user-visible.
9. **Write the handoff.** Summarize the lanes used, stack facts, UX/visual decisions, changed files, proof commands, and any skipped lanes with reasons.

## Decision Branches

| Request shape | Required route |
| --- | --- |
| "this UI sucks", "redesign this component", broken flow | `functional-ui` first, then `visual-design`, then implementation |
| App, dashboard, AI workflow UI | `functional-ui` if unsettled, `visual-design`, `frontend-design` references |
| Landing page, homepage, launch page, portfolio hero | `landing-page`, then `visual-design`, then motion/assets references |
| Visual polish only | `visual-design`, then implementation |
| Complex scroll animation | `landing-page` if narrative; otherwise `motion-routing.md` and official GreenSock skills or docs |
| Generated hero/image/texture/reference asset | `asset-generation.md` and `imagegen` |
| Canvas/WebGPU/futuristic rendering | `experimental-rendering.md`, progressive enhancement, and explicit fallback |

## Top Gotchas

- Do not skip `functional-ui` when the UI problem is behavioral, not just visual. Broken IA with prettier cards is still broken.
- Do not let `landing-page` rules leak into dense product tools. A settings page wants clarity and state feedback, not cinematic scrolltelling.
- Do not maintain local GSAP API truth. Use official `greensock/gsap-skills`; this skill only routes when GSAP is appropriate.
- Do not assume inference.sh, Nano Banana, video tooling, or external model CLIs are installed. Capability-gate and use built-in `imagegen` first.
- Do not use experimental rendering APIs without fallback, accessibility, and browser-support checks.
- Do not import icon, motion, chart, form, AI, or registry packages before checking `package.json`.
- Do not use Tailwind v4 syntax in a v3 project, or v3 config assumptions in a v4 project.
- Do not turn an entire Next.js App Router page into a client component just to support one animated widget; isolate interactive/motion-heavy pieces in client leaf components.

## Reference Map

- `references/routing.md` - entrypoint and lane selection.
- `references/architecture.md` - why this is a wrapper-plus-granular topology.
- `references/workflows.md` - common frontend orchestration paths.
- `references/gotchas.md` - high-risk routing and proof failures.
- `references/motion-routing.md` - CSS, Motion, GSAP, View Transitions, WebGL/WebGPU.
- `references/asset-generation.md` - native `imagegen`, project-bound assets, external-tool gates.
- `references/experimental-rendering.md` - HTML-in-Canvas, Pretext, WebGL/WebGPU, progressive enhancement.
- `references/qa.md` - browser/visual proof expectations.
- `references/upstream-sources.md` - pinned upstream repos and what to borrow from each.

## Outcome Contract

When this skill drives implementation, the final output must include:

- The lanes used or skipped, with one-line reasons.
- The stack facts captured before implementation.
- The implementation files changed.
- The validation commands and results.
- Any generated asset paths and prompts when assets were created.
- A clear handoff to `visual-qa` or ticket QA when UI changed.
