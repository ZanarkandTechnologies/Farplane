# Skill Contract Review

Use this family when skill files, skill-system behavior, registries, skill
templates, or skill maintenance rules changed.

## TAS Guide

- `TAS-A`: the skill can be used from files alone, with concise first-load
  logic, clear boundaries, no harmful duplication, and explicit proof.
- `TAS-B`: the skill is directionally useful, but a repeated-agent run would
  still depend on hidden context, duplicated instructions, vague proof, or a
  fuzzy branch.
- `TAS-C`: the skill is wrong-scope, misleading, non-repeatable, bloated enough
  to fail normal use, or mixes actor/runtime ownership into a reusable skill
  contract in a way that will recurse or drift.
- `TAS-D`: there is not enough task context, changed-skill content, or evidence
  to judge the skill honestly.

## Dimensions

### Trigger Accuracy

Inspect: frontmatter description, use-when text, and nearby registry metadata.

- Would another agent know when to invoke this skill?
- Is the trigger too broad, too narrow, or still tied to stale product names?
- Does the skill avoid pretending to be a universal router?

### First-Load Checklist

Inspect: `## Important Checklist` and any linked method or reference.

- Is the checklist operational rather than educational?
- Are branch labels clear without nested checklist complexity?
- Does it name required proof/review steps without copying whole references?

### Repeatability

Inspect: paths, scripts, commands, artifact locations, templates, and examples.

- Can another agent rerun the workflow from repo files alone?
- Are setup/onboarding details separated from normal run-path steps?
- Are hidden chat assumptions replaced with visible files or task pointers?

### Boundary Fit

Inspect: actor prompts, caller skills, references, and reusable skill body.

- Are actor identity, subagent spawning, tool-use policy, and artifact
  writeback kept outside reusable skills unless this is an orchestration skill?
- Does the skill own the reusable contract rather than the caller's routing
  decision?

### Duplication Control

Inspect: `SKILL.md`, references, templates, README, generated registry/plugin
copies when relevant.

- Is the same instruction repeated across surfaces without a distinct job?
- Would a future update have to fix the same rule in many places?
- Does generated output match source without becoming a second source of truth?

### Proof Readiness

Inspect: validator commands, registry sync commands, ticket evidence, and
generated artifacts.

- Are required checks explicit and runnable?
- Does evidence prove source and generated copies are synced when that matters?
- Are registry or plugin sync effects validated?

## Evidence Cues

- Source `SKILL.md` diff
- Relevant reference/template diffs
- `docs/skills/best-practices.md`
- `docs/skills/registry.jsonl` and generated graph/plugin sync outputs
- Skill-system validator output
- Ticket proof contract and review artifacts

## Finding Cues

- Hidden reviewer or subagent routing inside a reusable non-orchestration skill
- Long onboarding prose in the first-load checklist
- Missing proof commands for changed scripts or generated registries
- Stale generated plugin or graph copy
- Repeated wording that will drift across `SKILL.md`, references, and templates
