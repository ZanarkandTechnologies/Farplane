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
- Use diagram-first approval only when material work needs a diagram because the
  file map alone is not enough. See `MEM-0030`.
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

- Lead with one top-level delta diagram before the deeper prose only when the
  work needs a diagram because flow, ownership, or typed data path is not
  obvious from the file map alone.
- Require explicit `Execution steps` when the ticket is material enough that
  the builder should not have to infer sequencing.
- Require compact callable seams in `Signature delta` when trust depends on
  seeing code seams, interfaces, ownership boundaries, or changed handlers.
- Require `Type Sketch` plus one `Typed flow example` when trust depends on
  seeing structs, objects, payloads, or typed state evolve across boundaries.
- Keep the recommendation above the fold and phrased as a decisive action, not
  a tentative suggestion.
- When diagrams are needed, reference `skills/diagramming/SKILL.md` and
  `docs/specs/diagram-first-conventions.md` for compactness, color/legend
  practice, and inline-signature patterns.
- Reference `MEM-0007` for the original compact plan contract.
- Reference `MEM-0008` for the root-AGENTS compression boundary.
- Reference `MEM-0030` for the diagram-first contract.
- Reference `MEM-0031` for the compact file-map-first single-plan contract.
- Reference `MEM-0050` for the typed-data planning contract.
- Reference `MEM-0062` for the detailed, action-oriented planning contract.
- Make optional sections fail if they are decorative, duplicated, or
  placeholder-only.
- If `todos.md` exists here, keep it as plain natural-language checklist text
  with Markdown links rather than a custom mini-language. See `MEM-0028`.

## Checks

- The output matches the canonical ticket-body shape.
- `Diagram` is present when a material or cross-module plan needs one because
  flow, ownership, or typed data path is not obvious from the file map alone.
- `Signature delta` is present when interface shape matters.
- `Type Sketch` plus `Typed flow example` are present when typed data flow
  matters.
- `Execution steps` are present when sequencing is non-trivial.
- The recommendation is decisive and action-oriented when the ticket involves a
  material choice.
- Split rule remains explicit.
- Proof remains concrete.
- The applicability rule is explicit.
- Template and prompt match `SKILL.md`.

## Testing

- Re-read `SKILL.md` once and confirm the contract is executable without references.
- Compare prompt/template/example against `SKILL.md` for drift.
- Confirm the diagram-first approval surface can be skimmed without an
  appendix.
- Confirm the callable seams and type shapes prove real code understanding
  without becoming a type dump.
- Confirm any `Agent Testability Brief` is reflected in proof/testability planning.
- Confirm the recommendation is directly justified against the listed options.
