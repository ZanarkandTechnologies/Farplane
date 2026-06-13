---
title: "Subagent Context Packet Standard"
status: active
owner: deliberative-advice
created_at: 2026-06-13
updated_at: 2026-06-13
tags:
  - subagents
  - context
  - deliberative-advice
refs:
  - docs/specs/context-and-handoff-policy.md
  - skills/deliberative-advice/SKILL.md
  - templates/global/AGENTS.md
---

# Subagent Context Packet Standard

## Decision Or Task

Implement the discussed Farplane rule that nontrivial subagent handoffs should
not use thin prompts. Subagents should receive a durable `context_ref`, and
ticket IDs should be used when work is ticketed but not forced for pure advice
or decision councils.

## Why This Matters

A previous `deliberative-advice` council pass spawned independent lanes with
short prompts that summarized a long discussion. The lanes were technically
independent but lost important prior context, options, constraints, and user
intent. That made the council less valuable.

## Current Behavior

- Global delegation guidance asked callers to provide bounded inputs, files,
  expected output, evidence, and review focus.
- `deliberative-advice` asked for an evidence packet but did not require that
  packet to exist as a durable artifact.
- Receiver agents varied: `reviewer` required a durable task pointer, while
  other agents did not consistently ask for context packets.

## Expected Behavior

- Before spawning a nontrivial subagent, the caller writes or identifies a
  durable `context_ref`.
- Ticketed work uses the ticket path or ticket-scoped artifacts.
- Non-ticket advice, council, research, or decision work uses a context packet
  under `.farplane/context/` or `experiments/decisions/`.
- `deliberative-advice` council mode creates or identifies a Council Context
  Packet before spawning lanes.
- Receiver agents may block material handoffs that lack a durable pointer.

## Options Considered

1. Require every subagent to receive a ticket ID.
2. Require every nontrivial subagent to receive a `context_ref`; ticket ID is
   optional and preferred only for ticketed work.
3. Update every `agents/*.toml` with a hard ticket-or-context refusal rule.

Chosen option: Option 2, with light receiver-side updates for material
review/QA/planning/documentation/hardcase agents.

## Evidence Refs

- `docs/specs/context-and-handoff-policy.md`
- `templates/global/AGENTS.md`
- `AGENTS.md`
- `skills/deliberative-advice/SKILL.md`
- `skills/deliberative-advice/references/llm-council-model.md`
- `skills/deliberative-advice/eval_task.json`
- `agents/reviewer.toml`
- `agents/qa-tester.toml`
- `agents/planner-agent.toml`
- `agents/documentation-maintainer.toml`
- `agents/hardcase-curator.toml`
- `docs/fundamentals/prompt-engineering.md`
- `docs/skills/best-practices.md`
- `docs/features/registry.jsonl`

## Relevant Files

- Changed policy/spec surfaces:
  - `docs/specs/context-and-handoff-policy.md`
  - `templates/global/AGENTS.md`
  - `AGENTS.md`
  - `docs/fundamentals/prompt-engineering.md`
  - `docs/skills/best-practices.md`
- Changed council skill surfaces:
  - `skills/deliberative-advice/SKILL.md`
  - `skills/deliberative-advice/references/llm-council-model.md`
  - `skills/deliberative-advice/eval_task.json`
  - `skills/deliberative-advice/audits/2026-06-13-council-context-packet.md`
- Changed receiver prompts:
  - `agents/reviewer.toml`
  - `agents/qa-tester.toml`
  - `agents/planner-agent.toml`
  - `agents/documentation-maintainer.toml`
  - `agents/hardcase-curator.toml`

## Constraints And Non-Goals

- Do not force tickets for pure decision or council work.
- Do not update every agent prompt with bulky repeated policy.
- Do not add hidden orchestration, daemons, or hooks.
- Do not create a new skill; `deliberative-advice` owns council behavior.
- Keep the rule prompt-and-eval enforced; it is judgment-heavy and not a
  deterministic validator.

## Lane Assignments

Reviewer lane should check:

- skill-contract correctness for `deliberative-advice`
- integration readiness across global/project policy, spec, feature registry,
  and selected agent prompts
- evidence-quality for validation commands and eval coverage

## Expected Output

Return a TAS-style review with:

- `overall_tas`
- `verdict`
- blocking findings
- hard gate failures
- rerun requirement
- next action

## Proof Or Review Gate

Mechanical proof already run:

```text
python3 -m json.tool skills/deliberative-advice/eval_task.json
python3 <jsonl parse check for docs/features/registry.jsonl>
git diff --check
python3 skills/skill-maintenance/scripts/check_skills.py --write
```

Reviewer should verify the edited surfaces are consistent and that the new rule
does not create ticket bureaucracy for pure decision work.
