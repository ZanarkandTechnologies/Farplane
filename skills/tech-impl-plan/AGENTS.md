# Tech Impl Plan Maintenance

## Scope

- `SKILL.md`
- `prompts/plan.md`
- `references/template.md`
- `references/examples.md`
- `README.md`

## Boundaries

- Keep top-level planning output compact and approval-first.
- Keep repo rules in root `AGENTS.md`; keep plan mechanics in this skill.
- Add depth only when risk, novelty, or cross-cutting impact justifies it.

## Conventions

- Lead with `Pitch` + `B -> A`.
- Prefer `Core Flow` pseudocode over long dry-runs.
- Diagrams are optional, not default.
- Reference `MEM-0007` for the compact plan contract.
- Reference `MEM-0008` for the root-AGENTS compression boundary.

## Checks

- `Pitch`, `B -> A`, `Delta`, `Core Flow`, `Proof`, `Ask` are all present.
- Split rule remains explicit.
- Proof remains concrete.
- Template and prompt match `SKILL.md`.

## Testing

- Re-read `SKILL.md` once and confirm the contract is executable without references.
- Compare prompt/template/example against `SKILL.md` for drift.
- Confirm high-signal content appears before appendix content.
