---
skill: media-ingest
date: 2026-07-09
change_type: structure
owner: skill-maintenance
status: pass
review_route: self_check
before_ref: skills/media-ingest/SKILL.md before template_uses.skill-template 0.3.7
after_ref: skills/media-ingest/SKILL.md with template_uses.skill-template 0.3.7
reasoning_basis: first_principles
proof_artifacts:
  - python3 skills/skill-maintenance/scripts/check_skills.py --write
  - git diff --check -- skills/media-ingest/SKILL.md
eval_required: no
---

# Media Ingest Template 0.3.7 Format Audit

## Change

- Before: `media-ingest` used the older freeform skill layout with trigger,
  workflow, output-contract, decision-branch, judgment-question, gotcha, and
  reference sections.
- After: `media-ingest` declares `template_uses.skill-template: "0.3.7"` and
  uses the current `Context`, `Skill Signature`, `Phase Contract`,
  `Phase Boundary`, numbered `Todo List`, `Templates`, `Gotchas`,
  `Reference Map`, and `Output` shape.
- Why: the operator asked to update the skill with `skill-maintenance` and use
  the latest skill format.
- Tradeoff accepted: the first-load file grew from 174 to 179 lines during this
  format pass to make state, gates, routes, fails, and bundle shape explicit.

## First-Principles Reasoning

- Objective: make media ingest executable from first load while preserving the
  recent browser-backed `yt-dlp --cookies-from-browser` behavior.
- Placement logic: every-invocation routing, proof, privacy, transcript, frame,
  and retention behavior stayed in `SKILL.md`; conditional transcription and
  music-recognition details stayed in `references/`.
- Expected behavior delta: agents should identify the ingest contract from the
  signature, follow numbered todo gates, and produce a `MediaIngestBundle`
  without relying on hidden chat context.
- Proof needed: skill registry validation, generated registry sync, structure
  checklist self-check, line budget review, and live installed-copy sync.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Signature, gates, routes, todo list, template, gotchas, references, and output are in `SKILL.md`. |
| `reference_load_precision` | pass | `transcription.md` and `music-recognition.md` have explicit load conditions. |
| `missing_context_rate` | pass | Browser `yt-dlp`, transcript status, retention, frame, and bundle requirements remain in first load. |
| `noisy_context_rate` | pass | File is 179 lines; rare setup details remain in references. |
| `duplicated_instruction_count` | pass | Old workflow/branch sections were consolidated into signature, todo list, template, and gotchas. |
| `prompt_size_tokens` | pass | `SKILL.md` is below the 250-line review threshold. |
| `task_success_rate` | unknown | No live media ingest rerun was required for this structure-only update. |
| `review_tas_rate` | unknown | Reviewer subagent was not spawned because this turn did not explicitly authorize subagents. |
| `maintenance_locality` | pass | Future format, routing, and first-load behavior belong in `SKILL.md`; conditional details belong in `references/`. |
| `composition_clarity` | pass | `media_ingest(...)` signature names inputs, outputs, state, gates, routes, and fails. |

## Proof Artifacts

- Skill-local evals, when needed: not required; behavior was preserved and no
  eval task changed.
- Structure evals, when needed: `skill-maintenance` checklist applied by
  self-check.
- Reviewer receipt: not run; subagent spawning was not explicitly authorized in
  this turn.
- Validator: `python3 skills/skill-maintenance/scripts/check_skills.py --write`
  passed.
- Eval required: no.
- Evidence gaps: no real media source was re-ingested after the structure-only
  rewrite.

## Before Behavior

- Media ingest was readable and already had browser-backed `yt-dlp` guidance,
  but it was not onboarded to `skill-template: 0.3.7`.
- Registry listed `media-ingest` without template usage and with `version:
  0.1.0`.

## After Behavior

- Media ingest is a current `skill-template: 0.3.7` consumer.
- Registry lists `skill_template_version: "0.3.7"` and
  `template_uses.skill-template: "0.3.7"` for `media-ingest`.
- The live installed `~/.codex/skills/media-ingest/SKILL.md` should be synced
  after validation when installed behavior is being judged.

## Followups

- Consider adding a focused media-ingest eval only after a stable fixture can
  prove browser-cookie fetch fallback without touching real cookies or private
  media.
