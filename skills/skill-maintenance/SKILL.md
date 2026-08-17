---
name: skill-maintenance
description: "Turn skill behavior deltas, lesson hardening, or skill compaction into owner-local skill edits, eval/gotcha updates, registry sync, audit proof, and review."
tier: 3
group: operations
source: local
template_uses:
  skill-template: "0.2.0"
  skill-eval-task: "0.2.0"
  skill-qa-checklist: "0.1.0"
eval: evals/evals.json
qa_checklist: qa_checklist.md
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
state: reads(owner package, registry, evidence, lessons/troubles?);
       writes(owner package?, registry?, audit?, processed state?)
modes: harden_skill | refine_skill | upgrade_skill_from_sources |
  structure_update | metadata_update | qa_checklist_design | eval_to_qa_sync |
  low_value_prose_scan | audit | bulk_rollout | registry_validation |
  installed_copy_import
gates: delta_named; owner_clear; source_preserved; first_load_executable;
  skill_file_at_most_200_lines; standard_check_named;
  validation_passes_or_blocker_named; registry_synced;
  live_copy_only_after_source_acceptance; proof_and_review_routed
routes: research:source-synthesis | skill-creator | best-of-worlds | eval |
  self-improve | gap-analysis | harness-advisor | review
fails: installed-copy-only edit; oversized edited SKILL.md; hidden required
  behavior; arbitrary line-count splitting; fixture mutation outside sandbox;
  completion before validation;
  live-copy proof before source acceptance; bulk edit without prototype;
  material change without proof
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind `edited_skill`, `expected_behavior`, `current_behavior`, `mode`,
  and `evidence`; compute `behavior_delta := expected - current`.
- [ ] 2. Read the minimum authoritative context.
   - [ ] Always read target `SKILL.md`, registry row, relevant system docs or
     ticket, and `qa_checklist.md` for structure, refinement, or audit work.
   - [ ] Read target QA/evals when changing runtime guardrails or evals; read
     lessons, troubles, and processed state for `harden_skill`.
   - [ ] Load [maintenance modes](references/maintenance-modes.md) for mode-
     specific inputs, branches, automation presets, and handoff shapes.
   - [ ] Before mutating fixtures or proving a broad rollout, copy the target to
     a temporary sandbox or isolated checkout; never use the real skill tree as
     the experiment surface.
   - [ ] For installed-copy import, preview with
     `python3 scripts/import_installed_skills.py --skills <name> --dry-run`.
- [ ] 3. Confirm the owner surface.
   - [ ] First-load behavior → `SKILL.md`; conditional detail/template →
     references; repeatable behavior proof → evals; runtime prevention → QA or
     validator; generated metadata → its generator, never hand-edited output.
   - [ ] When frontmatter changes, validate description shape and every claimed
     template version against the actual file structure. Report missing QA
     checklists and missing or stale template-version findings explicitly.
   - [ ] Use `gap-analysis`, `harness-advisor`, or planning when the delta or
     owner remains unclear; prototype a representative sample before rollout.
- [ ] 4. Apply the smallest owner-local behavior delta.
   - [ ] `harden_skill`: add the smallest immediate eval, gate, gotcha, QA
     guardrail, or ticket that prevents recurrence.
   - [ ] `refine_skill`: consolidate duplicates and low-value prose while
     preserving evidence, required sections, routing, gates, and proof.
   - [ ] Keep every-invocation rules in `SKILL.md`; move only conditional
     branches, long examples, templates, rubrics, and rare recipes behind
     precise load conditions.
   - [ ] Reject skill-local `todos.md`; todo truth lives in the marker-delimited
     `## Todo List` in `SKILL.md`.
   - [ ] Keep every edited `SKILL.md` at or below 200 physical lines; treat
     PostToolUse feedback as the immediate repair loop and pre-commit as the
     hard backstop.
- [ ] 5. Improve structure only where ownership evidence supports it.
   - [ ] Split authored text by branch, provider, responsibility, or artifact
     type only when that reduces real first-load or maintenance cost.
   - [ ] Meet the envelope without moving default-path behavior out of first load.
   - [ ] Re-run links, imports, tests, and generators affected by a split.
- [ ] 6. Sync behavior proof and runtime guardrails.
   - [ ] If eval assertions changed, promote only reusable runtime prevention
     into QA, `SKILL.md`, a reference, or a validator; keep rare benchmark
     points in evals with an audit note.
   - [ ] For behavior-affecting maintenance, capture the current baseline, apply
     the bounded change, and run the same suite through
     [eval](../eval/SKILL.md) for candidate/baseline comparison before
     promotion. Mechanical-only changes may skip execution only with an exact
     `eval_skip_reason` and a deterministic replacement check.
   - [ ] Use `self-improve` only for measured variant search with a metric and
     promotion rule; it calls `eval` rather than owning another runner.
- [ ] 7. Validate the skill system.
   - [ ] Run `python3 scripts/check_skills.py --write` plus focused JSON, link,
     config, fixture, and eval checks.
   - [ ] Keep fixture validation rooted in its sandbox; regenerate the sandbox
     `docs/skills/registry.jsonl` rather than hand-editing it, and name every
     remaining blocker.
   - [ ] Apply `qa_checklist.md` to changed skill files and record
     kept/moved/deleted content, ownership changes, extra sections, and verdict.
   - [ ] Reinstall and inspect live copies only when installed behavior is part
     of the claim.
- [ ] 8. Finish with audit, review, and writeback.
   - [ ] Write a dated skill-local audit for material changes; otherwise record
     a mechanical/validation-only skip reason and remaining risk.
   - [ ] Use binary evidence and route material meta, cross-skill, prompt, eval,
     or precedent-setting changes through the native reviewer.
   - [ ] Update ticket/progress evidence before claiming completion.
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
- Do not treat a shorter skill as better without behavior-preservation proof.
- Do not hand-edit generated registries or graphs, bulk-edit without sample
  proof, auto-promote every eval point, or skip material audit/review.
- Do not convert checklist items into scalar metrics; project measurement
  belongs with `metric-advisor`, while skill repair needs reasons and evidence.

## Reference Map

- [skill system](../../docs/skills/system.md) — metadata, tiers, templates,
  registry, and todo contracts; read for structural changes.
- [skill best practices](../../docs/skills/best-practices.md) — first-load
  placement, examples, repeatability, and review.
- [structure QA](qa_checklist.md) — preflight and final structure checks.
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
