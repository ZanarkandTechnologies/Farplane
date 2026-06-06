# Skill Best Practices

Use this as the shared standard for creating, reviewing, and maintaining
Farplane skills. Apply it to `skill-creator` and `skill-maintenance` first;
roll it out to other skills only after a representative pass proves the shape.

## First-Load Shape

- Put a short `## Context` section near the top of `SKILL.md` before the todo
  list when the skill depends on tier, ownership, source, or surrounding
  system shape.
- `## Todo List` is the first-load todo list, not a generic checklist section.
- Use sequential task-list items such as `1. [ ]`, `2. [ ]`, and `3. [ ]` for
  ordered work.
- Make every top-level todo an executable action with an observable result.
  Move policy, tips, and warnings to `## Gotchas`, `## Core Rules`, or nested
  verification checks.
- Use nested numbered task-list items for branch choices that should stay
  ordered and easy to reference.
- Use plain markdown todos such as `- [ ]` only for embedded verification or
  detail checks under a numbered todo.
- Do not use unordered prose bullets inside `## Todo List`; branch choices
  should be numbered task items, and embedded checks should be checkbox items.
- Do not put literal `FARPLANE_IMPORTANT_CHECKLIST` marker comments inside
  fenced examples; link the source template instead.
- Fold the default workflow into the numbered todo list instead of repeating it
  in a second workflow section.
- Do not add a generic `## Job` section when `## Context` plus `## Todo List`
  already state the work. Use a specific section name such as `## Contract` only
  when it adds a durable contract that is not just a repeat of the todo list.
- Put final review as the last numbered todo. Embedded plain todo checks are
  allowed under that final todo; avoid deep checkbox trees elsewhere.
- Move onboarding, examples, rubric detail, and long rationale to references.
- A good first-load todo list should tell the next agent what to do now, not
  teach the whole domain.

## Main File Versus References

- `SKILL.md` owns trigger conditions, job, branch routing, hard gates, and proof
  obligations.
- References own conditional detail: onboarding, examples, templates, long
  rubrics, model maps, and rare-path recipes.
- If a reference must be read on every invocation, promote the needed rule into
  `SKILL.md`.
- Do not copy the same instruction into `SKILL.md`, references, templates, and
  README-style docs unless each surface has a distinct job.

## Actor Prompts Versus Skill Contracts

- Actor prompts such as `agents/*.toml` own identity, responsibility,
  delegation boundaries, tool use, durable task loading, artifact writeback,
  and anti-recursion rules.
- Skills own reusable domain contracts: trigger boundaries, rubric or workflow
  shape, templates, hard gates, and proof expectations.
- Do not put subagent spawning, caller routing, or actor identity inside a
  reusable skill unless that skill's primary job is orchestration.
- When a skill is equipped to an agent, the skill should remain usable as a
  lower-level contract without causing the agent to delegate itself.

## Repeatability

Repeatability is the core quality bar for skills.

A skill is repeatable when another agent can use it from repo files alone
without hidden chat context, rediscovering prior decisions, or depending on the
author's memory.

Check repeatability by asking:

- Can another agent identify when to use the skill from its description?
- Can it execute the first-load todo list without reading every reference?
- Are scripts, commands, paths, artifacts, and validation steps explicit?
- Are setup/onboarding paths separated from the normal run path?
- Does the skill avoid verbose duplication that would drift later?

## Review Gate

Before calling skill work complete, run a review pass that checks:

- concise first-load todo list
- branch-aware workflow shape
- references used only for conditional detail
- no duplicated instructions across surfaces
- explicit proof commands and artifacts
- repeatability from files alone

For nontrivial skill work, delegate review to the native `reviewer` subagent
when one is available. The calling skill owns rubric routing: pass a reviewer
handoff with the active ticket or task artifact, changed skill files, evidence
artifacts, review focus, rubric families, required TAS gates, hard gates, and
expected output path. Use
`skills/review/references/reviewer-handoff.md` for the template.

For skill work, the usual caller-declared families are `skill-contract`,
`integration-readiness`, and `evidence-quality`. Add task-specific hard gates
for repeatability, duplicated first-load logic, actor-prompt versus
skill-contract boundaries, and explicit proof commands. Self-review is
acceptable for tiny mechanical edits, but it is weaker at catching duplicated
instructions, hidden assumptions, and vague "sounds good" skill contracts.

For large skill-system rollouts, prove the pattern on a representative sample
before editing the whole registry.
