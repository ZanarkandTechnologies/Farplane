---
name: {skill_name}
description: [TODO: Clear trigger/use description. This metadata decides when the skill loads.]
tier: [TODO: 1 | 2 | 3]
source: local
skill_template_version: "0.1.0"
feature_refs:
  - FEAT-XXXX
group: [TODO: required for Tier 3]
allowed-tools: {tools}
---

# {skill_title}

## Context

[TODO: Only context needed every time this skill loads: tier/system placement,
source-of-truth docs, ownership constraints, and assumptions.]

[TODO: Do not add a generic `## Job`; put ordered work in `## Todo List` as
visible task labels like `- [ ] 1. ...`, and use a specific contract section
only when it adds non-duplicated durable shape.]

[TODO: Paths in this skill are relative to this skill package. Use
`scripts/foo.py` and `references/foo.md` for nearby files.]

## Function Contract

[TODO: Keep this only when it clarifies real inputs, outputs, artifacts,
evidence, or composition. Otherwise delete this section. See
`docs/specs/harness-algebra.md`.]

`{skill_name}: Inputs -> Outputs`

Inputs:
- operator intent:
- required context:
- readable artifacts:
- optional tools:

Outputs:
- primary response or artifact:
- write set:
- evidence:

Composition:
- upstream:
- downstream:
- transitive effects:

<!-- BEGIN FARPLANE_IMPORTANT_CHECKLIST -->
## Todo List

- [ ] 1. Read required context and current artifacts.
- [ ] 2. Choose the branch.
   - [ ] 1. Default branch.
   - [ ] 2. Update/repair branch.
   - [ ] 3. Review branch.
- [ ] 3. Execute the workflow for the selected branch.
- [ ] 4. Produce or update the required artifact.
- [ ] 5. Verify with the named proof command or evidence surface.
- [ ] 6. Review against the gotchas before completion.
   - [ ] Repeatability from files alone.
   - [ ] No duplicated first-load logic.
   - [ ] Explicit proof command or blocker.
<!-- END FARPLANE_IMPORTANT_CHECKLIST -->

## Templates

- [TODO: Inline one short positive example, or link to `templates/*` /
  `prompts/*` when examples are too long.]

## Gotchas

- [TODO: Negative example or failure pattern.]
- [TODO: Negative example or failure pattern.]
- [TODO: Negative example or failure pattern.]

## Reference Map

- [TODO: `references/name.md` - read only when ...]

## Output

- [TODO: Expected artifact, type, path, or response shape.]
