# Frontend Craft QA

Use this after frontend implementation.

## Default Checks

- Unit/type/lint/build checks that the repo already uses.
- Browser smoke for user-visible changes.
- Screenshot proof for visual changes.
- `visual-qa` judgment for UI layout, taste, overlap, and responsive issues.

## Special Cases

- Landing pages: capture first viewport plus important scroll checkpoints.
- Animation-heavy pages: verify reduced-motion behavior and nonblank moving/canvas frames.
- Generated assets: verify referenced paths load in the browser and are not left under `$CODEX_HOME`.
- Forms/workflows: verify default, loading, empty, error, success, and max-content states.

## Completion Rule

Do not claim the frontend is done until the implementation path and proof path both match the request. If a proof lane is skipped, state the reason.
