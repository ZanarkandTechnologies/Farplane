# Todos

- [ ] State the Codexter improvement request as one concrete harness failure or capability gap.
- [ ] Use [reference-grounding](../reference-grounding/SKILL.md) to inspect the
  smallest relevant local evidence before recommending a surface.
- [ ] Check `docs/features/registry.jsonl` for an existing or partial harness
  feature before proposing a new feature.
- [ ] Check `docs/skills/registry.jsonl` for an existing skill, method, source
  owner, or consolidation target before proposing a new skill.
- [ ] Read `docs/policies/README.md` when the request touches policy,
  canonical ownership, memory, specs, tickets, runtime, hooks, skills,
  registries, or source/feature provenance.
- [ ] Read `docs/specs/harness-engineering-doctrine.md` for placement rules.
- [ ] For material or ambiguous placement decisions, read
  [placement-axes](./references/placement-axes.md) and score context budget,
  reuse frequency, ownership fit, determinism, evidence surface, duplication
  risk, discoverability, and maintenance cost.
- [ ] Compare only realistic levers: repo `AGENTS.md`, global template, docs/specs,
  skill, subagent, hook/script, ticket contract, validator, or registry metadata.
- [ ] Use [advise](../advise/SKILL.md) to compare exactly 3 viable placement
  options and recommend one.
- [ ] Name one primary owner and any secondary sync points.
- [ ] Hand implementation to the relevant Tier 3 workflow or visible ticket
  instead of doing hidden stateful work in chat.
- [ ] Use [review](../review/SKILL.md) before treating a material placement
  decision as ready.
