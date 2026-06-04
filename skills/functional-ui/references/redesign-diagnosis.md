# Redesign Diagnosis

Use this when the user says a UI is bad, confusing, ugly in a functional way, or asks to "functional-ui" an existing component.

## Diagnosis Pass

Capture:

- `Primary user:` who is trying to do what.
- `Primary action:` the one action or decision the UI should make easy.
- `Current failure:` why the existing UI blocks that action.
- `State gaps:` missing default, loading, empty, error, success, disabled, max-content, permission, or offline states.
- `Information hierarchy:` what should be first, second, hidden, grouped, or removed.
- `Interaction cost:` extra clicks, unclear controls, modal abuse, bad defaults, missing undo, weak feedback.
- `Content/data ranges:` realistic minimum, typical, and maximum content.

## Common Failure Modes

- The UI exposes database structure instead of user intent.
- Everything has equal visual and interaction weight.
- Cards group decoration, not decisions.
- Layout uses columns even though the user reads the flow sequentially.
- Nested bordered containers compete with the actual content.
- Lists are nested because the author is explaining structure instead of
  designing a scannable surface.
- Empty/error/loading states are absent or generic.
- The primary action is below secondary controls.
- The component solves a rare edge case before the common path.
- The flow requires explanation text because the interaction is unclear.

## Output

End diagnosis with one sentence:

`The redesign should make <primary action> obvious by <main structural change>.`
