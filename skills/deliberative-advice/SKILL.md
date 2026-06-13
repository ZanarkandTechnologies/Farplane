---
name: deliberative-advice
description: "Turn a high-stakes or expensive decision into independent perspectives, critique, synthesis, dissent, and one recommended path."
tier: 2
source: local
skill_template_version: "0.1.0"
methods: ["advise:complex", "advise:council"]
allowed-tools: Read, Glob, Grep
---

# Deliberative Advice

## Context

`deliberative-advice` is the Tier 2 escalation path for decisions where plain
`advise` is too shallow. Use it when the decision is costly, irreversible,
cross-functional, strategically important, or likely to benefit from structured
disagreement.

This skill adapts the council pattern: independent first-pass positions,
blind or semi-blind critique, chair synthesis, and explicit dissent. Keep
normal reversible choices in [advise](../advise/SKILL.md).

## Skill Signature

```text
deliberative_advice(decision, stakes?, context_ref?, mode?) -> recommendation + dissent + next_owner
state: reads(context packet?, evidence refs, relevant files); writes(council context packet? or decision note?)
gates: decision_named; context_packet_for_council; independent_first_passes; dissent_preserved; next_owner_named
routes: advise | reference-grounding | research | review
fails: thin council prompts; shared hidden context; majority vote; recommendation without proof owner
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. State the real decision, stakes, default path, and what would make a
  recommendation useful.
- [ ] 2. Ground the decision before convening the council.
   - [ ] If compact evidence is enough, use
     [reference-grounding](../reference-grounding/SKILL.md).
   - [ ] If multiple sources, comparables, or source normalization are required,
     name the needed research method before finalizing.
- [ ] 3. Choose `3-5` perspective briefs that expose different failure modes.
   - [ ] Include an evidence-skeptic perspective for claims that depend on
     external facts, local baseline, cost, safety, or current behavior.
   - [ ] Include an operator-value perspective for decisions that affect the
     user's taste, time, money, reputation, or workflow.
- [ ] 4. For `advise:council`, create or identify a Council Context Packet
  before spawning lanes.
   - [ ] If a ticket exists, link or write the packet under that ticket's
     artifacts or progress surface.
   - [ ] If no ticket exists, write the packet under `.farplane/context/` for
     ephemeral decisions or `experiments/decisions/` for reusable decisions.
   - [ ] Include decision, stakes, prior discussion summary, options, evidence
     refs, relevant files, constraints, lane briefs, output shape, and proof or
     next-owner expectations.
- [ ] 5. Spawn native subagents or isolated lanes for the perspective briefs
  when the runtime supports them.
   - [ ] Give each lane the Council Context Packet path, lane-specific
     perspective, criteria, and output shape.
   - [ ] Keep each lane independent until its first-pass recommendation is
     captured.
   - [ ] If native subagents are unavailable, run clearly separated isolated
     perspective passes and state that limitation in the output.
- [ ] 6. Collect independent first-pass recommendations before showing any
  perspective the others' answers.
- [ ] 7. Run critique and ranking.
   - [ ] Use blind or semi-blind labels when feasible so the critique scores the
     argument rather than the author, model, or role.
   - [ ] Ask each perspective to name the strongest opposing point and the
     evidence that would change its mind.
- [ ] 8. Produce chair synthesis.
   - [ ] Compare exactly 3 viable final options unless fewer than 3 are real.
   - [ ] Recommend one option clearly.
   - [ ] Name dissent, uncertainty, and the tradeoff accepted.
- [ ] 9. Define the next owner and proof surface.
   - [ ] Route implementation to the owning skill, ticket, spec, or direct next
     action.
   - [ ] Record the evidence gap instead of overstating confidence when the
     council lacks the needed facts.
- [ ] 10. Review before completion.
   - [ ] The council used independent perspectives rather than one simulated
     monologue.
   - [ ] Council lanes received a durable context packet path rather than thin
     prompts that rely on hidden chat memory.
   - [ ] Native subagents or isolated lanes were used for first-pass
     recommendations, or the runtime limitation is explicit.
   - [ ] The final answer preserved meaningful dissent.
   - [ ] The recommendation is grounded, or the exact evidence gap is explicit.
   - [ ] The next step and owner are concrete.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Council Shape

Use this default set unless the decision clearly needs different lenses:

- `Operator value`: what best serves the user's goal, taste, leverage, and
  opportunity cost.
- `Engineering risk`: what can fail in implementation, maintenance, migration,
  integration, or proof.
- `Evidence skeptic`: what is unsupported, stale, overfit, missing, or
  dependent on current facts.
- `Systems fit`: what belongs in the right Farplane surface and avoids
  duplication or hidden state.
- `Chair`: synthesizes the strongest argument, dissent, confidence, and next
  owner.

## Templates

Council context packet:

- `Decision`
- `Why this matters`
- `Prior discussion summary`
- `Current behavior`
- `Expected behavior`
- `Options under consideration`
- `Evidence refs`
- `Relevant files`
- `Constraints / non-goals`
- `Lane briefs`
- `Output shape`
- `Proof / next owner`

Council decision note:

- `Decision`
- `Stakes`
- `Grounding`
- `Perspectives`
- `Critique / ranking`
- `Recommendation`
- `Dissent`
- `Tradeoff accepted`
- `Confidence`
- `Next owner`
- `Proof / evidence gap`

## Gotchas

- Do not use this to delay a simple reversible action.
- Do not let all perspectives share one hidden chain of reasoning; collect
  independent answers before critique.
- Do not spawn council lanes from thin prompts when prior discussion, options,
  evidence, or constraints matter. Write or reuse a Council Context Packet and
  pass its path to every lane.
- Do not create role theater. Each perspective must have a distinct failure
  mode or decision criterion.
- Do not convert ranked disagreement into majority vote. The chair must judge
  argument quality, evidence, and local fit.
- Do not hide cost, latency, or extra coordination. Use this only when the
  decision deserves the ceremony.

## Reference Map

- [references/llm-council-model.md](references/llm-council-model.md) - read
  when adapting Karpathy-style council mechanics or explaining why this skill
  uses independent answers, critique, and chair synthesis.
- [../advise/SKILL.md](../advise/SKILL.md) - use for normal recommendation
  calls that need 3 options and one direct recommendation.
- [../reference-grounding/SKILL.md](../reference-grounding/SKILL.md) - use for
  compact evidence checks before or during the council.
- [../research/SKILL.md](../research/SKILL.md) - use when the decision depends
  on multi-source parity, gap, official-docs, code-pattern, competitor, user, or
  source-synthesis evidence.
- [../review/SKILL.md](../review/SKILL.md) - use before treating material
  council output as ready.

## Output

Return or write a compact council decision note with:

- one clear recommendation
- the strongest dissent
- confidence level
- tradeoff accepted
- next owner or skill
- proof command, evidence artifact, or explicit evidence gap
