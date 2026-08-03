---
template_id: golden-example
template_version: "0.1.0"
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

## Accepted output

{Compact representative output. Preserve the owning skill's real output shape.}

## Why it passes QA

- {QA check -> evidence in the accepted output}
- {QA check -> evidence in the accepted output}

## Tempting negative

{One plausible bad output.}

Why it fails: {specific violated invariant, QA check, or owner boundary}.

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
heldout_required: true
review_input: candidate + transferable_invariants + qa + heldout_context
review_excludes: planner_scratch_reasoning
```
