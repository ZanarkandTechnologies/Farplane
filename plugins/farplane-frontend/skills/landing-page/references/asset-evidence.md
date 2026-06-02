# Asset Evidence Gate

Use this for premium, cinematic, generated-media, Terminal-style, or
visually ambitious landing pages.

## Rule

A premium generated-media landing page is not proved by code-native visuals
alone. Canvas, Three.js, and HTML/CSS visual systems can support the page, but
the page must include at least one real or generated filesystem-backed hero or
primary product media asset before it can claim premium/cinematic quality. For
premium landing graphics, do not create custom SVG illustrations or SVG diagram
overlays; use generated/real raster media or real WebGL/Three.js scenes instead.

For product, device, hardware, equipment, or object-focused pages, that primary
asset must be product-relevant: realistic product photography/render, product in
use, product macro/detail, assembly/disassembly, exploded view, or feature
callout sequence. Generic infographics, abstract diagrams, or random contextual
photos are support assets only.

## Required Evidence

The final site must include `assets/asset-manifest.json` with:

- page name and quality target,
- at least one primary media asset with a generated or real provenance,
- saved asset path or path list that exists in the workspace,
- poster or first-frame fallback,
- reduced-motion still or explicit static fallback,
- alt text,
- source prompt, capture source, model/tool, or real-asset provenance,
- video-generation provenance for `generated-video` assets: `videoModel`,
  `videoProvider`, `sourceVideo`, `sourceVideoPath`, `sourceVideoModel`, or a
  recognized video-generation app/model,
- product-demo role when the page sells a physical product or equipment,
- QA notes for asset loading and first viewport.

Accepted primary media types:

- `generated-video`
- `generated-image`
- `generated-product-shot`
- `product-render`
- `product-photography`
- `assembly-video`
- `exploded-view-sequence`
- `frame-sequence`
- `source-video`
- `filmed-video`
- `photography`
- `real-product-image`
- `edited-image`

Prototype-only or support-only types:

- `code-rendered-canvas`
- `html-css-visual`
- `three-js`
- `webgl`
- `procedural`

Hand-authored section SVGs are not valid premium visual carriers. SVG remains
acceptable only for tiny UI icons, logos, or imported icon systems; do not
declare custom section SVG illustrations as landing-page asset evidence.

Support-only types may appear in the manifest, but they do not satisfy the
premium asset evidence gate by themselves.

`generated-video` means a video-generation model or real source video produced
motion. A local `ffmpeg` transcode is allowed as packaging only when it starts
from a real/generated source video and records that source. An MP4 assembled
from generated still images, Seedream outputs, or a short image sequence must be
declared as `frame-sequence` or downgraded to prototype; it cannot satisfy a
premium generated-video requirement.

## Build Rule

If a page cannot generate or collect media during the current run, downgrade the
quality target to `prototype`, mark the missing media as a blocker, and do not
claim the page is premium, Terminal-level, cinematic-final, or production-ready.

## QA Rule

Run:

```bash
python3 skills/landing-page/scripts/asset_evidence_lint.py <site-dir>
```

before final landing-page claims. A passing section-quality score is not enough
when the premium lane requires generated or real assets.
