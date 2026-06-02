---
name: prototyping
version: 0.1.0
description: Tier 1 primitive for proving a pattern at the smallest honest scale before expanding scope, automation, data volume, user count, file count, research breadth, or implementation complexity.
tier: 1
source: local
allowed-tools: Read, Glob, Grep
---

# Prototyping

Use when work is tempted to scale before the pattern is proven: broad batch
edits, many records, many skills, many users, wide workflow coverage, new
architecture, full automation, or polish before the real behavior is known.

This is a primitive, not a domain builder. It gives planning, research,
execution, review, data work, app work, and skill maintenance the same
sample-first move: prove `1 -> 10 -> 100`, then scale only when the evidence
supports it.

## Job

Define the smallest honest prototype that can expose the real pattern, run or
plan that proof, and decide whether to scale, revise, or stop.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Important Checklist

- [ ] State the scale risk: data volume, users, workflow breadth, architecture,
  automation, polish, file count, research breadth, or operational complexity.
- [ ] Name the hypothesis the prototype must prove or falsify.
- [ ] Pick the smallest representative slice, usually `1 -> 10 -> 100`.
- [ ] Include real examples, real edge cases, real users, real files, or real
  records where possible.
- [ ] Prefer the manual or non-scalable path first when it reveals the pattern
  faster than automation.
- [ ] Define the evidence that promotes the work to the next scale.
- [ ] Define the evidence that forces revision, simplification, or stopping.
- [ ] Label prototype-only shortcuts so they do not masquerade as production
  readiness.
- [ ] Return a `Prototype Note` to the active workflow before broadening scope.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Core Flow

1. Name the scale risk and the decision it could distort.
2. State the hypothesis that needs proof before scale.
3. Select a representative slice:
   - `1` for one true path or one hard example
   - `10` for pattern confidence across variation
   - `100` only after the first two steps expose stable rules
4. Do the non-scalable version when manual work will teach faster than
   automation.
5. Inspect what changed, broke, surprised, or repeated.
6. Decide the next move: scale, revise, shrink, split, or stop.

## Decision Branches

- **Data:** inspect a small representative sample before designing the full
  parser, schema, model, cleaning pass, or migration.
- **Apps:** serve one workflow or `1-10` real users before broad roles,
  permissions, automations, or architecture.
- **Batch edits:** transform `1-3` representative files before running a
  command over the whole tree.
- **Skill maintenance:** update a small mix of Tier 1, Tier 2, and complex
  Tier 3 skills before rewriting the full registry.
- **Research:** inspect a few representative sources or skills before expanding
  to the full source set.
- **Agent behavior:** run a small behavior probe before claiming general agent,
  prompt, or skill reliability.

## Judgment Questions

Use [advise](../advise/SKILL.md) when the prototype slice is not mechanically
obvious:

- What is the riskiest assumption?
- What is the smallest slice that can falsify it?
- What must be real, and what can safely be mocked?
- What would prove the pattern is ready for the next scale?
- What would prove the current approach should stop or simplify?

## Prototype Note

Return this shape to the active workflow:

- `Hypothesis`
- `Scale risk`
- `Representative slice`
- `Manual / non-scalable move`
- `Evidence observed or required`
- `Promote criteria`
- `Revise / stop criteria`
- `Next scale step`

## Guardrails

- Do not use toy samples that dodge the actual hard case.
- Do not scale volume before representative failure modes are visible.
- Do not generalize from one example unless the next sample step is named.
- Do not hide prototype shortcuts inside production contracts.
- Do not turn this primitive into a full research, planning, or execution
  workflow; hand back to the owning Tier 2 or domain skill after the prototype
  decision is clear.
