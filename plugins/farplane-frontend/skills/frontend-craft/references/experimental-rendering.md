# Experimental Rendering

Use this for futuristic effects only when the experience earns the complexity.

## HTML-in-Canvas

`WICG/html-in-canvas` explores drawing DOM element snapshots into canvas, WebGL, and WebGPU contexts.

Current posture:

- Treat as experimental.
- Use for prototypes, demos, or progressive enhancement.
- Provide a DOM fallback.
- Preserve accessibility in real DOM where possible.
- Avoid depending on it for core production UI until browser support and privacy behavior are stable.

Useful ideas:

- Render HTML labels into canvas/WebGL scenes.
- Apply shader distortion or 3D transforms to UI-like DOM snapshots.
- Build experimental input or slider effects while keeping fallback controls.

## Pretext

`@chenglou/pretext` is useful for multiline text measurement and manual layout without forcing DOM reflow.

Good uses:

- Canvas/SVG/WebGL text layout.
- Virtualized lists or masonry where text height prediction prevents layout shift.
- Rich inline chips, mentions, or labels that need line measurement.
- Development-time overflow checks for dynamic copy.

Guardrails:

- Keep CSS font strings, line height, and letter spacing synced with the rendered UI.
- Named fonts are safer than `system-ui` for measurement accuracy.
- Do not use Pretext for ordinary DOM text unless measurement is the actual problem.

## WebGL / WebGPU

- Use [three-js.md](three-js.md) for Three.js, WebGL, and React Three Fiber scenes.
- Use WebGPU only with WebGL or static fallback.
- Lazy-initialize heavy contexts.
- Pause off-screen rendering.
- Run visual QA at desktop and mobile sizes.
