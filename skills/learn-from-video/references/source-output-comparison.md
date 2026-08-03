---
template_uses:
  skill-method-reference: "0.1.0"
---

# Source-Output Comparison

## Use When

Use this reference only after a candidate artifact exists.

```text
compare_source_output(frozen_eval, candidate, evidence)
  -> comparison_receipt + owner_failures + pass_or_blocked
state: reads(candidate media/code/manifests/probes/frames, frozen eval)
       writes(task-scoped comparison and repair handoff
gates: candidate_real; full_eval_run; failures_attributed
fails: render-only pass; cherry-picked frames; self-scored taste claim
```

## Inputs

Supply the frozen source-output eval, real candidate media/code, manifests,
probes, representative frames, and provenance evidence. Do not compare from a
render claim or thumbnail alone.

## Workflow

### Comparison order

1. **Integrity:** candidate file exists, decodes, has expected duration/frame
   count/dimensions, and references real inputs.
2. **Provenance:** candidate uses original/licensed substitutes and contains no
   prohibited source assets or identity.
3. **Mechanics:** inspect state continuity, topology, geometry, labels, timing,
   cue frames, parameter bounds, and deterministic behavior.
4. **Representative frames:** inspect source-target anchors and the matching
   candidate moments, including boundary and hold states.
5. **Judgment:** use independent visual/reviewer judgment for composition,
   motion readability, causal clarity, and whether the taught method remains
   recognizable after rights-safe substitution.

Never average away a hard failure. Integrity, rights, missing must-match
behavior, and unjudgeable evidence block the pass.

### Failure attribution

For every miss:

```text
failure:
  eval_check:
  source_anchor:
  expected_observation:
  candidate_observation:
  likely_owner:
  candidate_specific: yes | no
  smallest_repair:
  rerun_scope:
```

- Candidate-specific defects may use the remaining local reconstruction round.
- Reusable planning, asset, audio, render, or proof defects become a handoff to
  the existing owner.
- A stable capability with no owner becomes a Skill Creator handoff.

### Visual proof

Use contact sheets for coverage, but inspect full-resolution frames for text,
geometry, treatment, edge artifacts, and exact state. For video, include:

- final encoded contact sheet;
- source and candidate anchor table;
- boundary frames;
- hold-state frames;
- final output frame;
- media probe;
- reviewer receipt when visual match is material.

## Output Shape

```text
comparison_verdict:
  integrity: pass | fail
  rights: pass | fail
  must_match: pass | fail
  judgment: A | B | C | D
  overall: pass | blocked
  next_owner:
  rerun_rule:
```

Only judgment `A` passes. `B` is useful but requires repair.

Return `comparison_receipt`, `owner_failures`, the structured verdict, and the
smallest bounded rerun or handoff.

## Quality Gates

- The candidate decodes and matches the expected media envelope.
- Every must-match check runs against the frozen pre-generation eval.
- Rights and provenance pass independently of visual quality.
- Source/candidate anchors include boundaries, holds, and final output, with
  full-resolution inspection where exact detail matters.
- Every failure names its likely owner and smallest rerun scope; material
  judgment comes from an independent reviewer.

## Bad Output

- Passing because a render exists or one cherry-picked frame looks plausible.
- Averaging a rights, integrity, or missing must-match failure into a pass.
- Scoring taste without source/candidate anchors or a reviewer receipt.
- Rewriting the frozen eval after observing the candidate.
