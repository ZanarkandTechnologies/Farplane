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
- `Non-goals`: what the page must not become.
- `Decision boundaries`: what the agent may decide without asking.
- `Section matrix`: every section has a job, visual, asset, motion, proof, and
  QA assertion.
- `Asset plan`: generated, real, screenshot, video, canvas, SVG, or WebGL
  carrier named per section.
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
## Narrative Arc
## Low-fi ASCII Flow
## Section Matrix

| Section | User job | Narrative claim | Visual carrier | Asset plan | Motion/effect | Proof/copy payload | QA assertion |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Asset Plan
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
- For premium pages, every main section gets a user-visible visual carrier.
- For Terminal-style pages, hero scroll scrub is required but not sufficient.
- Use `section_quality_qa.cjs` after implementation to catch blank sections and
  placeholder proof.
- Use `designer-judgment.md` to score the final 5% that screenshots and
  mechanics cannot capture alone.
