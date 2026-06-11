---
name: react-flow
description: "Turn graph-app or node-editor needs into React Flow implementation guidance and best-practice patterns."
tier: 3
group: frontend-data
source: local
allowed-tools: mcp__sequential-thinking__sequentialthinking, Read, Write, Edit, LS
---

# React Flow Skill

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] Read the product/workflow goal, graph data source, active ticket, and
  existing UI conventions.
- [ ] Use [research:official-docs](../research/SKILL.md#researchofficial-docs)
  when React Flow API behavior, examples, or version details matter.
- [ ] Use [research:parity](../research/SKILL.md#researchparity) when node
  editor or workflow-builder patterns should be grounded in comparable apps.
- [ ] Define the graph model: node types, edge types, handles, layout,
  selection, editing, persistence, and validation.
- [ ] Define interaction states: drag, connect, delete, undo/redo, zoom/pan,
  keyboard, empty/loading/error, and permission boundaries.
- [ ] Use [functional-ui](../functional-ui/SKILL.md) when the workflow builder
  behavior or IA is still unclear.
- [ ] Use [frontend-craft](../frontend-craft/SKILL.md) or
  [frontend-design](../frontend-design/SKILL.md) for implementation handoff.
- [ ] Use [visual-qa](../visual-qa/SKILL.md) for browser-level proof of graph
  rendering and interaction.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

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
