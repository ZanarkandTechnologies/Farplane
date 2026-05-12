# Workflows

## End-To-End Build

1. Classify the frontend surface.
2. Use `functional-ui` unless UX/state/interaction shape is already settled.
3. Use `visual-design` unless an existing visual system fully settles the look.
4. Use `landing-page` for one-page or scrolltelling surfaces.
5. Capture stack facts: package availability, Tailwind version, shadcn config,
   aliases, registries, theme/preset status, and existing component paths.
6. Use `frontend-design` references for app-UI implementation details.
7. Use `imagegen` when a bitmap asset or visual probe is needed.
3. Use `landing-page` for one-page or scrolltelling surfaces before choosing the final visual system.
4. Use `visual-design` unless an existing visual system fully settles the look; for landing pages, refine it with the selected taste profile.
5. Use `frontend-design` references for app-UI implementation details.
6. Use `imagegen` when a bitmap asset or visual probe is needed.
7. Use `three-js.md` when the surface earns a real-time 3D/WebGL/R3F scene.
8. Implement, verify, and route visual proof through `visual-qa` when UI changed.

## Broken UI

1. Run `functional-ui` diagnosis.
2. Compare comparable/latest examples.
3. Choose one redesigned interaction model.
4. Use `visual-design` only after behavior is fixed.
5. Implement through `frontend-craft`.

## Landing Page

1. Run `landing-page`.
2. Use `visual-design` for the page's visual system.
3. Use motion/assets references only when earned by the story.
4. Verify first viewport, responsive fit, assets, and scroll checkpoints.

## Registry Or Theme Work

1. Inspect `components.json`, `package.json`, Tailwind setup, and existing UI
   directories.
2. Search/view/docs through shadcn MCP or CLI before adding unfamiliar
   components.
3. Apply only the theme/font/preset layer the ticket asks to change.
4. Customize imported registry components to match the visual brief.
5. Record installed components, package changes, and proof commands in the
   handoff.
2. Select a landing recipe, taste profile, and effect stack from the JSON registries when the page matches a reusable formula.
3. Use `visual-design` for the page's visual system, refined by the selected taste profile.
4. For cinematic/Terminal-style scroll pages, route through `industrial-mission-control`, `terminal-palantir`, and `cinematic-frame-sequence` unless the request clearly needs a different mix.
5. Use motion/assets references only when earned by the story.
6. Verify first viewport, responsive fit, assets, and scroll checkpoints.
