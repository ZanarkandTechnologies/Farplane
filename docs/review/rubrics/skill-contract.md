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
- [ ] `nodes-executable`: Every top-level Todo is one bounded Golden Workflow
  Node with a compact input/output-or-branch signature, a domain Rule,
  observable Assert conditions, and inspectable state for its consumer.
- [ ] `nodes-specific`: A node cannot be pasted into an unrelated skill with
  noun substitution. Generic bind, inspect, transform, preserve, self-audit,
  and next fields do not count as domain workflow value.
- [ ] `edge-visible`: At least one important node uses a non-obvious signal to
  change a decision or route. Important domain skills reach `differentiated`;
  `proven` is reserved for candidate/no-skill hardcase evidence.
- [ ] `golden-calibrated`: Judgment-heavy or quality-dependent paths include a
  representative end-to-end golden trace with decisive nodes, accepted output,
  transferable invariants, and a generic/no-skill comparison.
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
- [ ] `qa-owned`: A touched `qa_checklist.md` has an explicit `keep | migrate |
  delete` decision. Only skill-specific runtime, safety, or preflight guards
  remain; structure, judgment, and deterministic rules use their canonical
  node, golden, eval, rubric, or validator owners.

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
- [ ] `generic-default-path`: The normal path remains generic assistant hygiene
  and therefore supplies no reusable domain advantage.
- [ ] `golden-answer-key`: The example can be copied as fixture facts or wording
  instead of transferring decisive invariants to held-out inputs.

### Evidence Checks

- [ ] `source-diff-reviewed`: Source `SKILL.md` and relevant references or
  templates were inspected, not only generated registry rows.
- [ ] `best-practices-checked`: `docs/skills/best-practices.md` was checked
  when checklist shape, reference placement, or repeatability changed.
- [ ] `route-appropriate`: The chosen reasoning route matched
  `docs/skills/best-practices.md#advice-and-proof-routing`; standards,
  compounding surfaces, behavioral claims, and evidence gaps used the right
  combination of first-principles reasoning, `advise`, `deliberative-advice`,
  research, evals, and reviewer readiness.
- [ ] `registry-validated`: Registry or generated graph/plugin sync output was
  validated when metadata or generated surfaces changed.
- [ ] `behavior-compared`: Behavior-sensitive changes include normal, hard,
  and boundary cases; a `proven` edge includes candidate/no-skill evidence.

## Advantage Calibration

```text
generic        = reusable assistant hygiene
operational    = domain nouns and concrete outputs
differentiated = non-obvious signal -> decision rule -> changed route
proven         = differentiated behavior beats no-skill on representative hardcases
```

Do not average this into a numeric score. A skill is not ready when its default
path is `generic`; important domain skills require `differentiated`. Claim
`proven` only with inspected comparison evidence.

## Evidence Cues

- Source `SKILL.md` diff
- Relevant reference/template diffs
- `docs/skills/best-practices.md`
- `docs/skills/registry.jsonl` and generated graph/plugin sync outputs
- Skill-system validator output
- Ticket `Done / Proof` and review artifacts

## Finding Cues

- Hidden reviewer or subagent routing inside a reusable non-orchestration skill
- Long onboarding prose in the first-load todo list
- Missing proof commands for changed scripts or generated registries
- Stale generated plugin or graph copy
- Repeated wording that will drift across `SKILL.md`, references, and templates
- Todo nodes whose Rule or Assert merely restates their title
- Goldens that show a polished output but hide the decisive workflow moves
- QA sidecars containing shared structure checks or generic finish ceremony
