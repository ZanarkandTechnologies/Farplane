# Frontend Craft QA

Use this after frontend implementation.

## Default Checks

- Unit/type/lint/build checks that the repo already uses.
- Browser smoke for user-visible changes.
- Screenshot proof for visual changes.
- `visual-qa` judgment for UI layout, taste, overlap, and responsive issues.
- Small-phone proof around 375px width when the surface is responsive.
- Landscape or short-height proof when fixed headers, pinned scenes, sidebars,
  bottom bars, or large heroes are present.
- Text-fit proof for dynamic content, long labels, and increased text size where
  the platform/browser supports it.
- Reduced-motion proof for animation-heavy surfaces.
- Touch target, focus-visible, contrast, and keyboard reachability checks for
  interactive UI.
- No horizontal overflow and no hidden content behind fixed/sticky elements.
- Light/dark or theme-parity checks when themes or tokens changed.

## Special Cases

- Landing pages: capture first viewport plus important scroll checkpoints.
- Animation-heavy pages: verify reduced-motion behavior and nonblank moving/canvas frames.
- Generated assets: verify referenced paths load in the browser and are not left under `$CODEX_HOME`.
- Forms/workflows: verify default, loading, empty, error, success, and max-content states.
- Reusable components: verify the component-state matrix covers variants,
  disabled, loading, error, focus, and theme behavior.

## Completion Rule

Do not claim the frontend is done until the implementation path and proof path both match the request. If a proof lane is skipped, state the reason.
