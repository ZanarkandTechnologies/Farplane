# Three.js Gotchas

- **Canvas Sizing**: The `<Canvas>` component takes up 100% of its parent. Ensure the parent container has a height and width.
- **Lighting**: Without a light source (e.g., `<ambientLight />`), `meshStandardMaterial` will appear black.
- **Performance**: High polygon counts and complex shaders can crash mobile browsers. Always monitor `drawcalls`.

