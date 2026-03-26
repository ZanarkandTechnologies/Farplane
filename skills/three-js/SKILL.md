---
name: three-js
description: Index of best practices for building 3D web experiences using Three.js and React Three Fiber.
allowed-tools: mcp__sequential-thinking__sequentialthinking, mcp__Parallel-search-mcp__web_search, Read, Write, Edit, LS
---

# Three.js Skill

## Purpose

This skill serves as an index for building immersive 3D websites and experiences using Three.js and the React Three Fiber (R3F) ecosystem.

## Documentation Index (Source of Truth)

- **Three.js**: [Official Documentation](https://threejs.org/docs/)
- **React Three Fiber**: [Official Documentation](https://docs.pmnd.rs/react-three-fiber)
- **Drei**: [R3F Helper Library](https://github.com/pmndrs/drei)

## Integration Workflow

1. **Scene Setup**: Define the `Canvas`, `camera`, and `lighting`. See [references/architecture.md](references/architecture.md).
2. **Object Creation**: Build geometries and materials. Use `gltf` loaders for external models.
3. **Motion & Interaction**: Use `useFrame` for per-frame animations. Follow [references/workflows.md](references/workflows.md).
4. **Optimization**: Implement instancing, level-of-detail (LOD), and texture compression.

## Common Gotchas

- **Resource Disposal**: Always dispose of geometries and materials to avoid memory leaks.
- See [references/gotchas.md](references/gotchas.md).

## References

- [architecture.md](references/architecture.md) - Scene hierarchy and R3F integration.
- [workflows.md](references/workflows.md) - Animation and loading patterns.
- [gotchas.md](references/gotchas.md) - Performance and disposal pitfalls.

