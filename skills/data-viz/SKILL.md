---
name: data-viz
description: Index of best practices for building charts, dashboards, and knowledge graphs using D3.js and Recharts.
allowed-tools: mcp__sequential-thinking__sequentialthinking, Read, Write, Edit, LS
---

# Data Visualization Skill

## Purpose

This skill serves as an index for building informative and interactive data visualizations, ranging from simple charts (Recharts) to complex custom graphics and knowledge graphs (D3.js).

## Documentation Index (Source of Truth)

- **D3.js**: [Official Documentation](https://d3js.org/)
- **Recharts**: [Official Documentation](https://recharts.org/)
- **Observable**: [D3 Examples & Notebooks](https://observablehq.com/@d3/gallery)

## Integration Workflow

1. **Tool Selection**: Use Recharts for standard charts (line, bar, pie) and D3 for custom layouts or knowledge graphs. See [references/architecture.md](references/architecture.md).
2. **Data Transformation**: Shape data into the required format (e.g., D3 hierarchy, Recharts array).
3. **Implementation**: Build components following the patterns in [references/workflows.md](references/workflows.md).
4. **Refinement**: Add tooltips, legends, and animations for clarity.

## Common Gotchas

- **React vs D3 DOM**: Avoid letting D3 manipulate the DOM directly in React; use React for the DOM and D3 for math/scaling.
- See [references/gotchas.md](references/gotchas.md).

## References

- [architecture.md](references/architecture.md) - Visualization hierarchy and tool selection.
- [workflows.md](references/workflows.md) - D3 scale patterns and Recharts integration.
- [gotchas.md](references/gotchas.md) - Performance and responsiveness pitfalls.

