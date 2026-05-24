# Three.js Routing

Use this when a frontend surface earns a real-time 3D, shader, particle, WebGL, or React Three Fiber scene.

Three.js is not a public skill entrypoint. Route through `frontend-craft`, and for landing pages through `landing-page` first, then load this reference.

## When It Earns 3D

- Product viewer, configurator, spatial demo, or object-focused hero.
- Data or system model that becomes clearer as a 3D scene.
- Premium landing-page first viewport where 3D is the actual product/place/object signal.
- Game, simulation, or interactive canvas where DOM/SVG would be the wrong medium.

## Reference Files

- [architecture.md](three-js/architecture.md) - scene hierarchy and React Three Fiber integration.
- [how-to-plan.md](three-js/how-to-plan.md) - scene complexity, assets, interactions, and planning order.
- [workflows.md](three-js/workflows.md) - simple R3F patterns and model loading.
- [gotchas.md](three-js/gotchas.md) - canvas sizing, lighting, performance, and disposal pitfalls.
- [how-to-test.md](three-js/how-to-test.md) - visual, performance, and interaction checks.

## Frontend Contract

1. Define the scene purpose before choosing 3D.
2. Confirm the project has or can add Three.js/R3F dependencies.
3. Build progressive fallback or static poster behavior for unsupported/reduced-motion paths.
4. Lazy-load heavy scenes and pause off-screen rendering.
5. Verify desktop and mobile screenshots, canvas nonblank pixels, framing, interactions, and performance.
