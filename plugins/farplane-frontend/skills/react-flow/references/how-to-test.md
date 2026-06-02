# How to Test React Flow Features

## Testing Strategy
1. **Visual verification**: Screenshots of graph layouts.
2. **Interaction tests**: Drag, connect, delete nodes.
3. **Data integrity**: Graph state matches expected model.

## Key Areas
- Node positioning and layout.
- Edge connections (source/target correct).
- Selection and multi-select behavior.
- Undo/redo state management.

## Tools
- Playwright for drag-and-drop simulation.
- dev-browser skill for quick visual checks.
- Unit tests for graph state logic.

## Common Gotchas
- Test with many nodes (performance).
- Verify connection validation rules.
- Check keyboard shortcuts work.
