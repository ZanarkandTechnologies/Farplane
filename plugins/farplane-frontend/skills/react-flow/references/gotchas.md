# React Flow Gotchas

- **Immutability**: Always treat nodes and edges as immutable. Direct mutation will not trigger re-renders.
- **Z-Index**: Custom nodes might need explicit z-indexing if they overlap complex edges.
- **Performance**: For graphs with 1000+ nodes, use the `onlyRenderVisibleElements` prop and simplify custom node components.

