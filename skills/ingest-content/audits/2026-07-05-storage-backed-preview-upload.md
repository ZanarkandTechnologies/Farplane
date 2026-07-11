---
skill: ingest-content
date: 2026-07-05
change_type: behavior
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/ingest-content/SKILL.md
after_ref: skills/ingest-content/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - skills/ingest-content/SKILL.md
  - skills/ingest-content/references/resource-bank-contract.md
  - skills/ingest-content/qa_checklist.md
  - skills/ingest-content/eval_task.json
eval_required: yes
---

# Skill Audit

## Change

- Before: `ingest-content` saved compact Resource Bank captures and kept Tasty
  Pack output minimal, but did not tell agents to upload real contact sheets or
  representative frame images as storage-backed derived assets.
- After: The skill uploads a real thumbnail/contact sheet/frame image through
  the Farplane-UI `resource-bank:upload-thumbnail` script after the primary
  Resource Bank asset row exists, records returned `assetId`/`storageId`, and
  leaves preview upload skipped when no visual asset was extracted.
- Why: Farplane-UI now supports Convex storage-backed Resource Bank previews,
  so Farplane ingestion should enrich source tiles without re-expanding the
  active pack contract into an evidence vault.
- Tradeoff accepted: The workflow adds one optional storage-write edge, but only
  after media ingest has already produced a real visual and only after the
  primary asset row exists.

## First-Principles Reasoning

- Objective: Make real ingest-generated visuals visible in Resource Bank UI
  previews while preserving compact source/analysis/elements retrieval.
- Placement logic: `SKILL.md` owns the first-load trigger and gates;
  `references/resource-bank-contract.md` owns the exact command contract;
  `qa_checklist.md` and `eval_task.json` own regression checks.
- Expected behavior delta: Future video/social ingestions attach real extracted
  preview images as derived Resource Bank assets and do not fake missing
  thumbnails or return preview fields in Tasty Packs.
- Proof needed: Skill validation, checklist self-review, installed-copy sync,
  and a future live ingestion run that returns `previewAsset.storageUrl`.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | `SKILL.md` signature, todos, template, and gotchas now include optional derived preview upload. |
| `reference_load_precision` | pass | Full upload command lives in `references/resource-bank-contract.md`; `SKILL.md` points there through the normal Resource Bank reference route. |
| `missing_context_rate` | pass | Primary-asset-first, no-fake-preview, and pack-minimal gates are in first-load and QA surfaces. |
| `noisy_context_rate` | pass | Long command detail was kept out of the todo list except for one compact example. |
| `duplicated_instruction_count` | pass | `SKILL.md` has the operational gate; the reference has the command and verification detail. |
| `prompt_size_tokens` | pass | `SKILL.md` changed from 288 to 311 lines; added lines are gates/proof, not rationale. |
| `task_success_rate` | unknown | Requires future live ingestion run with extracted contact sheet/frame. |
| `review_tas_rate` | unknown | No independent reviewer lane was spawned in this thread. |
| `maintenance_locality` | pass | Changes stay inside `skills/ingest-content/`. |
| `composition_clarity` | pass | Media extraction remains owned by `media-ingest`/`video-understanding`; storage-backed preview upload is owned by `ingest-content`. |

## Proof Artifacts

- Skill-local evals, when needed: `skills/ingest-content/eval_task.json`
- Structure evals, when needed: `python3 skills/skill-maintenance/scripts/check_skills.py --write`
- Reviewer receipt: not run; self-check only.
- Validator: `python3 skills/skill-maintenance/scripts/check_skills.py --write`
  passed on 2026-07-05.
- Eval required: yes; regression reference points added, not executed.
- Evidence gaps: No new live Resource Bank ingestion was run in this thread, so
  `previewAsset.storageUrl` proof remains covered by the existing Farplane-UI
  manual uploads and a future Farplane ingestion run.

## Before Behavior

- A real contact sheet or selected frame from media ingest could remain only as
  a local proof artifact. Resource Bank source tiles would not be enriched by
  Farplane ingestion unless the operator manually uploaded the preview through
  Farplane-UI.

## After Behavior

- When media ingest or video understanding produces a real representative image,
  Farplane ingestion runs the Farplane-UI upload script after the primary asset
  exists and stores the result as a derived `thumbnail`/`image` asset with
  `parentAssetId`.
- When no real visual exists, the ingestion says `derived_preview:
  skipped_no_visual_asset` and leaves the source tile as-is.
- Tasty Pack and Inspiration Pack consumers still receive source, analysis, and
  creative elements rather than evidence assets or preview storage fields.

## Followups

- Run a live ingestion with a newly extracted contact sheet and verify the
  Resource Bank dashboard returns `previewAsset.storageUrl`.
