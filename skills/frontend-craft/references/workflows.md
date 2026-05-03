# Workflows

## End-To-End Build

1. Classify the frontend surface.
2. Use `functional-ui` unless UX/state/interaction shape is already settled.
3. Use `visual-design` unless an existing visual system fully settles the look.
4. Use `landing-page` for one-page or scrolltelling surfaces.
5. Use `frontend-design` references for app-UI implementation details.
6. Use `imagegen` when a bitmap asset or visual probe is needed.
7. Implement, verify, and route visual proof through `visual-qa` when UI changed.

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
