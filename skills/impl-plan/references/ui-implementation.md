# UI Implementation Evidence

Load this only after accepted UX, visual, asset, or landing context identifies
a real implementation decision. It is a reference, not a public frontend
planning skill.

## Inspect First

- Read the target app's `package.json`, router, CSS/Tailwind shape,
  `components.json` when present, existing tokens, and nearby component tests.
- Reuse local primitives and design-system conventions before importing a
  registry component or theme.
- Fetch current official documentation or maintained examples for a selected
  framework, shadcn registry, chart library, or animation package. Do not rely
  on a static component catalog.

## Component Decision

For a reusable or imported component, record only the facts the Change Plan
needs:

```text
component_decision(component, user_job, local_conventions)
  -> owner/path + variants + states + accessibility + responsive behavior + proof
```

Required states are the applicable subset of default, hover, focus, active,
disabled, loading, error, empty, and success. Imported components do not earn
their default styling automatically; apply the accepted visual constraints.

## Conditional References

- Chart or dashboard representation: [data visualization guidance](../../../docs/fundamentals/data-visualization.md).
- React Flow or another graph library: inspect its current official docs and
  examples after the ticket establishes the node/edge model.
- Generated or rendered website media: use the owning image, video, or
  Remotion advisor and preserve its asset receipt in the ticket.

## Proof

Name the component state, responsive breakpoint, browser evidence, and visual
judgment required by `tickets/TASK-XXXX/design.md`. Route source checks through
`web-design-guidelines` and screenshots through `visual-qa` only at QA/review.
