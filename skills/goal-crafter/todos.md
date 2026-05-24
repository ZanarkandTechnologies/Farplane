# Todos

- [ ] Read the operator ask and identify whether it needs a native `/goal`,
  normal prompt, ticket workflow, or `$ralph` board drain.
- [ ] Use [reference-grounding](../reference-grounding/SKILL.md) when the goal
  depends on current docs, repo behavior, source evidence, or tool capability.
- [ ] Use [advise](../advise/SKILL.md) when multiple goal framings are viable.
- [ ] Draft the goal with outcome, verification surface, constraints,
  boundaries, iteration policy, blocked stop condition, and optional budget.
- [ ] Ensure the blocked stop condition requires attempted paths, evidence,
  safe options, recommended next action, and the one missing user input.
- [ ] Prefer native `/goal` for evidence-based continuation; use `$ralph` only
  for prepared filesystem tickets that should drain through board context.
- [ ] Use `$work` in the Goal when Codexter must decide
  direct work, planning, implementation, batching, reslicing, compute, or proof.
- [ ] For ticket-batch Goals, require one proof row per ticket plus one
  batch-level regression row.
- [ ] Return a paste-ready `/goal` command and short use notes.
