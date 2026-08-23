---
template_id: skill-method-reference
template_version: "0.2.0"
feature_refs:
  - FEAT-0057
consumer_scope: skill-reference
applies_to:
  - skills/*/references/*.md
---

# {Method Title}

Use this reference when {specific branch condition}. It should describe a
conditional method, subworkflow, extraction recipe, or reusable branch for one
owning skill. Do not use this template for callable skill packages; those use
`SKILL_TEMPLATE.md`.

```text
{method_function}(input, state?) -> output + evidence?
state: reads(...); writes(...)
gates: required_check; proof_or_blocker
fails: known bad behavior; ownership drift
```

## Use When

- {Trigger condition.}

## Inputs

```text
input_packet:
  required:
  optional:
  source_refs:
```

## Workflow

- [ ] **M1 — {domain verb + concrete outcome}.**
  `{input_state} -> {output_state} | {named_branch}`

  Rule: {conditional method decision that changes the route.}

  Example: `{representative input} -> {decisive signal} -> {accepted output}`

  Assert:
  - {observable intermediate or final condition}
  - {rejection or branch condition}

Repeat only for bounded method nodes actually used by this branch.

## Output Shape

```text
method_output:
  result:
  evidence:
  blockers:
```

## Bad Output

- {Anti-pattern.}
