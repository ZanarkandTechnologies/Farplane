---
name: harness-advisor
description: Tier 2 Codexter harness placement advisor. Use when the user wants to make Codexter better at something and needs a grounded recommendation for whether to change AGENTS.md, global templates, skills, subagents, hooks/scripts, ticket contracts, docs/specs, validators, or registries.
tier: 2
source: local
---

# Harness Advisor

Use this when the operator asks how to improve Codexter itself and the right
surface is not obvious.

This is a Tier 2 workflow surface. It may call Tier 1 primitives directly, then
hand the chosen work to a Tier 3 domain skill such as `skill-maintenance`,
`impl-plan`, `$impl`, `qa`, `demo`, or another Codexter application skill.

## Job

1. Translate the improvement request into one concrete harness failure or
   capability gap.
2. Ground the current state in the smallest relevant Codexter surfaces.
3. Check whether the feature or skill already exists before proposing a new
   surface.
4. Compare the plausible placement levers.
5. Recommend one primary owner and any secondary sync points.
6. Name the implementation ticket(s), validation, and writeback required.

## Use When

- the user says "make Codexter better at X"
- the user asks where a harness rule, workflow, validator, skill, hook,
  subagent, ticket contract, registry field, or prompt policy should live
- a proposed improvement could fit several surfaces
- root `AGENTS.md` is at risk of absorbing procedural detail that may belong
  in a skill, spec, ticket contract, hook, or validator

## Do Not Use When

- the target surface is already chosen and the user only wants implementation
- the work is normal product/application code rather than Codexter harness work
- the question is only skill metadata/todos/registry maintenance; use
  [skill-maintenance](../skill-maintenance/SKILL.md)

## Required Grounding

Load only what the request needs:

- `docs/specs/harness-engineering-doctrine.md` for placement rules
- `docs/features/README.md` and `docs/features/registry.jsonl` for existing
  harness techniques
- `docs/skills/README.md` and `docs/skills/registry.jsonl` for existing skills
- root `AGENTS.md` and `templates/global/AGENTS.md` when policy placement is a
  candidate
- `agents/*.toml` when independent lane ownership is a candidate
- hooks and scripts under `bin/` when deterministic boundary checks are a
  candidate
- ticket templates/specs when the work-package or proof contract is the likely
  owner
- the relevant existing skill files before proposing a new skill

## Workflow

1. **State the decision.** Name the exact improvement and what needs to be
   placed.
2. **Ground current state.** Use
   [reference-grounding](../reference-grounding/SKILL.md) for compact local
   evidence. Use a focused `research:*` method only when local evidence is not
   enough.
3. **Check registries.** Look for existing feature rows, skill rows, source
   ownership, and known limits before creating anything new.
4. **Compare levers.** Consider only the surfaces that could realistically own
   the fix:
   - repo-local `AGENTS.md`
   - `templates/global/AGENTS.md`
   - `docs/specs/*`
   - `skills/*`
   - `agents/*.toml`
   - hooks or scripts under `bin/`
   - ticket templates or ticket workflow docs
   - validators
   - feature or skill registry metadata
5. **Advise.** Use [advise](../advise/SKILL.md) to compare exactly 3 viable
   placement options and recommend one.
6. **Define handoff.** Name the Tier 3 skill or artifact that should implement
   the chosen change.
7. **Review.** Use [review](../review/SKILL.md) before treating a material
   placement decision as ready.

## Output

Produce a compact placement decision:

- `Decision`
- `Current evidence`
- `Existing feature/skill match`
- `Options`
- `Recommendation`
- `Tradeoff accepted`
- `Primary owner`
- `Secondary sync points`
- `Validation`
- `Next ticket`

## Guardrails

- Do not turn this skill into a root-policy encyclopedia. Link the owning docs
  and registries instead.
- Do not default to root `AGENTS.md`; prefer the smallest surface that fixes
  the failure.
- Do not create a new skill before checking the existing skill registry.
- Do not create a new feature row before checking the feature registry.
- Do not use a hook or validator for judgment-heavy work that is not
  deterministic.
- Do not hide implementation state in chat; create or update the visible
  ticket when the recommendation becomes work.
