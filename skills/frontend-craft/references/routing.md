# Frontend Skill Routing

Use this when deciding which frontend skill should lead a request.

## Main Entrypoints

| Entrypoint | Use when | Output |
| --- | --- | --- |
| `frontend-craft` | Build or implement a frontend surface | Code plus proof, after routing through needed lanes |
| `functional-ui` | Fix or plan UX, IA, workflow, states, or broken components | Functional redesign handoff |
| `visual-design` | Improve look, taste, brand fit, hierarchy, typography, color, motion taste | Visual brief and implementation constraints |
| `landing-page` | One-page marketing, launch, portfolio, cinematic, scrolltelling | Landing brief, sections, assets, motion plan |
| `imagegen` | Generate or edit bitmap references/assets | Saved assets and prompts |

## Default Routes

- Broken component: `functional-ui` -> `visual-design` -> implementation.
- App screen: `functional-ui` if unsettled -> `visual-design` -> `frontend-design` references.
- Dashboard/tool: `functional-ui` -> restrained `visual-design` -> dense proof states.
- Landing page: `landing-page` -> `visual-design` -> motion/assets/QA references.
- Visual polish: `visual-design` -> implementation.
- Animation only: `motion-routing.md`, and official GreenSock skills or docs when GSAP is chosen.

## Required Stack Facts

Before frontend implementation, capture:

- framework/router and whether App Router/RSC is in play,
- Tailwind major version and config/CSS entrypoints,
- `components.json` existence, aliases, registries, and theme status,
- installed icon, motion, form, chart, AI, and state packages,
- existing component directories and design-system files,
- registry/theme/preset commands planned, or why none are needed.

## Skip Rules

- Skip `functional-ui` only when a current UX brief or explicit user instruction already fixes users, jobs, states, and interaction model.
- Skip `visual-design` only for non-visual wiring, pure bug fixes, or when an existing design system must be followed exactly.
- Skip `landing-page` for product dashboards, settings, forms, or repeated operational tools.
