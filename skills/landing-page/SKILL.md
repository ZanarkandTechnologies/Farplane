---
name: landing-page
version: 1.0.0
description: Use for one-page marketing, launch, homepage, portfolio, hero-heavy, cinematic, or scrolltelling frontend surfaces. Shapes the offer, story arc, sections, assets, motion, and proof before frontend-craft implements.
allowed-tools: Read, Grep, Glob, Bash
---

# Landing Page

Shape one-page frontend experiences that persuade, orient, or create memory. This skill owns page story and section architecture; it does not own GSAP API details or app-dashboard workflow design.

## Use When

- The user asks for a landing page, homepage, launch page, one-page site, portfolio page, product page, venue/person/object-focused page, hero page, or cinematic scroll experience.
- The frontend needs a strong first viewport, narrative sections, generated assets, media, or scroll-based storytelling.
- `frontend-craft` classifies the surface as brand/marketing rather than repeated product work.

## Do Not Use When

- The target is a dashboard, settings screen, CRUD workflow, or operational app UI: use `functional-ui`.
- The user only wants visual polish on an existing app component: use `visual-design`.
- The task is GSAP implementation details: use installed official GreenSock skills when available, or fetch official GSAP docs.

## Core Workflow

For cinematic, Terminal-style, premium industrial, asset-heavy, or generated-media pages, run the spec-first gate in `references/spec-first-cinematic-industrial.md` before implementation. If the user asks to build in the same turn, still separate the work into spec, assets, implementation, and visual-review phases so each builder pass has a bounded output.
For modern scroll-scrub or Terminal/Terminus-level work, also load `todos.md`
and follow it as the active recipe: competitor/inspiration analysis, user story,
ASCII page flow, nested `advise` section exploration, generated/rendered hero
media planning, asset conversion, implementation, and QA.

1. **Define the offer.** Name the product/person/place/object/category and the literal value proposition.
2. **Choose the story shape.** Problem -> shift -> proof -> action, or a stronger domain-specific arc when available.
3. **Select registry records when useful.** For repeatable high-taste pages, choose one recipe from `references/landing-recipes.json`, one taste profile from `references/taste-profiles.json`, and one effect stack from `references/effect-stacks.json`; use `references/registry-format.md` for field meanings.
4. **Map sections.** First viewport, proof, features, comparison, social proof, pricing/contact, final CTA. Keep only what the offer earns.
5. **Create visual scenes.** Decide which sections need real media, generated assets, product screenshots, video, Three.js/WebGL, or code-native visuals. Treat 3D as a first-class landing asset when it reveals the product, object, system, or place.
6. **Set landing visual rules.** Use `visual-design` for register, scene sentence, typography, color strategy, density, and anti-slop constraints, then refine with the chosen landing taste profile.
7. **Plan motion.** Choose CSS/Motion/GSAP/WebGL with `frontend-craft/references/motion-routing.md`; for cinematic scroll sites, use the selected effect-stack record and official GreenSock skills or docs for GSAP code.
8. **Plan proof.** Define mobile/desktop first-viewport checks, scroll checkpoints, asset-load checks, and reduced-motion checks.
9. **Hand off to `frontend-craft`.** Provide sections, selected registry IDs, assets, motion, and QA expectations.

## Decision Branches

| Landing type | Lead with |
| --- | --- |
| Product/app homepage | actual product state, screenshot, workflow, 3D product/system scene, or demo scene |
| Brand/portfolio | identity, work, material, and editorial composition |
| Venue/place/object | real first-viewport signal of the place/object, not generic atmosphere |
| Cinematic scrolltelling | story beats, pinned viewport, scene layers, scroll checkpoints |
| Simple launch page | sharp offer, strong proof, fast CTA, minimal sections |

## Registry Route

For landing pages with reusable formulas or inspiration references:

1. Open `references/landing-recipes.json` and select a recipe ID.
2. Open `references/taste-profiles.json` and select a compatible taste profile ID.
3. Open `references/effect-stacks.json` and select a compatible effect stack ID.
4. If the request intentionally mixes incompatible records, state the reason in the landing brief.
5. Keep `references/cinematic-scroll-site-guideline.md` as a compatibility pointer; do not treat it as the source of truth when JSON records apply.

## Top Gotchas

- Do not make a marketing landing page when the user asked for a usable app/tool.
- Do not hide the product/place/object behind tiny nav text or vague mood imagery.
- Do not use a split text/media hero when a full-bleed image or interactive scene should carry the page.
- Do not make static AI-art pages with no relationship to the offer.
- Do not add a decorative 3D scene that could be replaced by a better still image; 3D must clarify the product, object, system, or story.
- Do not add a new recipe, taste profile, or effect stack without a stable `id`, routing criteria, examples, compatibility, and QA expectations.
- Do not keep stale local GSAP examples as API truth; route to official GreenSock skills or docs.
- Do not ask one builder pass to plan, generate assets, implement, visually review, and repair a cinematic page. Split the pass or expect stalls and mismatched files.
- Do not accept code-native SVG stand-ins as Terminal-quality media unless the brief marks them as a placeholder and includes a concrete generated-media or real-media upgrade path.

## Reference Map

- `references/scrolltelling.md` - section/story and scroll narrative structure.
- `references/motion-and-media.md` - media, generated assets, GSAP/WebGL routing.
- [frontend-craft three-js.md](../frontend-craft/references/three-js.md) - Three.js/WebGL/R3F reference route for product/object/system hero scenes and interactive 3D assets.
- `references/landing-recipes.json` - JSON registry of page formulas and section structures.
- `references/taste-profiles.json` - JSON registry of landing-page visual registers.
- `references/effect-stacks.json` - JSON registry of implementation stacks, assets, debug hooks, and QA.
- `references/spec-first-cinematic-industrial.md` - Terminal-style spec-first gate, asset contract, external-builder phase split, and gold-reference comparison checklist.
- `references/registry-format.md` - JSON field contract, routing rules, and authoring checklist.
- `references/cinematic-scroll-site-guideline.md` - compatibility pointer for older Terminal-style cinematic-scroll references.
- `references/qa.md` - landing-page proof checks.
- `references/architecture.md` - landing-page ownership and handoff model.
- `references/workflows.md` - standard landing and cinematic scrolltelling paths.
- `references/gotchas.md` - common landing-page mistakes.
- `todos.md` - ordered modern scroll-scrub landing recipe with competitor analysis, nested `advise`, asset generation, scroll-scrub instrumentation, and QA handoff.

## Output Contract

Return a landing brief with:

- `Offer`
- `Audience`
- `Recipe route` with selected recipe, taste-profile, and effect-stack IDs when used
- `Story arc`
- `Section map`
- `Visual scenes/assets`
- `Motion plan`
- `QA plan`
- `Implementation handoff`

For cinematic industrial pages, the output must also name the current phase:
`spec`, `assets`, `implementation`, or `visual-review`. The `spec` phase must
include a file map, generated/real asset manifest plan, desktop and mobile hero
media plan, poster/reduced-motion fallback, scroll checkpoints, and the next
phase prompts or task slices.
