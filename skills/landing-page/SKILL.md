---
name: landing-page
version: 1.0.0
description: Use for one-page marketing, launch, homepage, portfolio, hero-heavy, cinematic, or scrolltelling frontend surfaces. Shapes the offer, story arc, sections, assets, motion, and proof before frontend-craft implements.
tier: 3
group: frontend-content
source: local
allowed-tools: Read, Grep, Glob, Bash
---

# Landing Page

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

# Landing Page Todos

Use this short checklist for landing-page work. Load the linked references only
when the request earns that depth.

## 1. Ground

- [ ] Identify the product, category, buyer, and promised transformation in one
  sentence.
- [ ] Collect 3-5 competitor or inspiration references, including the user's
  supplied reference when available.
- [ ] Use [research-synthesis](./references/research-synthesis.md) to extract
  section order, hero media, motion, proof, layout, and asset patterns.

## 2. Model

- [ ] Use [model](./references/model.md) to define
  `LandingPage := Offer + Audience + StoryArc + SectionMatrix + AssetPlan + MotionPlan + ProofPlan`.
- [ ] Build the section matrix before implementation. Each section needs job,
  claim, layout, asset carrier, motion lever, proof payload, fallback, and QA.
- [ ] Draft the low-fidelity ASCII page flow before generating assets or
  writing code.

## 3. Choose Methods

- [ ] For each major section, compare complete directions:
  `layout + asset carrier + motion lever + proof payload + fallback + QA`.
- [ ] Choose from filesystem-visible methods and levers:
  [landing-recipes](./references/landing-recipes.json),
  [taste-profiles](./references/taste-profiles.json),
  [effect-stacks](./references/effect-stacks.json), and
  [motion-and-media](./references/motion-and-media.md).
- [ ] Use
  [method-selection-smoke](./references/method-selection-smoke.md) as the
  sanity fixture for `frontend-craft:composed-scroll-animation` selection.
- [ ] Reject unused directions so the page does not stack every impressive
  effect at once.

## 4. Specify

- [ ] Write or update `LANDING_SPEC.md` with the section matrix, selected
  methods, execution packets, asset plan, motion plan, and QA gates.
- [ ] For premium/cinematic pages, use
  [planner-executor](./references/planner-executor.md) and
  [asset-evidence](./references/asset-evidence.md) before implementation.
- [ ] Keep readable text, CTAs, labels, logos, and product copy in HTML
  overlays unless the approved spec says otherwise.

## 5. Execute And Prove

- [ ] Hand approved execution packets to [frontend-craft](../frontend-craft/SKILL.md).
- [ ] Use [execute](../execute/SKILL.md) for proof, writeback, and review.
- [ ] Run landing QA from [qa](./references/qa.md), plus scroll/media QA when
  the selected method requires it.
- [ ] Record desktop/mobile screenshots, asset manifest/provenance, method
  selection notes, and final gap analysis.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

Shape one-page frontend experiences that persuade, orient, or create memory.
This skill owns page story, section architecture, planning gates, visual scenes,
media, motion intent, and landing-page QA. It does not own GSAP API details or
app-dashboard workflow design.

Compact model:

```text
LandingPage := Offer + Audience + StoryArc + SectionMatrix + AssetPlan + MotionPlan + ProofPlan

Section := Job + Claim + Layout + AssetCarrier + MotionLever + ProofPayload + Fallback + QA

MethodSelection(section, methods, constraints) :=
  candidates = filter(methods, section, constraints)
  chosen = advise(top3(candidates))
```

Use `references/model.md` for the algebra and section matrix rules. Keep the
Todo List short; detailed recipes live in references and method records.

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
3. **Research the competitive and inspiration set.** Before choosing a story or
   asset plan, collect 3-5 competitor/comparable/inspiration references and
   record what assets, section order, proof patterns, layout moves, motion
   style, and claim boundaries they use. For current websites, browse or inspect
   the live source instead of relying on memory.
4. **Synthesize best-of-worlds decisions.** Use `best-of-worlds` to mark the
   reference patterns `adopt`, `adapt`, `reject`, or `defer`, then use
   `brainstorm` to define a unique take that is not a collage of competitor
   sections. The spec must include the resulting golden standard and the local
   differentiation move.
5. **Choose the story shape.** Problem -> shift -> proof -> action, or a
   stronger domain-specific arc when available.
6. **Map sections.** First viewport, proof, features, comparison, social proof,
   pricing/contact, final CTA. Keep only what the offer earns.
7. **Draft the low-fidelity story.** Produce an ASCII page flow before asset or
   component work.
8. **Create the section matrix.** For every section, answer:
   - user job and narrative claim,
   - visual carrier users will actually see,
   - asset/media plan,
   - motion/effect plan,
   - proof/copy payload,
   - QA assertion that proves the section is not blank or generic.
9. **Explore effects per section.** For premium pages, explicitly consider
   video, GSAP/ScrollTrigger, WebGL/Three.js, HTML-in-canvas, generated bitmap
   media, and reduced-motion alternatives. Do not plan custom SVG illustrations
   or hand-authored SVG/data-overlay visuals for premium landing-page graphics;
   use generated/real raster media or real WebGL/Three.js when the page needs a
   visual system. Use `advise` when the best carrier is not obvious.
   For cinematic heroes, do not stop at "scroll scrub video" as a label: plan a
   long scrub with named story beats, progress ranges, and at least one
   sectioned effect layer such as GSAP timeline overlays, WebGL shader/scan
   effects, Three.js product staging, or HTML beat panels driven by the same
   scroll progress.
10. **Plan product demo media when a product, device, hardware, equipment, or
    physical object is being sold.** The plan must include realistic product
    shots or product photography/renders, in-context use shots, and at least
    one meaningful product-reveal sequence such as assembly, disassembly,
    exploded view, feature callout, material/detail macro, or before/after
    operation. For Apple-style product pages, the hero or primary motion should
    reveal the object by breaking it into meaningful parts and reassembling it.
    Generic infographics, abstract SVGs, hand-authored SVG diagrams, and
    decorative dashboards do not count as the product demo.
11. **Plan product clarity and accessibility.** For premium product pages, the
   product must remain inspectable in the hero and primary demo: no dark wash,
   heavy WebGL tint, tiny crop, low-opacity video, or decorative overlay can
   obscure the object. Plan contrast checks, focus/skip-link affordances, image
   width/height attributes, alt text, and a product-clarity score alongside the
   visual QA. Product disassembly media also needs a disassembly score covering
   object continuity, visible components, clean separation, lighting, and lack
   of baked readable text.
12. **Plan asset evidence.** For premium, cinematic, or generated-media pages,
   name the actual generated or real media assets that must exist before final
   implementation: hero video/image/frame sequence, poster, reduced-motion
   still, mobile variant, source prompt/provenance, and
   `assets/asset-manifest.json`. Canvas, Three.js, and WebGL may support the
   page, but they do not satisfy the generated-media asset requirement by
   themselves. Hand-authored SVG illustrations should not be used for premium
   landing-page graphics.
13. **Set landing visual rules.** Use `visual-design` for register, scene
   sentence, numeric taste dials, typography, color strategy, density, and
   anti-slop constraints. For premium or delegated pages, preserve those
   choices in the landing spec or a linked design brief.
14. **Plan proof.** Define mobile/desktop first-viewport checks, scroll
   checkpoints, asset-load checks, section-quality checks, designer-judgment
   review, asset-evidence checks, accessibility/product-clarity checks, and
   reduced-motion checks.
15. **Approval gate.** Mark the spec approved only after the user or ticket
    explicitly accepts the narrative, section matrix, and QA plan.

### Executor Stage

1. Read the approved `LANDING_SPEC.md`.
2. Validate it with `scripts/landing_spec_lint.py` when available.
3. Generate or collect the named assets before implementation. If assets cannot
   be generated or collected during the run, downgrade the page to a prototype,
   record the blocker, and do not claim premium/cinematic/Terminal quality.
   If the spec calls for generated video, use a real video-generation model or
   source video and record video provenance (`videoModel`, `videoProvider`,
   `sourceVideo`, or equivalent) in the asset manifest. Do not count Seedream or
   other image-generation stills assembled with `ffmpeg` as `generated-video`;
   declare that as `frame-sequence` or downgrade to prototype.
4. Implement the page through `frontend-craft` or `delegate-frontend`.
5. Run asset-evidence QA, scroll/media QA, section-quality QA,
   designer-judgment review, mobile, reduced-motion, browser console/error, and
   source review checks.
6. Do not claim Terminal/premium parity while any hard gate fails.
For cinematic, Terminal-style, premium industrial, asset-heavy, or generated-media pages, run the spec-first gate in `references/spec-first-cinematic-industrial.md` before implementation. If the user asks to build in the same turn, still separate the work into spec, assets, implementation, and visual-review phases so each builder pass has a bounded output.
For modern scroll-scrub or Terminal/Terminus-level work, follow the Important
Checklist as the active recipe: competitor/inspiration analysis, user story,
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
- Do not use generic infographics as the primary media for a physical product
  or device page. Show the actual product, the product in use, and the
  meaningful parts/features that make it worth buying.
- Do not keep stale local GSAP examples as API truth; route to official GreenSock skills or docs.
- Do not build before an approved landing spec exists.
- Do not let a passing hero scroll-scrub score hide blank lower-page sections.
- Do not accept a section plan that says "canvas", "video", or "GSAP" without
  saying what the user sees and what QA will assert.
- Do not create custom SVG illustrations or SVG diagram overlays for premium
  landing-page visuals. Generate raster assets, use real media, or build a real
  WebGL/Three.js scene instead.
- Do not treat code-rendered canvas, hand-authored SVG, Three.js, or HTML/CSS
  visuals as generated media. They are support visuals unless an explicit
  prototype downgrade is recorded.
- Do not accept short scroll scrub that only changes labels or fades a static
  image. Product scroll scrub must reveal meaningful product states, parts,
  assembly/disassembly, feature layers, or before/after operation.
- Do not rely on one hero image to imply the whole page. Premium pages need
  section-level image or media continuity so lower sections do not become
  generic copy blocks after the first viewport.
- Do not accept a cinematic hero scrub without a duration/beat plan. Premium
  hero scrub should normally be 8-15+ seconds or an equivalent 96+ frame
  sequence, include at least five named story beats, and expose debug evidence
  for media time, active beat, and effect layer state.
- Do not hide the product behind the visual system. If color washes, overlays,
  WebGL effects, video opacity, or background treatment make the product hard
  to see, the page fails product clarity even when the composition looks
  cinematic.
- Do not prompt product teardown assets with visible alphanumeric quality words
  such as `8K` inside the scene. Put resolution/quality in generation metadata
  or trailing style language only, and explicitly forbid readable text baked
  into pixels.
- Do not add a decorative 3D scene that could be replaced by a better still image; 3D must clarify the product, object, system, or story.
- Do not add a new recipe, taste profile, or effect stack without a stable `id`, routing criteria, examples, compatibility, and QA expectations.
- Do not keep stale local GSAP examples as API truth; route to official GreenSock skills or docs.
- Do not ask one builder pass to plan, generate assets, implement, visually review, and repair a cinematic page. Split the pass or expect stalls and mismatched files.
- Do not accept code-native SVG stand-ins as Terminal-quality media unless the brief marks them as a placeholder and includes a concrete generated-media or real-media upgrade path.

## Reference Map

- `references/scrolltelling.md` - section/story and scroll narrative structure.
- `references/model.md` - algebraic landing-page model, section matrix, method
  selection, and composed-scroll route.
- `references/method-selection-smoke.md` - text fixture for choosing
  `frontend-craft:composed-scroll-animation` only when section constraints
  require it.
- `references/motion-and-media.md` - media, generated assets, GSAP/WebGL routing.
- `references/product-demo-media.md` - realistic product shots, assembly /
  exploded-view sequences, and anti-infographic requirements.
- `references/research-synthesis.md` - competitor/inspiration research and
  best-of-worlds synthesis gate.
- [frontend-craft three-js.md](../frontend-craft/references/three-js.md) - Three.js/WebGL/R3F reference route for product/object/system hero scenes and interactive 3D assets.
- `references/landing-recipes.json` - JSON registry of page formulas and section structures.
- `references/taste-profiles.json` - JSON registry of landing-page visual registers.
- `references/effect-stacks.json` - JSON registry of implementation stacks, assets, debug hooks, and QA.
- `references/spec-first-cinematic-industrial.md` - Terminal-style spec-first gate, asset contract, external-builder phase split, and gold-reference comparison checklist.
- `references/terminal-scroll-review.md` - domain-specific review rubric and 80-point self-improvement score for Terminal/Terminus-style landing pages.
- `references/registry-format.md` - JSON field contract, routing rules, and authoring checklist.
- `references/cinematic-scroll-site-guideline.md` - compatibility pointer for older Terminal-style cinematic-scroll references.
- `references/qa.md` - landing-page proof checks.
- `references/architecture.md` - landing-page ownership and handoff model.
- `references/workflows.md` - standard landing and cinematic scrolltelling paths.
- `references/planner-executor.md` - spec-first planner/executor contract.
- `references/asset-evidence.md` - generated/real media proof gate.
- `references/designer-judgment.md` - final 5% premium quality rubric.
- `references/gotchas.md` - common landing-page mistakes.
- `SKILL.md` Todo List - ordered modern scroll-scrub landing recipe with competitor analysis, nested `advise`, asset generation, scroll-scrub instrumentation, and QA handoff.

## Output Contract

Return a landing brief with:

- `Offer`
- `Audience`
- `Reference research`
- `Best-of-worlds decisions`
- `Unique take`
- `Recipe route` with selected recipe, taste-profile, and effect-stack IDs when used
- `Story arc`
- `Low-fi ASCII flow`
- `Section map`
- `Visual scenes/assets`
- `Product demo plan`
- `Asset evidence plan`
- `Product clarity/accessibility plan`
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
- `Reference Research`
- `Best-of-worlds Decisions`
- `Unique Take`
- `Section Matrix`
- `Asset Plan`
- `Product Demo Plan` for physical product, device, hardware, equipment, or
  product-demo pages
- `Product Clarity and Accessibility Plan` for product/object-focused pages
- `Motion Plan`
- `QA Gates`
- `assets/asset-manifest.json`
For cinematic industrial pages, the output must also name the current phase:
`spec`, `assets`, `implementation`, or `visual-review`. The `spec` phase must
include a file map, generated/real asset manifest plan, desktop and mobile hero
media plan, poster/reduced-motion fallback, scroll checkpoints, and the next
phase prompts or task slices.

For Terminal/Terminus-style self-improvement runs, also include the
`terminal-scroll-review` target: score with
`scripts/terminal_landing_score.py`, treat `80` as the pass threshold, and use
the lowest scoring dimension as the next repair hypothesis.
