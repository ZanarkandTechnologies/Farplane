---
skill: audio-advisor
date: 2026-07-18
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: skills/audio-advisor/audits/2026-07-18-source-first-generation-merge.md
after_ref: skills/audio-advisor/SKILL.md
reasoning_basis: operator_correction
proof_artifacts:
  - skills/audio-advisor/evals/evals.json
  - skills/audio-advisor/qa_checklist.md
  - skills/audio-advisor/references/soundbuttonsworld.md
eval_required: yes
---

# Operator-Only SFX Retrieval

## Change

- Before: `audio-advisor` could download a permitted SoundButtonsWorld file
  after explicit authority.
- After: video planning performs candidate discovery only. The final content
  plan lists item-page links for operator download and approval; the agent never
  downloads or operates the site's search/download controls.
- Example: a “tiny receipt printer chirp” cue returns up to three item links
  marked `awaiting_operator_download_and_approval`, or `searched_no_fit` plus a
  generation fallback.

## Placement And Proof

- `audio-advisor/SKILL.md`: every-invocation discovery and no-download rule.
- `references/soundbuttonsworld.md`: public-index search method and shortlist
  schema.
- `content-impl-plan`: final-plan handoff and QA requirement.
- `validate_audio_packet.py`: returned source receipts require
  `retrieved_by: operator`.
- Evals: paid-ad and ordinary-SFX cases now require links-only behavior.

## Structure Accounting

- `audio-advisor/SKILL.md`: 221 -> 200 lines.
- `content-impl-plan/SKILL.md`: 220 -> 200 lines.
- Kept first-load: search trigger, shortlist fields, operator handoff,
  no-download gate, generation fallback, provider safety, and Remotion route.
- Moved: search detail and candidate schema remain in the conditional source
  reference.
- Deleted: retrieval execution prose, duplicated output prose, and redundant
  gotchas.

## Binary Evidence

| Check | Verdict | Evidence |
| --- | --- | --- |
| First-load sufficiency | pass | Normal discovery and handoff remain in todo. |
| Rights/side-effect boundary | pass | Links only; operator owns download/approval. |
| Authored file line cap | pass | Both changed `SKILL.md` files are 200 lines. |
| Eval/QA alignment | pass | Discovery, status, and no-download checks match. |
| Validation | pass | 21 focused tests and full skill-system checks passed. |
| Independent review | pass | TAS-A; all hard gates passed. |

## Residual Risk

- Public search indexing may return no suitable page even when the site has an
  unindexed sound; report `searched_no_fit` rather than claiming nonexistence.
