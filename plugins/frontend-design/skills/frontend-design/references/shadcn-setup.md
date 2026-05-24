# Shadcn Setup: MCP & Project Configuration

> **When to use**: First-time project setup or adding shadcn to an existing project.

## Preflight

Before installing anything, capture the project facts:

```bash
test -f package.json && cat package.json
test -f components.json && cat components.json
pnpm dlx shadcn@latest info
```

Record:

- framework/router and TypeScript setup,
- Tailwind major version and config style,
- whether shadcn is already initialized,
- aliases from `components.json`,
- existing icon, motion, chart, form, and AI packages,
- current theme/preset status.

## One-Time Setup

### 1. Initialize Shadcn MCP

Run this once per project to enable AI-assisted component discovery:

```bash
pnpm dlx shadcn@latest mcp init --client claude
```

This creates a `.mcp/` configuration that allows Claude to search and add components.

Codex caveat: the shadcn CLI cannot automatically update
`~/.codex/config.toml`. For Codex, add the server manually and restart Codex:

```toml
[mcp_servers.shadcn]
command = "npx"
args = ["shadcn@latest", "mcp"]
```

### 2. Initialize Shadcn (if not already done)

```bash
pnpm dlx shadcn@latest init
```

Choose your preferences:
- **TypeScript**: Yes
- **Style**: New York
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
    "@ai-elements": "https://ai-sdk.dev/elements/api/registry/{name}.json",
    "@assistant-ui": "https://r.assistant-ui.com/{name}.json",
    "@animate-ui": "https://animate-ui.com/r/{name}.json",
    "@elevenlabs-ui": "https://ui.elevenlabs.io/r/{name}.json",
    "@retroui": "https://retroui.dev/r/{name}.json"
  }
}
```

For private registries, use environment-backed headers:

```json
{
  "registries": {
    "@private": {
      "url": "https://registry.company.com/{name}.json",
      "headers": {
        "Authorization": "Bearer ${REGISTRY_TOKEN}"
      }
    }
  }
}
```

---

## Adding Components

Search and view before installing unfamiliar components:

```bash
pnpm dlx shadcn@latest search @shadcn -q "button"
pnpm dlx shadcn@latest search @ai-elements -q "conversation"
pnpm dlx shadcn@latest view button card dialog
pnpm dlx shadcn@latest docs button
```

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

When MCP is unavailable, use the CLI `search`, `view`, `docs`, and `add`
commands directly.

---

## Finding New Registries

If you need a registry not in your config:

1. Check the registry index: `https://ui.shadcn.com/r/registries.json`
2. Use `pnpm dlx shadcn@latest search @registry-name`
3. Add a registry to `components.json` only when the CLI cannot discover it
4. Use `@registry/component` namespace syntax to avoid conflicts

**Pattern format**: `https://<domain>/r/{name}.json`

Current useful registry categories:

| Need | Registries to consider |
| --- | --- |
| AI chat and agents | `@ai-elements`, `@assistant-ui`, `@agents-ui`, `@tool-ui` |
| Auth | `@auth0`, `@clerk` |
| Billing | `@billingsdk` |
| Forms/uploads | `@formcn`, `@better-upload` |
| Charts/data | `@evilcharts` |
| Motion and expressive UI | `@aceternity`, `@animate-ui`, `@cult-ui`, `@unlumen-ui` |
| Retro/brutalist | `@8bitcn`, `@retroui`, `@boldkit` |

## Presets and Theme Application

Use `apply` when the project should absorb only a preset's theme or font layer:

```bash
pnpm dlx shadcn@latest apply <preset-or-url> --only theme
pnpm dlx shadcn@latest apply <preset-or-url> --only font
pnpm dlx shadcn@latest preset resolve --json
pnpm dlx shadcn@latest preset decode <code> --json
pnpm dlx shadcn@latest preset open <code>
```

Do not run broad preset application when the project already has an approved
design system. Preserve local tokens unless the ticket explicitly changes them.

---

## Gotchas

1. **MCP not working?** Ensure you ran `mcp init --client claude` in the project root
2. **Registry not found?** Check the URL pattern matches exactly
3. **Component conflicts?** Registries may have overlapping component names - use the prefix (`@registry/component`)
4. **Style mismatch?** Some registries use "default" style, others "new-york" - may need manual adjustment
5. **Tailwind mismatch?** Check Tailwind v3/v4 before using config syntax
6. **Package mismatch?** Check `package.json` before importing icon, motion, chart, or form packages
