---
name: harness-advisor
description: Tier 2 Farplane harness placement advisor. Use when the user wants to make Farplane better at something and needs a grounded recommendation for whether to change AGENTS.md, global templates, skills, subagents, hooks/scripts, ticket contracts, docs/specs, validators, or registries.
tier: 2
source: local
---

# Harness Advisor

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] State the Farplane improvement request as one concrete harness failure or capability gap.
- [ ] Use [reference-grounding](../reference-grounding/SKILL.md) to inspect the
  smallest relevant local evidence before recommending a surface.
- [ ] Check `docs/features/registry.jsonl` for an existing or partial harness
  feature before proposing a new feature.
- [ ] Check `docs/skills/registry.jsonl` for an existing skill, method, source
  owner, or consolidation target before proposing a new skill.
- [ ] When a generated harness or skill graph exists, inspect it for backlinks,
  owner clusters, and surprising dependencies before recommending broad
  placement changes.
- [ ] Read `ARCHITECTURE.md` and the relevant owning spec when the request
  touches policy, canonical ownership, memory, specs, tickets, runtime, hooks,
  skills, registries, or source/feature provenance.
- [ ] Read `docs/specs/harness-engineering-doctrine.md` for placement rules.
- [ ] For material or ambiguous placement decisions, read
  [placement-axes](./references/placement-axes.md) and score context budget,
  reuse frequency, ownership fit, determinism, evidence surface, duplication
  risk, discoverability, and maintenance cost.
- [ ] Compare only realistic levers: repo `AGENTS.md`, global template, docs/specs,
  skill, subagent, hook/script, ticket contract, validator, or registry metadata.
- [ ] When the decision touches skills and subagents, separate actor-prompt
  ownership from reusable skill-contract ownership before recommending a
  surface.
- [ ] When recommending material review changes, place rubric routing in the
  calling skill or ticket `Proof Contract`, reviewer execution in
  `agents/reviewer.toml`, and TAS/family definitions in `skills/review`.
- [ ] Use [advise](../advise/SKILL.md) to compare exactly 3 viable placement
  options and recommend one.
- [ ] Name one primary owner and any secondary sync points.
- [ ] Hand implementation to the relevant Tier 3 workflow or visible ticket
  instead of doing hidden stateful work in chat.
- [ ] Use [review](../review/SKILL.md) before treating a material placement
  decision as ready.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

Use this when the operator asks how to improve Farplane itself and the right
surface is not obvious.

This is a Tier 2 workflow surface. It may call Tier 1 primitives directly, then
hand the chosen work to a Tier 3 domain skill such as `skill-maintenance`,
`impl-plan`, `$impl`, `qa`, `demo`, or another Farplane application skill.

## Job

1. Translate the improvement request into one concrete harness failure or
   capability gap.
2. Ground the current state in the smallest relevant Farplane surfaces.
3. Check whether the feature or skill already exists before proposing a new
   surface.
4. Score the placement axes: context budget, reuse, ownership, determinism,
   evidence surface, duplication risk, discoverability, and maintenance cost.
5. Compare the plausible placement levers.
6. Recommend one primary owner and any secondary sync points.
7. Name the implementation ticket(s), validation, and writeback required.

## Use When

- the user says "make Farplane better at X"
- the user asks where a harness rule, workflow, validator, skill, hook,
  subagent, ticket contract, registry field, or prompt policy should live
- a proposed improvement could fit several surfaces
- root `AGENTS.md` is at risk of absorbing procedural detail that may belong
  in a skill, spec, ticket contract, hook, or validator

## Do Not Use When

- the target surface is already chosen and the user only wants implementation
- the work is normal product/application code rather than Farplane harness work
- the question is only skill metadata/todos/registry maintenance; use
  [skill-maintenance](../skill-maintenance/SKILL.md)

## Required Grounding

Load only what the request needs:

- `docs/specs/harness-engineering-doctrine.md` for placement rules
- `ARCHITECTURE.md` for the canonical surface map when a request touches
  policy, memory, specs, tickets, runtime, hooks, skills, or feature/source
  provenance
- `references/placement-axes.md` for material or ambiguous placement decisions
  where context budget, reuse, ownership, determinism, or duplication risk
  needs explicit scoring
- `docs/features/README.md` and `docs/features/registry.jsonl` for existing
  harness techniques
- `docs/skills/README.md` and `docs/skills/registry.jsonl` for existing skills
- `skills/skill-maintenance/graph/*` or a future harness map artifact when the
  decision benefits from backlink, dependency, or owner-cluster context
- root `AGENTS.md` and `templates/global/AGENTS.md` when policy placement is a
  candidate
- `skills/deep-init-project/references/AGENTS_TEMPLATE.md` when generated
  project-agent behavior or project-local operating rules are a candidate
- `skills/deep-init-project/references/PROJECT_RULES_TEMPLATE.md` when
  generated project technical standards, commands, runtime, or QA paths are a
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
   Read `ARCHITECTURE.md` and the nearest owning spec when the request could
   affect canonical policy ownership or when the owning surface is ambiguous
   across docs, memory, tickets, skills, hooks, registries, or templates.
3. **Check registries.** Look for existing feature rows, skill rows, source
   ownership, and known limits before creating anything new.
4. **Score axes when needed.** For material or ambiguous decisions, use
   `references/placement-axes.md` to decide whether the problem is best solved
   by always-loaded policy, progressive skills, isolated subagents, durable
   docs/files, tools/MCPs, hooks/scripts, validators, tickets, or registries.
5. **Compare levers.** Consider only the surfaces that could realistically own
   the fix:
   - repo-local `AGENTS.md`
   - `templates/global/AGENTS.md`
   - generated project templates such as
     `skills/deep-init-project/references/AGENTS_TEMPLATE.md` and
     `PROJECT_RULES_TEMPLATE.md`
   - `docs/specs/*`
   - `skills/*`
   - `agents/*.toml`
   - hooks or scripts under `bin/`
   - ticket templates or ticket workflow docs
   - validators
   - feature or skill registry metadata
6. **Advise.** Use [advise](../advise/SKILL.md) to compare exactly 3 viable
   placement options and recommend one.
7. **Define handoff.** Name the Tier 3 skill or artifact that should implement
   the chosen change.
8. **Review.** Use [review](../review/SKILL.md) before treating a material
   placement decision as ready.

## Output

Produce a compact placement decision:

- `Decision`
- `Current evidence`
- `Existing feature/skill match`
- `Axes` when material or ambiguous
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
- Treat always-loaded prompt context as expensive. Prefer skills, references,
  docs, subagents, tools, hooks, or validators when the rule does not need to
  be active every turn.
- Do not create a new skill before checking the existing skill registry.
- Do not create a new feature row before checking the feature registry.
- Do not use a hook or validator for judgment-heavy work that is not
  deterministic.
- Do not hide implementation state in chat; create or update the visible
  ticket when the recommendation becomes work.
