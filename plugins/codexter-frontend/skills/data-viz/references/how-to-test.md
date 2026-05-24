# How to Test Data Visualization Features

## Testing Strategy
1. **Visual regression**: Screenshots of rendered charts.
2. **Data edge cases**: Empty, single, large datasets.
3. **Interaction tests**: Hover, click, zoom behavior.

## Key Areas
- Correct data mapping (values to visual elements).
- Axis labels and formatting.
- Legend accuracy and interactivity.
- Responsive resizing.

## Tools
- Playwright for interaction and screenshots.
- Storybook for isolated chart states.
- Synthetic data generators for edge cases.

## Common Gotchas
- Test with zero data (empty state).
- Test with very large datasets (performance).
- Verify tooltip positioning near edges.
