# Component State Matrix

Use this when adding or changing a reusable component, shared pattern, or
registry component that other screens will depend on.

## Required Matrix

```text
Component:
Owner/path:
User job:
Dependencies checked:
Variants:
Sizes:
States:
Accessibility:
Responsive behavior:
Theme behavior:
Proof:
```

## State Priority

When states overlap, the intended visual priority should be:

1. disabled
2. loading
3. error
4. active
5. focus
6. hover
7. default

## State Checklist

| State | Required proof |
| --- | --- |
| Default | Component renders with intended label/content |
| Hover | Pointer affordance is visible without layout shift |
| Focus | Keyboard focus ring is visible and contrast-safe |
| Active/pressed | Feedback appears within 300ms |
| Disabled | Semantics and visual treatment both block action |
| Loading | Size is stable and status is announced when needed |
| Error | Message is near the control and recovery is clear |
| Empty | Empty state explains how to proceed |
| Success | Confirmation is visible without stealing focus |

## Component Spec Fields

For reusable components, record:

- anatomy: slots, icons, labels, helper text, actions,
- variants: primary, secondary, destructive, outline, ghost, etc.,
- sizes: height, padding, icon size, text scale,
- responsive behavior: wrap, collapse, truncate, or stack rules,
- accessibility: labels, `aria-*`, focus trap, keyboard path, live regions,
- theme behavior: light/dark tokens and contrast,
- proof: tests, Storybook/story, screenshot, visual-qa, or browser notes.

## Registry Components

Imported shadcn or registry components still need this matrix when they become a
shared local primitive. Do not leave them in default skin unless the local
design brief explicitly says the default matches the system.
