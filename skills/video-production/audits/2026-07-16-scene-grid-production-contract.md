---
skill: video-production
date: 2026-07-16
change_type: behavior
owner: skill-maintenance
status: pass
review_route: reviewer
before_ref: skills/video-production/SKILL.md
after_ref: skills/video-production/references/scene-grid-production.md
reasoning_basis: first_principles
proof_artifacts:
  - tickets/TASK-0383/ticket.md
  - tickets/TASK-0383/artifacts/review/completion-review.md
  - tickets/TASK-0383/artifacts/eval/workflow-eval.md
eval_required: yes
---

# Scene-Grid Production Contract Audit

## Change

- Before: a whole-video storyboard, shot list, and topology could still leave
  the exact per-provider-call review artifact and asset reuse boundary implicit.
- After: one deliberate-break scene packet maps to one normally 4–5 second
  model-native clip. The packet collocates a clean grid, annotated grid, keyed
  notes, transition/audio obligations, provider strategy, and locked assets.
- Why: short independent generation units make camera changes intentional,
  reduce continuity burden, localize repair, and give the operator a cheap
  visual approval surface before spend.
- Tradeoff accepted: more storyboard artifacts and provider calls in exchange
  for clearer human review, smaller failure domains, and deterministic assembly.

## First-Principles Reasoning

- Objective: maximize control over generated visuals while reviewing the
  smallest artifact that honestly represents the future video.
- Placement logic: `video-production` owns the reusable production contract;
  `content-impl-plan` owns the approval gate; `storyboard` creates packets;
  provider skills generate clips; Remotion assembles accepted clips and audio.
- Expected behavior delta: plans expose real images and notes before generation,
  approval locks them for reuse, and a failed scene can be repaired without
  redrawing or regenerating unchanged scenes.
- Proof needed: natural eval coverage, checklist alignment, repository skill
  validation, link validation, whitespace checks, and independent TAS-A review.

## Files

- `skills/video-production/references/scene-grid-production.md`
- `skills/video-production/SKILL.md`
- `skills/video-production/qa_checklist.md`
- `skills/video-production/evals/evals.json`
- `skills/content-impl-plan/SKILL.md`
- `skills/content-impl-plan/qa_checklist.md`
- `skills/content-impl-plan/evals/evals.json`
- `skills/storyboard/SKILL.md`
- `skills/storyboard/qa_checklist.md`
- `skills/storyboard/evals/evals.json`
- `skills/remotion/SKILL.md`
- `skills/remotion/evals/evals.json`
- `skills/video-production/references/explainer-styles/retro-low-poly-consequence/{profile.md,prompts.md,example.md}`

## Binary Rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| `first_load_sufficiency` | pass | Four owner skills carry the load condition, hard gate, and handoff. |
| `reference_load_precision` | pass | Each owner names the deliberate-scene-break branch and exact shared reference. |
| `missing_context_rate` | pass | Approval, reuse, provider mapping, and Remotion ownership remain in first load. |
| `noisy_context_rate` | pass | Full packet schema, folder shape, examples, and character placement live in one conditional reference. |
| `duplicated_instruction_count` | pass | First-load skills state distinct owner obligations; the reference owns detailed semantics. |
| `prompt_size_tokens` | pass | Content plan was compacted from 397 to 222 lines by moving conditional detail and the ticket template to one precise reference. Storyboard and video-production remain below 250. Remotion remains over 400 because its pre-existing imported upstream body plus the eval-proven stitched-scene preflight must stay first-load for the normal assembly path. |
| `maintenance_locality` | pass | Shared behavior has one primary owner at `scene-grid-production.md`. |
| `composition_clarity` | pass | Input packet, approval state, provider clip output, and Remotion master are explicit. |
| `proof_surface_fit` | pass | JSON/link/registry rules use deterministic validators; variable routing behavior uses natural evals; completion uses reviewer judgment. |
| `task_case_quality` | pass | Existing natural cases were strengthened; the visual approval gate additionally uses an artifact-producing Codex behavior test because response-only judging cannot prove image existence. |
| `anti_cheat_case_design` | pass | Eval prompts remain ordinary operator requests and query lint passes. |
| `qa_preflight_loaded` | pass | Checklist-bearing skills load their QA files before execution. |
| `qa_finish_independence` | pass | Independent completion reviewer inspected final v5 images/evidence and returned TAS-A. |
| `project_specific_context_isolation` | pass | Shared schema now uses `conditioning_strategy`; Seedance-specific mapping stays inside the collocated style example. |

## First-Load Review

```yaml
first_load_review:
  line_count_before:
    content-impl-plan: 378
    storyboard: 199
    video-production: 236
    remotion: 459
  line_count_after:
    content-impl-plan: 222
    storyboard: 225
    video-production: 244
    remotion: 526
  kept_in_skill: branch trigger, review gate, reuse gate, owner handoff, proof path
  moved_to_reference: content-plan Resource Bank/creative-lock/template detail; scene packet schema, folder layout, strategy matrix, approval semantics, character placement, examples
  deleted_as_duplicate_or_rationale: none; additions were compacted before validation
  extra_sections_kept_with_reason: existing sections unchanged
  remaining_sections_over_budget: remotion imported upstream body plus mandatory eval-proven stitched-scene preflight; compaction would hide normal-path frame/audio/failure-routing gates from the inline skill runner
  proof_surface_fit: pass
  task_case_quality: pass
  anti_cheat_case_design: pass
  qa_preflight_loaded: pass
  qa_finish_independence: pass; final independent review TAS-A
  qa_gotcha_deduplication: pass
  project_specific_context_isolation: pass
  low_value_prose_scan: pass for added lines
  verdict: pass
```

## Proof Artifacts

- Eval query lint: `python3 skills/eval/scripts/check_eval_queries.py --root .`
  passed.
- Validator: `python3 skills/skill-maintenance/scripts/check_skills.py --write`
  passed, including registry generation, surface budget, config, eval query,
  method reference, capability fixture, and 1,923 documentation-reference checks.
- Whitespace: `git diff --check` passed for the changed skill and ticket paths.
- Workflow proof: final artifact-producing visual approval behavior test pass
  plus Remotion A/pass. The former creates four real 1254×418 PNGs, verifies
  one-action/one-POV semantics, zero-gap construction, visual integrity, hashes/
  dimensions, and the false→true approval gate; the latter preserves
  final agent, judge, task, and summary artifacts under the ticket.
- Reviewer receipt: two TAS-B rounds and parent visual rejection drove semantic,
  gutter, and annotation-renderer repairs; final independent rerun returned
  TAS-A with no blockers.
- Eval required: yes; synchronized four natural fixtures, used the Codex
  agent/judge harness for Remotion, and used `agent-behavior-test` for the
  artifact-producing visual gate.
- Evidence gaps: no generated-video quality claim is part of this workflow-only
  ticket; actual provider performance remains a production-run concern.

## Before Behavior

A plan could approve a story and whole-video board without exposing the exact
grid and notes attached to each model call. Regenerating a reference image was
not explicitly distinguished from repairing a generated clip.

## After Behavior

The operator reviews the overview plus every scene-local, existing, dimension-
verified clean/annotated image grid and keyed notes. Text panels remain draft-
only. Approval locks those assets. Each packet produces one clip,
and Remotion uses observed frame counts to assemble the accepted clips with the
named transitions, imported transcript/captions, and generated audio assets.

## Followups

- Validate the contract on the next new content implementation plan rather than
  spending against the nearly exhausted TASK-0378 experiment budget.
