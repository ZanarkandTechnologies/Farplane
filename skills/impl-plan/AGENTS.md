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
- Keep the top approval surface compact.
- Add deeper user-story/example detail only when the applicability rule requires it.
- Keep consensus challenge inside this skill instead of reviving a second public planner.

## Conventions

- Lead with `Pitch` + `B -> A`.
- Keep the recommendation above the fold.
- Prefer `Core Flow` pseudocode over long dry-runs.
- Diagrams are optional, not default.
- Reference `MEM-0007` for the compact plan contract.
- Reference `MEM-0008` for the root-AGENTS compression boundary.
- Make narrative sections fail if they are decorative, duplicated, or placeholder-only.
- If `todos.md` exists here, keep it as plain natural-language checklist text with Markdown links rather than a custom mini-language. See `MEM-0028`.

## Checks

- `Pitch`, `B -> A`, `Delta`, `Core Flow`, `Proof`, `Ask` are all present.
- `Recommendation` and `Options Appendix` are present.
- Split rule remains explicit.
- Proof remains concrete.
- 3 viable options with pros/cons exist when the ticket involves a material choice.
- The applicability rule is explicit.
- `User Story` / `High-Fidelity Example` are either required and useful, or intentionally omitted for a truly narrow fix.
- Template and prompt match `SKILL.md`.

## Testing

- Re-read `SKILL.md` once and confirm the contract is executable without references.
- Compare prompt/template/example against `SKILL.md` for drift.
- Confirm high-signal content appears before appendix content.
- Confirm the recommendation is directly justified against the listed options.
