## Canvas App Testing (Cheat Sheet)

### What to test (minimum)
- **Rendering correctness**: key primitives draw correctly (shapes, text, images).
- **Input**: pointer/mouse/touch events, drag, zoom/pan, keyboard shortcuts.
- **State**: undo/redo, selection rules, serialization/import/export.
- **Performance**: frame rate under typical and worst-case scenes.

### Agentic-friendly testability (strongly recommended)
Canvas UIs are hard to test purely visually. Make them testable:\n
- Add a debug overlay mode that draws bounding boxes + labels for selected/hovered objects.\n
- Expose selected object ID + key properties as **DOM text** (so Playwright can assert).\n
- Provide deterministic “test mode” toggles (disable animations, fixed RNG seed).\n

### Recommended backpressure
- **Unit**: geometry math, hit-testing, transforms.
- **Golden tests**: render to an offscreen canvas and compare image hashes within tolerance.\n
- **E2E**: a small set of user workflows (create object, move, group, export).\n
- **Perf budgets**: max frame time / max memory for N objects.

### Evidence to capture
- Golden screenshots (or perceptual diffs) for canonical scenes.
- Profiling snapshots for slow paths.

