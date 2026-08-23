---
title: Data Visualization Guidance
status: active
owner: impl-plan
created_at: 2026-08-06
updated_at: 2026-08-06
tags: [data-visualization, planning, frontend]
---

# Data Visualization Guidance

This is a conditional planning reference, not a standalone skill. Load it when
a ticket needs to choose how data is represented; use current official library
documentation only after the representation and data contract are decided.

```text
choose_visualization(decision, data_shape, audience, constraints)
  -> representation + interaction + accessibility + proof
```

## Representation First

| User decision | Default representation | Avoid when |
| --- | --- | --- |
| Compare values | bar or ranked table | labels or values are too numerous to read |
| See change over time | line or area chart | the time scale is irregular or only one snapshot exists |
| Understand distribution | histogram, box, or density view | categories need direct comparison |
| See relationship | scatter plot or table | the point count makes marks unreadable |
| Understand part-to-whole | stacked bar or ranked table | many small categories would create a pie |
| Follow a process or dependency | flow/graph view | a table or ordered steps explain it more directly |

Name the decision a viewer should make before selecting the chart. A dashboard
does not earn a chart when a sortable, accessible table answers the job better.

## Data And Interaction Contract

- Define source, unit, range, update cadence, missing values, and aggregation.
- Specify empty, loading, partial, error, and high-volume states.
- Use direct labels or accessible table/detail alternatives where color, hover,
  or position alone would hide meaning.
- Define tooltip, legend, filter, drill-down, keyboard, and mobile behavior
  only when they change the viewer's decision.
- Avoid overplotting; aggregate, sample, or change representation rather than
  turning dense data into an unreadable ink blob.

## Implementation And Proof

- Prefer the local chart library for standard charts; use D3 or a specialist
  library only when the data transformation or layout cannot be expressed by
  the existing component stack.
- Keep React responsible for DOM ownership; use D3 for scales, layout, and
  paths rather than uncontrolled DOM mutation.
- Test zero, one, typical, extreme, and malformed datasets; then capture the
  user-visible chart, label/tooltip behavior, and narrow viewport state.
