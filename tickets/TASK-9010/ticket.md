---
template_id: ticket-template
template_version: "0.2.5"
feature_refs:
  - FEAT-0022
  - FEAT-0008
ticket_id: TASK-9010
title: Add checkpointed visual reasoning workspaces
status: active
created_at: 2026-08-02T12:00:00+08:00
updated_at: 2026-08-02T13:00:00+08:00
claimed_by: codex-visual-reasoning
priority: high
---

# TASK-9010: Add checkpointed visual reasoning workspaces

## Summary

Create a reusable `visual-reasoning` skill that lets an agent reason through
deterministic edits to an image. Each image gets one ticket-artifact workspace
whose `latest.png` advances after every edit while immutable numbered
checkpoints and operation receipts preserve the full visual reasoning trail.

## Scope

- In:
  - Add a Tier 3 `visual-reasoning` skill with an explicit
    observe-mark-render-reobserve-verify loop.
  - Add a Pillow-based workspace helper for initialization, point/box/path/
    arrow/label/grid overlays, crops, latest-state inspection, and immutable
    checkpoint receipts.
  - Default workspaces to
    `tickets/TASK-XXXX/artifacts/visual-reasoning/<image-slug>/` when a ticket
    owns the task.
  - Add focused unit tests, natural behavior eval cases, skill-local QA, and a
    material skill audit.
- Out:
  - No Meta SAM, background-removal model, detector, OCR engine, or OpenCV
    dependency in the first version.
  - No generative image editing as analytical evidence.
  - No UI, daemon, MCP server, dedicated subagent, or cross-ticket visual
    workspace registry.
  - No feature/system promotion until repeated use proves the vertical family.

## Delta

```text
overall_before:
  - Agents can inspect images or generate edits, but no reusable Farplane workflow preserves visual annotations as reasoning state.
  - Image references remain linguistic or disappear into transcript context.
overall_after:
  - Each image can have one mutable latest view backed by immutable visual checkpoints and operation receipts.
  - Agents can place normalized points, boxes, paths, arrows, labels, grids, and crops, then reobserve the rendered result before answering.
why_now:
  - The supplied Thinking with Visual Primitives report identifies precise spatial reference as a reasoning bottleneck, and the operator approved a simple harness-level adaptation.
first_principles_basis:
  objective: reduce visual reference drift by externalizing spatial hypotheses into a replayable image workspace
  need: preserve what was marked, where it was marked, and what the model saw after each edit
  assumptions: deterministic overlays can approximate part of the benefit without retraining a multimodal model
  root_cause: language-only references and one-shot image inspection overload working memory in dense visual tasks
  constraints: keep source pixels recoverable; keep the first version dependency-light; never overstate overlay evidence
  first_viable_slice: one skill plus one deterministic checkpoint renderer and focused proof
  proof_or_falsification: tests prove checkpoint integrity and evals test whether agents choose and explain the workspace loop appropriately
  tradeoff: retain duplicate checkpoint images in exchange for direct inspectability and recovery
  non_goals: reproducing the paper's trained visual tokens; production CV model routing; general image editor
```

## Change Plan

```text
architecture_signatures:
  module_level:
    - skills/visual-reasoning/SKILL.md / visual_reason(image, question, workspace?) -> answer + checkpointed_workspace + evidence
    - skills/visual-reasoning/scripts/visual_workspace.py / init_workspace(source, workspace) -> checkpoint_000 + latest
    - skills/visual-reasoning/scripts/visual_workspace.py / apply_operations(workspace, operations) -> next_checkpoint + operation_receipt + latest
    - skills/visual-reasoning/scripts/visual_workspace.py / inspect_workspace(workspace) -> derived current state
  main_flow:
    - inspect source/latest -> identify reference gap -> write normalized operations -> render next checkpoint -> reobserve latest -> verify or revise -> answer with checkpoint evidence
  data_flow:
    - source image -> source.png + checkpoints/000.png -> operation JSON -> checkpoints/NNN.png + operations/NNN.json -> latest.png -> final response/evidence
  builder_freeform_boundary:
    - Rendering implementation and CLI ergonomics are builder-owned; changing immutable checkpoint semantics, normalized geometry, or analytical-versus-generative trust boundaries requires ticket revision.
```

### Change 1: Add the reusable skill contract

```text
fixes:
  - Farplane has no progressive workflow for using visual annotations as external reasoning memory.
before:
  - image creation, screenshot judgment, and video reconstruction are separate owners without analytical workspace behavior
after:
  - visual-reasoning owns when to externalize references, how to iterate, and when to stop or route a mechanical CV operation
write:
  - skills/visual-reasoning/SKILL.md
  - skills/visual-reasoning/qa_checklist.md
  - skills/visual-reasoning/evals/evals.json
  - skills/visual-reasoning/audits/2026-08-02-initial-checkpoint-workspace.md
operation:
  - keep the normal path first-load executable and route future heavy CV providers as conditional adapters
signature_or_type_impact:
  - introduces visual_reason(image, question, workspace?) as a reusable Tier 3 skill contract
routes:
  docs: skill-local package plus generated skill registry
  qa: tests + eval
  review: reviewer
qa:
  - skill structure, query-spoiler, registry, eval, and independent skill-contract review
failure_modes:
  - decorative annotations, prompt-only coordinates, hidden overwrites, or generative edits presented as measurement
```

### Change 2: Add the checkpoint workspace helper

```text
fixes:
  - agents need a deterministic way to update the current image without losing earlier visual states
before:
  - no common local helper renders normalized primitives or preserves edit receipts
after:
  - init/apply/inspect commands preserve source, numbered checkpoints, exact operation JSON, and an atomically updated latest.png
write:
  - skills/visual-reasoning/scripts/visual_workspace.py
  - skills/visual-reasoning/scripts/test_visual_workspace.py
operation:
  - use Pillow only; reject malformed/out-of-range geometry before writing; render from latest; write the next immutable checkpoint; atomically replace latest
signature_or_type_impact:
  - operation kinds are point, box, path, arrow, label, grid, and crop with normalized coordinates
routes:
  docs: no_docs beyond skill package
  qa: focused unittest
  review: reviewer
qa:
  - initialize, sequential overlay, crop, validation failure, receipt integrity, and inspect-state cases
failure_modes:
  - prior checkpoint mutation, partial latest update, coordinate overflow, invalid crop, receipt/image disagreement
```

## Done

```text
done_when:
  - The skill teaches an agent to diagnose the reference gap, create or resume one image workspace, render purposeful primitives, reobserve latest.png, and answer from checkpoint evidence.
  - The helper preserves source.png, checkpoints/000.png, every subsequent numbered checkpoint, matching operation receipts, and latest.png.
  - Point, box, path, arrow, label, grid, and crop operations accept normalized geometry and fail safely on malformed input.
  - Focused tests pass and natural eval cases are executed through the Eval owner or carry an explicit blocker.
  - Skill maintenance regenerates the canonical registry and all relevant validators pass without claiming unrelated dirty-worktree changes.
  - Independent reviewer gates reach TAS-A for skill-contract, integration-readiness, and evidence-quality.
```

## QA Strategy

```text
qa_strategy:
  proof_weight: eval + review
  critical_path:
    - initialize a workspace from a real image fixture
    - apply two overlay batches and confirm latest advances while prior hashes remain unchanged
    - crop from the current checkpoint and confirm the source and earlier checkpoints remain recoverable
    - inspect the resulting workspace and match checkpoint numbers to operation receipts
    - evaluate whether the skill selects the loop for dense spatial tasks and avoids it for simple visual questions
  checks:
    - python3 -m unittest skills/visual-reasoning/scripts/test_visual_workspace.py
    - python3 skills/eval/scripts/check_eval_queries.py --root skills/visual-reasoning
    - python3 skills/eval/scripts/run_evals.py run --harness codex --judge-harness codex --target-root . --skill visual-reasoning --label task-9010-visual-reasoning --behavior-trace --max-parallel-tasks 1
    - python3 skills/skill-maintenance/scripts/check_skills.py --write
    - farplane validate ticket tickets/TASK-9010/ticket.md --phase planning
    - farplane validate ticket tickets/TASK-9010/ticket.md --phase complete --path skills/visual-reasoning
  delegated_lanes:
    - reviewer: implementation and evidence acceptance
  review:
    - rubric: skill-contract
      required_tas: TAS-A
    - rubric: integration-readiness
      required_tas: TAS-A
    - rubric: evidence-quality
      required_tas: TAS-A
  evidence:
    - tickets/TASK-9010/artifacts/verification.md
    - .farplane/evals/runs/task-9010-visual-reasoning/
    - tickets/TASK-9010/artifacts/review/completion-review.md
  goal_advisor_inputs:
    proof_route: focused tests -> skill eval -> registry validation -> reviewer
    final_evidence: tickets/TASK-9010/artifacts/
    final_checkpoint: complete-phase validation and TAS-A completion review
  residual_risk:
    - Harness-level render-and-reobserve behavior is an adaptation, not the paper's trained interleaved token mechanism; behavioral advantage needs later ablation evidence.
    - Heavy CV adapters remain follow-up work and must earn dependencies from observed failures.
  grounding_evidence:
    - supplied Thinking with Visual Primitives report, Farplane skill system, adjacent image/visual skills, and local Pillow runtime
```

## Docs Strategy

```text
docs_strategy:
  outcome: update_docs
  doc_targets:
    - skills/visual-reasoning/SKILL.md
    - docs/skills/registry.jsonl and docs/skills/README.md through generated registry maintenance
  validation:
    - python3 skills/skill-maintenance/scripts/check_skills.py --write
```

## Links

- Visual companion: [diagrams.md](diagrams.md)
- Source report: https://github.com/mitkox/Thinking-with-Visual-Primitives/blob/main/Thinking_with_Visual_Primitives.pdf
- Placement doctrine: `docs/fundamentals/harness-engineering-doctrine.md`
- Evidence: `artifacts/verification.md`
- Completion review: `artifacts/review/completion-review.md`

## State

- Implementation: complete for the approved first slice.
- Deterministic proof: 5/5 focused tests pass; real workspace lineage and
  hashes recorded in `artifacts/verification.md`.
- Behavior proof: TAS-A for dense counting, tangled path, direct routing, and
  deterministic CV boundary; resume produced the correct append-only artifact
  trail and awaits substitute reviewer judgment after judge-process failure.
- Integration: installed through `farplane install`; generated registry
  contains `visual-reasoning`.
- Independent completion review: pass, overall TAS-A; skill-contract,
  integration-readiness, and evidence-quality each TAS-A.
- Complete-phase validation: TASK-9010 metadata, reward, completion evidence,
  and visual companion pass. The aggregate skills check remains blocked only
  by pre-existing `content-impl-plan` surface-budget debt outside this scope.

## Notes

- The operator explicitly approved implementation and delegated first-version
  detail after selecting latest-image updates with backup checkpoints.
- `plan_qa:` pass
  - Minimality: one skill, one deterministic helper, one focused test module;
    heavy CV providers, UI, service, and subagent surfaces are excluded.
  - Reuse/new-surface fit: existing image generation, visual QA, video
    understanding, and diagramming owners were inspected and do not own
    analytical visual scratchpad state.
  - Parameters: the helper exposes only workspace, source, and operation-file
    inputs; rendering defaults remain policy rather than configuration.
  - Visual companion: planning validation passed for `diagrams.md`.
  - Grounding: supplied technical report plus local skill-system and adjacent
    owner contracts.
  - Highest risk: behavior eval must prove appropriate loop selection rather
    than merely validate eval JSON; the Eval run and artifact path are now
    explicit QA gates.
