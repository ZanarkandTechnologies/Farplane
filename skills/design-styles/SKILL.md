---
name: design-styles
description: "Use for \"what style is this\", \"do it in an art deco style\", \"give me style names for this prompt\" or \"show me style references\": a named style with its Tasty Pack board and a prompt-ready style block."
source: local
department: marketing
template_uses:
  skill-template: "0.6.6"
  skill-eval-task: "0.2.0"
allowed-tools: Read, Glob, Grep, Bash
---

# Design Styles

## Context

Image models and designers respond to style names, not mood words: "Art Deco"
pulls a precise look where "elegant and premium" pulls a generic one. This
skill owns that vocabulary: the named styles and their families
([styles.json](references/styles.json)), each stored in the bunker's Resource
Bank as one Tasty Pack capture with its example board image and a recipe,
tagged `style:<slug>` and `style-family:<family>`. `styles.json` is where the
style text is written; `seed` syncs it into the Resource Bank, which is what
agents and Tasty Packs read. It picks named styles for an image, poster, page
or scene, or names the style of a reference, then returns a style block other
skills put into prompts. It does not generate images (`ai-image`), define a
product UI system (`visual-design`), or save new outside references
(`intelligest`).

## Skill Signature

```text
design_styles(brief | reference, count?: 1-2) -> style pick + board image + style block
reads: references/styles.json, the Resource Bank (Tasty Pack and creative elements)
does: maps the brief to named styles, pulls each board and recipe, applies house guards
writes: board images to .farplane/design-styles/refs/ (and Resource Bank rows only for `seed`)
returns: chosen style tags, why, board image paths, the style block, the next owner
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] **N1 — Map the brief to one or two named styles.**
  `surface + audience + emotional job | reference -> style:<slug> x1-2 + reason | no fit`

  Rule: Choose by the surface and the feeling it must create for its
  audience, never by echoing the operator's adjectives. Run
  `python3 skills/design-styles/scripts/design_styles.py list` (add
  `--family <family>` to narrow) and pick from the vocabulary; for a
  reference image, name the closest style and what differs. Pick and state
  the choice; ask only when two families would send the work in opposite
  directions and nothing recorded settles it.

  Example: `"calm, premium landing page for a tea brand" -> style:wabi-sabi
  (structure) + style:japandi (palette), not "minimal and elegant"`

  Assert:
  - Every pick is a `style:<slug>` from the vocabulary with a one-line reason.
- [ ] **N2 — Pull each style's board and recipe from the Tasty Pack.**
  `style:<slug> -> recipe + cues + board image looked at | not stored`

  Rule: The Resource Bank is the source, not memory. Run
  `python3 skills/design-styles/scripts/design_styles.py show <slug> ...`,
  which prints the stored cues and recipe and saves the board to
  `.farplane/design-styles/refs/<slug>.png`; open the image before writing a
  prompt, because some boards drift from the name (the Glassmorphism board
  shows reeded glass, not frosted UI panels). To combine a style with the
  operator's own saved taste, run
  `farplane resource-bank tasty-pack "<idea>" --tag style:<slug> --timeframe all --json`
  and a separate untagged pack; library captures never appear untagged.

  Assert:
  - The recipe came from `show` or the pack, and the board image was viewed.
- [ ] **N3 — Apply the house guards before composing.**
  `recipe + target surface -> guarded recipe + avoid list`

  Rule: Never orange, terracotta or rust anywhere: swap them for the
  recipe's named alternative or mustard, sage or clay-pink. Farplane product
  screens keep zero-chroma concrete neutrals; a style may shape type, layout
  and one accent there, not the greys. The boards are other designers'
  posters: recreate the style, never a poster, logo, character, film or brand
  property, and never feed a board to a generator as an image reference.

  Assert:
  - The avoid list names any swapped colour and any protected property.
- [ ] **N4 — Compose the style block.**
  `guarded recipes + subject -> style block | handoff`

  Rule: Lead with the style name, then four to six concrete cues: palette,
  type, composition, texture, light. With two styles, give one the structure
  and the other the surface ("Bauhaus layout, Brutalism halftone print") and
  stop at two; a third style blurs both. Hand the block to `ai-image` for an
  asset, `visual-design` for a direction, or `storyboard` for a scene look.

  Example: `style:art-deco + "cocktail night poster" -> "Art Deco poster:
  gold hairline sunburst frame on deep navy, centred coupe glass, tall
  geometric sans widely tracked, foil sheen; avoid: copying the board posters"`

  Assert:
  - The block names the style first and every cue is visual, not a mood word.
- [ ] **N5 — Keep saved taste on the same tags.**
  `new style or new reference -> styles.json row + seed | style tags on the capture`

  Rule: Edit style text only in `styles.json`, never in the bank, then run
  `python3 skills/design-styles/scripts/design_styles.py seed --only <slug>`:
  it updates a stored style's text in place and stores a new style (its row
  plus a board image named `NN.png`) as one capture. When `intelligest`
  saves a visual reference, it adds the matching `style:<slug>` tags so the operator's taste
  and this vocabulary filter together.

  Assert:
  - `show <slug>` returns the new style with its image after seeding.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Gotchas

- Calling `tasty-pack` without `--tag style:<slug> --timeframe all` returns no
  styles: library captures stay out of untagged packs on purpose, and the
  default window is the past week.
- Writing "clean, modern, premium" instead of a style name gets the generic
  look the operator was trying to escape.
- Three or more styles in one prompt produce mush; pick one, or one for
  structure and one for surface.
- Seeding writes to the bunker's live Convex deployment; `seed` reports
  `unchanged`, `updated` or `stored` per style, and a `warning` line means a
  duplicate capture to delete in the bunker's Resource Bank.

## Output

```text
Styles: style:<slug> [+ style:<slug>] — <one-line reason each>
Boards: <absolute image paths, viewed>
Style block: <style name>: <4-6 concrete cues>
Avoid: <swapped colours, protected properties>
Next: ai-image | visual-design | storyboard
```
