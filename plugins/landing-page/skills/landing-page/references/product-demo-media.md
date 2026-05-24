# Product Demo Media

Use this for product, device, hardware, equipment, vehicle, robotics, wearable,
medical-device, industrial-system, and object-focused landing pages.

## Core Rule

The primary media must let the buyer inspect the actual thing being sold. A
generic infographic, abstract SVG, hand-authored SVG diagram, dashboard mock,
orbiting lines, or decorative render cannot be the hero proof for a physical
product page.

## Required Product Demo Plan

Premium product specs must include a `Product Demo Plan` that answers:

- What realistic product shot anchors the first viewport?
- What in-context use shot shows where the product lives?
- What assembly, disassembly, exploded-view, or feature-reveal sequence shows
  the product's meaningful parts?
- Which parts/features are highlighted, and why do they matter to the buyer?
- What media assets exist or must be generated for desktop, mobile, poster, and
  reduced-motion fallback?
- What QA proves the sequence shows meaningful product states rather than a
  short decorative scrub?

## Preferred Media

- Real product photography when supplied or legally usable.
- Generated product photography/renders when no real asset exists.
- Product macro/detail shots: lens, sensor, enclosure, fasteners, materials,
  connector, battery, compute module, mounting, control surface.
- In-context use shots with the product clearly visible.
- Assembly/disassembly or exploded-view sequences where parts move apart and
  return together.
- Feature callout sequences where the visual shows function, not just labels.

## Product Clarity / Accessibility Gate

The product must remain inspectable before style is judged. A cinematic page
fails when the object is hidden by dark color washes, low-opacity video, tiny
crops, unreadable contrast, strong WebGL overlays, or decorative noise.

Minimum checks:

- hero product or primary demo product is large enough to inspect on desktop
  and has an intentional mobile fallback;
- product media renders at full or near-full opacity;
- WebGL/GSAP/HUD effects support the story without covering the product;
- section text meets normal contrast expectations against its background;
- all product and section images have alt text, width, and height attributes;
- keyboard focus is visible and skip-link/main-content navigation exists;
- reduced-motion fallback still shows the product clearly.

Record a `product_clarity_score` in QA. Premium product pages should target
90+ before final claims.

## Product Disassembly / Exploded-View Score

Use a dedicated teardown score for assembly/disassembly media. Score against:

- **Object continuity:** the assembled, separating, exploded, and reassembled
  states clearly depict the same product.
- **Component specificity:** visible lenses, sensors, circuit boards,
  batteries, fasteners, casing, mounts, or other product-specific parts.
- **Separation clarity:** components float apart with readable spacing and a
  clean engineering layout rather than visual clutter.
- **Product clarity:** product silhouette and key parts remain easy to see.
- **Lighting and background:** clean studio or context lighting with enough
  contrast and soft shadows.
- **No baked text:** no readable letters, numbers, fake labels, watermarks, or
  alphanumeric quality words rendered into the pixels.
- **Sequence meaning:** the states tell a story beyond a decorative label swap.

Premium product pages should target 80+ disassembly score and 90+ product
clarity score.

## Product Disassembly Prompt Template

Use detailed prompts for still frames or video planning, but avoid putting
visible words like `8K` in the scene where the model may render them as text.

```text
professional ultra-detailed photorealistic studio teardown of [product],
showcasing every internal and external component meticulously floating apart in
mid-air, straight-on camera, [specific components], clean minimalist white
background, dramatic cinematic studio lighting with soft shadows, technical
engineering teardown style, photorealistic, no readable text, no numbers, no
logos, no watermarks baked into pixels
```

For fast variants:

```text
clean exploded view of [product], internal and external components floating
apart, [specific components], photorealistic studio lighting, detailed interior
parts, white background, no readable text or alphanumeric markings
```

## Scroll / Video Requirements

For product scroll scrub, plan at least four meaningful states:

1. hero product in context,
2. product isolated or stabilized,
3. product parts/layers reveal,
4. feature callout or reassembled final state.

Short loops that only change text labels, tint, or generic HUD overlays do not
count as meaningful product animation.

For premium hero or product scrub, prefer a longer authored sequence over a
quick image swap: 8-15+ seconds of seekable video or a 96+ frame sequence, with
named beats and at least one synchronized effect layer such as GSAP timeline
overlays, WebGL scan/field effects, Three.js product staging, or HTML beat
panels. QA must sample the beat changes and the effect layer, not just the
final frame source.

## Generated Asset Prompt Shape

Prompts should specify:

- product form factor,
- material and scale,
- use context,
- parts/layers to reveal,
- camera angle and lighting,
- no readable text baked into pixels,
- mobile crop needs,
- poster/reduced-motion frame.
- no visible alphanumeric quality labels rendered into the image.

Example:

```text
realistic premium medical XR glasses product render in a sterile operating room,
optical waveguide lens, sensor bar, battery temple, lightweight frame, exploded
view sequence showing lens, sensor, compute module, and temple assembly,
restrained clinical lighting, no readable text baked into image
```

## Anti-Patterns

- Replacing product shots with abstract workflow diagrams.
- Replacing product shots with custom SVG illustrations or SVG overlays.
- Reusing the same generic support image across multiple sections.
- Showing a random adjacent object instead of the product being sold.
- Treating UI/HUD overlays as product evidence.
- Hiding the product behind copy, dark overlays, or tiny nav/logo treatment.
