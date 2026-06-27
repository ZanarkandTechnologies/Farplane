---
template_uses:
  skill-method-reference: "0.1.0"
---

# Feature And System Specs

Use this reference when deciding whether content should become or update a
feature doc, system spec, skill reference, ticket artifact, or deletion.

```text
feature_system_decision(change) -> feature_doc | system_doc | skill_reference | ticket_artifact | delete
state: reads(docs/systems/documentation-os.md, docs/features/README.md, docs/systems/README.md, target docs); writes(selected doc or decision note)
gates: capability_boundary_clear; system_boundary_clear; proof_path_named
fails: uses a feature doc for subsystem lore; creates a system for a single local recipe
```

## Use When

- A feature doc starts carrying broad subsystem policy.
- A new capability might deserve a stable `FEAT-*` handle.
- A group of features needs a product-layer owner.
- A skill reference is starting to become canonical docs lore.

## Inputs

```text
input_packet:
  required:
    change:
  optional:
    candidate_feature:
    candidate_system:
    owner_skill:
  source_refs:
    - docs/systems/documentation-os.md
    - docs/features/README.md
    - docs/systems/README.md
```

## Workflow

1. **Test for feature shape.** Use a feature doc when the content describes one
   stable capability with behavior, owner surfaces, evidence, known limits,
   rollout, and maintenance path.
2. **Test for system shape.** Use a system spec when the content groups multiple
   capabilities, defines a product-layer boundary, explains what belongs
   elsewhere, or governs a long-lived subsystem.
3. **Test for skill-reference shape.** Use a skill reference when the content is
   an executable branch for one skill and should be loaded conditionally.
4. **Test for ticket-artifact shape.** Keep content ticket-local when it is
   planning, proof, decision context, or temporary research.
5. **Delete or fold stale lore.** Remove content that duplicates stronger truth
   or only survives because an old registry row existed.

## Output Shape

```text
feature_system_decision:
  decision:
  owner_surface:
  why_not_feature:
  why_not_system:
  proof_or_validator:
  followup:
```

## Quality Gates

- Feature docs do not become subsystem lore buckets.
- System docs do not duplicate every feature detail.
- Skill references point to system or feature docs for durable theory.

## Bad Output

- Promoting broad documentation governance into one overloaded feature.
- Creating a system doc for a one-off recipe that belongs in a skill reference.
