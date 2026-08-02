---
title: Visual Reasoning QA Checklist
owner: visual-reasoning
status: active
kind: qa-checklist
applies_to:
  - checkpointed-visual-workspaces
  - analytical-image-annotations
---

# Visual Reasoning QA Checklist

Use this before the first workspace edit and again before returning the visual
conclusion.

```text
visual_reasoning_check(question, workspace, final_checkpoint, answer)
  -> pass | revise | blocked
```

## Checks

- [ ] `workspace-lineage`: `source.png`, `latest.png`, numbered checkpoints,
  and matching operation receipts exist; no earlier checkpoint changed.
- [ ] `purposeful-primitives`: every mark helps identify, compare, count,
  trace, measure, crop, or falsify something needed by the question.
- [ ] `normalized-geometry`: authored coordinates are within `[0,1]` and map
  to the intended content in the rendered checkpoint.
- [ ] `rendered-reobservation`: the agent inspected `latest.png` after the last
  material edit and checked for misplaced, missing, duplicated, or biasing marks.
- [ ] `claim-evidence-map`: the answer names or clearly maps to the final
  checkpoint and does not claim more precision than the overlay or tool receipt
  supports.
- [ ] `trust-boundary`: generative pixels are not used as analytical evidence;
  deterministic CV output is labeled as tool output and remains auditable.
- [ ] `direct-path-discipline`: a workspace was not created for a simple visual
  question that one inspection could answer reliably.
- [ ] `recovery`: destructive-looking operations such as crop affect only the
  new checkpoint; the source and earlier context remain recoverable.

## Verdicts

- `pass`: lineage is intact, the last checkpoint was reobserved, and the answer
  stays within the evidence.
- `revise`: the workspace can be repaired by appending another checkpoint.
- `blocked`: required source pixels, a trustworthy mechanical tool, or enough
  visual resolution are unavailable.
