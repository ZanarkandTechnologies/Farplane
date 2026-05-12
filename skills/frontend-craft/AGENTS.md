# Frontend Craft Maintenance

## Scope

- `SKILL.md`
- `README.md`
- `AGENTS.md`
- `references/*`

## Boundaries

- `frontend-craft` orchestrates frontend implementation; it does not replace the granular skills.
- `functional-ui` owns UX, IA, workflow, comparable examples, and broken-component redesign.
- `visual-design` owns taste, visual systems, typography, color, layout rhythm, density, and anti-slop.
- `landing-page` owns one-page marketing, launch pages, story arcs, cinematic heroes, and scrolltelling.
- `frontend-design` remains an implementation reference for app UI, shadcn, AI Elements, registries, and theming.
- `references/three-js.md` owns Three.js/WebGL/R3F reference routing; do not keep a separate public `three-js` skill.

## Checks

- The first-load workflow remains executable without loading references.
- References enrich routing but do not hide mandatory steps.
- Community skill learnings stay behind a Codexter-owned control layer.
- Frontend implementation guidance must capture stack facts before adding packages or registry components. See `MEM-0085`.
