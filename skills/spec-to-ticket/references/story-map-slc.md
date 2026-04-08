## Story Map + SLC Slice Planning

**One-liner**: Turn many possible activities into a **single shippable slice** (Simple, Lovable, Complete).

### Inputs
- `docs/prd.md` (recommended)
- `docs/specs/*` (activities / topics)
- Existing codebase (what already exists)

### Outputs
- A chosen slice summary
- Raw ticket files in `tickets/` scoped to the slice

### Story map (structure)
Columns = journey backbone (activities). Rows = capability depth.

Example:

UPLOAD -> EXTRACT -> ARRANGE -> SHARE
basic     auto       manual     export
bulk      palette    templates  collab

### SLC criteria
- **Simple**: narrow scope, no unnecessary breadth
- **Complete**: accomplishes a meaningful job end-to-end
- **Lovable**: delivers real value within the boundary

### Agentic rule
If the slice is not testable by an agent, add testability instrumentation (selectors, overlays, steppers) into the slice tasks.
