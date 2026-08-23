---
template_id: golden-example
template_version: "0.2.0"
status: active
feature_refs:
  - FEAT-0057
consumer_scope: skills/*/examples/golden/*.md
---

# {Case title}

Use this example to calibrate invariants for one prompt-heavy or
quality-dependent branch. It is not an answer key.

## Input and context

- Request: {realistic user or caller input}
- Source context: {files, state, constraints, and known failure}
- Branch: {why this golden applies}

## Decisive workflow trace

| Node | Input state | Decisive signal or rule | Output / branch | Evidence |
| --- | --- | --- | --- | --- |
| N1 | {state} | {non-obvious signal that changes the route} | {state or branch} | {inspectable proof} |

## Accepted output

{Compact representative output. Preserve the owning skill's real output shape.}

## Why the skilled route wins

- {Decisive move -> evidence in the accepted output.}
- {Invariant or boundary -> evidence in the accepted output.}

## Tempting negative

{One plausible bad output.}

Why it fails: {specific missed signal, violated assertion, or owner boundary}.

No-skill comparison: {generic behavior and the observable loss avoided by this
workflow}.

## Transferable invariants

- {Behavior or quality property that should transfer to held-out contexts.}
- {Owner, evidence, boundary, or proof property that should transfer.}

## Non-copyable facts and wording

- {Fixture-specific names, numbers, paths, or prose that must not be reused.}
- Generate fresh wording from the current task and sources.

## Proof receipt

```yaml
golden_case: {skill}/{case}
source_refs: []
qa_refs: []
accepted_because: []
decisive_nodes: []
no_skill_comparison:
heldout_required: true
review_input: candidate + transferable_invariants + qa + heldout_context
review_excludes: planner_scratch_reasoning
```
