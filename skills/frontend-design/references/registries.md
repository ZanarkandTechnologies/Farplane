# Shadcn Registries: Component Libraries Index

> **When to use**: Looking for the right registry/component for your use case.

## Registry Overview

| Registry | Aesthetic | Best For |
|----------|-----------|----------|
| **@ai-elements** | Clean, functional | AI apps, chatbots, workflows |
| **@aceternity** | Glassmorphism, motion | Landing pages, hero sections |
| **@animate-ui** | Smooth transitions | Interactive components |
| **@8bitcn** | Pixel art, retro | Gaming, nostalgic themes |
| **@retroui** | Neobrutalism | Bold, statement pieces |
| **@elevenlabs-ui** | Audio-focused | Voice AI, audio apps |

---

## @ai-elements (AI SDK)

**URL**: `https://registry.ai-sdk.dev/{name}.json`  
**Docs**: [ai-sdk.dev/elements](https://ai-sdk.dev/elements)

Pre-built components for AI applications:

| Component | Use Case |
|-----------|----------|
| `prompt-input` | Rich chat input with attachments, model picker |
| `conversation` | Chat message container with scroll |
| `message` | Message bubble with actions |
| `reasoning` | Expandable thinking display |
| `sources` | Citation display |
| `loader` | AI thinking indicator |
| `suggestion` | Quick action chips |
| `web-preview` | Iframe preview (v0-style) |
| `task` | Progress/status display |

```bash
# Full AI chat kit
pnpm dlx shadcn@latest add @ai-elements/prompt-input @ai-elements/conversation @ai-elements/message @ai-elements/reasoning @ai-elements/sources @ai-elements/loader
```

---

## @aceternity

**URL**: `https://ui.aceternity.com/registry/{name}.json`  
**Docs**: [ui.aceternity.com](https://ui.aceternity.com)

High-impact visual effects:

| Component | Effect |
|-----------|--------|
| `aurora-background` | Animated gradient aurora |
| `spotlight` | Mouse-following spotlight |
| `background-beams` | Animated beam lines |
| `tracing-beam` | Scroll-following line |
| `text-generate-effect` | Typing animation |
| `sparkles` | Particle sparkle effect |
| `3d-card` | Perspective tilt on hover |
| `infinite-moving-cards` | Auto-scrolling carousel |

```bash
# Hero section kit
pnpm dlx shadcn@latest add @aceternity/aurora-background @aceternity/spotlight @aceternity/text-generate-effect
```

---

## @animate-ui

**URL**: `https://animate-ui.com/r/{name}.json`  
**Docs**: [animate-ui.com](https://animate-ui.com)

Animated versions of common components:

| Component | Animation |
|-----------|-----------|
| `accordion` | Smooth expand/collapse |
| `button` | Press/hover effects |
| `dialog` | Scale/fade transition |
| `dropdown-menu` | Slide animations |
| `tabs` | Underline/slide indicator |
| `tooltip` | Fade with delay |

```bash
# Animated essentials
pnpm dlx shadcn@latest add @animate-ui/button @animate-ui/dialog @animate-ui/tabs
```

---

## @8bitcn

**URL**: `https://www.8bitcn.com/r/{name}.json`  
**Docs**: [8bitcn.com](https://www.8bitcn.com)

Pixel art / retro gaming aesthetic:

| Component | Style |
|-----------|-------|
| `button` | Pixel borders, press effect |
| `card` | 8-bit frame |
| `input` | Retro text field |
| `progress` | Pixel loading bar |
| `badge` | Pixel label |

```bash
# Retro gaming UI
pnpm dlx shadcn@latest add @8bitcn/button @8bitcn/card @8bitcn/progress
```

---

## @retroui

**URL**: `https://retroui.dev/r/{name}.json`  
**Docs**: [retroui.dev](https://retroui.dev)

Neobrutalism / bold design:

| Component | Style |
|-----------|-------|
| `button` | Bold shadows, thick borders |
| `card` | Offset shadow, strong outlines |
| `input` | Chunky, high-contrast |
| `badge` | Bold labels |
| `alert` | Statement alerts |

```bash
# Neobrutalist kit
pnpm dlx shadcn@latest add @retroui/button @retroui/card @retroui/alert
```

---

## @elevenlabs-ui

**URL**: `https://ui.elevenlabs.io/r/{name}.json`  
**Docs**: [ui.elevenlabs.io](https://ui.elevenlabs.io)

Audio AI interface components:

| Component | Use Case |
|-----------|----------|
| `audio-player` | Waveform playback |
| `voice-selector` | Voice picker UI |
| `recording-button` | Mic input control |
| `transcript` | Real-time transcription |

```bash
# Audio AI kit
pnpm dlx shadcn@latest add @elevenlabs-ui/audio-player @elevenlabs-ui/voice-selector
```

---

## Decision Matrix

| I need... | Use |
|-----------|-----|
| Chat interface | `@ai-elements` |
| Hero with wow factor | `@aceternity` |
| Smooth component animations | `@animate-ui` |
| Retro/gaming theme | `@8bitcn` |
| Bold, statement design | `@retroui` |
| Voice/audio UI | `@elevenlabs-ui` |

---

## Combining Registries

You can mix registries in the same project:

```tsx
// Core shadcn layout
import { Card } from "@/components/ui/card"

// Aceternity for hero effect
import { AuroraBackground } from "@/components/ui/aurora-background"

// AI Elements for chat
import { PromptInput } from "@/components/ai-elements/prompt-input"

// Animate UI for interactions
import { Button } from "@/components/animate-ui/button"
```

**Tip**: Keep components from different registries in separate directories to avoid conflicts.

---

## Finding More

Full directory with 100+ registries: [ui.shadcn.com/docs/directory](https://ui.shadcn.com/docs/directory)

To add a new registry:
1. Find the registry URL pattern
2. Add to `components.json` under `"registries"`
3. Install components with `@registry-name/component`

