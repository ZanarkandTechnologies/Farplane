# Taste Dials

Use dials to make visual decisions concrete.

## Dials

| Dial | Low | High |
| --- | --- | --- |
| Visual density | gallery-like, sparse | cockpit-like, packed |
| Design variance | symmetrical, predictable | asymmetric, editorial, tense |
| Motion intensity | static, tactile states | choreographed, scroll/canvas effects |
| Color commitment | tinted neutrals, one accent | saturated fields or full palette |
| Materiality | flat and quiet | texture, depth, media, lighting |

Score each dial from 1-10 and include a short rationale. Numeric values make
the handoff enforceable without forcing every project into the same aesthetic.

## Defaults

- Product UI: density 4-7, variance 3-6, motion 2-5, restrained color.
- Brand UI: density 2-5, variance 5-9, motion 4-8, committed color when earned.
- Data-heavy UI: density 7-9, variance 2-5, motion 1-4, clear semantic color.

## Output Shape

```text
Visual density: 6/10 - repeated operator screen with scan-friendly grouping.
Design variance: 4/10 - stable grid with one asymmetric emphasis region.
Motion intensity: 3/10 - tactile states and short loading transitions only.
Color commitment: 5/10 - neutral system with one strong semantic accent.
Materiality: 3/10 - mostly flat, with elevation only for overlays.
```

## Optional Archetypes

Use these as starting recipes, not new public skills:

| Archetype | Good for | Watch out |
| --- | --- | --- |
| Utilitarian minimal | Settings, admin, repeated work | Too much blankness or weak hierarchy |
| Industrial telemetry | Dense ops, security, monitoring | Faux terminal gimmicks |
| Soft structural | Consumer, wellness, portfolio | Low contrast and vague CTAs |
| Editorial product | Brand pages, portfolio, case studies | Weak product usability |
| Brutalist statement | Campaign, creative tools | Accessibility and fatigue |

## Anti-Slop Bans

- Purple-blue gradient defaults.
- Generic card grids with icon, heading, paragraph repeated endlessly.
- Gradient text as the main premium move.
- Glassmorphism as decoration.
- Huge hero metrics as proof.
- Unstyled default shadcn.
- Decorative motion that hurts the user task.
- Fake data like `99.99%` unless domain-realistic.
- Generic names, fake avatars, filler startup names, and empty SaaS copy.

## Implementation Notes

- Prefer OKLCH or tokenized color systems when the project supports it.
- Avoid pure `#000` and `#fff` unless the existing system intentionally uses them.
- Animate transforms and opacity by default.
- Avoid font churn. Use existing fonts unless the visual brief explicitly requires a new pairing.
- For shared UI, pair this with `frontend-design/references/component-state-matrix.md`.
