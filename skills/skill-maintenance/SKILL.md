---
name: skill-maintenance
description: "Turn a desired skill behavior delta into owner-local skill edits, registry sync, audit proof, and review when updating Farplane skills."
tier: 3
group: skills
source: local
skill_template_version: "0.2.0"
feature_refs:
  - FEAT-0037
  - FEAT-0040
  - FEAT-0044
  - FEAT-0057
---

# Skill Maintenance

## Context

Use this as the entrypoint whenever the operator wants to update, audit,
repair, consolidate, or roll out changes to Farplane skills. Treat the task as
a behavior delta over one or more `edited_skill` packages, then update the
owner-local skill surface and prove the skill system still holds together.

`skill-maintenance` owns skill-package mechanics after the owner surface is
known: `SKILL.md` shape, references, eval/checklist sync, source ownership,
frontmatter, registry sync, audit records, reinstall checks, and review routing.
It does not replace `optimize-harness`, `gap-analysis`, `skill-creator`, `eval`,
or `review`.

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
  structure_update | metadata_update | eval_to_qa_sync | audit |
  bulk_rollout | registry_validation | installed_copy_import

gates:
  behavior_delta_named; owner_surface_clear; source_owner_preserved;
  first_load_executable; template_version_truthful; registry_synced;
  eval_guardrails_synced_or_skipped; audit_or_skip_recorded;
  check_skills_passed; reviewer_routed_when_material

routes:
  skill-creator | eval | advise | deliberative-advice | review |
  gap-analysis | harness-advisor

fails:
  vague update; hidden installed-copy edit; bulk edit without prototype;
  eval changed without QA-sync check; bloated first-load contract;
  template version claim without structure proof; audit skipped for material change
```

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind variables before editing.
  - [ ] `edited_skill := target skill package(s)`.
  - [ ] `expected_behavior := desired operator-visible behavior`.
  - [ ] `current_behavior := observed or file-backed current behavior`.
  - [ ] `mode := structure_update | metadata_update | eval_to_qa_sync | audit | bulk_rollout | registry_validation | installed_copy_import`.
  - [ ] `evidence := user request + target files + ticket/council/eval/review artifacts`.
- [ ] 2. Read the minimum authoritative context.
  - [ ] Always read `edited_skill/SKILL.md`, `docs/skills/registry.jsonl`, and
    the relevant anchored skill-system docs or active ticket.
  - [ ] If `mode in [structure_update, audit]`, read
    [Skill Structure QA Checklist](qa_checklist.md).
  - [ ] If `mode == eval_to_qa_sync` or `edited_skill/eval_task.json` changed,
    read `edited_skill/eval_task.json` and `edited_skill/qa_checklist.md` when
    it exists.
  - [ ] If `mode == installed_copy_import`, preview the import path with
    `python3 ../../bin/import_installed_skills.py --skills <name> --dry-run`
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
  - [ ] Keep every-invocation gates, routing, proof, stop conditions, and output
    contract in `SKILL.md`.
  - [ ] Move long examples, rare recipes, templates, detailed rubrics, and
    conditional branches to references only when the todo names when to load them.
  - [ ] Reject skill-local `todos.md`; first-load todo truth lives only in the
    marker-delimited `## Todo List` inside `SKILL.md`.
- [ ] 6. Sync eval reference points into runtime guardrails when warranted.
  - [ ] `if edited_skill/eval_task.json changed: compare changed reference_points against edited_skill/qa_checklist.md when present, otherwise decide whether to create one`.
  - [ ] `if reference_point is reusable_runtime_guardrail: promote it into checklist, QA wording, validator candidate, or SKILL.md hard gate`.
  - [ ] `else: record skipped rare, hardcase, benchmark-only, or judgment-heavy points in the audit`.
- [ ] 7. Validate and prove the skill-system state.
  - [ ] Run `python3 scripts/check_skills.py --write` from this skill package.
  - [ ] Run focused JSON, link, template-version, fixture, eval, or import
    checks required by `mode` and the active ticket.
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
- [../skill-creator/references/SKILL_TEMPLATE.md](../skill-creator/references/SKILL_TEMPLATE.md)
  - current baseline skill template.
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
- Regenerated `docs/skills/registry.jsonl` when metadata or skill shape changes.
- Skill-local audit record for material changes, or explicit audit skip reason.
- Validation output from `python3 scripts/check_skills.py --write` plus any
  focused fixture/eval/template checks required by the active mode.
- Reviewer result or recorded blocker when the change is material.
