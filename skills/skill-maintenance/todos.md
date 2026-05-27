# Todos

- [ ] Read `docs/specs/skill-tier-rollout-plan.md`,
  `docs/skills/README.md`, `docs/skills/registry.jsonl`, active tickets, and
  the target skill files before editing.
- [ ] Use [research:source-synthesis](../research/SKILL.md#researchsource-synthesis)
  when upstream/external skill examples should inform local updates.
- [ ] Use [plan](../plan/SKILL.md) when tier, source, group, method ownership,
  or consolidation choices are not mechanical.
- [ ] For each target skill, identify project files, related skills, proof
  surfaces, and source ownership before editing the first-load contract.
- [ ] Put required checklist items directly in `SKILL.md` under
  `## Important Checklist`; update `todos.md` only while legacy tooling needs
  it.
- [ ] Keep every-invocation logic in `SKILL.md`; move only conditional
  branches, examples, templates, long rubric detail, model maps, delegated
  prompts, and rare-path recipes into references.
- [ ] Promote reference logic back into `SKILL.md` when it must be read every
  time.
- [ ] Keep Tier 2 todos linked to Tier 1 primitives; keep Tier 3 todos linked
  to Tier 2 surfaces plus intentional peer Tier 3 handoffs only.
- [ ] Keep external skill packages thin and move Codexter wrapper policy into
  local caller skills.
- [ ] Regenerate and validate the registry with
  `python3 skills/skill-maintenance/scripts/check_skills.py --write` after
  edits.
- [ ] Use [execute](../execute/SKILL.md) for final proof, docs writeback, and
  ticket evidence.
