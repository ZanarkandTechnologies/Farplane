# How to Plan React Flow Features

## Before You Start
1. Define node and edge types needed.
2. Identify data model for graph state.
3. Determine interaction requirements (add, delete, connect).

## Planning Order
1. **Data model**: Nodes and edges structure.
2. **Node components**: Custom node renderers.
3. **Edge components**: Custom edge styles.
4. **Interactions**: Drag, connect, select, delete.
5. **Persistence**: Save/load graph state.

## Key Questions
- Is the graph editable or view-only?
- Are there validation rules for connections?
- Does it need undo/redo?

## Common Patterns
- Workflow editor: Nodes as steps → edges as transitions
- Knowledge graph: Nodes as entities → edges as relationships
- Data pipeline: Nodes as transforms → edges as data flow
