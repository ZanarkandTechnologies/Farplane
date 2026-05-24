# React Flow Architecture

## Node-Based Data Modeling
- **Nodes**: Represent entities. Use custom `data` properties to store application-specific state.
- **Edges**: Represent relationships. Use `type` (e.g., 'smoothstep', 'straight') to define visual style.
- **Handles**: Connection points. Ensure `source` and `target` handles are logically placed for the workflow.

## State Management
- Prefer using the built-in `useNodesState` and `useEdgesState` hooks for simple graphs.
- For complex apps, integrate with external stores like Zustand (highly recommended by React Flow team).

