---
kind: project-harness
status: active
project: Farplane
created_at: 2026-06-15
updated_at: 2026-06-25
framework_template_version: "0.2.0"
owner: harness
---

# Farplane Harness

## Mission

Make autonomous Codex work visible, reviewable, repeatable, and useful through
files, tickets, skills, goals, and proof.

## Human Thesis

Farplane exists to help humans form reliable digital clones that can do
meaningful work: long-running, evidence-producing, goal-aware agent teams that
preserve human intent instead of drifting into busywork.

## Operating Principles

- Prefer visible artifacts over hidden runtime state.
- Keep reusable behavior in skills and project-specific coordinates in
  bindings.
- Shape work through tickets before long autonomous execution.
- Prove behavior with validators, reviews, evals, or artifact evidence.

## Static Leverage Commitments

| Commitment | Why It Compounds | Evidence To Seek | Pivot Signal |
| --- | --- | --- | --- |
| Evals and proof systems | Each accepted proof pattern increases trust and reduces future supervision. | Accepted agent-hours per human intervention rises while false completion falls. | Proof artifacts add friction but do not change decisions or trust. |
| Skill systems | Lessons stop being trapped in transcripts and become callable workflows. | Repeated misses decrease after skill updates; skill invocation heat matches important work. | Skills become stale docs that agents ignore or over-call. |
| Template tracking | Framework fixes become defaults instead of one-off repairs. | New projects reach first measured loop faster with fewer missing surfaces. | Templates drift faster than they help or become too hard to configure. |

## Non-Tradeoffs

- Do not hide orchestration state in chat.
- Do not create a scheduler or daemon when a visible automation prompt is
  enough.
- Do not store secrets in tracked project config.
- Do not silently rewrite the human thesis, durable leverage commitments, or
  product/domain boundary through product, goal, ticket, or interval updates.

## Agent Authority

- Agents may evolve products, audiences, tickets, and goals through
  evidence-backed deltas.
- Agents may challenge the static thesis with evidence.
- Agents may propose a charter delta in a dated interval report.
- Agents may not silently rewrite the static thesis or durable leverage
  commitments.

## Change Rule

Static charter changes require an explicit human-approved harness delta. Weekly
Interval may propose the delta, but cannot apply it silently.

## Charter-Level Operating Loop

```text
observe harness pain, trust gap, or efficiency opportunity
  -> research real-world equivalents and current baseline
  -> run an experiment or ablation with proof
  -> write the evidence as a paper, report, or decision artifact
  -> productize accepted wins into Farplane
  -> distribute trust through educational product content
  -> use adoption, trust, and operator feedback to choose the next experiment
```

## File Boundaries

- `farplane/harness.md`: static human charter, durable thesis, leverage
  commitments, non-tradeoffs, authority, and change rule.
- `farplane/products.md`: dynamic product pipelines, autonomous project types,
  and Pulse refill guidance.
- `farplane/goals.md`: current strategy, KPIs, bets, milestones, holds, and
  Goal Advisor handoffs.
- `farplane/automations.md`: exact Pulse and Interval Codex automation prompts.
- `farplane/bindings.md`: non-secret project coordinates.
- `farplane/evals.md`: proof and eval policy.
