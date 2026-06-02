# Planner / Executor Contract

Use this when a landing page needs enough craft that implementation should not
start from a vague prompt.

## Decision Rule

- No approved `LANDING_SPEC.md` -> stay in Planner.
- Approved `LANDING_SPEC.md` exists -> Executor may build.
- If the spec exists but fails `landing_spec_lint.py`, return to Planner.

## Planner Gates

Ask one focused question at a time, borrowing the `deep-interview` style, until
these gates are explicit:

- `Audience`: who must believe this page.
- `Offer`: literal product/category and value proposition.
- `Narrative`: why the section sequence is the right story.
- `Taste references`: 2-4 references and what to adopt or reject.
- `Reference research`: 3-5 competitor/comparable/inspiration sources with
  notes on asset strategy, section order, proof pattern, layout, motion, and
  claim boundaries.
- `Best-of-worlds decisions`: source patterns are marked `adopt`, `adapt`,
  `reject`, or `defer` before they become local requirements.
- `Unique take`: one differentiated creative/narrative move that prevents the
  page from becoming a stitched-together competitor clone.
- `Non-goals`: what the page must not become.
- `Decision boundaries`: what the agent may decide without asking.
- `Section matrix`: every section has a job, visual, asset, motion, proof, and
  QA assertion.
- `Asset plan`: generated, real, screenshot, video, canvas, SVG, or WebGL
  carrier named per section.
- `Product demo plan`: for physical products, devices, hardware, equipment, or
  object demos, name realistic product shots, in-context use, assembly or
  disassembly / exploded-view sequence, product parts/features to highlight,
  and the QA proof that scroll/video changes meaningful product states.
- `Asset evidence`: premium/cinematic pages name the actual generated or real
  filesystem-backed media assets, poster, reduced-motion still, mobile variant,
  provenance, and `assets/asset-manifest.json`.
- `Motion plan`: effect exists because it reveals meaning, not because motion is
  decorative.
- `QA gates`: first viewport, mobile, reduced motion, scroll checkpoints,
  section quality, designer judgment, browser console/errors, source review.

If more than two of these are unresolved, use `deep-interview` rather than
pretending a landing brief is ready.

## LANDING_SPEC Shape

```markdown
---
status: approved
approval_source: user|ticket|brief
landing_type: cinematic-scrolltelling
quality_target: terminal-level
---

# LANDING_SPEC

## Offer
## Audience
## Non-goals
## Decision Boundaries
## Taste References
## Reference Research
## Best-of-worlds Decisions
## Unique Take
## Narrative Arc
## Low-fi ASCII Flow
## Section Matrix

| Section | Job | Claim | Layout | Asset carrier | Motion lever | Proof payload | QA |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Method Selection

Use `references/model.md` to choose a complete direction for each major
section. A direction is:

`layout + asset carrier + motion lever + proof payload + fallback + QA`

Do not advise isolated variables unless one variable is the real blocker. For
layered generated-media sections, use `references/method-selection-smoke.md` to
verify when `frontend-craft:composed-scroll-animation` is the correct handoff.

## Asset Plan
## Product Demo Plan
## Motion Plan
## Proof Plan
## Designer Judgment Plan
## QA Gates
## Executor Handoff
```

## Executor Rules

- Run `scripts/landing_spec_lint.py <LANDING_SPEC.md>` before build.
- Build from the section matrix; do not invent missing sections during
  implementation.
- Generate or collect the approved media assets before the final build claim.
  If the run cannot do that, downgrade the quality target to `prototype` and
  record the missing media blocker.
- For product pages, fail the plan when the product demo is only a generic
  infographic, dashboard mock, abstract diagram, or short label-changing scrub.
- Run `scripts/asset_evidence_lint.py <site-dir>` after build. Premium pages
  fail when the manifest contains only canvas, SVG, WebGL, Three.js, or HTML/CSS
  support visuals.
- For premium pages, every main section gets a user-visible visual carrier.
- For Terminal-style pages, hero scroll scrub is required but not sufficient.
- Use `section_quality_qa.cjs` after implementation to catch blank sections and
  placeholder proof.
- Use `designer-judgment.md` to score the final 5% that screenshots and
  mechanics cannot capture alone.
