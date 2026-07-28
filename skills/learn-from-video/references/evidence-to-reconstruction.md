---
template_uses:
  skill-method-reference: "0.1.0"
---

# Evidence-To-Reconstruction

Use this reference after transcript and representative frames exist and before
any candidate is generated.

```text
compile_reconstruction(source_evidence, learning_goal, rights_policy)
  -> output_target + reconstruction_prompt + frozen_source_output_eval
state: reads(transcript, frames, storyboard, visible prompts/parameters/output)
       writes(task-scoped prompt and eval
gates: output_judgeable; anchors_present; rights_substitutions_named
fails: summary prompt; style adjectives without mechanics; post-hoc rubric
```

## Evidence ledger

For each relevant beat record:

| Field | Meaning |
| --- | --- |
| `anchor` | timestamp, selected frame, contact-sheet cell, or transcript line |
| `evidence_class` | transcript fact, frame fact, creator claim, inference |
| `input_state` | data, assets, parameters, scene state, or prior output |
| `operation` | visible or spoken transformation |
| `output_state` | observable intermediate/final state |
| `confidence` | high, medium, low |
| `proof_use` | prompt constraint, must-match, may-vary, reject, or context |

Do not promote low-confidence inference into a must-match check without a
separate visible output observation.

## Reconstruction prompt

Compile the prompt in this order:

1. **Job and output:** what artifact is produced, dimensions/duration/runtime,
   and who owns implementation.
2. **Original substitute content:** invented or licensed data, geometry,
   assets, narration, and audio that avoid source expression.
3. **Mechanism:** the source-taught transformation, state graph, topology,
   timing, controls, or workflow.
4. **Observable states:** required start, boundary, hold, and final states.
5. **Parameters:** named values or bounded ranges supported by evidence.
6. **Rights/negative constraints:** source identity and assets that must not
   appear.
7. **Proof outputs:** probes, representative frames, manifests, and comparison
   evidence the production owner must return.

Avoid creator/style-name prompts. Replace “make it like X” with source-anchored
mechanics and observable output.

## Frozen source-output eval

Write before generation:

```text
source_output_eval:
  target_artifact:
  source_anchors:
  must_match:
  may_vary:
  reject:
  mechanical_checks:
  judgment_checks:
  rights_checks:
  evidence_outputs:
  pass_rule:
```

Must-match checks should be boolean or coarse-tier judgeable. Examples:

- scene B frame 0 equals scene A's declared terminal state;
- every chart preserves labels, domain, final values, and topology;
- event audio begins within the declared frame tolerance;
- treatment does not move data marks or blur text.

“Looks professional” and “feels similar” are not sufficient checks.

## Output

Return the evidence ledger, reconstruction prompt, frozen eval, unresolved
evidence gaps, and production-owner requirements.
