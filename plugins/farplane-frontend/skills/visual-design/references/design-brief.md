# Design Brief

Use this when visual direction must survive beyond one chat response: new app
surfaces, redesigns, multi-screen flows, delegated frontend implementation, or
substantial theme work.

Prefer the active ticket or spec as the durable surface. Create a standalone
`DESIGN_BRIEF.md` only when the project already has a design-doc convention or
the ticket explicitly needs one.

## Template

```text
# Design Brief

Status:
Owner:
Source request:

## Functional Basis

User:
Primary job:
Key screens/states:

## Register

Product or brand:
Scene sentence:
Non-goals:

## Taste Dials

Visual density:
Design variance:
Motion intensity:
Color commitment:
Materiality:

## Visual System

Typography:
Color roles:
Spacing rhythm:
Radius/elevation:
Component treatment:
Icon/media language:
Motion vocabulary:

## Tokens and Theme

Existing token source:
Theme/preset plan:
Dark/light expectations:

## Component Proof

Reusable components needing a state matrix:
States that must be captured:

## Anti-Slop Constraints

Forbidden patterns:
Content realism rules:

## Implementation Handoff

Frontend references:
Stack facts required:
QA gates:
```

## Rules

- Keep design brief text concrete enough to build from.
- Do not let the brief replace `functional-ui`; it assumes workflow and states
  are already known.
- Record numeric taste dials.
- Record whether shadcn/tweakcn/theme changes are intended.
- For delegated frontend work, pass this path in the delegate prompt.
