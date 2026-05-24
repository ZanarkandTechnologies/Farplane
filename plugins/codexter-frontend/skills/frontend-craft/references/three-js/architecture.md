# Three.js Architecture

## Scene Hierarchy
- **Canvas**: The root component that sets up the renderer and scene.
- **Mesh**: Combination of **Geometry** (shape) and **Material** (appearance).
- **Group**: Use to transform multiple meshes together.

## React Three Fiber (R3F)
- Uses a declarative approach to Three.js.
- Objects are managed within the React lifecycle, making it easier to sync 3D state with UI state.

