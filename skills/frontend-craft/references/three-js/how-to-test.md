# How to Test Three.js Features

## Testing Strategy
1. **Visual regression**: Screenshots of rendered scenes.
2. **Performance profiling**: FPS, draw calls, memory.
3. **Interaction tests**: Camera controls, object picking.

## Key Areas
- Scene renders without errors.
- Lighting and materials appear correct.
- Interactions trigger expected behavior.
- Performance stays within budget.

## Tools
- Playwright for screenshots (canvas snapshot).
- Chrome DevTools for WebGL profiling.
- Three.js stats panel for live FPS.

## Common Gotchas
- Test on low-end devices or throttled GPU.
- Verify asset loading errors are handled.
- Check for memory leaks on scene cleanup.
