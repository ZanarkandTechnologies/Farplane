---
title: TASK-0197 Proof Notes
ticket_id: TASK-0197
status: complete
created_at: 2026-06-13
---

# TASK-0197 Proof Notes

## Mechanical Checks

| Check | Result | Evidence |
| --- | --- | --- |
| `python3 skills/skill-maintenance/scripts/check_skills.py --write` | pass | Rerun 2026-06-13 17:54 +0800. Todo sections, registry check, tier check, Tier 0 protocol, capability fixtures, doc refs, and py_compile all passed; registry regenerated with 86 skill rows. |
| `python3 skills/skill-maintenance/scripts/check_skills.py --template-version 0.2.0` | blocked by unrelated global errors | Rerun 2026-06-13 17:54 +0800. `skill-maintenance` is not listed in template structure errors. The command fails on unrelated skills: `code-review`, `goal-advisor`, `learning-drain`, and `plan`. |
| `python3 -m json.tool skills/skill-maintenance/eval_task.json` | pass | Rerun 2026-06-13 17:54 +0800; JSON parsed successfully. |
| `git diff --check` | pass | Rerun 2026-06-13 17:54 +0800; no whitespace errors. |

## Existing Eval Case Review

| Eval case | Required behavior | Rewritten skill evidence |
| --- | --- | --- |
| `skill_maintenance_signature_rollout_01` | Use sandbox/isolated checkout, identify broad migration, prototype before bulk rollout, check template structure, validate registry, record audit/proof. | Todo steps 2-4 explicitly read structure checklist, handle broad deltas with representative sample proof, branch on `template_version_changed`, regenerate registry, and keep audit/proof rows. |
| `skill_maintenance_registry_sync_01` | Keep fixture repair in sandbox, run standard validation, regenerate registry rather than hand-edit, check frontmatter/template promises, report blockers honestly. | Todo steps 4 and 7 explicitly regenerate `docs/skills/registry.jsonl`, never hand-edit generated rows, prove template version changes, run `check_skills.py --write`, and report blockers. |
| `skill_maintenance_source_owner_01` | Reject installed copies as durable source of truth, route to repo source/import preview, reinstall only after accepted source edits, use fixture/sandbox. | Signature fails hidden installed-copy edits; Todo step 2 has dry-run import preview; Todo step 4 handles `installed_copy_differs`; Gotchas reject live installed copies as durable source. |

## Sandbox Fixture Dry-Run

Command shape:

```bash
tmp=$(mktemp -d)
cp -R skills/skill-maintenance/tests/fixtures/bad-skill-repo "$tmp/bad-skill-repo"
find "$tmp/bad-skill-repo" -maxdepth 3 -type f | sort
rg -n "sandbox|source|installed|template|registry|audit|bulk|prototype|dry-run|overwrite|check_skills" \
  skills/skill-maintenance/SKILL.md \
  skills/skill-maintenance/eval_task.json \
  skills/skill-maintenance/tests/fixtures/bad-skill-repo
```

Result, rerun 2026-06-13 17:54 +0800:

- The fixture was copied to a temp sandbox path:
  `/var/folders/98/ht394qw529jbzxvzl7ldp1040000gn/T/tmp.b7b7ljqXtQ/bad-skill-repo`.
- `bad-signature-rollout` and `installed-copy-only` fixture files were present
  in the sandbox copy.
- Search evidence showed the rewritten skill explicitly carries the sandbox,
  bulk prototype, template-version, registry, audit, source-owner,
  installed-copy, dry-run import, overwrite, and `check_skills` branches needed
  by the eval cases.
- No real fixture files or installed skill files were mutated.

## Structure Checklist Self-Check

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` contains trigger context, one signature, mode list, gates, branch routing, validation, audit/review, gotchas, references, and output. |
| `reference_load_precision` | pass | Every reference in the Reference Map names its load/use condition. Todo step 2 names when to load structure checklist, eval/checklist surfaces, and import preview. |
| `missing_context_rate` | pass | Required gates for source ownership, prototype-before-bulk, template truth, registry sync, eval-to-QA sync, validation, audit, reinstall, and reviewer routing remain in first load. |
| `noisy_context_rate` | pass | Detailed rationale and council analysis remain in the ticket/council artifacts; first load is 201 lines and branch-oriented. |
| `duplicated_instruction_count` | pass | The second signature was collapsed into `audit` mode; eval-to-QA sync is a branch, not a duplicated standalone policy body. |
| `prompt_size_tokens` | pass | `skills/skill-maintenance/SKILL.md` is 201 lines, below the roughly 250-line review threshold. |
| `maintenance_locality` | pass | Future edits have one owner-local path: decide `behavior_delta`, choose owner surface, edit `edited_skill`, validate, audit. |
| `composition_clarity` | pass | Signature exposes inputs, outputs, state reads/writes, modes, gates, routes, and failure modes. |

## Reviewer And Drift

| Requirement | Status | Evidence |
| --- | --- | --- |
| Goal drift review | pass with reviewer gate dependency | `goal-drift-reviewer` returned aligned on the target rewrite and proof, with completion blocked only until reviewer TAS-A pass and scoped template-version disposition. |
| Reviewer pass for `skill-contract`, `integration-readiness`, `evidence-quality` | pass | `reviewer` returned overall `TAS-A`, with `skill-contract: TAS-A`, `integration-readiness: TAS-A`, `evidence-quality: TAS-A`, no blocking findings, and no rerun required. |

## Evidence Gaps / Disposition

- The global template-version command currently fails because unrelated skills
  with `skill_template_version: 0.2.0` are missing template headings. This
  ticket does not broaden into those skills. `reviewer` accepted this as an
  allowed scoped exception because the failures are on `code-review`,
  `goal-advisor`, `learning-drain`, and `plan`, not `skill-maintenance`.
- Optional follow-up: create a separate cleanup ticket for unrelated global
  `--template-version 0.2.0` failures if template cleanliness becomes a release
  gate.
