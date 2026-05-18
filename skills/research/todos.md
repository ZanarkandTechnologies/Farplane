# Todos

- [ ] Choose exactly one primary method first:
  [research:parity](SKILL.md#researchparity),
  [research:gap](SKILL.md#researchgap),
  [research:competitor](SKILL.md#researchcompetitor),
  [research:official-docs](SKILL.md#researchofficial-docs),
  [research:code-patterns](SKILL.md#researchcode-patterns), or
  [research:user-grounding](SKILL.md#researchuser-grounding), or
  [research:source-synthesis](SKILL.md#researchsource-synthesis).
- [ ] Use [reference-grounding](../reference-grounding/SKILL.md) as the Tier 1
  evidence discipline: local baseline, primary sources, source confidence, and
  local impact.
- [ ] Read the active ticket, local docs, specs, registry rows, or nearby code
  needed to state the local baseline.
- [ ] Add a supporting method only when the primary method exposes a real gap:
  - official/API uncertainty -> [research:official-docs](SKILL.md#researchofficial-docs)
    or [documentation](../documentation/SKILL.md)
  - real repo implementation pattern needed ->
    [research:code-patterns](SKILL.md#researchcode-patterns) or
    [external-patterns](../external-patterns/SKILL.md)
  - peer/product norm missing -> [research:parity](SKILL.md#researchparity)
  - current-state production gap needed -> [research:gap](SKILL.md#researchgap)
  - user groups, jobs, stories, context, friction, or success signals needed ->
    [research:user-grounding](SKILL.md#researchuser-grounding)
  - several sources need normalization ->
    [research:source-synthesis](SKILL.md#researchsource-synthesis)
- [ ] Stop after the smallest method set that can produce the needed brief; do
  not run every research method by default.
- [ ] Route the brief to the next owner:
  [advise](../advise/SKILL.md) for judgment calls,
  [best-of-worlds](../best-of-worlds/SKILL.md) for adopt/adapt/reject/defer
  synthesis, or the relevant domain planning skill such as
  [impl-plan](../impl-plan/SKILL.md) for coding.
- [ ] Run [review](../review/SKILL.md) after meaningful research-skill,
  registry, ticket-handoff, or public-doc changes.
