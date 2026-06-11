---
name: visual-design
version: 1.0.0
description: "Turn a known frontend workflow into typography, color, layout, hierarchy, motion, and anti-generic visual direction."
tier: 3
group: frontend
source: local
common_chains:
  after: ["frontend-craft"]
allowed-tools: Read, Grep, Glob
---

# Visual Design

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] Confirm the functional basis: user, primary action, states, workflow, and
  existing UX decision. If missing, route to
  [functional-ui](../functional-ui/SKILL.md).
- [ ] Use [research:parity](../research/SKILL.md#researchparity) or
  [research:competitor](../research/SKILL.md#researchcompetitor) when visual
  direction needs product, brand, or peer grounding.
- [ ] When the user provides a strong reference or the surface needs a taste
  upgrade, use [best-of-worlds](../best-of-worlds/SKILL.md) to extract what to
  adopt, adapt, reject, or defer before defining the final visual system.
- [ ] Use [plan](../plan/SKILL.md) to choose the visual register and accepted
  tradeoff before specifying style.
- [ ] Set numeric taste dials for density, variance, motion, color commitment,
  and materiality.
- [ ] Define typography, color roles, spacing rhythm, radius/elevation,
  component treatment, icon/media language, and motion vocabulary.
- [ ] Write or update a durable design brief when the surface is substantial or
  delegated.
- [ ] Hand off to [frontend-design](../frontend-design/SKILL.md) for app UI
  implementation references or [frontend-craft](../frontend-craft/SKILL.md) for
  the full build path.
- [ ] Use [execute](../execute/SKILL.md) for proof/writeback shape before
  claiming the visual direction is ready.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

Own the look and taste of a frontend surface after its functional purpose is known. This skill is about visual judgment, not workflow design or component wiring.

## Use When

- The user asks for visual polish, better aesthetics, taste, style, hierarchy, typography, color, density, or brand fit.
- `functional-ui` has already decided how the surface should work.
- `frontend-craft` needs a visual brief before implementation.
- A UI looks generic, default, AI-made, or visually incoherent.

## Do Not Use When

- The workflow, IA, or component behavior is still broken: use `functional-ui` first.
- The target is a one-page marketing or cinematic landing page: use `landing-page` first, then this skill for visual system decisions.
- The task is only code wiring with a fixed design system.

## Core Workflow

1. **Confirm functional basis.** Identify the user, primary action, states, and interaction model. If missing, route to `functional-ui`.
2. **Classify register.** Product UI serves repeated work; brand UI creates memory and desire. Choose the register before taste decisions.
3. **Write a scene sentence.** Name who uses the surface, where, under what ambient light, and in what mood. Let that force dark/light, density, and contrast.
4. **Choose numeric taste dials.** Set visual density, design variance, motion intensity, color commitment, and materiality on a 1-10 scale with one-line rationale for each.
5. **Define the visual system.** Typography, color roles, spacing rhythm, radius/elevation, component treatment, icon/media language, and motion vocabulary.
6. **Write a durable design brief when the work is substantial.** For a new app surface, redesign, multi-screen UI, or delegated implementation, create or update a ticket/spec-local `DESIGN_BRIEF.md` or equivalent ticket section before build handoff.
7. **Reject AI tells.** Run the anti-slop check from `taste-dials.md` and `critique-audit.md`.
8. **Hand off to implementation.** Produce concrete constraints that `frontend-craft` or `frontend-design` references can build.

## Decision Branches

| Surface | Visual default |
| --- | --- |
| Operational app/dashboard | restrained, dense enough to scan, stable controls, low ornament |
| AI workflow/chat | clear message hierarchy, strong state visibility, careful empty/loading/error states |
| Brand/marketing surface | more committed color, image-led composition, stronger typography |
| Creative/portfolio | higher variance and motion, still readable and responsive |
| Existing design system | preserve tokens and components; improve hierarchy and rhythm before inventing new style |

## Top Gotchas

- Do not use visual polish to hide weak functionality.
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
- `references/taste-dials.md` - density, variance, motion, color, anti-slop.
- `references/design-brief.md` - durable visual-system handoff shape.
- `references/critique-audit.md` - review checklist and score shape.
- `references/architecture.md` - input/output boundary with functional and implementation skills.
- `references/workflows.md` - visual direction and polish paths.
- `references/gotchas.md` - common taste and visual-system mistakes.

## Output Contract

Return a concise visual brief with:

- `Register`
- `Scene sentence`
- `Taste dials` with 1-10 numeric values
- `Visual system`
- `Design brief path` when one was created or updated
- `Anti-slop constraints`
- `Implementation handoff`
