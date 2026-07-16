---
skill: audio-generation
date: 2026-07-15
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: tickets/TASK-0376/ticket.md#change-3-provider-neutral-audio-generation
after_ref: skills/audio-generation/SKILL.md
reasoning_basis: reviewer
proof_artifacts:
  - skills/audio-generation/evals/evals.json
  - skills/audio-generation/examples/explainer-audio-packet/example.md
  - skills/audio-generation/scripts/validate_audio_packet.py
eval_required: yes
---

# Audio Generation Skill Audit

## Change

- Before: audio direction existed, but provider execution for voice, music, and
  SFX had no local owner or common packet/receipt contract.
- After: one provider-neutral skill resolves Fish voice and ElevenLabs
  voice/music/SFX into dry-run packets or explicitly authorized execution.
- Why: provider choice and reusable parameters should not be rediscovered or
  embedded in Remotion for every content task.
- Tradeoff accepted: provider-specific details live behind conditional
  references, so a provider route incurs one deliberate extra read.

## First-Principles Reasoning

- Objective: make approved audio briefs executable without mixing creative
  direction, credentials, spend authority, and final video assembly.
- Placement logic: first-load keeps capability, consent, secret, spend, packet,
  and receipt gates; API-specific detail lives in provider references.
- Expected behavior delta: calls produce a safe packet by default, block
  unsupported pairs, and execute only with explicit authority and runtime
  readiness.
- Proof needed: config parse/secret validation, eval-query validation,
  representative packet fixtures, behavior QA, and independent review.

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Signature and seven-step todo own the normal path. |
| `reference_load_precision` | pass | Provider refs have exact route conditions. |
| `missing_context_rate` | pass | Capability, authority, consent, secret, and receipt gates stay first-load. |
| `noisy_context_rate` | pass | Endpoint detail and full example are deferred. |
| `duplicated_instruction_count` | pass | Checklist verifies rather than re-explains workflow. |
| `prompt_size_tokens` | pass | `SKILL.md` remains below the approximate 250-line limit. |
| `task_success_rate` | pass | Two isolated fresh-caller runs and exact packet/blocker validation passed. |
| `review_tas_rate` | pass | Final completion review passed skill-contract, integration-readiness, and evidence-quality at TAS-A. |
| `maintenance_locality` | pass | Generation behavior is package-local; direction and assembly stay external. |
| `composition_clarity` | pass | Inputs, outputs, state, gates, routes, and failures are explicit. |

## Proof Artifacts

- Skill-local evals, when needed: `evals/evals.json`
- Structure evals, when needed: skill-creator and skill-maintenance checklists
- Evidence reviewers: `evidence-review-rerun-02.json` passed after exact packet
  shape was fixed; `evidence-review-rerun-03.json` passed after supported-pair
  blockers, canonical example validation, and reference-free content proof were
  added.
- Validator: TASK-0376 config validator plus `check_eval_queries.py`
- Packet validator: provider/capability, packet shape, blocker behavior, and
  credential-key/value redaction with a focused unit suite
- Eval required: yes; deterministic query validation now, agent behavior QA in
  the parent ticket
- Evidence gaps: no live provider execution by ticket design

## Before Behavior

- Remotion contained a direct ElevenLabs voice recipe, and no local skill
  indexed Fish/ElevenLabs across voice, music, and SFX.

## After Behavior

- `audio-advisor` can hand approved briefs to one wrapper that defaults to dry
  run, enforces the capability matrix, preserves runtime-only secrets, and
  emits artifact-ready packets or sanitized receipts.

## Followups

- Parent ticket completion reviewer passed at TAS-A.
- Do not start a self-improve loop yet: this slice establishes the baseline
  contract, and no repeated output-quality measurements exist.
