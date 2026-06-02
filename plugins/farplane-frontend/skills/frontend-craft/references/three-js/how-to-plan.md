# How to Plan Three.js Features

## Before You Start
1. Define scene complexity (objects, lights, effects).
2. Identify asset requirements (models, textures).
3. Determine interaction needs (orbit, click, drag).

## Planning Order
1. **Scene setup**: Camera, renderer, lighting.
2. **Geometry/models**: Load or create 3D objects.
3. **Materials/textures**: Apply visual appearance.
4. **Animation/interaction**: Controls, raycasting, loops.
5. **Optimization**: LOD, instancing, culling.

## Key Questions
- Is this real-time or pre-rendered?
- What's the target device (mobile/desktop)?
- Are there physics or collision requirements?

## Common Patterns
- Product viewer: Load model → orbit controls → lighting
- Data visualization: Procedural geometry → animation
- Game scene: Physics → controls → game loop
