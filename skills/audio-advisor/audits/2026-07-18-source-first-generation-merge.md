---
skill: audio-advisor
date: 2026-07-18
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: skills/audio-advisor/SKILL.md@pre-merge
after_ref: skills/audio-advisor/SKILL.md
reasoning_basis: first_principles
proof_artifacts:
  - skills/audio-advisor/evals/evals.json
  - skills/audio-advisor/qa_checklist.md
  - skills/audio-advisor/references/soundbuttonsworld.md
  - skills/audio-advisor/scripts/validate_audio_packet.py
eval_required: yes
---

# Source-First Audio And Generation Merge

## Change

- Before: `audio-advisor` planned direction and handed approved briefs to a
  separate `audio-generation` skill; common SFX had no explicit
  retrieve-before-generate workflow.
- After: `audio-advisor` owns direction, source selection, retrieval receipts,
  provider packets/execution, verification, mix handoff, and five public
  methods. The separate `audio-generation` package and active references are
  removed.
- Why: callers need one coherent cue lifecycle and should not pay to generate a
  common effect when an approved asset is faster and better.
- Tradeoff accepted: the skill has a larger first-load contract (172 -> 221
  lines), while provider and site-specific detail remains behind conditional
  references. SoundButtonsWorld is not treated as commercially cleared because
  its current terms grant personal, noncommercial access and its catalog
  includes user-uploaded material subject to takedowns.

## First-Principles Reasoning

- Objective: turn a storyboard cue into a verified audio asset and Remotion
  handoff through the shortest rights-safe route.
- Placement logic: one skill owns the full audio lifecycle; provider scripts,
  config, references, example, and validators move into the same package.
- Expected behavior delta: each cue chooses `reuse -> retrieve licensed ->
  generate`, captures provenance/rights evidence for downloads, and preserves
  explicit authority and secret-redaction gates for provider calls.
- Proof needed: package validators, surface budget, eval lint, provider unit
  tests, stale active-reference scan, source-terms grounding, and reviewer
  judgment.

## Structure Accounting

- `line_count_before`: 172
- `line_count_after`: 221
- `kept_in_skill`: trigger/signature, audio-spine planning, rights/consent,
  source-versus-generate decision, provider capability/authority gates,
  verification, output contract, and precise load conditions.
- `moved_to_reference`: SoundButtonsWorld browser/rights workflow, Fish and
  ElevenLabs parameters, and the combined packet example.
- `deleted_as_duplicate_or_rationale`: the separate downstream-skill handoff
  prose and duplicate generation todo/checklist surface.
- `extra_sections_kept_with_reason`: none beyond the current template set.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Seven-step todo covers plan, source, generate, verify, and handoff. |
| `reference_load_precision` | pass | Each source/provider/example ref has an exact branch condition. |
| `missing_context_rate` | pass | Rights, consent, authority, capability, secret, receipt, and proof gates remain first-load. |
| `noisy_context_rate` | pass | Browser steps, provider parameters, and full example are deferred. |
| `duplicated_instruction_count` | pass | One public skill owns the lifecycle; QA verifies rather than restating the full todo. |
| `prompt_size_tokens` | pass | First load remains below the approximate 250-line threshold. |
| `task_success_rate` | unknown | Eval cases are linted but no fresh agent behavior run was required in this direct update. |
| `review_tas_rate` | pass | Independent rerun passed skill-contract, integration-readiness, and evidence-quality at TAS-A. |
| `maintenance_locality` | pass | All audio acquisition/generation mechanics now live under `skills/audio-advisor/`. |
| `composition_clarity` | pass | Methods, inputs, outputs, state, routes, failures, and receipts are explicit. |

## Proof Artifacts

- Skill-local evals: five cases cover audio continuity, avatar/consent routing,
  unsafe commercial soundboard reuse, permitted source-first retrieval, and
  provider packet safety.
- Structure checks: `check_skills.py --write` passed registry, config, surface,
  eval-query, reference, template, and compilation validation.
- Focused tests: 20 packet/source-receipt/Fish/ElevenLabs executor tests passed
  after relocation, including rejection of site terms as commercial clearance
  and official Music v2 request construction.
- Source grounding: current SoundButtonsWorld terms of use, DMCA policy, and
  visible sound-page download affordance checked on 2026-07-18; current
  ElevenLabs Compose Music API and Music v2 quickstart checked before adding
  the missing local executor route.
- Reviewer receipt: initial review returned TAS-C/block because generated graph
  outputs were stale and ElevenLabs music execution was advertised but absent.
  After graph regeneration and `POST /v1/music` execution/tests, the independent
  rerun passed all hard gates at TAS-A; see
  `2026-07-18-source-first-generation-merge-review.md`.
- Evidence gaps: no live library download or paid provider call was needed to
  update the skill; creative-quality behavior remains eval/review territory.

## Before Behavior

- Audio planning stopped at a production route and a second skill had to be
  loaded to build or execute provider packets.
- Common SFX could be generated without first checking an approved existing or
  downloadable option.

## After Behavior

- One invocation can plan the cue sheet, retrieve a permitted common SFX or
  generate a bespoke one, validate the asset, record a sanitized receipt, and
  hand the exact file/timing/mix contract to Remotion.
- SoundButtonsWorld is usable as a convenient personal/noncommercial source or
  with separate item-level clearance, while commercial ambiguity blocks reuse.

## Followups

- Consider validating ElevenLabs music duration bounds (3-600 seconds) before
  paid execution; current provider errors remain an honest fallback.
