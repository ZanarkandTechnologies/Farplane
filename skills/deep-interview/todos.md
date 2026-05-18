# Todos

- [ ] Read available context before asking: active ticket, `docs/prd.md`,
  `docs/specs/`, project README/AGENTS, and relevant local files.
- [ ] Use [reference-grounding](../reference-grounding/SKILL.md) for local
  baseline facts instead of asking the user for discoverable project context.
- [ ] Ask one question per round and target the weakest clarity dimension.
- [ ] Track the required gates: intent, outcome, scope, constraints, success
  criteria, non-goals, decision boundaries, and one pressure pass.
- [ ] Re-score ambiguity after each answer and keep interviewing until the
  configured threshold and gates are satisfied.
- [ ] Use [advise](../advise/SKILL.md) only when the interview exposes real
  tradeoff options that need a recommendation.
- [ ] Use [review](../review/SKILL.md) before handing off a material interview
  summary as execution-ready.
- [ ] Write the crystallized summary into the active ticket or the next
  canonical artifact owner; do not create hidden sidecar state.
