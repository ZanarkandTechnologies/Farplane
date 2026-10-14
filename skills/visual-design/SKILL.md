---
name: visual-design
version: 1.2.0
description: "Use for \"make it look good\", \"pick a visual style\", \"it looks generic\" or \"define the design system\": a reference-backed visual system, anti-patterns and a planning handoff."
department: delivery
source: local
allowed-tools: Read, Write, Glob, Grep, Bash, web_search
---

# Visual Design

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] Confirm the functional basis: user, primary action, states, workflow, and
  existing UX decision. If missing, route to
  [prd](../prd/SKILL.md).
- [ ] Run the **Steve Jobs Focus & Simplicity Pass**: state the user-facing
  benefit, visual focal action, elements to remove or defer, and deliberate
  `no`; preserve functional requirements, accessibility, and necessary state.
- [ ] Use [research](../research/SKILL.md) when visual direction needs
  product, brand, or peer grounding (`market`).
- [ ] **Story first.** Choose the register (product UI serves repeated work;
  brand UI creates memory), write the scene sentence (who, where, light,
  mood), and name a **visual concept** from the product's own world (a place,
  object, craft, or ritual), never an adjective like "clean". Reject any
  concept that would fit an unrelated app. For polish, name the existing
  concept or `none recorded`; do not invent one.
- [ ] **Reference fidelity.** When the operator names references or states a
  palette or fonts, write the **steal table** (source, trait with exact
  value, `adopt | adapt | reject`, where it shows) before any styling, show
  it, and wait for a yes. Operator-stated palette and fonts and standing
  operator rules (banned hues, a product UI's neutral rule) beat any tasty
  pack, concept, or direction: reject a clashing saved element with the rule
  and a substitute from the same pack; a conflict with a stated value is a
  question, never a silent swap.
- [ ] **Match the story to the library.** For a new direction or a taste
  upgrade, query both halves of the Resource Bank with the story:
  1. **Named styles.** Run
     `python3 skills/design-styles/scripts/design_styles.py list`, shortlist
     the styles that could tell this story, then `show <slug> ...` and open
     each board. Untagged Tasty Packs never return these
     ([design-styles](../design-styles/SKILL.md) owns the vocabulary and
     house guards).
  2. **Saved taste.** Run
     `farplane resource-bank tasty-pack "<2-4 story keywords>" --timeframe all --limit 20 --json`
     with no output-type filter, and read each pinned element's recipe as a
     candidate steal row with its exact values.
  Record both in the library receipt. An empty pull is a stated result;
  skipping the pull is a miss.
- [ ] **Three directions.** Propose three ways to tell the story, each through
  a different library style (slug and board path on the card) plus the saved
  elements it borrows; a direction with no anchor states why none fit. They
  differ in concept, not palette. Skip per the existing-design-system branch.
- [ ] **Concept art before any system.** Make one concept-art image per
  direction through [ai-image](../ai-image/SKILL.md) (style recipe + concept +
  the focal moment, house guards applied, spend logged) and show the three
  side by side with their source boards and a one-line story each. The
  operator picks. Unattended, pick against the scene sentence and focal
  action, record why the others lost, and say so. No dials or tokens before
  a direction is picked.
- [ ] When the user provides a strong reference or the surface needs a taste
  upgrade, use its `synthesis` branch to extract what to adopt, adapt,
  reject, or defer before defining the final visual system.
- [ ] Record a compact visual evidence receipt for every reference used:
  source, trait with its exact value (hex, font and weight, size, layout
  move), `adopt | adapt | reject`, and where it shows on the screen. Do not
  run a separate stateful taste-interview workflow; the concept art is the
  taste question.
- [ ] Set numeric taste dials for density, variance, motion, color commitment,
  and materiality; the dials set how loudly the concept is expressed.
- [ ] Define typography, color roles, spacing rhythm, radius/elevation,
  component treatment, icon/media language, and motion vocabulary. Build
  colour as ground (~60%), figure (~30%), one accent (~10%) on the single
  focal action, and prove ground plus figure work before the accent; set
  empty space as a numeric budget (footprint, measure, column width). See
  `references/color-and-space.md`.
- [ ] **Render, critique, refine.** Write the key screen as a standalone static
  HTML mock in the ticket folder (never edit app source), screenshot it in the
  in-app Browser at the target viewport with the project's real fonts, tokens,
  and realistic content, and score it with `critique-audit.md`. Refine at most
  twice; then hand off with `verdict: revise` and the open issue. With no
  browser available, label the critique `unrendered`.
- [ ] **Independent critique before promotion.** The author's own score is a
  `self-check`, never a `pass`. Before a mock is promoted, accepted, or handed
  off as ready, get the verdict from the operator or from a reviewer subagent
  (`farplane:reviewer` in Claude, `agents/reviewer.toml` in Codex) run through
  [review](../review/SKILL.md) with rubric families `ui-quality` and
  `user-intent-satisfaction`, the design brief (or the ticket plus steal
  table when no brief exists) as `context_ref`, the screenshot, steal table,
  and one screenshot per reference. The reviewer
  checks every steal-table trait side by side with its reference.
- [ ] Write or update a durable design brief when the surface is substantial or
  delegated.
- [ ] Hand the accepted visual brief to [impl-plan](../impl-plan/SKILL.md) for
  ticket composition and conditional implementation research.
- [ ] Use the native execution phase for proof/writeback shape before
  claiming the visual direction is ready.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

Own the look and taste of a frontend surface after its functional purpose is known. This skill is about visual judgment, not workflow design or component wiring.

## Use When

- The user asks for visual polish, better aesthetics, taste, style, hierarchy, typography, color, density, or brand fit.
- `prd` workflow mode has already decided how the surface should work.
- `impl-plan` needs a visual brief before composing UI implementation work.
- A UI looks generic, default, AI-made, or visually incoherent.

## Do Not Use When

- The workflow, IA, or component behavior is still broken: use `prd` workflow mode first.
- The target is a one-page marketing or cinematic landing page: use `landing-page` first, then this skill for visual system decisions.
- The task is only code wiring with a fixed design system.

## Core Workflow

1. **Confirm functional basis.** Identify the user, primary action, states, and interaction model. If missing, route to `prd` workflow mode.
2. **Run the Steve Jobs Focus & Simplicity Pass.** State the user-facing benefit, visual focal action, elements to remove or defer, and deliberate `no`; do not remove functional requirements, accessibility, or necessary state.
3. **Lock reference fidelity.** When the operator named references, palette, or fonts, get a yes on the steal table first. Concept, directions, dials, and visual system then work inside those values.
4. **Classify register.** Product UI serves repeated work; brand UI creates memory and desire. Choose the register before taste decisions.
5. **Write a scene sentence.** Name who uses the surface, where, under what ambient light, and in what mood. Let that force dark/light, density, and contrast.
6. **Find the visual concept.** One idea from the product's world that typography, layout, color, illustration, and motion can all borrow from. In the brand register it drives the whole surface; in the product register it stays quiet (accent, icons, empty and loading states, one signature moment) and never costs scanability. For polish, name the existing concept or `none recorded`. See `references/concept-and-directions.md`.
7. **Match the story to the library.** Pull named styles and all-time saved taste with the story as the query, and open every shortlisted board.
8. **Diverge with concept art.** For a new direction, propose three tellings of the story, each through a different library style, render one concept-art image per direction, and show them side by side with their boards. The operator picks; record the losers as `reject` with a reason.
9. **Choose numeric taste dials.** Set visual density, design variance, motion intensity, color commitment, and materiality on a 1-10 scale with one-line rationale for each.
10. **Define the visual system.** Typography, color roles, spacing rhythm, radius/elevation, component treatment, icon/media language, and motion vocabulary, each traceable to the concept.
11. **Render, critique, refine.** Run the render loop from the Todo List: static HTML mock, in-app Browser screenshot at the target viewport, `critique-audit.md` score, at most two refine passes. Only an independent reviewer or the operator can return `pass`; with operator references, the critique includes a side-by-side shot of each reference.
12. **Write a durable design brief when the work is substantial.** For a new app surface, redesign, multi-screen UI, or delegated implementation, create or update a ticket/spec-local `DESIGN_BRIEF.md` or equivalent ticket section before build handoff.
13. **Hand off to planning.** Produce concrete constraints that `impl-plan` incorporates into the ticket `design.md` baseline; link the rendered mock from it as reference evidence, not a second baseline.

## Decision Branches

| Surface | Visual default |
| --- | --- |
| Operational app/dashboard | restrained, dense enough to scan, stable controls, low ornament |
| AI workflow/chat | clear message hierarchy, strong state visibility, careful empty/loading/error states |
| Brand/marketing surface | more committed color, image-led composition, stronger typography |
| Creative/portfolio | higher variance and motion, still readable and responsive |
| Existing design system or accepted board | preserve tokens and components; skip the three directions, the style shortlist, and the concept; still pull saved taste for steal rows; improve hierarchy and rhythm before inventing new style |
| Operator-named references, palette, or fonts | approved steal table first; directions vary concept inside the stated values; a tasty pack fills only what the operator left open |

## Top Gotchas

- Do not use visual polish to hide weak functionality.
- Do not swap an operator's palette or font for a tasty-pack accent, the
  concept, or your own taste. Ask. Do not promote a mock on your own score.
- Do not design from memory when the library holds a board for the look:
  pull it, open it, and cite its slug.
- Do not commit to the first direction, and do not pass off three palette swaps
  of one layout as three directions.
- Do not accept an adjective ("clean", "modern", "premium") as a concept.
- Do not default to dark mode, purple-blue gradients, identical card grids, or generic SaaS hero metrics.
- Do not create unnecessary columns for sequential workflows. Use one full-width
  flow first; reserve columns for genuinely parallel comparison, inspector
  layouts, file-tree + file-viewer workspaces, dashboards, or side-by-side
  editor surfaces.
- Do not stack generic bordered divs inside generic bordered divs. Avoid
  "container soup": section wrappers should use whitespace, headings,
  dividers, or bands; inner bordered cards are only for repeated items,
  selectable options, interactive controls, or genuinely separate tools.
- Do not import new fonts, colors, or animation libraries without checking the project and the implementation owner.
- Do not make every product UI cinematic. Repeated-use tools should feel efficient, calm, and inspectable.
- Do not ignore mobile text fit, contrast, focus states, or reduced-motion needs.
- Do not copy community taste-skill bans wholesale. Convert them into context-aware Farplane constraints.

## Reference Map

- `references/brand-product-register.md` - product vs brand visual rules.
- `references/concept-and-directions.md` - concept test, direction cards, render spec.
- `references/taste-dials.md` - density, variance, motion, color, anti-slop.
- `references/color-and-space.md` - three-colour build, space budget, saved taste versus standing rules.
- `references/design-brief.md` - durable visual-system handoff shape.
- `references/critique-audit.md` - review checklist and score shape.
- `references/architecture.md` - input/output boundary with functional and implementation skills.
- `references/workflows.md` - visual direction and polish paths.
- `references/gotchas.md` - common taste and visual-system mistakes.

## Output Contract

Return a concise visual brief with:

- `Register`
- `Scene sentence`
- `Visual concept` and how loudly it shows in this register
- `Library receipt`: the shortlisted `style:<slug>` picks with board paths
  viewed, and the saved-taste captures and pinned elements used or rejected
  (or `none matched` for either pull)
- `Directions considered`: three direction cards, each with its story line,
  library anchor, and concept-art image path, the chosen one and who chose
  it, and why the others lost, or the skip reason
- `Steve Jobs Focus & Simplicity Pass`: user-facing benefit, visual focal
  action, elements removed or deferred, and deliberate `no`
- `Taste dials` with 1-10 numeric values
- `Visual system`, with colour roles and their shares, the accent-off check
  (ground plus figure must read before the accent is added: pass or fail), and
  the space budget in numbers
- `Visual evidence receipt` (the steal table, with operator approval, when
  references were named)
- `Render receipt`: rendered key-screen path, viewport, critique scores,
  reviewer (subagent or operator, never only the author), per-trait reference
  check, and refine passes used
- `Design brief path` when one was created or updated
- `Anti-slop constraints`
- `Implementation handoff`
