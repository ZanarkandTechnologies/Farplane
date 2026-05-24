# Motion Routing

Use this to select the motion engine. Load official docs or external skills for API details.

## Decision Table

| Need | Default |
| --- | --- |
| Hover, focus, active states | CSS transitions |
| Component enter/exit, layout transitions | Motion / Framer Motion if already in project |
| Complex timelines, ScrollTrigger, pinning, scrub, motion paths | Official `greensock/gsap-skills` |
| Shared-element transitions | View Transitions API with fallback |
| Shader, particles, 3D, post-processing | `three-js.md` for Three.js/WebGL/R3F, or WebGPU only with fallback |
| Reduced-motion support | Always required |

## GSAP Source Of Truth

Do not copy GSAP API details into Codexter references. Use installed official GreenSock skills when available, or fetch official GSAP docs when they are not installed:

- `gsap-react` for React/Next cleanup, `useGSAP`, scoping, SSR safety.
- `gsap-scrolltrigger` for pinning, scrub, refresh, container animation.
- `gsap-performance` for transforms, opacity, `will-change`, batching, cleanup.
- `gsap-plugins` for Flip, SplitText, MorphSVG, Draggable, ScrollSmoother, and other plugins.

## Guardrails

- Animate transform and opacity by default.
- Avoid scroll listeners for scroll-linked effects unless a library or browser API is clearly unsuitable.
- Remove debug markers in production.
- Respect `prefers-reduced-motion`.
- Keep heavy animation in isolated client components.
- Verify in browser; animation-heavy work is not done from code inspection alone.

## Next.js / React Boundaries

- Check `package.json` before importing Motion, GSAP, Three.js, or icon
  packages.
- In Next.js App Router, keep Server Components static by default. Move only the
  interactive or animation-heavy widget into a `"use client"` leaf component.
- Do not use React `useState` for continuous cursor or scroll physics. Prefer
  motion values, refs, requestAnimationFrame with cleanup, or the chosen
  animation library's off-render primitives.
- Do not mix GSAP/Three/WebGL and Motion in the same component tree unless a
  local architecture reason and cleanup plan are explicit.
- Every `useEffect` animation setup needs teardown for listeners, timelines,
  animation frames, observers, and media queries.
