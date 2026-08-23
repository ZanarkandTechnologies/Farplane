---
name: skill-maintenance
description: "Turn skill behavior deltas, lesson hardening, or skill compaction into owner-local skill edits, eval/gotcha updates, registry sync, audit proof, and review."
tier: 3
group: operations
source: local
template_uses:
  skill-template: "0.5.0"
  skill-eval-task: "0.2.0"
skill_ui: skills/skill-maintenance/graph/index.html
---

# Skill Maintenance

## Context

Use this skill to update, audit, repair, harden, refine, consolidate, or roll
out Farplane skill changes after the owner surface is known. It owns package
mechanics: `SKILL.md` shape, references, eval/checklist sync, source ownership,
metadata, registry sync, audits, installed-copy checks, and review routing.

Every edited `skills/**/SKILL.md` has a hard envelope of 200 physical lines.
Within that envelope, use responsibility, first-load cost, duplication, and
observed maintenance pain to decide what should split. Use
`consolidate(target = edited_skill, structure = skill)` when compaction needs
judgment rather than mechanical extraction.

## Skill Signature

```text
skill_maintenance(expected_behavior, current_behavior, edited_skill, mode?, evidence?)
  -> updated_skill | audit_record | blocked_report
reads: owner package, registry, evidence, and applicable lessons or troubles
does: applies the smallest owner-local skill behavior or structure change
writes: owner package, generated registry data, and audit evidence when needed
returns: updated skill or audit, validation evidence, and review result or blocker
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] **N1 — Bind one observable skill behavior delta.**
  `expected + current + evidence -> behavior_delta + mode | insufficient basis`

  Rule: Maintain only from an observable gap, lesson, or compaction target.

  Assert:
  - Expected and current behavior are separately evidenced.
- [ ] **N2 — Load the minimum authoritative package state.**
  `behavior_delta -> source + registry + proof context | missing owner context`

  Rule: Load only sources consumed by the selected maintenance mode; isolate
  broad experiments from the real skill tree.

  Assert:
  - The selected mode and its required sources are explicit.
- [ ] **N3 — Resolve one primary owner surface.**
  `behavior_delta + package state -> owner file set | planning branch`

  Rule: Default behavior belongs in `SKILL.md`, conditional depth in references,
  repeated proof in evals, runtime prevention in QA or validators, and generated
  metadata in its generator.

  Assert:
  - Each planned edit has one primary owner.
- [ ] **N4 — Apply the smallest owner-local repair.**
  `owner file set + behavior_delta -> changed package | no-change verdict`

  Rule: Harden with the smallest recurrence guard; refine only after classifying
  candidates `keep | rewrite | move | delete` and preserving behavior.

  Assert:
  - Default-path behavior remains in first load.
- [ ] **N5 — Upgrade workflow nodes where the edge is visible.**
  `changed Todo path -> Golden Workflow Nodes + advantage rating | generic path`

  Rule: Each node is one n8n-sized operation; proven advantage requires
  candidate/no-skill evidence, not domain nouns or reviewer intuition.

  Assert:
  - Important domain paths contain a differentiated signal-to-decision move.
- [ ] **N6 — Reconcile behavior proof and QA ownership.**
  `changed behavior + existing guards -> eval/golden/QA migration receipt`

  Rule: Reject QA sidecars; retain normal guardrails only in Todo List Rule/Assert blocks,
  skill-specific runtime, safety, or preflight guards.

  Assert:
  - Unique prevention rules survive migration.
  - Behavior changes have comparison proof or a named blocker.
- [ ] **N7 — Synchronize and validate the skill system.**
  `changed package -> registry-consistent evidence | repair`

  Rule: Regenerate registries and run focused JSON, link, config, fixture, and
  eval checks; when an eval changes, run `farplane lint evals --changed` before
  behavior proof. Never hand-edit generated state.

  Assert:
  - Template versions match actual structure.
- [ ] **N8 — Close with independent contract review.**
  `validated package -> reviewed maintenance receipt | revision`

  Rule: Material meta, prompt, eval, or precedent-setting changes require a
  dated audit and native reviewer verdict.

  Assert:
  - Ticket/progress evidence is updated before completion.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

Use [skill audit](templates/skill-audit.md) for material changes. Load
[maintenance modes](references/maintenance-modes.md) for hardening, refinement,
source upgrades, automation presets, and review handoff templates.

## Gotchas

- Repo source is canonical; do not patch installed `~/.codex/skills/*` as the
  durable owner unless the operator explicitly requests that exact edit.
- Reinstall or inspect the live installed copy only after repo-source edits are
  accepted; never use live-copy success as a substitute for source proof.
- Do not meet the cap by hiding first-load routing, gates, proof, or outputs.
- Keep `Skill Signature` as compact input/work/output type linting. Remove its
  state-machine catalog rather than deleting the callable contract.
- Do not treat a shorter skill as better without behavior-preservation proof.
- Do not hand-edit generated registries or graphs, bulk-edit without sample
  proof, auto-promote every eval point, or skip material audit/review.
- An eval or line-count comparison does not replace skill-system validation.
  After structural edits, run `python3 scripts/check_skills.py --write` and
  report its result.
- Do not convert checklist items into scalar metrics; project measurement
  belongs with `metric-advisor`, while skill repair needs reasons and evidence.

## Reference Map

- [skill system](../../docs/skills/system.md) — metadata, tiers, templates,
  registry, and todo contracts; read for structural changes.
- [skill best practices](../../docs/skills/best-practices.md) — first-load
  placement, examples, repeatability, and review.
- [skill-contract rubric](../../docs/review/rubrics/skill-contract.md) —
  centralized structure, Golden Node, edge, calibration, and proof review.
- [maintenance modes](references/maintenance-modes.md) — load after choosing a
  mode for detailed branches and handoff shapes.
- [low-value prose scan](references/low-value-prose-scan.md) — load for
  compaction or bloated first-load prose.
- [source upgrade](references/upgrade-skill-from-sources.md) — load for bounded
  external-source upgrades.
- [eval fixture sandbox](references/eval-fixture-sandbox.md) — load before eval
  or fixture work that must not mutate the real skill tree.
- [check skills](scripts/check_skills.py) — standard registry, template, todo,
  capability, config, eval-query, and doc-reference checks.

## Output

Return owner-local changes, structure results, registry/validation proof, audit
or skip reason, eval comparison receipt or `eval_skip_reason`, and reviewer
verdict or blocker.
