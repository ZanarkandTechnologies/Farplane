# Compiled Spec: Terminal Industries Landing Page

> **Phase:** `spec`
> **Builder run:** `delegate-frontend-compiled-spec-live-1`
> **Date:** 2026-05-07
> **Route:** `cinematic-industrial-scroll` + `terminal-mission-control` + `video-frame-sequence-scroll-scrub`

## 1. Identity

| Field | Value |
|---|---|
| **Offer** | Warehouse computer vision operating system |
| **Audience** | Enterprise logistics, warehouse, yard, and supply-chain executives |
| **Carrier object / world** | Terminal Industries — a live logistics node (yard, dock, and warehouse perimeters) that transforms from raw physical chaos into an AI command surface as the user scrolls. |

## 2. Registry Route

- **Recipe ID:** `cinematic-industrial-scroll` *(closest registry match: `industrial-mission-control`)*
- **Taste Profile ID:** `terminal-mission-control` *(closest registry match: `terminal-palantir`)*
- **Effect Stack ID:** `video-frame-sequence-scroll-scrub` *(closest registry match: `cinematic-frame-sequence`)*

> **Note:** The exact IDs requested for this route do not yet exist in the landing-page JSON registries. This spec treats them as canonical IDs and maps compatibility to the existing registry records above. If implementation proceeds with the registry-native IDs, update the brief accordingly.

## 3. Story Arc

1. **The Yard as Reality** — A photographic, pre-rendered logistics world (trucks, docks, containers, yard traffic) dominates the first viewport. No vague SaaS UI wallpaper.
2. **Rupture / The Cost of Blind Spots** — As scroll begins, the frame sequence fractures: occlusion, delays, manual gate checks, and lost trailers become visible.
3. **The Command Layer** — Vision overlays appear: bounding boxes, trail labels, gate-state HUD, and route predictions resolve on top of the physical scene.
4. **Proof in Operations** — Three concrete missions (Truck & Trailer, Dock & Door, Yard & Inventory) with inspectable product states and metrics.
5. **Convert** — A stable, non-moving final section with enterprise CTA and credibility layer.

## 4. Section Map (7 Beats)

| # | Section | Narrative Role | Motion / Scroll Binding |
|---|---|---|---|
| 1 | **Hero — The Live Yard** | First signal: trucks, containers, yard traffic at dusk. | Pinned viewport; frame-sequence scrub from 0% → ~30% scroll. |
| 2 | **Tension — Blind Spots Cost Money** | Reveal the chaos: idling trucks, missed trailers, gate queues. | Continues pinned scrub; overlays (opacity + translateY) timed to frame phase. |
| 3 | **Mechanism — Vision OS Activates** | Command layer resolves: bounding boxes, HUD labels, state indicators. | Overlay timeline peaks here; frame sequence still drives background. |
| 4 | **Missions — Three Jobs the System Performs** | Inspectable proof cards for Truck/Trailer, Dock/Door, Yard/Inventory. | Native scroll ( unpinned ) with IntersectionObserver-driven reveal or light parallax. |
| 5 | **Proof — Metrics, Logos, Quotes** | Throughput numbers, operator quotes, deployment evidence. | Static or light fade-up; visually calmer than hero. |
| 6 | **Transition — The Transformed Yard** | A final, stable composite image: the yard now operating under full CV control. | Reduced-motion fallback becomes the canonical hero for this section. |
| 7 | **CTA — Schedule a Command-Center Briefing** | Single enterprise CTA, contact form, or scheduling module. | Fully static; no scrub dependency. |

## 5. Motion Checkpoints

| Progress | Narrative State | Frame / Visual State | Overlay State |
|---|---|---|---|
| **0%** | Hero at rest — live yard photograph / poster frame. Nav + primary CTA visible. H1: "The yard sees everything." | Frame 0 (or poster). Full photographic yard scene. | Minimal: nav, H1, CTA only. |
| **25%** | Tension onset — camera begins a slow lateral drift through the yard. Trucks idle, gate queue forms. | Frame ~90 (30fps, 3s into hero sequence). Slight desaturation / motion blur increases. | "1 in 4 trailers is misidentified" HUD label fades in top-right. |
| **50%** | Rupture peak — a single truck is "lost" in the frame; surrounding traffic continues. | Frame ~180. Selective dimming on the lost trailer; other vehicles sharp. | Chaos metrics overlay: delay counters, missed-scan badges, manual gate icons. |
| **75%** | Command layer resolves — bounding boxes snap onto every asset. Routes light up in signal green. | Frame ~270. Full vision overlay composited into frame sequence; image begins to stabilize. | HUD settles: "Vision OS active." Bounding boxes, confidence scores, ETA labels. Grid/map layer at 10% opacity. |
| **95%** | Transformed world — the yard is now an intelligent surface. Scrub ends cleanly before the native-scroll proof sections. | Final frame (or custom poster of the transformed yard). Stable, brightened detail. | All HUD transitions to reduced-motion still for the final CTA zone. |

## 6. Asset Prompts & Source Intent

All prompts follow the effect-stack rule: **no readable text, no logos, no CTAs baked into generated pixels.** Prose labels, button text, and brand marks stay in HTML/CSS overlays.

### Asset 1 — Hero Desktop Frame Sequence
- **Source intent:** Generated or pre-rendered cinematic video, then converted to frames via ffmpeg.
- **Prompt shape:**
  *Aerial dusk shot of a busy freight yard with semi-trucks, shipping containers, and a distribution dock. Slow lateral camera drift from left to right. Industrial sodium-vapor lighting mixed with deep twilight sky. Concrete, gravel, corrugated metal. High detail, photorealistic, cinematic color grade with restrained teal shadows and warm amber highlights. No readable text, no logos, no UI elements. Clean composition with strong depth layers for parallax-like separation. 4K, stable geometry.*
- **Output:** `public/frames/hero/desktop/webp/frame_%04d.webp` (30fps, ~300 frames for ~10s of scrub)

### Asset 2 — Hero Mobile Frame Sequence
- **Source intent:** ffmpeg rescale + re-crop of desktop source, or a separate generated video cropped for portrait readability.
- **Prompt shape:**
  *Vertical portrait aerial dusk shot of the same freight yard, re-composed so the central truck and dock remain in the upper-middle third. Same lighting, same material quality. No text, no logos. 1080p portrait, stable geometry.*
- **Output:** `public/frames/hero/mobile/webp/frame_%04d.webp` (24fps, ~240 frames)

### Asset 3 — Support Loop: Dock Door Close-Up
- **Source intent:** Short generated video loop for the Missions section background or inline card media.
- **Prompt shape:**
  *Close-up of a distribution dock door from an interior warehouse perspective. A trailer backs into the bay; overhead LED strips light the container interior. Reflections on polished concrete floor. POV is static, 3-6 second seamless loop. No readable text, no faces. High detail, photorealistic, cinematic warm industrial grade.*
- **Output:** `public/video/dock-loop-01.mp4` (H.264, CRF 23, faststart)

### Asset 4 — Support Still: Transformed Yard (Reduced-Motion Hero & Poster)
- **Source intent:** Single high-detail still extracted from the final frame of the hero sequence, or generated as a still.
- **Prompt shape:**
  *The same freight yard at dusk, but now every truck and container has a faint, subtle bounding-box glow and route-line overlay, suggesting AI visibility rather than literal UI. Clean, stable, authoritative. No text, no logos. High detail, photorealistic, 4K.*
- **Output:** `public/frames/hero/poster.webp` (poster) and `public/frames/hero/reduced-motion.webp` (reduced-motion canonical)

## 7. File Map & Implementation Slices

Planned implementation passes (for future phases only):

| Slice | Files | Owner Pass |
|---|---|---|
| Shell + layout | `index.html`, `Layout.tsx` | `implementation-1` |
| Styles + tokens | `globals.css`, `tokens.css` | `implementation-1` |
| Asset manifest + loader | `assets.ts`, `FrameManifest.json` | `implementation-2` |
| Scroll-scrub engine | `CinematicScrollPage.tsx`, `FrameSequence.tsx` | `implementation-2` |
| Overlay + HUD | `OverlayHUD.tsx`, `MissionCards.tsx` | `implementation-3` |
| Proof + CTA sections | `ProofSection.tsx`, `CTASection.tsx` | `implementation-3` |
| Debug instrumentation | `ScrollDebugHud.tsx`, `useScrollScrub.ts` | `implementation-2` |

## 8. Scroll-Scrub Instrumentation Contract

Per `effect-stacks.json` and `landing-page/references/qa.md`, the pinned stage must expose:

- `data-scroll-scrub-root` attribute on the scrubbed stage element.
- `window.__scrollScrubDebug` object with:
  - `.progress` — 0 to 1
  - `.phase` — string, maps to narrative beat (e.g., `"hero"`, `"tension"`, `"command"`, `"transformed"`)
  - `.frame` — integer frame index, OR `.mediaTime` if using video element
  - `.active` — boolean, is the scrub timeline active
  - `.ready` — boolean, are enough frames loaded for the current segment
  - `.reducedMotion` — boolean, matches `prefers-reduced-motion`

This contract must remain available in production builds unless a future ticket explicitly scopes a removal pass.

## 9. QA Plan

| QA Lane | Check | Method |
|---|---|---|
| **Desktop** | First viewport signals physical yard, H1 + CTA visible, nav usable, no overlap. | Screenshot at 1440×900 and 1920×1080. |
| **Mobile** | Portrait reframe preserves central truck/dock, H1 + CTA fit above fold, no text overlap. | Screenshot at 390×844 and 414×896. |
| **Reduced Motion** | `prefers-reduced-motion: reduce` renders `reduced-motion.webp` as static hero, all HTML overlays present, CTA reachable without scrub. | Browser toggle + manual scroll. |
| **Scroll-Scrub** | `window.__scrollScrubDebug` populates; checkpoints at 0%, 25%, 50%, 75%, 95% map to distinct narrative states with nonblank frame surfaces. | `skills/landing-page/scripts/scroll_scrub_qa.cjs --url <page> --out <qa-dir>` |
| **Visual Geometry** | Text never overlaps generated media; bounding boxes / HUD remain legible at all breakpoints; no layout shift after frame load. | Visual-diff per breakpoint. |
| **Review** | Run `review` skill for code quality and `web-design-guidelines` for source-level UI compliance. | Automated review pass in same Pi thread post-implementation. |

## 10. Next Phase Prompt

After Codexter approves this spec, proceed to:

**Phase: `assets`**
Generate or create the four asset items above (desktop frame sequence, mobile frame sequence, support loop, poster/reduced-motion still). Verify every referenced path returns 200. Write `assets/asset-manifest.json` with frame counts, dimensions, and source prompts. Produce a handoff before implementation.
