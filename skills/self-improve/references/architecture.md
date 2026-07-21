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
  initial leverage roadmap, evidence-updated selection policy, budgets, drift,
  and stop conditions.
- Ticket `progress.md`: append-only observations, measurements, decisions, and
  evidence links.
- `.farplane/evals/runs/<job-id>`: generated Eval evidence only.
- Native Goal: sole continuation engine.
- Leverage Advisor: chooses each next experiment from the roadmap plus progress
  learnings, current evidence, and remaining budget.
- Eval: suite execution, grading, and comparison.

The reusable reference is policy source, not runtime state. Leverage Advisor is
an existing skill composition, not a second state or continuation owner. Do not
add a deterministic decision helper, event schema, runner, counter file,
target-local program/progress pair, or another loop owner.
