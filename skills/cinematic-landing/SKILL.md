---
name: cinematic-landing
version: 1.0.0
description: Build narrative-driven scroll experiences that avoid AI slop. Covers storytelling, scroll-scrubbing, WebGL effects, motion, and asset generation for cinematic landing pages.
allowed-tools: mcp__sequential-thinking__sequentialthinking, mcp__Parallel-search-mcp__web_search, Read, Write, Edit, LS, mcp__grep__searchGitHub
---

# Cinematic Landing Skill

> **Purpose**: Build distinctive, story-driven landing pages with scroll-scrubbed video, WebGL effects, and generated assets that look intentionally designed—not AI-generated.

## What Reference Do I Need?

| I'm doing... | Load this |
|--------------|-----------|
| Starting new landing page | [storytelling.md](references/storytelling.md) |
| Setting up scroll engine | [scroll-architecture.md](references/scroll-architecture.md) |
| Adding WebGL/shaders | [webgl-effects.md](references/webgl-effects.md) |
| Using Efecto-exported effects | [efecto.md](references/efecto.md) |
| Adding scroll-based animations | [motion-patterns.md](references/motion-patterns.md) → GSAP section |
| Adding hover/layout animations | [motion-patterns.md](references/motion-patterns.md) → Framer Motion section |
| Testing scroll behavior | [testing.md](references/testing.md) |

### GSAP vs Framer Motion

| Use Case | Recommended |
|----------|-------------|
| Video scrub to scroll | **Framer Motion + RAF** (production-proven) |
| Content opacity/transforms | **Framer Motion** |
| Simple hover/tap states | **Framer Motion** |
| Layout animations | **Framer Motion** |
| Complex multi-element timelines | **GSAP** (if needed) |
| Motion paths | **GSAP** (if needed) |

> **Default**: Use Framer Motion. Only add GSAP if you need complex timeline orchestration.

---

## Official Documentation

### Animation Libraries
- [Framer Motion](https://www.framer.com/motion/) - React animation
- [GSAP ScrollTrigger](https://gsap.com/docs/v3/Plugins/ScrollTrigger/) - Scroll-based timelines
- [GSAP + React](https://gsap.com/resources/React/) - Integration guide

### WebGL / 3D
- [React Three Fiber](https://docs.pmnd.rs/react-three-fiber) - React renderer for Three.js
- [Drei](https://github.com/pmndrs/drei) - R3F helpers (useVideoTexture, etc.)
- [PostProcessing](https://github.com/pmndrs/postprocessing) - Effects library

### Asset Generation
- [NanoBanana](https://replicate.com/fofr/nanobanana) - Stylized image generation
- [Kling](https://klingai.com/) - Video animation from images

### Visual Effects Tools
- [Efecto](https://efecto.app/) - ASCII, dither, glitch effects with **code export** → [efecto.md](references/efecto.md)
- [Tooooools](https://www.tooooools.app/) - Stippling, patterns, dithering, ASCII, CRT effects

---

## Core Workflow (5 Phases)

### Phase 1: Story Design
**Reference**: [storytelling.md](references/storytelling.md)

1. Write your **pitch** (Problem → Solution → CTA)
2. Create a **parable** that embodies the pitch
3. Extract **4 key visual scenes** from the parable
4. Choose a **style** (renaissance oil, pixel art, etc.)

### Phase 2: Asset Generation

**Mode A: Human-in-the-Loop** (default)
1. Agent brainstorms visual concepts and prompts
2. 🛑 **PAUSE** - Human generates assets using:
   - Images: [NanoBanana](https://replicate.com/fofr/nanobanana), Midjourney, etc.
   - Videos: [Kling](https://klingai.com/), Runway
   - Effects: [Efecto](https://efecto.app/), [Tooooools](https://www.tooooools.app/)
3. Human provides asset paths to agent
4. Agent encodes videos with FFmpeg and integrates

**Mode B: Automated** (if Replicate MCP available)
1. Agent generates assets via Replicate API
2. Agent downloads and encodes automatically
3. No human pause required

> 💡 **Efecto Tip**: Configure your ASCII/glitch effect in [efecto.app](https://efecto.app/), then export the code. See [efecto.md](references/efecto.md) for integration.

### Phase 3: Scroll Architecture
**Reference**: [scroll-architecture.md](references/scroll-architecture.md)

1. Define NARRATIVE timeline config
2. Set up sticky viewport container
3. Implement video scrubbing RAF loop
4. Layer backgrounds with z-index management

### Phase 4: Motion & Effects
**References**: [motion-patterns.md](references/motion-patterns.md), [webgl-effects.md](references/webgl-effects.md)

1. Add content overlays with opacity transforms
2. Implement WebGL effects (optional)
3. Add preloader for asset loading

### Phase 5: Testing & Polish
**Reference**: [testing.md](references/testing.md)

1. Test scroll at multiple breakpoints
2. Visual regression with Playwright
3. Performance audit (video compression, lazy loading)

---

## Style Presets

| Style | Characteristics | Best For |
|-------|-----------------|----------|
| **Renaissance Oil** | Rich textures, dramatic lighting, impasto effects | Luxury, authority, timelessness |
| **Pixel Art** | Retro gaming aesthetic, limited palette | Tech, gaming, nostalgia |
| **Brutalist** | Raw, monochrome, high contrast | Bold statements, disruption |
| **Cinematic** | Film grain, letterbox, moody lighting | Premium, storytelling |

---

## Anti-Patterns (AI Slop Checklist)

### ❌ Never Do
- Purple-to-blue gradients on white backgrounds
- Inter, Roboto, Space Grotesk, Arial fonts
- Static hero images with no motion
- Generic component-first layouts
- Unstyled shadcn defaults

### ✅ Always Do
- Commit to an extreme aesthetic (maximalist OR brutalist OR minimalist)
- Use distinctive display fonts that match the parable
- Add motion to every visible asset
- Use video backgrounds or animated WebGL
- Create depth with multi-layer parallax

---

## Reference Files

### Story & Design
- [storytelling.md](references/storytelling.md) - Pitch → Parable → Scene workflow

### Implementation
- [scroll-architecture.md](references/scroll-architecture.md) - NARRATIVE config, video scrubbing, preloader
- [webgl-effects.md](references/webgl-effects.md) - ASCII effect, shaders, R3F patterns
- [motion-patterns.md](references/motion-patterns.md) - **GSAP ScrollTrigger** + Framer Motion patterns
- [efecto.md](references/efecto.md) - Efecto code export integration

### Quality
- [testing.md](references/testing.md) - Playwright scroll testing workflow

### Templates
- [narrative-config.ts](templates/narrative-config.ts) - Configurable timeline template

---

## When to Add a Reference File

| Scenario | Action |
|----------|--------|
| Pure library feature | Link to official docs |
| Our pattern on top of library | Create reference file |
| Pattern from production codebase | Use transfer-learn to extract |
| Gotcha we discovered | Add to relevant reference file |

