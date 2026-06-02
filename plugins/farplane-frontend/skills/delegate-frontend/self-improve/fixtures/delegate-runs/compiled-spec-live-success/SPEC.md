# Compiled Spec Live 2 — Enterprise Warehouse CV Landing Page

## Phase
`spec`

## Route
- **recipe_id**: `cinematic-industrial-scroll`
- **taste_profile_id**: `terminal-mission-control`
- **effect_stack_id**: `video-frame-sequence-scroll-scrub`

> Registry references used for content fidelity:
> - Recipe closest match: `industrial-mission-control`
> - Taste profile closest match: `terminal-palantir`
> - Effect stack closest match: `cinematic-frame-sequence`

---

## Offer
Enterprise-grade computer vision and operational intelligence platform built for warehouse / distribution-center / fulfillment operations. The product turns every pallet, truck, aisle, and scanner event into machine-readable telemetry — enabling real-time inventory tracking, autonomous anomaly detection, operator safety compliance, and throughput optimization at terminal-level industrial scale.

**Literal value proposition**: "See what’s inside every truck, every pallet, every shift — before your operators walk the floor."

## Audience
- Primary: VP of Operations / General Manager at 3PL, national distribution center, or large-scale retail fulfillment network.
- Secondary: Head of Supply Chain, Chief Information Officer evaluating AI-powered warehouse initiatives.
- Gatekeeper: Engineering lead who needs to know the system installs on existing camera infrastructure.
- Motivation: Reduce shrink, accelerate receiving accuracy, and make yard management predictable.

## Carrier Object / World
**Physical warehouse / distribution yard becomes a digital command surface.**

The scroll narrative carries the audience through the same physical world from two states:
1. **Raw operation** (pre-dawn trucking yard, unlabeled pallets, manual scan gaps, operator near-misses).
2. **Command layer** (AI-labeled freight, real-time manifest reconstruction, spatial heat maps, predictive yard scheduling).

The carrier object is the warehouse itself — specifically the receiving dock and first-mile yard — rendered as an immersive pre-dawn industrial environment that transforms into a precise instrumentation layer.

---

## Story Arc
**Problem → Shift → Proof → Action**

1. **Problem**: Yard chaos — inbound trucks, misplaced pallets, clipping scans, near-miss incidents.
2. **Shift**: CV system turns the same camera feeds into a live operating system with labeled cargo, spatial maps, and predictive signals.
3. **Proof**: Concrete throughput metrics, operational outcome comparisons, operator safety deltas.
4. **Action**: Talk to a warehouse solutions engineer.

---

## Section Map (8 Sections / Beats)

### Beat 1 — First Viewport: Pre-Dawn Yard
- Full-viewport cinematic frame of a dark distribution yard at blue hour.
- Headlights on trucks, warehouse loading bay inactive, fog / sodium vapor.
- Headline: every truck and pallet, before dawn, in one frame.
- CTA: *See a demo* — nav is pinned, dimmed, industrial grotesk.
- Asset: desktop hero frame sequence (pre-dawn → sunrise transformation).

### Beat 2 — The Operation: Inbound Chaos
- Scroll-pinned section. The yarn unfolds the raw state:
  - Inbound trucks queued.
  - Pallets scanned or missed.
  - Forklifts maneuver in partial visibility.
- Headline: The world your operators navigate every shift.
- Overlay labels with numbers: trucks in yard, scan accuracy rate, near-miss count.
- Asset: frame sequence continues, camera locks onto the open truck trailer.

### Beat 3 — The Rupture: What the Cameras See
- The shift beat. Camera feeds layer onto the physical world like a digital grid.
- Overlay dots, bounding boxes, and cargo labels appear on the frame.
- Headline: Your cameras already see everything. Start reading it.
- Sub-lineal: No retrofit. No new hardware. Same feeds, new intelligence.
- Asset: support loop showing bounding-box detection on a pallet stack.

### Beat 4 — Three Missions
- Calmer proof section. Three concrete jobs the system performs:
  1. **Manifest Autopsy** — reconstruct missing inbound manifests from camera evidence.
  2. **Spatial Inventory** — map pallet locations floor-to-rack in real time.
  3. **Safety Gate** — flag near-miss events and PPE violations before incident reports.
- Each mission shows a compact metric card + a nearby support loop or still.
- Asset: 3 support loops (or generated stills) — one per mission.

### Beat 5 — Live Command Surface
- Return to cinematic pinned section. The warehouse is now fully annotated.
- Command-overlay grid: Yard status, dock-door schedule, predicted unload times, flagged anomalies.
- Headline: A terminal for your terminal.
- Animation: frame sequence reaches full-dawn command grid.
- Asset: frame sequence concluding, HUD overlay layers in code.

### Beat 6 — Metrics Proof
- Quiet text-forward section. Before / after comparison:
  - Receiving accuracy: 84% → 97%
  - Unload-to-slot time: 4.2h → 1.8h
  - Shrink events per month: 22 → 4
  - Near-miss incidents flagged: 0/month → 311/month
- Logo bar of referenceable enterprise clients.
- Asset: code-native typography and metric cards only.

### Beat 7 — Capability Details
- Expandable accordion + summary cards for:
  - Multi-camera fusion & 3D reprojection
  - Edge-to-cloud deployment
  - WMS / TMS / YMS integration
  - SOC 2 Type II & ITAR readiness
- Asset: code-native UI, no generated media needed here.

### Beat 8 — Final CTA: Schedule an Evaluation
- Stable final viewport. The transformed yard at sunrise.
- Primary CTA: *Schedule evaluation* (calendar integration).
- Secondary CTA: *Download architecture brief* (PDF).
- Contact form minimal: Name, Company, Email, Center volume.
- Asset: poster frame / reduced-motion still of sunrise command yard.

---

## Asset Plan

All readable text, logos, CTAs, and labels remain in HTML/CSS overlays per the Terminal-style gate.

### Asset Manifest
`assets/asset-manifest.json`

### Asset Prompts (4 primary)

**A1 — Desktop Hero Frame Sequence (Source: video-generation)**
- *Prompt*: Cinematic wide shot of an industrial distribution yard at pre-dawn blue hour, trucks backed into loading bays, fog rolling over asphalt, sodium vapor lights casting amber through mist, cold industrial palette with deep charcoal and dark forest green, slow dolly camera movement forward through the yard, shot composition leaves center top third empty for HTML overlay headline, no readable text, no logos, steady geometry, high detail, photorealistic cinematic style, 3-second motion suitable for scroll-scrub frame extraction.
- *Intent*: Full-viewport hero opening; establishes physical world before the transformation.
- *Output*: hero-source-desktop.mp4 → frame extraction pipeline.

**A2 — Mobile Hero Frame Sequence (Source: video-generation)**
- *Prompt*: Vertical cinematic shot of the same industrial distribution yard at pre-dawn blue hour, trucks and loading bay doors visible, fog and sodium vapor lights, cold industrial palette with deep charcoal and dark forest green, slow camera push forward, composition centers on one truck trailer leaving upper half open for HTML overlay text, no readable text, no logos, steady geometry, high detail, photorealistic cinematic style, 3-second motion.
- *Intent*: Mobile scroll-scrub hero; deliberate portrait crop, not a shrunken desktop composition.
- *Output*: hero-source-mobile.mp4 → frame extraction pipeline.

**A3 — Manifest Autopsy Detection Loop (Source: video-generation)**
- *Prompt*: Close-up tracking shot of a forklift unloading labeled cardboard boxes from a flatbed trailer inside a high-ceiling warehouse, boxes marked with barcodes, warm industrial lighting, cold desaturated palette with charcoal walls, cinematic but operational feel, no readable text, no logos, smooth camera motion, high detail, 3-second seamless loop.
- *Intent*: Support loop for Beat 4 "Manifest Autopsy" mission card.
- *Output*: mission-01-manifest.mp4

**A4 — Sunrise Command Yard Still (Source: image-generation)**
- *Prompt*: Aerial dawn view of a fully operational industrial distribution yard, trucks organized at bays, clean lanes, modern warehouse roof with solar panels, warm sunrise light breaking through overcast sky, subtle digital overlay grid lines visible but faint, photorealistic, high detail, cinematic industrial photography, cold palette with restrained warm amber sunrise accents, no readable text, no logos, composition balanced for top HTML overlay.
- *Intent*: Poster frame, reduced-motion fallback, and final CTA background still.
- *Output*: yard-sunrise-command.webp

**A5 — Safety Gate Detection Loop (Source: video-generation)** *(recommended but optional beyond the 4 required)*
- *Prompt*: Interior warehouse aisle, warehouse worker in high-vis vest approaching a forklift intersection, overhead LED lighting, deep charcoal palette, camera slowly tracking left, the worker is centered, industrial cinematic tone, no readable text, no logos, 3-second loop.
- *Intent*: Support loop for Beat 4 "Safety Gate" mission card.
- *Output*: mission-03-safety.mp4

### Frame Extraction Pipeline
```bash
ffmpeg -i hero-source-desktop.mp4 -vf "fps=30,scale=1920:-2:flags=lanczos" -q:v 75 public/frames/hero/desktop/webp/frame_%04d.webp
ffmpeg -i hero-source-mobile.mp4 -vf "fps=24,scale=1080:-2:flags=lanczos" -q:v 80 public/frames/hero/mobile/webp/frame_%04d.webp
ffmpeg -ss 00:00:00 -i hero-source-desktop.mp4 -frames:v 1 public/frames/hero/poster.webp
```

### Fallback Assets
- `poster.webp`: Extracted from the first frame of desktop hero; shown while frames preload.
- `reduced-motion-still.webp`: `yard-sunrise-command.webp` repurposed as the static reduced-motion hero.
- Mobile frame sequence is distinct from desktop (not a downscaled crop).

---

## Motion Plan

### Primary Effect Stack
Video frame sequence scroll-scrub via GSAP ScrollTrigger pinned timelines, with HTML/CSS HUD overlays decoupled from media.

### Frame Sequence Mapping
| Scroll % | Phase | Frame Index | Narrative State |
|----------|-------|-------------|-----------------|
| 0% | `intro` | 1–12 | Pre-dawn yard, static atmosphere, no overlays. |
| 25% | `problem` | 30–54 | Camera locked on yard. Metric labels fade in: trucks queued, scan gaps, incidents. |
| 50% | `rupture` | 72–90 | Detection grid and bounding boxes begin overlaying the physical yard. |
| 75% | `command` | 108–132 | Fully annotated command surface. HUD overlays (dock schedule, heat map, predicted times) become primary. |
| 95% | `proof` | 150–180 (hold) | Camera settles into sunrise command surface. Proof metrics and features transition in over reduced-motion safe zone. |

- Total frames: ~180 at 30fps (≈6 seconds of scrub-friendly motion).
- Frame format: WebP for bandwidth; JPEG fallback if needed.
- Frame load strategy: load + decode first 30 frames immediately, lazy-load remainder.

### Overlay Motion
- Fade + slight translateY on labels as each phase boundary crosses.
- Metric labels use CSS `will-change: transform, opacity` with `transform: translate3d()`.
- No blur/backdrop-filter on overlay panels to preserve scroll performance.

### Reduced Motion
- When `prefers-reduced-motion: reduce`:
  - Frame sequence replaced by static `reduced-motion-still.webp`.
  - Pinned scroll sections become normal flow.
  - Overlays fade in with no scroll-driven scrub; state controlled by IntersectionObserver thresholds.
  - `window.__scrollScrubDebug.reducedMotion = true`.

### Debug / Instrumentation Contract
- Scrubbed stage element: `data-scroll-scrub-root`.
- Global debug object:
  ```ts
  window.__scrollScrubDebug = {
    progress: 0.0,        // 0.0–1.0 (scroll-driven)
    phase: "intro",       // intro | problem | rupture | command | proof
    frame: 1,             // current displayed frame index
    active: true,         // ScrollTrigger is active/pinned
    ready: false,         // enough frames loaded for current phase
    reducedMotion: false, // matches prefers-reduced-motion
    breakpoint: "desktop" // desktop | mobile
  };
  ```
- Query params for force state: `?debugScroll=1`, `?phase=rupture`, `?frame=90`.

---

## QA Plan

### Desktop QA
- Open page at 1440×900 / 1920×1080.
- First viewport must clearly signal industrial warehouse/yard domain.
- Nav and primary CTA are immediately visible and clickable.
- Overlay text does not overlap media at any pinned scroll position.
- All frame / poster URLs return 200.
- Final CTA section is stable, not pinned/scrolled-away unexpectedly.

### Mobile QA
- Open page at 390×844 (iPhone 14 proxy).
- Hero composition uses distinct mobile crop (vertical composition).
- Text remains legible without zoom; no horizontal overflow.
- Pinned sections do not trap scroll.
- Touch targets ≥ 44×44.

### Reduced Motion QA
- Enable `prefers-reduced-motion: reduce`.
- Static background image replaces frame sequence.
- Overlay content still appears in document order; no blank sections.
- CTA remains accessible without scroll-scrub dependency.

### Scroll-Scrub QA
- Run: `skills/landing-page/scripts/scroll_scrub_qa.cjs --url <page> --out <qa-dir>`
- Assert:
  - `hasRequiredDebugContract === true`
  - `window.__scrollScrubDebug.progress` advances across checkpoints.
  - `frame` or `mediaTime` changes across checkpoints.
  - Canvas/image surface is nonblank at each checkpoint.
  - Checkpoint 0%/25%/50%/75%/95% map to expected phases.

### Visual Geometry QA
- Primary CTA region: expected `x/y` within [85,100] / [5,20], width [8,20] / height [5,12] (viewport pct).
- Header pinned to top with clear boundary.
- No overlap between overlay text and HUD-style grid at mobile widths.
- Baseline alignment of metric cards in Beat 6.

### Review QA
- Source review includes `web-design-guidelines` via `review` skill `frontend-guidelines` rubric.
- Artifact scoring alongside `ui-quality` for taste judgment.
- Evaluate: media quality, text contrast, motion performance, asset pipeline.

### Maximum Checkpoint Delta
- At adjacent checkpoints (0%→25%→50%→75%→95%), the visual screenshot changed ratio must exceed 8% per checkpoint to pass cinematic scrub; ratios below 4% indicate stagnant scrub and fail visual parity.

---

## File Map & Implementation Slices

### Slice A — HTML Shell + Styles
- `index.html` — root, loads assets, font preconnect, reduced-motion support class.
- `src/styles/global.css` — Terminal/Palantir palette, typography scale, spacing tokens.
- `src/styles/landing.css` — section spacing, pinned states, overlay positioning.

### Slice B — Assets + Frame Manifest
- `public/frames/hero/desktop/webp/*.webp`
- `public/frames/hero/mobile/webp/*.webp`
- `public/frames/hero/poster.webp`
- `public/frames/hero/reduced-motion-still.webp`
- `src/lib/assets.ts` — manifest loader, frame preloader, path builder.
- `assets/asset-manifest.json` — canonical list of all generated/rendered media.

### Slice C — Scroll Engine
- `src/lib/scrollEngine.ts` — frame-to-progress mapping, phase detection, lazy loader.
- `src/components/FrameSequence.tsx` — canvas or `<img>` renderer with RAF throttle.
- `src/components/ScrollDebugHud.tsx` — optional debug overlay (enabled by `?debugScroll=1`).

### Slice D — Page Sections
- `src/sections/HeroSection.tsx` — Beat 1 + scrubbed container.
- `src/sections/InboundChaosSection.tsx` — Beat 2.
- `src/sections/DetectionRevealSection.tsx` — Beat 3.
- `src/sections/MissionsSection.tsx` — Beat 4.
- `src/sections/CommandSurfaceSection.tsx` — Beat 5.
- `src/sections/MetricsSection.tsx` — Beat 6.
- `src/sections/CapabilitiesSection.tsx` — Beat 7.
- `src/sections/FinalCTASection.tsx` — Beat 8.

### Slice E — Integration + Performance
- `src/components/PinnedStage.tsx` — `data-scroll-scrub-root` wrapper with resize observer.
- `src/components/SafeOverlay.tsx` — positioned text layer with safe-zone margins per breakpoint.
- `src/lib/reducedMotion.ts` — media query watcher + fallback control.

---

## Gold-Reference Comparison Checklist
- [ ] First viewport shows a physical-world operation (yard/truck/dock), not a generic software mockup.
- [ ] Media reads as photographic or intentionally art-directed, not SVG/code-native filler.
- [ ] Nav and CTA are enterprise-serious and immediately usable.
- [ ] Product category signal (warehouse CV) appears before scrolling.
- [ ] Mobile has a deliberate vertical crop, not a shrunken desktop composition.
- [ ] Hint of next section is visible without a dead blank band.
- [ ] Scroll checkpoints map to narrative phases, not random motion.
- [ ] Reduced-motion fallback is a strong static composition, not a blank space.
</details>
