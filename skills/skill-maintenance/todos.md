# Todos

- [ ] Read `docs/specs/skill-tier-rollout-plan.md`,
  `docs/skills/README.md`, `docs/skills/registry.jsonl`, active tickets, and
  the target skill files before editing.
- [ ] Use [research:source-synthesis](../research/SKILL.md#researchsource-synthesis)
  when upstream/external skill examples should inform local updates.
- [ ] Use [plan](../plan/SKILL.md) when tier, source, group, method ownership,
  or consolidation choices are not mechanical.
- [ ] For each target skill, identify project files, related skills, proof
  surfaces, and source ownership before writing todos.
- [ ] Keep Tier 2 todos linked to Tier 1 primitives; keep Tier 3 todos linked
  to Tier 2 surfaces plus intentional peer Tier 3 handoffs only.
- [ ] Keep external skill packages thin and move Codexter wrapper policy into
  local caller skills.
- [ ] Use [batch-work](../batch-work/SKILL.md) when the operator wants several
  low-risk skill updates handled in one bounded pass.
- [ ] Regenerate and validate the registry with
  `python3 bin/check_skills.py --write` after edits.
- [ ] Use [execute](../execute/SKILL.md) for final proof, docs writeback, and
  ticket evidence.
