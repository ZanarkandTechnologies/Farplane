---
name: visual-reasoning
description: "Turn a spatially difficult image question into a checkpointed visual workspace, verified annotations, and an evidence-grounded answer."
tier: 3
group: intelligence
source: local
template_uses:
  skill-template: "0.3.9"
allowed-tools: Read, Glob, Grep, Bash
---

# Visual Reasoning

## Context

Use this skill when a visual task is likely to fail because language cannot
keep exact entities, regions, paths, or intermediate spatial hypotheses
distinct. It externalizes those references into deterministic image overlays,
then requires the agent to inspect the rendered result before continuing.

This is analytical editing, not image generation. Preserve the source image
and every checkpoint. Generative edits may support a separate creative task,
but they are not valid localization, counting, geometry, or measurement
evidence.

## Skill Signature

```text
visual_reason(image, question, workspace?)
  -> answer + checkpointed_workspace + evidence
state:
  reads(source.png, latest.png, checkpoints/*, operations/*);
  writes(next checkpoint, matching operation receipt, latest.png)
gates:
  spatial_reference_gap_named; edit_has_reasoning_purpose;
  rendered_checkpoint_reobserved; answer_maps_to_evidence
routes: direct-answer | visual-reasoning:cv-adapter | eval | review
fails:
  decorative drawing; overwritten history; coordinates without reobservation;
  generative pixels treated as analytical truth; unsupported CV capability
```

Default ticket-owned workspace:

```text
tickets/TASK-XXXX/artifacts/visual-reasoning/<image-slug>/
  source.png
  latest.png
  checkpoints/000.png
  checkpoints/001.png
  operations/001.json
```

`latest.png` is a convenience copy. Numbered checkpoints and their operation
receipts are the canonical, immutable reasoning trail.

## Phase Boundary

This skill owns visual reference management and deterministic workspace edits.
It does not own image generation, UI screenshot judgment, or a general CV
service. Use an available deterministic CV tool only through the adapter branch
when the task needs mechanical perception that points, boxes, paths, crops, or
grids cannot supply efficiently.

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Bind the image, question, and workspace.
  - [ ] Read the first-load Todo List guardrails before creating or changing a
    workspace.
  - [ ] Use the ticket artifact path when a ticket owns the task; otherwise use
    a task-local output directory.
- [ ] 2. Inspect the source or `latest.png` and name the reference failure.
  - [ ] Use the ordinary direct-answer path when one inspection is enough.
  - [ ] Start the workspace loop only for entity tracking, dense counting,
    correspondence, topology, geometry, comparison, or spatial action grounding.
- [ ] 3. Initialize or resume one workspace for the image.
  - [ ] Never reinitialize a populated workspace or edit an old checkpoint.
  - [ ] Inspect existing operation receipts before continuing another agent's
    visual trail.
- [ ] 4. Choose the smallest purposeful primitive batch.
  - [ ] Use points for instances or waypoints, boxes for bounded regions,
    paths/arrows for continuity or direction, labels for stable identities,
    grids for systematic scans, and crops for perception-limited regions.
  - [ ] Keep coordinates normalized to `[0,1]` relative to the current image.
- [ ] 5. Render the next checkpoint with
  [scripts/visual_workspace.py](scripts/visual_workspace.py).
  - [ ] Validate the whole batch before publishing it.
  - [ ] Treat the operation JSON and resulting checkpoint as one evidence step.
- [ ] 6. Reobserve `latest.png` before reasoning further.
  - [ ] Check misplaced marks, missed entities, duplicate identities, path
    discontinuities, crop damage, and anchoring bias.
  - [ ] Revise with a new checkpoint; never silently repair an earlier one.
- [ ] 7. Use the CV-adapter branch only when a mechanical operation is needed.
  - [ ] Prefer an already available background remover, segmentation model,
    OCR engine, detector, or OpenCV-style operation; do not claim an unavailable
    tool or install a heavy dependency implicitly.
  - [ ] Preserve the tool input, result, and rendered overlay in the workspace,
    and distinguish measured output from model inference.
- [ ] 8. Stop and answer from evidence.
  - [ ] Stop when the relevant entities or path are uniquely referenced and one
    reobservation supports the answer, or report the unresolved ambiguity.
  - [ ] Name the final checkpoint and any deterministic tool receipt used.
  - [ ] For a workspace branch, return the compact receipt from `Output`; do
    not hide verification in tool logs or return only an annotated image.
  - [ ] Reapply the first-load Todo List guardrails; use [review](../review/SKILL.md)
    when the visual conclusion is material or consequential.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

Initialize and inspect:

```bash
python3 skills/visual-reasoning/scripts/visual_workspace.py init \
  --source path/to/image.png \
  --workspace tickets/TASK-XXXX/artifacts/visual-reasoning/example

python3 skills/visual-reasoning/scripts/visual_workspace.py inspect \
  --workspace tickets/TASK-XXXX/artifacts/visual-reasoning/example
```

Apply one batch from a JSON file:

```bash
python3 skills/visual-reasoning/scripts/visual_workspace.py apply \
  --workspace tickets/TASK-XXXX/artifacts/visual-reasoning/example \
  --operations path/to/operations.json
```

```json
{
  "operations": [
    {"op": "point", "at": [0.25, 0.4], "label": "candidate 1"},
    {"op": "box", "box": [0.52, 0.18, 0.76, 0.63], "label": "target"},
    {"op": "arrow", "points": [[0.25, 0.4], [0.52, 0.4]]}
  ]
}
```

## Gotchas

- Drawing is useful only when the rendered mark changes what can be tracked,
  checked, or falsified.
- A clean-looking overlay can still anchor the next inspection to a wrong
  hypothesis; recheck unmarked regions and revise in a new checkpoint.
- Cropping improves perception but removes surrounding context from the latest
  view; earlier checkpoints remain the recovery path.
- Keep authored operation-input JSON outside a new workspace until `init`
  succeeds; initialization rejects any populated workspace to protect history.
- A segmentation or detector result is evidence about that tool's output, not
  automatic proof that its class or mask matches the user's concept.
- Temporary files are working state, not final evidence. Copy the final
  checkpoint and any CV receipts into the task workspace before answering.

## Reference Map

- [Checkpoint workspace helper](scripts/visual_workspace.py) — initialize,
  apply deterministic operations, and inspect workspace lineage.
- the first-load Todo List guardrails — read before the first edit and
  reapply before returning an answer.
- [Behavior eval cases](evals/evals.json) — routing, checkpoint, reobservation,
  direct-answer, and CV-boundary cases.

## Output

For the direct-answer branch, return the answer and brief visual grounding
without creating workspace ceremony.

For every workspace or CV-adapter branch, return this compact receipt:

```text
Answer: <answer or unresolved ambiguity>
Workspace: <durable task-workspace path>
Final checkpoint: <path>
Established: <what the marks or measurement established or falsified>
Verification: <reobservation plus the relevant missed/duplicate, continuity,
correspondence, crop-context, lineage, or batch-validation check>
Tool evidence: <deterministic tool + receipt/mask/overlay, or none>
Limits: <remaining ambiguity, or none>
```

The receipt must state completed checks, not merely planned checks. Omit no
field; use `none` when a field has no applicable value.
