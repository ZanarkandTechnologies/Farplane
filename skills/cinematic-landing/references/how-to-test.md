# How to Test Cinematic Landing Pages

## Testing Strategy
1. **Visual verification**: Screenshots at key scroll positions.
2. **Performance profiling**: FPS, LCP, CLS metrics.
3. **Cross-browser testing**: Chrome, Safari, Firefox.

## Key Areas
- Scroll animation smoothness (60fps target).
- Mobile performance (reduced motion, fallbacks).
- Asset loading (lazy load, preload critical).
- Accessibility (reduced motion preference).

## Tools
- Playwright for scroll automation and screenshots.
- Lighthouse for performance audits.
- dev-browser skill for quick visual checks.

## Common Gotchas
- Test with slow network (3G simulation).
- Verify prefers-reduced-motion behavior.
- Check for jank on section transitions.
