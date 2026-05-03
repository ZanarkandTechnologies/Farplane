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

1. **Define the offer.** Name the product/person/place/object/category and the literal value proposition.
2. **Choose the story shape.** Problem -> shift -> proof -> action, or a stronger domain-specific arc when available.
3. **Map sections.** First viewport, proof, features, comparison, social proof, pricing/contact, final CTA. Keep only what the offer earns.
4. **Create visual scenes.** Decide which sections need real media, generated assets, product screenshots, video, WebGL, or code-native visuals.
5. **Set landing visual rules.** Use `visual-design` for register, scene sentence, typography, color strategy, density, and anti-slop constraints.
6. **Plan motion.** Choose CSS/Motion/GSAP/WebGL with `frontend-craft/references/motion-routing.md`; use official GreenSock skills or docs for GSAP code.
7. **Plan proof.** Define mobile/desktop first-viewport checks, scroll checkpoints, asset-load checks, and reduced-motion checks.
8. **Hand off to `frontend-craft`.** Provide sections, assets, motion, and QA expectations.

## Decision Branches

| Landing type | Lead with |
| --- | --- |
| Product/app homepage | actual product state, screenshot, workflow, or demo scene |
| Brand/portfolio | identity, work, material, and editorial composition |
| Venue/place/object | real first-viewport signal of the place/object, not generic atmosphere |
| Cinematic scrolltelling | story beats, pinned viewport, scene layers, scroll checkpoints |
| Simple launch page | sharp offer, strong proof, fast CTA, minimal sections |

## Top Gotchas

- Do not make a marketing landing page when the user asked for a usable app/tool.
- Do not hide the product/place/object behind tiny nav text or vague mood imagery.
- Do not use a split text/media hero when a full-bleed image or interactive scene should carry the page.
- Do not make static AI-art pages with no relationship to the offer.
- Do not keep stale local GSAP examples as API truth; route to official GreenSock skills or docs.

## Reference Map

- `references/scrolltelling.md` - section/story and scroll narrative structure.
- `references/motion-and-media.md` - media, generated assets, GSAP/WebGL routing.
- `references/qa.md` - landing-page proof checks.
- `references/architecture.md` - landing-page ownership and handoff model.
- `references/workflows.md` - standard landing and cinematic scrolltelling paths.
- `references/gotchas.md` - common landing-page mistakes.

## Output Contract

Return a landing brief with:

- `Offer`
- `Audience`
- `Story arc`
- `Section map`
- `Visual scenes/assets`
- `Motion plan`
- `QA plan`
- `Implementation handoff`
