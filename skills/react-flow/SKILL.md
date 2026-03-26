---
name: react-flow
description: Index of best practices for building graph-based applications and node-based editors using React Flow.
allowed-tools: mcp__sequential-thinking__sequentialthinking, Read, Write, Edit, LS
---

# React Flow Skill

## Purpose

This skill serves as an index for building complex graph-based applications, node editors, and visual workflows using React Flow.

## Documentation Index (Source of Truth)

- **React Flow**: [Official Documentation](https://reactflow.dev/docs/introduction/)
- **Examples**: [React Flow Examples](https://reactflow.dev/docs/examples/overview/)

## Integration Workflow

1. **Schema Design**: Define the node and edge types. See [references/architecture.md](references/architecture.md).
2. **Setup**: Initialize the `ReactFlow` component with `nodes` and `edges` state.
3. **Customization**: Create custom node and edge components as needed. Follow [references/workflows.md](references/workflows.md).
4. **Interactivity**: Implement node dragging, connection handling, and zoom/pan logic.

## Common Gotchas

- **State Updates**: Use `onNodesChange` and `onEdgesChange` handlers correctly to avoid UI lag.
- See [references/gotchas.md](references/gotchas.md).

## References

- [architecture.md](references/architecture.md) - Graph data structures and node types.
- [workflows.md](references/workflows.md) - Implementation patterns for custom nodes and edges.
- [gotchas.md](references/gotchas.md) - Performance optimization and state management pitfalls.

