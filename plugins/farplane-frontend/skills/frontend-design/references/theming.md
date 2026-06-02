# Theming: Shadcn Themes & tweakcn

> **When to use**: Customizing colors, fonts, and design tokens before building.

## Quick Start: Darkmatter Theme

The **darkmatter** theme is a dark, refined aesthetic that works well for most apps:

```bash
pnpm dlx shadcn@latest add https://tweakcn.com/r/themes/darkmatter.json
```

This updates your `globals.css` with the theme's CSS variables.

When the project already has shadcn presets or a generated theme URL, prefer
applying only the intended layer:

```bash
pnpm dlx shadcn@latest apply <preset-or-url> --only theme
pnpm dlx shadcn@latest apply <preset-or-url> --only font
pnpm dlx shadcn@latest preset resolve --json
```

---

## tweakcn: Theme Customization Tool

[tweakcn.com](https://tweakcn.com) is a visual theme editor for shadcn/ui.

### Workflow

1. Confirm the visual brief and numeric taste dials from `visual-design`.
2. Visit [tweakcn.com](https://tweakcn.com) or inspect the existing preset.
3. Customize colors, radius, fonts, and surface contrast.
4. Apply only the theme/font layer that the project should change.
5. Check dark and light mode contrast separately.

### Popular Themes

| Theme | Command |
|-------|---------|
| Darkmatter | `pnpm dlx shadcn@latest add https://tweakcn.com/r/themes/darkmatter.json` |
| Catppuccin | `pnpm dlx shadcn@latest add https://tweakcn.com/r/themes/catppuccin.json` |
| Rosepine | `pnpm dlx shadcn@latest add https://tweakcn.com/r/themes/rosepine.json` |
| Nord | `pnpm dlx shadcn@latest add https://tweakcn.com/r/themes/nord.json` |

---

## CSS Variables Structure

Shadcn themes use HSL CSS variables:

```css
:root {
  --background: 0 0% 100%;
  --foreground: 222.2 84% 4.9%;
  --card: 0 0% 100%;
  --card-foreground: 222.2 84% 4.9%;
  --popover: 0 0% 100%;
  --popover-foreground: 222.2 84% 4.9%;
  --primary: 222.2 47.4% 11.2%;
  --primary-foreground: 210 40% 98%;
  --secondary: 210 40% 96.1%;
  --secondary-foreground: 222.2 47.4% 11.2%;
  --muted: 210 40% 96.1%;
  --muted-foreground: 215.4 16.3% 46.9%;
  --accent: 210 40% 96.1%;
  --accent-foreground: 222.2 47.4% 11.2%;
  --destructive: 0 84.2% 60.2%;
  --destructive-foreground: 210 40% 98%;
  --border: 214.3 31.8% 91.4%;
  --input: 214.3 31.8% 91.4%;
  --ring: 222.2 84% 4.9%;
  --radius: 0.5rem;
}

.dark {
  --background: 222.2 84% 4.9%;
  --foreground: 210 40% 98%;
  /* ... dark mode overrides */
}
```

---

## Token Layering

For larger app UI work, keep theme values in three layers:

1. Primitive tokens: raw colors, spacing, radius, shadows, durations.
2. Semantic tokens: purpose aliases such as background, foreground, primary,
   muted, destructive, surface, border, ring.
3. Component tokens: component-specific roles such as button background,
   input border, card padding, badge tone, dialog scrim.

Use [design-tokens.md](design-tokens.md) when changing or creating a token
system. Do not scatter raw hex values across components when the project uses
CSS variables.

---

## Custom Theme Recipe

### 1. Define Your Palette

```css
/* app/globals.css */
@layer base {
  :root {
    /* Custom brand colors */
    --brand: 262 83% 58%;      /* Purple accent */
    --brand-foreground: 0 0% 100%;

    /* Override shadcn tokens */
    --primary: var(--brand);
    --primary-foreground: var(--brand-foreground);

    /* Custom accent */
    --accent: 200 95% 50%;     /* Cyan */

    /* Adjust radius */
    --radius: 0.75rem;         /* Rounder corners */
  }
}
```

### 2. Add Custom Fonts

```tsx
// app/layout.tsx
import { Inter, Space_Grotesk, JetBrains_Mono } from 'next/font/google';

const display = Space_Grotesk({
  subsets: ['latin'],
  variable: '--font-display'
});

const mono = JetBrains_Mono({
  subsets: ['latin'],
  variable: '--font-mono'
});

export default function RootLayout({ children }) {
  return (
    <html className={`${display.variable} ${mono.variable}`}>
      <body>{children}</body>
    </html>
  );
}
```

```css
/* globals.css */
:root {
  --font-display: var(--font-space-grotesk);
  --font-mono: var(--font-jetbrains-mono);
}

h1, h2, h3, h4 {
  font-family: var(--font-display);
}

code, pre {
  font-family: var(--font-mono);
}
```

---

## Theme Presets by Aesthetic

### Neobrutalism

```css
:root {
  --background: 60 9.1% 97.8%;
  --foreground: 24 9.8% 10%;
  --border: 20 5.9% 10%;
  --radius: 0rem;  /* Sharp corners */

  /* Add shadow utility */
  --shadow-brutal: 4px 4px 0px var(--foreground);
}
```

### Retro/Pixel

```css
:root {
  --background: 220 13% 18%;
  --foreground: 60 9% 98%;
  --primary: 142 71% 45%;  /* Retro green */
  --radius: 0rem;

  /* Pixel font */
  --font-display: 'Press Start 2P', monospace;
}
```

### Luxury/Refined

```css
:root {
  --background: 0 0% 3%;
  --foreground: 0 0% 98%;
  --primary: 45 93% 47%;  /* Gold */
  --muted: 0 0% 10%;
  --radius: 0.25rem;  /* Subtle rounding */
}
```

---

## Dark Mode Setup

### Using next-themes

```bash
npm i next-themes
```

```tsx
// app/providers.tsx
'use client';

import { ThemeProvider } from 'next-themes';

export function Providers({ children }) {
  return (
    <ThemeProvider attribute="class" defaultTheme="dark">
      {children}
    </ThemeProvider>
  );
}
```

```tsx
// app/layout.tsx
import { Providers } from './providers';

export default function RootLayout({ children }) {
  return (
    <html suppressHydrationWarning>
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
```

### Theme Toggle

```tsx
'use client';

import { useTheme } from 'next-themes';
import { Button } from '@/components/ui/button';
import { Moon, Sun } from 'lucide-react';

export function ThemeToggle() {
  const { theme, setTheme } = useTheme();

  return (
    <Button
      variant="ghost"
      size="icon"
      onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
    >
      <Sun className="h-5 w-5 rotate-0 scale-100 dark:-rotate-90 dark:scale-0" />
      <Moon className="absolute h-5 w-5 rotate-90 scale-0 dark:rotate-0 dark:scale-100" />
    </Button>
  );
}
```

---

## Gotchas

1. **HSL values**: Shadcn uses space-separated HSL (not commas): `222.2 84% 4.9%`
2. **Theme precedence**: `globals.css` loads last, so your overrides should work
3. **Font loading**: Use `next/font` for optimal loading, not `@import`
4. **Dark mode**: Add both `:root` and `.dark` selectors for full theme support
5. **Registry conflicts**: Some registries have their own styling - may need to override

---

## Recommended Workflow

1. **Start with tweakcn**: Get a base theme you like
2. **Install darkmatter** (or preferred theme)
3. **Override tokens**: Adjust primary, accent, radius
4. **Add custom fonts**: Match the aesthetic direction
5. **Test dark/light**: Ensure both modes look intentional

For existing systems, reverse the order: inspect current tokens first, then
apply the smallest theme/font patch that supports the visual brief.
