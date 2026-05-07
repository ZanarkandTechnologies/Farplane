---
name: landing-page
version: 1.0.0
description: Use for one-page marketing, launch, homepage, portfolio, hero-heavy, cinematic, or scrolltelling frontend surfaces. Shapes the offer, story arc, sections, assets, motion, and proof before frontend-craft implements.
allowed-tools: Read, Grep, Glob, Bash
---

# Landing Page

Shape one-page frontend experiences that persuade, orient, or create memory.
This skill owns page story, section architecture, planning gates, visual scenes,
media, motion intent, and landing-page QA. It does not own GSAP API details or
app-dashboard workflow design.

## Use When

- The user asks for a landing page, homepage, launch page, one-page site, portfolio page, product page, venue/person/object-focused page, hero page, or cinematic scroll experience.
- The frontend needs a strong first viewport, narrative sections, generated assets, media, or scroll-based storytelling.
- `frontend-craft` classifies the surface as brand/marketing rather than repeated product work.

## Do Not Use When

- The target is a dashboard, settings screen, CRUD workflow, or operational app UI: use `functional-ui`.
- The user only wants visual polish on an existing app component: use `visual-design`.
- The task is GSAP implementation details: use installed official GreenSock skills when available, or fetch official GSAP docs.

## Core Workflow

`landing-page` has two stages:

1. **Planner:** interview, compare references, draft and approve
   `LANDING_SPEC.md`.
2. **Executor:** build only from an approved spec, then run landing QA.

If no approved `LANDING_SPEC.md` or equivalent section exists, stay in Planner.
Do not hand off to `frontend-craft`, `delegate-frontend`, or an external CLI
builder until the spec passes the planning gates below.

### Planner Stage

1. **Define the offer.** Name the product/person/place/object/category and the literal value proposition.
2. **Interview with gates.** Ask one high-leverage question at a time when
   audience, narrative, taste, non-goals, or decision boundaries are vague. Use
   `deep-interview` when more than two gates remain unresolved.
3. **Choose the story shape.** Problem -> shift -> proof -> action, or a
   stronger domain-specific arc when available.
4. **Map sections.** First viewport, proof, features, comparison, social proof,
   pricing/contact, final CTA. Keep only what the offer earns.
5. **Draft the low-fidelity story.** Produce an ASCII page flow before asset or
   component work.
6. **Create the section matrix.** For every section, answer:
   - user job and narrative claim,
   - visual carrier users will actually see,
   - asset/media plan,
   - motion/effect plan,
   - proof/copy payload,
   - QA assertion that proves the section is not blank or generic.
7. **Explore effects per section.** For premium pages, explicitly consider
   video, GSAP/ScrollTrigger, WebGL/Three.js, SVG/data-overlay, HTML-in-canvas,
   and reduced-motion alternatives. Use `advise` when the best carrier is not
   obvious.
8. **Set landing visual rules.** Use `visual-design` for register, scene
   sentence, typography, color strategy, density, and anti-slop constraints.
9. **Plan proof.** Define mobile/desktop first-viewport checks, scroll
   checkpoints, asset-load checks, section-quality checks, designer-judgment
   review, and reduced-motion checks.
10. **Approval gate.** Mark the spec approved only after the user or ticket
    explicitly accepts the narrative, section matrix, and QA plan.

### Executor Stage

1. Read the approved `LANDING_SPEC.md`.
2. Validate it with `scripts/landing_spec_lint.py` when available.
3. Generate or collect the named assets before implementation.
4. Implement the page through `frontend-craft` or `delegate-frontend`.
5. Run scroll/media QA, section-quality QA, designer-judgment review, mobile,
   reduced-motion, browser console/error, and source review checks.
6. Do not claim Terminal/premium parity while any hard gate fails.

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
- Do not build before an approved landing spec exists.
- Do not let a passing hero scroll-scrub score hide blank lower-page sections.
- Do not accept a section plan that says "canvas", "video", or "GSAP" without
  saying what the user sees and what QA will assert.

## Reference Map

- `references/scrolltelling.md` - section/story and scroll narrative structure.
- `references/motion-and-media.md` - media, generated assets, GSAP/WebGL routing.
- `references/qa.md` - landing-page proof checks.
- `references/architecture.md` - landing-page ownership and handoff model.
- `references/workflows.md` - standard landing and cinematic scrolltelling paths.
- `references/planner-executor.md` - spec-first planner/executor contract.
- `references/designer-judgment.md` - final 5% premium quality rubric.
- `references/gotchas.md` - common landing-page mistakes.

## Output Contract

Return a landing brief with:

- `Offer`
- `Audience`
- `Story arc`
- `Low-fi ASCII flow`
- `Section map`
- `Visual scenes/assets`
- `Motion plan`
- `Designer judgment plan`
- `QA plan`
- `Implementation handoff`

For executor handoff, prefer a checked-in or ticket-attached `LANDING_SPEC.md`
with:

- `status: approved`
- `approval_source`
- `Non-goals`
- `Decision boundaries`
- `Section Matrix`
- `Asset Plan`
- `Motion Plan`
- `QA Gates`
