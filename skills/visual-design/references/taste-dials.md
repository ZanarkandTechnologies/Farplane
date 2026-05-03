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

## Defaults

- Product UI: density 4-7, variance 3-6, motion 2-5, restrained color.
- Brand UI: density 2-5, variance 5-9, motion 4-8, committed color when earned.
- Data-heavy UI: density 7-9, variance 2-5, motion 1-4, clear semantic color.

## Anti-Slop Bans

- Purple-blue gradient defaults.
- Generic card grids with icon, heading, paragraph repeated endlessly.
- Gradient text as the main premium move.
- Glassmorphism as decoration.
- Huge hero metrics as proof.
- Unstyled default shadcn.
- Decorative motion that hurts the user task.
- Fake data like `99.99%` unless domain-realistic.

## Implementation Notes

- Prefer OKLCH or tokenized color systems when the project supports it.
- Avoid pure `#000` and `#fff` unless the existing system intentionally uses them.
- Animate transforms and opacity by default.
- Avoid font churn. Use existing fonts unless the visual brief explicitly requires a new pairing.
