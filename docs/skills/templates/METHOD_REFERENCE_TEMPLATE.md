---
template_id: skill-method-reference
template_version: "0.1.0"
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

1. **{Step name}.** {Action and expected intermediate result.}
2. **{Step name}.** {Action and expected intermediate result.}
3. **{Step name}.** {Action and expected intermediate result.}

## Output Shape

```text
method_output:
  result:
  evidence:
  blockers:
```

## Quality Gates

- {Gate that proves the method transformed inputs into usable behavior.}
- {Gate that prevents common drift or misuse.}

## Bad Output

- {Anti-pattern.}
