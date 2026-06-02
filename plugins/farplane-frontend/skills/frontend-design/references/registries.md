# Shadcn Registries: Component Libraries Index

> **When to use**: Looking for the right registry/component for your use case.

## Registry Overview

| Registry | Aesthetic | Best For |
|----------|-----------|----------|
| **@ai-elements** | Clean, functional | AI apps, chatbots, workflows |
| **@assistant-ui** | Headless/chat primitives | AI chat with AI SDK, LangGraph, Mastra, custom adapters |
| **@agents-ui** | Agent/audio/video workflows | LiveKit AI agent interfaces |
| **@tool-ui** | Tool-call output UI | Rich assistant tool widgets |
| **@auth0** | Enterprise auth | SSO, MFA, organizations |
| **@clerk** | Auth and user management | Sign-in, user profile, org surfaces |
| **@billingsdk** | SaaS billing | Pricing, subscriptions, invoices |
| **@formcn** | Forms | Production forms |
| **@better-upload** | Uploads | S3-compatible file uploads |
| **@evilcharts** | Data visualization | shadcn + Recharts chart UI |
| **@aceternity** | Glassmorphism, motion | Landing pages, hero sections |
| **@animate-ui** | Smooth transitions | Interactive components |
| **@cult-ui** | Animated composables | Tasteful Framer Motion components |
| **@unlumen-ui** | Animation-focused | Design-heavy primitives |
| **@8bitcn** | Pixel art, retro | Gaming, nostalgic themes |
| **@retroui** | Neobrutalism | Bold, statement pieces |
| **@boldkit** | Neobrutalism | Thick borders, blocks, shapes |
| **@elevenlabs-ui** | Audio-focused | Voice AI, audio apps |

---

## @ai-elements (AI SDK)

**URL**: `https://ai-sdk.dev/elements/api/registry/{name}.json`
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

## AI and Agent Registries

| Registry | Use Case |
| --- | --- |
| `@assistant-ui` | Chat primitives and adapters for AI SDK, LangGraph, Mastra, or custom backends |
| `@agents-ui` | LiveKit AI agent interfaces |
| `@tool-ui` | Rich rendering of AI tool calls and assistant output widgets |
| `@ai-blocks` | Local/WebLLM-style AI blocks when serverless/local inference is the point |

Use these when AI workflow UI needs more than static chat bubbles. Still route
conversation states, tool progress, sources, retry, and failure recovery through
`functional-ui` first.

---

## App-Domain Registries

| Registry | Use Case |
| --- | --- |
| `@auth0` | Universal auth components, SSO, MFA, organizations |
| `@clerk` | Auth and user-management components |
| `@billingsdk` | Billing, subscriptions, invoices, pricing |
| `@formcn` | Complex production forms |
| `@better-upload` | Direct-to-storage file uploads |
| `@evilcharts` | shadcn/Recharts chart UI |

Use app-domain registries when they match a real product workflow. Do not add a
full domain SDK just to avoid building one simple local component.

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
| Auth | `@auth0`, `@clerk` |
| Billing | `@billingsdk` |
| Forms/uploads | `@formcn`, `@better-upload` |
| Charts | `@evilcharts` |
| Agent/tool output | `@assistant-ui`, `@agents-ui`, `@tool-ui` |

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

Full current index: [ui.shadcn.com/r/registries.json](https://ui.shadcn.com/r/registries.json)

To add a new registry:
1. Search first: `pnpm dlx shadcn@latest search @registry-name`
2. View before install: `pnpm dlx shadcn@latest view @registry-name/component`
3. Add to `components.json` under `"registries"` only when needed
4. Install components with `@registry-name/component`

## Registry Guardrails

- Check `package.json` before importing dependencies that registry components assume.
- Keep registries namespaced to avoid component name conflicts.
- Keep private registry credentials in environment variables.
- Customize imported components to match the visual brief; default registry skin is not enough.
- Prefer official docs or `shadcn docs <component>` when API details matter.
