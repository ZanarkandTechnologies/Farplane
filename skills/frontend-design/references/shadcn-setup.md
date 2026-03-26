# Shadcn Setup: MCP & Project Configuration

> **When to use**: First-time project setup or adding shadcn to an existing project.

## One-Time Setup

### 1. Initialize Shadcn MCP

Run this once per project to enable AI-assisted component discovery:

```bash
pnpm dlx shadcn@latest mcp init --client claude
```

This creates a `.mcp/` configuration that allows Claude to search and add components.

### 2. Initialize Shadcn (if not already done)

```bash
pnpm dlx shadcn@latest init
```

Choose your preferences:
- **TypeScript**: Yes
- **Style**: Default or New York
- **Base color**: Neutral (customize later with tweakcn)
- **CSS variables**: Yes
- **Tailwind config**: `tailwind.config.ts`
- **Components path**: `@/components`
- **Utils path**: `@/lib/utils`

---

## Components.json Configuration

After init, edit `components.json` to add registries:

```json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "new-york",
  "rsc": true,
  "tsx": true,
  "tailwind": {
    "config": "tailwind.config.ts",
    "css": "app/globals.css",
    "baseColor": "neutral",
    "cssVariables": true,
    "prefix": ""
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils",
    "ui": "@/components/ui",
    "lib": "@/lib",
    "hooks": "@/hooks"
  },
  "registries": {
    "@8bitcn": "https://www.8bitcn.com/r/{name}.json",
    "@aceternity": "https://ui.aceternity.com/registry/{name}.json",
    "@ai-elements": "https://registry.ai-sdk.dev/{name}.json",
    "@animate-ui": "https://animate-ui.com/r/{name}.json",
    "@elevenlabs-ui": "https://ui.elevenlabs.io/r/{name}.json",
    "@retroui": "https://retroui.dev/r/{name}.json"
  }
}
```

---

## Adding Components

### From shadcn/ui (core)

```bash
# Single component
pnpm dlx shadcn@latest add button

# Multiple components
pnpm dlx shadcn@latest add button card dialog input

# All components (not recommended - pick what you need)
pnpm dlx shadcn@latest add --all
```

### From Registries

```bash
# AI Elements
pnpm dlx shadcn@latest add @ai-elements/prompt-input
pnpm dlx shadcn@latest add @ai-elements/conversation
pnpm dlx shadcn@latest add @ai-elements/message

# Aceternity (effects)
pnpm dlx shadcn@latest add @aceternity/aurora-background
pnpm dlx shadcn@latest add @aceternity/spotlight

# Animate UI
pnpm dlx shadcn@latest add @animate-ui/accordion
pnpm dlx shadcn@latest add @animate-ui/button

# Retro UI (neobrutalism)
pnpm dlx shadcn@latest add @retroui/button
pnpm dlx shadcn@latest add @retroui/card

# 8bitcn (pixel art)
pnpm dlx shadcn@latest add @8bitcn/button
```

---

## Using Shadcn MCP

Once configured, the shadcn MCP allows Claude to:

1. **Search for components**: Find components across all configured registries
2. **Add components**: Install components directly to your project
3. **Preview components**: See component documentation and usage

**Trigger**: When you ask for a component, Claude will use the MCP to search and suggest.

---

## Finding New Registries

If you need a registry not in your config:

1. Visit [ui.shadcn.com/docs/directory](https://ui.shadcn.com/docs/directory)
2. Find the registry you want
3. Click the MCP button to get the registry pattern
4. Add to `components.json`

**Pattern format**: `https://<domain>/r/{name}.json`

---

## Gotchas

1. **MCP not working?** Ensure you ran `mcp init --client claude` in the project root
2. **Registry not found?** Check the URL pattern matches exactly
3. **Component conflicts?** Registries may have overlapping component names - use the prefix (`@registry/component`)
4. **Style mismatch?** Some registries use "default" style, others "new-york" - may need manual adjustment

