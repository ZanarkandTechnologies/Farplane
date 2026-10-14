# Concept And Directions

Use this to start a new visual direction from an idea instead of from generic
UI patterns, and to avoid committing to the first answer.

## Visual Concept

A concept is one idea from the product's own world that the visual system can
borrow from: a place, object, craft, material, ritual, or artifact the user
already knows.

| Product | Weak concept | Strong concept |
| --- | --- | --- |
| Running tracker | "energetic and modern" | an athletics track: lane lines, bib numbers, split boards |
| Sleep app | "calm and soft" | a village going to sleep: lights switching off house by house |
| Plant care | "fresh and green" | paper cut-out: layered flat shapes, visible edges |
| Italian learning | "fun and colorful" | Neapolitan playing cards: suits, framed figures, card stock |

### Concept Test

Accept the concept only when all hold:

- It comes from the product's domain or the user's world, not from UI trends.
- It would look wrong on an unrelated app.
- It gives at least three concrete moves: one each for type or layout, color,
  and media or motion.
- It does not fight the primary job. If it hurts scanning, state, or the focal
  action, turn it down or pick another.

### Loudness By Register

| Register | How the concept shows |
| --- | --- |
| Brand | Drives composition, type, color, illustration, and motion. |
| Product | Quiet: accent color, icon style, empty and loading states, naming, and one signature moment. Layout stays a scannable tool. |
| Data-heavy | Mostly in semantic color and chart styling; never in layout. |

The design-variance and materiality dials set the exact loudness.

## Three Directions

Run this for a new surface or redesign; `SKILL.md` owns the skip rule.

Each direction is a card:

```text
Direction <A|B|C>: <concept name>
Library anchor: style:<slug> (.farplane/design-styles/refs/<slug>.png) + saved elements borrowed
Concept: <one line>
Dials: density / variance / motion / color / materiality
Type and color: <pairing and role colors>
Signature move: <the one thing someone would remember>
Story: <one line: how this direction tells the product's story>
Concept art: <image path, made through ai-image from the style recipe + concept>
Risk: <what could go wrong for the primary job>
```

Rules:

- The three must differ in concept, not just in palette, font, or radius.
- Each card anchors to a different style from the library pull. The style
  supplies type, layout, and texture moves; the concept still comes from the
  product's world, and house guards (banned hues, product neutrals) still
  apply. A card with no anchor says why no library style fit.
- One direction may be the safe option; at least one must be a bolder bet.
- Choose against the scene sentence, the focal action, and the dials, not
  against which looks prettiest in isolation.
- Record the losing directions as `reject` with one reason each. Ideas taken
  from a loser are `adapt`.
- Show the three concept-art images side by side with their source boards
  before any dials or tokens; the operator picks. Unattended, pick against
  the scene sentence and focal action and say so.

## Render Spec

Critique the real thing, not the idea of it.

- Write the key screen as a standalone static HTML mock in the ticket folder;
  never edit app source. Screenshot it in the in-app Browser at the target
  viewport: 390x844 for phone, the project's desktop width for desktop, both
  when the surface ships on both.
- Use the project's real fonts and tokens. For native iOS targets use the
  system font; otherwise do not swap in a font the project will not ship.
- Fill it with realistic content: real-length names, numbers, and empty or
  error states where they matter.
- Link it from the ticket `design.md` as reference evidence; `design.md`
  stays the one QA baseline.
- Score it with `critique-audit.md`.
