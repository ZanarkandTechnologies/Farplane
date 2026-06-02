# Prompt Quality Review

Use this family when subagent prompts, delegated CLI prompts, AI-powered app
behavior prompts, structured-output prompts, eval judges, or reusable operator
prompts changed.

## TAS Guide

- `TAS-A`: the prompt has clear job boundaries, durable context inputs,
  concrete output shape, grounded constraints, and no role or delegation drift.
- `TAS-B`: the prompt is usable but has meaningful ambiguity, overbroad role
  claims, weak output constraints, or underspecified evidence/tool expectations.
- `TAS-C`: the prompt would likely cause wrong-role behavior, hallucinated
  claims, missing proof, recursive delegation, unsafe action, or unusable
  output.
- `TAS-D`: the prompt cannot be judged because the task, caller context, or
  expected runtime is missing.

## Dimensions

### Task Clarity

- Is the job concrete enough that the model can act without guessing intent?
- Are scope boundaries and non-goals explicit?
- Are material terms defined or grounded in linked artifacts?

### Context Contract

- Does the prompt require durable pointers when material judgment depends on
  files, tickets, PRs, specs, or artifacts?
- Does it avoid relying on hidden chat-only state?
- Are newer user updates handled as local overrides without discarding
  non-conflicting earlier constraints?

### Role Boundary

- Does the actor know what it owns and does not own?
- Are implementation, review, QA, planning, and routing responsibilities kept
  separate when separation matters?
- Does the prompt prevent recursive delegation when equipped with the skill it
  calls?

### Output Contract

- Is the expected output shape explicit enough to be consumed by the caller?
- Are verdicts, gates, next actions, and artifact paths specified when needed?
- Does the prompt avoid fake precision and unsupported scores?

### Groundedness And Safety

- Does the prompt require evidence before claims?
- Does it prevent invented facts, unsupported certainty, and overclaiming?
- Are destructive, external, spend, deploy, or publish actions gated by the
  surrounding workflow?

## Evidence Cues

- Prompt file diff
- `rules/prompt-engineering.md`
- Caller workflow or agent config
- Ticket proof contract or expected output schema
- Prior failure notes in `docs/TROUBLES.md` when relevant

## Finding Cues

- Chat-only task context accepted for material review
- Role says "review" but also implements fixes
- Prompt asks for a score without calibrated meaning
- Output shape missing `verdict`, `hard_gate_failures`, or `next_action`
- Subagent prompt tells itself to spawn the same subagent again
