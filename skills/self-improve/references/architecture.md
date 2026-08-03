# Self Improve Architecture

Self-improvement is one native Goal over one target skill and one frozen suite.

```text
local/source/adversarial coverage preparation
  -> ordinary ticket Goal Packet
  -> baseline
  -> harden until performance target passes
  -> refine repeatedly while preserving the target
  -> shortest verified passing candidate
```

## Ownership

- Target `SKILL.md`: editable live behavior.
- Target `evals/evals.json`: canonical behavior cases.
- Ticket `ticket.md`: objective, scope, Done, and proof contract.
- Ticket `program.md`: instantiated harden/refine policy, metrics, budgets,
  source/search policy, evidence-updated selection policy, drift, and stop
  conditions.
- Ticket `hypothesis-tree.json`: current source synthesis, hypotheses, results,
  and insights.
- Ticket `progress.md`: append-only selection and mutation receipts.
- `.farplane/evals/runs/<job-id>`: generated Eval evidence only.
- Native Goal: sole continuation engine.
- Active Goal: owns `choose_next` from eligible pending tree leaves, progress
  learnings, current evidence, and remaining budget.
- Leverage Advisor: supplies a stateless ordinal comparison only when several
  eligible moves need judgment.
- Eval: suite execution, grading, and comparison.

The reusable reference is policy source, not runtime state. Leverage Advisor is
a conditional skill composition, not a state, decision, or continuation owner. Do not
add a deterministic decision helper, event schema, runner, counter file,
target-local program/tree/progress set, tournament, or another loop owner.
