---
kind: skill-example-fixture
skill: infographic
method: infographic:handdrawn-saas-wireframe
created_at: 2026-06-27
---

# Hand-Drawn SaaS Wireframe Example

## Use When

Use this fixture when the user wants a dense monochrome product-state
infographic like a hand-drawn SaaS dashboard storyboard. It is especially
useful for product concepts, workflow states, agent dashboards, scorecards,
governance screens, integration maps, and strategy sketches where the output
must hold lots of inspectable information.

## Input Brief

Create a product-concept infographic for a workforce automation dashboard. The
visual should explain four states of the product: daily executive pulse,
digital worker team, worker profile, and integrations. Use a monochrome
hand-drawn wireframe style with annotations that explain system state and
future product boundaries.

## Reference

- `assets/reference.png`: user-provided visual reference for the desired style.

Transfer these qualities, not the private product content:

- 2x2 storyboard with four app states.
- Repeated left navigation and shared SaaS shell.
- Dense UI objects: metric cards, worker tables, tabs, profile panels,
  integration cards, queues, source-health rows, chips, buttons, and callouts.
- Black ink on white paper with light gray fills, uneven rounded rectangles,
  simple icons, arrows, and handwritten labels.
- Right-side notes that explain data freshness, policy, lifecycle, approvals,
  and deferred functionality.

## Good Output

- `assets/good-output.png`: accepted dense sample output generated from this
  skill after the first sparse attempt failed the density bar.
- `assets/good-output.svg`: deterministic source for the accepted sample.

The good output uses a new concept, `Farplane Skill Factory`, while preserving
the reference method: four dense panels, shared nav, compact UI tables/cards,
specific status labels, and behavior-oriented annotations.

## Comparison Gates

- `density_match`: each large panel has multiple visible UI regions, roughly
  8-14 UI objects, 20-45 exact text labels, 2-4 annotation notes, and only
  intentional gutter whitespace.
- `state_story`: every panel teaches a different product state rather than a
  decorative variant.
- `shared_shell`: panels reuse the same app-frame grammar, navigation, title
  treatment, card shapes, and annotation lane.
- `copy_inventory`: important labels, numbers, buttons, and callouts are
  planned before rendering and remain readable in the final asset.
- `annotation_value`: notes explain product behavior, policy, source state,
  lifecycle, or deferrals.
- `style_match`: monochrome hand-drawn SaaS wireframe, not polished colorful
  SaaS mockup, poster art, 3D UI, gradient background, or stock illustration.

Fail the example when the output has the right sketch line style but feels
empty, has unreadable small labels, lacks product logic, or compresses the
story into generic dashboard boxes.

## Provenance / Rights

`assets/reference.png` was supplied by the operator in this thread as the style
reference. `assets/good-output.png` and `assets/good-output.svg` are generated
Farplane sample artifacts created for this skill. Treat the reference as a
taste and layout anchor; do not copy its private product text or metrics into
client/public work unless the operator explicitly authorizes reuse.
