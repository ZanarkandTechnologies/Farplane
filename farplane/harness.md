---
kind: project-harness
status: active
project: Farplane
created_at: 2026-06-15
updated_at: 2026-07-07
framework_template_version: "0.3.1"
owner: harness
---

# Farplane Harness

## Mission

Make autonomous Codex work visible, reviewable, repeatable, and useful through
files, tickets, skills, goals, and proof.

Farplane is an agentic maintenance tool for harnesses. Product features must
serve that identity: they should improve how humans and agents maintain,
evaluate, steer, prove, or productize autonomous harness behavior.

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
| Evals and proof systems | Accepted proof patterns raise trust and reduce supervision. | Accepted agent-hours per human intervention rises while false completion falls. | Proof artifacts add friction but do not change decisions or trust. |
| Skill systems | Lessons become callable workflows instead of transcript residue. | Repeated misses decrease after skill updates. | Skills become stale docs that agents ignore or over-call. |
| Template tracking | Framework fixes become defaults instead of one-off repairs. | New projects reach first measured loop faster with fewer missing surfaces. | Templates drift faster than they help or become too hard to configure. |

## Feature Policy

Use this policy when creating, reviewing, or dogfooding `FEAT-*` docs:

```text
farplane_feature(candidate)
  -> stable_or_experimental_feature | system_policy | skill_workflow |
     ticket_artifact | report_evidence | retire
```

A Farplane feature is a durable capability or UX contract for an agentic
harness-maintenance product. It must help an operator or agent maintain,
evaluate, steer, prove, report on, or productize harness behavior.

Feature docs are allowed to be experimental when the capability is real enough
to dogfood but not globally stable. Experiments, automation runs, tickets, and
reports are evidence for a feature; they are not automatically features.

| Candidate | Classification |
| --- | --- |
| A recurring report that lets the operator evaluate harness behavior | feature |
| A scheduled automation row that invokes an existing skill | automation evidence |
| A generic reusable skill unrelated to Farplane's harness-maintenance UX | skill workflow |
| A broad product layer with multiple capabilities | system |
| A one-off hypothesis, ticket, or implementation patch | experiment or ticket artifact |
| A dead or superseded implementation shape | retired feature handle or folded history |

Feature docs should answer:

- What harness-maintenance UX or capability does this create?
- Which system owns it?
- Which surfaces implement it?
- What reports, tickets, evals, or artifacts prove it works?
- Is it stable, experimental, or superseded?

Dogfood and interval review should read this policy before judging whether an
experimental feature should continue, adjust, graduate, split, merge, or retire.

## Non-Tradeoffs

- Do not hide orchestration state in chat.
- Do not create a scheduler or daemon when visible automation prompts are
  enough.
- Do not store secrets in tracked project config.
- Do not silently rewrite the human thesis, durable leverage commitments, or
  product/domain boundary.

## Allocation Guardrails

| Guardrail | Rule |
| --- | --- |
| Proof | Claims about harness behavior, autonomy, trust, quality, or productivity need nonzero proof work. |
| Maintenance | Admin work stays bounded unless it unblocks product, proof, or current goals. |
| Distribution | Trust distribution must be grounded in accepted evidence, user pain, or an adoption gap. |
| Productization | Productization should follow accepted experiment, ablation, review, or operator-feedback evidence. |
| Runway | Active work must justify burn through revenue, validated learning, proof quality, distribution, reusable harness leverage, or unblock value. Work without weekly evidence should be paused, narrowed, or converted into instrumentation. |
| Authority | Publishing, spend, customer contact, deploys, destructive cleanup, and product/domain-boundary changes require explicit authorization unless already granted by ticket or policy. |

## Agent Authority

- Agents may evolve products, audiences, tickets, and goals through
  evidence-backed deltas.
- Agents may challenge the static thesis with evidence.
- Agents may propose a charter delta in a dated interval report.
- Agents may propose runway decisions in dated interval reports, but live spend,
  publishing, customer contact, and product/domain-boundary changes still
  require explicit authorization unless granted by ticket or policy.
- Agents may not silently rewrite the static thesis or durable leverage
  commitments.

## Change Rule

Static charter changes require an explicit human-approved harness delta.
