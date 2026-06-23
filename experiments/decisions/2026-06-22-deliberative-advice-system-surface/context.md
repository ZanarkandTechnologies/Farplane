---
title: Deliberative Advice System Surface Council Context
date: 2026-06-22
status: active
owner: deliberative-advice
decision_type: harness-placement
---

# Decision

Should Farplane make council-style deliberative advice a first-class system
workflow surface beyond the existing `deliberative-advice` skill, or keep it as
an on-demand skill invoked only for costly decisions?

# Why This Matters

Council mode is useful when the operator wants structured disagreement,
independent first passes, critique, synthesis, and preserved dissent. But a
first-class system surface can add ceremony, latency, prompt bloat, and hidden
orchestration if it is promoted too broadly. The recommendation should preserve
operator leverage without making routine work heavier.

# Prior Discussion Summary

The operator asked to test the full council on something for the system. No
implementation change has been requested. This is a reusable decision test for
Farplane's harness design.

# Current Behavior

- `deliberative-advice` exists as a local Tier 2 skill at
  `/Users/kenjipcx/.codex/skills/deliberative-advice/SKILL.md`.
- The skill requires a named decision, grounding, a durable Council Context
  Packet, independent perspective passes, critique/ranking, chair synthesis,
  preserved dissent, and a concrete next owner.
- Farplane project policy says reusable procedures belong in skills, detailed
  state belongs in visible artifacts, subagents are bounded specialists, and
  root/global prompt expansion is a last resort.
- Farplane doctrine says the default tuning order is proof/review, ticket or
  work-package contract, skill contract, context/file policy, subagent
  boundary, hooks/validators/tools, automation, then root/global prompt.

# Expected Behavior

Farplane should have a clear rule for when to use a council, where its artifacts
belong, and whether any additional system surface is worth adding now.

# Options Under Consideration

1. Keep council mode as an on-demand `deliberative-advice` skill only.
2. Add a lightweight checklist or routing note in repo/global policy that points
   agents to `deliberative-advice` for high-stakes decisions.
3. Create a first-class council workflow package with templates, lane prompts,
   aggregation scripts, and optional reviewer/QA gates.

# Evidence Refs

- `AGENTS.md`: Farplane local harness policy and surface placement rules.
- `docs/fundamentals/harness-engineering-doctrine.md`: priority order,
  lever guide, promotion rules, and placement analysis.
- `docs/LESSONS.md`: `2026-06-13 thin council prompts` lesson requiring a
  durable Context Packet and bounded subagent lane contracts.
- `skills/skill-maintenance/audits/2026-06-13-behavior-delta-compression.md`:
  prior council use that produced reusable decision artifacts.
- `/Users/kenjipcx/.codex/skills/deliberative-advice/SKILL.md`: active skill
  contract being tested.

# Grounding Note

- Question / claim: Council deliberation should be promoted only if the current
  skill surface is insufficient for repeated high-stakes Farplane decisions.
- Local baseline: Farplane already recognizes `deliberative-advice` as a Tier 2
  escalation path, requires durable context packets for nontrivial subagent
  handoffs, and prefers skills over always-loaded prompt for repeated but
  non-global procedures.
- Source need: local-only evidence is enough for this test because the decision
  concerns Farplane's internal harness surface placement, not current external
  APIs or market behavior.
- Sources checked: the local project policy, harness doctrine, lessons ledger,
  existing prior council audit, and the skill contract.
- Evidence: local doctrine favors the smallest lever; council mode already has
  an owner skill; thin council prompts have been a known failure mode; prior
  useful council output lives as experiment/audit artifacts rather than hidden
  chat state.
- Confidence: medium-high for placement; low for usage frequency because no
  metric was gathered on how often operators want councils.
- Local impact: the likely near-term improvement is better invocation guidance
  and templates, not a new orchestration runtime.
- Escalation needed: usage telemetry or operator interviews before building a
  larger workflow package.

# Constraints / Non-Goals

- Do not edit live installed skill bodies or global prompt files during this
  test.
- Do not create a ticket unless the final recommendation calls for follow-up
  implementation.
- Do not treat this as a majority vote; chair synthesis should judge argument
  quality and local fit.
- Preserve meaningful dissent even if the recommendation is clear.

# Lane Briefs

## Operator Value

Judge what best serves the operator's time, taste, leverage, and trust in the
system. Focus on when council ceremony feels valuable versus heavy.

## Engineering Risk

Judge implementation, maintenance, integration, proof, and failure risks.
Focus on prompt bloat, hidden orchestration, stale templates, and fragmented
surfaces.

## Evidence Skeptic

Judge what is unsupported or overclaimed. Focus on whether the evidence proves
need, frequency, or insufficiency of the existing skill.

## Systems Fit

Judge where this belongs across repo `AGENTS.md`, `templates/global/AGENTS.md`,
`skills/*`, `agents/*.toml`, hooks/scripts, tickets, docs, and experiments.

# Output Shape

Each lane should return:

- Recommendation: choose option 1, 2, or 3.
- Strongest reason.
- Strongest opposing point.
- Evidence that would change your mind.
- Concrete next owner or proof surface.

# Proof / Next Owner

This test is complete when:

- independent lane outputs are collected before critique;
- chair synthesis compares exactly three options;
- dissent and confidence are explicit;
- the next owner or evidence gap is named;
- artifacts are stored under this decision directory.
