# Frontend Craft QA

Use this after frontend implementation.

## Default Checks

- Unit/type/lint/build checks that the repo already uses.
- `web-design-guidelines` on changed UI source files, with the latest upstream
  rules fetched by that skill.
- Browser smoke for user-visible changes.
- Screenshot proof for visual changes.
- `visual-qa` judgment for UI layout, taste, overlap, and responsive issues.

## Special Cases

- Landing pages: capture first viewport plus important scroll checkpoints.
- Animation-heavy pages: verify reduced-motion behavior and nonblank moving/canvas frames.
- Generated assets: verify referenced paths load in the browser and are not left under `$CODEX_HOME`.
- Generated image assets: verify workspace/public path loading, dimensions, responsive crop, file size, alpha/background expectations, and alt text when semantic.
- Generated video assets: verify workspace/public path loading, poster/fallback, stable aspect ratio, autoplay constraints, muted/controls policy, captions or transcript when semantic, and reduced-motion behavior.
- Three.js/WebGL assets: verify nonblank canvas pixels, correct framing, lighting/material visibility, interaction controls, mobile performance, lazy-load/off-screen pause, and reduced-motion/static fallback.
- Forms/workflows: verify default, loading, empty, error, success, and max-content states.

## Review Metric

When a review pass follows frontend implementation, attach the
`frontend-guidelines` score from `review/references/frontend-guidelines.md`
beside the normal `ui-quality` score. Use disagreement between the two scores to
find agents that overvalue visual taste or miss standards fundamentals.

## Completion Rule

Do not claim the frontend is done until the implementation path and proof path both match the request. If a proof lane is skipped, state the reason.
