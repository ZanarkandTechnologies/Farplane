# Remocn Reference

Use this reference when the user mentions Remocn or when a Remotion project
would benefit from copied motion primitives, transitions, backgrounds, UI
scenes, demo-video blocks, or polished text effects instead of hand-building
every motion component.

## What It Is

Remocn is a shadcn-style registry for Remotion components. Components are copied
into the project with `shadcn`, then owned and edited locally. It is a component
source, not a rendering service, Remotion replacement, or black-box dependency.

## When To Use

- Product demos, launch trailers, changelog clips, proof videos, or feature
  walkthroughs that need polished motion quickly.
- Kinetic text, reveal effects, transitions, browser/device scenes, terminal or
  code scenes, charts, social UI cards, AI chat scenes, backgrounds, or
  timeline-driven UI primitives.
- A local Remotion project already exists or can be created with
  `npx create-video@latest`.

## Setup

```bash
npx create-video@latest --yes --blank --no-tailwind my-video
npx shadcn@latest init
npx shadcn@latest add @remocn/blur-reveal
```

Use the current component name from the registry or docs. If a project already
has `components.json`, inspect its aliases before running `shadcn init`.

## Routing Rules

- Load `rules/video-layout.md` before placing Remocn components into a final
  scene.
- Treat copied Remocn components as local code: inspect props, timing,
  dimensions, imports, Tailwind usage, and static asset paths after install.
- Keep Remotion frame math and local render proof in the owning Remotion
  project. Do not assume a Remocn component is render-ready in the target
  composition until a still or render check passes.
- If a Remocn component creates or implies source assets, route missing asset
  planning through `asset-advisor` before composing.
- If Tailwind is required by a copied component, verify the Remotion project
  supports that Tailwind setup before relying on the component.

## Current Grounding

- Website: `https://www.remocn.dev/`
- Repository: `https://github.com/Remocn/remocn`
- Install pattern: `npx shadcn@latest add @remocn/<component>`
- Registry examples include typography effects, transitions/wipes, environment
  effects, UI blocks, AI scenes, social scenes, and composition blocks.
