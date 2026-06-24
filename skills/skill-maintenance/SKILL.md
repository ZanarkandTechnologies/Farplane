---
name: skill-maintenance
description: "Turn skill behavior deltas, lesson hardening, or skill compaction into owner-local skill edits, eval/gotcha updates, registry sync, audit proof, and review."
tier: 3
group: skills
source: local
template_uses:
  skill-template: "0.2.0"
  skill-eval-task: "0.1.0"
  skill-qa-checklist: "0.1.0"
eval: eval_task.json
qa_checklist: qa_checklist.md
skill_ui: skills/skill-maintenance/graph/index.html

---

# Skill Maintenance

## Context

Use this as the entrypoint whenever the operator wants to update, audit,
repair, harden, refine, consolidate, or roll out changes to Farplane skills.
Treat the task as a behavior delta over one or more `edited_skill` packages,
then update the owner-local skill surface and prove the skill system still
holds together.

`skill-maintenance` owns skill-package mechanics after the owner surface is
known: `SKILL.md` shape, references, eval/checklist sync, source ownership,
frontmatter, registry sync, audit records, reinstall checks, and review
routing. It also owns the weekly skill upkeep interface:

```text
harden_skill = turn fresh lessons/troubles into evals, gotchas, and blockers now
refine_skill = consolidate older evals/gotchas and shorten the skill later
```

It does not replace `optimize-harness`, `gap-analysis`, `skill-creator`,
`eval`, `self-improve`, or `review`. Use `self-improve` only for measured
variant/search loops with a program, metric, progress, and promotion rule.

## Automation Presets

`skill-maintenance.harden_skill @7d -> reports.skill_hardening`

Turns fresh lesson/trouble rows into immediate evals, gotchas, checklist
guardrails, or tickets. The automation manifest supplies cadence, report paths,
freshness, and gates; this skill owns dedupe, source ownership, eval handoff,
audit/proof, registry sync, and blocker reporting.

`skill-maintenance.refine_skill @7d -> reports.skill_refinement`

Compacts older accumulated evals/gotchas only after hardening exists. This skill
owns behavior-preserving consolidation, reference moves, audit evidence, and
review routing.

`skill-maintenance.registry_drift @7d -> reports.registry_drift`

Checks skill/source/feature registries against the current repo state. This
skill owns registry validation, generated-file sync, ambiguous-gap reporting,
and follow-up ticket suggestions.

Eval surface: `eval_task.json`, `qa_checklist.md`, fixture skill repos under
`tests/fixtures/`, and `scripts/check_skills.py --write`.

## Skill Signature

```text
skill_maintenance(expected_behavior, current_behavior, edited_skill, mode?, evidence?)
  -> updated_skill | audit_record | blocked_report

state:
  reads(edited_skill.SKILL.md, edited_skill.references?, edited_skill.eval_task?,
        edited_skill.qa_checklist?, docs/skills/registry.jsonl, prior_audits?,
        run_artifacts?, reviewer_receipts?)
  writes(edited_skill.SKILL.md?, edited_skill.references?, edited_skill.eval_task?,
         edited_skill.qa_checklist?, skill-local audit?, docs/skills/registry.jsonl)

modes:
  harden_skill | refine_skill |
  structure_update | metadata_update | qa_checklist_design |
  eval_to_qa_sync | audit | bulk_rollout | registry_validation |
  installed_copy_import

gates:
  behavior_delta_named; owner_surface_clear; source_owner_preserved;
  first_load_executable; template_version_truthful; registry_synced;
  eval_guardrails_synced_or_skipped; audit_or_skip_recorded;
  check_skills_passed; reviewer_routed_when_material

routes:
  skill-creator | eval | self-improve | advise | deliberative-advice |
  review | gap-analysis | harness-advisor

fails:
  vague update; hidden installed-copy edit; bulk edit without prototype;
  eval changed without QA-sync check; bloated first-load contract;
  template version claim without structure proof; audit skipped for material change;
  treats hardening as optional cleanup after a known repeated failure;
  uses self-improve when immediate eval/gotcha hardening is enough
```

## Upkeep Modes

```text
harden_skill(edited_skill, lessons?, troubles?, usage_evidence?, cap?)
  -> eval_candidates + gotchas + regression_cases + improvement_tickets
   + processed_state_delta?

refine_skill(edited_skill, evals?, gotchas?, usage_results?, target_size?)
  -> consolidated_evals + consolidated_gotchas + skill_delta
   + deleted_or_moved_detail + review_notes
```

Use `harden_skill` for fresh prevention: take new `docs/LESSONS.md` and
`docs/TROUBLES.md` rows, dedupe them, and add the smallest durable blockers
against recurrence: eval cases, gotchas, QA/checklist guardrails, or tickets.
Legacy `learning-drain` automations should migrate to this mode; the
`learning-drain` skill remains a compatibility wrapper around this intake.

Use `refine_skill` for compaction after hardening has accumulated material:
merge duplicate evals, collapse overlapping gotchas, move long examples into
references, shorten first-load text, and preserve behavior with eval/review
proof.

Use `self-improve` only when `harden_skill` or `refine_skill` finds a measured
search problem: multiple candidate variants, a metric, an experiment program,
or a Goal/autoresearch loop.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind variables before editing.
  - [ ] `edited_skill := target skill package(s)`.
  - [ ] `expected_behavior := desired operator-visible behavior`.
  - [ ] `current_behavior := observed or file-backed current behavior`.
  - [ ] `mode := harden_skill | refine_skill | structure_update |
    metadata_update | qa_checklist_design | eval_to_qa_sync | audit |
    bulk_rollout | registry_validation | installed_copy_import`.
  - [ ] `evidence := user request + target files + ticket/council/eval/review artifacts`.
- [ ] 2. Read the minimum authoritative context.
  - [ ] Always read `edited_skill/SKILL.md`, `docs/skills/registry.jsonl`, and
    the relevant anchored skill-system docs or active ticket.
  - [ ] If `mode in [structure_update, refine_skill, audit]`, read
    [Skill Structure QA Checklist](qa_checklist.md).
  - [ ] If `mode == qa_checklist_design`, read target `SKILL.md`, existing
    target `qa_checklist.md` when present, `eval_task.json` when present,
    `## Gotchas`, recent audits, and [Skill Structure QA Checklist](qa_checklist.md).
  - [ ] If `mode == eval_to_qa_sync` or `edited_skill/eval_task.json` changed,
    read `edited_skill/eval_task.json` and `edited_skill/qa_checklist.md` when
    it exists.
  - [ ] If `mode == harden_skill`, read the relevant `docs/TROUBLES.md`,
    `docs/LESSONS.md`, processed-state refs, and target `eval_task.json`.
  - [ ] If `mode == refine_skill`, read target `SKILL.md`, references,
    `eval_task.json`, `qa_checklist.md`, skill-local audits, and recent usage
    or eval results.
  - [ ] If `mode == installed_copy_import`, preview the import path with
    `python3 scripts/import_installed_skills.py --skills <name> --dry-run`
    from this skill package before any overwrite.
- [ ] 3. Compute `behavior_delta := expected_behavior - current_behavior`.
  - [ ] If the delta is vague, first use `gap-analysis`, `harness-advisor`, or
    `advise`; do not patch a skill until the owner surface is clear.
  - [ ] If the delta is broad or repeated across many skills, prototype on a
    representative sample before bulk rollout.
- [ ] 4. Choose the owner surface with explicit branch routing.
  - [ ] `if first_load_behavior_changed: edit edited_skill/SKILL.md`.
  - [ ] `else if conditional_detail_or_template_changed: edit edited_skill/references/*`.
  - [ ] `else if repeatable_behavior_proof_changed: edit edited_skill/eval_task.json`.
  - [ ] `else if runtime_guardrail_changed: edit edited_skill/qa_checklist.md, a reference, or a validator candidate`.
  - [ ] `if registry_or_frontmatter_changed: regenerate docs/skills/registry.jsonl; never hand-edit generated rows`.
  - [ ] `if template_version_changed: prove the actual headings/todo/signature match the promised template`.
  - [ ] `if installed_copy_differs: import or patch repo source first; reinstall/live-inspect only after source edits are accepted`.
  - [ ] `if bulk_rollout: use sandbox/sample proof before scaling and keep one audit/proof row per affected class`.
- [ ] 5. Apply the smallest owner-local edit.
  - [ ] `if mode == harden_skill: add or propose the smallest immediate evals,
    gotchas, checklist guardrails, or improvement tickets that block repeated
    failures before optimizing prose length`.
  - [ ] `if mode == refine_skill: consolidate duplicate evals/gotchas and
    shorten first-load text only after preserving the behavioral guardrails`.
  - [ ] `if mode == qa_checklist_design: create or update
    edited_skill/qa_checklist.md as a preflight plus final-review contract;
    add only a compact first-load pointer in SKILL.md unless a gotcha must be
    known before execution`.
  - [ ] Keep every-invocation gates, routing, proof, stop conditions, and output
    contract in `SKILL.md`.
  - [ ] Fold operational gotchas into todos, gates, fails, or concise stop
    conditions before adding or preserving a standalone gotcha catalog.
  - [ ] Move long examples, rare recipes, templates, detailed rubrics, and
    conditional branches to references only when the todo names when to load them.
  - [ ] If a reference is a reusable subskill or method workflow, require
    `template_uses.skill-method-reference` and validate it against
    [docs/skills/templates/METHOD_REFERENCE_TEMPLATE.md](../../docs/skills/templates/METHOD_REFERENCE_TEMPLATE.md).
  - [ ] Move or delete rationale, history, philosophy, tutorial prose, duplicated
    workflow explanation, and template inventories unless they satisfy the
    `qa_checklist.md` First-Load Required Set.
  - [ ] Convert long intake question lists into function signatures, parameter
    lists, or schemas when normal agent behavior can ask for missing params.
  - [ ] Compare top-level sections against the current skill template; fold,
    move, or delete extra sections unless they add substantial unique first-load
    value that core sections cannot preserve.
  - [ ] Reject skill-local `todos.md`; first-load todo truth lives only in the
    marker-delimited `## Todo List` inside `SKILL.md`.
- [ ] 6. Sync eval reference points into runtime guardrails when warranted.
  - [ ] `if edited_skill/eval_task.json changed: compare changed reference_points against edited_skill/qa_checklist.md when present, otherwise decide whether to create one`.
  - [ ] `if reference_point is reusable_runtime_guardrail: promote it into checklist, QA wording, validator candidate, or SKILL.md hard gate`.
  - [ ] `else: record skipped rare, hardcase, benchmark-only, or judgment-heavy points in the audit`.
  - [ ] For `harden_skill`, call [eval](../eval/SKILL.md) when the lesson or
    trouble can become a runnable regression case.
  - [ ] For `refine_skill`, call [eval](../eval/SKILL.md) when consolidation
    might weaken coverage, and call [self-improve](../self-improve/SKILL.md)
    only for measured search over variants.
- [ ] 7. Validate and prove the skill-system state.
  - [ ] Run `python3 scripts/check_skills.py --write` from this skill package.
  - [ ] Run focused JSON, link, template-version, fixture, eval, or import
    checks required by `mode` and the active ticket.
  - [ ] If `SKILL.md` changed, run `qa_checklist.md` against the changed skill and
    record `line_count_before`, `line_count_after`, `kept_in_skill`,
    `moved_to_reference`, `deleted_as_duplicate_or_rationale`,
    `extra_sections_kept_with_reason`, and verdict.
  - [ ] If `qa_checklist.md` changed, verify it has prevention value before
    execution and final-review value after execution; do not keep checklist
    items that only restate the todo list or duplicate `## Gotchas`.
  - [ ] Reinstall touched local skills and inspect the live copy only when the
    user is judging installed behavior.
- [ ] 8. Finish with audit/review/writeback.
  - [ ] For material skill changes, write or update
    `skills/<skill-name>/audits/YYYY-MM-DD-<short-change>.md` from
    [skill-audit.md](templates/skill-audit.md); otherwise record a skip reason.
  - [ ] Use binary `pass | fail | unknown` evidence; do not invent numeric
    health scores or claim task/review improvement without run artifacts.
  - [ ] Route final review through `reviewer` for Tier 1, meta, `eval`, stale,
    high-blast-radius, cross-skill, or precedent-setting changes.
  - [ ] For material `qa_checklist.md` changes, hand reviewer both
    `edited_skill/SKILL.md` and `edited_skill/qa_checklist.md`; reviewer should
    independently apply the target checklist and this skill's structure checklist.
  - [ ] Update ticket/progress evidence before claiming completion.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

Behavior-delta handoff:

```text
edited_skill:
expected_behavior:
current_behavior:
mode:
behavior_delta:
owner_surface:
proof_required:
```

Hardening handoff:

```text
mode: harden_skill
edited_skill:
source_rows:
  - docs/TROUBLES.md:
  - docs/LESSONS.md:
immediate_blockers:
  eval_candidates:
  gotchas:
  checklist_guardrails:
  tickets:
processed_state:
proof_required:
```

Refinement handoff:

```text
mode: refine_skill
edited_skill:
inputs:
  evals:
  gotchas:
  usage_results:
compaction_plan:
  keep:
  merge:
  move_to_references:
  delete_as_duplicate:
proof_required:
```

Audit skip reason:

```text
audit_skipped:
  reason: tiny mechanical edit | no behavior delta | validation-only
  evidence:
  remaining_risk:
```

Review handoff:

```text
Review changed skill files for skill-contract, integration-readiness, and
evidence-quality. Check source ownership, first-load sufficiency, registry sync,
template-version truth, eval-to-QA sync, audit evidence, and reviewer routing.
Return TAS verdicts, blockers, and smallest required fixes.
```

## Gotchas

- Do not treat installed `~/.codex/skills/*` files as the durable source of
  truth unless the operator explicitly asks for that exact installed-copy edit.
- Do not mark a skill as onboarded or versioned unless its actual structure
  matches the template promise.
- Do not use brevity as proof. A shorter `SKILL.md` is worse if it hides
  required routing, gates, proof, or output contract.
- Do not let `skill-maintenance` become a second `optimize-harness`; this skill
  changes skill packages after the owner surface is known.
- Do not use `refine_skill` to delay urgent hardening. Fresh repeated failures
  get evals/gotchas first; compaction can happen in the later weekly pass.
- Do not use `self-improve` for every skill update. It is for measured search
  or variants, not ordinary lesson/trouble hardening.
- Do not auto-promote every eval reference point into a checklist. Promote only
  reusable runtime guardrails.
- Do not bypass `check_skills.py --write`, hand-edit generated registry rows,
  bulk-edit without sample proof, or skip audit/review for material changes.

## Reference Map

- [docs/skills/system.md](../../docs/skills/system.md) - tier model, source
  ownership, frontmatter contract, template versioning, feature tracking, and
  todo-link rules.
- [docs/skills/README.md](../../docs/skills/README.md) - human skill selection
  guide, generated registry surface, and maintenance commands.
- [docs/skills/best-practices.md](../../docs/skills/best-practices.md) -
  first-load shape, structure optimization metrics, reference placement,
  repeatability, advice/proof routing, and finish gates.
- [qa_checklist.md](qa_checklist.md) - first-class skill-local QA checklist for
  material skill structure changes, first-load size, progressive disclosure,
  reference routing, or compaction-risk review.
- [docs/skills/templates/SKILL_TEMPLATE.md](../../docs/skills/templates/SKILL_TEMPLATE.md)
  - current baseline skill template.
- [../eval/SKILL.md](../eval/SKILL.md) - create or consolidate runnable
  regression proof when hardening or refinement touches behavior.
- [../self-improve/SKILL.md](../self-improve/SKILL.md) - use only for measured
  variant/search loops, not default weekly hardening.
- [templates/skill-audit.md](templates/skill-audit.md) - binary before/after
  audit record template for material skill changes.
- [references/eval-fixture-sandbox.md](references/eval-fixture-sandbox.md) -
  load when writing or running evals/fixtures that must not mutate the real
  skill tree.
- [scripts/check_skills.py](scripts/check_skills.py) - standard validation,
  registry sync, todo checks, doc refs, and template-version report.

## Output

- Updated owner-local skill files: `SKILL.md`, references, evals, or checklist
  surfaces as selected by `behavior_delta`.
- Hardening outputs when `mode == harden_skill`: eval candidates, gotchas,
  regression cases, improvement tickets, and processed-state notes.
- Refinement outputs when `mode == refine_skill`: consolidated evals/gotchas,
  shortened skill text, moved reference detail, and review notes.
- Regenerated `docs/skills/registry.jsonl` when metadata or skill shape changes.
- Skill-local audit record for material changes, or explicit audit skip reason.
- Validation output from `python3 scripts/check_skills.py --write` plus any
  focused fixture/eval/template checks required by the active mode.
- Reviewer result or recorded blocker when the change is material.
