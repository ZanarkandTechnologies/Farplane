---
title: Create Script Storyboard Skill
owner: script-storyboard
status: complete
kind: skill-audit
created_at: 2026-07-03
---

# Create Script Storyboard Skill

## Change

Created `script-storyboard` as a content-production planning skill. The skill
turns a creative idea, ICP, proof, or offer into a ticket-shaped script and
storyboard handoff before Remotion, video-generation, video-production, or
social-content execution.

## Why

The content system needed an implementation-plan analogue for creative work:
an artifact that binds viewer promise, narrative shape, script, storyboard,
assets, production route, and proof before agents start rendering or posting.

## Structure QA

- first_load_sufficiency: pass
- reference_load_precision: pass
- missing_context_rate: pass
- noisy_context_rate: pass
- duplicated_instruction_count: pass
- maintenance_locality: pass
- composition_clarity: pass
- qa_preflight_loaded: pass
- qa_finish_independence: pass
- task_case_quality: pass

## Skill Creator QA

- ownership_explicit: pass
- first_load_executable: pass
- template_metadata_truthful: pass
- conservative_scaffolding: pass
- proof_and_qa_match_risk: pass

## Proof

- Added `qa_checklist.md` with five runtime guardrails.
- Added `eval_task.json` with two behavior cases.
- Added `examples/remotion-proof-video/example.md` as a positive example for a
  Remotion-ready creative ticket.
- Validation command: `python3 skills/skill-maintenance/scripts/check_skills.py --write`.

## Remaining Risk

The skill has not yet been used to produce and render a live Remotion video.
The first production run should compare the generated plan against the
checklist and tighten eval cases if agents skip storyboard or proof details.
