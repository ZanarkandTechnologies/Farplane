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
- Keep the top approval surface compact and explicitly reviewer-facing.
- Make the top approval surface diagram-first for material work. See `MEM-0030`.
- Keep the top of the ticket split into `Human` first and `Agent` second. See
  `MEM-0031`.
- Keep reusable diagram taste and pattern depth in `skills/diagramming/*`; keep
  only planning-specific diagram rules here.
- Add deeper user-story/example detail only when the applicability rule requires it.
- Keep consensus challenge inside this skill instead of reviving a second public planner.

## Conventions

- Lead with one top-level delta diagram before the deeper prose when the work
  is material or cross-module.
- Require a compact `Signature Sketch` near the top when trust depends on
  seeing code seams, interfaces, ownership boundaries, or changed handlers.
- Keep the recommendation above the fold.
- When diagrams are needed, reference `skills/diagramming/SKILL.md` and
  `docs/specs/diagram-first-conventions.md` for compactness, color/legend
  practice, and inline-signature patterns.
- Reference `MEM-0007` for the compact plan contract.
- Reference `MEM-0008` for the root-AGENTS compression boundary.
- Reference `MEM-0030` for the diagram-first contract.
- Reference `MEM-0031` for the `Human` / `Agent` split plus signature-sketch
  contract.
- Make narrative sections fail if they are decorative, duplicated, or placeholder-only.
- If `todos.md` exists here, keep it as plain natural-language checklist text with Markdown links rather than a custom mini-language. See `MEM-0028`.

## Checks

- `Human` and `Agent` are both present and `Human` comes first.
- `Decision`, `B -> A`, `Proof`, and `Ask` are all present in `Human`.
- `Diagram` is present for any material or cross-module plan.
- `Signature Sketch` is present when interface shape matters.
- `Delta`, `Execution Plan`, `Plan Review`, and `Ticket Move` are present in
  `Agent`.
- `Options Appendix` is present for material choices.
- Split rule remains explicit.
- Proof remains concrete.
- 3 viable options with pros/cons exist when the ticket involves a material choice.
- The applicability rule is explicit.
- `User Story` / `High-Fidelity Example` are either required and useful, or
  intentionally omitted for a truly narrow fix.
- Template and prompt match `SKILL.md`.

## Testing

- Re-read `SKILL.md` once and confirm the contract is executable without references.
- Compare prompt/template/example against `SKILL.md` for drift.
- Confirm high-signal `Human` content appears before appendix content.
- Confirm the diagram-first approval surface can be skimmed without the
  `Agent` lane or appendix.
- Confirm the signature sketch proves real code understanding without becoming a
  type dump.
- Confirm the recommendation is directly justified against the listed options.
