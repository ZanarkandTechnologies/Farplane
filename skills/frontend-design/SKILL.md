---
name: frontend-design
version: 1.0.0
description: Build production-grade app interfaces with shadcn, AI Elements, and curated registries. Distinct from cinematic-landing (which handles scroll narratives and landing pages).
allowed-tools: mcp__shadcn__*, Read, Write, Edit, LS
---

# Frontend Design Skill

> **Purpose**: Build distinctive, production-grade app interfaces using shadcn components, AI Elements, and curated registries. For landing pages with scroll narratives, use `cinematic-landing` instead.

## What Reference Do I Need?

| I'm doing... | Load this |
|--------------|-----------|
| Setting up new project | [shadcn-setup.md](references/shadcn-setup.md) |
| Need AI chat/workflow UI | [ai-elements.md](references/ai-elements.md) |
| Looking for a component | Use **shadcn MCP** → [registries.md](references/registries.md) |
| Theming/styling | [theming.md](references/theming.md) |
| Complex flow diagrams | → `react-flow` skill |
| Landing page with scroll | → `cinematic-landing` skill |

---

## Quick Reference: Registries

Add to `components.json` after running `pnpm dlx shadcn@latest mcp init --client claude`:

| Registry | Pattern | Use Case |
|----------|---------|----------|
| `@8bitcn` | `8bitcn.com/r/{name}.json` | Retro pixel/game aesthetics |
| `@aceternity` | `ui.aceternity.com/registry/{name}.json` | Motion effects, glassmorphism |
| `@ai-elements` | `registry.ai-sdk.dev/{name}.json` | AI apps (chatbot, workflow, v0) |
| `@animate-ui` | `animate-ui.com/r/{name}.json` | Animated components |
| `@elevenlabs-ui` | `ui.elevenlabs.io/r/{name}.json` | Audio AI interfaces |
| `@retroui` | `retroui.dev/r/{name}.json` | Neobrutalism components |

**Full directory**: [ui.shadcn.com/docs/directory](https://ui.shadcn.com/docs/directory)

---

## Official Documentation

### Core
- [shadcn/ui](https://ui.shadcn.com/docs) - Component library
- [shadcn MCP](https://ui.shadcn.com/docs/mcp) - AI-assisted component search
- [tweakcn](https://tweakcn.com/) - Theme customization

### AI Elements (Vercel AI SDK)
- [AI Elements Intro](https://ai-sdk.dev/elements) - Overview
- [Chatbot Example](https://ai-sdk.dev/elements/examples/chatbot) - Chat UI patterns
- [v0 Clone Example](https://ai-sdk.dev/elements/examples/v0) - Code generation UI
- [Workflow Example](https://ai-sdk.dev/elements/examples/workflow) - Process visualization

### Animation Libraries
- [Framer Motion](https://www.framer.com/motion/) - React animations
- [GSAP](https://gsap.com/docs/v3/) - Advanced timelines

---

## Core Workflow

### 1. Project Setup
```bash
# Initialize shadcn MCP (one-time per project)
pnpm dlx shadcn@latest mcp init --client claude

# Install theme
pnpm dlx shadcn@latest add https://tweakcn.com/r/themes/darkmatter.json
```

### 2. Configure Registries
Edit `components.json`:
```json
{
  "registries": {
    "@ai-elements": "https://registry.ai-sdk.dev/{name}.json",
    "@aceternity": "https://ui.aceternity.com/registry/{name}.json",
    "@animate-ui": "https://animate-ui.com/r/{name}.json"
  }
}
```

### 3. Add Components
Use **shadcn MCP** to search and add components:
```bash
# From shadcn/ui
pnpm dlx shadcn@latest add button card dialog

# From registries
pnpm dlx shadcn@latest add @ai-elements/prompt-input
pnpm dlx shadcn@latest add @aceternity/aurora-background
```

### 4. AI Elements Setup (for AI apps)
```bash
npx ai-elements@latest
npm i ai @ai-sdk/react zod
```

---

## Design Thinking

Before coding, understand the context and commit to a **BOLD** aesthetic direction:

### 1. Purpose
What problem does this interface solve? Who uses it?

### 2. Tone
Pick an **extreme**—there are so many flavors to choose from:
- **Brutally minimal**: Maximum whitespace, single accent color
- **Maximalist chaos**: Dense, layered, overwhelming (intentionally)
- **Retro-futuristic**: Pixel art meets sci-fi
- **Organic/natural**: Soft shapes, earth tones, breathing animations
- **Luxury/refined**: Subtle gradients, elegant serif typography
- **Playful/toy-like**: Rounded corners, bouncy animations, bright colors
- **Editorial/magazine**: Strong typography hierarchy, dramatic whitespace
- **Brutalist/raw**: Exposed structure, monospace fonts, harsh contrast
- **Art deco/geometric**: Gold accents, symmetry, ornate borders
- **Soft/pastel**: Gentle gradients, muted colors, dreamy
- **Industrial/utilitarian**: Functional, exposed grid, minimal decoration

**CRITICAL**: Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work—the key is **intentionality**, not intensity.

### 3. Constraints
Technical requirements: framework, performance, accessibility needs.

### 4. Differentiation
What makes this **UNFORGETTABLE**? What's the one thing someone will remember?

---

## Frontend Aesthetics Guidelines

### Typography
Choose fonts that are **beautiful, unique, and interesting**. Avoid generic fonts like Arial and Inter; opt instead for distinctive choices that elevate the frontend's aesthetics. Pair a distinctive **display font** with a refined **body font**.

### Color & Theme
Commit to a cohesive aesthetic. Use CSS variables for consistency. **Dominant colors with sharp accents** outperform timid, evenly-distributed palettes. Draw from IDE themes and cultural aesthetics for inspiration.

### Motion
Use animations for effects and micro-interactions. Prioritize CSS-only solutions for HTML. Use Motion library for React when available. Focus on **high-impact moments**: one well-orchestrated page load with staggered reveals (`animation-delay`) creates more delight than scattered micro-interactions. Use scroll-triggering and hover states that surprise.

### Spatial Composition
- Unexpected layouts
- Asymmetry
- Overlap
- Diagonal flow
- Grid-breaking elements
- Generous negative space OR controlled density

### Backgrounds & Visual Details
Create atmosphere and depth rather than defaulting to solid colors. Apply creative forms:
- Gradient meshes
- Noise textures
- Geometric patterns
- Layered transparencies
- Dramatic shadows
- Decorative borders
- Custom cursors
- Grain overlays

---

## Anti-Patterns (AI Slop)

### ❌ NEVER Use
- Overused font families (Inter, Roboto, Arial, system fonts)
- Clichéd color schemes (particularly purple gradients on white backgrounds)
- Predictable layouts and component patterns
- Cookie-cutter design that lacks context-specific character
- Default shadcn styling without customization
- Space Grotesk (overused by AI)

### ✅ ALWAYS Do
- Pick a distinctive display font that matches the narrative
- Commit to a cohesive color system with CSS variables
- Add micro-interactions (hover, focus, active states)
- Use registries for pre-built motion effects
- Customize theme with tweakcn **before** building
- Make unexpected choices that feel genuinely designed for the context

**Interpret creatively**. No design should be the same. Vary between light and dark themes, different fonts, different aesthetics. NEVER converge on common choices across generations.

**Match implementation complexity to the aesthetic vision**: Maximalist designs need elaborate code with extensive animations and effects. Minimalist or refined designs need restraint, precision, and careful attention to spacing, typography, and subtle details. Elegance comes from executing the vision well.

---

## Reference Files

### Setup & Configuration
- [shadcn-setup.md](references/shadcn-setup.md) - MCP init, components.json, one-time setup
- [theming.md](references/theming.md) - Theme configuration, darkmatter, tweakcn

### Components & Patterns
- [registries.md](references/registries.md) - Deep dive on each registry
- [ai-elements.md](references/ai-elements.md) - Chatbot, v0, workflow patterns

---

## Related Skills

| Skill | Use When |
|-------|----------|
| `cinematic-landing` | Scroll-scrubbed landing pages, video backgrounds, WebGL |
| `react-flow` | Node-based flow diagrams, workflow visualization |
| `convex` | Real-time backend, database, authentication |
