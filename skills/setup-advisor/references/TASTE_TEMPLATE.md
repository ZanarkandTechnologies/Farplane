# Taste

## Core Direction

- Dense, operational, restrained
- Minimal chrome
- Serious tone over playful SaaS tone
- Tooltip over explanatory paragraph
- High information density without clutter
- Strong hierarchy, compact spacing, explicit states

## Reference Questions

- How would Palantir design this surface?
- What can be removed without losing clarity?
- Should this be a tooltip instead of persistent text?
- Does this feel operational or generic?
- Does any panel feel too bulky or padded?
- Is there decorative whitespace that is not earning its keep?

## Component Bias

- Prefer `shadcn`-quality primitives for app UI by default
- For UI-bearing app projects, start from the default tweakcn darkmatter theme
  unless the user explicitly disables it or the project already has a stronger
  design system:
  `pnpm dlx shadcn@latest add https://tweakcn.com/r/themes/darkmatter.json`
- Do not use plain HTML/CSS/JS as the default app UI foundation; reserve it for
  explicit static/throwaway artifacts.
- Avoid default-looking controls and unstyled browser UI
- Favor compact panels, sharp alignment, and disciplined spacing
- Use restrained color and decoration; signal state with clarity, not noise

## Project Overrides

- Add or remove references here as the product develops a sharper visual doctrine.
- Keep this file stable and reusable; ticket-specific exceptions belong in the active ticket file.
