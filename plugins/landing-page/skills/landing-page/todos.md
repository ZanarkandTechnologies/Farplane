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
