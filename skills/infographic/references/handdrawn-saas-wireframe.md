---
template_id: skill-method-reference
template_version: "0.1.0"
feature_refs:
  - FEAT-0057
consumer_scope: skill-reference
applies_to:
  - skills/*/references/*.md
method: infographic:handdrawn-saas-wireframe
---

# Hand-Drawn SaaS Wireframe

Use this reference when the infographic should look like a monochrome,
hand-drawn product storyboard: multiple annotated SaaS dashboard states, dense
UI components, left navigation, callout arrows, and handwritten implementation
notes.

```text
handdrawn_saas_wireframe(brief, product_states, style_ref?)
  -> wireframe_storyboard_spec + prompt_or_renderer_plan + proof_notes
state: reads(brief, source facts, UI states, style reference asset); writes(layout spec, copy inventory, prompt/render plan, optional image asset)
gates: exact copy inventory; 2-4 coherent states; shared UI shell; annotations explain behavior/state; text-fidelity route chosen
fails: vague boxes with no product logic; decorative sketch with unreadable labels; copied source data without permission; image-model-only tiny text
```

## Use When

- The user wants an infographic like the reference asset at
  `examples/handdrawn-saas-wireframe/assets/reference.png`.
- The story is about product strategy, workflow states, app capabilities,
  automation, agents, dashboards, metrics, or operating model.
- The desired output is a visual thinking artifact, pitch diagram, spec sketch,
  product concept, or social/slide image.

## Inputs

```text
input_packet:
  required:
    - product or concept name
    - audience and purpose
    - 2-4 screens, states, or workflow moments
    - exact headings, labels, callouts, and important numbers
  optional:
    - aspect ratio: 3:2 landscape, 16:9, 1:1, or carousel panels
    - brand words to include or avoid
    - source data or proof links
    - final route: deterministic render, image model, or handoff prompt
  source_refs:
    - examples/handdrawn-saas-wireframe/assets/reference.png
```

## Workflow

1. **Storyboard the states.** Choose 2-4 named panels. Each panel should show a
   meaningful product state, not a random screenshot. Good panel names look like
   `Today - Workforce Pulse`, `Team - Digital Workers`, `Worker Profile`, and
   `Integrations`.
2. **Freeze the shared shell.** Reuse a consistent app frame across panels:
   thin outer browser border, left nav, logo box, active nav highlight, page
   title, tabs/chips, cards, tables, queues, and a right-side annotation lane.
3. **Write exact copy.** Build a copy inventory before drawing: panel titles,
   nav labels, table headers, card labels, chip text, metric values, callouts,
   button labels, and small notes. Mark placeholders.
4. **Compose for scan order.** Use thick panel boundaries, large circled
   numbers, generous section labels, and repeated component grammar so the eye
   moves panel by panel, then into callouts.
5. **Match the reference density.** Each large panel should include several
   distinct UI objects: metric cards or chips, one dense table/list/card grid,
   one secondary queue/detail area, and 2-4 annotation notes. A panel that is
   mostly empty whitespace is a failed match even if the line style is correct.
6. **Add behavioral annotations.** Callouts should explain state, data source,
   lifecycle, policy, approvals, or what is intentionally deferred. Avoid
   generic praise.
7. **Choose production route.** Use deterministic HTML/SVG/canvas when exact
   labels matter. Use image generation only for the hand-drawn texture or when
   labels can be manually corrected. A mixed route is often best: render the
   layout and text first, then add slight line wobble/noise.
8. **Verify.** Check that every panel has one job, every callout points to a
   real element, and no important text is too small to read at the final size.

## Visual Grammar

- Canvas: wide landscape, usually 1536x1024 or 16:9 when slide-bound.
- Palette: white background, black ink, light gray fills only for active nav,
  selected chips, separators, and minor emphasis.
- Line: thin uneven black strokes, rounded rectangles, simple icons, no color
  gradients, no drop shadows, no polished SaaS glass.
- Typography: handwritten print feel, uppercase only for page-level emphasis,
  compact labels, clear numeric hierarchy.
- Layout: 2x2 storyboard or one wide dashboard panel; shared left nav in every
  product panel; right-side callout lane with arrows.
- Components: metric cards, mini sparklines, status chips, worker cards,
  tables, tabs, queues, buttons, progress bars, integration cards, proof rows.
- Annotation tone: product/system notes such as `State:`, `Only show stale or
  unknown when provider sync is missing`, or `Mutations require approval`.

## Density Target

The provided reference is information-dense. Use this as the minimum bar for a
2x2 storyboard:

```text
density_target:
  per_panel:
    visible_ui_objects: 8-14
    exact_text_labels: 20-45
    annotation_notes: 2-4
    dense_regions:
      - top metric/chip/control band
      - main table/card/list/detail region
      - secondary queue/source/detail/limits region
      - right-side state notes with arrows
  whole_canvas:
    repeated_nav_shells: 4
    panels: 4
    empty_whitespace: intentional gutters only
```

Fail the style match when the output has the right monochrome sketch treatment
but fewer than roughly half of these information objects.

## Prompt Template

Use this only after the copy inventory exists:

```text
Create a monochrome hand-drawn SaaS product wireframe infographic on a white
background. It should be a dense 2x2 storyboard of <product/concept>, with
thin black uneven ink lines, rounded rectangles, simple icons, light gray fills,
handwritten print labels, and right-side annotation callouts with arrows.

Panel 1: <title>. Include <key components and exact labels>.
Panel 2: <title>. Include <key components and exact labels>.
Panel 3: <title>. Include <key components and exact labels>.
Panel 4: <title>. Include <key components and exact labels>.

Shared UI shell: left nav with <nav labels>, logo box, page title row, cards,
tables, chips, queues, and small product-state notes.

Constraints: readable text, exact labels from the copy inventory, no color
except light gray fills, no glossy UI, no photorealism, no gradients, no
decorative background, no extra fake brands or metrics.
```

## Deterministic Renderer Plan

Use this route when text fidelity matters:

```text
renderer_plan:
  canvas: 1536x1024
  layers:
    - background paper
    - 2x2 panel frames
    - repeated app shells
    - component rectangles and icons
    - text labels from copy inventory
    - arrows and callout notes
    - optional line jitter/noise overlay
  proof:
    - compare rendered text count against copy inventory
    - inspect at 100% and expected embed size
    - capture final PNG/SVG path
```

## Output Shape

```text
wireframe_storyboard_spec:
  title:
  canvas:
  panels:
    - number:
      title:
      job:
      components:
      copy:
      callouts:
  shared_shell:
  style_profile:
  production_route:
  prompt_or_renderer_plan:
  proof_notes:
```

## Quality Gates

- At least 2 panels and at most 4 panels unless the user asks for a carousel.
- The same product shell appears across product panels.
- Every panel has a state/job sentence.
- The copy inventory can be checked against the final asset.
- Right-side notes explain product behavior, not generic visual decoration.
- Each panel reaches the density target or records why a lighter panel is
  intentionally better for the user's format.
- The production route acknowledges text-fidelity risk.

## Bad Output

- A pretty sketch with fake unreadable UI text.
- A single generic dashboard with unrelated callouts.
- Four panels that do not share a product concept.
- Colorful polished SaaS mockup, 3D UI, gradients, or stock-photo background.
- A bitmap-only output where exact labels are the acceptance criterion.
