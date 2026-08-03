---
skill: ai-video-advisor
date: 2026-08-02
change_type: material-method-augmentation
owner: TASK-0424
status: pass
review_route: reviewer
reasoning_basis: first-principles placement, two real video experiments, iterative skill evals
eval_required: yes - topology selection and evidence behavior are regression-prone
no_self_improve_reason: one bounded method augmentation has concrete experiment and eval proof; no continuing optimization Goal or canonical multi-iteration suite was requested
proof_artifacts:
  - tickets/TASK-0424/artifacts/experiment-evidence.md
  - tickets/TASK-0424/artifacts/eval-result.md
  - .farplane/evals/runs/20260802-153846-task-0424-visual-camera-control-rerun/tasks/ai_video_advisor_visual_camera_simple_single_shot_01.json
  - .farplane/evals/runs/20260802-154700-task-0424-compound-rerun-3/tasks/ai_video_advisor_visual_camera_compound_chain_01.json
---

# Visual camera control skill audit

## Before behavior

- AI Video Advisor provided generic camera prompting and narrative continuity
  guidance.
- Annotated arrows had no reusable semantic compiler or topology gate.
- One overloaded generation could absorb several independently testable camera
  states without being blocked before spend.

## After behavior

- `ai-video-advisor:visual-camera-control` is a discoverable conditional method.
- Visual marks compile into path, altitude, orientation, gaze, speed, time, and
  terminal-state semantics.
- Simple compatible moves use `single_shot`; complex or previously failed
  geometry uses `chained_maneuvers` with explicit frame handoffs.
- Every response names exact planned or created paths, observable acceptance,
  three-state adherence scores, and failed-clip retention.

## Placement

| Surface | Decision | Reason |
| --- | --- | --- |
| `ai-video-advisor` | primary owner | Owns model-native provider inputs, spend, generation topology, saved clips, and adherence evidence. |
| Resource Bank | source/example storage only | Stores source captures, annotations, prompts, and golden or failed examples; it is not an executable procedure owner. |
| `asset-advisor` | upstream handoff | Supplies missing clean identity and perspective anchors; it does not execute camera generation. |
| `video-production` | upstream artifact intent | Owns story and shot purpose, not provider camera-control execution. |
| New standalone skill | rejected | One execution method has an existing owner and does not yet justify a separate callable package. |

## Structure rubric

| Check | Verdict | Evidence |
| --- | --- | --- |
| ownership_explicit | pass | Method is declared under AI Video Advisor; other surfaces have bounded roles. |
| first_load_sufficiency | pass | `SKILL.md` names trigger, topology gate, proof state, and return schema. |
| reference_load_precision | pass | First load links the method only for arrows, maps, camera paths, landmark orbits, and multi-perspective movement. |
| missing_context_rate | pass | Packet schema names required identity, maneuver, anchor, provider, and evidence inputs. |
| noisy_context_rate | pass | Detailed compiler and examples remain in one conditional method reference. |
| duplicated_instruction_count | pass | First load owns hard gates; the reference owns the executable branch detail. |
| prompt_size_tokens | unknown | No token benchmark was run; progressive disclosure limits normal-load growth. |
| task_success_rate | pass | Both new behavior cases finish at verdict A after repairs. |
| review_tas_rate | pass | `tickets/TASK-0424/artifacts/reviewer-report.md` records TAS-A for skill-contract, integration-readiness, and evidence-quality. |
| maintenance_locality | pass | Method, example, evals, and audit stay inside the owner package. |
| composition_clarity | pass | Resource Bank, Asset Advisor, Video Production, Remotion, and AI Video Advisor roles are distinct. |

## Creator and maintenance checklist

| Item | Verdict |
| --- | --- |
| Stable reusable trigger | pass |
| Existing owner updated instead of duplicate skill | pass |
| Method-reference template truthful | pass |
| Default hard gates visible on first load | pass |
| Conditional detail progressively loaded | pass |
| Natural runnable eval rows | pass |
| Query-spoiler check | pass |
| Focused package validation | pass |
| Generated registry sync | pass |
| Supported live install | pass - repo and installed `SKILL.md` checksums match |
| Global all-skill check | deferred - unrelated existing `content-impl-plan` surface-budget violations |
| Independent reviewer | pass - overall TAS-A, no blockers |

## Follow-ups

- Promote this method to a standalone skill only after repeated independent
  callers prove that AI Video Advisor is too narrow an owner.
- Add provider-specific camera adherence comparisons as separate experiments;
  do not hard-code one provider into the method contract.
