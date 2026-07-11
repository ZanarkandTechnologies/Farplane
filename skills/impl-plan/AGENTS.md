# Impl Plan Maintenance

## Scope

- `SKILL.md`
- `prompts/plan.md`
- `references/template.md`
- `references/examples.md`
- `README.md`

## Boundaries

- Keep one public planner only: `impl-plan`. See `MEM-0014`.
- Keep repo rules in root `AGENTS.md`; keep planning mechanics in this skill.
- Keep the plan detailed enough that a builder can execute it without
  inventing missing steps, while still staying skimmable from the top.
- Center the output on `Delta`, `Change Plan`, `Done`, `QA Strategy`,
  `Docs Strategy`, `Links`, and sparse `Notes`; keep bulky evidence, review
  reports, `Options considered`, `Agent Contract`, and `Run Hints` conditional
  or sidecar-owned.
- Use `Change Plan` units as the primary approval surface for material work.
  Each unit should carry local before/after, read/write surface, operation,
  routes, QA expectations, and failure modes.
- Put compact `architecture_signatures` before material Change Plan units so
  top-level module seams, main flow signatures, and relevant typed movement are
  reviewable without reading every unit.
- Keep diagrams out of `ticket.md` without exception. Always use the post-plan
  `diagrams.md` visual companion for ownership, before/after flow, changed
  seams, or typed data paths that are easier to understand visually. See
  `MEM-0030`.
- Keep `impl-plan` aligned with the canonical ticket template instead of
  inventing a parallel `Human` / `Agent` contract. See `MEM-0031`.
- When an `Agent Testability Brief` exists, preserve its proof/testability
  doctrine in the plan rather than re-deriving it. See `MEM-0043`.
- Keep reusable diagram taste and pattern depth in `skills/diagramming/*`; keep
  only planning-specific diagram rules here.
- `impl-plan` should keep an approved coherent ticket intact by default. Do not force "one commit" or smallest-slice decomposition unless a real proof, blocker, reuse, or runtime boundary requires it. See `MEM-0044`.
- Add deeper user-story/example detail only when the applicability rule requires it.
- Keep consensus challenge inside this skill instead of reviving a second public planner.

## Conventions

- Lead with brief `Delta`, then make `Change Plan` the executable structure.
- Require explicit `Change Plan` units when the ticket is material enough that
  the builder should not have to infer sequencing, file ownership, or QA.
- Put compact top-level callable seams in `architecture_signatures`; use
  `signature_or_type_impact` only for local deltas inside a change unit.
- Put typed flow in `architecture_signatures`, local `signature_or_type_impact`,
  and the required visual companion when trust depends on seeing structs, objects,
  payloads, or typed state evolve across boundaries.
- Add a linked `plan.md` only when `Change Plan` would become crowded or
  independently valuable.
- Keep the recommendation above the fold and phrased as a decisive action, not
  a tentative suggestion.
- For every impl-plan's required diagrams, keep the template in
  `skills/impl-plan/references/visual-companion-template.md` and reference
  `skills/diagramming/SKILL.md` for rendering compactness, color/legend
  practice, and inline-signature patterns.
- Reference `MEM-0007` for the original compact plan contract.
- Reference `MEM-0008` for the root-AGENTS compression boundary.
- Reference `MEM-0030` for the diagram-first contract.
- Reference `MEM-0031` for the compact file-map-first single-plan contract.
- Reference `MEM-0050` for the typed-data planning contract.
- Reference `MEM-0062` for the detailed, action-oriented planning contract.
- Make optional sections fail if they are decorative, duplicated, or
  placeholder-only.
- Keep the `SKILL.md` Todo List as plain natural-language todo-list text
  with Markdown links rather than a custom mini-language. See `MEM-0028`.

## Checks

- The output matches the canonical ticket-body shape.
- `Change Plan` is present and locally executable when sequencing is
  non-trivial.
- Every impl-plan ticket has an existing, validator-passing `diagrams.md`
  companion; a link alone is insufficient, there is no not-applicable
  exemption, and inline ticket diagrams are forbidden.
- Changed callable seams are visible in `signature_or_type_impact` and mirrored
  in the visual companion when interface shape matters locally.
- Material top-level seams are visible in `architecture_signatures`.
- Typed flow is visible in `architecture_signatures`, local
  `signature_or_type_impact`, and the visual companion when data movement
  matters.
- The recommendation is decisive and action-oriented when the ticket involves a
  material choice.
- Split rule remains explicit.
- QA Strategy remains concrete.
- The applicability rule is explicit.
- Template and prompt match `SKILL.md`.

## Testing

- Re-read `SKILL.md` once and confirm the contract is executable without references.
- Compare prompt/template/example against `SKILL.md` for drift.
- Confirm the Change Plan approval surface can be skimmed without an appendix.
- Confirm callable seams and typed flow prove real code understanding inside
  `architecture_signatures` and relevant change units without becoming a type
  dump.
- Confirm any `Agent Testability Brief` is reflected in proof/testability planning.
- Confirm options, refs, autonomy, evidence, and gap sections appear only when
  they reduce ambiguity.
