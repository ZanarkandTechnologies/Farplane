# Todos

- [ ] Read the requested capability, existing skills, registry, and nearby
  project docs before creating or updating a skill.
- [ ] Use [plan](../plan/SKILL.md) when tier, ownership, package boundary, or
  first-load contract is unclear.
- [ ] Use [research:parity](../research/SKILL.md#researchparity) or
  [research:source-synthesis](../research/SKILL.md#researchsource-synthesis)
  when external skill examples should inform the design.
- [ ] Define trigger conditions, job, direct `## Important Checklist`, decision
  branches, gotchas or hard gates, judgment questions, and outcome contract in
  `SKILL.md`.
- [ ] Keep every-invocation logic in `SKILL.md`; use references only for
  conditional branches, examples, templates, long rubric detail, model maps,
  delegated prompts, and rare-path recipes.
- [ ] Promote reference logic back into `SKILL.md` when it must be read every
  time.
- [ ] Add `tier`, `source`, Tier 3 `group`, optional `methods`, optional
  `common_chains`, and optional `upstream_url` frontmatter as appropriate.
- [ ] Add or maintain `todos.md` only while legacy Codexter tooling still needs
  it; the direct checklist belongs in `SKILL.md`.
- [ ] Run the skill registry and tier validators after edits.
- [ ] Use [execute](../execute/SKILL.md) for final proof/writeback after skill
  files change.
