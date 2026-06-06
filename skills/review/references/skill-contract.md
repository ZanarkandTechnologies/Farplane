# Skill Contract Review

Use this family when skill files, skill-system behavior, registries, skill
templates, or skill maintenance rules changed.

## TAS Guide

- `TAS-A`: the skill can be used from files alone, with concise first-load
  logic, clear boundaries, no harmful duplication, and explicit proof.
- `TAS-B`: the skill is directionally useful, but one or more required checks
  fail in a repairable way.
- `TAS-C`: a blocker check fails, the skill is wrong-scope, misleading,
  non-repeatable, bloated enough to fail normal use, or mixes actor/runtime
  ownership into a reusable skill contract in a way that will recurse or drift.
- `TAS-D`: there is not enough task context, changed-skill content, or evidence
  to judge the skill honestly.

## Checklist Modules

### Required Checks

- [ ] `trigger-clear`: Frontmatter description, use-when text, and nearby
  registry metadata let another agent identify when to invoke the skill.
- [ ] `scope-bounded`: The trigger is neither too broad nor too narrow and does
  not pretend the skill is a universal router.
- [ ] `checklist-operational`: The `## Todo List` tells the next
  agent what to do now instead of teaching the whole domain.
- [ ] `branch-aware`: Branch labels or conditional steps are clear without
  nested checklist complexity.
- [ ] `reference-placement`: Onboarding, examples, templates, long rubric
  detail, and rare paths live in references rather than the first-load body.
- [ ] `file-repeatable`: Another agent can rerun the workflow from repo files,
  paths, scripts, commands, and artifact locations alone.
- [ ] `proof-explicit`: Required checks, validators, generated-registry sync,
  or artifact proof commands are explicit and runnable.
- [ ] `source-of-truth-clear`: Generated copies, registries, plugin outputs, or
  installed copies are not treated as a second source of truth.

### Blocker Checks

- [ ] `wrong-scope`: The skill solves a different workflow than the user,
  ticket, or registry claims.
- [ ] `actor-boundary-leak`: Actor identity, subagent spawning, tool-use policy,
  or artifact writeback is placed inside a reusable non-orchestration skill.
- [ ] `non-repeatable`: A repeated-agent run depends on hidden chat context,
  unstated local state, or undocumented operator memory.
- [ ] `harmful-duplication`: The same rule is duplicated across `SKILL.md`,
  references, templates, README, or generated outputs in a way likely to drift.
- [ ] `bloated-first-load`: Required first-load content is long enough that a
  normal invocation will skip or misapply it.

### Evidence Checks

- [ ] `source-diff-reviewed`: Source `SKILL.md` and relevant references or
  templates were inspected, not only generated registry rows.
- [ ] `best-practices-checked`: `docs/skills/best-practices.md` was checked
  when checklist shape, reference placement, or repeatability changed.
- [ ] `registry-validated`: Registry or generated graph/plugin sync output was
  validated when metadata or generated surfaces changed.

## Evidence Cues

- Source `SKILL.md` diff
- Relevant reference/template diffs
- `docs/skills/best-practices.md`
- `docs/skills/registry.jsonl` and generated graph/plugin sync outputs
- Skill-system validator output
- Ticket proof contract and review artifacts

## Finding Cues

- Hidden reviewer or subagent routing inside a reusable non-orchestration skill
- Long onboarding prose in the first-load todo list
- Missing proof commands for changed scripts or generated registries
- Stale generated plugin or graph copy
- Repeated wording that will drift across `SKILL.md`, references, and templates
