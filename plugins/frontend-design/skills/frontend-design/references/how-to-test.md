# How to Test Frontend Features

## Testing Strategy
1. **Visual verification**: dev-browser skill for screenshots.
2. **Interaction tests**: Playwright for user flows.
3. **Accessibility audits**: axe-core or manual checks.

## Key Areas
- Responsive layouts (mobile, tablet, desktop).
- Form validation (required fields, error messages).
- Loading and error states.
- Keyboard navigation and focus management.

## Tools
- Playwright for E2E and visual regression.
- dev-browser skill for quick visual checks.
- Storybook for component isolation (if available).

## Common Gotchas
- Test dark mode and light mode separately.
- Check for layout shifts on data load.
- Verify focus trapping in modals.
