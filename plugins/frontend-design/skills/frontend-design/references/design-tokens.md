# Design Tokens

Use this when creating, preserving, or changing a frontend token system.

## Three-Layer Model

Keep tokens layered so theme changes do not leak random raw values through the
component tree.

| Layer | Purpose | Examples |
| --- | --- | --- |
| Primitive | Raw values with no product meaning | `--color-zinc-950`, `--space-4`, `--radius-sm` |
| Semantic | Purpose aliases used across the app | `--background`, `--foreground`, `--primary`, `--surface-raised` |
| Component | Component-specific roles and states | `--button-bg`, `--input-border-focus`, `--card-padding` |

## Handoff Shape

```text
Token source:
Existing files:
Primitive layer:
Semantic layer:
Component layer:
Theme modes:
Tailwind/shadcn mapping:
Hardcoded value exceptions:
Migration notes:
```

## Rules

- Preserve existing tokens unless the ticket explicitly changes the visual
  system.
- Prefer CSS variables for shadcn themes and component styling.
- Put raw values in the primitive layer first, then map them to semantic roles.
- Use component tokens only when a component needs a repeatable local contract.
- Test dark/light contrast separately; never assume one mode proves the other.
- Avoid raw hex, arbitrary shadow, and random radius values inside components
  when a token exists.

## Minimal Example

```css
:root {
  --color-ink-950: 230 24% 8%;
  --color-mint-500: 160 68% 42%;
  --space-4: 1rem;

  --background: var(--color-ink-950);
  --foreground: 210 20% 96%;
  --primary: var(--color-mint-500);

  --button-bg: var(--primary);
  --button-padding-x: var(--space-4);
}
```

## Verification

- `components.json` still points at the right CSS and aliases.
- Tailwind v3/v4 syntax matches the installed version.
- Component examples use semantic or component tokens.
- Focus, disabled, loading, error, and hover states remain visible in every
  theme mode.
