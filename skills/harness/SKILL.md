---
name: harness
description: "Use for \"make a skill\", \"fix this skill\", \"improve the harness\" or \"where should this rule live\": create, maintain, optimize or place one harness change, with proof and a validated registry."
source: local
department: operations
template_uses:
  skill-template: "0.6.9"
  skill-eval-task: "0.2.0"
skill_ui: skills/harness/graph/index.html
allowed-tools: Read, Write, Glob, Grep, Bash
---

# Harness

## Context

Use this when Farplane itself should behave differently: a new skill, a fix or
compaction of an existing skill, a measured optimization of one skill, or a
decision about where a rule belongs. One pass runs one mode on one target and
returns one receipt. It owns the skill-system check scripts under `scripts/`
(registry, checklists, profiles, install selection, graphs, template
intelligence) that install, validators, and git gates call.

It does not write eval rows or judges (`eval`), schedule jobs
(`automation-advisor`), plan product code (`impl-plan`), or issue a TAS verdict
(`review`). Repo source is canonical; never patch installed copies under
`~/.codex/skills/` or `~/.claude/skills/` unless the operator names that target.

## Skill Signature

```text
harness(request, mode?: create | maintain | optimize | place, target?, evidence?, metric?)
  -> mode_receipt { owner + change | placement + proof + validation + review_route } | blocked
reads: references/skill-system/system.md, references/skill-system/best-practices.md, skills/registry.jsonl,
  harness doctrine, the target package, its evals, tickets and evidence
does: picks the mode, applies the smallest owner-local change, proves it, syncs generated state
writes: owner-local skill files, generated registries via scripts/, ticket progress
returns: changed files, proof commands and results, reviewer verdict or blocker
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] **N1 — Bind the observed gap and pick the mode.**
  `request + evidence -> mode + target + expected vs current | blocked`

  Rule: State current and expected behavior separately; never mutate on vague
  quality, taste, or ROI language. A new stable reusable trigger with no owner
  is `create`; an existing package is `maintain`; a measurable gap needing
  several bounded rounds is `optimize`; an unclear owner surface is `place`.
  Check `skills/registry.jsonl` for an existing owner before `create`.

  Example: "the commit skill keeps forgetting to label other threads' work" ->
  `maintain` on `skills/commit`, not a new skill or a root prompt rule.

  Assert:
  - The mode, target, and both behaviors are named, or the missing input is the blocker.
- [ ] **N2 — place: choose one owner surface before editing.**
  `gap + loss term -> primary owner + rejected surfaces + proof route`

  Rule: Reject the generic "edit the prompt" instinct: do not default to root
  `AGENTS.md` or `runtimes/AGENTS.md`; prefer the smallest surface that fixes
  the failure (ticket, skill, eval, validator, QA). Hooks and validators only
  for deterministic work, never judgment. Read the harness doctrine first; load
  `docs/fundamentals/harness-algebra.md` only for high-blast-radius decisions.
  Full steps: [place](references/place.md).

  Assert:
  - One primary owner, rejected surfaces with reasons, and a proof route.
- [ ] **N3 — create: draft the smallest first skill contract.**
  `accepted owner -> SKILL.md + evals + references | reject as summary`

  Rule: A node is one n8n-sized operation with inspectable state and a domain
  decision a generic agent would miss; three to seven nodes. Keep source
  knowledge only when it changes a signal, decision, branch, output, or proof.
  Start from [the skill template](templates/SKILL_TEMPLATE.md);
  description per best practices (2-4 operator phrases, then the output).
  Full steps and the book-grounded branch: [create](references/create.md).

  Assert:
  - Every retained insight maps to a node, example, eval, guard, or validator.
- [ ] **N4 — maintain: apply the smallest owner-local repair.**
  `target package + delta -> changed package | no-change verdict`

  Rule: Default behavior stays in `SKILL.md`, conditional depth in references,
  repeated proof in evals, runtime prevention in validators or QA. Compare the
  declared template version to the canonical template and upgrade a stale
  package in the same change. Never hand-edit generated registries or graphs;
  regenerate them. Compaction classifies each unit `keep | rewrite | move |
  delete` and preserves behavior. Full steps: [maintain](references/maintain.md).

  Assert:
  - Template claims match the actual structure; first-load routing, gates, and output survive.
- [ ] **N5 — optimize: harden until the target passes, then minimize length.**
  `target + metric + frozen suite -> shortest passing candidate | blocked`

  Rule: Bind metric, passing target, guards, and separate harden/refine budgets;
  record the baseline before any edit. Freeze the suite for the whole Goal: never
  change cases mid-goal; an accepted new case means a fresh packet and baseline.
  Retain a hardening edit only when behavior improves and every guard passes;
  refine only after the full target passes, keeping only shorter candidates that
  hold the floor. `goal-advisor` compiles the packet. Full loop and report
  shape: [optimize](references/optimize.md).

  Assert:
  - No refinement before the target passes; no behavior traded for length.
- [ ] **N6 — Prove the change against no-skill or the previous version.**
  `changed owner -> eval evidence + validation | blocked`

  Rule: Behavior-sensitive changes need normal, hard, and boundary cases and a
  candidate vs no-skill (or previous-skill) comparison through `eval`; an
  inspection-only dry run never proves readiness. Run
  `python3 skills/harness/scripts/check_skills.py --write`, and
  `farplane lint evals --changed` when an eval changed.

  Assert:
  - The receipt names the comparison evidence or an `eval_skip_reason`.
- [ ] **N7 — Close with an independent verdict and the receipt.**
  `validated change -> accept | hold | rollback + review route`

  Rule: Accept only when the named loss falls, proof supports the claim, and
  guards hold; hold when composition proof is missing; roll back on regression
  or wrong placement. Material meta, prompt, eval, or precedent-setting changes
  get a `skill-contract` reviewer verdict. Update ticket progress first.

  Assert:
  - Prose alone never proves behavior changed.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Gotchas

- Every edited `skills/**/SKILL.md` stays at or below 200 physical lines; never
  meet the cap by hiding first-load routing, gates, proof, or output.
- Do not create skills for generic knowledge, one-off notes, raw library docs,
  or behavior better owned by a script, ticket, prompt, or existing skill.
- A shorter skill is not better without behavior-preservation proof.
- A generated harness map or graph is navigation, not source of truth.
- Installed-copy success never substitutes for repo-source proof; reinstall
  only after the source edit is accepted.
- Do not convert checklist items into scalar metrics; project measurement
  belongs to the `goal-advisor` metric card.

## Reference Map

- [create](references/create.md) - create mode nodes, book-to-skill branch
  ([book-to-skill](references/book-to-skill.md)), workflows, output patterns.
- [maintain](references/maintain.md) - maintain nodes; by sub-mode
  [maintenance modes](references/maintenance-modes.md),
  [low-value prose scan](references/low-value-prose-scan.md),
  [source upgrade](references/upgrade-skill-from-sources.md), [eval fixture sandbox](references/eval-fixture-sandbox.md);
  [harness maintenance](references/harness-maintenance.md) for registries, rollout, graphs and health.
- [optimize](references/optimize.md) - the Goal-backed loop, budgets, choose-next,
  writeback order, and turn report; [Goal program](references/goal-program-template.md).
- [place](references/place.md) and [placement axes](references/placement-axes.md)
  - owner-surface comparison and material placement scoring.
- [skill system](references/skill-system/system.md) and
  [best practices](references/skill-system/best-practices.md) - every structural change.
- [skill-contract rubric](../review/references/rubrics/skill-contract.md) - review gate.
- [check skills](scripts/check_skills.py) - registry, template, todo, capability,
  config, eval-query, and doc-reference checks.

## Output

```yaml
mode: create | maintain | optimize | place
observed: <current behavior + evidence>
expected: <target behavior>
primary_owner: <file or surface>; rejected: <surfaces + why>
change: <changed files> | placement only | none
proof: <eval comparison, commands and results> | eval_skip_reason
validation: check_skills --write result (+ lint evals when changed)
decision: accept | hold | rollback | blocked
review: <skill-contract verdict or route>
next: <one concrete action or owner>
```
